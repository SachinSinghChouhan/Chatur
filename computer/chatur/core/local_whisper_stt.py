"""
Local Whisper STT using faster-whisper (runs fully on-device, no API key needed).
Model is downloaded automatically on first use to ~/.cache/huggingface/hub/
"""

import io
import wave
import pyaudio
import threading
from typing import Optional
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.local_whisper_stt')

# Default model: "base" is a good balance of speed vs accuracy (~300MB download).
# Options: tiny (~150MB), base (~300MB), small (~500MB), medium (~1.5GB), large (~3GB)
DEFAULT_MODEL = "base"


class LocalWhisperSTT:
    """
    Offline speech-to-text using faster-whisper.
    No internet connection or API key required after the first-time model download.
    """

    def __init__(self):
        model_size = config.get('whisper.model', DEFAULT_MODEL)
        device = config.get('whisper.device', 'cpu')          # 'cpu' or 'cuda'
        compute_type = config.get('whisper.compute_type', 'int8')  # 'int8' is fastest on CPU

        self._model = None
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._lock = threading.Lock()

        # Audio recording settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.SILENCE_THRESHOLD = 500   # RMS below this = silence
        self.SILENCE_SECONDS = 1.5     # Stop after this many seconds of silence
        self.MAX_RECORD_SECONDS = 10   # Hard cap

        logger.info(f"LocalWhisperSTT configured (model={model_size}, device={device})")

    def _load_model(self):
        """Lazy-load the Whisper model on first use."""
        if self._model is not None:
            return True
        with self._lock:
            if self._model is not None:
                return True
            try:
                from faster_whisper import WhisperModel
                logger.info(f"Loading Whisper model '{self._model_size}' — may download on first run (~300 MB for 'base')...")
                self._model = WhisperModel(
                    self._model_size,
                    device=self._device,
                    compute_type=self._compute_type,
                )
                logger.info("Whisper model loaded successfully")
                return True
            except ImportError:
                logger.error("faster-whisper not installed. Run: pip install faster-whisper")
                return False
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}", exc_info=True)
                return False

    def _rms(self, data: bytes) -> float:
        """Calculate RMS amplitude of a raw PCM chunk."""
        import audioop
        try:
            return audioop.rms(data, 2)  # 2 bytes per sample (paInt16)
        except Exception:
            return 0.0

    def _record_audio(self) -> Optional[bytes]:
        """
        Record from microphone until silence is detected or max duration reached.
        Returns WAV bytes or None on error.
        """
        try:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )

            frames = []
            silent_chunks = 0
            speaking_started = False
            max_chunks = int(self.RATE / self.CHUNK * self.MAX_RECORD_SECONDS)
            silence_chunks_needed = int(self.RATE / self.CHUNK * self.SILENCE_SECONDS)

            for _ in range(max_chunks):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
                rms = self._rms(data)

                if rms > self.SILENCE_THRESHOLD:
                    speaking_started = True
                    silent_chunks = 0
                elif speaking_started:
                    silent_chunks += 1
                    if silent_chunks >= silence_chunks_needed:
                        break  # Natural end of speech

            stream.stop_stream()
            stream.close()
            p.terminate()

            if not frames:
                return None

            # Encode as WAV in-memory
            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)  # paInt16 = 2 bytes
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            buf.seek(0)
            return buf.read()

        except Exception as e:
            logger.error(f"Audio recording error: {e}", exc_info=True)
            return None

    def _transcribe(self, wav_bytes: bytes) -> Optional[str]:
        """Transcribe WAV bytes using faster-whisper."""
        if not self._load_model():
            return None
        try:
            buf = io.BytesIO(wav_bytes)
            segments, info = self._model.transcribe(buf, beam_size=5, language=None)
            text = " ".join(seg.text for seg in segments).strip()
            logger.info(f"Whisper transcribed [{info.language}]: {text!r}")
            return text or None
        except Exception as e:
            logger.error(f"Transcription error: {e}", exc_info=True)
            return None

    def recognize_once(self) -> Optional[str]:
        """Record one utterance and return the transcribed text."""
        wav = self._record_audio()
        if not wav:
            return None
        return self._transcribe(wav)

    # Alias used by the assistant loop
    listen = recognize_once

    def recognize_with_language_detection(self) -> Optional[tuple]:
        """
        Record one utterance and return (text, language_code).
        faster-whisper auto-detects the language.
        """
        wav = self._record_audio()
        if not wav:
            return None
        if not self._load_model():
            return None
        try:
            buf = io.BytesIO(wav)
            segments, info = self._model.transcribe(buf, beam_size=5, language=None)
            text = " ".join(seg.text for seg in segments).strip()
            lang = info.language or 'en'
            logger.info(f"Whisper detected language={lang}, text={text!r}")
            return (text, lang) if text else None
        except Exception as e:
            logger.error(f"Transcription error: {e}", exc_info=True)
            return None

"""Wake word detection — openWakeWord (free, offline) with Porcupine fallback"""

import os
import threading
from typing import Callable, Optional, List, Any
from pathlib import Path

from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.wake_word')

try:
    import pyaudio
except Exception:
    pyaudio = None


# ---------------------------------------------------------------------------
# openWakeWord detector (primary — no API key, runs fully offline)
# ---------------------------------------------------------------------------

class OpenWakeWordDetector:
    """Wake word detection using openWakeWord (free, no API key required).

    Pre-trained model names (examples):
        'hey_jarvis', 'alexa', 'hey_mycroft', 'timer', 'weather'
    Full list: https://github.com/dscripka/openWakeWord#pre-trained-models
    """

    def __init__(self, on_wake_word: Callable, model_name: str = "hey_jarvis", threshold: float = 0.5):
        self.on_wake_word = on_wake_word
        self.model_name = model_name
        self.threshold = threshold
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._oww = None
        self._pa = None
        self._stream = None
        self._init_model()

    def _init_model(self):
        try:
            from openwakeword.model import Model
            self._oww = Model(wakeword_models=[self.model_name], inference_framework="onnx")
            logger.info(f"openWakeWord initialized with model: {self.model_name}")
        except Exception as e:
            logger.warning(f"openWakeWord unavailable: {e}")
            self._oww = None

    def start(self) -> bool:
        if self._oww is None or pyaudio is None:
            logger.error("Cannot start openWakeWord: dependencies missing")
            return False
        if self._running:
            return True
        try:
            self._pa = pyaudio.PyAudio()
            self._stream = self._pa.open(
                rate=16000, channels=1, format=pyaudio.paInt16,
                input=True, frames_per_buffer=1280,
            )
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
            logger.info("openWakeWord detection started")
            return True
        except Exception as e:
            logger.error(f"Failed to start openWakeWord: {e}")
            return False

    def _loop(self):
        while self._running:
            try:
                import numpy as np
                raw = self._stream.read(1280, exception_on_overflow=False)
                audio = np.frombuffer(raw, dtype=np.int16)
                prediction = self._oww.predict(audio)
                score = prediction.get(self.model_name, 0.0)
                if score >= self.threshold:
                    logger.info(f"Wake word detected! (score={score:.2f})")
                    self._oww.reset()
                    if self.on_wake_word:
                        self.on_wake_word()
            except Exception as e:
                if self._running:
                    logger.error(f"openWakeWord loop error: {e}")

    def stop(self):
        self._running = False
        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except Exception:
                pass
        if self._pa:
            try:
                self._pa.terminate()
            except Exception:
                pass
        logger.info("openWakeWord detection stopped")

    def is_running(self) -> bool:
        return self._running


# ---------------------------------------------------------------------------
# Porcupine detector (legacy fallback — requires PORCUPINE_ACCESS_KEY)
# ---------------------------------------------------------------------------

class PorcupineDetector:
    """Wake word detection using Picovoice Porcupine (fallback)."""

    def __init__(self, on_wake_word: Callable, keywords: List[str], sensitivity: float = 0.5):
        self.on_wake_word = on_wake_word
        self.keywords = keywords
        self.sensitivity = sensitivity
        self._running = False
        self._porcupine = None
        self._pa = None
        self._stream = None
        self._init()

    def _init(self):
        try:
            import pvporcupine
        except ImportError:
            logger.warning("pvporcupine not installed — Porcupine fallback unavailable")
            return

        access_key = os.getenv('PORCUPINE_ACCESS_KEY')
        if not access_key:
            logger.warning("PORCUPINE_ACCESS_KEY not set — Porcupine fallback disabled")
            return

        try:
            keyword_paths = [p for k in self.keywords if (p := self._find_ppn(k))]
            if not keyword_paths:
                logger.warning("No .ppn keyword files found for Porcupine")
                return
            self._porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=keyword_paths,
                sensitivities=[self.sensitivity] * len(keyword_paths),
            )
            logger.info(f"Porcupine initialized for: {self.keywords}")
        except Exception as e:
            logger.error(f"Porcupine init failed: {e}")

    @staticmethod
    def _find_ppn(keyword: str) -> Optional[str]:
        stem = keyword.lower().replace(' ', '_')
        base = Path(__file__).parent.parent.parent
        candidates = [
            base / 'resources' / 'wake_words' / f'{stem}_windows.ppn',
            base / 'resources' / 'wake_words' / f'{stem}.ppn',
            base / 'resources' / 'wake_words' / f'{stem}_linux.ppn',
        ]
        for p in candidates:
            if p.exists():
                return str(p)
        return None

    def start(self) -> bool:
        if self._porcupine is None or pyaudio is None:
            return False
        if self._running:
            return True
        try:
            self._pa = pyaudio.PyAudio()
            self._stream = self._pa.open(
                rate=self._porcupine.sample_rate,
                channels=1, format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._porcupine.frame_length,
            )
            self._running = True
            threading.Thread(target=self._loop, daemon=True).start()
            logger.info("Porcupine detection started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Porcupine: {e}")
            return False

    def _loop(self):
        while self._running:
            try:
                raw = self._stream.read(self._porcupine.frame_length, exception_on_overflow=False)
                idx = self._porcupine.process(raw)
                if idx >= 0:
                    logger.info("Porcupine: wake word detected")
                    if self.on_wake_word:
                        self.on_wake_word()
            except Exception as e:
                if self._running:
                    logger.error(f"Porcupine loop error: {e}")

    def stop(self):
        self._running = False
        for obj in (self._stream, self._pa):
            if obj:
                try:
                    obj.stop_stream() if hasattr(obj, 'stop_stream') else None
                    obj.close() if hasattr(obj, 'close') else obj.terminate()
                except Exception:
                    pass
        logger.info("Porcupine detection stopped")

    def is_running(self) -> bool:
        return self._running


# ---------------------------------------------------------------------------
# Public alias kept for backward compat (used in main.py)
# ---------------------------------------------------------------------------
WakeWordDetector = OpenWakeWordDetector


def create_wake_word_detector(
    on_wake_word: Callable,
    config_override: Optional[dict] = None,
) -> Optional[Any]:
    """
    Factory: tries openWakeWord first, falls back to Porcupine.

    Config keys (config.yaml  wake_word.*):
        engine:    "openwakeword" | "porcupine"   (default: "openwakeword")
        model:     openWakeWord model name         (default: "hey_jarvis")
        keyword:   Porcupine keyword               (default: "computer")
        threshold: detection threshold 0-1         (default: 0.5)
        enabled:   bool                            (default: false)
    """
    cfg = config_override or {}
    enabled = cfg.get('enabled', config.get_bool('wake_word.enabled', False))
    if not enabled:
        logger.info("Wake word detection is disabled in config")
        return None

    engine = cfg.get('engine', config.get('wake_word.engine', 'openwakeword')).lower()
    threshold = cfg.get('threshold', config.get_float('wake_word.threshold', 0.5))

    if engine == 'porcupine':
        keywords = cfg.get('keywords', [config.get('wake_word.keyword', 'computer')])
        detector = PorcupineDetector(on_wake_word, keywords, sensitivity=threshold)
        if detector._porcupine:
            return detector
        logger.warning("Porcupine unavailable, falling back to openWakeWord")

    model_name = cfg.get('model', config.get('wake_word.model', 'hey_jarvis'))
    detector = OpenWakeWordDetector(on_wake_word, model_name=model_name, threshold=threshold)
    if detector._oww:
        return detector

    logger.error("No wake word engine available (install openwakeword or configure Porcupine)")
    return None

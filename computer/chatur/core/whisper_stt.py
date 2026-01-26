"""
Alternative Speech-to-Text using OpenAI Whisper
More reliable for local microphone access
"""

import os
import io
import wave
import pyaudio
from openai import OpenAI
from chatur.utils.logger import setup_logger
from typing import Optional

logger = setup_logger('chatur.whisper_stt')

class WhisperSTT:
    """OpenAI Whisper Speech-to-Text (more reliable than Azure for local mic)"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            logger.warning("OPENAI_API_KEY not set - Whisper STT will not be available")
            self.client = None
            return
        
        self.client = OpenAI(api_key=api_key)
        
        # Audio recording settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        
        logger.info("Whisper STT engine initialized")
    
    def record_audio(self, duration_seconds: int = 5) -> Optional[bytes]:
        """
        Record audio from microphone
        
        Args:
            duration_seconds: How long to record
            
        Returns:
            Audio data as bytes or None if failed
        """
        try:
            p = pyaudio.PyAudio()
            
            # Open microphone stream
            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            logger.info(f"Recording for {duration_seconds} seconds...")
            print(f"🎤 Recording for {duration_seconds} seconds... Speak now!")
            
            frames = []
            for i in range(0, int(self.RATE / self.CHUNK * duration_seconds)):
                data = stream.read(self.CHUNK)
                frames.append(data)
            
            print("✅ Recording complete!")
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Convert to WAV format
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            
            wav_buffer.seek(0)
            return wav_buffer.read()
            
        except Exception as e:
            logger.error(f"Recording error: {e}", exc_info=True)
            print(f"❌ Microphone error: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Check Windows microphone permissions")
            print("   2. Ensure microphone is not being used by another app")
            print("   3. Try a different microphone")
            return None
    
    def recognize_once(self, duration_seconds: int = 5) -> Optional[str]:
        """
        Record audio and transcribe using Whisper
        
        Args:
            duration_seconds: How long to listen
            
        Returns:
            Recognized text or None if recognition failed
        """
        if not self.client:
            logger.error("Whisper STT not available - OPENAI_API_KEY not set")
            return None
        
        # Record audio
        audio_data = self.record_audio(duration_seconds)
        if not audio_data:
            return None
        
        try:
            # Save to temporary file (Whisper API requires a file)
            temp_file = "temp_audio.wav"
            with open(temp_file, 'wb') as f:
                f.write(audio_data)
            
            logger.info("Transcribing with Whisper...")
            print("🔄 Transcribing...")
            
            # Transcribe using Whisper
            with open(temp_file, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Can be "hi" for Hindi or None for auto-detect
                )
            
            # Clean up temp file
            os.remove(temp_file)
            
            text = transcript.text.strip()
            logger.info(f"Recognized: {text}")
            print(f"✅ Recognized: {text}")
            
            return text
            
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}", exc_info=True)
            print(f"❌ Transcription error: {e}")
            return None
    
    def recognize_with_language_detection(self, duration_seconds: int = 5) -> Optional[tuple[str, str]]:
        """
        Record and transcribe with automatic language detection
        
        Returns:
            Tuple of (recognized_text, detected_language) or None
        """
        if not self.client:
            logger.error("Whisper STT not available")
            return None
        
        # Record audio
        audio_data = self.record_audio(duration_seconds)
        if not audio_data:
            return None
        
        try:
            # Save to temporary file
            temp_file = "temp_audio.wav"
            with open(temp_file, 'wb') as f:
                f.write(audio_data)
            
            logger.info("Transcribing with language detection...")
            
            # Transcribe with auto language detection
            with open(temp_file, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                    # No language specified = auto-detect
                )
            
            # Clean up
            os.remove(temp_file)
            
            text = transcript.text.strip()
            # Whisper doesn't return detected language in API response
            # We'll detect it ourselves based on text
            language = self._detect_language(text)
            
            logger.info(f"Recognized: {text} (language: {language})")
            return (text, language)
            
        except Exception as e:
            logger.error(f"Whisper error: {e}", exc_info=True)
            return None
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on character set"""
        # Check for Hindi characters
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        if hindi_chars > len(text) * 0.3:  # If >30% Hindi chars
            return "hi"
        return "en"

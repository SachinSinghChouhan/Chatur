"""
Vosk Speech Recognition STT implementation
Offline, free, no internet required
"""

import json
import pyaudio
from vosk import Model, KaldiRecognizer
from chatur.utils.logger import setup_logger
from typing import Optional
from pathlib import Path

logger = setup_logger('chatur.vosk_stt')


class VoskSTT:
    """Vosk offline speech recognition wrapper"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize Vosk Speech Recognition
        
        Args:
            model_path: Path to Vosk model directory
                       If None, looks for 'vosk-model' in project root
        """
        try:
            # Find model path
            if model_path is None:
                # Look for model in common locations
                possible_paths = [
                    Path(__file__).parent.parent.parent / 'vosk-model',
                    Path(__file__).parent.parent.parent / 'models' / 'vosk-model-small-en-in-0.4',
                    Path('vosk-model'),
                ]
                
                for path in possible_paths:
                    if path.exists():
                        model_path = str(path)
                        break
            
            if not model_path or not Path(model_path).exists():
                logger.error("Vosk model not found. Please download from https://alphacephei.com/vosk/models")
                logger.error("Extract to project root as 'vosk-model' folder")
                self.model = None
                return
            
            logger.info(f"Loading Vosk model from {model_path}...")
            self.model = Model(model_path)
            
            # Audio settings
            self.sample_rate = 16000
            self.chunk_size = 4000
            
            logger.info("Vosk STT engine initialized (offline mode)")
            
        except Exception as e:
            logger.error(f"Failed to initialize Vosk: {e}")
            self.model = None
    
    def recognize_once(self, timeout_seconds: int = 10) -> Optional[str]:
        """
        Recognize speech from microphone using Vosk
        
        Args:
            timeout_seconds: Maximum time to wait for speech
            
        Returns:
            Recognized text or None if recognition failed
        """
        if not self.model:
            logger.error("Vosk model not loaded")
            print("❌ Vosk model not available")
            print("💡 Download from: https://alphacephei.com/vosk/models")
            print("   Extract to project root as 'vosk-model' folder")
            return None
        
        try:
            logger.info("Listening for speech...")
            print("🎤 Listening... (speak clearly)")
            
            # Create recognizer
            recognizer = KaldiRecognizer(self.model, self.sample_rate)
            recognizer.SetWords(True)
            
            # Open microphone
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            stream.start_stream()
            
            logger.info("Recording...")
            
            # Record and recognize
            frames_recorded = 0
            max_frames = int(self.sample_rate / self.chunk_size * timeout_seconds)
            
            final_result = None
            
            while frames_recorded < max_frames:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames_recorded += 1
                
                if recognizer.AcceptWaveform(data):
                    # Got a complete phrase
                    result = json.loads(recognizer.Result())
                    if result.get('text'):
                        final_result = result['text']
                        break
            
            # Get final result if nothing was captured yet
            if not final_result:
                result = json.loads(recognizer.FinalResult())
                final_result = result.get('text', '')
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            if final_result:
                logger.info(f"Recognized: {final_result}")
                print(f"✅ Recognized: {final_result}")
                return final_result
            else:
                logger.warning("No speech detected")
                print("⚠️  No speech detected")
                return None
                
        except Exception as e:
            logger.error(f"Vosk STT error: {e}", exc_info=True)
            print(f"❌ Error: {e}")
            return None
    
    def recognize_with_language_detection(self) -> Optional[tuple[str, str]]:
        """
        Recognize speech with language detection
        
        Returns:
            Tuple of (recognized_text, detected_language) or None
        """
        text = self.recognize_once()
        if text:
            # Vosk model determines language, assume English for now
            return (text, 'en')
        return None

"""
Google Speech Recognition STT implementation
Free, no API key required
"""

import speech_recognition as sr
from chatur.utils.logger import setup_logger
from typing import Optional

logger = setup_logger('chatur.google_stt')


class GoogleSTT:
    """Google Speech Recognition wrapper"""
    
    def __init__(self):
        """Initialize Google Speech Recognition"""
        try:
            self.recognizer = sr.Recognizer()
            
            # Adjust for ambient noise
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            
            logger.info("Google STT engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google STT: {e}")
            self.recognizer = None
    
    def recognize_once(self, timeout_seconds: int = 10) -> Optional[str]:
        """
        Recognize speech from microphone using Google
        
        Args:
            timeout_seconds: Maximum time to wait for speech
            
        Returns:
            Recognized text or None if recognition failed
        """
        if not self.recognizer:
            logger.error("Google STT not available")
            return None
        
        try:
            logger.info("Listening for speech...")
            print("🎤 Listening... (speak clearly)")
            
            with sr.Microphone() as source:
                # Adjust for ambient noise
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=timeout_seconds)
                
                logger.info("Processing speech...")
                print("🔄 Processing...")
                
                # Recognize using Google
                text = self.recognizer.recognize_google(audio, language='en-IN')
                
                logger.info(f"Recognized: {text}")
                print(f"✅ Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("No speech detected (timeout)")
            print("⚠️  No speech detected - timeout")
            return None
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            print("⚠️  Could not understand - please speak clearly")
            return None
            
        except sr.RequestError as e:
            logger.error(f"Google API error: {e}")
            print(f"❌ Google API error: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Google STT error: {e}", exc_info=True)
            print(f"❌ Error: {e}")
            return None
    
    def recognize_with_language_detection(self) -> Optional[tuple[str, str]]:
        """
        Recognize speech with language detection
        
        Returns:
            Tuple of (recognized_text, detected_language) or None
        """
        # Try English first
        text = self.recognize_once()
        if text:
            # Simple language detection based on characters
            hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
            language = 'hi' if hindi_chars > len(text) * 0.3 else 'en'
            return (text, language)
        
        return None

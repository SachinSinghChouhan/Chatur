"""Improved Speech-to-Text with better error handling and audio configuration"""

import os
from typing import Optional, Tuple, Callable
import azure.cognitiveservices.speech as speechsdk
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.stt')

class SpeechToText:
    """Azure Speech-to-Text wrapper with improved audio handling"""
    
    def __init__(self) -> None:
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
        
        if not speech_key:
            logger.warning("AZURE_SPEECH_KEY not set - STT will not be available")
            self.recognizer = None
            self.speech_config = None
            return
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        self.speech_config.speech_recognition_language = "en-IN"
        self.speech_config.output_format = speechsdk.OutputFormat.Detailed
        
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, 
            "8000"
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, 
            "2000"
        )
        
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        logger.info("STT engine initialized with improved settings (en-IN)")
    
    def recognize_once(self, timeout_seconds: int = 15) -> Optional[str]:
        """
        Recognize speech from microphone (single utterance)
        
        Args:
            timeout_seconds: Maximum time to wait for speech
            
        Returns:
            Recognized text or None if recognition failed
        """
        if not self.recognizer:
            logger.error("STT not available - AZURE_SPEECH_KEY not set")
            return None
        
        try:
            logger.info("Listening for speech...")
            print("🎤 Listening... (speak clearly into your microphone)")
            
            result = self.recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Recognized: {result.text}")
                return result.text
            
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech recognized - please speak louder or closer to mic")
                print("⚠️  No speech detected. Please:")
                print("   - Speak louder")
                print("   - Move closer to the microphone")
                print("   - Check Windows microphone volume settings")
                return None
            
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech recognition canceled: {cancellation.reason}")
                
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_details = cancellation.error_details
                    logger.error(f"Error details: {error_details}")
                    
                    if "401" in str(error_details) or "Unauthorized" in str(error_details):
                        print("❌ Authentication error - check your Azure Speech key")
                    elif "timeout" in str(error_details).lower():
                        print("⚠️  Timeout - no speech detected")
                        print("💡 Try: Settings → Privacy → Microphone → Allow apps to access")
                    else:
                        print(f"❌ Error: {error_details}")
                
                return None
            
        except Exception as e:
            logger.error(f"STT error: {e}", exc_info=True)
            print(f"❌ Error: {e}")
            return None
        
        return None
    
    def listen(self) -> Optional[str]:
        """Alias for recognize_once for compatibility"""
        return self.recognize_once()
    
    def recognize_with_language_detection(self) -> Optional[tuple[str, str]]:
        """
        Recognize speech with automatic language detection
        
        Returns:
            Tuple of (recognized_text, detected_language) or None
        """
        if not self.recognizer or not self.speech_config:
            logger.error("STT not available")
            return None
        
        try:
            # Create auto-detect config for English only (as per user request)
            auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=["en-IN"]
            )
            
            # Create recognizer with auto language detection
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                auto_detect_source_language_config=auto_detect_config,
                audio_config=audio_config
            )
            
            logger.info("Listening with language detection...")
            print("🎤 Listening... (English or Hindi)")
            
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # Get detected language
                detected_language = result.properties.get(
                    speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult,
                    "en-IN"
                )
                logger.info(f"Recognized: {result.text} (language: {detected_language})")
                return (result.text, detected_language)
            
            return None
            
        except Exception as e:
            logger.error(f"Language detection error: {e}", exc_info=True)
            return None
    
    def start_continuous_recognition(self, callback):
        """
        Start continuous speech recognition
        
        Args:
            callback: Function to call with recognized text
        """
        if not self.recognizer:
            logger.error("STT not available")
            return
        
        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Continuous recognition: {evt.result.text}")
                callback(evt.result.text)
        
        self.recognizer.recognized.connect(recognized_handler)
        self.recognizer.start_continuous_recognition()
        logger.info("Continuous recognition started")
    
    def stop_continuous_recognition(self):
        """Stop continuous speech recognition"""
        if self.recognizer:
            self.recognizer.stop_continuous_recognition()
            logger.info("Continuous recognition stopped")

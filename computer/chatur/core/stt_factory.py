"""
STT Engine Factory
Provides unified interface for all speech-to-text engines
"""

from typing import Optional
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.stt_factory')


class STTFactory:
    """Factory for creating STT engine instances"""
    
    @staticmethod
    def create(engine_name: Optional[str] = None):
        """
        Create an STT engine instance
        
        Args:
            engine_name: Name of engine ('google', 'whisper', 'vosk', 'azure')
                        If None, reads from config
        
        Returns:
            STT engine instance
        
        Raises:
            ValueError: If engine name is invalid
            ImportError: If engine dependencies not installed
        """
        if engine_name is None:
            engine_name = config.get('stt.engine', 'google')
        
        engine_name = engine_name.lower()
        
        logger.info(f"Creating STT engine: {engine_name}")
        
        try:
            if engine_name == 'google':
                from chatur.core.google_stt import GoogleSTT
                return GoogleSTT()
            
            elif engine_name == 'whisper':
                from chatur.core.whisper_stt import WhisperSTT
                return WhisperSTT()
            
            elif engine_name == 'vosk':
                from chatur.core.vosk_stt import VoskSTT
                return VoskSTT()
            
            elif engine_name == 'azure':
                from chatur.core.stt import SpeechToText
                return SpeechToText()
            
            else:
                raise ValueError(f"Unknown STT engine: {engine_name}")
        
        except ImportError as e:
            logger.error(f"Failed to import {engine_name} STT: {e}")
            logger.info("Attempting fallback to Google STT...")
            
            # Fallback to Google if available
            try:
                from chatur.core.google_stt import GoogleSTT
                logger.info("Using Google STT as fallback")
                return GoogleSTT()
            except ImportError:
                raise ImportError(
                    f"Could not load {engine_name} STT and fallback failed. "
                    f"Please install required dependencies."
                )
    
    @staticmethod
    def list_available_engines():
        """
        List all available STT engines
        
        Returns:
            List of available engine names
        """
        available = []
        
        # Check Google
        try:
            import speech_recognition
            available.append('google')
        except ImportError:
            pass
        
        # Check Whisper
        try:
            import openai
            available.append('whisper')
        except ImportError:
            pass
        
        # Check Vosk
        try:
            import vosk
            available.append('vosk')
        except ImportError:
            pass
        
        # Check Azure
        try:
            import azure.cognitiveservices.speech
            available.append('azure')
        except ImportError:
            pass
        
        return available
    
    @staticmethod
    def get_engine_info(engine_name: str) -> dict:
        """
        Get information about an STT engine
        
        Args:
            engine_name: Name of the engine
        
        Returns:
            Dictionary with engine information
        """
        engines = {
            'google': {
                'name': 'Google Speech Recognition',
                'requires_internet': True,
                'requires_api_key': False,
                'cost': 'Free (limited)',
                'accuracy': 'High',
                'languages': ['en-US', 'en-IN', 'en-GB'],
            },
            'whisper': {
                'name': 'OpenAI Whisper',
                'requires_internet': True,
                'requires_api_key': True,
                'cost': 'Paid',
                'accuracy': 'Very High',
                'languages': ['en', 'multilingual'],
            },
            'vosk': {
                'name': 'Vosk Offline STT',
                'requires_internet': False,
                'requires_api_key': False,
                'cost': 'Free',
                'accuracy': 'Medium',
                'languages': ['en-US'],
            },
            'azure': {
                'name': 'Azure Speech Services',
                'requires_internet': True,
                'requires_api_key': True,
                'cost': 'Paid',
                'accuracy': 'Very High',
                'languages': ['en-US', 'en-IN', 'en-GB'],
            },
        }
        
        return engines.get(engine_name.lower(), {})

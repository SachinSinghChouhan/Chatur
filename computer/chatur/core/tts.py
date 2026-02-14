"""Text-to-Speech engine with Hindi transliteration fallback"""

from typing import Optional, List
import pyttsx3
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.tts')

class TextToSpeech:
    """Text-to-Speech wrapper using pyttsx3"""
    
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        
        voices = self.engine.getProperty('voices')
        self.hindi_voice: Optional[str] = None
        
        for voice in voices:
            if 'hindi' in voice.name.lower() or 'hemant' in voice.name.lower() or 'kalpana' in voice.name.lower():
                self.hindi_voice = voice.id
                break
        
        if self.hindi_voice:
            logger.info("TTS engine initialized with Hindi voice support")
        else:
            logger.info("TTS engine initialized (Hindi voice not available - will use transliteration)")
        
        self.engine.setProperty('rate', config.tts_rate)
        self.engine.setProperty('volume', config.tts_volume)
    
    def _transliterate_hindi(self, text: str) -> str:
        """Convert Devanagari to Roman script for English TTS"""
        transliteration_map: dict = {
            'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
            'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
            'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
            'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
            'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
            'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va', 'श': 'sha',
            'ष': 'sha', 'स': 'sa', 'ह': 'ha',
            'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo',
            'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'n', 'ः': 'h',
            '्': '', 'ँ': 'n'
        }
        
        result: List[str] = []
        for char in text:
            if char in transliteration_map:
                result.append(transliteration_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    def speak(self, text: str, language: str = 'en') -> None:
        """Speak text using TTS"""
        try:
            safe_text = text.encode('ascii', 'replace').decode('ascii')
            logger.info(f"Speaking: {safe_text} (language: {language})")
            
            if language == 'hi' and not self.hindi_voice:
                has_devanagari = any('\u0900' <= char <= '\u097F' for char in text)
                if has_devanagari:
                    text = self._transliterate_hindi(text)
                    logger.info(f"Transliterated to: {text}")
            
            if language == 'hi' and self.hindi_voice:
                self.engine.setProperty('voice', self.hindi_voice)
            else:
                voices = self.engine.getProperty('voices')
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
            
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def speak_async(self, text: str, language: str = 'en') -> None:
        """Speak text asynchronously (non-blocking)"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text, language))
        thread.daemon = True
        thread.start()

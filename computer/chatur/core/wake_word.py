"""Wake word detection using Picovoice Porcupine"""

import os
import threading
from typing import Callable, Optional, List
from pathlib import Path
import pvporcupine
import pyaudio
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.wake_word')


class WakeWordDetector:
    """Wake word detection using Porcupine"""
    
    def __init__(
        self,
        on_wake_word: Callable,
        keywords: Optional[List[str]] = None,
        sensitivity: float = 0.5
    ):
        """
        Initialize wake word detector
        
        Args:
            on_wake_word: Callback function to call when wake word is detected
            keywords: List of wake words to detect (default: ['computer'])
            sensitivity: Detection sensitivity (0.0 to 1.0, lower is more sensitive)
        """
        self.on_wake_word = on_wake_word
        self.keywords = keywords or ['computer']
        self.sensitivity = sensitivity
        
        self.porcupine: Optional[pvporcupine.Porcupine] = None
        self.audio_stream: Optional[pyAudio.PyAudio] = None
        self.stream: Optional[pvporcupine._onnxruntime.OrtIO] = None
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        self._init_porcupine()
    
    def _init_porcupine(self) -> None:
        """Initialize Porcupine engine"""
        try:
            access_key = os.getenv('PORCUPINE_ACCESS_KEY')
            if not access_key:
                logger.warning("PORCUPINE_ACCESS_KEY not set - wake word detection disabled")
                return
            
            keyword_paths = []
            for keyword in self.keywords:
                keyword_path = self._get_keyword_path(keyword)
                if keyword_path:
                    keyword_paths.append(keyword_path)
            
            if not keyword_paths:
                logger.warning("No valid keyword paths found - wake word disabled")
                return
            
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=keyword_paths,
                sensitivities=[self.sensitivity]
            )
            
            logger.info(f"Wake word detector initialized for: {self.keywords}")
            
        except pvporcupine.PorcupineInvalidArgumentError as e:
            logger.error(f"Invalid arguments for Porcupine: {e}")
        except pvporcupine.PorcupineActivationError as e:
            logger.error(f"Porcupine activation error: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize wake word detector: {e}")
    
    def _get_keyword_path(self, keyword: str) -> Optional[str]:
        """Get the path to the keyword .ppn file"""
        keyword_lower = keyword.lower().replace(' ', '_')
        
        base_dir = Path(__file__).parent.parent.parent
        
        search_paths = [
            base_dir / 'resources' / 'wake_words' / f'{keyword_lower}_windows.ppn',
            base_dir / 'resources' / 'wake_words' / f'{keyword_lower}.ppn',
            base_dir / 'resources' / 'wake_words' / f'{keyword_lower}_linux.ppn',
            base_dir / 'config' / 'wake_words' / f'{keyword_lower}_windows.ppn',
        ]
        
        for path in search_paths:
            if path.exists():
                logger.info(f"Found keyword file: {path}")
                return str(path)
        
        logger.warning(f"Keyword file not found for: {keyword}")
        return None
    
    def start(self) -> bool:
        """Start listening for wake word"""
        if not self.porcupine:
            logger.error("Cannot start - Porcupine not initialized")
            return False
        
        if self._running:
            logger.warning("Wake word detector already running")
            return True
        
        try:
            self.audio_stream = pyaudio.PyAudio()
            
            self.stream = self.audio_stream.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
                stream_callback=self._audio_callback
            )
            
            self._running = True
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()
            
            logger.info("Wake word detection started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start wake word detection: {e}")
            return False
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio stream callback - called by PyAudio"""
        if not self._running:
            return (None, pyaudio.paComplete)
        
        try:
            keyword_index = self.porcupine.process(in_data)
            
            if keyword_index >= 0:
                logger.info(f"Wake word detected! (keyword index: {keyword_index})")
                if self.on_wake_word:
                    self.on_wake_word()
                    
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
        
        return (None, pyaudio.paContinue)
    
    def _listen_loop(self):
        """Main listening loop (runs in separate thread)"""
        logger.info("Wake word listening thread started")
        
        while self._running:
            if self.stream and self.stream.is_active():
                pass
            else:
                break
        
        logger.info("Wake word listening thread stopped")
    
    def stop(self) -> None:
        """Stop listening for wake word"""
        self._running = False
        
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error stopping stream: {e}")
            self.stream = None
        
        if self.audio_stream:
            try:
                self.audio_stream.terminate()
            except Exception as e:
                logger.error(f"Error terminating audio: {e}")
            self.audio_stream = None
        
        logger.info("Wake word detection stopped")
    
    def is_running(self) -> bool:
        """Check if wake word detection is running"""
        return self._running


class BuiltInKeywords:
    """Built-in Porcupine keywords that don't require custom .ppn files"""
    
    ALEXA = "alexa"
    AMAZON = "amazon"
    COMPUTER = "computer"
    BLUEBERRY = "blueberry"
    BUMBLEBEE = "bumblebee"
    CORNFLOWER = "cornflower"
    GRASSHOPPER = "grasshopper"
    HEY_GOOGLE = "hey google"
    HEY_SIRI = "hey siri"
    JARVIS = "jarvis"
    OK_GOOGLE = "ok google"
    PICOVOICE = "picovoice"
    PORCUPINE = "porcupine"
    TERMINATOR = "terminator"
    
    @classmethod
    def all(cls) -> List[str]:
        """Get all built-in keywords"""
        return [
            cls.ALEXA, cls.AMAZON, cls.COMPUTER, cls.BLUEBERRY,
            cls.BUMBLEBEE, cls.CORNFLOWER, cls.GRASSHOPPER,
            cls.HEY_GOOGLE, cls.HEY_SIRI, cls.JARVIS, cls.OK_GOOGLE,
            cls.PICOVOICE, cls.PORCUPINE, cls.TERMINATOR
        ]


def create_wake_word_detector(
    on_wake_word: Callable,
    config_override: Optional[dict] = None
) -> Optional[WakeWordDetector]:
    """
    Factory function to create wake word detector from config
    
    Args:
        on_wake_word: Callback function
        config_override: Optional config dict to override defaults
        
    Returns:
        WakeWordDetector instance or None if disabled
    """
    cfg = config_override or {}
    
    enabled = cfg.get('enabled', config.get_bool('wake_word.enabled', False))
    if not enabled:
        logger.info("Wake word detection is disabled in config")
        return None
    
    keywords = cfg.get('keywords', [config.get('wake_word.keyword', 'computer')])
    sensitivity = cfg.get('sensitivity', config.get_float('wake_word.sensitivity', 0.5))
    
    return WakeWordDetector(
        on_wake_word=on_wake_word,
        keywords=keywords,
        sensitivity=sensitivity
    )

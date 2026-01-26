"""Configuration management"""

import yaml
from pathlib import Path
from typing import Any, List
import os
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.config')

class Config:
    """Configuration loader with singleton pattern"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = None):
        if self._initialized:
            return
            
        if config_path is None:
            # Default to config/config.yaml relative to project root
            config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
        
        try:
            with open(config_path, encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")
            self._config = {}
        
        self._initialized = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer"""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get configuration value as float"""
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        return bool(value)
    
    def get_list(self, key: str, default: List = None) -> List:
        """Get configuration value as list"""
        value = self.get(key, default or [])
        if isinstance(value, list):
            return value
        return default or []
    
    # Convenience properties
    @property
    def default_browser(self) -> str:
        return self.get('browser.default', 'brave')
    
    @property
    def scheduler_interval(self) -> int:
        return self.get_int('scheduler.check_interval_seconds', 30)
    
    @property
    def reminder_window(self) -> int:
        return self.get_int('scheduler.reminder_window_seconds', 30)
    
    @property
    def tts_rate(self) -> int:
        return self.get_int('tts.rate', 150)
    
    @property
    def tts_volume(self) -> float:
        return self.get_float('tts.volume', 0.9)
    
    @property
    def openai_model(self) -> str:
        return self.get('openai.model', 'gpt-3.5-turbo')
    
    @property
    def openai_max_tokens(self) -> int:
        return self.get_int('openai.max_tokens', 150)
    
    @property
    def recognized_apps(self) -> List[str]:
        return self.get_list('app_launch.recognized_apps', 
                           ['brave', 'chrome', 'firefox', 'edge', 'calculator', 
                            'notepad', 'gmail', 'explorer', 'whatsapp', 'spotify'])
    
    @property
    def file_search_locations(self) -> List[str]:
        return self.get_list('file_search.search_locations',
                           ['Desktop', 'Documents', 'Downloads', 'C:\\', 'D:\\', '~'])
    
    @property
    def supported_file_extensions(self) -> List[str]:
        return self.get_list('file_search.supported_extensions',
                           ['pdf', 'docx', 'doc', 'xlsx', 'txt', 'jpg', 'png'])
    
    @property
    def supported_tlds(self) -> List[str]:
        return self.get_list('url_detection.supported_tlds',
                           ['com', 'org', 'net', 'in', 'io', 'co', 'edu', 'gov'])
    
    @property
    def hindi_char_threshold(self) -> float:
        return self.get_float('language.hindi_char_threshold', 0.3)


# Global config instance
config = Config()

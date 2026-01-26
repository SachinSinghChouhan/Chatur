"""Script to recreate all empty files"""

import os
from pathlib import Path

# Change to computer directory
os.chdir(r'd:\protocol\computer')

# Database initialization
init_db_content = '''"""Database initialization module"""

import sqlite3
from pathlib import Path
import os

DB_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'computer.db'

def init_database():
    """Initialize database with schema and default data"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript(\'''
        -- Reminders
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            scheduled_time DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            triggered BOOLEAN DEFAULT 0,
            language VARCHAR(10) DEFAULT 'en',
            UNIQUE(text, scheduled_time)
        );
        CREATE INDEX IF NOT EXISTS idx_reminders_scheduled 
        ON reminders(scheduled_time, triggered);
        
        -- Timers
        CREATE TABLE IF NOT EXISTS timers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            duration_seconds INTEGER NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            completed BOOLEAN DEFAULT 0,
            cancelled BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_timers_end_time 
        ON timers(end_time, completed);
        
        -- Notes
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            language VARCHAR(10) DEFAULT 'en',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_notes_key ON notes(key);
        
        -- Apps
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            display_name TEXT NOT NULL,
            path TEXT NOT NULL,
            app_type VARCHAR(20) DEFAULT 'exe',
            aliases TEXT,
            is_default BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_apps_name ON apps(name);
        
        -- Conversation History
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            assistant_response TEXT NOT NULL,
            intent_type VARCHAR(50),
            language VARCHAR(10),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_conversation_timestamp 
        ON conversation_history(timestamp DESC);
        
        -- Config
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    \''')
    
    # Insert default apps
    default_apps = [
        ('chrome', 'Google Chrome', 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe', 'exe', 'browser,google', 1),
        ('gmail', 'Gmail', 'https://mail.google.com', 'url', 'email,mail', 1),
        ('calculator', 'Calculator', 'calc.exe', 'exe', 'calc', 1),
        ('notepad', 'Notepad', 'notepad.exe', 'exe', 'text,editor', 1),
        ('explorer', 'File Explorer', 'explorer.exe', 'exe', 'files,folder', 1),
    ]
    
    cursor.executemany(\'''
        INSERT OR IGNORE INTO apps (name, display_name, path, app_type, aliases, is_default)
        VALUES (?, ?, ?, ?, ?, ?)
    \''', default_apps)
    
    # Insert default config
    default_config = [
        ('wake_word_sensitivity', '0.5'),
        ('tts_rate', '150'),
        ('tts_volume', '0.9'),
        ('language_preference', 'en'),
        ('azure_region', 'eastus'),
        ('reminder_check_interval', '30'),
        ('max_conversation_history', '100'),
    ]
    
    cursor.executemany(\'''
        INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)
    \''', default_config)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == '__main__':
    init_database()
'''

# Write init_db.py
with open('chatur/storage/init_db.py', 'w', encoding='utf-8') as f:
    f.write(init_db_content)

print("Created: chatur/storage/init_db.py")

# Config utility
config_content = '''"""Configuration management"""

import yaml
from pathlib import Path
from typing import Any
import os

class Config:
    """Configuration loader"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to config/config.yaml relative to project root
            config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
        
        with open(config_path) as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
'''

with open('chatur/utils/config.py', 'w', encoding='utf-8') as f:
    f.write(config_content)

print("Created: chatur/utils/config.py")

# TTS
tts_content = '''"""Text-to-Speech module using pyttsx3"""

import pyttsx3
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.tts')

class TextToSpeech:
    """Text-to-Speech engine wrapper"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.voices = self.engine.getProperty('voices')
        logger.info("TTS engine initialized")
    
    def _get_voice_for_language(self, language: str) -> str:
        """Select appropriate voice based on language"""
        for voice in self.voices:
            if language == 'hi' and 'hindi' in voice.name.lower():
                return voice.id
            elif language == 'en' and 'english' in voice.name.lower():
                return voice.id
        return self.voices[0].id  # Default voice
    
    def speak(self, text: str, language: str = 'en'):
        """Speak text in specified language"""
        try:
            voice_id = self._get_voice_for_language(language)
            self.engine.setProperty('voice', voice_id)
            logger.info(f"Speaking: {text} (language: {language})")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def speak_async(self, text: str, language: str = 'en'):
        """Speak text asynchronously"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text, language))
        thread.start()
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
        except Exception as e:
            logger.error(f"Error stopping TTS: {e}")
'''

with open('chatur/core/tts.py', 'w', encoding='utf-8') as f:
    f.write(tts_content)

print("Created: chatur/core/tts.py")

print("\\nAll files recreated successfully!")

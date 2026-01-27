"""Database initialization module"""

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
    cursor.executescript('''
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
            session_id TEXT,
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
    ''')
    
    # Insert default apps
    default_apps = [
        ('brave', 'Brave Browser', 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe', 'exe', 'browser,brave', 1),
        ('chrome', 'Google Chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'exe', 'browser,google', 1),
        ('firefox', 'Mozilla Firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe', 'exe', 'browser,mozilla', 1),
        ('edge', 'Microsoft Edge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', 'exe', 'browser,microsoft', 1),
        ('gmail', 'Gmail', 'https://mail.google.com', 'url', 'email,mail', 1),
        ('calculator', 'Calculator', 'calc.exe', 'exe', 'calc', 1),
        ('notepad', 'Notepad', 'notepad.exe', 'exe', 'text,editor', 1),
        ('explorer', 'File Explorer', 'explorer.exe', 'exe', 'files,folder', 1),
        ('whatsapp', 'WhatsApp', 'C:\\Users\\' + os.getenv('USERNAME', 'User') + '\\AppData\\Local\\WhatsApp\\WhatsApp.exe', 'exe', 'chat,messaging', 1),
        ('spotify', 'Spotify', 'C:\\Users\\' + os.getenv('USERNAME', 'User') + '\\AppData\\Roaming\\Spotify\\Spotify.exe', 'exe', 'music,audio', 1),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO apps (name, display_name, path, app_type, aliases, is_default)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', default_apps)
    
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
    
    cursor.executemany('''
        INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)
    ''', default_config)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == '__main__':
    init_database()

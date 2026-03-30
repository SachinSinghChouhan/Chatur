"""Database initialization module"""

import sqlite3
from pathlib import Path
from chatur.utils.platform import get_app_data_dir, get_default_apps

DB_PATH = get_app_data_dir() / 'computer.db'

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

    # Insert platform-specific default apps
    cursor.executemany('''
        INSERT OR IGNORE INTO apps (name, display_name, path, app_type, aliases, is_default)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', get_default_apps())

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

# Computer Voice Assistant - Database Schema

## Database Technology

**SQLite 3** - Local, serverless, zero-configuration database

**Location:** `%APPDATA%/Computer/computer.db`

---

## Schema Design

### 1. Reminders Table

Stores user-created reminders with scheduling information.

```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,                    -- Reminder message
    scheduled_time DATETIME NOT NULL,      -- When to trigger (ISO 8601)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    triggered BOOLEAN DEFAULT 0,           -- 0 = pending, 1 = triggered
    language VARCHAR(10) DEFAULT 'en',     -- 'en', 'hi', 'hinglish'
    UNIQUE(text, scheduled_time)           -- Prevent duplicates
);

CREATE INDEX idx_reminders_scheduled ON reminders(scheduled_time, triggered);
```

**Sample Data:**
```sql
INSERT INTO reminders (text, scheduled_time, language) 
VALUES ('Call mom', '2026-01-22 17:00:00', 'en');
```

---

### 2. Timers Table

Stores active countdown timers.

```sql
CREATE TABLE timers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT,                            -- Optional timer label
    duration_seconds INTEGER NOT NULL,     -- Total duration
    start_time DATETIME NOT NULL,          -- When timer started
    end_time DATETIME NOT NULL,            -- When timer should end
    completed BOOLEAN DEFAULT 0,           -- 0 = active, 1 = completed
    cancelled BOOLEAN DEFAULT 0,           -- 0 = running, 1 = cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timers_end_time ON timers(end_time, completed);
```

**Sample Data:**
```sql
INSERT INTO timers (label, duration_seconds, start_time, end_time) 
VALUES ('Tea timer', 300, '2026-01-22 11:00:00', '2026-01-22 11:05:00');
```

---

### 3. Notes Table

Stores simple key-value facts and notes.

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,              -- Searchable key (e.g., "favorite_color")
    value TEXT NOT NULL,                   -- Note content
    language VARCHAR(10) DEFAULT 'en',     -- Language of the note
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notes_key ON notes(key);
```

**Sample Data:**
```sql
INSERT INTO notes (key, value, language) 
VALUES ('favorite_color', 'blue', 'en');

INSERT INTO notes (key, value, language) 
VALUES ('birthday', '15 January', 'hi');
```

---

### 4. Apps Table

Stores registered applications for voice launching.

```sql
CREATE TABLE apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,             -- App name (e.g., "chrome", "gmail")
    display_name TEXT NOT NULL,            -- Display name (e.g., "Google Chrome")
    path TEXT NOT NULL,                    -- Executable path or URL
    app_type VARCHAR(20) DEFAULT 'exe',    -- 'exe', 'url', 'uwp'
    aliases TEXT,                          -- Comma-separated aliases (e.g., "browser,google")
    is_default BOOLEAN DEFAULT 0,          -- 1 = pre-installed, 0 = user-added
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_apps_name ON apps(name);
```

**Sample Data:**
```sql
-- Pre-installed apps
INSERT INTO apps (name, display_name, path, app_type, aliases, is_default) VALUES
('chrome', 'Google Chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'exe', 'browser,google', 1),
('gmail', 'Gmail', 'https://mail.google.com', 'url', 'email,mail', 1),
('calculator', 'Calculator', 'calc.exe', 'exe', 'calc', 1),
('notepad', 'Notepad', 'notepad.exe', 'exe', 'text,editor', 1),
('explorer', 'File Explorer', 'explorer.exe', 'exe', 'files,folder', 1);
```

---

### 5. Conversation History Table

Stores recent conversation context for better responses.

```sql
CREATE TABLE conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT NOT NULL,              -- User's command
    assistant_response TEXT NOT NULL,      -- Assistant's response
    intent_type VARCHAR(50),               -- Intent classification
    language VARCHAR(10),                  -- Detected language
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_timestamp ON conversation_history(timestamp DESC);
```

**Retention Policy:** Keep last 100 conversations, auto-delete older ones.

---

### 6. Config Table

Stores application configuration settings.

```sql
CREATE TABLE config (
    key TEXT PRIMARY KEY,                  -- Config key
    value TEXT NOT NULL,                   -- Config value (JSON or plain text)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```sql
INSERT INTO config (key, value) VALUES
('wake_word_sensitivity', '0.5'),
('tts_rate', '150'),
('tts_volume', '0.9'),
('language_preference', 'en'),
('azure_region', 'eastus'),
('reminder_check_interval', '30'),
('max_conversation_history', '100');
```

---

## Database Initialization Script

```python
# storage/init_db.py

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
        ('chrome', 'Google Chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'exe', 'browser,google', 1),
        ('gmail', 'Gmail', 'https://mail.google.com', 'url', 'email,mail', 1),
        ('calculator', 'Calculator', 'calc.exe', 'exe', 'calc', 1),
        ('notepad', 'Notepad', 'notepad.exe', 'exe', 'text,editor', 1),
        ('explorer', 'File Explorer', 'explorer.exe', 'exe', 'files,folder', 1),
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
```

---

## Data Access Layer (Repository Pattern)

### Base Repository

```python
# storage/repository.py

from typing import List, Optional, Any
import sqlite3
from pathlib import Path
import os

DB_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'computer.db'

class BaseRepository:
    def __init__(self):
        self.db_path = DB_PATH
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def fetchall(self, query: str, params: tuple = ()) -> List[dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
```

### Reminder Repository

```python
# storage/reminder_repository.py

from datetime import datetime
from typing import List, Optional
from .repository import BaseRepository

class ReminderRepository(BaseRepository):
    def create(self, text: str, scheduled_time: datetime, language: str = 'en') -> int:
        query = '''
            INSERT INTO reminders (text, scheduled_time, language)
            VALUES (?, ?, ?)
        '''
        cursor = self.execute(query, (text, scheduled_time.isoformat(), language))
        return cursor.lastrowid
    
    def get_pending(self) -> List[dict]:
        query = '''
            SELECT * FROM reminders 
            WHERE triggered = 0 AND scheduled_time <= datetime('now')
            ORDER BY scheduled_time ASC
        '''
        return self.fetchall(query)
    
    def mark_triggered(self, reminder_id: int) -> None:
        query = 'UPDATE reminders SET triggered = 1 WHERE id = ?'
        self.execute(query, (reminder_id,))
    
    def delete(self, reminder_id: int) -> None:
        query = 'DELETE FROM reminders WHERE id = ?'
        self.execute(query, (reminder_id,))
```

---

## Database Backup Strategy

### Auto-Backup on Startup

```python
# storage/backup.py

import shutil
from datetime import datetime
from pathlib import Path

def backup_database(db_path: Path) -> None:
    """Create timestamped backup of database"""
    if not db_path.exists():
        return
    
    backup_dir = db_path.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f'chatur_backup_{timestamp}.db'
    
    shutil.copy2(db_path, backup_path)
    
    # Keep only last 7 backups
    backups = sorted(backup_dir.glob('chatur_backup_*.db'))
    for old_backup in backups[:-7]:
        old_backup.unlink()
```

---

## Migration Strategy

For future schema changes, use simple migration scripts:

```python
# storage/migrations/001_add_priority_to_reminders.py

def migrate(conn):
    conn.execute('''
        ALTER TABLE reminders 
        ADD COLUMN priority INTEGER DEFAULT 0
    ''')
```

---

## Performance Optimization

### Indexes
- All foreign keys indexed
- Timestamp columns indexed for range queries
- Text search columns indexed

### Query Optimization
- Use prepared statements (parameterized queries)
- Limit conversation history to last 100 entries
- Periodic VACUUM to reclaim space

### Connection Pooling
Not needed for SQLite (single-user, local file)

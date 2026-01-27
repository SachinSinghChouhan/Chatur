# Computer Voice Assistant - File Structure

## Project Root Structure

```
chatur/
├── chatur/                      # Main package
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── core/                    # Core components
│   │   ├── __init__.py
│   │   ├── wake_word.py         # Porcupine wake word detection
│   │   ├── stt.py               # Azure Speech-to-Text
│   │   ├── tts.py               # pyttsx3 Text-to-Speech
│   │   └── llm.py               # OpenAI intent classification
│   ├── handlers/                # Action handlers
│   │   ├── __init__.py
│   │   ├── base.py              # Base handler interface
│   │   ├── reminder.py          # Reminder handler
│   │   ├── timer.py             # Timer handler
│   │   ├── notes.py             # Notes handler
│   │   ├── qa.py                # Question answering handler
│   │   ├── app_launcher.py      # App launching handler
│   │   └── media_control.py     # Spotify/media control handler
│   ├── storage/                 # Database layer
│   │   ├── __init__.py
│   │   ├── init_db.py           # Database initialization
│   │   ├── repository.py        # Base repository
│   │   ├── reminder_repository.py
│   │   ├── timer_repository.py
│   │   ├── notes_repository.py
│   │   ├── app_repository.py
│   │   ├── conversation_repository.py
│   │   ├── config_repository.py
│   │   └── backup.py            # Database backup utilities
│   ├── service/                 # Service management
│   │   ├── __init__.py
│   │   ├── manager.py           # Main service orchestrator
│   │   ├── tray.py              # System tray interface
│   │   └── scheduler.py         # Background task scheduler
│   ├── utils/                   # Utilities
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── logger.py            # Logging setup
│   │   ├── audio.py             # Audio utilities
│   │   └── time_parser.py       # Natural language time parsing
│   └── models/                  # Data models
│       ├── __init__.py
│       ├── intent.py            # Intent data classes
│       ├── reminder.py          # Reminder data classes
│       ├── timer.py             # Timer data classes
│       └── app.py               # App data classes
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_wake_word.py
│   ├── test_stt.py
│   ├── test_handlers.py
│   └── test_storage.py
├── resources/                   # Static resources
│   ├── icons/
│   │   ├── tray_idle.ico
│   │   ├── tray_listening.ico
│   │   └── tray_processing.ico
│   ├── wake_words/
│   │   └── chatur_windows.ppn  # Porcupine wake word model
│   └── prompts/
│       └── intent_classifier.txt
├── config/                      # Configuration files
│   ├── config.yaml              # Main config (template)
│   └── .env.example             # Environment variables template
├── scripts/                     # Utility scripts
│   ├── install.bat              # Windows installation script
│   ├── uninstall.bat            # Uninstallation script
│   └── setup_autostart.py       # Auto-start configuration
├── docs/                        # Documentation
│   ├── README.md
│   ├── SETUP.md
│   └── API_KEYS.md
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── pyproject.toml               # Modern Python project config
└── .gitignore
```

---

## File Responsibilities

### Core Components (`chatur/core/`)

#### `wake_word.py`
- Initialize Porcupine with custom wake word
- Continuous audio monitoring
- Emit wake detection events
- Handle microphone errors

#### `stt.py`
- Azure Speech API integration
- Bilingual speech recognition (en-IN, hi-IN)
- Audio capture and streaming
- Error handling and retries

#### `tts.py`
- pyttsx3 initialization
- Language-aware voice selection
- Asynchronous speech synthesis
- Volume and rate control

#### `llm.py`
- OpenAI API client
- Intent classification
- Parameter extraction
- Multilingual prompt handling

---

### Handlers (`chatur/handlers/`)

#### `base.py`
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseHandler(ABC):
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can process the intent"""
        pass
    
    @abstractmethod
    def handle(self, intent: Intent) -> str:
        """Process the intent and return response text"""
        pass
```

#### `reminder.py`
- Parse reminder time from natural language
- Create and store reminders
- Return confirmation message

#### `timer.py`
- Parse timer duration
- Start countdown timer
- Return confirmation message

#### `notes.py`
- Extract key-value pairs
- Store/retrieve notes
- Handle search queries

#### `qa.py`
- Forward questions to OpenAI
- Format responses
- Handle context

#### `app_launcher.py`
- Resolve app names to paths
- Launch applications
- Handle launch errors

#### `media_control.py`
- Simulate keyboard shortcuts
- Control playback
- Handle Spotify not running

---

### Storage Layer (`chatur/storage/`)

#### `init_db.py`
- Create database schema
- Insert default data
- Run on first startup

#### `repository.py`
- Base repository with common DB operations
- Connection management
- Query execution helpers

#### `*_repository.py`
- Specific CRUD operations for each table
- Business logic queries
- Data validation

---

### Service Layer (`chatur/service/`)

#### `manager.py`
- Main orchestrator
- Component lifecycle management
- Event coordination
- State machine implementation

#### `tray.py`
- System tray icon
- Right-click menu
- Status updates
- User interactions

#### `scheduler.py`
- APScheduler integration
- Reminder checking (every 30s)
- Timer monitoring
- Cleanup tasks

---

### Utilities (`chatur/utils/`)

#### `config.py`
```python
import yaml
from pathlib import Path
from typing import Any

class Config:
    def __init__(self, config_path: Path):
        with open(config_path) as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
```

#### `logger.py`
```python
import logging
from pathlib import Path
import os

def setup_logger(name: str) -> logging.Logger:
    log_dir = Path(os.getenv('APPDATA')) / 'Computer' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(log_dir / 'chatur.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

#### `time_parser.py`
- Parse natural language time expressions
- Convert to datetime objects
- Handle relative times ("tomorrow", "in 5 minutes")

---

### Models (`chatur/models/`)

#### `intent.py`
```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class IntentType(Enum):
    REMINDER = "reminder"
    TIMER = "timer"
    NOTE = "note"
    QUESTION = "question"
    APP_LAUNCH = "app_launch"
    MEDIA_CONTROL = "media_control"
    UNKNOWN = "unknown"

@dataclass
class Intent:
    type: IntentType
    language: str  # 'en', 'hi', 'hinglish'
    parameters: Dict[str, Any]
    response_language: str
    confidence: float
```

---

### Configuration Files

#### `config/config.yaml`
```yaml
# Computer Configuration

wake_word:
  sensitivity: 0.5
  keyword_path: "resources/wake_words/chatur_windows.ppn"

azure:
  region: "eastus"
  languages:
    - "en-IN"
    - "hi-IN"

openai:
  model: "gpt-3.5-turbo"
  max_tokens: 150

tts:
  rate: 150
  volume: 0.9

scheduler:
  reminder_check_interval: 30  # seconds
  max_conversation_history: 100

logging:
  level: "INFO"
  max_file_size_mb: 10
```

#### `config/.env.example`
```env
# API Keys (DO NOT COMMIT)
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus
OPENAI_API_KEY=your_openai_key_here
```

---

### Entry Point (`chatur/main.py`)

```python
import sys
from pathlib import Path
from chatur.service.manager import ServiceManager
from chatur.utils.logger import setup_logger
from chatur.storage.init_db import init_database

def main():
    # Setup logging
    logger = setup_logger('chatur')
    logger.info("Starting Computer Voice Assistant")
    
    # Initialize database
    init_database()
    
    # Start service
    try:
        manager = ServiceManager()
        manager.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        manager.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

### Installation Script (`scripts/install.bat`)

```batch
@echo off
echo Installing Computer Voice Assistant...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Initialize database
python -m chatur.storage.init_db

REM Setup auto-start
python scripts\setup_autostart.py

echo Installation complete!
pause
```

---

## Dependencies (`requirements.txt`)

```txt
# Wake Word Detection
pvporcupine==2.2.0

# Speech Recognition
azure-cognitiveservices-speech==1.34.0

# Text-to-Speech
pyttsx3==2.90

# LLM
openai==1.6.1

# Database
# (sqlite3 is built-in)

# Scheduling
APScheduler==3.10.4

# System Tray
pystray==0.19.5
Pillow==10.1.0

# Notifications
win10toast==0.9

# Media Control
pyautogui==0.9.54

# Configuration
PyYAML==6.0.1
python-dotenv==1.0.0

# Utilities
python-dateutil==2.8.2
```

---

## Build Configuration (`setup.py`)

```python
from setuptools import setup, find_packages

setup(
    name="chatur",
    version="1.0.0",
    description="Personal PC Voice Assistant",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # (same as requirements.txt)
    ],
    entry_points={
        'console_scripts': [
            'chatur=chatur.main:main',
        ],
    },
    package_data={
        'chatur': [
            'resources/icons/*.ico',
            'resources/wake_words/*.ppn',
            'resources/prompts/*.txt',
        ],
    },
)
```

---

## Packaging for Distribution

### PyInstaller Spec (`chatur.spec`)

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['chatur/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('config/config.yaml', 'config'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Computer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/tray_idle.ico',
)
```

Build command:
```bash
pyinstaller chatur.spec
```

---

## Development Workflow

1. **Setup:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run in development:**
   ```bash
   python -m chatur.main
   ```

3. **Run tests:**
   ```bash
   pytest tests/
   ```

4. **Build executable:**
   ```bash
   pyinstaller chatur.spec
   ```

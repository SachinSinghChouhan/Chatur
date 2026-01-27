# Technical Constraints & Stack

## Architecture Philosophy

**Hybrid Approach:**
- Local processing for privacy-critical components (wake word, memory)
- Cloud APIs for accuracy-critical components (STT, LLM)
- Minimize latency while maximizing reliability

## Required Stack

### Core Language
- **Python 3.10+** (AI/ML ecosystem, rapid development)

### Wake Word Detection
- **Porcupine by Picovoice** (offline, lightweight, custom wake word support)
- Custom wake word: "Computer"
- Runs continuously in background thread

### Speech Recognition (STT)
- **Azure Speech API** (cloud-based)
- Languages: English (en-IN) + Hindi (hi-IN)
- Auto language detection enabled for Hinglish
- Reason: High accuracy, multilingual support, low latency
- Fallback: Whisper (offline) for future versions

### Language Model (LLM)
- **OpenAI API** (GPT-4 or GPT-3.5-turbo)
- Purpose: Question answering, intent classification
- Multilingual prompting: Handles English + Hindi/Hinglish
- Alternative considered: Gemini API

### Text-to-Speech (TTS)
- **pyttsx3** (offline, Windows SAPI)
- Languages: English + Hindi (if available voices installed)
- Language detection from response text
- Reason: Zero latency, no API costs, sufficient quality for v1
- Future: Azure TTS or ElevenLabs for natural voices

### Memory & Storage
- **SQLite** (local database)
- Tables: reminders, timers, notes, conversation_history
- Location: `%APPDATA%/Computer/computer.db`

### Background Service
- **Windows Service** (using `pywin32`)
- Auto-start with Windows
- System tray integration with `pystray`

### Notifications
- **Windows Toast Notifications** (using `win10toast` or `plyer`)
- **Voice Alerts** (via pyttsx3)

### App Control & Automation
- **subprocess** + **os.startfile()** (built-in Python)
- Purpose: Launch applications (Chrome, Gmail, Calculator, etc.)
- App registry: Configurable app paths in database

### Media Control (Spotify)
- **pyautogui** or **keyboard** library (simulates keyboard shortcuts)
- Controls: Play/Pause, Next, Previous, Volume
- Works with Spotify Free (no API/Premium required)
- Uses Windows media keys (Space, Ctrl+Right, Ctrl+Left)

## System Architecture

```
┌─────────────────────────────────────────┐
│         System Tray Interface           │
│    (Status, Mic Toggle, Settings)       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Background Service Manager        │
│  (Windows Service / Auto-start)         │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼──────────┐
│  Wake Word     │  │  Command        │
│  Listener      │  │  Processor      │
│  (Porcupine)   │  │                 │
└───────┬────────┘  └──────┬──────────┘
        │                  │
        │         ┌────────▼─────────┐
        │         │  STT (Azure)     │
        │         └────────┬─────────┘
        │                  │
        │         ┌────────▼─────────┐
        │         │  Intent Parser   │
        │         │  (OpenAI API)    │
        │         └────────┬─────────┘
        │                  │
        │         ┌────────▼─────────┐
        │         │  Action Handler  │
        │         │  - Reminder      │
        │         │  - Timer         │
        │         │  - Notes         │
        │         │  - QA            │
        │         └────────┬─────────┘
        │                  │
        │         ┌────────▼─────────┐
        │         │  Memory Store    │
        │         │  (SQLite)        │
        │         └──────────────────┘
        │                  │
        └──────────────────▼──────────┐
                   TTS Response        │
                   (pyttsx3)           │
                   + Notifications     │
                   (win10toast)        │
        ────────────────────────────────┘
```

## Patterns & Principles

### Design Patterns
- **Event-Driven Architecture:** Wake word triggers event pipeline
- **Plugin Pattern:** Modular action handlers (reminder, timer, notes, QA)
- **Repository Pattern:** Abstract database operations
- **Singleton:** Single instance of service manager

### Code Organization
```
chatur/
├── core/
│   ├── wake_word.py       # Porcupine integration
│   ├── stt.py             # Azure Speech STT
│   ├── tts.py             # pyttsx3 wrapper
│   └── llm.py             # OpenAI API client
├── handlers/
│   ├── reminder.py        # Reminder logic
│   ├── timer.py           # Timer logic
│   ├── notes.py           # Notes storage
│   ├── qa.py              # Question answering
│   ├── app_launcher.py    # App launching
│   └── media_control.py   # Spotify/media control
├── storage/
│   ├── database.py        # SQLite operations
│   └── models.py          # Data models
├── service/
│   ├── manager.py         # Main service orchestrator
│   ├── tray.py            # System tray UI
│   └── scheduler.py       # Background task scheduler
├── utils/
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging setup
└── main.py                # Entry point
```

## Non-Negotiables

### Platform
- ✅ Must run on Windows 10/11
- ✅ Must auto-start with Windows
- ✅ Must run in background (no console window)

### Privacy
- ✅ Wake word detection must be 100% offline
- ✅ All memory/data stored locally
- ✅ No audio recording sent to cloud without active command

### Performance
- ✅ Wake word latency < 500ms
- ✅ Command response time < 3 seconds (end-to-end)
- ✅ Idle CPU usage < 2%
- ✅ RAM footprint < 150MB

### Reliability
- ✅ Reminders must trigger within ±30 seconds of scheduled time
- ✅ Timers must be accurate to ±1 second
- ✅ Service must auto-restart on crash
- ✅ Data must persist across restarts

## API Keys Required

- **Porcupine:** Free tier or paid license
- **Azure Speech:** Subscription key
- **OpenAI:** API key

## Development Environment

- **OS:** Windows 10/11
- **Python:** 3.10+
- **IDE:** VS Code (recommended)
- **Testing:** Physical Windows machine (not VM for audio testing)

## Deployment Strategy (v1)

- **Package:** PyInstaller (single executable)
- **Installer:** NSIS or Inno Setup
- **Auto-start:** Windows Registry entry or Startup folder
- **Updates:** Manual (future: auto-update mechanism)

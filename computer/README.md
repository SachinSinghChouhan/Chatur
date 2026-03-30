# Chatur — Personal Voice Assistant

Bilingual (English + Hindi/Hinglish) desktop voice assistant with wake word detection, intelligent task management, and a floating animated overlay. Runs on **Windows 10/11** and **Ubuntu 20.04+**.

## Features

- Wake word ("Hey Computer") or Ctrl+Space hotkey activation
- Bilingual voice commands — English & Hindi/Hinglish
- 13+ intent handlers: reminders, timers, notes, calendar, email, tasks, media control, file search, weather, system info, math, app launch, Q&A
- Google Calendar / Gmail / Tasks integration
- Floating React overlay with real-time state animations
- System tray background service

## Quick Start

### Prerequisites

**Ubuntu:**
```bash
# System libraries required before pip install
sudo apt update
sudo apt install -y \
    portaudio19-dev \
    espeak espeak-ng libespeak-ng-dev \
    python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0 \
    libgirepository1.0-dev gcc libcairo2-dev pkg-config
```

**Windows:** No extra system libraries needed — everything installs via pip.

### 1. Install Python dependencies

**Ubuntu:**
```bash
cd computer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
cd computer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` in the `computer/` directory:
```
PORCUPINE_ACCESS_KEY=<key from https://console.picovoice.ai/>
AZURE_SPEECH_KEY=<key from https://portal.azure.com/>
AZURE_SPEECH_REGION=centralindia
OPENAI_API_KEY=<key from https://platform.openai.com/api-keys>
```

### 3. (Optional) Set up Google integration

Run the OAuth2 setup once to enable Calendar, Gmail, and Tasks:
```bash
python setup_google.py
```

### 4. Run

```bash
# System tray mode with overlay (default)
python -m chatur.main

# Text-only console mode (no microphone / tray needed)
python -m chatur.main --console
```

## Build standalone executable

```bash
# Build React UI first
cd ui && npm install && npm run build && cd ..

# Package into single executable
python build.py
# Output: dist/ChaturAssistant  (Linux)  or  dist/ChaturAssistant.exe  (Windows)
```

## Project Structure

```
computer/
├── chatur/
│   ├── core/           # STT, TTS, LLM, wake word, state machine
│   ├── handlers/       # 13+ intent handlers
│   ├── service/        # Command processor, scheduler
│   ├── storage/        # SQLite repositories
│   ├── api/            # FastAPI WebSocket server
│   ├── ui/             # System tray, webview overlay
│   ├── utils/          # Config, logger, platform helpers, responses
│   └── models/         # Intent dataclass
├── config/config.yaml  # Application settings
├── .env                # API keys (not committed)
├── requirements.txt    # Python dependencies
├── build.py            # PyInstaller build script
└── ui/                 # React/Tailwind frontend source
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `portaudio` not found (Ubuntu) | `sudo apt install portaudio19-dev` |
| TTS silent on Ubuntu | `sudo apt install espeak espeak-ng` |
| Overlay not showing on Ubuntu | `sudo apt install python3-gi gir1.2-webkit2-4.0` |
| Azure STT auth error | Check `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` in `.env` |
| Wake word not triggering | Set `wake_word.enabled: true` in `config.yaml` and add `PORCUPINE_ACCESS_KEY` |
| Google features not working | Run `python setup_google.py` to authenticate |

## License

MIT

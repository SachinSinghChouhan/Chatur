# Computer Voice Assistant

Personal PC voice assistant with wake word detection, bilingual support (English + Hindi/Hinglish), and intelligent task management.

## Features

- 🎤 Wake word detection ("Hi Computer", "Sun Computer")
- 🗣️ Bilingual voice commands (English + Hindi/Hinglish)
- ⏰ Reminders and timers
- 📝 Note taking and retrieval
- ❓ Question answering
- 🚀 App launching
- 🎵 Spotify control

## Setup

### 1. Install Dependencies

```bash
cd computer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp config/.env.example .env
```

Edit `.env` and add:
- `PORCUPINE_ACCESS_KEY` - Get from https://console.picovoice.ai/
- `AZURE_SPEECH_KEY` - Get from https://portal.azure.com/
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys

### 3. Run

```bash
python -m chatur.main
```

## Project Structure

```
computer/
├── chatur/              # Main package
│   ├── core/           # Core components (TTS, STT, LLM, Wake Word)
│   ├── handlers/       # Action handlers
│   ├── storage/        # Database layer
│   ├── service/        # Service management
│   ├── utils/          # Utilities
│   └── models/         # Data models
├── config/             # Configuration files
├── resources/          # Static resources
└── tests/              # Unit tests
```

## Development Status

- ✅ Project setup
- ✅ Database layer
- ✅ TTS (Text-to-Speech)
- ✅ LLM integration
- ⏳ Wake word detection
- ⏳ Speech-to-text
- ⏳ Action handlers
- ⏳ Background service

## License

MIT

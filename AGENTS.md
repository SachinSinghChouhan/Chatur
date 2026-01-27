# AI Agent Context - Chatur Voice Assistant

> **Project**: Chatur - Personal Voice Assistant  
> **Language**: Python 3.8+  
> **Platform**: Windows 10/11  
> **Status**: Active Development

---

## 📋 Project Overview

**Chatur** is a bilingual (English + Hindi/Hinglish) voice assistant for Windows with wake word detection and intelligent task management. The project aims to provide hands-free PC control with natural language understanding.

### Core Capabilities
- Wake word detection ("Hi Computer", "Sun Computer")
- Speech-to-text (multiple engine support)
- Text-to-speech (Azure TTS)
- LLM-powered responses (OpenAI GPT)
- Task management (reminders, notes, app launching, Spotify control)

---

## 🏗️ Architecture

### High-Level Structure

```
Chatur Voice Assistant
│
├── Core Layer (chatur/core/)
│   ├── Wake Word Detection (Porcupine)
│   ├── Speech-to-Text (Azure/Google/Vosk/Whisper)
│   ├── Text-to-Speech (Azure TTS)
│   └── LLM Integration (OpenAI)
│
├── Handler Layer (chatur/handlers/)
│   ├── Reminder Handler
│   ├── Note Handler
│   ├── App Launcher
│   └── Spotify Controller
│
├── Storage Layer (chatur/storage/)
│   └── SQLite Database
│
└── Service Layer (chatur/service/)
    └── Background Service Manager
```

### Key Design Decisions

1. **Modular STT Support**: Multiple speech recognition engines for flexibility
2. **Bilingual Processing**: Seamless English/Hindi/Hinglish support
3. **Cloud-First**: Azure/OpenAI for quality, with offline fallbacks
4. **SQLite Storage**: Lightweight, serverless database for notes/reminders
5. **Event-Driven**: Async processing for responsive UX

---

## 📂 Codebase Navigation

### Core Components (`chatur/core/`)

- **`tts.py`** - Text-to-Speech engine (Azure)
- **`stt.py`** - Speech-to-Text with multi-engine support
- **`llm.py`** - OpenAI GPT integration for intelligent responses
- **`wake_word.py`** - Porcupine wake word detection

### Handlers (`chatur/handlers/`)

- **`reminder.py`** - Reminder creation and notification
- **`note.py`** - Voice note taking and retrieval
- **`app_launcher.py`** - Launch Windows applications
- **`spotify.py`** - Spotify playback control

### Storage (`chatur/storage/`)

- **`db.py`** - SQLite database interface for persistent data

### Service (`chatur/service/`)

- **`manager.py`** - Background service and system tray integration

### Configuration

- **`.env`** - API keys and configuration (not in repo)
- **`config/.env.example`** - Template for environment variables
- **`requirements.txt`** - Python dependencies

---

## 🔧 Development Guidelines

### Code Style

- Follow **PEP 8** conventions
- Use **type hints** for function signatures
- Write **docstrings** for all public functions/classes
- Keep functions **focused and small** (single responsibility)

### Testing

- Write tests for all new features
- Test files located in `tests/` and root-level `test_*.py`
- Run tests before committing: `python -m pytest tests/`

### Error Handling

- Use try-except blocks for external API calls
- Log errors appropriately (use Python `logging` module)
- Provide user-friendly error messages via TTS

### API Keys & Secrets

- **NEVER** commit API keys to the repository
- Always use `.env` file for sensitive data
- Required keys:
  - `PORCUPINE_ACCESS_KEY` (Picovoice)
  - `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` (Microsoft Azure)
  - `OPENAI_API_KEY` (OpenAI)

---

## 🎯 Current Development Status

### ✅ Completed
- Project architecture and structure
- Database layer (SQLite)
- Text-to-Speech (Azure TTS)
- LLM integration (OpenAI GPT)
- Speech-to-Text (Azure, Google, Vosk, Whisper)
- Wake word detection (Porcupine)

### ⏳ In Progress
- Action handlers (reminders, notes, app launching)
- Background service implementation
- System tray integration

### 📋 Planned
- Advanced Spotify integration
- Calendar integration
- Email reading/sending
- Smart home control
- Custom wake word training

---

## 🔍 Key Files to Understand

### Entry Points
- **`run_console.py`** - Console mode launcher
- **`run_tray.py`** - System tray mode launcher

### Core Logic
- **`chatur/core/stt.py`** - Speech recognition logic
- **`chatur/core/llm.py`** - Natural language processing
- **`chatur/storage/db.py`** - Data persistence

### Testing
- **`test_azure_stt.py`** - Azure STT testing
- **`test_llm.py`** - LLM integration testing
- **`TESTING.md`** - Comprehensive testing guide
- **`TEST_RESULTS.md`** - Latest test results

---

## 🛠️ Common Development Tasks

### Adding a New Handler

1. Create handler file in `chatur/handlers/`
2. Implement handler class with required methods
3. Register handler in main service loop
4. Add tests in `tests/`
5. Update documentation

### Adding a New STT Engine

1. Implement engine interface in `chatur/core/stt.py`
2. Add configuration in `.env.example`
3. Update `requirements.txt` if needed
4. Create test file `test_[engine]_stt.py`
5. Document in README.md

### Debugging Speech Recognition

1. Check microphone permissions in Windows settings
2. Verify API keys in `.env`
3. Run specific STT test: `python test_azure_stt.py`
4. Check logs for error messages
5. Test with different microphone input levels

---

## 🧪 Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock external API calls
- Located in `tests/` directory

### Integration Tests
- Test component interactions
- Use real API calls (with test keys)
- Root-level `test_*.py` files

### Manual Testing
- Voice command testing with real microphone
- Wake word detection accuracy
- End-to-end user flows

---

## 📚 External Dependencies

### Cloud Services
- **Picovoice Porcupine** - Wake word detection
- **Microsoft Azure Speech** - STT and TTS
- **OpenAI GPT** - Natural language understanding
- **Google Speech** (optional) - Alternative STT

### Python Libraries
- `pvporcupine` - Wake word detection
- `azure-cognitiveservices-speech` - Azure Speech SDK
- `openai` - OpenAI API client
- `SpeechRecognition` - Multi-engine STT wrapper
- `sqlite3` - Database (built-in)

See `requirements.txt` for complete list.

---

## 🚀 Quick Start for Development

1. **Setup environment**
   ```bash
   cd computer
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API keys**
   ```bash
   copy config\.env.example .env
   # Edit .env with your API keys
   ```

3. **Run tests**
   ```bash
   python test_azure_stt.py
   python test_llm.py
   ```

4. **Start development**
   ```bash
   python run_console.py
   ```

---

## 🎨 Code Patterns

### Async/Await
Use async patterns for I/O operations (API calls, file operations)

### Dependency Injection
Pass dependencies (API clients, config) to constructors

### Factory Pattern
Use factories for creating STT/TTS engines based on config

### Observer Pattern
Event-driven architecture for wake word → STT → LLM → TTS flow

---

## 🐛 Known Issues & Limitations

- Wake word detection requires quiet environment
- Hindi/Hinglish accuracy depends on STT engine quality
- Cloud services require internet connection
- Windows-only (Linux/Mac support planned)
- System tray integration incomplete

---

## 📖 Additional Resources

- [Main README](README.md) - User-facing documentation
- [Testing Guide](TESTING.md) - Comprehensive testing docs
- [Test Results](TEST_RESULTS.md) - Latest test outcomes
- [Computer README](computer/README.md) - Detailed setup guide

---

## 💡 Development Philosophy

- **User-First**: Natural, conversational interactions
- **Privacy-Aware**: Offer offline alternatives where possible
- **Bilingual by Design**: English and Hindi are first-class citizens
- **Extensible**: Easy to add new handlers and capabilities
- **Well-Tested**: Comprehensive test coverage for reliability

---

> This file adheres to the [AGENTS.md](https://agents.md) standard for AI discovery.

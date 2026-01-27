# Chatur - Personal Voice Assistant

> 🎤 Your bilingual PC companion with wake word detection and intelligent task management.

## Overview

**Chatur** is a personal voice assistant for Windows that brings hands-free control to your PC. With wake word detection, bilingual support (English + Hindi/Hinglish), and intelligent task management, Chatur makes interacting with your computer as natural as having a conversation.

---

## ✨ Features

- 🎤 **Wake Word Detection** - "Hi Computer" or "Sun Computer" to activate
- 🗣️ **Bilingual Support** - Seamlessly handles English, Hindi, and Hinglish commands
- ⏰ **Smart Reminders** - Set timers and get notified at the right time
- 📝 **Note Taking** - Voice-to-text notes with easy retrieval
- ❓ **Question Answering** - Powered by LLM for intelligent responses
- 🚀 **App Launching** - Open applications with voice commands
- 🎵 **Spotify Control** - Play, pause, skip tracks hands-free
- 🔊 **Natural TTS** - High-quality text-to-speech responses

---

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.8 or higher
- Microphone access
- Internet connection (for cloud services)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd protocol/computer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Copy `.env.example` to `.env`:
   ```bash
   copy config\.env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - `PORCUPINE_ACCESS_KEY` - Get from [Picovoice Console](https://console.picovoice.ai/)
   - `AZURE_SPEECH_KEY` - Get from [Azure Portal](https://portal.azure.com/)
   - `AZURE_SPEECH_REGION` - Your Azure region (e.g., `eastus`)
   - `OPENAI_API_KEY` - Get from [OpenAI Platform](https://platform.openai.com/api-keys)

5. **Run Chatur**
   ```bash
   # Console mode
   python run_console.py
   
   # System tray mode (background service)
   python run_tray.py
   ```

---

## 📁 Project Structure

```
computer/
├── chatur/                 # Main package
│   ├── core/              # Core components
│   │   ├── tts.py         # Text-to-Speech engine
│   │   ├── stt.py         # Speech-to-Text engine
│   │   ├── llm.py         # LLM integration
│   │   └── wake_word.py   # Wake word detection
│   ├── handlers/          # Action handlers
│   │   ├── reminder.py    # Reminder management
│   │   ├── note.py        # Note taking
│   │   ├── app_launcher.py
│   │   └── spotify.py     # Spotify control
│   ├── storage/           # Database layer
│   │   └── db.py          # SQLite database
│   ├── service/           # Service management
│   │   └── manager.py     # Background service
│   ├── utils/             # Utilities
│   └── models/            # Data models
├── config/                # Configuration files
│   └── .env.example       # Environment template
├── resources/             # Static resources
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🎯 Usage Examples

### Basic Commands

```
"Hi Computer"                    # Activate assistant
"Set a reminder for 5 minutes"   # Create reminder
"Take a note"                    # Start note taking
"What's the weather?"            # Ask questions
"Open Chrome"                    # Launch applications
"Play music on Spotify"          # Control Spotify
```

### Bilingual Examples

```
"Computer, mujhe 10 minute baad remind karo"
"Note likh: meeting kal 3 baje hai"
"Spotify pe gaana bajao"
```

---

## 🔧 Configuration

### Speech Recognition Options

Chatur supports multiple STT engines:
- **Azure Speech** (default) - Cloud-based, high accuracy
- **Google Speech** - Alternative cloud option
- **Vosk** - Offline, privacy-focused
- **Whisper** - OpenAI's model, high accuracy

Configure in `.env`:
```env
STT_ENGINE=azure  # Options: azure, google, vosk, whisper
```

### Wake Word Customization

Modify wake words in `config/wake_words.json` or use Picovoice Console to train custom wake words.

---

## 🧪 Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python test_azure_stt.py
python test_llm.py
```

### Development Status

- ✅ Project setup and architecture
- ✅ Database layer (SQLite)
- ✅ Text-to-Speech (Azure TTS)
- ✅ LLM integration (OpenAI)
- ✅ Speech-to-Text (Multiple engines)
- ✅ Wake word detection (Porcupine)
- ⏳ Action handlers (In progress)
- ⏳ Background service
- ⏳ System tray integration

---

## 🤖 For AI Agents

> **IMPORTANT**: Please read [AGENTS.md](AGENTS.md) for project context and development guidelines.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **STT**: Azure Speech, Google Speech, Vosk, Whisper
- **TTS**: Azure Text-to-Speech
- **LLM**: OpenAI GPT
- **Wake Word**: Picovoice Porcupine
- **Database**: SQLite
- **UI**: System tray (Windows)

---

## 📚 Documentation

- [Testing Guide](TESTING.md) - Comprehensive testing documentation
- [Test Results](TEST_RESULTS.md) - Latest test outcomes
- [API Documentation](docs/) - Detailed API reference

---

## 🐛 Troubleshooting

### Common Issues

**Microphone not detected**
- Check Windows privacy settings for microphone access
- Ensure microphone is set as default recording device

**Wake word not responding**
- Verify `PORCUPINE_ACCESS_KEY` is valid
- Check microphone volume levels
- Try speaking closer to the microphone

**API errors**
- Verify all API keys in `.env` are correct
- Check internet connection
- Ensure API quotas are not exceeded

---

## 📄 License

MIT - Use this however you want. Attribution appreciated but not required.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## 🙏 Acknowledgments

- **Picovoice** - Wake word detection
- **Microsoft Azure** - Speech services
- **OpenAI** - LLM capabilities
- **Community** - For feedback and support
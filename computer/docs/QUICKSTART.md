# Quick Start Guide

## Testing the Voice Assistant (Without Wake Word)

Since wake word detection requires Porcupine setup, you can test all other features using the interactive command-line interface.

### 1. Setup Environment

```bash
cd d:\protocol\computer

# Activate virtual environment (if not already active)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file in project root:

```env
OPENAI_API_KEY=your_openai_key_here
# Azure and Porcupine keys optional for basic testing
```

### 3. Run Interactive Mode

```bash
python -m chatur.main
```

### 4. Test Commands

Try these commands:

**Reminders:**
```
Set a reminder for 5 PM
Remind me to call mom tomorrow at 8 AM
Kal subah 9 baje meeting ka reminder
```

**Timers:**
```
Set a timer for 30 seconds
Start a 5 minute timer
10 minute ka timer lagao
```

**Notes:**
```
Remember my favorite color is blue
What's my favorite color?
Mera birthday 15 January hai
```

**Questions:**
```
What's the capital of France?
How does photosynthesis work?
Bharat ki population kitni hai?
```

**App Launching:**
```
Open Chrome
Open Calculator
Gmail kholo
```

**Media Control:**
```
Play music
Pause
Next song
```

### 5. Expected Behavior

- Command is processed by LLM
- Intent is classified
- Appropriate handler executes
- Response is spoken via TTS
- Response is printed to console

### 6. Logs

Check logs at: `%APPDATA%\Computer\logs\computer.log`

### 7. Database

View database at: `%APPDATA%\Computer\computer.db`

You can use DB Browser for SQLite to inspect:
- Reminders created
- Notes stored
- Apps registered

## Next Steps

1. Get Porcupine API key for wake word
2. Get Azure Speech key for voice input
3. Implement wake word detection
4. Implement speech-to-text
5. Add background service
6. Add system tray

## Troubleshooting

**TTS not working:**
- Check if pyttsx3 is installed
- Verify Windows SAPI voices are available

**LLM errors:**
- Verify OPENAI_API_KEY in `.env`
- Check internet connection
- Ensure you have API credits

**Import errors:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

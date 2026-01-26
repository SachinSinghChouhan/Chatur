# Computer Voice Assistant - Setup Guide

## Prerequisites

- Windows 10/11
- Python 3.10 or higher
- Microphone access
- Internet connection (for cloud APIs)

## Step 1: Get API Keys

### Porcupine (Wake Word Detection)

1. Go to https://console.picovoice.ai/
2. Sign up for a free account
3. Create a new project
4. Copy your Access Key
5. Create custom wake word "Computer" and download `.ppn` file
6. Place `.ppn` file in `resources/wake_words/computer_windows.ppn`

### Azure Speech Services

1. Go to https://portal.azure.com/
2. Create a new "Speech Services" resource
3. Copy the Key and Region
4. Free tier: 5 hours/month

### OpenAI API

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key
4. Costs: ~$0.10 per 1000 requests (GPT-3.5-turbo)

## Step 2: Installation

```bash
# Navigate to project directory
cd d:\protocol\computer

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configuration

Create `.env` file in project root:

```bash
cp config\.env.example .env
```

Edit `.env` and add your API keys:

```env
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus
OPENAI_API_KEY=your_openai_key_here
```

## Step 4: Initialize Database

```bash
python -m chatur.storage.init_db
```

## Step 5: Test Run

```bash
python -m chatur.main
```

You should see:
- Database initialized
- TTS engine initialized
- LLM client initialized
- Test voice output: "Hello, I am Computer..."

## Troubleshooting

### TTS Not Working

- Check if Windows SAPI voices are installed
- For Hindi TTS: Windows Settings → Time & Language → Language → Add Hindi → Download speech pack

### API Errors

- Verify API keys are correct in `.env`
- Check internet connection
- Verify Azure region matches your resource

### Database Errors

- Check `%APPDATA%\Computer\` directory exists
- Ensure write permissions

## Next Steps

Once basic setup works:
1. Add wake word `.ppn` file
2. Test voice commands
3. Configure auto-start (optional)

## Support

Check logs at: `%APPDATA%\Computer\logs\computer.log`

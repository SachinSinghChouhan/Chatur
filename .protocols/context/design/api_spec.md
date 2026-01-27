# Computer Voice Assistant - API Integration Specifications

## External API Integrations

This document specifies how Computer integrates with external cloud services.

---

## 1. Porcupine Wake Word Detection

### Provider
**Picovoice Porcupine**

### Authentication
- Access Key (API key)
- Obtained from: https://console.picovoice.ai/

### Integration Type
- **Local SDK** (offline processing)
- No network calls during runtime

### Setup

```python
import pvporcupine

porcupine = pvporcupine.create(
    access_key='YOUR_ACCESS_KEY',
    keyword_paths=['resources/wake_words/chatur_windows.ppn']
)
```

### Custom Wake Word Creation

1. Go to https://console.picovoice.ai/
2. Create custom wake word: "Computer"
3. Download `.ppn` file for Windows
4. Place in `resources/wake_words/`

### Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `PorcupineInvalidArgumentError` | Invalid access key | Check API key in config |
| `PorcupineActivationError` | License expired | Renew license |
| `PorcupineIOError` | Microphone access denied | Request microphone permission |

---

## 2. Azure Speech Services (STT)

### Provider
**Microsoft Azure Cognitive Services**

### Authentication
- Subscription Key
- Region (e.g., "eastus")
- Obtained from: https://portal.azure.com/

### Endpoints

**Speech-to-Text:**
```
https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1
```

### Integration

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv('AZURE_SPEECH_KEY'),
    region=os.getenv('AZURE_SPEECH_REGION')
)

# Bilingual configuration
speech_config.speech_recognition_language = "en-IN"
auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    languages=["en-IN", "hi-IN"]
)

recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    auto_detect_source_language_config=auto_detect_config
)
```

### Request Format

**Audio Requirements:**
- Format: PCM 16-bit
- Sample Rate: 16kHz
- Channels: Mono

### Response Format

```json
{
  "RecognitionStatus": "Success",
  "DisplayText": "set a reminder for 5 PM",
  "Offset": 0,
  "Duration": 25000000,
  "Language": "en-IN"
}
```

### Error Handling

| Status Code | Error | Solution |
|-------------|-------|----------|
| 401 | Unauthorized | Check subscription key |
| 403 | Forbidden | Check region configuration |
| 429 | Rate limit exceeded | Implement retry with backoff |
| 500 | Service error | Retry request |

### Retry Strategy

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def recognize_speech(audio):
    # Azure STT call
    pass
```

### Pricing Considerations

**Free Tier:**
- 5 audio hours/month
- Sufficient for MVP testing

**Standard Tier:**
- $1 per audio hour
- Estimate: ~10 hours/month for personal use = $10/month

---

## 3. OpenAI API (LLM)

### Provider
**OpenAI**

### Authentication
- API Key
- Obtained from: https://platform.openai.com/api-keys

### Endpoints

**Chat Completions:**
```
POST https://api.openai.com/v1/chat/completions
```

### Integration

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": INTENT_CLASSIFIER_PROMPT},
        {"role": "user", "content": user_command}
    ],
    temperature=0.3,
    max_tokens=150
)
```

### Request Format

**Intent Classification:**

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are a voice assistant intent classifier. Analyze commands and return JSON with intent type, language, and parameters."
    },
    {
      "role": "user",
      "content": "Remind me to call mom at 5 PM"
    }
  ],
  "temperature": 0.3,
  "max_tokens": 150,
  "response_format": { "type": "json_object" }
}
```

### Response Format

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "{\"intent\":\"reminder\",\"language\":\"en\",\"parameters\":{\"text\":\"call mom\",\"time\":\"17:00\"},\"response_language\":\"en\"}"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 30,
    "total_tokens": 80
  }
}
```

### System Prompts

#### Intent Classifier Prompt

```text
You are Computer, a personal voice assistant. Analyze user commands and return JSON.

Supported intents:
- reminder: Set time-based reminders
- timer: Set countdown timers
- note: Store/retrieve facts
- question: Answer general questions
- app_launch: Open applications
- media_control: Control music playback
- unknown: Cannot understand

Response format:
{
  "intent": "reminder|timer|note|question|app_launch|media_control|unknown",
  "language": "en|hi|hinglish",
  "parameters": {
    // Intent-specific parameters
  },
  "response_language": "en|hi"
}

Examples:

Input: "Remind me to call mom at 5 PM"
Output: {"intent":"reminder","language":"en","parameters":{"text":"call mom","time":"17:00"},"response_language":"en"}

Input: "Kal subah 8 baje meeting ka reminder"
Output: {"intent":"reminder","language":"hi","parameters":{"text":"meeting","time":"tomorrow 08:00"},"response_language":"hi"}

Input: "Set timer for 5 minutes"
Output: {"intent":"timer","language":"en","parameters":{"duration_seconds":300},"response_language":"en"}

Input: "Open Chrome"
Output: {"intent":"app_launch","language":"en","parameters":{"app_name":"chrome"},"response_language":"en"}

Input: "Play music"
Output: {"intent":"media_control","language":"en","parameters":{"action":"play"},"response_language":"en"}

Input: "What's the capital of France?"
Output: {"intent":"question","language":"en","parameters":{"question":"What's the capital of France?"},"response_language":"en"}

Now analyze: {user_command}
```

#### Question Answering Prompt

```text
You are Computer, a helpful voice assistant. Answer the user's question concisely in {language}.

Keep responses:
- Short (2-3 sentences max)
- Conversational
- In the same language as the question

Question: {question}
```

### Error Handling

| Status Code | Error | Solution |
|-------------|-------|----------|
| 401 | Invalid API key | Check API key |
| 429 | Rate limit | Implement exponential backoff |
| 500 | Server error | Retry request |
| 503 | Service unavailable | Retry with backoff |

### Retry Strategy

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def classify_intent(text: str) -> Intent:
    # OpenAI API call
    pass
```

### Pricing Considerations

**GPT-3.5-turbo:**
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens
- Estimate: ~50 tokens per request
- 1000 requests = ~$0.10

**GPT-4 (optional upgrade):**
- Input: $30 / 1M tokens
- Output: $60 / 1M tokens
- Better accuracy but 60x more expensive

**Recommendation:** Start with GPT-3.5-turbo for MVP

---

## 4. Local TTS (pyttsx3)

### Provider
**Windows SAPI (built-in)**

### Integration

```python
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Get available voices
voices = engine.getProperty('voices')

# Select voice based on language
def get_voice_for_language(language: str):
    for voice in voices:
        if language == 'hi' and 'hindi' in voice.name.lower():
            return voice.id
        elif language == 'en' and 'english' in voice.name.lower():
            return voice.id
    return voices[0].id  # Default

engine.setProperty('voice', get_voice_for_language('en'))
engine.say("Hello, I am Computer")
engine.runAndWait()
```

### Voice Installation

**For Hindi TTS:**
1. Windows Settings → Time & Language → Language
2. Add Hindi language
3. Download speech pack
4. Restart application

### Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `RuntimeError` | Engine not initialized | Reinitialize engine |
| No Hindi voice | Language pack not installed | Guide user to install |

---

## 5. Windows Toast Notifications

### Provider
**win10toast (local library)**

### Integration

```python
from win10toast import ToastNotifier

toaster = ToastNotifier()

toaster.show_toast(
    title="Reminder",
    msg="Call mom",
    duration=10,
    icon_path="resources/icons/tray_idle.ico",
    threaded=True
)
```

### Notification Format

- **Title:** Action type (e.g., "Reminder", "Timer Complete")
- **Message:** User-defined text
- **Duration:** 10 seconds
- **Icon:** Computer logo

---

## API Key Management

### Storage

**Environment Variables (.env):**
```env
PORCUPINE_ACCESS_KEY=your_key_here
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=eastus
OPENAI_API_KEY=your_key_here
```

**Loading:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

PORCUPINE_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
AZURE_KEY = os.getenv('AZURE_SPEECH_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
```

### Security Best Practices

1. ✅ Never commit `.env` to git
2. ✅ Add `.env` to `.gitignore`
3. ✅ Provide `.env.example` template
4. ✅ Never log API keys
5. ✅ Use environment variables in production

---

## Network Error Handling Strategy

### General Retry Logic

```python
import time
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Any:
    """Retry function with exponential backoff"""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor
```

### Offline Fallback

When cloud APIs are unavailable:

1. **STT Failure:**
   - Response: "I'm having trouble hearing you. Please check your internet connection."
   - Log error for debugging

2. **OpenAI Failure:**
   - For intent classification: Use simple keyword matching as fallback
   - For QA: Response: "I can't answer that right now. Please try again later."

3. **Azure Failure:**
   - Switch to offline Whisper model (future enhancement)

---

## Rate Limiting

### Azure Speech
- Free tier: 20 transactions/minute
- Standard: No limit
- Implementation: Not needed for personal use

### OpenAI
- Free tier: 3 requests/minute
- Paid tier: 3500 requests/minute
- Implementation: Not needed for personal use

---

## Monitoring & Logging

### API Call Logging

```python
import logging

logger = logging.getLogger('chatur.api')

def log_api_call(service: str, endpoint: str, status: str, duration_ms: int):
    logger.info(f"{service} | {endpoint} | {status} | {duration_ms}ms")
```

### Metrics to Track

- API call count per service
- Average response time
- Error rate
- Token usage (OpenAI)

---

## Cost Estimation (Monthly)

| Service | Usage | Cost |
|---------|-------|------|
| Porcupine | Unlimited (local) | Free (or $5/month for commercial) |
| Azure Speech | ~10 hours | $10 |
| OpenAI (GPT-3.5) | ~1000 requests | $0.10 |
| **Total** | | **~$10-15/month** |

**Note:** Free tiers available for testing. Costs scale with usage.

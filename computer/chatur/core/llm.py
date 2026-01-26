"""OpenAI LLM integration for intent classification and Q&A"""

import os
import json
from openai import OpenAI
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
from chatur.utils.config import config
from tenacity import retry, stop_after_attempt, wait_exponential

logger = setup_logger('chatur.llm')

INTENT_CLASSIFIER_PROMPT = """You are Computer, a personal voice assistant. Analyze user commands and return JSON.

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
  "parameters": {},
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

Now analyze: {user_command}"""

class LLMClient:
    """OpenAI API client for intent classification and Q&A"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not set - LLM features will be limited")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
            logger.info("LLM client initialized")
    
    def classify_intent(self, text: str) -> Intent:
        """Classify user intent from text using rule-based approach"""
        # Use reliable rule-based classification (same as test mode)
        text_lower = text.lower()
        
        # Detect language - check for Hindi characters OR Hindi keywords
        has_hindi_chars = any(char in text for char in ['क', 'ख', 'ग', 'च', 'ज', 'त', 'द', 'न', 'प', 'म', 'य', 'र', 'ल', 'व', 'श', 'स', 'ह'])
        has_hindi_keywords = any(word in text_lower for word in [
            # Common Hindi words
            'kholo', 'khol', 'chalu', 'chalao', 'bajao', 'roko', 'band', 
            'agla', 'pichla', 'gana', 'baje', 'minute', 'ka', 'ko', 'pe', 'pr',
            'karo', 'kro', 'kr', 'de', 'do', 'hai', 'hain', 'mera', 'meri',
            # Hinglish patterns
            'karde', 'krde', 'karde', 'lagao', 'laga', 'set', 'reminder',
            'timer', 'yaad', 'rakh', 'batao', 'bata', 'kya', 'kaise', 'kab',
            'awaz', 'awaaz', 'tez', 'dheere', 'kam', 'badha', 'zyada', 'thoda'
        ])
        
        language = 'hi' if (has_hindi_chars or has_hindi_keywords) else 'en'
        response_language = language
        
        # Reminder intent
        if any(word in text_lower for word in ['remind', 'reminder', 'याद', 'रिमाइंडर']):
            # Extract time
            time_str = 'in 1 hour'
            if 'at' in text_lower:
                time_str = text_lower.split('at')[-1].strip()
            elif 'बजे' in text_lower or 'baje' in text_lower:
                time_str = text_lower
            
            return Intent(
                type=IntentType.REMINDER,
                language=language,
                parameters={'text': text, 'time': time_str},
                response_language=response_language
            )
        
        # Timer intent
        elif any(word in text_lower for word in ['timer', 'टाइमर', 'countdown']):
            # Extract duration
            duration = '5 minutes'
            if 'second' in text_lower:
                import re
                match = re.search(r'(\d+)\s*second', text_lower)
                if match:
                    duration = f"{match.group(1)} seconds"
            elif 'minute' in text_lower or 'min' in text_lower:
                import re
                match = re.search(r'(\d+)\s*min', text_lower)
                if match:
                    duration = f"{match.group(1)} minutes"
            
            return Intent(
                type=IntentType.TIMER,
                language=language,
                parameters={'duration': duration, 'label': 'Timer'},
                response_language=response_language
            )
        
        # Note intent
        elif any(word in text_lower for word in ['remember', 'note', 'याद रख', 'save']):
            return Intent(
                type=IntentType.NOTE,
                language=language,
                parameters={'action': 'store', 'key': 'note', 'value': text},
                response_language=response_language
            )
        
        # App launch intent
        elif any(word in text_lower for word in ['open', 'launch', 'start', 'close', 'quit', 'exit', 'kill', 'band', 'खोल', 'kholo', 'khol', 'chalu', 'chalao', 'browser']):
            # Determine action
            action = 'close' if any(word in text_lower for word in ['close', 'quit', 'exit', 'kill', 'band', 'बंद']) else 'open'
            
            # Check for URLs or websites
            import re
            # Build TLD pattern from config
            tlds = '|'.join(config.supported_tlds)
            url_pattern = rf'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.(?:{tlds})(?:/[^\s]*)?)'
            url_match = re.search(url_pattern, text_lower)
            
            # Check for file extensions - build pattern from config
            extensions = '|'.join(config.supported_file_extensions)
            file_pattern = rf'([a-zA-Z0-9_\-\.]+\.(?:{extensions}))'
            file_match = re.search(file_pattern, text_lower)
            
            # Check for "site" keyword
            site_keyword = 'site' in text_lower or 'website' in text_lower
            
            if url_match or site_keyword:
                # URL or website request - open in browser
                url = url_match.group(0) if url_match else None
                
                # If no URL found but "site" keyword present, extract the name
                if not url and site_keyword:
                    # Extract potential site name (word before "site")
                    site_name_match = re.search(r'(\w+)\s+(?:site|website)', text_lower)
                    if site_name_match:
                        url = f"{site_name_match.group(1)}.com"
                
                # Ensure URL has protocol
                if url and not url.startswith('http'):
                    url = f"https://{url}"
                
                return Intent(
                    type=IntentType.APP_LAUNCH,
                    language=language,
                    parameters={'app_name': config.default_browser, 'action': 'open', 'url': url},
                    response_language=response_language
                )
            
            elif file_match:
                # File request - use file search
                filename = file_match.group(0)
                return Intent(
                    type=IntentType.FILE_SEARCH,
                    language=language,
                    parameters={'query': filename},
                    response_language=response_language
                )
            
            else:
                # Regular app launch
                # Extract app name (default browser from config)
                app_name = config.default_browser
                for word in config.recognized_apps:
                    if word in text_lower:
                        app_name = word
                        break
                
                # If user just says "browser", use default browser
                if 'browser' in text_lower and app_name == config.default_browser:
                    app_name = config.default_browser
                
                return Intent(
                    type=IntentType.APP_LAUNCH,
                    language=language,
                    parameters={'app_name': app_name, 'action': action},
                    response_language=response_language
                )
        
        
        # Media control intent
        elif any(word in text_lower for word in ['play', 'pause', 'next', 'previous', 'stop', 'music', 'song', 'track', 'gana', 'bajao', 'roko', 'volume', 'awaz', 'awaaz', 'mute', 'loud', 'quiet']):
            action = 'play'
            volume_level = None
            
            # Extract volume level if present
            import re
            volume_match = re.search(r'(?:volume|awaz|awaaz)?\s*(?:to|ko|pe)?\s*(\d+)', text_lower)
            if volume_match:
                volume_level = volume_match.group(1)
                action = 'set_volume'
            elif 'pause' in text_lower or 'roko' in text_lower or 'band' in text_lower:
                action = 'pause'
            elif 'next' in text_lower or 'agla' in text_lower or 'aage' in text_lower:
                action = 'next'
            elif 'previous' in text_lower or 'prev' in text_lower or 'pichla' in text_lower or 'peeche' in text_lower:
                action = 'previous'
            elif 'volume up' in text_lower or 'increase' in text_lower or 'badha' in text_lower or 'loud' in text_lower or 'tez' in text_lower:
                action = 'volume_up'
            elif 'volume down' in text_lower or 'decrease' in text_lower or 'kam' in text_lower or 'quiet' in text_lower or 'dheere' in text_lower:
                action = 'volume_down'
            elif 'mute' in text_lower or 'silent' in text_lower or 'chup' in text_lower:
                action = 'mute'
            
            params = {'action': action}
            if volume_level:
                params['volume_level'] = volume_level
            
            return Intent(
                type=IntentType.MEDIA_CONTROL,
                language=language,
                parameters=params,
                response_language=response_language
            )
        
        # Question intent (everything else)
        else:
            return Intent(
                type=IntentType.QUESTION,
                language=language,
                parameters={'question': text},
                response_language=response_language
            )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def answer_question(self, question: str, language: str = 'en') -> str:
        """Answer a question using OpenAI"""
        if not self.client:
            return "I need an OpenAI API key to answer questions. Please add OPENAI_API_KEY to your .env file."
        
        try:
            system_prompt = f"""You are Computer, a helpful voice assistant. Answer the user's question concisely in {language}.

Keep responses:
- Short (2-3 sentences max)
- Conversational
- In the same language as the question"""
            
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=config.openai_max_tokens
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Generated answer for question: {question[:50]}...")
            return answer
            
        except Exception as e:
            logger.error(f"Question answering error: {e}")
            return "I'm having trouble answering that right now. Please try again later."

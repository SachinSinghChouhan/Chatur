"""Simple test script without OpenAI dependency"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from chatur.utils.logger import setup_logger
from chatur.storage.init_db import init_database
from chatur.core.tts import TextToSpeech
from chatur.models.intent import Intent, IntentType
from chatur.handlers.reminder import ReminderHandler
from chatur.handlers.timer import TimerHandler
from chatur.handlers.notes import NotesHandler
from chatur.handlers.app_launcher import AppLauncherHandler
from chatur.handlers.media_control import MediaControlHandler

logger = setup_logger('chatur.test')

def simple_classify_intent(text: str) -> Intent:
    """Simple rule-based intent classification for testing"""
    text_lower = text.lower()
    
    if 'remind' in text_lower:
        return Intent(
            type=IntentType.REMINDER,
            language='en',
            parameters={'text': text, 'time': '5 PM'},
            response_language='en'
        )
    elif 'timer' in text_lower:
        duration = '30 seconds' if 'second' in text_lower else '5 minutes'
        return Intent(
            type=IntentType.TIMER,
            language='en',
            parameters={'duration': duration, 'label': 'Timer'},
            response_language='en'
        )
    elif 'remember' in text_lower:
        words = text.split()
        key = words[-3] if len(words) >= 3 else 'item'
        value = words[-1]
        return Intent(
            type=IntentType.NOTE,
            language='en',
            parameters={'action': 'store', 'key': key, 'value': value},
            response_language='en'
        )
    elif 'open' in text_lower:
        app_name = text_lower.split('open')[-1].strip()
        return Intent(
            type=IntentType.APP_LAUNCH,
            language='en',
            parameters={'app_name': app_name},
            response_language='en'
        )
    elif any(word in text_lower for word in ['play', 'pause', 'next', 'previous']):
        action = 'play' if 'play' in text_lower else 'pause' if 'pause' in text_lower else 'next'
        return Intent(
            type=IntentType.MEDIA_CONTROL,
            language='en',
            parameters={'action': action},
            response_language='en'
        )
    else:
        return Intent(
            type=IntentType.QUESTION,
            language='en',
            parameters={'question': text},
            response_language='en'
        )

def main():
    """Test mode - no OpenAI required"""
    print("=" * 60)
    print("Computer Voice Assistant - TEST MODE")
    print("(Running without OpenAI - using simple intent classification)")
    print("=" * 60)
    
    try:
        # Initialize database
        print("\nInitializing database...")
        init_database()
        
        # Initialize TTS
        print("Initializing TTS engine...")
        tts = TextToSpeech()
        
        # Initialize handlers
        print("Initializing handlers...")
        handlers = {
            IntentType.REMINDER: ReminderHandler(),
            IntentType.TIMER: TimerHandler(tts_engine=tts),
            IntentType.NOTE: NotesHandler(),
            IntentType.APP_LAUNCH: AppLauncherHandler(),
            IntentType.MEDIA_CONTROL: MediaControlHandler(),
        }
        
        print("\n" + "=" * 60)
        print("Initialization complete!")
        print("=" * 60)
        
        # Welcome message
        tts.speak("Hello, I am Computer. Test mode activated.", 'en')
        
        # Interactive mode
        print("\nType your commands (or 'quit' to exit):")
        print("\nExample commands:")
        print("  - Set a reminder for 5 PM")
        print("  - Start a timer for 30 seconds")
        print("  - Remember my favorite color is blue")
        print("  - Open Chrome")
        print("  - Play music")
        print("\n" + "-" * 60 + "\n")
        
        while True:
            try:
                command = input("You: ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'bye']:
                    tts.speak("Goodbye!", 'en')
                    break
                
                # Classify intent
                intent = simple_classify_intent(command)
                print(f"[Intent: {intent.type.value}]")
                
                # Find handler
                handler = handlers.get(intent.type)
                
                if handler and handler.can_handle(intent):
                    response = handler.handle(intent)
                    print(f"Computer: {response}\n")
                    tts.speak_async(response, intent.response_language)
                else:
                    if intent.type == IntentType.QUESTION:
                        response = "I need an OpenAI API key to answer questions. For now, I can help with reminders, timers, notes, apps, and media control."
                        print(f"Computer: {response}\n")
                        tts.speak_async(response, 'en')
                    else:
                        response = "I didn't understand that command."
                        print(f"Computer: {response}\n")
                        tts.speak_async(response, 'en')
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error processing command: {e}", exc_info=True)
                print(f"Error: {e}\n")
        
        print("\nShutting down...")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

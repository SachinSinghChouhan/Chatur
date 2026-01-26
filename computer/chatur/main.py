"""Voice-enabled main application with console and system tray modes"""

import sys
import threading
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from chatur.utils.logger import setup_logger
from chatur.storage.init_db import init_database
from chatur.core.tts import TextToSpeech
from chatur.core.stt import SpeechToText
from chatur.core.llm import LLMClient
from chatur.service.command_processor import CommandProcessor
from chatur.service.scheduler import ReminderScheduler
from chatur.service.service_manager import ManagedService
from chatur.ui.system_tray import create_tray

logger = setup_logger('chatur')

# Global components (shared between modes)
tts = None
stt = None
llm = None
processor = None
scheduler = None


def initialize_components():
    """Initialize all core components"""
    global tts, stt, llm, processor, scheduler
    
    logger.info("=" * 60)
    logger.info("Computer Voice Assistant - Initializing")
    logger.info("=" * 60)
    
    # Initialize database
    logger.info("Initializing database...")
    init_database()
    
    # Initialize core components
    logger.info("Initializing TTS engine...")
    tts = TextToSpeech()
    
    logger.info("Initializing STT engine...")
    stt = SpeechToText()
    
    logger.info("Initializing LLM client...")
    llm = LLMClient()
    
    # Initialize command processor
    logger.info("Initializing command processor...")
    processor = CommandProcessor(llm, tts)
    
    # Initialize and start reminder scheduler
    logger.info("Initializing reminder scheduler...")
    scheduler = ReminderScheduler(tts_engine=tts)
    scheduler.start()
    
    logger.info("=" * 60)
    logger.info("Initialization complete!")
    logger.info("=" * 60)


def shutdown_components():
    """Shutdown all components gracefully"""
    global scheduler
    
    logger.info("Shutting down components...")
    
    # Stop scheduler
    if scheduler:
        scheduler.stop()
    
    logger.info("Shutdown complete")


def run_assistant_loop(stop_event: threading.Event):
    """
    Core assistant loop that can run in background
    
    Args:
        stop_event: Event to signal when to stop
    """
    global tts, stt, processor
    
    logger.info("Assistant loop started")
    
    # Check if STT is available
    use_voice = stt.recognizer is not None
    
    if not use_voice:
        logger.warning("STT not available - text mode only")
    
    # Main loop
    while not stop_event.is_set():
        try:
            # Text input mode (for now, until voice is fully working)
            command = input("You: ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'bye']:
                logger.info("User requested exit")
                tts.speak("Goodbye!", 'en')
                stop_event.set()
                break
            
            # Process command
            response = processor.process_command(command)
            print(f"Computer: {response}\n")
            
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            stop_event.set()
            break
        except Exception as e:
            logger.error(f"Error in assistant loop: {e}", exc_info=True)
            print(f"Error: {e}\n")
    
    logger.info("Assistant loop stopped")


def main_console():
    """Run in console mode (original behavior)"""
    logger.info("Starting in CONSOLE mode")
    
    try:
        # Initialize components
        initialize_components()
        
        # Welcome message
        tts.speak("Hello, I am Computer. I'm ready to help you.", 'en')
        
        # Check if STT is available
        if not stt.recognizer:
            print("\n⚠️  Azure Speech-to-Text not configured")
            print("Running in TEXT MODE - type your commands\n")
        else:
            print("\n" + "=" * 60)
            print("Computer Voice Assistant - Voice Mode")
            print("=" * 60)
            print("\nVoice input enabled! Speak your commands.")
            print("Press Enter to start listening, or type 'text' for text mode")
            print("\n" + "-" * 60 + "\n")
        
        # Show example commands
        print("Example commands:")
        print("  - Set a reminder for 5 PM")
        print("  - Start a timer for 5 minutes")
        print("  - Remember my favorite color is blue")
        print("  - What's the capital of France?")
        print("  - Open Chrome")
        print("  - Play music")
        print("\nType 'quit' to exit\n")
        print("-" * 60 + "\n")
        
        # Run the assistant loop
        stop_event = threading.Event()
        run_assistant_loop(stop_event)
        
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt - shutting down")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        shutdown_components()


def main_tray():
    """Run in system tray mode"""
    logger.info("Starting in SYSTEM TRAY mode")
    
    try:
        # Initialize components
        initialize_components()
        
        # Create managed service
        managed_service = ManagedService(
            run_callback=run_assistant_loop,
            auto_restart=True
        )
        
        # Start control loop
        managed_service.start_control_loop()
        
        # Auto-start the assistant
        managed_service.send_command('start')
        
        # Create and run system tray (blocking)
        tray = create_tray(
            managed_service=managed_service,
            on_exit=shutdown_components
        )
        
        logger.info("System tray starting...")
        tray.run()  # Blocking call
        
    except Exception as e:
        logger.error(f"Fatal error in tray mode: {e}", exc_info=True)
        sys.exit(1)
    finally:
        shutdown_components()


def main():
    """Main entry point - choose mode based on arguments"""
    
    # Check command line arguments
    if '--tray' in sys.argv:
        main_tray()
    elif '--console' in sys.argv:
        main_console()
    else:
        # Default to console mode
        main_console()


if __name__ == '__main__':
    main()

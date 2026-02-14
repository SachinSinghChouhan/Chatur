"""Voice-enabled main application with console and system tray modes"""

import sys
import threading
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from chatur.utils.logger import setup_logger
from chatur.storage.init_db import init_database
from chatur.core.tts import TextToSpeech
from chatur.core.stt import SpeechToText
from chatur.core.llm import LLMClient
from chatur.core.wake_word import WakeWordDetector, create_wake_word_detector
from chatur.service.command_processor import CommandProcessor
from chatur.service.scheduler import ReminderScheduler
from chatur.ui.system_tray import create_tray
from chatur.ui.webview_overlay import WebViewOverlay
from chatur.api.socket_server import run_api_server, broadcast_message_sync
from chatur.core.assistant_state import AssistantStateMachine, AssistantState
from chatur.core.activation import ActivationListener
from chatur.utils.config import config

logger = setup_logger('chatur')

tts = None
stt = None
llm = None
processor = None
scheduler = None
state_machine = None
activation_listener = None
wake_word_detector = None
native_overlay = None


def initialize_components():
    """Initialize all core components"""
    global tts, stt, llm, processor, scheduler, state_machine, native_overlay, wake_word_detector
    
    logger.info("=" * 60)
    logger.info("Computer Voice Assistant - Initializing")
    logger.info("=" * 60)
    
    logger.info("Initializing database...")
    init_database()
    
    logger.info("Initializing TTS engine...")
    tts = TextToSpeech()
    
    logger.info("Initializing STT engine...")
    stt = SpeechToText()
    
    logger.info("Initializing LLM client...")
    llm = LLMClient()
    
    logger.info("Starting API server...")
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()

    logger.info("Initializing webview overlay...")
    if getattr(sys, 'frozen', False):
        static_dir = Path(sys._MEIPASS) / "ui" / "dist"
    else:
        static_dir = Path(__file__).parent.parent / "ui" / "dist"
    
    native_overlay = WebViewOverlay(static_dir=static_dir)
    native_overlay.create_window()

    logger.info("Initializing state machine...")
    def on_state_change(event_type, data):
        broadcast_message_sync(event_type, data)
        if event_type == 'state_change' and data.get('state'):
            state_str = data['state']
            state = AssistantState(state_str)
            native_overlay.update_state(state)
    
    state_machine = AssistantStateMachine(broadcast_callback=on_state_change)

    logger.info("Initializing command processor...")
    processor = CommandProcessor(llm, tts, broadcast_callback=broadcast_message_sync)
    
    logger.info("Initializing reminder scheduler...")
    scheduler = ReminderScheduler(tts_engine=tts)
    scheduler.start()
    
    wake_word_enabled = config.get_bool('wake_word.enabled', False)
    if wake_word_enabled:
        logger.info("Initializing wake word detector...")
        wake_word_detector = create_wake_word_detector(
            on_wake_word=handle_user_activation
        )
        if wake_word_detector:
            wake_word_detector.start()
            logger.info("Wake word detection started")
        else:
            logger.warning("Wake word detector failed to initialize")
    else:
        logger.info("Wake word detection is disabled")
        wake_word_detector = None
    
    logger.info("=" * 60)
    logger.info("Initialization complete!")
    logger.info("=" * 60)


def shutdown_components():
    """Shutdown all components gracefully"""
    global scheduler, activation_listener, native_overlay, wake_word_detector
    
    logger.info("Shutting down components...")
    
    if wake_word_detector:
        wake_word_detector.stop()
    
    if activation_listener:
        activation_listener.stop()
    
    if native_overlay:
        native_overlay.stop()
    
    if scheduler:
        scheduler.stop()
    
    logger.info("Shutdown complete")



def handle_user_activation():
    """
    Called when user presses Ctrl+Space
    Triggers one complete interaction cycle: Listen → Process → Speak → Idle
    """
    global state_machine, stt, processor
    
    if not state_machine.is_idle():
        logger.warning("Activation ignored - assistant already active")
        return
    
    try:
        # Transition to LISTENING state
        state_machine.transition_to(AssistantState.LISTENING)
        logger.info("Listening for user input...")
        
        # Capture voice input
        user_input = stt.listen()
        
        if not user_input:
            logger.info("No input detected")
            state_machine.transition_to(AssistantState.IDLE)
            return
        
        logger.info(f"User said: {user_input}")
        
        # Transition to PROCESSING state
        state_machine.transition_to(AssistantState.PROCESSING)
        
        # Process command (this will transition to SPEAKING internally via processor)
        response = processor.process_command(user_input)
        logger.info(f"Response: {response}")
        
        # Return to IDLE after speaking completes
        state_machine.transition_to(AssistantState.IDLE)
        
    except Exception as e:
        logger.error(f"Error during activation: {e}", exc_info=True)
        state_machine.transition_to(AssistantState.IDLE)


def run_idle_loop(stop_event: threading.Event):
    """
    IDLE loop - waits for wake word OR keyboard activation
    Does NOT record audio or show UI until activated
    """
    global activation_listener
    
    wake_word_enabled = wake_word_detector is not None
    
    if wake_word_enabled:
        logger.info("Assistant running in IDLE mode - listening for 'Hey Computer'")
    else:
        logger.info("Assistant running in IDLE mode")
        logger.info("Press Ctrl+Space to activate")
        
        activation_listener = ActivationListener(on_activate=handle_user_activation)
        activation_listener.start()
    
    while not stop_event.is_set():
        stop_event.wait(timeout=1.0)
    
    logger.info("Idle loop stopped")


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
            broadcast_message_sync('listening')
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
    """Run in system tray mode with embedded webview overlay"""
    logger.info("Starting in SYSTEM TRAY mode")
    
    try:
        initialize_components()
        
        stop_event = threading.Event()
        idle_thread = threading.Thread(target=run_idle_loop, args=(stop_event,), daemon=True)
        idle_thread.start()
        
        def run_tray():
            def on_exit():
                stop_event.set()
                shutdown_components()
            
            tray = create_tray(
                managed_service=None,
                on_exit=on_exit
            )
            
            logger.info("System tray starting...")
            tray.run()
        
        tray_thread = threading.Thread(target=run_tray, daemon=True)
        tray_thread.start()
        
        wake_word_enabled = wake_word_detector is not None
        if wake_word_enabled:
            logger.info("Starting webview overlay - say 'Hey Computer' to activate")
        else:
            logger.info("Starting webview overlay - press Ctrl+Space to activate")
        
        native_overlay.start_blocking()

    except Exception as e:
        logger.error(f"Fatal error in tray mode: {e}", exc_info=True)
        sys.exit(1)
    finally:
        shutdown_components()


def main():
    """Main entry point - defaults to tray mode for silent background"""
    
    if '--console' in sys.argv:
        main_console()
    else:
        # Default to tray mode (silent background with Ctrl+Space activation)
        main_tray()


if __name__ == '__main__':
    main()

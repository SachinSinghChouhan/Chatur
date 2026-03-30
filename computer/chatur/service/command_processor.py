"""Command processor - integrates all handlers"""

import importlib
from typing import Any, Dict, Optional

from chatur.core.llm import LLMClient
from chatur.core.tts import TextToSpeech
from chatur.storage.conversation_repository import ConversationRepository
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.command_processor')

# Slots each intent needs to be complete, and the question to ask for each missing slot
_REQUIRED_SLOTS: Dict[IntentType, Dict[str, str]] = {
    IntentType.REMINDER: {
        'text':  "What should I remind you about?",
        'time':  "When should I remind you?",
    },
    IntentType.TIMER: {
        'duration': "How long should the timer run?",
    },
}

class CommandProcessor:
    """Process voice commands and execute actions"""
    
    def __init__(self, llm_client: LLMClient, tts_engine: TextToSpeech, broadcast_callback=None):
        self.llm = llm_client
        self.tts = tts_engine
        self.broadcast = broadcast_callback
        self.conversation_repo = ConversationRepository()
        # Pending multi-turn dialog state
        self._pending_intent: Optional[Intent] = None
        self._pending_slot: Optional[str] = None  # which slot we're waiting for
        
        # Initialize handlers
        self.handlers: Dict[IntentType, Any] = {}
        self._register_handler(IntentType.REMINDER, 'chatur.handlers.reminder', 'ReminderHandler')
        self._register_handler(IntentType.TIMER, 'chatur.handlers.timer', 'TimerHandler', tts_engine=tts_engine)
        self._register_handler(IntentType.NOTE, 'chatur.handlers.notes', 'NotesHandler')
        self._register_handler(IntentType.QUESTION, 'chatur.handlers.qa', 'QAHandler', llm_client, self.conversation_repo)
        self._register_handler(IntentType.APP_LAUNCH, 'chatur.handlers.app_launcher', 'AppLauncherHandler')
        self._register_handler(IntentType.MEDIA_CONTROL, 'chatur.handlers.media_control', 'MediaControlHandler')
        self._register_handler(IntentType.FILE_SEARCH, 'chatur.handlers.file_search', 'FileSearchHandler')
        self._register_handler(IntentType.WEATHER, 'chatur.handlers.weather', 'WeatherHandler')
        self._register_handler(IntentType.SYSTEM_INFO, 'chatur.handlers.system_info', 'SystemInfoHandler')
        self._register_handler(IntentType.MATH, 'chatur.handlers.math', 'MathHandler')
        self._register_handler(IntentType.CALENDAR, 'chatur.handlers.calendar', 'CalendarHandler')
        self._register_handler(IntentType.EMAIL, 'chatur.handlers.email', 'GmailHandler')
        self._register_handler(IntentType.TASK, 'chatur.handlers.tasks', 'GoogleTasksHandler')

        logger.info(f"Command processor initialized with {len(self.handlers)} handlers")

    def _register_handler(self, intent_type: IntentType, module_path: str, class_name: str, *args, **kwargs) -> None:
        """Safely register a handler; skip it if dependencies are unavailable."""
        try:
            module = importlib.import_module(module_path)
            handler_cls = getattr(module, class_name)
            self.handlers[intent_type] = handler_cls(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Skipping {class_name}: {e}")
    
    def process_command(self, command_text: str) -> str:
        """Process a voice command and return response"""
        try:
            logger.info(f"Processing command: {command_text}")
            if self.broadcast: self.broadcast('processing')

            # --- Multi-turn: fill in a pending slot ---
            if self._pending_intent and self._pending_slot:
                intent = self._pending_intent
                intent.parameters[self._pending_slot] = command_text
                self._pending_slot = None

                # Check if there are still missing slots
                follow_up = self._get_next_missing_slot(intent)
                if follow_up:
                    self._pending_slot = follow_up
                    question = _REQUIRED_SLOTS[intent.type][follow_up]
                    self.tts.speak(question, intent.response_language)
                    return question

                self._pending_intent = None
                logger.info(f"Filled slot; proceeding with {intent.type.value}")
            else:
                intent = self.llm.classify_intent(command_text)
                logger.info(f"Classified as: {intent.type.value} (language: {intent.language})")

                # Check for missing required slots before routing to handler
                missing = self._get_next_missing_slot(intent)
                if missing:
                    self._pending_intent = intent
                    self._pending_slot = missing
                    question = _REQUIRED_SLOTS[intent.type][missing]
                    self.tts.speak(question, intent.response_language)
                    return question
            
            # Find appropriate handler
            handler = self.handlers.get(intent.type)
            
            if handler and handler.can_handle(intent):
                # Execute handler
                response = handler.handle(intent)
                logger.info(f"Handler response: {response}")
                
                # Store in conversation history
                self.conversation_repo.add_exchange(
                    user_input=command_text,
                    assistant_response=response,
                    intent_type=intent.type.value
                )
                
                # Speak response
                if self.broadcast: self.broadcast('speaking')
                self.tts.speak(response, intent.response_language)
                
                if self.broadcast: self.broadcast('idle')
                return response
            else:
                # Unknown intent
                logger.warning(f"No handler for intent: {intent.type.value}")
                
                if intent.response_language == 'hi':
                    response = "मुझे समझ नहीं आया। कृपया दोबारा कहें।"
                else:
                    response = "I didn't understand that. Could you please repeat?"
                
                self.tts.speak(response, intent.response_language)
                return response
                
        except Exception as e:
            logger.error(f"Error processing command: {e}", exc_info=True)
            self._pending_intent = None
            self._pending_slot = None
            response = "Sorry, I had trouble processing that command"
            self.tts.speak(response, 'en')
            return response

    def _get_next_missing_slot(self, intent: Intent) -> Optional[str]:
        """Return the name of the first required-but-empty slot, or None if complete."""
        required = _REQUIRED_SLOTS.get(intent.type, {})
        for slot, _question in required.items():
            val = intent.parameters.get(slot)
            if not val or (isinstance(val, str) and not val.strip()):
                return slot
        return None

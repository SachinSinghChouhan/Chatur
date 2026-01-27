"""Command processor - integrates all handlers"""

from chatur.core.llm import LLMClient
from chatur.core.tts import TextToSpeech
from chatur.handlers.reminder import ReminderHandler
from chatur.handlers.timer import TimerHandler
from chatur.handlers.notes import NotesHandler
from chatur.handlers.qa import QAHandler
from chatur.handlers.app_launcher import AppLauncherHandler
from chatur.handlers.media_control import MediaControlHandler
from chatur.handlers.file_search import FileSearchHandler
from chatur.handlers.weather import WeatherHandler
from chatur.handlers.system_info import SystemInfoHandler
from chatur.handlers.math import MathHandler
from chatur.handlers.calendar import CalendarHandler
from chatur.handlers.email import GmailHandler
from chatur.storage.conversation_repository import ConversationRepository
from chatur.models.intent import IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.command_processor')

class CommandProcessor:
    """Process voice commands and execute actions"""
    
    def __init__(self, llm_client: LLMClient, tts_engine: TextToSpeech):
        self.llm = llm_client
        self.tts = tts_engine
        self.conversation_repo = ConversationRepository()
        
        # Initialize handlers
        self.handlers = {
            IntentType.REMINDER: ReminderHandler(),
            IntentType.TIMER: TimerHandler(tts_engine=tts_engine),
            IntentType.NOTE: NotesHandler(),
            IntentType.QUESTION: QAHandler(llm_client, self.conversation_repo),
            IntentType.APP_LAUNCH: AppLauncherHandler(),
            IntentType.MEDIA_CONTROL: MediaControlHandler(),
            IntentType.FILE_SEARCH: FileSearchHandler(),
            IntentType.WEATHER: WeatherHandler(),
            IntentType.SYSTEM_INFO: SystemInfoHandler(),
            IntentType.MATH: MathHandler(),
            IntentType.CALENDAR: CalendarHandler(),
            IntentType.EMAIL: GmailHandler(),
        }
        
        logger.info("Command processor initialized with all handlers")
    
    def process_command(self, command_text: str) -> str:
        """Process a voice command and return response"""
        try:
            logger.info(f"Processing command: {command_text}")
            
            # Classify intent
            intent = self.llm.classify_intent(command_text)
            logger.info(f"Classified as: {intent.type.value} (language: {intent.language})")
            
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
                self.tts.speak(response, intent.response_language)
                
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
            response = "Sorry, I had trouble processing that command"
            self.tts.speak(response, 'en')
            return response

"""Reminder handler"""

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.storage.reminder_repository import ReminderRepository
from chatur.utils.time_parser import parse_time
from chatur.utils.logger import setup_logger
from chatur.utils.responses import ResponseBuilder

logger = setup_logger('chatur.handlers.reminder')

class ReminderHandler(BaseHandler):
    """Handler for reminder intents"""
    
    def __init__(self):
        self.repo = ReminderRepository()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a reminder intent"""
        return intent.type == IntentType.REMINDER
    
    def handle(self, intent: Intent) -> str:
        """Create a reminder"""
        try:
            text = intent.parameters.get('text', 'Reminder')
            time_str = intent.parameters.get('time', 'in 1 hour')
            language = intent.response_language
            
            scheduled_time = parse_time(time_str)
            reminder_id = self.repo.create(text, scheduled_time, intent.language)
            
            logger.info(f"Created reminder #{reminder_id}: '{text}' at {scheduled_time}")
            
            time_formatted = scheduled_time.strftime('%I:%M %p on %B %d')
            
            return ResponseBuilder.get(language, {
                'en': f"Reminder set: {text} at {time_formatted}",
                'hi': f"रिमाइंडर सेट कर दिया गया है: {text} - {time_formatted}"
            })
                
        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            return ResponseBuilder.error(intent.response_language, "set that reminder")

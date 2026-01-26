"""Notes handler"""

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.storage.notes_repository import NotesRepository
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.notes')

class NotesHandler(BaseHandler):
    """Handler for note storage and retrieval"""
    
    def __init__(self):
        self.repo = NotesRepository()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a note intent"""
        return intent.type == IntentType.NOTE
    
    def handle(self, intent: Intent) -> str:
        """Store or retrieve a note"""
        try:
            action = intent.parameters.get('action', 'store')  # store or retrieve
            key = intent.parameters.get('key', '')
            value = intent.parameters.get('value', '')
            
            if action == 'store' and key and value:
                # Store note
                self.repo.create_or_update(key, value, intent.language)
                logger.info(f"Stored note: {key} = {value}")
                
                if intent.response_language == 'hi':
                    return f"याद रख लिया: {key}"
                else:
                    return f"Got it, I'll remember that {key}"
            
            elif action == 'retrieve' and key:
                # Retrieve note
                note = self.repo.get(key)
                if note:
                    logger.info(f"Retrieved note: {key} = {note['value']}")
                    return note['value']
                else:
                    if intent.response_language == 'hi':
                        return f"मुझे {key} याद नहीं है"
                    else:
                        return f"I don't remember anything about {key}"
            
            else:
                if intent.response_language == 'hi':
                    return "कृपया स्पष्ट रूप से बताएं"
                else:
                    return "Please tell me what to remember or what you want to know"
                
        except Exception as e:
            logger.error(f"Error handling note: {e}")
            if intent.response_language == 'hi':
                return "नोट सेव करने में समस्या हुई"
            else:
                return "Sorry, I had trouble with that note"

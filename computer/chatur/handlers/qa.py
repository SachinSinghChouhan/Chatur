"""Question answering handler"""

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.qa')

class QAHandler(BaseHandler):
    """Handler for question answering"""
    
    def __init__(self, llm_client, conversation_repo=None):
        self.llm = llm_client
        self.conversation_repo = conversation_repo
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a question intent"""
        return intent.type == IntentType.QUESTION
    
    def handle(self, intent: Intent) -> str:
        """Answer a question using LLM"""
        try:
            question = intent.parameters.get('question', '')
            
            if not question:
                if intent.response_language == 'hi':
                    return "कृपया अपना सवाल पूछें"
                else:
                    return "What would you like to know?"
            
            logger.info(f"Answering question: {question}")
            
            # Fetch conversation history if repo is available
            history = None
            if self.conversation_repo:
                # Get last 5 exchanges
                history = self.conversation_repo.get_recent_exchanges(limit=5)
            
            answer = self.llm.answer_question(question, intent.response_language, conversation_history=history)
            
            return answer
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            if intent.response_language == 'hi':
                return "मुझे इसका जवाब देने में समस्या हो रही है"
            else:
                return "I'm having trouble answering that question right now"

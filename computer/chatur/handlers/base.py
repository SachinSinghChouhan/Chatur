"""Base handler interface"""

from abc import ABC, abstractmethod
from chatur.models.intent import Intent

class BaseHandler(ABC):
    """Abstract base class for all action handlers"""
    
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can process the intent"""
        pass
    
    @abstractmethod
    def handle(self, intent: Intent) -> str:
        """Process the intent and return response text"""
        pass

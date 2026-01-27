"""Intent data models"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class IntentType(Enum):
    """Types of intents the assistant can handle"""
    REMINDER = "reminder"
    TIMER = "timer"
    NOTE = "note"
    QUESTION = "question"
    APP_LAUNCH = "app_launch"
    MEDIA_CONTROL = "media_control"
    FILE_SEARCH = "file_search"
    WEATHER = "weather"
    SYSTEM_INFO = "system_info"
    MATH = "math"
    CALENDAR = "calendar"
    EMAIL = "email"
    TASK = "task"
    UNKNOWN = "unknown"

@dataclass
class Intent:
    """Intent classification result"""
    type: IntentType
    language: str  # 'en', 'hi', 'hinglish'
    parameters: Dict[str, Any]
    response_language: str
    confidence: float = 1.0

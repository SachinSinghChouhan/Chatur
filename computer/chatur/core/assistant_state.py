"""State machine for assistant activation and control"""

from enum import Enum
from typing import Optional, Callable
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.state')

class AssistantState(Enum):
    """Assistant operational states"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"

class AssistantStateMachine:
    """Manages assistant state transitions and broadcasts"""
    
    def __init__(self, broadcast_callback: Optional[Callable] = None):
        self._state = AssistantState.IDLE
        self.broadcast_callback = broadcast_callback
        logger.info("State machine initialized in IDLE state")
    
    @property
    def state(self) -> AssistantState:
        return self._state
    
    def transition_to(self, new_state: AssistantState):
        """Transition to a new state and broadcast the change"""
        if self._state == new_state:
            return
        
        old_state = self._state
        self._state = new_state
        
        logger.info(f"State transition: {old_state.value} → {new_state.value}")
        
        # Broadcast state change to UI
        if self.broadcast_callback:
            self.broadcast_callback('state_change', {'state': new_state.value})
    
    def is_idle(self) -> bool:
        return self._state == AssistantState.IDLE
    
    def is_active(self) -> bool:
        return self._state != AssistantState.IDLE

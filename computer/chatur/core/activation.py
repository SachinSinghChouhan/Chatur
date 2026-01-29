"""Keyboard activation handler for on-demand assistant triggering"""

from pynput import keyboard
from typing import Callable
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.activation')

class ActivationListener:
    """Listens for keyboard activation (Ctrl+Space) to trigger assistant"""
    
    def __init__(self, on_activate: Callable):
        self.on_activate = on_activate
        self.listener = None
        self._active = False
    
    def start(self):
        """Start listening for activation hotkey"""
        if self._active:
            logger.warning("Activation listener already running")
            return
        
        try:
            # Global hotkey: Ctrl+Space
            self.listener = keyboard.GlobalHotKeys({
                '<ctrl>+<space>': self._handle_activation
            })
            self.listener.start()
            self._active = True
            logger.info("Activation listener started (Hotkey: Ctrl+Space)")
        except Exception as e:
            logger.error(f"Failed to start activation listener: {e}")
    
    def _handle_activation(self):
        """Called when user presses Ctrl+Space"""
        logger.info("Activation hotkey triggered by user")
        try:
            self.on_activate()
        except Exception as e:
            logger.error(f"Error in activation callback: {e}", exc_info=True)
    
    def stop(self):
        """Stop listening"""
        if self.listener:
            self.listener.stop()
            self._active = False
            logger.info("Activation listener stopped")

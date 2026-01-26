"""Timer handler"""

import threading
import time
from datetime import datetime, timedelta
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.time_parser import parse_duration
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.timer')

class TimerHandler(BaseHandler):
    """Handler for timer intents"""
    
    def __init__(self, tts_engine=None, notification_callback=None):
        self.tts_engine = tts_engine
        self.notification_callback = notification_callback
        self.active_timers = {}
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a timer intent"""
        return intent.type == IntentType.TIMER
    
    def handle(self, intent: Intent) -> str:
        """Start a timer"""
        try:
            duration_str = intent.parameters.get('duration', '5 minutes')
            label = intent.parameters.get('label', 'Timer')
            
            # Parse duration
            duration_seconds = parse_duration(duration_str)
            
            # Start timer in background thread
            timer_thread = threading.Thread(
                target=self._run_timer,
                args=(duration_seconds, label, intent.response_language)
            )
            timer_thread.daemon = True
            timer_thread.start()
            
            logger.info(f"Started timer: {label} for {duration_seconds} seconds")
            
            # Format response
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            
            if intent.response_language == 'hi':
                if minutes > 0:
                    return f"टाइमर शुरू हो गया है: {minutes} मिनट"
                else:
                    return f"टाइमर शुरू हो गया है: {seconds} सेकंड"
            else:
                if minutes > 0:
                    return f"Timer started for {minutes} minute{'s' if minutes != 1 else ''}"
                else:
                    return f"Timer started for {seconds} second{'s' if seconds != 1 else ''}"
                
        except Exception as e:
            logger.error(f"Error starting timer: {e}")
            if intent.response_language == 'hi':
                return "टाइमर शुरू करने में समस्या हुई"
            else:
                return "Sorry, I couldn't start that timer"
    
    def _run_timer(self, duration_seconds: int, label: str, language: str):
        """Run timer in background"""
        time.sleep(duration_seconds)
        
        # Timer complete
        logger.info(f"Timer complete: {label}")
        
        # Print notification (avoid TTS threading issues)
        if language == 'hi':
            message = f"⏰ टाइमर पूरा हो गया: {label}"
        else:
            message = f"⏰ Timer complete: {label}"
        
        print(f"\n{message}\n")
        
        # Show toast notification if callback provided
        if self.notification_callback:
            self.notification_callback("Timer Complete", label)

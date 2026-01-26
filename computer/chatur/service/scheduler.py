"""Background scheduler for reminders and timers"""

import threading
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from chatur.storage.reminder_repository import ReminderRepository
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.scheduler')

class ReminderScheduler:
    """Background scheduler for checking and triggering reminders"""
    
    def __init__(self, tts_engine=None, notification_callback=None):
        self.tts_engine = tts_engine
        self.notification_callback = notification_callback
        self.reminder_repo = ReminderRepository()
        self.scheduler = BackgroundScheduler()
        self.running = False
        
        logger.info("Reminder scheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        # Add job to check reminders (interval from config)
        interval = config.scheduler_interval
        self.scheduler.add_job(
            self._check_reminders,
            'interval',
            seconds=interval,
            id='check_reminders',
            replace_existing=True
        )
        
        self.scheduler.start()
        self.running = True
        logger.info(f"Reminder scheduler started (checking every {interval} seconds)")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return
        
        self.scheduler.shutdown()
        self.running = False
        logger.info("Reminder scheduler stopped")
    
    def _check_reminders(self):
        """Check for due reminders and trigger them"""
        try:
            now = datetime.now()
            
            # Get all pending reminders
            reminders = self.reminder_repo.get_pending_reminders()
            
            for reminder in reminders:
                reminder_time = datetime.fromisoformat(reminder['scheduled_time'])
                
                # Check if reminder is due (window from config)
                time_diff = (reminder_time - now).total_seconds()
                window = config.reminder_window
                
                if -window <= time_diff <= window:  # Due within configured window
                    logger.info(f"Triggering reminder: {reminder['text']}")
                    self._trigger_reminder(reminder)
                    
                    # Mark as completed
                    self.reminder_repo.complete_reminder(reminder['id'])
        
        except Exception as e:
            logger.error(f"Error checking reminders: {e}", exc_info=True)
    
    def _trigger_reminder(self, reminder):
        """Trigger a reminder notification"""
        try:
            text = reminder['text']
            language = reminder.get('language', 'en')
            
            # Speak reminder
            if self.tts_engine:
                if language == 'hi':
                    message = f"रिमाइंडर: {text}"
                else:
                    message = f"Reminder: {text}"
                
                # Speak in a separate thread to avoid blocking
                threading.Thread(
                    target=self.tts_engine.speak,
                    args=(message, language),
                    daemon=True
                ).start()
            
            # Show notification
            if self.notification_callback:
                self.notification_callback("Reminder", text)
            
            # Console notification
            print(f"\n🔔 REMINDER: {text}\n")
            
        except Exception as e:
            logger.error(f"Error triggering reminder: {e}", exc_info=True)

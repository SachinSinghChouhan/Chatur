"""Reminder repository for database operations"""

from datetime import datetime
from typing import List, Optional
from chatur.storage.repository import BaseRepository

class ReminderRepository(BaseRepository):
    """Repository for reminder operations"""
    
    def create(self, text: str, scheduled_time: datetime, language: str = 'en') -> int:
        """Create a new reminder"""
        query = '''
            INSERT INTO reminders (text, scheduled_time, language)
            VALUES (?, ?, ?)
        '''
        cursor = self.execute(query, (text, scheduled_time.isoformat(), language))
        return cursor.lastrowid
    
    def create_reminder(self, text: str, reminder_time: str, language: str = 'en') -> int:
        """Create a new reminder (alternative method for scheduler)"""
        query = '''
            INSERT INTO reminders (text, scheduled_time, language, triggered)
            VALUES (?, ?, ?, 0)
        '''
        cursor = self.execute(query, (text, reminder_time, language))
        return cursor.lastrowid
    
    def get_pending(self) -> List[dict]:
        """Get all pending reminders that are due"""
        query = '''
            SELECT * FROM reminders 
            WHERE triggered = 0 AND scheduled_time <= datetime('now')
            ORDER BY scheduled_time ASC
        '''
        return self.fetchall(query)
    
    def get_pending_reminders(self) -> List[dict]:
        """Get all pending (not triggered) reminders"""
        query = '''
            SELECT * FROM reminders 
            WHERE triggered = 0 
            ORDER BY scheduled_time ASC
        '''
        return self.fetchall(query)
    
    def mark_triggered(self, reminder_id: int) -> None:
        """Mark reminder as triggered"""
        query = 'UPDATE reminders SET triggered = 1 WHERE id = ?'
        self.execute(query, (reminder_id,))
    
    def complete_reminder(self, reminder_id: int) -> None:
        """Mark reminder as completed (alias for mark_triggered)"""
        self.mark_triggered(reminder_id)

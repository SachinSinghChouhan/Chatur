"""Notes repository"""

from typing import List, Optional
from chatur.storage.repository import BaseRepository

class NotesRepository(BaseRepository):
    """Repository for notes operations"""
    
    def create_or_update(self, key: str, value: str, language: str = 'en') -> int:
        """Create or update a note"""
        query = '''
            INSERT INTO notes (key, value, language, updated_at)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                language = excluded.language,
                updated_at = datetime('now')
        '''
        cursor = self.execute(query, (key, value, language))
        return cursor.lastrowid
    
    def get(self, key: str) -> Optional[dict]:
        """Get a note by key"""
        query = 'SELECT * FROM notes WHERE key = ?'
        return self.fetchone(query, (key,))

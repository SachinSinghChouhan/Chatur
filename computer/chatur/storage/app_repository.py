"""App repository"""

from typing import List, Optional
from chatur.storage.repository import BaseRepository

class AppRepository(BaseRepository):
    """Repository for app operations"""
    
    def get_by_name(self, name: str) -> Optional[dict]:
        """Get app by name or alias"""
        query = '''
            SELECT * FROM apps 
            WHERE name = ? OR aliases LIKE ?
            LIMIT 1
        '''
        return self.fetchone(query, (name.lower(), f'%{name.lower()}%'))
    
    def get_all(self) -> List[dict]:
        """Get all registered apps"""
        query = 'SELECT * FROM apps ORDER BY display_name'
        return self.fetchall(query)

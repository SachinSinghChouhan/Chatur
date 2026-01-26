"""Base repository for database operations"""

from typing import List, Optional
import sqlite3
from pathlib import Path
import os

DB_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'computer.db'

class BaseRepository:
    """Base class for all repositories"""
    
    def __init__(self):
        self.db_path = DB_PATH
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query and return cursor"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Fetch one row as dictionary"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def fetchall(self, query: str, params: tuple = ()) -> List[dict]:
        """Fetch all rows as list of dictionaries"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

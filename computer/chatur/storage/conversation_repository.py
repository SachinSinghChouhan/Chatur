"""Conversation history repository"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from chatur.storage.repository import BaseRepository
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.storage.conversation')


class ConversationRepository(BaseRepository):
    """Repository for conversation history"""
    
    def __init__(self):
        super().__init__()
        self._create_table()
    
    def _create_table(self):
        """Create conversation history table"""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    assistant_response TEXT NOT NULL,
                    intent_type TEXT,
                    session_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster queries
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_conversation_timestamp 
                ON conversation_history(timestamp DESC)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_conversation_session 
                ON conversation_history(session_id)
            ''')
    
    def add_exchange(self, user_input: str, assistant_response: str, 
                    intent_type: str = None, session_id: str = None) -> int:
        """
        Add a conversation exchange
        
        Args:
            user_input: What the user said
            assistant_response: What the assistant responded
            intent_type: Type of intent (optional)
            session_id: Session identifier (optional)
        
        Returns:
            ID of the created record
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO conversation_history 
                (user_input, assistant_response, intent_type, session_id)
                VALUES (?, ?, ?, ?)
            ''', (user_input, assistant_response, intent_type, session_id))
            
            return cursor.lastrowid
    
    def get_recent_exchanges(self, limit: int = 10, session_id: str = None) -> List[Dict]:
        """
        Get recent conversation exchanges
        
        Args:
            limit: Maximum number of exchanges to return
            session_id: Filter by session (optional)
        
        Returns:
            List of conversation exchanges
        """
        with self._get_connection() as conn:
            if session_id:
                cursor = conn.execute('''
                    SELECT id, user_input, assistant_response, intent_type, 
                           session_id, timestamp
                    FROM conversation_history
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (session_id, limit))
            else:
                cursor = conn.execute('''
                    SELECT id, user_input, assistant_response, intent_type, 
                           session_id, timestamp
                    FROM conversation_history
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            exchanges = []
            for row in cursor.fetchall():
                exchanges.append({
                    'id': row[0],
                    'user_input': row[1],
                    'assistant_response': row[2],
                    'intent_type': row[3],
                    'session_id': row[4],
                    'timestamp': row[5]
                })
            
            # Return in chronological order (oldest first)
            return list(reversed(exchanges))
    
    def get_last_exchange(self) -> Optional[Dict]:
        """
        Get the most recent exchange
        
        Returns:
            Last exchange or None
        """
        exchanges = self.get_recent_exchanges(limit=1)
        return exchanges[0] if exchanges else None
    
    def clear_old_history(self, days: int = 30):
        """
        Clear conversation history older than specified days
        
        Args:
            days: Number of days to keep
        """
        with self._get_connection() as conn:
            conn.execute('''
                DELETE FROM conversation_history
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            deleted = conn.total_changes
            logger.info(f"Cleared {deleted} old conversation records")
    
    def get_conversation_context(self, limit: int = 5) -> str:
        """
        Get recent conversation as formatted context for LLM
        
        Args:
            limit: Number of recent exchanges to include
        
        Returns:
            Formatted conversation context
        """
        exchanges = self.get_recent_exchanges(limit=limit)
        
        if not exchanges:
            return ""
        
        context_lines = ["Recent conversation:"]
        for exchange in exchanges:
            context_lines.append(f"User: {exchange['user_input']}")
            context_lines.append(f"Assistant: {exchange['assistant_response']}")
        
        return "\n".join(context_lines)

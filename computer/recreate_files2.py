"""Script to create all remaining files"""

import os

os.chdir(r'd:\protocol\computer')

# LLM Client
llm_content = '''"""OpenAI LLM integration for intent classification and Q&A"""

import os
import json
from openai import OpenAI
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = setup_logger('chatur.llm')

INTENT_CLASSIFIER_PROMPT = """You are Computer, a personal voice assistant. Analyze user commands and return JSON.

Supported intents:
- reminder: Set time-based reminders
- timer: Set countdown timers
- note: Store/retrieve facts
- question: Answer general questions
- app_launch: Open applications
- media_control: Control music playback
- unknown: Cannot understand

Response format:
{
  "intent": "reminder|timer|note|question|app_launch|media_control|unknown",
  "language": "en|hi|hinglish",
  "parameters": {},
  "response_language": "en|hi"
}

Examples:
Input: "Remind me to call mom at 5 PM"
Output: {"intent":"reminder","language":"en","parameters":{"text":"call mom","time":"17:00"},"response_language":"en"}

Input: "Kal subah 8 baje meeting ka reminder"
Output: {"intent":"reminder","language":"hi","parameters":{"text":"meeting","time":"tomorrow 08:00"},"response_language":"hi"}

Input: "Set timer for 5 minutes"
Output: {"intent":"timer","language":"en","parameters":{"duration_seconds":300},"response_language":"en"}

Input: "Open Chrome"
Output: {"intent":"app_launch","language":"en","parameters":{"app_name":"chrome"},"response_language":"en"}

Input: "Play music"
Output: {"intent":"media_control","language":"en","parameters":{"action":"play"},"response_language":"en"}

Now analyze: {user_command}"""

class LLMClient:
    """OpenAI API client for intent classification and Q&A"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        logger.info("LLM client initialized")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def classify_intent(self, text: str) -> Intent:
        """Classify user intent from text"""
        try:
            prompt = INTENT_CLASSIFIER_PROMPT.format(user_command=text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful intent classifier. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            result = json.loads(response.choices[0].message.content)
            
            intent = Intent(
                type=IntentType(result.get('intent', 'unknown')),
                language=result.get('language', 'en'),
                parameters=result.get('parameters', {}),
                response_language=result.get('response_language', 'en')
            )
            
            logger.info(f"Classified intent: {intent.type.value} (language: {intent.language})")
            return intent
            
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            # Return unknown intent on error
            return Intent(
                type=IntentType.UNKNOWN,
                language='en',
                parameters={},
                response_language='en',
                confidence=0.0
            )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def answer_question(self, question: str, language: str = 'en') -> str:
        """Answer a question using OpenAI"""
        try:
            system_prompt = f"""You are Computer, a helpful voice assistant. Answer the user's question concisely in {language}.

Keep responses:
- Short (2-3 sentences max)
- Conversational
- In the same language as the question"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Generated answer for question: {question[:50]}...")
            return answer
            
        except Exception as e:
            logger.error(f"Question answering error: {e}")
            return "I'm having trouble answering that right now. Please try again later."
'''

with open('chatur/core/llm.py', 'w', encoding='utf-8') as f:
    f.write(llm_content)

print("Created: chatur/core/llm.py")

# Base Repository
repo_content = '''"""Base repository for database operations"""

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
'''

with open('chatur/storage/repository.py', 'w', encoding='utf-8') as f:
    f.write(repo_content)

print("Created: chatur/storage/repository.py")

print("\\nAll core files created successfully!")

"""Google Tasks Handler"""

import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import difflib

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.tasks')

SCOPES = ['https://www.googleapis.com/auth/tasks']
TOKEN_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'token.json'
CREDENTIALS_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'credentials.json'

class GoogleTasksHandler(BaseHandler):
    """Handler for Google Tasks interactions"""
    
    def __init__(self):
        self.service = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Google Tasks API"""
        creds = None
        try:
            if TOKEN_PATH.exists():
                # We expect the token to already have the 'tasks' scope if setup_google.py was run
                creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
                
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
            if creds and creds.valid:
                self.service = build('tasks', 'v1', credentials=creds)
                logger.info("Google Tasks service initialized")
            else:
                if CREDENTIALS_PATH.exists():
                     logger.info("Credentials found but require re-authorization for Tasks scope.")
                else:
                     logger.warning("No credentials found for Google Tasks.")
                     
        except Exception as e:
            logger.error(f"Google Tasks auth failed: {e}")
            self.service = None

    def can_handle(self, intent: Intent) -> bool:
        return intent.type == IntentType.TASK
        
    def handle(self, intent: Intent) -> str:
        """Process task intent"""
        if not self.service:
             if CREDENTIALS_PATH.exists():
                return "I need permission to access your Google Tasks. Please run the setup script again."
             return "I need Google credentials to manage tasks."
            
        action = intent.parameters.get('action', 'add')
        
        try:
            if action == 'add':
                title = intent.parameters.get('title')
                if not title:
                    return "What should I add to your list?"
                return self._add_task(title)
            elif action == 'list':
                return self._list_tasks()
            elif action == 'complete':
                title = intent.parameters.get('title')
                if not title:
                    return "Which task should I complete?"
                return self._complete_task(title)
            else:
                return "I'm not sure what you want to do with your tasks."
        except Exception as e:
            logger.error(f"Task operation failed: {e}")
            return "Sorry, something went wrong with your task list."

    def _add_task(self, title: str) -> str:
        """Add a new task to the default list, optionally extracting a due date"""
        try:
            import datetime
            from dateutil import parser
            
            due_date = None
            clean_title = title
            
            # Simple heuristic to extract "at 5 PM", "tomorrow", etc.
            # We use fuzzy parsing on the whole string to find a date
            try:
                # This is a basic implementation. For production, use specific extraction or regex
                # to avoid removing parts of the actual task name. 
                # Here we check if the string *contains* a time-like phrase.
                # A better approach is to let the user specify parsing logic or use the extracted time.
                
                # We will check specific keywords to attempt parsing
                time_keywords = [' at ', ' on ', ' tomorrow', ' today', ' next ', ' in ']
                if any(k in title.lower() for k in time_keywords):
                    # Attempt to parse. fuzz=True allows skipping unknown tokens
                    dt = parser.parse(title, fuzzy=True)
                    
                    # If we found a date/time in the future (or today)
                    if dt:
                        # Ensure it's unaware or UTC for API
                        # Google Tasks 'due' is technically a date string YYYY-MM-DDT00:00:00.000Z 
                        # but standard usage often implies the deadline.
                        # API Requirement: RFC 3339 timestamp.
                        due_date = dt.isoformat() + 'Z'
                        
                        # Can we clean the title? It's hard to know exactly what substring was the date
                        # without a dedicated NER library like spacy or dateparser with span info.
                        # For now, we will NOT aggressively clean the title to avoid deleting useful info.
                        # We will just append the parsed time to the confirmation message.
            except Exception:
                # If parsing fails, just ignore/proceed without due date
                pass

            task_body = {'title': clean_title}
            if due_date:
                task_body['due'] = due_date

            result = self.service.tasks().insert(tasklist='@default', body=task_body).execute()
            
            msg = f"Added '{clean_title}' to your tasks"
            if due_date:
                # Format for display
                display_time = dt.strftime("%I:%M %p, %b %d")
                msg += f", due {display_time}."
            else:
                msg += "."
                
            return msg
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            raise e

    def _list_tasks(self) -> str:
        """List upcoming tasks"""
        try:
            # Fetch pending tasks
            results = self.service.tasks().list(tasklist='@default', maxResults=10, showCompleted=False).execute()
            items = results.get('items', [])
            
            if not items:
                return "You have no pending tasks."
                
            response_lines = ["Here are your tasks:"]
            for item in items:
                response_lines.append(f"- {item['title']}")
                
            return "\n".join(response_lines)
            
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            raise e

    def _complete_task(self, title: str) -> str:
        """Mark a task as complete by fuzzy matching the title"""
        try:
            # 1. Fetch current tasks
            results = self.service.tasks().list(tasklist='@default', showCompleted=False).execute()
            items = results.get('items', [])
            
            if not items:
                return "You have no pending tasks to complete."
            
            # 2. Fuzzy match to find the best candidate
            task_titles = [item['title'] for item in items]
            
            # Find closest match
            matches = difflib.get_close_matches(title, task_titles, n=1, cutoff=0.4)
            
            if not matches:
                return f"I couldn't find a task named '{title}'."
                
            matched_title = matches[0]
            
            # Find the item ID for the matched title
            task_item = next((item for item in items if item['title'] == matched_title), None)
            
            if not task_item:
                return "Error identifying the task ID."

            # 3. Update the task status to 'completed'
            task_item['status'] = 'completed'
            self.service.tasks().update(tasklist='@default', task=task_item['id'], body=task_item).execute()
            
            return f"Completed task: {matched_title}"
            
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            raise e

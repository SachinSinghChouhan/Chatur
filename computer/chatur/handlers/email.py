"""Gmail Handler"""

import os
import base64
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.email')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'credentials.json'
TOKEN_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'token.json'

class GmailHandler(BaseHandler):
    """Handler for Gmail interactions"""
    
    def __init__(self):
        self.service = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Gmail API (reusing token from Calendar if possible)"""
        creds = None
        
        try:
            # Load existing token
            if TOKEN_PATH.exists():
                creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
                
            # Refresh if expired via valid refresh token
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
            # If no valid credentials, we need to login
            # Note: Assuming manual/setup logic handles initial token creation
            if not creds or not creds.valid:
                if CREDENTIALS_PATH.exists():
                    logger.info("Credentials found, waiting for authorization execution.")
                    pass
                else:
                    logger.warning(f"No credentials.json found at {CREDENTIALS_PATH}")
                    
            if creds and creds.valid:
                self.service = build('gmail', 'v1', credentials=creds)
                logger.info("Gmail service initialized successfully")
                
        except Exception as e:
            logger.error(f"Gmail authentication failed: {e}")
            self.service = None

    def can_handle(self, intent: Intent) -> bool:
        return intent.type == IntentType.EMAIL
        
    def handle(self, intent: Intent) -> str:
        """Process email intent"""
        if not self.service:
            if CREDENTIALS_PATH.exists():
                 return "I have your credentials but need authorization. Please run the setup again or check permissions."
            return "I need Google credentials to access your emails. Please setup credentials.json."
            
        action = intent.parameters.get('action', 'read')
        
        try:
            if action == 'read' or action == 'check':
                count = intent.parameters.get('count', 3)
                return self._read_emails(count)
            elif action == 'search':
                query = intent.parameters.get('query')
                if not query:
                    return "What emails should I look for?"
                return self._search_emails(query)
            else:
                return "I'm not sure what you want to do with your email."
        except Exception as e:
            logger.error(f"Email operation failed: {e}")
            return "Sorry, something went wrong accessing your emails."

    def _read_emails(self, max_results: int = 3) -> str:
        """Read latest unread emails"""
        try:
            # List messages in INBOX that are UNREAD
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['INBOX', 'UNREAD'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return "You have no unread emails."
                
            response_lines = [f"Here are your last {len(messages)} unread emails:"]
            
            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                payload = txt['payload']
                headers = payload['headers']
                
                subject = "No Subject"
                sender = "Unknown"
                
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
                        # Clean up sender name
                        if '<' in sender:
                            sender = sender.split('<')[0].strip().replace('"', '')
                
                response_lines.append(f"- From {sender}: {subject}")
                
            return "\n".join(response_lines)
            
        except Exception as e:
            logger.error(f"Error reading emails: {e}")
            raise e

    def _search_emails(self, query: str) -> str:
        """Search emails"""
        try:
            # Search query
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=3
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return f"I couldn't find any emails matching '{query}'."
                
            response_lines = [f"Found {len(messages)} recent emails properly matching '{query}':"]
            
            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                payload = txt['payload']
                headers = payload['headers']
                
                subject = "No Subject"
                sender = "Unknown"
                
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
                        if '<' in sender:
                            sender = sender.split('<')[0].strip().replace('"', '')

                response_lines.append(f"- {sender}: {subject}")
                
            return "\n".join(response_lines)
            
        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            raise e

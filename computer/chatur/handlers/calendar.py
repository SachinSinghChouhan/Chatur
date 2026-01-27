"""Google Calendar Handler"""

import os
import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import dateutil.parser

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.calendar')

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'credentials.json'
TOKEN_PATH = Path(os.getenv('APPDATA')) / 'Computer' / 'token.json'

class CalendarHandler(BaseHandler):
    """Handler for Google Calendar interactions"""
    
    def __init__(self):
        self.service = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        try:
            # Load existing token
            if TOKEN_PATH.exists():
                creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
                
            # Refresh if expired via valid refresh token
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
            # If no valid credentials, we need to login
            # NOTE: We can't do interactive login easily in a background/voice app
            # Ideally this is done once manually via a setup script
            if not creds or not creds.valid:
                if CREDENTIALS_PATH.exists():
                    logger.info("Credentials found, but assuming token generation needed externally or UI interaction required first time.")
                    # For now, we only support if token already exists or credentials file is present for manual run
                    # If we run this interactively (console mode), we can launch browser
                    pass
                else:
                    logger.warning(f"No credentials.json found at {CREDENTIALS_PATH}")
                    
            if creds and creds.valid:
                self.service = build('calendar', 'v3', credentials=creds)
                logger.info("Calendar service initialized successfully")
                
        except Exception as e:
            logger.error(f"Calendar authentication failed: {e}")
            self.service = None

    def can_handle(self, intent: Intent) -> bool:
        return intent.type == IntentType.CALENDAR
        
    def handle(self, intent: Intent) -> str:
        """Process calendar intent"""
        if not self.service:
             # Attempt re-auth locally just in case
            if CREDENTIALS_PATH.exists():
                 return "I found your credentials but need you to authorize me first. Run the setup wizard."
            return "I need Google Calendar credentials to access your schedule. Please add credentials.json to your Computer folder."
            
        action = intent.parameters.get('action', 'list')
        
        try:
            if action == 'list':
                return self._list_events(intent.parameters)
            elif action == 'create':
                return self._create_event(intent.parameters)
            else:
                return "I'm not sure what you want to do with your calendar."
        except Exception as e:
            logger.error(f"Calendar operation failed: {e}")
            return "Sorry, something went wrong accessing your calendar."

    def _list_events(self, params: dict) -> str:
        """List upcoming events"""
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            # Default to 5 events
            max_results = 5
            
            events_result = self.service.events().list(
                calendarId='primary', 
                timeMin=now,
                maxResults=max_results, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "You have no upcoming events."
                
            response_lines = ["Here are your upcoming events:"]
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                # Format time nicely
                try:
                    dt = dateutil.parser.parse(start)
                    # If today, say "Today at X", else "Tomorrow/Day at X"
                    # For now simply standard string
                    time_str = dt.strftime("%A at %I:%M %p")
                except:
                    time_str = start
                    
                response_lines.append(f"- {event['summary']} on {time_str}")
                
            return "\n".join(response_lines)
            
        except Exception as e:
            logger.error(f"Error listing events: {e}")
            raise e

    def _create_event(self, params: dict) -> str:
        """Create a new event"""
        summary = params.get('summary', 'New Event')
        time_str = params.get('time') # "tomorrow at 5pm" or similar natural text
        
        if not time_str:
            return "When should I schedule that?"
            
        try:
            # Use dateutil to parse the natural language time (imperfect, but decent start)
            # Ideally LLM gives us ISO format, but let's assume LLM passes "2024-05-05 17:00" or we parse natural 
            # We already have dateutil installed
            
            # If LLM didn't normalize, we try parsing (assuming current context)
            start_dt = dateutil.parser.parse(time_str)
            end_dt = start_dt + datetime.timedelta(hours=1)
            
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'UTC', # Should configure from system ideally
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return f"Okay, I've added '{summary}' to your calendar for {start_dt.strftime('%A at %I:%M %p')}."
            
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return "I had trouble understanding the date and time for that event."

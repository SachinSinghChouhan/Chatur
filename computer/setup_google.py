"""
Google Services Setup Script
Run this script ONCE to authorize the application to access your Google Calendar and Gmail.
This will open a browser window for you to log in.
"""
import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Define scopes for both Calendar and Gmail
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/tasks'
]

def setup_google_auth():
    print("=" * 60)
    print("Google Services Authorization Setup")
    print("=" * 60)
    
    app_data = Path(os.getenv('APPDATA'))
    computer_dir = app_data / 'Computer'
    credentials_path = computer_dir / 'credentials.json'
    token_path = computer_dir / 'token.json'
    
    # Ensure directory exists
    if not computer_dir.exists():
        print(f"Error: {computer_dir} does not exist.")
        return

    if not credentials_path.exists():
        print(f"Error: credentials.json not found at {credentials_path}")
        print("Please place your credentials.json file in this folder first.")
        return

    creds = None
    
    # Check if we already have a token
    if token_path.exists():
        print(f"Found existing token at {token_path}")
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"Existing token is invalid: {e}")
            
    # Refresh or re-auth if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refeshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Refresh failed: {e}")
                creds = None
                
        if not creds:
            print("Launching browser for authentication...")
            print(f"Using credentials from: {credentials_path}")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Authorization failed: {e}")
                return

        # Save the credentials for the next run
        print(f"Saving new token to {token_path}")
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    print("\nSUCCESS! Google services are now authorized.")
    print("You can now restart 'chatur' and use Calendar and Email commands.")

if __name__ == '__main__':
    setup_google_auth()

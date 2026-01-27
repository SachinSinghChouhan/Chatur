"""
Test script for Gmail Integration
"""
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatur.handlers.email import GmailHandler
from chatur.models.intent import Intent, IntentType

def test_gmail_handler():
    print("="*60)
    print("Testing Gmail Handler")
    print("="*60)
    
    # Initialize handler
    handler = GmailHandler()
    
    # Check simple service status
    # Note: Since the user just added credentials, this might actually prompt for auth
    # or just say service is None but credentials exist
    if handler.service:
        print("[INFO] Gmail service is ACTIVE (authenticated)")
    else:
        print("[INFO] Gmail service is INACTIVE (needs authorization)")
    
    # Test 1: Read Emails (Graceful failure or success)
    print("\n--- Test 1: Read Emails ---")
    intent_read = Intent(
        type=IntentType.EMAIL,
        language='en',
        parameters={'action': 'read', 'count': 1},
        response_language='en'
    )
    result_read = handler.handle(intent_read)
    print(f"Result: {result_read}")
    
    if "credentials" in result_read: # If it detected credentials but needs auth
        print("[PASS] Detected credentials correctly")
    elif "unread emails" in result_read: # If somehow auth worked
         print("[PASS] Read emails successfully")
    elif "need Google credentials" in result_read: # Should NOT happen if files exist
        print("[FAIL] Did not detect credentials.json")
        
    # Test 2: Search Emails
    print("\n--- Test 2: Search Emails ---")
    intent_search = Intent(
        type=IntentType.EMAIL,
        language='en',
        parameters={'action': 'search', 'query': 'subject:Test'},
        response_language='en'
    )
    result_search = handler.handle(intent_search)
    # Just checking it doesn't crash
    print(f"Result: {result_search}")

if __name__ == "__main__":
    test_gmail_handler()

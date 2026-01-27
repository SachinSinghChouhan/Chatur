"""
Test script for Google Calendar Integration
"""
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatur.handlers.calendar import CalendarHandler
from chatur.models.intent import Intent, IntentType

def test_calendar_handler():
    print("="*60)
    print("Testing Calendar Handler (Google Calendar)")
    print("="*60)
    
    # Initialize handler
    handler = CalendarHandler()
    
    # Check simple service status
    if handler.service:
        print("[INFO] Calendar service is ACTIVE (credentials found)")
    else:
        print("[INFO] Calendar service is INACTIVE (no credentials)")
    
    # Test 1: List Events (Graceful failure check)
    print("\n--- Test 1: List Events ---")
    intent_list = Intent(
        type=IntentType.CALENDAR,
        language='en',
        parameters={'action': 'list'},
        response_language='en'
    )
    result_list = handler.handle(intent_list)
    print(f"Result: {result_list}")
    
    if "credentials" in result_list or "upcoming events" in result_list:
        print("[PASS] Handled missing credentials or success correctly")
    else:
        print(f"[FAIL] Unexpected response: {result_list}")

if __name__ == "__main__":
    test_calendar_handler()

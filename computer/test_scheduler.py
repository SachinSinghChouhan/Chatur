"""Test reminder scheduler functionality"""

import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Add to path
sys.path.insert(0, '.')

from chatur.storage.init_db import init_database
from chatur.storage.reminder_repository import ReminderRepository
from chatur.core.tts import TextToSpeech
from chatur.service.scheduler import ReminderScheduler

def test_scheduler():
    """Test the reminder scheduler"""
    print("=" * 60)
    print("Testing Reminder Scheduler")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_database()
    
    # Initialize TTS
    print("2. Initializing TTS...")
    tts = TextToSpeech()
    
    # Initialize scheduler
    print("3. Initializing scheduler...")
    scheduler = ReminderScheduler(tts_engine=tts)
    
    # Create test reminders
    print("\n4. Creating test reminders...")
    repo = ReminderRepository()
    
    # Reminder 1: Due in 10 seconds
    reminder1_time = datetime.now() + timedelta(seconds=10)
    repo.create_reminder(
        text="Test reminder 1 - This should trigger in 10 seconds",
        reminder_time=reminder1_time.isoformat(),
        language='en'
    )
    print(f"   ✅ Created reminder 1 for {reminder1_time.strftime('%H:%M:%S')}")
    
    # Reminder 2: Due in 30 seconds
    reminder2_time = datetime.now() + timedelta(seconds=30)
    repo.create_reminder(
        text="Test reminder 2 - This should trigger in 30 seconds",
        reminder_time=reminder2_time.isoformat(),
        language='en'
    )
    print(f"   ✅ Created reminder 2 for {reminder2_time.strftime('%H:%M:%S')}")
    
    # Start scheduler
    print("\n5. Starting scheduler...")
    scheduler.start()
    print("   ✅ Scheduler running (checking every 30 seconds)")
    
    # Wait for reminders to trigger
    print("\n6. Waiting for reminders to trigger...")
    print("   (This will take about 40 seconds)")
    print("\n" + "-" * 60)
    
    try:
        for i in range(45):
            remaining = 45 - i
            print(f"\r   Waiting... {remaining} seconds remaining", end="", flush=True)
            time.sleep(1)
        
        print("\n" + "-" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    
    # Stop scheduler
    print("\n7. Stopping scheduler...")
    scheduler.stop()
    
    # Check results
    print("\n8. Checking results...")
    pending = repo.get_pending_reminders()
    
    if len(pending) == 0:
        print("   ✅ All reminders triggered successfully!")
    else:
        print(f"   ⚠️  {len(pending)} reminders still pending")
        for reminder in pending:
            print(f"      - {reminder['text']}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_scheduler()

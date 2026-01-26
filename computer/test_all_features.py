"""Comprehensive test suite for Computer Voice Assistant"""

import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '.')

from chatur.storage.init_db import init_database
from chatur.core.tts import TextToSpeech
from chatur.core.llm import LLMClient
from chatur.service.command_processor import CommandProcessor

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_test(number, description):
    """Print test number and description"""
    print(f"\n{number}. {description}")
    print("-" * 60)

def test_feature(processor, command, expected_keywords):
    """Test a command and verify response contains expected keywords"""
    print(f"Command: '{command}'")
    response = processor.process_command(command)
    print(f"Response: {response}")
    
    # Check if response contains expected keywords
    success = any(keyword.lower() in response.lower() for keyword in expected_keywords)
    
    if success:
        print("✅ PASS")
    else:
        print(f"⚠️  FAIL - Expected keywords: {expected_keywords}")
    
    return success

def main():
    """Run comprehensive feature tests"""
    print_header("Computer Voice Assistant - Comprehensive Test Suite")
    
    # Initialize
    print("\nInitializing components...")
    init_database()
    tts = TextToSpeech()
    llm = LLMClient()
    processor = CommandProcessor(llm, tts)
    print("✅ Initialization complete\n")
    
    results = []
    
    # ========================================
    # Test 1: Timer Commands
    # ========================================
    print_header("TEST 1: Timer Commands")
    
    print_test("1.1", "Start timer for 5 seconds")
    results.append(test_feature(
        processor,
        "Start a timer for 5 seconds",
        ["timer", "started", "5", "second"]
    ))
    
    print_test("1.2", "Start timer for 2 minutes")
    results.append(test_feature(
        processor,
        "Set a timer for 2 minutes",
        ["timer", "started", "2", "minute"]
    ))
    
    # ========================================
    # Test 2: Reminder Commands
    # ========================================
    print_header("TEST 2: Reminder Commands")
    
    print_test("2.1", "Set reminder for specific time")
    results.append(test_feature(
        processor,
        "Remind me to call mom at 5 PM",
        ["reminder", "set", "5", "PM"]
    ))
    
    print_test("2.2", "Set reminder for tomorrow")
    results.append(test_feature(
        processor,
        "Set a reminder for tomorrow at 9 AM",
        ["reminder", "set", "tomorrow", "9"]
    ))
    
    # ========================================
    # Test 3: Notes Commands
    # ========================================
    print_header("TEST 3: Notes/Memory Commands")
    
    print_test("3.1", "Store a fact")
    results.append(test_feature(
        processor,
        "Remember my favorite color is blue",
        ["remember", "blue", "favorite color"]
    ))
    
    print_test("3.2", "Store another fact")
    results.append(test_feature(
        processor,
        "Remember my birthday is January 15",
        ["remember", "birthday", "January 15"]
    ))
    
    print_test("3.3", "Retrieve a fact")
    results.append(test_feature(
        processor,
        "What's my favorite color?",
        ["blue", "favorite", "color"]
    ))
    
    # ========================================
    # Test 4: Question Answering
    # ========================================
    print_header("TEST 4: Question Answering")
    
    print_test("4.1", "General knowledge question")
    results.append(test_feature(
        processor,
        "What's the capital of France?",
        ["Paris", "France", "capital"]
    ))
    
    print_test("4.2", "Another question")
    results.append(test_feature(
        processor,
        "Who invented the telephone?",
        ["Bell", "Alexander", "telephone", "invented"]
    ))
    
    # ========================================
    # Test 5: App Launching
    # ========================================
    print_header("TEST 5: App Launching")
    
    print_test("5.1", "Open Chrome")
    results.append(test_feature(
        processor,
        "Open Chrome",
        ["opening", "chrome", "launched"]
    ))
    
    print_test("5.2", "Open Calculator")
    results.append(test_feature(
        processor,
        "Open Calculator",
        ["opening", "calculator", "launched"]
    ))
    
    # ========================================
    # Test 6: Media Control
    # ========================================
    print_header("TEST 6: Media Control")
    
    print("\n⚠️  Note: These tests require Spotify to be running")
    input("Press Enter when Spotify is ready (or skip)...")
    
    print_test("6.1", "Play music")
    results.append(test_feature(
        processor,
        "Play music",
        ["play", "music", "playing"]
    ))
    
    print_test("6.2", "Pause music")
    results.append(test_feature(
        processor,
        "Pause music",
        ["pause", "paused"]
    ))
    
    # ========================================
    # Test 7: Bilingual Support (Hindi)
    # ========================================
    print_header("TEST 7: Bilingual Support (Hindi)")
    
    print_test("7.1", "Hindi timer command")
    results.append(test_feature(
        processor,
        "5 minute ka timer lagao",
        ["timer", "5", "minute"]
    ))
    
    print_test("7.2", "Hindi reminder command")
    results.append(test_feature(
        processor,
        "Kal subah 8 baje reminder set karo",
        ["reminder", "set"]
    ))
    
    # ========================================
    # Summary
    # ========================================
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if pass_rate == 100:
        print("\n🎉 All tests passed! MVP is working perfectly!")
    elif pass_rate >= 80:
        print("\n✅ Most tests passed! MVP is functional with minor issues.")
    else:
        print("\n⚠️  Several tests failed. Review the output above.")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()

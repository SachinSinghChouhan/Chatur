"""Tests for handler responses and ResponseBuilder utility"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatur.utils.responses import ResponseBuilder
from chatur.models.intent import Intent, IntentType


def test_response_builder_english():
    """Test ResponseBuilder with English"""
    assert ResponseBuilder.get('en', {'en': 'Hello', 'hi': 'नमस्ते'}) == 'Hello'
    assert ResponseBuilder.success('en', 'Opening', 'Chrome') == 'Done: Opening Chrome'
    assert ResponseBuilder.error('en', 'open the app') == "Sorry, I couldn't open the app"
    assert ResponseBuilder.not_found('en', 'Chrome') == "I couldn't find Chrome"
    assert ResponseBuilder.confirm('en', 'Okay') == 'Okay'


def test_response_builder_hindi():
    """Test ResponseBuilder with Hindi"""
    assert ResponseBuilder.get('hi', {'en': 'Hello', 'hi': 'नमस्ते'}) == 'नमस्ते'
    # Hindi success format: "{action} हो गया" + " {item}"
    assert ResponseBuilder.success('hi', 'Opening', 'Chrome') == 'Opening हो गया Chrome'
    assert ResponseBuilder.error('hi', 'open the app') == "माफ़ करें, open the app में समस्या हुई"
    assert ResponseBuilder.not_found('hi', 'Chrome') == 'Chrome नहीं मिला'
    assert ResponseBuilder.confirm('hi', 'Okay') == 'ठीक है'
    
    # Test without item
    assert ResponseBuilder.success('hi', 'खोल रहा हूं') == 'खोल रहा हूं हो गया'


def test_response_builder_fallback():
    """Test ResponseBuilder fallback to English"""
    assert ResponseBuilder.get('fr', {'en': 'Hello'}) == 'Hello'
    assert ResponseBuilder.success('fr', 'Done') == 'Done: Done'


def test_intent_creation():
    """Test Intent model creation"""
    intent = Intent(
        type=IntentType.APP_LAUNCH,
        language='en',
        parameters={'app_name': 'chrome', 'action': 'open'},
        response_language='en'
    )
    assert intent.type == IntentType.APP_LAUNCH
    assert intent.language == 'en'
    assert intent.parameters['app_name'] == 'chrome'


def test_intent_types():
    """Test all IntentType values"""
    assert IntentType.REMINDER.value == "reminder"
    assert IntentType.TIMER.value == "timer"
    assert IntentType.NOTE.value == "note"
    assert IntentType.QUESTION.value == "question"
    assert IntentType.APP_LAUNCH.value == "app_launch"
    assert IntentType.MEDIA_CONTROL.value == "media_control"
    assert IntentType.TASK.value == "task"


if __name__ == "__main__":
    print("Running handler utility tests...")
    print("-" * 40)
    
    test_response_builder_english()
    print("✓ test_response_builder_english passed")
    
    test_response_builder_hindi()
    print("✓ test_response_builder_hindi passed")
    
    test_response_builder_fallback()
    print("✓ test_response_builder_fallback passed")
    
    test_intent_creation()
    print("✓ test_intent_creation passed")
    
    test_intent_types()
    print("✓ test_intent_types passed")
    
    print("-" * 40)
    print("All tests passed!")

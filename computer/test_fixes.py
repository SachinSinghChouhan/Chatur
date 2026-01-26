"""Quick test for the fixes"""

import sys
sys.path.insert(0, '.')

from chatur.core.llm import LLMClient

def test_intent(command, expected_type):
    """Test a command and show the classified intent"""
    llm = LLMClient()
    intent = llm.classify_intent(command)
    
    status = "✅" if intent.type.value == expected_type else "❌"
    print(f"{status} '{command}'")
    print(f"   Type: {intent.type.value} (expected: {expected_type})")
    print(f"   Params: {intent.parameters}")
    print()

print("=" * 60)
print("Testing Fixed Intent Classification")
print("=" * 60)
print()

# Test Hindi/Hinglish
print("1. Hindi/Hinglish App Launch:")
test_intent("gmail khol", "app_launch")
test_intent("whatsapp kholo", "app_launch")
test_intent("chrome chalu karo", "app_launch")

print("2. Media Control:")
test_intent("next track", "media_control")
test_intent("agla gana", "media_control")
test_intent("pause karo", "media_control")

print("3. Timer (Hindi):")
test_intent("5 minute ka timer", "timer")

print("=" * 60)
print("Test Complete!")
print("=" * 60)

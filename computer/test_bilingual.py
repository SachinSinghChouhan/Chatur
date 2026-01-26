"""Test bilingual responses"""

import sys
sys.path.insert(0, '.')

from chatur.core.llm import LLMClient
from chatur.core.tts import TextToSpeech
from chatur.service.command_processor import CommandProcessor

def test_command(processor, command):
    """Test a command and show response"""
    print(f"\nCommand: '{command}'")
    response = processor.process_command(command)
    print(f"Response: {response}")
    print("-" * 60)

print("=" * 60)
print("Testing Bilingual Responses")
print("=" * 60)

# Initialize
tts = TextToSpeech()
llm = LLMClient()
processor = CommandProcessor(llm, tts)

# Test Hindi commands
print("\n📱 Hindi Commands:")
test_command(processor, "chrome kholo")
test_command(processor, "gmail khol")
test_command(processor, "agla gana")
test_command(processor, "music roko")
test_command(processor, "5 minute ka timer")

# Test English commands
print("\n📱 English Commands:")
test_command(processor, "open calculator")
test_command(processor, "next track")
test_command(processor, "pause music")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)

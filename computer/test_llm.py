"""Test the LLM client with actual API call"""

import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add to path
sys.path.insert(0, '.')

from chatur.core.llm import LLMClient
from chatur.utils.logger import setup_logger

logger = setup_logger('test_llm')

def test_llm():
    """Test LLM intent classification"""
    print("=" * 60)
    print("Testing LLM Client")
    print("=" * 60)
    
    try:
        # Initialize client
        print("\n1. Initializing LLM client...")
        llm = LLMClient()
        
        if not llm.client:
            print("❌ No OpenAI API key found")
            return
        
        print("✅ LLM client initialized")
        
        # Test commands
        test_commands = [
            "Start a timer for 10 seconds",
            "What's the capital of France?",
            "Remind me to call mom at 5 PM",
            "Open Chrome",
        ]
        
        for i, command in enumerate(test_commands, 1):
            print(f"\n{i}. Testing: '{command}'")
            try:
                intent = llm.classify_intent(command)
                print(f"   ✅ Intent: {intent.type.value}")
                print(f"   Language: {intent.language}")
                print(f"   Parameters: {intent.parameters}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("Test complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_llm()

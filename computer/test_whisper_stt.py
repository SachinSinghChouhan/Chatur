"""
Test script for Whisper STT
Run this to test if Whisper works better than Azure for your microphone
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_whisper():
    """Test Whisper STT"""
    print("=" * 60)
    print("WHISPER STT TEST")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("[FAIL] OPENAI_API_KEY not set in .env file")
        print("\nWhisper requires OpenAI API key.")
        print("Add it to your .env file:")
        print("OPENAI_API_KEY=your_key_here")
        return False
    
    print(f"[OK] OPENAI_API_KEY: {api_key[:8]}... (hidden)")
    
    # Check if pyaudio is installed
    try:
        import pyaudio
        print("[OK] PyAudio is installed")
    except ImportError:
        print("[FAIL] PyAudio is not installed")
        print("\nInstall it with:")
        print("pip install pyaudio")
        print("\nNote: On Windows, you may need to install it from:")
        print("https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
        return False
    
    # Import and test Whisper STT
    try:
        from chatur.core.whisper_stt import WhisperSTT
        
        print("\n" + "=" * 60)
        print("INITIALIZING WHISPER")
        print("=" * 60)
        
        stt = WhisperSTT()
        
        if not stt.client:
            print("[FAIL] Whisper initialization failed")
            return False
        
        print("[OK] Whisper initialized")
        
        print("\n" + "=" * 60)
        print("MICROPHONE TEST")
        print("=" * 60)
        print("You will record for 5 seconds.")
        print("Speak clearly when recording starts!")
        print("")
        input("Press Enter to start recording...")
        
        # Test recognition
        text = stt.recognize_once(duration_seconds=5)
        
        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)
        
        if text:
            print(f"[SUCCESS] Recognized: '{text}'")
            print("\nWhisper STT is working correctly!")
            return True
        else:
            print("[FAIL] No text recognized")
            print("\nPossible causes:")
            print("  1. Microphone permissions not granted")
            print("  2. You didn't speak during recording")
            print("  3. Microphone volume too low")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n")
    success = test_whisper()
    
    print("\n" + "=" * 60)
    if success:
        print("RESULT: Whisper STT is working!")
        print("\nYou can now use Whisper for voice input.")
        print("It's more reliable than Azure for local microphones.")
    else:
        print("RESULT: Whisper STT test failed - see errors above")
    print("=" * 60)
    print("\n")
    
    sys.exit(0 if success else 1)

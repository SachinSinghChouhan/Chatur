"""
Test script for Google Speech Recognition
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("GOOGLE SPEECH RECOGNITION TEST")
print("=" * 60)

# Check if SpeechRecognition is installed
try:
    import speech_recognition as sr
    print("[OK] SpeechRecognition library installed")
except ImportError:
    print("[FAIL] SpeechRecognition not installed")
    print("\nInstall with:")
    print("pip install SpeechRecognition pyaudio")
    sys.exit(1)

# Check if pyaudio is installed
try:
    import pyaudio
    print("[OK] PyAudio installed")
except ImportError:
    print("[FAIL] PyAudio not installed")
    print("\nInstall with:")
    print("pip install pyaudio")
    sys.exit(1)

# Test Google STT
try:
    from chatur.core.google_stt import GoogleSTT
    
    print("\n" + "=" * 60)
    print("INITIALIZING GOOGLE STT")
    print("=" * 60)
    
    stt = GoogleSTT()
    
    if not stt.recognizer:
        print("[FAIL] Google STT initialization failed")
        sys.exit(1)
    
    print("[OK] Google STT initialized")
    
    print("\n" + "=" * 60)
    print("MICROPHONE TEST")
    print("=" * 60)
    print("You will have 10 seconds to speak.")
    print("Speak clearly when recording starts!")
    print("")
    input("Press Enter to start...")
    
    # Test recognition
    text = stt.recognize_once(timeout_seconds=10)
    
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    
    if text:
        print(f"[SUCCESS] Recognized: '{text}'")
        print("\nGoogle STT is working!")
    else:
        print("[FAIL] No text recognized")
        print("\nPossible causes:")
        print("  1. Microphone permissions not granted")
        print("  2. You didn't speak during recording")
        print("  3. Microphone volume too low")
        print("  4. No internet connection")
    
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] Exception occurred: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

"""
Test script for Vosk Speech Recognition (Offline)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("VOSK SPEECH RECOGNITION TEST (OFFLINE)")
print("=" * 60)

# Check if vosk is installed
try:
    import vosk
    print("[OK] Vosk library installed")
except ImportError:
    print("[FAIL] Vosk not installed")
    print("\nInstall with:")
    print("pip install vosk")
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

# Test Vosk STT
try:
    from chatur.core.vosk_stt import VoskSTT
    
    print("\n" + "=" * 60)
    print("INITIALIZING VOSK STT")
    print("=" * 60)
    
    stt = VoskSTT()
    
    if not stt.model:
        print("[FAIL] Vosk model not loaded")
        print("\n" + "=" * 60)
        print("VOSK MODEL SETUP INSTRUCTIONS")
        print("=" * 60)
        print("\n1. Download a Vosk model from:")
        print("   https://alphacephei.com/vosk/models")
        print("\n2. Recommended models:")
        print("   - vosk-model-small-en-in-0.4 (40MB) - Indian English")
        print("   - vosk-model-en-us-0.22 (1.8GB) - US English (better quality)")
        print("\n3. Extract the downloaded model to:")
        print("   d:\\protocol\\computer\\vosk-model")
        print("\n4. The folder structure should be:")
        print("   d:\\protocol\\computer\\vosk-model\\")
        print("     ├── am/")
        print("     ├── conf/")
        print("     ├── graph/")
        print("     └── ...")
        print("\n5. Run this test again")
        print("=" * 60)
        sys.exit(1)
    
    print("[OK] Vosk model loaded")
    print("[OK] Vosk STT initialized (OFFLINE MODE)")
    
    print("\n" + "=" * 60)
    print("MICROPHONE TEST")
    print("=" * 60)
    print("You will have 10 seconds to speak.")
    print("Speak clearly when recording starts!")
    print("Note: Offline recognition may be less accurate than online services")
    print("")
    input("Press Enter to start...")
    
    # Test recognition
    text = stt.recognize_once(timeout_seconds=10)
    
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    
    if text:
        print(f"[SUCCESS] Recognized: '{text}'")
        print("\nVosk STT is working!")
        print("Note: This works completely offline - no internet needed!")
    else:
        print("[FAIL] No text recognized")
        print("\nPossible causes:")
        print("  1. Microphone permissions not granted")
        print("  2. You didn't speak during recording")
        print("  3. Microphone volume too low")
        print("  4. Speech was unclear (offline models are less accurate)")
    
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] Exception occurred: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

"""
Test script for STT Factory
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatur.core.stt_factory import STTFactory

print("=" * 60)
print("STT FACTORY TEST")
print("=" * 60)

# List available engines
print("\n1. Checking available STT engines...")
available = STTFactory.list_available_engines()
print(f"   Available engines: {', '.join(available) if available else 'None'}")

if not available:
    print("\n[ERROR] No STT engines available!")
    print("Install at least one:")
    print("  pip install SpeechRecognition  # For Google")
    print("  pip install openai             # For Whisper")
    print("  pip install vosk               # For Vosk")
    sys.exit(1)

# Show engine info
print("\n2. Engine Information:")
for engine in available:
    info = STTFactory.get_engine_info(engine)
    print(f"\n   {info['name']}:")
    print(f"   - Internet: {'Required' if info['requires_internet'] else 'Not required'}")
    print(f"   - API Key: {'Required' if info['requires_api_key'] else 'Not required'}")
    print(f"   - Cost: {info['cost']}")
    print(f"   - Accuracy: {info['accuracy']}")

# Test factory creation
print("\n3. Testing factory creation...")
try:
    # Try to create from config
    print("   Creating STT from config...")
    stt = STTFactory.create()
    print(f"   [OK] Created: {type(stt).__name__}")
    
    # Test each available engine
    print("\n4. Testing each engine:")
    for engine_name in available:
        try:
            print(f"   Creating {engine_name}...")
            engine = STTFactory.create(engine_name)
            print(f"   [OK] {engine_name}: {type(engine).__name__}")
        except Exception as e:
            print(f"   [FAIL] {engine_name}: {e}")

except Exception as e:
    print(f"   [ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("STT FACTORY TEST COMPLETE")
print("=" * 60)
print("\nThe factory is working! You can now switch STT engines")
print("by editing config/config.yaml:")
print("  stt:")
print("    engine: 'google'  # or 'whisper', 'vosk', 'azure'")

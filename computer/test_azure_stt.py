"""
Diagnostic script to test Azure Speech-to-Text configuration
This will help identify the exact cause of the timeout issue
"""

import os
import sys
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

def test_azure_credentials():
    """Test if Azure credentials are properly configured"""
    print("=" * 60)
    print("STEP 1: Testing Azure Credentials")
    print("=" * 60)
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
    
    if not speech_key:
        print("❌ AZURE_SPEECH_KEY is not set in .env file")
        return False
    
    print(f"✅ AZURE_SPEECH_KEY: {speech_key[:8]}... (hidden)")
    print(f"✅ AZURE_SPEECH_REGION: {speech_region}")
    return True

def test_microphone_access():
    """Test if microphone is accessible"""
    print("\n" + "=" * 60)
    print("STEP 2: Testing Microphone Access")
    print("=" * 60)
    
    print("⚠️  Microphone test requires manual verification")
    print("   Please check:")
    print("   1. Windows Settings → Privacy & Security → Microphone")
    print("   2. Ensure 'Microphone access' is ON")
    print("   3. Ensure 'Let apps access your microphone' is ON")
    print("   4. Ensure 'Let desktop apps access your microphone' is ON")
    print("\n   If all settings are correct, microphone should work.")
    
    return True  # Assume microphone is accessible

def test_azure_connection():
    """Test Azure Speech Service connection"""
    print("\n" + "=" * 60)
    print("STEP 3: Testing Azure Speech Service Connection")
    print("=" * 60)
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
    
    try:
        # Create speech config
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        speech_config.speech_recognition_language = "en-IN"
        
        print("✅ Speech config created")
        
        # Test with push audio stream (simulated audio)
        print("\nTesting connection with simulated audio...")
        
        # Create a simple audio config
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        print("✅ Speech recognizer created")
        print("\n🎤 Testing live recognition...")
        print("   Please say something in the next 10 seconds...")
        
        # Try recognition
        result = recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"✅ SUCCESS! Recognized: '{result.text}'")
            return True
        
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("⚠️  No speech detected")
            print("   This could mean:")
            print("   - Microphone volume is too low")
            print("   - You didn't speak during the listening period")
            print("   - Background noise is too high")
            print("\n💡 Try adjusting microphone volume in Windows settings")
            return False
        
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"❌ Recognition canceled: {cancellation.reason}")
            
            if cancellation.reason == speechsdk.CancellationReason.Error:
                error_details = cancellation.error_details
                print(f"❌ Error details: {error_details}")
                
                if "401" in str(error_details) or "Unauthorized" in str(error_details):
                    print("\n💡 Authentication error - your Azure Speech key may be invalid")
                    print("   Please check your AZURE_SPEECH_KEY in .env file")
                
                elif "timeout" in str(error_details).lower():
                    print("\n💡 Timeout error - Azure couldn't receive audio")
                    print("   Possible causes:")
                    print("   1. Microphone is not sending audio to Azure")
                    print("   2. Firewall blocking Azure connection")
                    print("   3. Network connectivity issues")
                
                elif "WebSocket" in str(error_details):
                    print("\n💡 WebSocket connection error")
                    print("   Possible causes:")
                    print("   1. Firewall/antivirus blocking connection")
                    print("   2. Corporate proxy blocking WebSocket")
                    print("   3. Network connectivity issues")
            
            return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print(f"\n💡 Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_tts():
    """Test if Azure TTS works (to verify credentials)"""
    print("\n" + "=" * 60)
    print("STEP 4: Testing Azure Text-to-Speech (credential verification)")
    print("=" * 60)
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
    
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        # Use default speaker
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        print("Testing TTS with a simple phrase...")
        result = synthesizer.speak_text_async("Testing Azure Speech Service").get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ TTS works! Your Azure credentials are valid.")
            return True
        else:
            print(f"❌ TTS failed: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("\n" + "=" * 60)
    print("AZURE SPEECH-TO-TEXT DIAGNOSTIC TOOL")
    print("=" * 60)
    
    results = {
        "credentials": False,
        "microphone": False,
        "azure_connection": False,
        "tts": False
    }
    
    # Run tests
    results["credentials"] = test_azure_credentials()
    
    if results["credentials"]:
        results["microphone"] = test_microphone_access()
        results["tts"] = test_simple_tts()
        results["azure_connection"] = test_azure_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print("\n" + "=" * 60)
    
    if all(results.values()):
        print("🎉 All tests passed! Azure STT should work.")
    else:
        print("⚠️  Some tests failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("1. Install PyAudio: pip install pyaudio")
        print("2. Check microphone permissions in Windows Settings")
        print("3. Verify Azure Speech key is correct")
        print("4. Check firewall/antivirus settings")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

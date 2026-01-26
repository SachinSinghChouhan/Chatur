"""
Simple Azure Speech-to-Text diagnostic script (ASCII-safe)
"""

import os
import sys
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

def test_azure_stt():
    """Test Azure Speech-to-Text"""
    print("=" * 60)
    print("AZURE SPEECH-TO-TEXT DIAGNOSTIC")
    print("=" * 60)
    
    # Check credentials
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
    
    if not speech_key:
        print("[FAIL] AZURE_SPEECH_KEY is not set in .env file")
        return False
    
    print(f"[OK] AZURE_SPEECH_KEY: {speech_key[:8]}... (hidden)")
    print(f"[OK] AZURE_SPEECH_REGION: {speech_region}")
    
    try:
        # Create speech config
        print("\n" + "=" * 60)
        print("Creating Speech Recognizer...")
        print("=" * 60)
        
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        speech_config.speech_recognition_language = "en-IN"
        
        # Increase timeout settings
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
            "10000"  # 10 seconds
        )
        
        print("[OK] Speech config created")
        
        # Create recognizer with default microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        print("[OK] Speech recognizer created")
        print("\n" + "=" * 60)
        print("MICROPHONE TEST")
        print("=" * 60)
        print("Please say something in the next 10 seconds...")
        print("(Speak clearly into your microphone)")
        print("")
        
        # Try recognition
        result = recognizer.recognize_once()
        
        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"[SUCCESS] Recognized: '{result.text}'")
            print("\nAzure STT is working correctly!")
            return True
        
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("[WARNING] No speech detected")
            print("\nPossible causes:")
            print("  1. Microphone volume is too low")
            print("  2. You didn't speak during the listening period")
            print("  3. Background noise is too high")
            print("\nTroubleshooting:")
            print("  - Check Windows Settings > Privacy > Microphone")
            print("  - Ensure 'Let apps access your microphone' is ON")
            print("  - Ensure 'Let desktop apps access your microphone' is ON")
            print("  - Increase microphone volume in Windows sound settings")
            return False
        
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"[ERROR] Recognition canceled: {cancellation.reason}")
            
            if cancellation.reason == speechsdk.CancellationReason.Error:
                error_details = str(cancellation.error_details)
                print(f"[ERROR] Error details: {error_details}")
                
                if "401" in error_details or "Unauthorized" in error_details:
                    print("\n[DIAGNOSIS] Authentication error")
                    print("  Your Azure Speech key may be invalid or expired")
                    print("  Please check your AZURE_SPEECH_KEY in .env file")
                
                elif "timeout" in error_details.lower():
                    print("\n[DIAGNOSIS] Timeout error")
                    print("  Azure couldn't receive audio from your microphone")
                    print("\nPossible causes:")
                    print("  1. Microphone permissions not granted")
                    print("  2. Firewall blocking Azure connection")
                    print("  3. Network connectivity issues")
                    print("  4. Microphone driver issues")
                    print("\nTroubleshooting:")
                    print("  - Check Windows microphone permissions")
                    print("  - Temporarily disable firewall/antivirus")
                    print("  - Test microphone in other apps (e.g., Voice Recorder)")
                
                elif "WebSocket" in error_details:
                    print("\n[DIAGNOSIS] WebSocket connection error")
                    print("  Cannot establish connection to Azure")
                    print("\nPossible causes:")
                    print("  1. Firewall/antivirus blocking WebSocket connections")
                    print("  2. Corporate proxy blocking connection")
                    print("  3. Network connectivity issues")
                    print("\nTroubleshooting:")
                    print("  - Temporarily disable firewall/antivirus")
                    print("  - Check if you're behind a corporate proxy")
                    print("  - Try on a different network")
                
                else:
                    print("\n[DIAGNOSIS] Unknown error")
                    print("  Please check the error details above")
            
            return False
        
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_azure_stt()
    
    print("\n" + "=" * 60)
    if success:
        print("RESULT: Azure STT is working!")
    else:
        print("RESULT: Azure STT test failed - see errors above")
    print("=" * 60)
    
    sys.exit(0 if success else 1)

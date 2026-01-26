"""Media control handler with exact volume percentage control"""

import time
import re
import pyautogui
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.media_control')

class MediaControlHandler(BaseHandler):
    """Handler for media playback control"""
    
    def __init__(self):
        # Set pyautogui to be faster
        pyautogui.PAUSE = 0.1
        
        # Try to initialize exact volume control using COM
        try:
            from comtypes import CoCreateInstance, GUID, CLSCTX_ALL
            from pycaw.pycaw import IMMDeviceEnumerator, EDataFlow, ERole, IAudioEndpointVolume
            from ctypes import cast, POINTER
            
            # CLSID for MMDeviceEnumerator
            CLSID_MMDeviceEnumerator = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
            
            deviceEnumerator = CoCreateInstance(
                CLSID_MMDeviceEnumerator,
                IMMDeviceEnumerator,
                CLSCTX_ALL
            )
            
            defaultDevice = deviceEnumerator.GetDefaultAudioEndpoint(
                EDataFlow.eRender.value, ERole.eMultimedia.value
            )
            
            interface = defaultDevice.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.has_volume_control = True
            
            # Test it works
            current = self.volume.GetMasterVolumeLevelScalar()
            logger.info(f"Volume control initialized successfully (current: {int(current*100)}%)")
            
        except Exception as e:
            logger.warning(f"Could not initialize exact volume control: {e}")
            self.volume = None
            self.has_volume_control = False
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a media control intent"""
        return intent.type == IntentType.MEDIA_CONTROL
    
    def handle(self, intent: Intent) -> str:
        """Control media playback"""
        try:
            action = intent.parameters.get('action', 'play')
            volume_level = intent.parameters.get('volume_level')
            language = intent.response_language
            
            if action == 'play' or action == 'pause':
                # Toggle play/pause
                pyautogui.press('playpause')
                time.sleep(0.1)
                logger.info("Toggled play/pause")
                
                if language == 'hi':
                    return "ठीक है"
                else:
                    return "Okay"
                
            elif action == 'next':
                # Next track
                pyautogui.press('nexttrack')
                time.sleep(0.1)
                logger.info("Next track")
                
                if language == 'hi':
                    return "अगला गाना चला रहा हूं"
                else:
                    return "Playing next track"
                
            elif action == 'previous':
                # Previous track
                pyautogui.press('prevtrack')
                time.sleep(0.1)
                logger.info("Previous track")
                
                if language == 'hi':
                    return "पिछला गाना चला रहा हूं"
                else:
                    return "Playing previous track"
            
            elif action == 'volume_up':
                # Increase volume
                pyautogui.press('volumeup')
                time.sleep(0.1)
                logger.info("Volume up")
                
                if language == 'hi':
                    return "आवाज़ बढ़ा रहा हूं"
                else:
                    return "Increasing volume"
            
            elif action == 'volume_down':
                # Decrease volume
                pyautogui.press('volumedown')
                time.sleep(0.1)
                logger.info("Volume down")
                
                if language == 'hi':
                    return "आवाज़ कम कर रहा हूं"
                else:
                    return "Decreasing volume"
            
            elif action == 'set_volume':
                # Set volume to exact percentage
                if not self.has_volume_control or not self.volume:
                    if language == 'hi':
                        return "माफ़ करें, exact volume control उपलब्ध नहीं है"
                    else:
                        return "Sorry, exact volume control is not available"
                
                if volume_level is None:
                    if language == 'hi':
                        return "कितना volume चाहिए?"
                    else:
                        return "What volume level?"
                
                try:
                    # Convert percentage to 0.0-1.0 range
                    level = int(volume_level) / 100.0
                    level = max(0.0, min(1.0, level))  # Clamp between 0 and 1
                    
                    self.volume.SetMasterVolumeLevelScalar(level, None)
                    logger.info(f"Set volume to {volume_level}%")
                    
                    # Verify
                    actual = int(self.volume.GetMasterVolumeLevelScalar() * 100)
                    
                    if language == 'hi':
                        return f"Volume {actual} पर सेट किया"
                    else:
                        return f"Volume set to {actual}"
                
                except Exception as e:
                    logger.error(f"Error setting volume: {e}")
                    if language == 'hi':
                        return "Volume सेट करने में समस्या हुई"
                    else:
                        return "Sorry, I couldn't set the volume"
            
            elif action == 'mute':
                # Mute/unmute
                pyautogui.press('volumemute')
                time.sleep(0.1)
                logger.info("Toggled mute")
                
                if language == 'hi':
                    return "म्यूट किया"
                else:
                    return "Muted"
            
        except Exception as e:
            logger.error(f"Media control error: {e}", exc_info=True)
            if intent.response_language == 'hi':
                return "माफ़ करें, media control में समस्या हुई"
            else:
                return "Sorry, I couldn't control media playback"

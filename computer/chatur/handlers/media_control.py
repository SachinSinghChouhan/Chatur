"""Media control handler with exact volume percentage control"""

import time
from typing import Optional, Any
import pyautogui
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
from chatur.utils.responses import ResponseBuilder

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
                pyautogui.press('playpause')
                time.sleep(0.1)
                logger.info("Toggled play/pause")
                return ResponseBuilder.confirm(language, "Okay")
                
            elif action == 'next':
                pyautogui.press('nexttrack')
                time.sleep(0.1)
                logger.info("Next track")
                return ResponseBuilder.success(language, "Playing next track")
                
            elif action == 'previous':
                pyautogui.press('prevtrack')
                time.sleep(0.1)
                logger.info("Previous track")
                return ResponseBuilder.success(language, "Playing previous track")
            
            elif action == 'volume_up':
                pyautogui.press('volumeup')
                time.sleep(0.1)
                logger.info("Volume up")
                return ResponseBuilder.success(language, "Increasing volume")
            
            elif action == 'volume_down':
                pyautogui.press('volumedown')
                time.sleep(0.1)
                logger.info("Volume down")
                return ResponseBuilder.success(language, "Decreasing volume")
            
            elif action == 'set_volume':
                if not self.has_volume_control or not self.volume:
                    return ResponseBuilder.get(language, {
                        'en': "Sorry, exact volume control is not available",
                        'hi': "माफ़ करें, exact volume control उपलब्ध नहीं है"
                    })
                
                if volume_level is None:
                    return ResponseBuilder.ask(language, "What volume level?")
                
                try:
                    level = int(volume_level) / 100.0
                    level = max(0.0, min(1.0, level))
                    
                    self.volume.SetMasterVolumeLevelScalar(level, None)
                    logger.info(f"Set volume to {volume_level}%")
                    
                    actual = int(self.volume.GetMasterVolumeLevelScalar() * 100)
                    return ResponseBuilder.get(language, {
                        'en': f"Volume set to {actual}",
                        'hi': f"Volume {actual} पर सेट किया"
                    })
                
                except Exception as e:
                    logger.error(f"Error setting volume: {e}")
                    return ResponseBuilder.error(language, "set the volume")
            
            elif action == 'mute':
                pyautogui.press('volumemute')
                time.sleep(0.1)
                logger.info("Toggled mute")
                return ResponseBuilder.get(language, {'en': "Muted", 'hi': "म्यूट किया"})
            
            return ResponseBuilder.error(language, "control media playback")
            
        except Exception as e:
            logger.error(f"Media control error: {e}", exc_info=True)
            return ResponseBuilder.error(language, "control media playback")

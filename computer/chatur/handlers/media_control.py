"""Media control handler with exact volume percentage control"""

import sys
import time
from typing import Optional, Any
try:
    import pyautogui
except ImportError:
    pyautogui = None
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
from chatur.utils.responses import ResponseBuilder
from chatur.utils.platform import IS_WINDOWS, set_volume_linux

logger = setup_logger('chatur.handlers.media_control')

class MediaControlHandler(BaseHandler):
    """Handler for media playback control"""
    
    def __init__(self):
        # Set pyautogui to be faster
        pyautogui.PAUSE = 0.1

        self.volume: Any = None
        self.has_volume_control = False

        if IS_WINDOWS:
            # Windows: try exact volume control via COM / pycaw
            try:
                from comtypes import CoCreateInstance, GUID, CLSCTX_ALL
                from pycaw.pycaw import IMMDeviceEnumerator, EDataFlow, ERole, IAudioEndpointVolume
                from ctypes import cast, POINTER

                CLSID_MMDeviceEnumerator = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
                deviceEnumerator = CoCreateInstance(
                    CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, CLSCTX_ALL
                )
                defaultDevice = deviceEnumerator.GetDefaultAudioEndpoint(
                    EDataFlow.eRender.value, ERole.eMultimedia.value
                )
                interface = defaultDevice.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                self.volume = cast(interface, POINTER(IAudioEndpointVolume)) # type: ignore
                self.has_volume_control = True
                current = self.volume.GetMasterVolumeLevelScalar() if self.volume else 0.0 # type: ignore
                logger.info(f"Windows volume control initialized (current: {int(current*100)}%)")
            except ImportError:
                logger.warning("Windows volume control imports failed. Ensure pycaw and comtypes are installed.")
            except Exception as e:
                logger.warning(f"Could not initialize Windows volume control: {e}")
        else:
            # Linux / macOS: use pactl or amixer (checked at runtime)
            self.has_volume_control = True
            logger.info("Linux/macOS volume control will use pactl/amixer")
    
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
                if not self.has_volume_control:
                    return ResponseBuilder.get(language, {
                        'en': "Sorry, exact volume control is not available",
                        'hi': "माफ़ करें, exact volume control उपलब्ध नहीं है"
                    })

                if volume_level is None:
                    return ResponseBuilder.ask(language, "What volume level?")

                try:
                    level_int = int(volume_level)

                    if IS_WINDOWS and self.volume:
                        # Windows COM path
                        level = max(0.0, min(1.0, level_int / 100.0))
                        self.volume.SetMasterVolumeLevelScalar(level, None) # type: ignore
                        actual = int(self.volume.GetMasterVolumeLevelScalar() * 100) # type: ignore
                        logger.info(f"Set volume to {actual}% (Windows COM)")
                        return ResponseBuilder.get(language, {
                            'en': f"Volume set to {actual}%",
                            'hi': f"Volume {actual}% पर सेट किया"
                        })
                    else:
                        # Linux / macOS path
                        success = set_volume_linux(level_int)
                        if success:
                            logger.info(f"Set volume to {level_int}% (pactl/amixer)")
                            return ResponseBuilder.get(language, {
                                'en': f"Volume set to {level_int}%",
                                'hi': f"Volume {level_int}% पर सेट किया"
                            })
                        else:
                            return ResponseBuilder.error(language, "set the volume")

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

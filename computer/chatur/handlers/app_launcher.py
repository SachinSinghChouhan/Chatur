"""App launcher handler with open and close functionality"""

import os
import subprocess
import webbrowser
import psutil
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.storage.app_repository import AppRepository
from chatur.utils.logger import setup_logger
from chatur.utils.responses import ResponseBuilder

logger = setup_logger('chatur.handlers.app_launcher')

class AppLauncherHandler(BaseHandler):
    """Handler for launching and closing applications"""
    
    def __init__(self):
        self.repo = AppRepository()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is an app launch intent"""
        return intent.type == IntentType.APP_LAUNCH
    
    def handle(self, intent: Intent) -> str:
        """Launch or close an application"""
        try:
            app_name = intent.parameters.get('app_name', '').lower()
            action = intent.parameters.get('action', 'open')  # 'open' or 'close'
            url = intent.parameters.get('url')  # Optional URL to open
            language = intent.response_language
            
            # If URL is provided, open it in browser
            if url:
                try:
                    webbrowser.open(url)
                    logger.info(f"Opened URL in browser: {url}")
                    return ResponseBuilder.get(language, {
                        'en': f"Opening {url}",
                        'hi': f"{url} खोल रहा हूं"
                    })
                except Exception as e:
                    logger.error(f"Failed to open URL: {e}")
                    return ResponseBuilder.error(language, "open the website")
            
            if not app_name:
                return ResponseBuilder.ask(language, "Which app?")
            
            # Find app in database
            app = self.repo.get_by_name(app_name)
            
            if not app:
                logger.warning(f"App not found: {app_name}")
                return ResponseBuilder.not_found(language, app_name)
            
            # Close or open app
            if action == 'close':
                success = self._close_app(app)
                if success:
                    logger.info(f"Closed app: {app['display_name']}")
                    return ResponseBuilder.success(language, "Closed", app['display_name'])
                else:
                    return ResponseBuilder.error(language, f"close {app['display_name']}")
            else:
                # Open app
                success = self._launch_app(app)
                if success:
                    logger.info(f"Launched app: {app['display_name']}")
                    return ResponseBuilder.success(language, "Opening", app['display_name'])
                else:
                    return ResponseBuilder.error(language, f"open {app['display_name']}")
                
        except Exception as e:
            logger.error(f"Error with app: {e}")
            return ResponseBuilder.error(language, "with that app")
    
    def _launch_app(self, app: dict) -> bool:
        """Launch the application"""
        try:
            if app['app_type'] == 'url':
                # Open URL in browser
                webbrowser.open(app['path'])
                return True
            else:
                # Launch executable
                subprocess.Popen(app['path'], shell=True)
                return True
        except Exception as e:
            logger.error(f"Failed to launch {app['display_name']}: {e}")
            return False
    
    def _close_app(self, app: dict) -> bool:
        """Close/kill the application"""
        import sys
        try:
            app_name = app['display_name'].lower()
            closed = False

            # app_type is stored as 'exe' (not 'executable') in the database
            if app['app_type'] == 'exe':
                exe_name = os.path.basename(app['path']).lower()
                # Strip .exe suffix for cross-platform matching
                exe_stem = exe_name.replace('.exe', '')

                for proc in psutil.process_iter(['name', 'exe']):
                    try:
                        proc_name = proc.info['name'].lower() if proc.info['name'] else ''

                        if (exe_stem in proc_name or app_name in proc_name):
                            logger.info(f"Killing process: {proc.info['name']} (PID: {proc.pid})")
                            proc.kill()
                            closed = True

                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass

                return closed

            elif app['app_type'] == 'url':
                # Cross-platform browser process names
                if sys.platform == 'win32':
                    browser_stems = ['chrome', 'firefox', 'msedge', 'brave']
                else:
                    browser_stems = ['chrome', 'chromium', 'firefox', 'brave', 'brave-browser']

                for proc in psutil.process_iter(['name']):
                    try:
                        proc_name = proc.info['name'].lower() if proc.info['name'] else ''
                        if any(stem in proc_name for stem in browser_stems):
                            logger.info(f"Closing browser: {proc.info['name']}")
                            proc.kill()
                            closed = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                return closed

        except Exception as e:
            logger.error(f"Failed to close {app['display_name']}: {e}")
            return False

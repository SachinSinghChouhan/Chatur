"""
System Tray Interface for the Voice Assistant
Provides a system tray icon with menu for controlling the assistant
"""

import os
import sys
import threading
from pathlib import Path
from typing import Optional, Callable
from PIL import Image
import pystray
from pystray import MenuItem as item
from chatur.utils.logger import setup_logger
from chatur.service.service_manager import ManagedService, ServiceCommand

logger = setup_logger('chatur.system_tray')


class SystemTray:
    """System tray interface for the voice assistant"""
    
    def __init__(self, managed_service: ManagedService, 
                 on_exit: Optional[Callable] = None):
        """
        Initialize system tray
        
        Args:
            managed_service: The managed service to control
            on_exit: Optional callback when user exits
        """
        self.managed_service = managed_service
        self.on_exit_callback = on_exit
        self.icon: Optional[pystray.Icon] = None
        self.running = False
        
        # Load icons
        self.icons = self._load_icons()
        
        logger.info("System tray initialized")
    
    def _load_icons(self) -> dict:
        """Load icon images"""
        icons_dir = Path(__file__).parent / "icons"
        
        try:
            return {
                'active': Image.open(icons_dir / "microphone_active.png"),
                'inactive': Image.open(icons_dir / "microphone_inactive.png"),
                'error': Image.open(icons_dir / "microphone_error.png")
            }
        except Exception as e:
            logger.error(f"Failed to load icons: {e}")
            # Create a simple fallback icon
            fallback = Image.new('RGB', (64, 64), color='gray')
            return {
                'active': fallback,
                'inactive': fallback,
                'error': fallback
            }
    
    def _get_current_icon(self) -> Image.Image:
        """Get the appropriate icon based on service status"""
        if not self.managed_service.service_manager.is_running():
            return self.icons['inactive']
        
        error = self.managed_service.service_manager.get_error()
        if error:
            return self.icons['error']
        
        return self.icons['active']
    
    def _create_menu(self) -> pystray.Menu:
        """Create the system tray menu"""
        return pystray.Menu(
            item(
                'Status',
                self._show_status,
                default=True
            ),
            pystray.Menu.SEPARATOR,
            item(
                'Start Assistant',
                self._start_service,
                visible=lambda item: not self.managed_service.service_manager.is_running()
            ),
            item(
                'Stop Assistant',
                self._stop_service,
                visible=lambda item: self.managed_service.service_manager.is_running()
            ),
            item(
                'Restart Assistant',
                self._restart_service
            ),
            pystray.Menu.SEPARATOR,
            item(
                'Open Logs',
                self._open_logs
            ),
            item(
                'About',
                self._show_about
            ),
            pystray.Menu.SEPARATOR,
            item(
                'Exit',
                self._exit
            )
        )
    
    def _show_status(self, icon, item):
        """Show current status"""
        is_running = self.managed_service.service_manager.is_running()
        error = self.managed_service.service_manager.get_error()
        
        if error:
            status = f"Error: {str(error)[:50]}"
        elif is_running:
            status = "Assistant is running"
        else:
            status = "Assistant is stopped"
        
        logger.info(f"Status check: {status}")
        
        # Show notification
        if self.icon:
            self.icon.notify(
                title="Voice Assistant Status",
                message=status
            )
    
    def _start_service(self, icon, item):
        """Start the assistant service"""
        logger.info("Starting service from tray menu")
        self.managed_service.send_command(ServiceCommand.START)
        
        # Update icon after a short delay
        threading.Timer(0.5, self._update_icon).start()
        
        if self.icon:
            self.icon.notify(
                title="Voice Assistant",
                message="Assistant started"
            )
    
    def _stop_service(self, icon, item):
        """Stop the assistant service"""
        logger.info("Stopping service from tray menu")
        self.managed_service.send_command(ServiceCommand.STOP)
        
        # Update icon after a short delay
        threading.Timer(0.5, self._update_icon).start()
        
        if self.icon:
            self.icon.notify(
                title="Voice Assistant",
                message="Assistant stopped"
            )
    
    def _restart_service(self, icon, item):
        """Restart the assistant service"""
        logger.info("Restarting service from tray menu")
        self.managed_service.send_command(ServiceCommand.RESTART)
        
        # Update icon after a short delay
        threading.Timer(1.0, self._update_icon).start()
        
        if self.icon:
            self.icon.notify(
                title="Voice Assistant",
                message="Assistant restarting..."
            )
    
    def _open_logs(self, icon, item):
        """Open the log file"""
        log_file = Path("logs") / "chatur.log"
        
        if log_file.exists():
            # Open with default text editor
            if sys.platform == 'win32':
                os.startfile(log_file)
            else:
                os.system(f'xdg-open "{log_file}"')
            logger.info("Opened log file")
        else:
            logger.warning("Log file not found")
            if self.icon:
                self.icon.notify(
                    title="Voice Assistant",
                    message="Log file not found"
                )
    
    def _show_about(self, icon, item):
        """Show about information"""
        if self.icon:
            self.icon.notify(
                title="Computer Voice Assistant",
                message="Version 1.0\nBilingual AI Assistant\nEnglish & Hindi Support"
            )
    
    def _exit(self, icon, item):
        """Exit the application"""
        logger.info("Exit requested from tray menu")
        
        # Stop the service
        self.managed_service.shutdown()
        
        # Stop the tray icon
        if self.icon:
            self.icon.stop()
        
        self.running = False
        
        # Call exit callback if provided
        if self.on_exit_callback:
            self.on_exit_callback()
    
    def _update_icon(self):
        """Update the tray icon based on current status"""
        if self.icon:
            self.icon.icon = self._get_current_icon()
            # Force menu update
            self.icon.update_menu()
    
    def run(self):
        """Run the system tray (blocking)"""
        logger.info("Starting system tray")
        
        self.running = True
        
        # Create the icon
        self.icon = pystray.Icon(
            name="VoiceAssistant",
            icon=self._get_current_icon(),
            title="Computer Voice Assistant",
            menu=self._create_menu()
        )
        
        # Start periodic icon updates (every 2 seconds)
        def update_loop():
            while self.running:
                threading.Event().wait(2.0)
                if self.running:
                    self._update_icon()
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
        # Run the icon (blocking)
        try:
            self.icon.run()
        except Exception as e:
            logger.error(f"System tray error: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info("System tray stopped")
    
    def stop(self):
        """Stop the system tray"""
        self.running = False
        if self.icon:
            self.icon.stop()


def create_tray(managed_service: ManagedService, 
                on_exit: Optional[Callable] = None) -> SystemTray:
    """
    Helper function to create a system tray
    
    Args:
        managed_service: The managed service to control
        on_exit: Optional callback when user exits
        
    Returns:
        SystemTray instance
    """
    return SystemTray(managed_service, on_exit)

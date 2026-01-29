"""Embedded webview overlay using pywebview to display React UI"""

import pywebview as webview
import threading
from pathlib import Path
from typing import Optional, Callable
from chatur.utils.logger import setup_logger
from chatur.core.assistant_state import AssistantState
import time

logger = setup_logger('chatur.overlay')


class WebViewOverlay:
    """Embedded webview overlay displaying React UI"""
    
    def __init__(self, static_dir: Path):
        """
        Initialize webview overlay
        
        Args:
            static_dir: Path to built React static files
        """
        self.static_dir = static_dir
        self.window: Optional[webview.Window] = None
        self._current_state = AssistantState.IDLE
        self._ready_event = threading.Event()
        
        logger.info(f"WebView overlay initialized with static dir: {static_dir}")
    
    def create_window(self):
        """Create the webview window (call before start)"""
        overlay_file = self.static_dir / "overlay.html"
        
        # Fallback to index.html if overlay.html doesn't exist
        if not overlay_file.exists():
            overlay_file = self.static_dir / "index.html"
            logger.warning(f"overlay.html not found, using index.html")
        
        if not overlay_file.exists():
            logger.error(f"HTML file not found: {overlay_file}")
            logger.info(f"Static dir exists: {self.static_dir.exists()}")
            if self.static_dir.exists():
                logger.info(f"Contents: {list(self.static_dir.iterdir())}")
            return
        
        # Convert to file:// URI
        file_uri = f'file:///{str(overlay_file.absolute()).replace(chr(92), "/")}'
        
        # Create window
        self.window = webview.create_window(
            title='Voice Assistant',
            url=file_uri,
            width=400,
            height=250,
            resizable=False,
            frameless=True,
            easy_drag=False,
            on_top=True,
            hidden=True  # Start hidden (IDLE)
        )
        
        logger.info(f"WebView window created: {file_uri}")
        self._ready_event.set()
    
    def start_blocking(self):
        """Start webview (blocking - must be called from main thread)"""
        if not self.window:
            logger.error("Window not created. Call create_window() first")
            return
        
        logger.info("Starting webview in main thread...")
        
        # Start webview (blocking call)
        webview.start(debug=False)
        
        logger.info("WebView stopped")
    
    def update_state(self, state: AssistantState):
        """
        Update overlay visibility based on state
        
        Args:
            state: New assistant state
        """
        # Wait for window to be ready
        if not self._ready_event.wait(timeout=5):
            logger.warning("WebView window not ready")
            return
        
        if not self.window:
            logger.warning("No window available")
            return
        
        self._current_state = state
        
        try:
            if state == AssistantState.IDLE:
                # Hide overlay
                self.window.hide()
                logger.debug("Overlay hidden (IDLE)")
            else:
                # Show overlay
                self.window.show()
                logger.debug(f"Overlay shown ({state.value})")
        except Exception as e:
            logger.error(f"Error updating overlay state: {e}", exc_info=True)
    
    def stop(self):
        """Stop the overlay"""
        if self.window:
            try:
                self.window.destroy()
            except:
                pass
        logger.info("Overlay stopped")

"""Native overlay window using pywebview for voice assistant UI"""

import webview
import threading
from pathlib import Path
from typing import Optional
from chatur.utils.logger import setup_logger
from chatur.core.assistant_state import AssistantState

logger = setup_logger('chatur.overlay')


class NativeOverlay:
    """Native desktop overlay window using embedded webview"""
    
    def __init__(self, static_dir: Path, api_port: int = 8000):
        """
        Initialize native overlay
        
        Args:
            static_dir: Path to built React static files
            api_port: Port where API server is running
        """
        self.static_dir = static_dir
        self.api_port = api_port
        self.window: Optional[webview.Window] = None
        self.running = False
        self._current_state = AssistantState.IDLE
        self._ready = threading.Event()
        
        logger.info(f"Native overlay initialized with static dir: {static_dir}")
    
    def start(self):
        """Start the overlay window"""
        if self.running:
            logger.warning("Overlay already running")
            return
        
        self.running = True
        
        try:
            # Path to index.html
            index_file = self.static_dir / "index.html"
            
            if not index_file.exists():
                logger.error(f"Index file not found: {index_file}")
                logger.info(f"Static dir contents: {list(self.static_dir.iterdir()) if self.static_dir.exists() else 'DIR NOT FOUND'}")
                return
            
            # Create window (non-blocking)
            self.window = webview.create_window(
                title='Voice Assistant',
                url=f'file:///{str(index_file.absolute()).replace(" + "chr(92)" + ", "/")}',
                width=400,
                height=250,
                resizable=False,
                frameless=True,
                easy_drag=False,
                on_top=True,
                transparent=False,  # Windows doesn't support transparent well
                hidden=True  # Start hidden (IDLE state)
            )
            
            self._ready.set()
            logger.info("Native overlay window created")
            
        except Exception as e:
            logger.error(f"Error creating overlay window: {e}", exc_info=True)
            self.running = False
    
    def start_blocking(self):
        """Start webview in blocking mode (call from main thread)"""
        try:
            logger.info("Starting webview (blocking)...")
            webview.start(debug=False)
        except Exception as e:
            logger.error(f"Error running webview: {e}", exc_info=True)
        finally:
            self.running = False
    
    def update_state(self, state: AssistantState):
        """
        Update overlay visibility based on state
        
        Args:
            state: New assistant state
        """
        # Wait for window to be ready
        if not self._ready.wait(timeout=5):
            logger.warning("Overlay window not ready")
            return
        
        if not self.window:
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
            logger.error(f"Error updating overlay state: {e}")
    
    def stop(self):
        """Stop the overlay window"""
        if self.window:
            try:
                self.window.destroy()
            except:
                pass
        
        self.running = False
        logger.info("Overlay stopped")

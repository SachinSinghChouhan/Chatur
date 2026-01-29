"""Simple native overlay using Tkinter (built-in, no dependencies)"""

import tkinter as tk
from tkinter import ttk
import threading
from typing import Optional
from chatur.utils.logger import setup_logger
from chatur.core.assistant_state import AssistantState

logger = setup_logger('chatur.overlay')


class TkinterOverlay:
    """Lightweight native overlay using Tkinter"""
    
    def __init__(self):
        """Initialize Tkinter overlay"""
        self.root: Optional[tk.Tk] = None
        self.running = False
        self._current_state = AssistantState.IDLE
        self.status_label: Optional[tk.Label] = None
        self.icon_label: Optional[tk.Label] = None
        
        logger.info("Tkinter overlay initialized")
    
    def start(self):
        """Start the overlay window in a background thread"""
        if self.running:
            logger.warning("Overlay already running")
            return
        
        self.running = True
        
        # Start in background thread
        overlay_thread = threading.Thread(target=self._run_window, daemon=True)
        overlay_thread.start()
        
        logger.info("Tkinter overlay started")
    
    def _run_window(self):
        """Create and run the Tk window (blocking)"""
        try:
            self.root = tk.Tk()
            self.root.title("Voice Assistant")
            
            # Window configuration
            self.root.overrideredirect(True)  # Frameless
            self.root.attributes('-topmost', True)  # Always on top
            self.root.attributes('-alpha', 0.95)  # Slightly transparent
            
            # Window size and position
            window_width = 300
            window_height = 150
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Position at bottom-center
            x = (screen_width - window_width) // 2
            y = screen_height - window_height - 100
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Dark background
            self.root.configure(bg='#1a1a1a')
            
            # Create main frame with padding
            main_frame = tk.Frame(self.root, bg='#1a1a1a')
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Icon indicator (large circle)
            self.icon_label = tk.Label(
                main_frame,
                text="●",  # Circle character
                font=("Segoe UI", 48),
                fg="#3b82f6",  # Blue
                bg='#1a1a1a'
            )
            self.icon_label.pack(pady=(0, 10))
            
            # Status text
            self.status_label = tk.Label(
                main_frame,
                text="Listening...",
                font=("Segoe UI", 14, "bold"),
                fg="white",
                bg='#1a1a1a'
            )
            self.status_label.pack()
            
            # Subtitle
            self.subtitle_label = tk.Label(
                main_frame,
                text="Speak now",
                font=("Segoe UI", 10),
                fg="#888888",
                bg='#1a1a1a'
            )
            self.subtitle_label.pack()
            
            # Start hidden (IDLE state)
            self.root.withdraw()
            
            # Run main loop
            logger.info("Starting Tkinter mainloop")
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error running Tkinter overlay: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info("Tkinter overlay stopped")
    
    def update_state(self, state: AssistantState):
        """
        Update overlay visibility and appearance based on state
        
        Args:
            state: New assistant state
        """
        if not self.root:
            return
        
        self._current_state = state
        
        try:
            if state == AssistantState.IDLE:
                # Hide overlay
                self.root.after(0, self.root.withdraw)
                logger.debug("Overlay hidden (IDLE)")
            else:
                # Show overlay and update appearance
                self.root.after(0, lambda: self._update_appearance(state))
                self.root.after(0, self.root.deiconify)
                logger.debug(f"Overlay shown ({state.value})")
        except Exception as e:
            logger.error(f"Error updating overlay state: {e}")
    
    def _update_appearance(self, state: AssistantState):
        """Update overlay appearance based on state"""
        if not self.status_label or not self.icon_label or not hasattr(self, 'subtitle_label'):
            return
        
        if state == AssistantState.LISTENING:
            self.status_label.config(text="Listening..." )
            self.icon_label.config(fg="#3b82f6")  # Blue
            self.subtitle_label.config(text="Speak now")
            
        elif state == AssistantState.PROCESSING:
            self.status_label.config(text="Thinking...")
            self.icon_label.config(fg="#8b5cf6")  # Purple
            self.subtitle_label.config(text="Processing")
            
        elif state == AssistantState.SPEAKING:
            self.status_label.config(text="Speaking...")
            self.icon_label.config(fg="#10b981")  # Green
            self.subtitle_label.config(text="")
    
    def stop(self):
        """Stop the overlay window"""
        if self.root:
            try:
                self.root.after(0, self.root.destroy)
            except:
                pass
        
        self.running = False
        logger.info("Overlay stopped")

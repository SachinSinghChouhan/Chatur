"""
Service Manager for running the voice assistant as a background service
Handles lifecycle management, threading, and graceful shutdown
"""

import threading
import time
import logging
from typing import Optional, Callable
from queue import Queue, Empty
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.service_manager')


class ServiceManager:
    """Manages the voice assistant as a background service"""
    
    def __init__(self, run_callback: Callable):
        """
        Initialize the service manager
        
        Args:
            run_callback: Function to run in the background thread
                         Should accept a stop_event parameter
        """
        self.run_callback = run_callback
        self.service_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.status_lock = threading.Lock()
        self._running = False
        self._error: Optional[Exception] = None
        
        logger.info("Service manager initialized")
    
    def start(self) -> bool:
        """
        Start the service in a background thread
        
        Returns:
            True if started successfully, False if already running
        """
        with self.status_lock:
            if self._running:
                logger.warning("Service already running")
                return False
            
            try:
                # Clear stop event and error
                self.stop_event.clear()
                self._error = None
                
                # Create and start service thread
                self.service_thread = threading.Thread(
                    target=self._run_service,
                    name="AssistantService",
                    daemon=True
                )
                self.service_thread.start()
                
                self._running = True
                logger.info("Service started successfully")
                return True
                
            except Exception as e:
                logger.error(f"Failed to start service: {e}", exc_info=True)
                self._error = e
                return False
    
    def stop(self, timeout: float = 5.0) -> bool:
        """
        Stop the service gracefully
        
        Args:
            timeout: Maximum time to wait for service to stop (seconds)
            
        Returns:
            True if stopped successfully, False if timeout
        """
        with self.status_lock:
            if not self._running:
                logger.warning("Service not running")
                return True
            
            logger.info("Stopping service...")
            
            # Signal the service to stop
            self.stop_event.set()
        
        # Wait for thread to finish (outside the lock)
        if self.service_thread and self.service_thread.is_alive():
            self.service_thread.join(timeout=timeout)
            
            if self.service_thread.is_alive():
                logger.error(f"Service did not stop within {timeout} seconds")
                return False
        
        with self.status_lock:
            self._running = False
            logger.info("Service stopped successfully")
            return True
    
    def restart(self) -> bool:
        """
        Restart the service
        
        Returns:
            True if restarted successfully
        """
        logger.info("Restarting service...")
        
        if not self.stop():
            logger.error("Failed to stop service for restart")
            return False
        
        # Small delay to ensure clean shutdown
        time.sleep(0.5)
        
        return self.start()
    
    def is_running(self) -> bool:
        """Check if service is running"""
        with self.status_lock:
            return self._running
    
    def get_error(self) -> Optional[Exception]:
        """Get the last error that occurred"""
        with self.status_lock:
            return self._error
    
    def _run_service(self):
        """Internal method that runs in the service thread"""
        try:
            logger.info("Service thread started")
            
            # Run the callback with stop event
            self.run_callback(self.stop_event)
            
            logger.info("Service thread finished normally")
            
        except Exception as e:
            logger.error(f"Service thread error: {e}", exc_info=True)
            with self.status_lock:
                self._error = e
                self._running = False
        
        finally:
            with self.status_lock:
                self._running = False


class ServiceCommand:
    """Commands that can be sent to the service"""
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    SHUTDOWN = "shutdown"


class ManagedService:
    """
    Higher-level service manager with command queue and auto-restart
    Useful for system tray integration
    """
    
    def __init__(self, run_callback: Callable, auto_restart: bool = True):
        """
        Initialize managed service
        
        Args:
            run_callback: Function to run in the background
            auto_restart: Automatically restart on error
        """
        self.service_manager = ServiceManager(run_callback)
        self.auto_restart = auto_restart
        self.command_queue: Queue = Queue()
        self.control_thread: Optional[threading.Thread] = None
        self.control_stop_event = threading.Event()
        
        logger.info("Managed service initialized")
    
    def start_control_loop(self):
        """Start the control loop that processes commands"""
        if self.control_thread and self.control_thread.is_alive():
            logger.warning("Control loop already running")
            return
        
        self.control_stop_event.clear()
        self.control_thread = threading.Thread(
            target=self._control_loop,
            name="ServiceControl",
            daemon=True
        )
        self.control_thread.start()
        logger.info("Control loop started")
    
    def stop_control_loop(self):
        """Stop the control loop"""
        self.control_stop_event.set()
        if self.control_thread:
            self.control_thread.join(timeout=2.0)
        logger.info("Control loop stopped")
    
    def send_command(self, command: str):
        """Send a command to the service"""
        self.command_queue.put(command)
        logger.debug(f"Command queued: {command}")
    
    def _control_loop(self):
        """Control loop that processes commands and monitors service"""
        logger.info("Control loop running")
        
        while not self.control_stop_event.is_set():
            try:
                # Check for commands (with timeout)
                try:
                    command = self.command_queue.get(timeout=1.0)
                    self._process_command(command)
                except Empty:
                    pass
                
                # Check if service crashed and auto-restart is enabled
                if self.auto_restart and not self.service_manager.is_running():
                    error = self.service_manager.get_error()
                    if error:
                        logger.warning(f"Service crashed, auto-restarting: {error}")
                        time.sleep(2.0)  # Brief delay before restart
                        self.service_manager.start()
                
            except Exception as e:
                logger.error(f"Control loop error: {e}", exc_info=True)
        
        logger.info("Control loop exiting")
    
    def _process_command(self, command: str):
        """Process a service command"""
        logger.info(f"Processing command: {command}")
        
        if command == ServiceCommand.START:
            self.service_manager.start()
        
        elif command == ServiceCommand.STOP:
            self.service_manager.stop()
        
        elif command == ServiceCommand.RESTART:
            self.service_manager.restart()
        
        elif command == ServiceCommand.STATUS:
            status = "running" if self.service_manager.is_running() else "stopped"
            logger.info(f"Service status: {status}")
        
        elif command == ServiceCommand.SHUTDOWN:
            self.service_manager.stop()
            self.control_stop_event.set()
        
        else:
            logger.warning(f"Unknown command: {command}")
    
    def shutdown(self):
        """Shutdown the entire managed service"""
        logger.info("Shutting down managed service")
        self.service_manager.stop()
        self.stop_control_loop()

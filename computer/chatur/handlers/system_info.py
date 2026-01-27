"""System information handler"""

import psutil
import socket
import platform
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.system_info')


class SystemInfoHandler(BaseHandler):
    """Handler for system information queries"""
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a system info intent"""
        return intent.type == IntentType.SYSTEM_INFO
    
    def handle(self, intent: Intent) -> str:
        """Handle system information query"""
        try:
            query_type = intent.parameters.get('query_type', 'general')
            
            if query_type == 'battery':
                return self._get_battery_info()
            elif query_type == 'cpu':
                return self._get_cpu_info()
            elif query_type == 'memory':
                return self._get_memory_info()
            elif query_type == 'disk':
                return self._get_disk_info()
            elif query_type == 'network':
                return self._get_network_info()
            else:
                return self._get_general_info()
        
        except Exception as e:
            logger.error(f"System info error: {e}", exc_info=True)
            return "Sorry, I couldn't get that information"
    
    def _get_battery_info(self) -> str:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "No battery found - you might be on a desktop"
            
            percent = battery.percent
            plugged = battery.power_plugged
            
            status = "plugged in" if plugged else "on battery"
            
            if plugged:
                return f"Battery is at {percent}% and charging"
            else:
                time_left = battery.secsleft
                if time_left == psutil.POWER_TIME_UNLIMITED:
                    return f"Battery is at {percent}%"
                else:
                    hours = time_left // 3600
                    minutes = (time_left % 3600) // 60
                    return f"Battery is at {percent}%, about {hours} hours and {minutes} minutes remaining"
        
        except Exception as e:
            logger.error(f"Battery info error: {e}")
            return "Couldn't get battery information"
    
    def _get_cpu_info(self) -> str:
        """Get CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            return f"CPU usage is {cpu_percent}% across {cpu_count} cores"
        
        except Exception as e:
            logger.error(f"CPU info error: {e}")
            return "Couldn't get CPU information"
    
    def _get_memory_info(self) -> str:
        """Get memory usage"""
        try:
            memory = psutil.virtual_memory()
            percent = memory.percent
            used_gb = memory.used / (1024**3)
            total_gb = memory.total / (1024**3)
            
            return f"Memory usage is {percent}%, using {used_gb:.1f} GB out of {total_gb:.1f} GB"
        
        except Exception as e:
            logger.error(f"Memory info error: {e}")
            return "Couldn't get memory information"
    
    def _get_disk_info(self) -> str:
        """Get disk space"""
        try:
            disk = psutil.disk_usage('/')
            percent = disk.percent
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            
            return f"Disk usage is {percent}%, {free_gb:.1f} GB free out of {total_gb:.1f} GB total"
        
        except Exception as e:
            logger.error(f"Disk info error: {e}")
            return "Couldn't get disk information"
    
    def _get_network_info(self) -> str:
        """Get network information"""
        try:
            # Get hostname
            hostname = socket.gethostname()
            
            # Get IP address
            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = "unknown"
            
            # Check internet connectivity
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                connected = True
            except:
                connected = False
            
            if connected:
                return f"You're connected to the internet. Your local IP is {ip}"
            else:
                return f"You're not connected to the internet. Your local IP is {ip}"
        
        except Exception as e:
            logger.error(f"Network info error: {e}")
            return "Couldn't get network information"
    
    def _get_general_info(self) -> str:
        """Get general system information"""
        try:
            system = platform.system()
            release = platform.release()
            machine = platform.machine()
            
            return f"You're running {system} {release} on {machine} architecture"
        
        except Exception as e:
            logger.error(f"General info error: {e}")
            return "Couldn't get system information"

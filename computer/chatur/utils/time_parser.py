"""Time parsing utility for natural language time expressions"""

from datetime import datetime, timedelta
from dateutil import parser
import re

def parse_time(time_str: str) -> datetime:
    """Parse natural language time expression to datetime"""
    
    time_str = time_str.lower().strip()
    now = datetime.now()
    
    # Handle "tomorrow" + time
    if 'tomorrow' in time_str or 'kal' in time_str:
        base_date = now + timedelta(days=1)
        time_match = re.search(r'(\d{1,2})\s*(am|pm|baje)?', time_str)
        if time_match:
            hour = int(time_match.group(1))
            if 'pm' in time_str and hour < 12:
                hour += 12
            return base_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        return base_date.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Handle specific time today
    time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', time_str)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        
        if time_match.group(3):
            if time_match.group(3) == 'pm' and hour < 12:
                hour += 12
        
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target_time < now:
            target_time += timedelta(days=1)
        return target_time
    
    return now + timedelta(hours=1)

def parse_duration(duration_str: str) -> int:
    """Parse duration string to seconds"""
    duration_str = duration_str.lower().strip()
    number_match = re.search(r'(\d+)', duration_str)
    if not number_match:
        return 300
    number = int(number_match.group(1))
    if 'second' in duration_str:
        return number
    elif 'minute' in duration_str or 'min' in duration_str:
        return number * 60
    elif 'hour' in duration_str:
        return number * 3600
    else:
        return number * 60

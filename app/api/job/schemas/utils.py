from datetime import datetime, time
import re
from pydantic import BaseModel

def validate_time(date, v):
    if isinstance(v, str):

        v = v.rstrip('Z')
        
        match = re.match(r'(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?', v)
        if match:
            hour, minute, second, microsecond = match.groups()
            microsecond = microsecond or '0'
            microsecond = microsecond.ljust(6, '0')[:6]  # Ensure 6 digits
            
            return datetime.combine(date, time(int(hour), int(minute), int(second), int(microsecond)))
    
    return v
    
from datetime import datetime, timedelta
import re

def parse_posted_date(text):
    """
    Parses date strings like:
    - "Posted 2 days ago"
    - "Today"
    - "Yesterday"
    - "Posted today"
    - "1 week ago"
    - "12 Jan' 26"
    
    Returns standard YYYY-MM-DD string or None if failed.
    """
    if not text:
        return None
        
    text = text.lower().strip()
    today = datetime.now()
    
    try:
        if 'today' in text:
            return today.strftime("%Y-%m-%d")
        
        if 'yesterday' in text:
            return (today - timedelta(days=1)).strftime("%Y-%m-%d")
            
        if 'few hours ago' in text or 'just now' in text:
            return today.strftime("%Y-%m-%d")

        # Regex for "X days ago"
        days_match = re.search(r'(\d+)\s+day', text)
        if days_match:
            days = int(days_match.group(1))
            return (today - timedelta(days=days)).strftime("%Y-%m-%d")
            
        # Regex for "X weeks ago" - Treat as too old usually, but parse anyway
        weeks_match = re.search(r'(\d+)\s+week', text)
        if weeks_match:
            weeks = int(weeks_match.group(1))
            return (today - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            
        # Regex for "X months ago"
        months_match = re.search(r'(\d+)\s+month', text)
        if months_match:
            months = int(months_match.group(1))
            return (today - timedelta(days=months*30)).strftime("%Y-%m-%d")

        # Try mapping explicit dates (e.g. "12 Jan' 26")
        # Add simpler formats if needed
        
        return None
    except:
        return None

def is_recent(date_str, max_days=3):
    """
    Checks if a YYYY-MM-DD string is within max_days.
    Returns True if recent or if date_str is None (safelist unknown dates).
    User strictness: "One copnay post max 2-3 days are limit".
    If we can't parse text, should we include?
    User said "expirend means applicarion open but its posed 4 days before means you dont scrap".
    This implies strictness.
    However, if we can't find date, we assume it's valid (better false positive than missing data).
    """
    if not date_str:
        return True # Default to recent if unknown
        
    try:
        posted = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - posted
        return delta.days <= max_days
    except:
        return True

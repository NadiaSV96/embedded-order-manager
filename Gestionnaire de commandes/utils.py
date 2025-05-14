# utils.py
from datetime import datetime

def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date

def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

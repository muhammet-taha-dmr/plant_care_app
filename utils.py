from datetime import datetime, timedelta

def days_until_watering(last_watered_str, interval_days):
    if not last_watered_str:
        return -999 # Urgent case: never watered
    
    last_watered = datetime.strptime(last_watered_str, '%Y-%m-%d')
    next_watering = last_watered + timedelta(days=interval_days)
    delta = next_watering - datetime.now()
    return delta.days

def get_watering_status_label(days):
    if days == -999:
        return "Urgent! Never Watered", "danger"
    if days < 0:
        return "Urgent! Overdue", "danger"
    if days == 0:
        return "Due Today", "warning"
    if days == 1:
        return "Due Tomorrow", "info"
    return f"In {days} Days", "success"

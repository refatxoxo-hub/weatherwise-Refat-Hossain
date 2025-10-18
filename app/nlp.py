import re
from datetime import datetime, timedelta

ATTRIBUTES = {
    "temperature": ["temperature", "temp", "hot", "cold", "warm", "cool"],
    "precipitation": ["rain", "precipitation", "wet", "storm", "showers"],
    "wind": ["wind", "breeze", "gust"],
    "humidity": ["humidity", "humid"],
}

def parse_weather_question(question):
    """
    Parse a natural language weather question.
    
    Args:
        question (str): User's weather-related question
        
    Returns:
        dict: Extracted info: {'location': str|None, 'period': 'today'|'tomorrow'|'next', 'days': int, 'attribute': str}
    """
    text = (question or "").strip().lower()
    if not text:
        return {"location": None, "period": "today", "days": 1, "attribute": "temperature"}

    # location: naive regex after 'in' or 'for'
    loc = None
    m = re.search(r"(?:in|for)\s+([a-zA-Z\s\-]+)", text)
    if m:
        loc = m.group(1).strip().rstrip("?!.").title()

    # period/days
    period = "today"
    days = 1
    if "tomorrow" in text:
        period = "tomorrow"
        days = 1
    else:
        m2 = re.search(r"next\s+(\d+)\s*day", text)
        if m2:
            period = "next"
            days = max(1, min(int(m2.group(1)), 5))

    # attribute
    attr = "temperature"
    for key, words in ATTRIBUTES.items():
        if any(w in text for w in words):
            attr = key
            break

    return {"location": loc, "period": period, "days": days, "attribute": attr}

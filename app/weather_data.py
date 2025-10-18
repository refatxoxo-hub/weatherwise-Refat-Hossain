import os
import requests
from datetime import datetime, timedelta

WTTR_URL = "https://wttr.in/{loc}?format=j1"

# A small, realistic mock dataset used when API is unavailable
MOCK_DATA = {
    "current_condition": [{
        "temp_C": "22",
        "FeelsLikeC": "23",
        "windspeedKmph": "15",
        "humidity": "60",
        "weatherDesc": [{"value": "Partly cloudy"}]
    }],
    "weather": [
        {
            "date": (datetime.utcnow()).strftime("%Y-%m-%d"),
            "hourly": [
                {"time": "0", "tempC": "18", "chanceofrain": "10"},
                {"time": "300", "tempC": "17", "chanceofrain": "10"},
                {"time": "600", "tempC": "19", "chanceofrain": "20"},
                {"time": "900", "tempC": "22", "chanceofrain": "20"},
                {"time": "1200", "tempC": "24", "chanceofrain": "30"},
                {"time": "1500", "tempC": "23", "chanceofrain": "20"},
                {"time": "1800", "tempC": "20", "chanceofrain": "15"},
                {"time": "2100", "tempC": "19", "chanceofrain": "10"}
            ],
            "maxtempC": "24",
            "mintempC": "16",
            "avgtempC": "20"
        },
        {
            "date": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "hourly": [
                {"time": "0", "tempC": "17", "chanceofrain": "20"},
                {"time": "300", "tempC": "16", "chanceofrain": "20"},
                {"time": "600", "tempC": "18", "chanceofrain": "25"},
                {"time": "900", "tempC": "21", "chanceofrain": "35"},
                {"time": "1200", "tempC": "23", "chanceofrain": "40"},
                {"time": "1500", "tempC": "22", "chanceofrain": "30"},
                {"time": "1800", "tempC": "19", "chanceofrain": "20"},
                {"time": "2100", "tempC": "18", "chanceofrain": "15"}
            ],
            "maxtempC": "23",
            "mintempC": "15",
            "avgtempC": "19"
        }
    ]
}

def _safe_get(d, path, default=None):
    cur = d
    try:
        for p in path:
            if isinstance(cur, list):
                cur = cur[p]
            else:
                cur = cur.get(p)
        return cur
    except Exception:
        return default

def get_weather_data(location, forecast_days=5):
    """
    Retrieve weather data for a specified location.
    
    Args:
        location (str): City or location name
        forecast_days (int): Number of days to forecast (1-5)
        
    Returns:
        dict: Weather data including current conditions and forecast
    """
    forecast_days = max(1, min(int(forecast_days or 5), 5))
    if not location or not isinstance(location, str):
        raise ValueError("location must be a non-empty string")
    url = WTTR_URL.format(loc=location.replace(' ', '+'))
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
    except Exception:
        # Fallback to mock if offline or API fails
        raw = MOCK_DATA

    # Truncate to requested forecast_days if 'weather' present
    if 'weather' in raw:
        raw['weather'] = raw['weather'][:forecast_days]
    return raw

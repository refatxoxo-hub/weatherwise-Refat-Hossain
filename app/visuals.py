import matplotlib.pyplot as plt
from datetime import datetime

def _extract_daily_series(weather_data):
    days = []
    tmax = []
    tmin = []
    prcp = []
    for day in weather_data.get("weather", []):
        days.append(day.get("date"))
        tmax.append(float(day.get("maxtempC", 0)))
        tmin.append(float(day.get("mintempC", 0)))
        # approximate precipitation chance as avg of hourly 'chanceofrain'
        hourly = day.get("hourly", [])
        if hourly:
            chances = [float(h.get("chanceofrain", 0)) for h in hourly if "chanceofrain" in h]
            prcp.append(sum(chances)/len(chances) if chances else 0.0)
        else:
            prcp.append(0.0)
    return days, tmax, tmin, prcp

def create_temperature_visualisation(weather_data, output_type='display'):
    """
    Create visualisation of temperature data.
    Args:
        weather_data (dict): The processed weather data
        output_type (str): 'display' or 'figure'
    Returns:
        matplotlib.figure.Figure or None
    """
    days, tmax, tmin, _ = _extract_daily_series(weather_data)
    fig, ax = plt.subplots()
    ax.plot(days, tmax, marker="o", label="Max Temp (°C)")
    ax.plot(days, tmin, marker="o", label="Min Temp (°C)")
    ax.set_title("Temperature Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("°C")
    ax.legend()
    fig.autofmt_xdate()
    if output_type == 'figure':
        return fig
    else:
        plt.show()
        return None

def create_precipitation_visualisation(weather_data, output_type='display'):
    """
    Create visualisation of precipitation chance.
    Args:
        weather_data (dict): The processed weather data
        output_type (str): 'display' or 'figure'
    Returns:
        matplotlib.figure.Figure or None
    """
    days, _, _, prcp = _extract_daily_series(weather_data)
    fig, ax = plt.subplots()
    ax.bar(days, prcp, label="Chance of Rain (%)")
    ax.set_title("Precipitation Probability")
    ax.set_xlabel("Date")
    ax.set_ylabel("%")
    ax.legend()
    fig.autofmt_xdate()
    if output_type == 'figure':
        return fig
    else:
        plt.show()
        return None

import pyinputplus as pyip
from .weather_data import get_weather_data
from .nlp import parse_weather_question
from .visuals import create_temperature_visualisation, create_precipitation_visualisation

def run_menu():
    print("=== Weather Advisor ===")
    while True:
        choice = pyip.inputMenu(
            ["Ask a natural language question",
             "Lookup by location & days",
             "Show temperature chart",
             "Show precipitation chart",
             "Quit"],
            numbered=True
        )

        if choice == "Ask a natural language question":
            q = pyip.inputStr("Type your question (e.g., 'Will it rain tomorrow in Perth?'):\n> ")
            parsed = parse_weather_question(q)
            loc = parsed.get("location") or pyip.inputStr("Enter a location (e.g., Perth): ")
            data = get_weather_data(loc, parsed.get("days", 1))
            print(generate_weather_response(parsed, data))

        elif choice == "Lookup by location & days":
            loc = pyip.inputStr("Location (e.g., Perth): ")
            days = pyip.inputInt("Forecast days (1-5): ", min=1, max=5)
            data = get_weather_data(loc, days)
            print(summarise(data))

        elif choice == "Show temperature chart":
            loc = pyip.inputStr("Location (e.g., Perth): ")
            days = pyip.inputInt("Forecast days (1-5): ", min=1, max=5)
            data = get_weather_data(loc, days)
            create_temperature_visualisation(data, output_type='display')

        elif choice == "Show precipitation chart":
            loc = pyip.inputStr("Location (e.g., Perth): ")
            days = pyip.inputInt("Forecast days (1-5): ", min=1, max=5)
            data = get_weather_data(loc, days)
            create_precipitation_visualisation(data, output_type='display')

        else:
            print("Goodbye!")
            break

def summarise(weather_data):
    cur = weather_data.get("current_condition", [{}])[0]
    desc = (cur.get("weatherDesc", [{}])[0] or {}).get("value", "N/A")
    temp = cur.get("temp_C", "N/A")
    wind = cur.get("windspeedKmph", "N/A")
    hum  = cur.get("humidity", "N/A")
    days = weather_data.get("weather", [])
    if days:
        first = days[0]
        line = f"Today: {desc}, {temp}°C, wind {wind} km/h, humidity {hum}% | High {first.get('maxtempC','?')}°C / Low {first.get('mintempC','?')}°C"
    else:
        line = f"Now: {desc}, {temp}°C, wind {wind} km/h, humidity {hum}%"
    return line

def generate_weather_response(parsed_question, weather_data):
    """Generate a natural language response to a weather question.
    Args:
        parsed_question (dict): Parsed question data
        weather_data (dict): Weather data
    Returns:
        str
    """
    attr = parsed_question.get("attribute", "temperature")
    period = parsed_question.get("period", "today")
    cur = weather_data.get("current_condition", [{}])[0]
    days = weather_data.get("weather", [])
    def safe(v, default="N/A"):
        return v if (v is not None and v != "") else default

    if attr == "precipitation":
        # Answer with average chance of rain for the first day (or tomorrow)
        idx = 0 if period == "today" else 1 if len(days) > 1 else 0
        if days:
            hourly = days[min(idx, len(days)-1)].get("hourly", [])
            chances = [float(h.get("chanceofrain", 0)) for h in hourly if "chanceofrain" in h]
            if chances:
                avg = sum(chances)/len(chances)
                when = "today" if idx == 0 else "tomorrow"
                return f"Average chance of rain {when} is about {avg:.0f}%."
        return "I couldn't find reliable precipitation data."
    elif attr == "wind":
        spd = safe(cur.get("windspeedKmph"))
        return f"Current wind speed is around {spd} km/h."
    elif attr == "humidity":
        h = safe(cur.get("humidity"))
        return f"Current humidity is about {h}%."
    else:
        # temperature
        if days:
            first = days[0] if period == "today" else (days[1] if len(days) > 1 else days[0])
            when = "today" if period == "today" else "tomorrow"
            hi = safe(first.get("maxtempC"))
            lo = safe(first.get("mintempC"))
            now = safe(cur.get("temp_C"))
            return f"It is {now}°C now; {when}'s forecast: high {hi}°C, low {lo}°C."
        now = safe(cur.get("temp_C"))
        return f"It is currently {now}°C."

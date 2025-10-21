import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


# Ucitavanje API kljuceva
def load_api_keys() -> dict[str, str]:
    return {
        "openWeather": os.getenv("OPENWEATHER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY")
    }


# User input
def get_user_input() -> tuple[str, str]:
    while True:
        city: str = input("Enter a city (Zagreb): ").strip()

        if not city:
            print("Error: City can't be empty.")
            continue

        date: str = input("Enter a date (example 2025-10-30): ")

        try:
            # parsiraj string u datetime objekt
            dateObject: datetime = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            continue

        # provjeri jel datum u proslosti
        today: datetime.date = datetime.now().date()
        if dateObject.date() < today:
            print("Error: the date is in the past.")
            continue

        # provjeri jel datum stariji od 5 dana
        five_days: datetime.date = today + timedelta(days=5)
        if dateObject.date() > five_days:
            print("Error: Date is too far ahead (max. 5 days).")
            continue

        return city, date


# dohvacanje vremena
def fetch_weather_data(city: str, date: str, api_key: str) -> dict | None:
    url: str = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    # print(f"URL: {Url}")
    response = requests.get(url,verify=False)
    # print(f"Status code: {response.status_code}")

    if response.status_code == 404:
        print("City not found")
        return None

    data: dict = response.json()
    for item in data['list']:
        if item['dt_txt'].startswith(date):
            return {
                "temp": item['main']['temp'],
                "humidity": item['main']['humidity'],
                "description": item['weather'][0]['description'],
                "wind_speed": item['wind']['speed'],
                "pop": item.get('pop', 0)
            }
    print("Error: No weather data for that date.")
    return None


# kreiranje prompta
def create_ai_prompt(city: str, date: str, weather_data: dict) -> str:
    prompt: str = f"""
    You are a helpful weather assistant providing practical advice for {city}.

    WEATHER FORECAST ({date}):
    - Temperature: {weather_data['temp']}°C
    - Humidity: {weather_data['humidity']}%
    - Conditions: {weather_data['description']}
    - Wind speed: {weather_data['wind_speed']} m/s
    - Precipitation probability: {weather_data['pop'] * 100}%

    Provide recommendations in EXACTLY this format:

    **1. WHAT TO WEAR** 🧥
    Be specific about clothing layers, jacket type, and footwear based on temperature, wind, and rain conditions.

    **2. WHAT TO DO** ✅
    Suggest 2-3 activities that work well in these conditions (indoor/outdoor depending on weather).

    **3. WHAT TO AVOID** ❌
    List 2-3 activities that would be uncomfortable or impractical in this weather.

    Requirements:
    - Use bullet points with emoji
    - Be practical and actionable
    - Consider ALL weather factors (temp, wind, rain, humidity)
    - Keep each section to 3-4 points
    - No medical advice or overly cautious warnings
    """
    return prompt


# dobivanje preporuka
def get_ai_recommendations(prompt: str, api_key: str) -> str:
    url: str = "https://api.groq.com/openai/v1/chat/completions"

    headers: dict[str, str] = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload: dict = {'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': prompt}],
                     'temperature': 0.1}
    response = requests.post(url, headers=headers, json=payload, verify=False)

    data: dict = response.json()
    ai_text: str = data["choices"][0]["message"]["content"]

    return ai_text


# CLI formatiranje
def display_results(city: str, date: str, weather_data: dict, ai_response: str) -> None:
    print("\n" + "=" * 50)
    print("    WEATHER FORECAST AND RECOMMENDATIONS")
    print("=" * 50 + "\n")

    print(f"📍 City: {city}")
    print(f"📅 Date: {date}\n")

    print("🌤️  Weather forecast:")
    print(f"   Temperature: {weather_data['temp']}°C")
    print(f"   Humidity: {weather_data['humidity']}%")
    print(f"   Description: {weather_data['description']}")
    print(f"   Wind: {weather_data['wind_speed']} m/s")
    print(f"   Probability of precipitation: {weather_data['pop'] * 100}%\n")

    print("🤖 AI RECOMMENDATIONS:")
    print(f"   {ai_response}\n")

    print("=" * 50)


def main() -> None:
    # print("Asistent pokrenut")
    keys: dict[str, str] = load_api_keys()
    city: str
    date: str
    city, date = get_user_input()
    weather: dict | None = fetch_weather_data(city, date, keys["openWeather"])
    prompt: str = create_ai_prompt(city, date, weather)
    recommendations: str = get_ai_recommendations(prompt, keys['groq'])
    display_results(city, date, weather, recommendations)


if __name__ == "__main__":
    main()

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

#Ucitavanje API kljuceva
def load_API_keys():
    return {
        "openWeather": os.getenv("OPENWEATHER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY")
    }

#User input
def get_user_input():
    while True:
        city = input("Enter a city (Zagreb): ").strip()

        if not city:
            print("Error: City can't be empty.")
            continue

        date = input("Enter a date (example 2025-10-30): ")

        try:
            #parsiraj string u datetime objekt
            dateObject = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            continue

        #provjeri jel datum u proslosti
        today = datetime.now().date()
        if dateObject.date() < today:
            print("Error: the date is in the past.")
            continue

        #provjeri jel datum stariji od 5 dana
        five_days = today + timedelta(days=5)
        if dateObject.date() > five_days:
            print("Error: Date is too far ahead (max. 5 days).")
            continue

        return city, date


#dohvacanje vremena
def fetch_weather_data(city, date, api_key):
    Url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    #print(f"URL: {Url}")
    response = requests.get(Url)
   #print(f"Status code: {response.status_code}")


    if response.status_code == 404:
        print("City not found")
        return None

    data = response.json()
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

#kreiranje prompta
def create_ai_prompt(city, date, weather_data):
    prompt = f"""
    You are a helpful local weather assistant for {city}.
    Provide practical, actionable advice based on the forecast below.

    Weather forecast for {city} on {date}:
    - Temperature: {weather_data['temp']}°C
    - Humidity: {weather_data['humidity']}%
    - Conditions: {weather_data['description']}
    - Wind: {weather_data['wind_speed']} m/s
    - Precipitation: {weather_data['pop'] * 100}%

    Give me clothing and activity recommendations for city and weather you're given.
    
    Provide:
    1. **What to wear** - Be specific (jacket type, layers, footwear)
    2. **What to do** - Activity suggestions
    3. **What to avoid** - Activities not recommended ({weather_data} needs to be taken into consideration)
    
    Do NOT:
    - Suggest medical advice
    - Be overly cautious
    - Use technical jargon

Keep it concise and practical. Use bullet points.
    """
    return prompt

#dobivanje preporuka
def get_ai_recommendations(prompt, api_key):

    Url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
    }

    payload = {'model': 'llama-3.1-8b-instant', 'messages': [{'role':'user', 'content':prompt}], 'temperature': 0.8}
    response = requests.post(Url, headers=headers, json=payload)

    data = response.json()
    ai_text = data["choices"][0]["message"]["content"]

    return ai_text

#CLI formatiranje
def display_results(city, date, weather_data,ai_response):
    print("\n" + "="*50)
    print("    WEATHER FORECAST AND RECOMMENDATIONS")
    print("="*50 + "\n")

    print(f"📍 City: {city}")
    print(f"📅 Date: {date}\n")

    print("🌤️  Weather forecast:")
    print(f"   Temperature: {weather_data['temp']}°C")
    print(f"   Humidity: {weather_data['humidity']}%")
    print(f"   Description: {weather_data['description']}")
    print(f"   Wind: {weather_data['wind_speed']} m/s")
    print(f"   Probability of precipitation: {weather_data['pop']*100}%\n")

    print("🤖 AI RECOMMENDATIONS:")
    print(f"   {ai_response}\n")

    print("="*50)

def main():
    #print("Asistent pokrenut")
    keys = load_API_keys()
    city, date = get_user_input()
    weather = fetch_weather_data(city, date, keys["openWeather"])
    prompt = create_ai_prompt(city, date, weather)
    recommendations = get_ai_recommendations(prompt, keys['groq'])
    display_results(city, date, weather, recommendations)

if __name__ == "__main__":
    main()
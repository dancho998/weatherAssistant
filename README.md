# Personal Weather Assistant 🌤️

AI-powered weather assistant that provides personalized clothing and activity recommendations based on real-time weather data.

## Features

- Fetches 5-day weather forecasts from OpenWeatherMap API
- AI-powered recommendations using Groq's LLaMA 3.3 versatile model (temperature: 0.1)
- Enhanced prompt engineering with role assignment and constraints
- Input validation (date range, city verification, empty inputs)
- Clean CLI interface with emojis and structured output
- Specific recommendations: what to wear, what to do, what to avoid
- Supports any city worldwide

## How It Works

1. **User Input**: Enter city name and date (within 5 days)
2. **Weather Fetch**: Retrieves forecast from OpenWeatherMap API
3. **AI Processing**: Sends structured prompt to Groq's LLaMA 3.3 model with:
    - Role assignment (local weather assistant)
    - Weather context
    - Specific output structure
    - Constraints (no medical advice, concise format)
4. **Display**: Shows weather data + AI recommendations in formatted CLI

## Technologies

- **Language:** Python 3.11
- **APIs:**
    - OpenWeatherMap (weather data)
    - Groq API (AI recommendations with LLaMA 3.3)
- **Libraries:** requests, python-dotenv

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/dancho998/weatherAssistant.git
cd weatherAssistant
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```
**Dependencies:**
- `requests==2.32.5` - HTTP library for API calls
- `python-dotenv==1.1.1` - Environment variable management

### 5. Set up API keys

Create a `.env` file in the root directory:
```env
OPENWEATHER_API_KEY=your_openweather_key_here
GROQ_API_KEY=your_groq_key_here
```

**Get your API keys:**
- OpenWeatherMap: https://openweathermap.org/api
- Groq: https://console.groq.com/

## Usage

Run the application:
```bash
python weatherAssistant.py
```

Follow the prompts:
1. Enter a city name (e.g., Zagreb)
2. Enter a date in YYYY-MM-DD format (max 5 days ahead)

### Example
```
Enter a city (Zagreb): London
Enter a date (example 2025-10-30): 2025-10-22

==================================================
    WEATHER FORECAST AND RECOMMENDATIONS
==================================================

📍 City: London
📅 Date: 2025-10-22

🌤️  Weather forecast:
   Temperature: 15.5°C
   Humidity: 75%
   Description: light rain
   Wind: 3.5 m/s
   Probability of precipitation: 60.0%

🤖 AI RECOMMENDATIONS:
   **What to wear:**
   - Waterproof jacket or raincoat
   - Layers (t-shirt + sweater)
   - Comfortable waterproof shoes or boots
   
   **What to do:**
   - Visit museums or indoor attractions
   - Enjoy cafes and restaurants
   - Short walks with umbrella
   
   **What to avoid:**
   - Outdoor sports without rain gear
   - Long hikes
   - Activities requiring dry conditions

==================================================
```

## Project Structure
```
weatherAssistant/
├── venv/                    # Virtual environment
├── .env                     # API keys
├── .gitignore              # Git ignore file
├── README.md               # 
├── requirements.txt        # Python dependencies
└── weatherAssistant.py     # Main application
```

## Prompt Engineering Techniques Used

- **Role Assignment**: AI acts as a local weather assistant
- **Structured Output**: Specific format (what to wear, do, avoid)
- **Negative Prompting**: Constraints on what NOT to include
- **Context Loading**: City-specific advice
- **Temperature Control**: Set to 0.1 for deterministic responses

## Error Handling

The application validates:
- Empty city names
- Invalid date formats
- Past dates
- Dates more than 5 days in the future
- Invalid cities (404 from API)
- Missing weather data for specified date

## Limitations

- Weather forecast limited to 5 days (OpenWeatherMap free tier)
- Requires active internet connection
- API rate limits apply (1000 calls/day for OpenWeatherMap free tier)

## Troubleshooting

### SSL Certificate Verification

By default, the code includes `verify=False` in API requests to avoid SSL certificate errors caused by corporate proxies or antivirus software that intercept HTTPS traffic.

**If you want to enable SSL verification (recommended for production):**
- Remove `verify=False` from `requests.get()` in `fetch_weather_data()`
- Remove `verify=False` from `requests.post()` in `get_ai_recommendations()`

**Note:** After enabling verification, if you encounter SSL errors, you may need to:
- Configure your antivirus to exclude Python from HTTPS scanning
- Add your corporate proxy certificate to Python's trust store
- Use a different network without SSL inspection


## License

This project is open source and available under the MIT License.

## Author

Danijel Domjanović
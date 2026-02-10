# Weather Dashboard

A simple weather dashboard built with Flask and Bootstrap that displays current weather and 3-day forecast using the OpenWeatherMap API.

## Features

- Search weather by city name
- Get weather by current location (geolocation)
- Current weather data (temperature, humidity, wind speed, pressure)
- Display local time for searched city (12-hour AM/PM format)
- Temperature unit toggle (°C/°F)
- Dynamic background based on weather conditions
- Interactive map showing city location
- 3-day weather forecast
- Weather icons
- Loading spinner
- Error handling
- Responsive design

## Tech Stack

- **Backend:** Flask, Flask-CORS, Requests
- **Frontend:** HTML5, Bootstrap 5, Leaflet.js, JavaScript
- **API:** OpenWeatherMap API

## Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd weather-dashboard
```

2. Create `.env` file from sample
```bash
cp .env.sample .env
```

3. Add your OpenWeatherMap API key to `.env`
```
OPENWEATHER_API_KEY=your_api_key_here
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Run the application
```bash
python app.py
```

6. Open browser at `http://127.0.0.1:5000`

## Project Structure

```
weather-dashboard/
├── app.py
├── requirements.txt
├── .env
├── .env.sample
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md
```

## Environment Variables

Create a `.env` file with the following variables:

```
OPENWEATHER_API_KEY=your_api_key_here
FLASK_DEBUG=True
FLASK_PORT=5000
```

Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

## License

Free to use for learning and portfolio projects.

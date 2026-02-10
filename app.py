from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'pressure': data['main']['pressure'],
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon'],
                'timezone': data['timezone']
            }
            return jsonify({'success': True, 'data': weather_data})
        else:
            return jsonify({'success': False, 'message': 'City not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/weather/coords', methods=['GET'])
def get_weather_by_coords():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            return jsonify({'success': False, 'message': 'Latitude and longitude required'}), 400

        url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'pressure': data['main']['pressure'],
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon'],
                'timezone': data['timezone']
            }
            return jsonify({'success': True, 'data': weather_data})
        else:
            return jsonify({'success': False, 'message': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/forecast/<city>', methods=['GET'])
def get_forecast(city):
    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            forecast_list = []

            seen_dates = set()
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]
                if date not in seen_dates and len(forecast_list) < 3:
                    forecast_list.append({
                        'date': item['dt_txt'],
                        'temperature': round(item['main']['temp'], 1),
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    })
                    seen_dates.add(date)

            return jsonify({'success': True, 'data': forecast_list})
        else:
            return jsonify({'success': False, 'message': 'City not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/forecast/coords', methods=['GET'])
def get_forecast_by_coords():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            return jsonify({'success': False, 'message': 'Latitude and longitude required'}), 400

        url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            forecast_list = []

            seen_dates = set()
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]
                if date not in seen_dates and len(forecast_list) < 3:
                    forecast_list.append({
                        'date': item['dt_txt'],
                        'temperature': round(item['main']['temp'], 1),
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    })
                    seen_dates.add(date)

            return jsonify({'success': True, 'data': forecast_list})
        else:
            return jsonify({'success': False, 'message': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=debug_mode, port=port)

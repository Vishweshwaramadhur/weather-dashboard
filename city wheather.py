import requests

def get_weather_by_city(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        print(f"\n📍 Location: {city}")
        print(f"🌡 Temperature: {temp}°C")
        print(f"💧 Humidity: {humidity}%")
        print(f"🌬 Wind Speed: {wind_speed} m/s")
        print(f"🌤 Weather Condition: {weather}\n")
    else:
        print("\n❌ Error: City not found or network issue.\n")

# Your API Key
API_KEY = "ea63db2e668eb09c1bf2dd299fe64785"

# Input from user
city = input("Enter your city name: ")
get_weather_by_city(city, API_KEY)
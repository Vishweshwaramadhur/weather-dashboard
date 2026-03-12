const API_BASE_URL = '/api';
let map = null;
let isCelsius = true;
let currentWeatherData = null;
let currentForecastData = null;

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        searchWeather();
    }
}

function getCurrentLocationWeather() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported by your browser');
        return;
    }

    hideElements();
    showLoading();

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            try {
                const weatherResponse = await fetch(`${API_BASE_URL}/weather/coords?lat=${lat}&lon=${lon}`);
                const weatherData = await weatherResponse.json();

                if (!weatherData.success) {
                    showError(weatherData.message);
                    hideLoading();
                    return;
                }

                const forecastResponse = await fetch(`${API_BASE_URL}/forecast/coords?lat=${lat}&lon=${lon}`);
                const forecastData = await forecastResponse.json();

                currentWeatherData = weatherData.data;
                displayCurrentWeather(weatherData.data);
                displayMap(weatherData.data.lat, weatherData.data.lon, weatherData.data.city);
                changeBackgroundByWeather(weatherData.data.description);

                if (forecastData.success) {
                    currentForecastData = forecastData.data;
                    displayForecast(forecastData.data);
                }

                hideLoading();

            } catch (error) {
                showError('Unable to fetch weather data. Please try again.');
                hideLoading();
            }
        },
        (error) => {
            hideLoading();
            if (error.code === error.PERMISSION_DENIED) {
                showError('Location access denied. Please enable location permissions.');
            } else {
                showError('Unable to get your location. Please try again.');
            }
        }
    );
}

async function searchWeather() {
    const cityInput = document.getElementById('cityInput');
    const city = cityInput.value.trim();

    if (!city) {
        showError('Please enter a city name');
        return;
    }

    hideElements();
    showLoading();

    try {
        const weatherResponse = await fetch(`${API_BASE_URL}/weather/${encodeURIComponent(city)}`);
        const weatherData = await weatherResponse.json();

        if (!weatherData.success) {
            showError(weatherData.message);
            hideLoading();
            return;
        }

        const forecastResponse = await fetch(`${API_BASE_URL}/forecast/${encodeURIComponent(city)}`);
        const forecastData = await forecastResponse.json();

        currentWeatherData = weatherData.data;
        displayCurrentWeather(weatherData.data);
        displayMap(weatherData.data.lat, weatherData.data.lon, weatherData.data.city);
        changeBackgroundByWeather(weatherData.data.description);

        if (forecastData.success) {
            currentForecastData = forecastData.data;
            displayForecast(forecastData.data);
        }

        hideLoading();

    } catch (error) {
        showError('Unable to fetch weather data. Please try again.');
        hideLoading();
    }
}

function displayCurrentWeather(data) {
    const localTime = getLocalTime(data.timezone);
    document.getElementById('cityName').textContent = `${data.city}, ${data.country} - ${localTime}`;

    const temp = isCelsius ? data.temperature : celsiusToFahrenheit(data.temperature);
    const feelsLike = isCelsius ? data.feels_like : celsiusToFahrenheit(data.feels_like);
    const unit = isCelsius ? '°C' : '°F';

    document.getElementById('temperature').textContent = `${temp}${unit}`;
    document.getElementById('description').textContent = data.description;
    document.getElementById('feelsLike').textContent = `${feelsLike}${unit}`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    document.getElementById('pressure').textContent = `${data.pressure} hPa`;

    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@4x.png`;
    document.getElementById('weatherIcon').src = iconUrl;

    document.getElementById('currentWeather').classList.remove('d-none');
    document.getElementById('unitToggle').classList.remove('d-none');
}

function displayForecast(forecastData) {
    const forecastCards = document.getElementById('forecastCards');
    forecastCards.innerHTML = '';
    const unit = isCelsius ? '°C' : '°F';

    forecastData.forEach((day) => {
        const date = new Date(day.date);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
        const iconUrl = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;
        const temp = isCelsius ? day.temperature : celsiusToFahrenheit(day.temperature);

        const card = `
            <div class="col-md-4 mb-3">
                <div class="card forecast-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">${dayName}</h5>
                        <img src="${iconUrl}" alt="Weather Icon" class="forecast-icon">
                        <h3>${temp}${unit}</h3>
                        <p class="text-capitalize">${day.description}</p>
                        <div class="row mt-2">
                            <div class="col-6">
                                <small><i class="bi bi-droplet"></i> ${day.humidity}%</small>
                            </div>
                            <div class="col-6">
                                <small><i class="bi bi-wind"></i> ${day.wind_speed} m/s</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        forecastCards.innerHTML += card;
    });

    document.getElementById('forecastSection').classList.remove('d-none');
}

function showLoading() {
    document.getElementById('loadingSpinner').classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.add('d-none');
}

function showError(message) {
    const toastElement = document.getElementById('errorToast');
    const toastBody = document.getElementById('toastMessage');
    toastBody.textContent = message;

    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 4000
    });
    toast.show();
}

function displayMap(lat, lon, cityName) {
    document.getElementById('mapSection').classList.remove('d-none');

    if (map !== null) {
        map.remove();
    }

    setTimeout(() => {
        map = L.map('map').setView([lat, lon], 10);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);

        L.marker([lat, lon])
            .addTo(map)
            .bindPopup(`<b>${cityName}</b><br>Latitude: ${lat}<br>Longitude: ${lon}`)
            .openPopup();

        map.invalidateSize();
    }, 100);
}

function getLocalTime(timezoneOffset) {
    const now = new Date();
    const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    const cityTime = new Date(utc + (timezoneOffset * 1000));

    let hours = cityTime.getHours();
    const minutes = cityTime.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12;
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;

    return `${hours}:${minutesStr} ${ampm}`;
}

function hideElements() {
    document.getElementById('currentWeather').classList.add('d-none');
    document.getElementById('mapSection').classList.add('d-none');
    document.getElementById('forecastSection').classList.add('d-none');
    document.getElementById('loadingSpinner').classList.add('d-none');
    document.getElementById('unitToggle').classList.add('d-none');
}

function toggleTemperatureUnit() {
    isCelsius = !isCelsius;
    const button = document.getElementById('unitToggle');
    button.textContent = isCelsius ? '°F' : '°C';

    if (currentWeatherData) {
        displayCurrentWeather(currentWeatherData);
    }
    if (currentForecastData) {
        displayForecast(currentForecastData);
    }
}

function celsiusToFahrenheit(celsius) {
    return Math.round((celsius * 9/5) + 32);
}

function changeBackgroundByWeather(description) {
    const body = document.body;
    const desc = description.toLowerCase();

    if (desc.includes('clear') || desc.includes('sun')) {
        body.style.background = 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)';
    } else if (desc.includes('rain') || desc.includes('drizzle')) {
        body.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
    } else if (desc.includes('cloud')) {
        body.style.background = 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)';
    } else if (desc.includes('snow')) {
        body.style.background = 'linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%)';
    } else if (desc.includes('thunder') || desc.includes('storm')) {
        body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    } else {
        body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
}

// API configuration with the correct endpoint
const API_KEY = '232327a71eca66cfc681f5110c0c7709';

// Default cities to show on the dashboard
const defaultCities = [
    "New York", "London", "Paris", "Tokyo", 
    "Sydney", "Berlin", "Rome", "Madrid"
];

// Utility function to convert Kelvin to Celsius
function kelvinToCelsius(kelvin) {
    return Math.round(kelvin - 273.15);
}

// Utility function to format wind speed
function formatWindSpeed(speed) {
    return Math.round(speed * 3.6); // Convert m/s to km/h
}

// Function to fetch weather data for a single city
async function fetchCityWeather(city) {
    try {
        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}`
        );
        
        if (!response.ok) {
            throw new Error(`Weather data not found for ${city}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error fetching data for ${city}:`, error);
        return null;
    }
}

// Function to fetch weather data for coordinates
async function fetchWeatherByCoords(lat, lon) {
    try {
        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}`
        );
        
        if (!response.ok) {
            throw new Error('Weather data not found for your location');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching data for your location:', error);
        return null;
    }
}

// Function to update the main location weather display
function updateMainLocation(weatherData) {
    if (!weatherData) return;

    document.querySelector('.location-name').textContent = weatherData.name;
    document.getElementById('main-temp').textContent = 
        `${kelvinToCelsius(weatherData.main.temp)}°C`;
    document.getElementById('main-humidity').textContent = 
        `${weatherData.main.humidity}%`;
    document.getElementById('main-wind').textContent = 
        `${formatWindSpeed(weatherData.wind.speed)} km/h`;
    document.getElementById('main-conditions').textContent = 
        weatherData.weather[0].main;
}

// Function to create a weather card for a city
function createCityCard(weatherData) {
    if (!weatherData) return null;

    const card = document.createElement('div');
    card.classList.add('city-card');
    
    const iconUrl = `https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@2x.png`;
    
    card.innerHTML = `
        <div class="city-info">
            <div class="weather-icon">
                <img src="${iconUrl}" alt="${weatherData.weather[0].description}">
            </div>
            <div class="city-details">
                <span class="city-name">${weatherData.name}</span>
                <span class="city-weather">${weatherData.weather[0].main}</span>
            </div>
        </div>
        <div class="temperature">${kelvinToCelsius(weatherData.main.temp)}°C</div>
    `;
    
    return card;
}

// Function to populate the cities grid with real-time data
async function populateCityCards() {
    const citiesGrid = document.querySelector('.cities-grid');
    citiesGrid.innerHTML = '<div class="spinner"></div>';

    try {
        // Fetch weather data for all default cities in parallel
        const weatherDataPromises = defaultCities.map(city => 
            fetchCityWeather(city)
        );
        const weatherDataResults = await Promise.all(weatherDataPromises);

        // Clear loading spinner
        citiesGrid.innerHTML = '';

        // Create and append cards for each city
        weatherDataResults.forEach(weatherData => {
            if (weatherData) {
                const card = createCityCard(weatherData);
                if (card) citiesGrid.appendChild(card);
            }
        });

        // Get user's current location and update main location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const { latitude, longitude } = position.coords;
                const userWeatherData = await fetchWeatherByCoords(latitude, longitude);
                if (userWeatherData) {
                    updateMainLocation(userWeatherData);
                }
            }, (error) => {
                console.error('Error getting user location:', error);
                // Fallback to the first valid city data if location access is denied
                const firstValidData = weatherDataResults.find(data => data !== null);
                if (firstValidData) {
                    updateMainLocation(firstValidData);
                }
            });
        } else {
            // Fallback to the first valid city data if geolocation is not supported
            const firstValidData = weatherDataResults.find(data => data !== null);
            if (firstValidData) {
                updateMainLocation(firstValidData);
            }
        }
    } catch (error) {
        console.error('Error populating city cards:', error);
        citiesGrid.innerHTML = '<div class="error-message active">Failed to load weather data</div>';
    }
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Function to handle search
async function handleSearch(searchValue) {
    if (!searchValue.trim()) {
        dropdown.classList.remove('active');
        return;
    }

    try {
        const weatherData = await fetchCityWeather(searchValue);
        
        if (weatherData) {
            dropdown.innerHTML = '';
            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            
            const iconUrl = `https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@2x.png`;
            
            div.innerHTML = `
                <div class="city-info">
                    <div class="weather-icon">
                        <img src="${iconUrl}" alt="${weatherData.weather[0].description}">
                    </div>
                    <div class="city-details">
                        <span class="city-name">${weatherData.name}</span>
                        <span class="city-weather">${weatherData.weather[0].description}</span>
                    </div>
                </div>
            `;
            dropdown.appendChild(div);
            dropdown.classList.add('active');
        } else {
            dropdown.classList.remove('active');
        }
    } catch (error) {
        console.error('Error fetching search data:', error);
        dropdown.classList.remove('active');
    }
}

const searchInput = document.querySelector('.search-input');
const dropdown = document.querySelector('.dropdown');

searchInput.addEventListener('input', debounce((event) => {
    handleSearch(event.target.value);
}, 500));

// Initial population of city cards
populateCityCards();

// Modal functionality
const loginBtn = document.querySelector('.login_btn');
const modalOverlay = document.querySelector('.modal-overlay');
const modalClose = document.querySelector('.modal-close');
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

// Open modal
loginBtn.addEventListener('click', () => {
    modalOverlay.classList.add('active');
});

// Close modal when clicking outside
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
    }
});

// Close modal with X button
modalClose.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
});

// Tab switching
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and contents
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Add active class to clicked tab and corresponding content
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages
    const alerts = document.querySelectorAll('.alert');
    
    // Log number of alerts found (helps with debugging)
    console.log(`Number of alerts found: ${alerts.length}`);
    
    alerts.forEach(alert => {
        // Automatically hide alerts after 5 seconds
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });

    // Add close button functionality to dismiss alerts
    const closeButtons = document.querySelectorAll('.alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').style.display = 'none';
        });
    });
});
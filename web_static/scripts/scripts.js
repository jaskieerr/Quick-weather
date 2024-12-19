const citiesWithWeather = [
    { name: "New York", weather: "Partly Cloudy", temp: "24°C", icon: "☁️" },
    { name: "London", weather: "Light Rain", temp: "18°C", icon: "🌧️" },
    { name: "Paris", weather: "Sunny", temp: "22°C", icon: "☀️" },
    { name: "Tokyo", weather: "Cloudy", temp: "20°C", icon: "⛅" },
    { name: "Sydney", weather: "Clear Sky", temp: "26°C", icon: "☀️" },
    { name: "Berlin", weather: "Thunderstorm", temp: "19°C", icon: "⛈️" },
    { name: "Rome", weather: "Hot", temp: "28°C", icon: "🌡️" },
    { name: "Madrid", weather: "Clear", temp: "25°C", icon: "☀️" }
];

const searchInput = document.querySelector('.search-input');
const dropdown = document.querySelector('.dropdown');
const citiesGrid = document.querySelector('.cities-grid');

// Populate the grid with city cards
function populateCityCards() {
    citiesGrid.innerHTML = '';
    citiesWithWeather.forEach(city => {
        const card = document.createElement('div');
        card.classList.add('city-card');
        card.innerHTML = `
            <div class="city-info">
                <div class="weather-icon">${city.icon}</div>
                <div class="city-details">
                    <span class="city-name">${city.name}</span>
                    <span class="city-weather">${city.weather}</span>
                </div>
            </div>
            <div class="temperature">${city.temp}</div>
        `;
        citiesGrid.appendChild(card);
    });
}

// Show filtered cities in dropdown
function showDropdownItems(searchValue) {
    dropdown.innerHTML = '';
    
    const filteredCities = citiesWithWeather.filter(city => 
        city.name.toLowerCase().includes(searchValue.toLowerCase())
    );

    if (filteredCities.length > 0 && searchValue) {
        filteredCities.forEach(city => {
            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            div.innerHTML = `
                <div class="city-info">
                    <div class="weather-icon">${city.icon}</div>
                    <div class="city-details">
                        <span class="city-name">${city.name}</span>
                        <span class="city-weather">${city.weather}</span>
                    </div>
                </div>
                <div class="temperature">${city.temp}</div>
            `;
            
            div.addEventListener('click', () => {
                searchInput.value = city.name;
                dropdown.classList.remove('active');
            });
            
            dropdown.appendChild(div);
        });
    }
}

// Event Listeners
searchInput.addEventListener('input', (e) => {
    if (e.target.value) {
        showDropdownItems(e.target.value);
        dropdown.classList.add('active');
    } else {
        dropdown.classList.remove('active');
    }
});

searchInput.addEventListener('focus', () => {
    if (searchInput.value) {
        showDropdownItems(searchInput.value);
        dropdown.classList.add('active');
    }
});

document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('active');
    }
});

// Initialize the city cards
populateCityCards();
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

// Prevent form submission (for demo)
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your form submission logic here
        alert('Form submitted! (Demo only)');
    });
});
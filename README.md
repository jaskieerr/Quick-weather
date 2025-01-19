---

# Quick-weather

## Description

Quick-weather is a professional weather application developed as part of an end-of-studies portfolio project. This application provides accurate and up-to-date weather information with a sleek and user-friendly interface. It includes a "Favorite Cities" tab, allowing users to save and quickly access weather information for their preferred locations.

## Features

- **Current Weather**: Real-time weather updates for your current location.
- **Forecast**: Detailed 7-day weather forecast.
- **Search**: Search for weather information by city or ZIP code.
- **Favorite Cities**: Save and quickly access weather information for your favorite cities.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Technologies Used

### Frontend

- **CSS**: Styling the user interface, ensuring a responsive and modern look.
- **JavaScript**: Handling client-side logic and API interactions.
- **HTML**: Structuring the web pages.

### Backend

- **Python**: Backend services and API integration.
- **Nginx**: Web server for serving the application.
- **HAProxy**: Load balancer to distribute traffic across multiple servers.
- **Firewall**: Security measure to protect the backend infrastructure.
- **PostgreSQL**: Relational database for storing user data and weather information.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/jaskieerr/Quick-weather.git
   cd Quick-weather
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Configure the backend:
   - Ensure Nginx and HAProxy are properly configured on your backend machine.
   - Set up firewall rules to allow necessary traffic.
   - Install and configure PostgreSQL as the database.

## Usage

1. Open your browser and navigate to `http://localhost:3000`.
2. Enter your location or allow the app to access your current location.
3. Use the "Favorite Cities" tab to save and view weather information for your preferred locations.
4. View current weather updates and forecasts.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Contact

For any inquiries, contact me at nizar.zairat@gmail.com


# Quick Weather

Quick Weather is a web portfolio project that provides weather updates. It is built using a variety of technologies to ensure a robust and secure application.

## Technologies Used

### Backend
- **Flask**: A lightweight WSGI web application framework in Python.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Password Hashing**: Ensures secure storage of user passwords.
- **Routes**: Defined for various functionalities of the application.

### Frontend
- **HTML**: The standard markup language for creating web pages.
- **CSS**: Used for describing the presentation of a document written in HTML.
- **JavaScript**: A programming language that enables interactive web pages.

### Hosting and Deployment
- **Nginx**: A high-performance HTTP server and reverse proxy.
- **HAProxy**: Provides load balancing across two servers using the round-robin method.
- **SSL/TLS Termination**: Ensures secure communication over the network.
- **Basic Firewall**: Provides a layer of security by controlling incoming and outgoing network traffic.

## Features
- **Weather Updates**: Get real-time weather information.
- **Secure Authentication**: User passwords are securely hashed.
- **Load Balancing**: Ensures high availability and reliability.
- **SSL/TLS**: Secure data transmission.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/quick-weather.git
    ```
2. Navigate to the project directory:
    ```bash
    cd quick-weather
    ```
3. Set up the virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Set up the PostgreSQL database and configure the environment variables.

6. Run the application:
    ```bash
    flask run
    ```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact
For any inquiries, please contact nizar.zairat@gmail.com

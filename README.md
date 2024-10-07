A Python application to fetch, store, analyze, and visualize real-time weather data for any city using the OpenWeatherMap API.

Features:
    Fetch & Display Weather: Get current weather details for any city.
    Store Data: Save weather information in an SQLite database.
    Visualize Data: Create bar plots for weather parameters like temperature, humidity, wind speed, etc.
    Analyze Data: Perform basic statistical analysis (e.g., average temperature).
    Display Stored Data: View previously saved weather records in a table.

Installation:
    1. Clone the repository:
          git clone <repository_url>
          cd weather-tracker-analyzer
          
    2. Install dependencies:
          pip install requests pandas matplotlib seaborn
    
    3. Run the application:
          python weather_tracker.py
    
API Key:
    Replace the placeholder in the code with your OpenWeatherMap API key:
    API_KEY = 'your_api_key_here'

Usage:
    Run the program and choose from the menu:
    View, analyze, visualize, or store weather data.
    Display previously stored data.
    Enter the city name as prompted.

Requirements:
    Python 3.x
    SQLite
    Required Python Libraries:
    requests
    pandas
    matplotlib
    seaborn

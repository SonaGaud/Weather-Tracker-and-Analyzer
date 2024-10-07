import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Constants
API_KEY = 'd3fd4c36a3541e29bbcbc221941fdcf6'  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Initialize SQLite database
conn = sqlite3.connect('weather_d.db')  # Changed database name to weather_d
cursor = conn.cursor()

# Create structured weather_data table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        feels_like REAL,
        temp_min REAL,
        temp_max REAL,
        pressure INTEGER,
        humidity INTEGER,
        wind_speed REAL,
        description TEXT,
        timestamp TEXT
    )
''')
conn.commit()

def kelvin_to_celsius(kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return kelvin - 273.15

def fetch_weather(city):
    """Fetch current weather data for the given city using OpenWeatherMap API."""
    complete_url = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(complete_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("City not found!")
        return None

def store_weather_data(city, weather_data):
    """Store the weather data in the database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = kelvin_to_celsius(weather_data['main']['temp'])
    feels_like = kelvin_to_celsius(weather_data['main']['feels_like'])
    temp_min = kelvin_to_celsius(weather_data['main']['temp_min'])
    temp_max = kelvin_to_celsius(weather_data['main']['temp_max'])
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    description = weather_data['weather'][0]['description']
    
    cursor.execute('''
        INSERT INTO weather_data 
        (city, temperature, feels_like, temp_min, temp_max, pressure, humidity, wind_speed, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, temp, feels_like, temp_min, temp_max, pressure, humidity, wind_speed, description, timestamp))
    conn.commit()
    print("Data stored successfully.")

def view_weather_data(city):
    """Fetch and display the current weather data for the city."""
    weather_data = fetch_weather(city)
    if weather_data:
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {kelvin_to_celsius(weather_data['main']['temp']):.2f}°C")
        print(f"Feels Like: {kelvin_to_celsius(weather_data['main']['feels_like']):.2f}°C")
        print(f"Min Temperature: {kelvin_to_celsius(weather_data['main']['temp_min']):.2f}°C")
        print(f"Max Temperature: {kelvin_to_celsius(weather_data['main']['temp_max']):.2f}°C")
        print(f"Pressure: {weather_data['main']['pressure']} hPa")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Weather: {weather_data['weather'][0]['description']}")
        return weather_data

def display_stored_data():
    """Display all stored weather data in a structured table format without asking for city name."""
    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'City', 'Temperature (°C)', 'Feels Like (°C)', 'Min Temp (°C)', 
                                         'Max Temp (°C)', 'Pressure (hPa)', 'Humidity (%)', 'Wind Speed (m/s)', 
                                         'Description', 'Timestamp'])
        print(df)
    else:
        print("No data found in the database.")

def visualize_weather_data(weather_data):
    """Visualize the current weather data using a bar plot."""
    temp_data = {
        'Temperature (°C)': kelvin_to_celsius(weather_data['main']['temp']),
        'Feels Like (°C)': kelvin_to_celsius(weather_data['main']['feels_like']),
        'Min Temp (°C)': kelvin_to_celsius(weather_data['main']['temp_min']),
        'Max Temp (°C)': kelvin_to_celsius(weather_data['main']['temp_max']),
        'Wind Speed (m/s)': weather_data['wind']['speed'],
        'Pressure (hPa)': weather_data['main']['pressure'],
        'Humidity (%)': weather_data['main']['humidity']
    }
    categories = list(temp_data.keys())
    values = list(temp_data.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=categories, y=values, palette="coolwarm")
    plt.title(f"Weather Data Visualization for {weather_data['name']}")
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_weather_data(weather_data):
    """Analyze the current weather data (simple statistical analysis)."""
    temp = kelvin_to_celsius(weather_data['main']['temp'])
    feels_like = kelvin_to_celsius(weather_data['main']['feels_like'])
    temp_min = kelvin_to_celsius(weather_data['main']['temp_min'])
    temp_max = kelvin_to_celsius(weather_data['main']['temp_max'])

    print(f"Average Temperature: {(temp_min + temp_max) / 2:.2f}°C")
    print(f"Feels Like Temperature: {feels_like:.2f}°C")

def main():
    while True:
        print("\nWeather Data Aggregator and Analyzer")
        print("1. View current weather data")
        print("2. Visualize current weather data")
        print("3. Analyze current weather data")
        print("4. Store current weather data in the database")
        print("5. Display stored weather data")
        print("6. Exit")

        choice = input("Enter the number of your choice from a: ")

        if choice == '6':
            break

        if choice in ['1', '2', '3', '4']:
            city = input("Enter city name: ")

        if choice == '1':
            weather_data = view_weather_data(city)

        elif choice == '2':
            weather_data = fetch_weather(city)
            if weather_data:
                visualize_weather_data(weather_data)

        elif choice == '3':
            weather_data = fetch_weather(city)
            if weather_data:
                analyze_weather_data(weather_data)

        elif choice == '4':
            weather_data = fetch_weather(city)
            if weather_data:
                store_weather_data(city, weather_data)

        elif choice == '5':
            display_stored_data()

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

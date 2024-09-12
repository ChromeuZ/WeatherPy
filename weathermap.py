import os
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

def fetch_temperature_data(lat, lng, api_key):
    base_url = "https://api.stormglass.io/v2/weather/point"
    end = datetime.now()
    start = end - timedelta(days=7)  # Fetch data for the last 7 days
    
    params = {
        'lat': lat,
        'lng': lng,
        'params': 'airTemperature',
        'start': start.isoformat(),
        'end': end.isoformat()
    }
    
    headers = {
        'Authorization': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def process_temperature_data(data):
    if data is None or 'hours' not in data:
        print("No valid data to process.")
        return None

    hours = data['hours']
    df = pd.DataFrame(hours)
    df['time'] = pd.to_datetime(df['time'])
    df['temperature'] = df['airTemperature'].apply(lambda x: x.get('sg', None))
    return df[['time', 'temperature']]

def analyze_temperature_data(df):
    if df is None or df.empty:
        print("No data to analyze.")
        return

    avg_temp = df['temperature'].mean()
    max_temp = df['temperature'].max()
    min_temp = df['temperature'].min()
    
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Maximum Temperature: {max_temp:.2f}°C")
    print(f"Minimum Temperature: {min_temp:.2f}°C")

def plot_temperature_data(df):
    if df is None or df.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['temperature'], color='tab:red')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Air Temperature Over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    lat = float(input("Enter latitude: "))
    lng = float(input("Enter longitude: "))
    
    # Fetch API key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API key not found. Please set the API_KEY environment variable.")
        return
    
    data = fetch_temperature_data(lat, lng, api_key)
    if data:
        df = process_temperature_data(data)
        if df is not None:
            analyze_temperature_data(df)
            plot_temperature_data(df)
    else:
        print("Failed to fetch data. Please check your inputs and try again.")

if __name__ == "__main__":
    main()

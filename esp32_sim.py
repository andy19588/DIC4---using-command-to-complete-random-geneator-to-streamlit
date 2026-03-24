import time
import requests
import random

def generate_sensor_data():
    # Simulate DHT11 data and ESP32 WiFi metadata
    return {
        "temperature": round(random.uniform(20.0, 30.0), 1),
        "humidity": round(random.uniform(40.0, 60.0), 1)
    }

def main():
    url = "http://127.0.0.1:5000/sensor"
    print("Starting ESP32 Simulator...")
    print(f"Sending POST requests to {url} every 5 seconds.")
    
    while True:
        data = generate_sensor_data()
        try:
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 201:
                print(f"Success: Sent {data}")
            else:
                print(f"Error: Server responded with status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to server: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()

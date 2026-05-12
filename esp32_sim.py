import time
import sqlite3
import random
from datetime import datetime

DB_NAME = 'aiotdb.db'

def init_db():
    """Create the sensors table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            temperature REAL,
            humidity REAL
        )
    ''')
    conn.commit()
    conn.close()

def generate_sensor_data():
    """Simulate DHT11 sensor: temperature 20~30°C, humidity 40~60%."""
    temperature = round(random.uniform(20.0, 30.0), 1)
    humidity = round(random.uniform(40.0, 60.0), 1)
    return temperature, humidity

def insert_data(temperature, humidity):
    """Insert one record into the sensors table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO sensors (timestamp, temperature, humidity)
        VALUES (?, ?, ?)
    ''', (current_time, temperature, humidity))
    conn.commit()
    conn.close()
    return current_time

def main():
    init_db()
    print("=" * 50)
    print("DHT11 Sensor Simulator Started")
    print(f"Database: {DB_NAME} | Table: sensors")
    print("Generating 1 record every 2 seconds...")
    print("=" * 50)

    count = 0
    while True:
        temperature, humidity = generate_sensor_data()
        ts = insert_data(temperature, humidity)
        count += 1
        print(f"[{ts}] #{count} | Temp={temperature}°C, Humidity={humidity}%")
        time.sleep(2)

if __name__ == "__main__":
    main()

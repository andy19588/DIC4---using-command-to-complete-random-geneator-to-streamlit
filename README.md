# DIC4 HW1 - DHT11 Random Sensor Simulator to Streamlit

## Project Overview

This project simulates a DHT11 temperature and humidity sensor using Python random number generation. Data is inserted into a SQLite3 database (`aiotdb.db`) every **2 seconds** and visualized dynamically using **Streamlit**.

## Architecture

```
esp32_sim.py (Python)  →  aiotdb.db (SQLite3)  →  dashboard.py (Streamlit)
   Random Generator          sensors table           Line Charts + KPIs
   Every 2 seconds           Auto-created            Auto-refresh 2s
```

- **`esp32_sim.py`**: Generates **1 record every 2 seconds** with random temperature (20–30°C) and humidity (40–60%) and inserts directly into SQLite3.
- **`aiotdb.db`**: SQLite3 database with a `sensors` table (id, timestamp, temperature, humidity).
- **`dashboard.py`**: Streamlit dashboard that reads from the database and displays real-time line charts for temperature and humidity, with auto-refresh every 2 seconds.

## sensors Table Schema

| Column      | Type    | Description                        |
|-------------|---------|------------------------------------|
| id          | INTEGER | Primary key, auto-increment        |
| timestamp   | DATETIME| Record creation time               |
| temperature | REAL    | Simulated temperature (20–30°C)    |
| humidity    | REAL    | Simulated humidity (40–60%)        |

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start the sensor simulator
python esp32_sim.py

# Terminal 2: Start the Streamlit dashboard
python -m streamlit run dashboard.py
```

Then open http://localhost:8501 in your browser to see the dashboard.

## Requirements

- Python 3.x
- streamlit
- pandas
- sqlite3 (built-in)

## GitHub Repository

[DIC4---using-command-to-complete-random-geneator-to-streamlit](https://github.com/andy19588/DIC4---using-command-to-complete-random-geneator-to-streamlit)

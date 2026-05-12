# DIC4 HW1 - DHT11 Random Sensor Simulator to Streamlit

## 🔗 Live Demo

👉 [**Click here for Live Demo**](https://dic4---using-command-to-complete-random-geneator-to-app-wzrxat.streamlit.app/)

## Project Overview

This project simulates a DHT11 temperature and humidity sensor using Python random number generation. Data is inserted into a SQLite3 database (`aiotdb.db`) every **2 seconds** and visualized dynamically using **Streamlit**.

## Architecture

```
Background Thread (Python)  →  aiotdb.db (SQLite3)  →  Streamlit Dashboard
   Random Generator              sensors table           Line Charts + KPIs
   Every 2 seconds               Auto-created            Auto-refresh 2s
```

- **`esp32_sim.py`**: Standalone simulator — generates **1 record every 2 seconds** with random temperature (20–30°C) and humidity (40–60%) and inserts directly into SQLite3.
- **`dashboard.py`**: Streamlit dashboard with **built-in background simulator**. Reads from the database and displays real-time line charts for temperature and humidity, auto-refreshes every 2 seconds. Can run independently on Streamlit Cloud.
- **`aiotdb.db`**: SQLite3 database with a `sensors` table (id, timestamp, temperature, humidity). Auto-created at runtime.

## sensors Table Schema

| Column      | Type    | Description                        |
|-------------|---------|------------------------------------|
| id          | INTEGER | Primary key, auto-increment        |
| timestamp   | DATETIME| Record creation time               |
| temperature | REAL    | Simulated temperature (20–30°C)    |
| humidity    | REAL    | Simulated humidity (40–60%)        |

## Setup & Run (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Option A: Run simulator + dashboard separately
python esp32_sim.py          # Terminal 1
python -m streamlit run dashboard.py  # Terminal 2

# Option B: Run dashboard only (has built-in simulator)
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

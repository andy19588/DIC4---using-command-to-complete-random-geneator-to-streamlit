import streamlit as st
import sqlite3
import pandas as pd
import time
import random
import threading
from datetime import datetime

st.set_page_config(page_title="AIoT Sensor Dashboard", layout="wide")

DB_NAME = 'aiotdb.db'

# ──────────────────────────────────────────────
# Database & Sensor Simulator (background thread)
# ──────────────────────────────────────────────

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

def sensor_loop():
    """Background thread: generate 1 DHT11 record every 2 seconds."""
    init_db()
    while True:
        temperature = round(random.uniform(20.0, 30.0), 1)
        humidity = round(random.uniform(40.0, 60.0), 1)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO sensors (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                (current_time, temperature, humidity)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass
        time.sleep(2)

# Start the background simulator exactly once per server process
if 'simulator_started' not in st.session_state:
    st.session_state.simulator_started = True
    init_db()
    t = threading.Thread(target=sensor_loop, daemon=True)
    t.start()

# ──────────────────────────────────────────────
# Dashboard UI
# ──────────────────────────────────────────────

st.title("🌡️ DHT11 Sensor Dashboard")
st.caption("Real-time simulated temperature & humidity → SQLite3 (aiotdb.db) → Streamlit")

def load_data():
    """Load sensor data from SQLite3 database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT id, timestamp, temperature, humidity FROM sensors ORDER BY id DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.info("⏳ Generating sensor data... please wait a few seconds.")
else:
    # --- KPI Metrics ---
    latest = df.iloc[0]
    total_records = len(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Latest Temperature", f"{latest['temperature']:.1f} °C")
    with col2:
        st.metric("💧 Latest Humidity", f"{latest['humidity']:.1f} %")
    with col3:
        st.metric("📊 Total Records", f"{total_records}")

    st.markdown("---")

    # --- Line Charts (latest 50 records) ---
    df_chart = df.head(50).copy()
    df_chart = df_chart.sort_values('timestamp')
    df_chart.set_index('timestamp', inplace=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Temperature History")
        st.line_chart(df_chart['temperature'], height=300)

    with chart_col2:
        st.subheader("Humidity History")
        st.line_chart(df_chart['humidity'], height=300)

    st.markdown("---")

    # --- Raw Data Table ---
    st.subheader("📋 Raw Data (Latest 100 records)")
    st.dataframe(df.head(100), width='stretch')

# --- Auto Refresh every 2 seconds ---
time.sleep(2)
st.rerun()

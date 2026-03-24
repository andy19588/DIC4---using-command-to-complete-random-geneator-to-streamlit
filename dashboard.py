import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="AIoT Dashboard", layout="wide")
st.title("ESP32 Sensor Dashboard")

DB_NAME = 'aiotdb.db'

def load_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT timestamp, device_id, temperature, humidity, wifi_ssid, wifi_rssi FROM sensors ORDER BY timestamp DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available yet.")
else:
    # KPIs
    latest = df.iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Temperature", f"{latest['temperature']:.1f} °C")
    with col2:
        st.metric("Latest Humidity", f"{latest['humidity']:.1f} %")
    with col3:
        st.metric("WiFi Network", latest['wifi_ssid'])
    with col4:
        st.metric("WiFi RSSI", f"{latest['wifi_rssi']} dBm")

    st.markdown("---")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    df_chart = df.copy()
    df_chart.set_index('timestamp', inplace=True)
    df_chart = df_chart.sort_index()

    with chart_col1:
        st.subheader("Temperature History")
        st.line_chart(df_chart['temperature'], height=300)
        
    with chart_col2:
        st.subheader("Humidity History")
        st.line_chart(df_chart['humidity'], height=300)

    st.markdown("---")
    
    # Table
    st.subheader("Raw Data")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Auto-refresh helper button
    if st.button("Refresh Data"):
        st.rerun()

import time
time.sleep(2)
st.rerun()

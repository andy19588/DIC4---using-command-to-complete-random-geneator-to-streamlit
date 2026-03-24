# DIC4 MVC Web-MySQL-DB-Flask AIoT Demo

This repository fulfills the requirements for **Lecture 4 HW1**:
1. **GitHub Repository**: [DIC4---using-command-to-complete-random-geneator-to-streamlit](https://github.com/andy19588/DIC4---using-command-to-complete-random-geneator-to-streamlit)
2. **Live Demo / Live Share**: [https://f97c7c6d646fde.lhr.life](https://f97c7c6d646fde.lhr.life)

## Project Overview (MVC Architecture)
- **Model**: SQLite3 (`aiotdb.db`) acts as our persistent data layer (equivalent to the MySQL schema mentioned in Notion).
- **View**: 
  1. **Streamlit Dashboard** (`dashboard.py`): Real-time KPI and line charts.
  2. **Highcharts View** (`/highcharts`): A pure HTML/JS page rendering a Line chart and a Pie chart example.
- **Controller**: **Flask** (`app.py`), which orchestrates routes, handles JSON POSTs, and serves endpoints.

## Features implemented from Notion
* **Step 1 (Web Fundamentals):** JS-based random simulator sending POSTs via Fetch API to Flask.
* **Step 2 (Flask Python Web with DB Interaction):** Flask backend interacting securely with a SQL database using the Python connector.
* **Step 3 (Database Schema):** `sensors` table collecting `temperature`, `humidity`, and generating auto-incrementing timestamps.
* **Step 4 (Data Visualization):** 
  * Included a `show()` function for a Pie Chart & Line chart using **Highcharts**.
  * Streamlit rendering dynamic line charts for temperature and humidity.
* **Step 5 (Dynamic Data Flow):** Periodic AJAX requests updating the dashboard automatically every 2 seconds without page reloading.

## Setup Instructions
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Start Flask Backend & Web Simulator
python app.py

# Start Streamlit Dashboard
streamlit run dashboard.py
```

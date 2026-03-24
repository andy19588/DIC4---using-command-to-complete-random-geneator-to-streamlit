import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = 'aiotdb.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            device_id TEXT,
            temperature REAL,
            humidity REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/simulator', methods=['GET'])
def simulator():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML JS Web Simulator</title>
        <script>
            function generateData() {
                const temp = (Math.random() * 10 + 20).toFixed(1);
                const hum = (Math.random() * 20 + 40).toFixed(1);
                const rssi = Math.floor(Math.random() * 35) - 85;
                const reqData = {
                    device_id: "WEB_JS_SIM_01",
                    temperature: parseFloat(temp),
                    humidity: parseFloat(hum)
                };
                
                fetch('/sensor', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(reqData)
                })
                .then(response => response.json())
                .then(d => {
                    const log = document.getElementById('log');
                    log.innerHTML = `<p>Sent: Temp=${temp}C, Hum=${hum}%</p>` + log.innerHTML;
                })
                .catch(error => console.error('Error:', error));
            }
            // Generate data every 2 seconds
            setInterval(generateData, 2000);
        </script>
    </head>
    <body>
        <h1>Web Browser Sensor Simulator</h1>
        <p>This page randomly generates temperature and humidity data every 2 seconds using JavaScript and inserts it into the SQLite backend via the API.</p>
        <div id="log" style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;"></div>
    </body>
    </body>
    </html>
    '''

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT temperature, humidity, timestamp FROM sensors ORDER BY timestamp DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    
    rows.reverse() # chronological
    
    data = {
        'categories': [row[2] for row in rows],
        'temperature': [row[0] for row in rows],
        'humidity': [row[1] for row in rows],
        'pie_data': [
            {'name': 'Temp > 25°C', 'y': sum(1 for r in rows if r[0] > 25)},
            {'name': 'Temp <= 25°C', 'y': sum(1 for r in rows if r[0] <= 25)}
        ]
    }
    return jsonify(data)

@app.route('/highcharts', methods=['GET'])
def highcharts_demo():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Highcharts Visualization</title>
        <script src="https://code.highcharts.com/highcharts.js"></script>
    </head>
    <body onload="show()">
        <h1 style="text-align: center;">Highcharts Data Visualization (Notion Step 4)</h1>
        <div id="line-chart" style="width: 80%; height: 400px; margin: 0 auto;"></div>
        <br>
        <div id="pie-chart" style="width: 80%; height: 400px; margin: 0 auto;"></div>
        
        <script>
            function show() {
                fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    Highcharts.chart('line-chart', {
                        chart: { type: 'line' },
                        title: { text: 'Latest 20 Sensor Readings' },
                        xAxis: { categories: data.categories },
                        yAxis: { title: { text: 'Values' } },
                        series: [
                            { name: 'Temperature (°C)', data: data.temperature },
                            { name: 'Humidity (%)', data: data.humidity }
                        ]
                    });
                    
                    Highcharts.chart('pie-chart', {
                        chart: { type: 'pie' },
                        title: { text: 'Temperature Rules (Pie Chart Example)' },
                        series: [{
                            name: 'Count',
                            colorByPoint: true,
                            data: data.pie_data
                        }]
                    });
                })
                .catch(err => console.error('Error fetching data:', err));
            }
            setInterval(show, 2000);
        </script>
    </body>
    </html>
    '''

@app.route('/sensor', methods=['POST', 'OPTIONS'])
def sensor_data():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    device_id = data.get('device_id', 'unknown')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    
    if temperature is None or humidity is None:
        return jsonify({"error": "Missing temperature or humidity"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO sensors (device_id, temperature, humidity, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (device_id, temperature, humidity, current_time))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)

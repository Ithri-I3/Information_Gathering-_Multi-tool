import json
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to SQLite database (it will create the file if it doesn't exist)
def get_db_connection():
    conn = sqlite3.connect('system_info.db')
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            os_info TEXT,
            cpu_info TEXT,
            memory_info TEXT,
            storage_info TEXT,
            devices_info TEXT,
            battery_info TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/system_info', methods=['POST'])
def receive_system_info():
    data = request.get_json()
    if data:
        # Print to console
        print("Received data:", data)

        # Insert data into SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO system_info (os_info, cpu_info, memory_info, storage_info, devices_info, battery_info)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            json.dumps(data.get('OS_Info')),
            json.dumps(data.get('CPU_Info')),
            json.dumps(data.get('Memory_Info')),
            json.dumps(data.get('Storage_Info')),
            json.dumps(data.get('Devices_Info')),
            json.dumps(data.get('Battery_Info'))
        ))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Data received and saved"}), 200
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400

# Endpoint to retrieve all stored data
@app.route('/api/system_info/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM system_info')
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

# Initialize the table when the server starts
create_table()

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

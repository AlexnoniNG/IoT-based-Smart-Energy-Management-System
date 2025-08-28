import paho.mqtt.client as mqtt
import sqlite3
import json
import time

# MQTT settings
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/#"

# SQLite database setup
def init_db():
    conn = sqlite3.connect("energy_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (timestamp TEXT, sensor_type TEXT, value REAL)''')
    conn.commit()
    conn.close()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        sensor_type = msg.topic.split("/")[-1]
        value = data["value"]
        
        # Store in SQLite
        conn = sqlite3.connect("energy_data.db")
        c = conn.cursor()
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (?, ?, ?)",
                  (timestamp, sensor_type, value))
        conn.commit()
        conn.close()
        print(f"Stored: {timestamp}, {sensor_type}, {value}")
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

# Initialize database
init_db()

# Start MQTT loop
client.loop_forever()
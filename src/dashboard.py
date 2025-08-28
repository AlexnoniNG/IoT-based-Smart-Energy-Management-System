import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import json
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import atexit
import queue
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load model and scaler
try:
    model = joblib.load('src/model.pkl')
    scaler = joblib.load('src/scaler.pkl')
except FileNotFoundError:
    st.error("Model or scaler file not found. Run smart_energy_prediction.ipynb first.")
    st.stop()

# MQTT settings
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/#"

# Message queue for thread-safe MQTT processing
message_queue = queue.Queue()

# Database connection
def fetch_data(sensor_type, limit=100):
    try:
        conn = sqlite3.connect("energy_data.db")
        df = pd.read_sql_query(f"SELECT timestamp, value FROM sensor_data WHERE sensor_type = '{sensor_type}' ORDER BY timestamp DESC LIMIT {limit}", conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT broker with code {rc}")
        client.subscribe(TOPIC)
    else:
        logger.error(f"MQTT connection failed with code {rc}")
        st.error(f"MQTT connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        sensor_type = msg.topic.split("/")[-1]
        message_queue.put((sensor_type, data["value"]))
        logger.info(f"Received MQTT message: {sensor_type} = {data['value']}")
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    logger.info(f"Connecting to MQTT broker at {BROKER}:{PORT}")
    client.connect(BROKER, PORT, 60)
except Exception as e:
    logger.error(f"Failed to connect to MQTT broker: {e}")
    st.error(f"Failed to connect to MQTT broker: {e}")
    st.stop()
client.loop_start()

# Register cleanup
def cleanup():
    logger.info("Cleaning up MQTT client")
    client.loop_stop()
    client.disconnect()
atexit.register(cleanup)

# Streamlit dashboard
st.set_page_config(page_title="Smart Energy Management System", layout="wide")
st.title("Smart Energy Management System")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Home")
st.sidebar.button("Settings")
st.sidebar.button("About")

# Process queued MQTT messages in main thread
def process_queue():
    while not message_queue.empty():
        try:
            sensor_type, value = message_queue.get_nowait()
            st.session_state[sensor_type] = value
            logger.info(f"Processed queued message: {sensor_type} = {value}")
        except queue.Empty:
            break
        except Exception as e:
            logger.error(f"Error processing queued message: {e}")

# Energy consumption section
st.subheader("Energy Usage")
energy_data = fetch_data("energy")
if not energy_data.empty:
    fig, ax = plt.subplots()
    ax.plot(pd.to_datetime(energy_data["timestamp"]), energy_data["value"], label="Global Active Power (kW)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Power (kW)")
    ax.legend()
    st.pyplot(fig)
else:
    st.write("No energy data available.")

# Anomaly alerts section
st.subheader("Anomaly Alerts")
process_queue()  # Process queued messages
if "energy" in st.session_state and "temperature" in st.session_state and "humidity" in st.session_state:
    features = np.array([[
        st.session_state["temperature"],
        st.session_state["humidity"],
        pd.Timestamp.now().hour,
        pd.Timestamp.now().day,
        pd.Timestamp.now().month,
        0.1,  # Mock Global_reactive_power
        230.0,  # Mock Voltage
        st.session_state["energy"] * 4  # Mock Global_intensity
    ]])
    try:
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)
        if prediction[0] == 1:
            st.error("High consumption detected! Consider reducing appliance usage.")
        else:
            st.success("No anomalies detected.")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        st.error(f"Prediction error: {e}")
else:
    st.warning("Waiting for sensor data...")

# Weather section
st.subheader("Weather")
process_queue()  # Process queued messages
if "temperature" in st.session_state and "humidity" in st.session_state:
    st.write(f"Temperature: {st.session_state['temperature']:.2f}°C")
    st.write(f"Humidity: {st.session_state['humidity']:.2f}%")
else:
    st.write("Temperature: 22.00°C (simulated)")
    st.write("Humidity: 65.00% (simulated)")

# Controls section
st.subheader("Controls")
if st.button("Reduce AC Load"):
    st.write("AC load reduced by 10% (simulated).")
load_level = st.slider("Adjust Energy Load (%)", 0, 100, 50)
st.write(f"Energy load set to {load_level}%.")
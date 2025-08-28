import pandas as pd
import paho.mqtt.client as mqtt
import json
import time
import numpy as np
import os

# MQTT settings
BROKER = "localhost"
PORT = 1883

# Verify dataset exists
data_path = "data/household_power_consumption.txt"
if not os.path.exists(data_path):
    print(f"Error: Dataset not found at {data_path}. Download from https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption")
    exit(1)

# Load dataset
try:
    print("Loading dataset...")
    df = pd.read_csv(data_path, sep=';', low_memory=False)
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Preprocess dataset
try:
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Global_active_power'] = pd.to_numeric(df['Global_active_power'], errors='coerce')
    df.fillna(df.mean(numeric_only=True), inplace=True)
except Exception as e:
    print(f"Error preprocessing dataset: {e}")
    exit(1)

# Simulate weather data
np.random.seed(42)
df['Temperature'] = np.random.normal(20, 5, len(df))
df['Humidity'] = np.random.normal(60, 10, len(df))

# MQTT client setup
client = mqtt.Client()
try:
    print(f"Connecting to MQTT broker at {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)

# Publish data
print("Publishing data to MQTT topics...")
try:
    for index, row in df.head(1000).iterrows():  # Limit to 1000 records
        energy_data = {"value": row['Global_active_power']}
        temp_data = {"value": row['Temperature']}
        hum_data = {"value": row['Humidity']}
        
        client.publish("sensors/energy", json.dumps(energy_data))
        client.publish("sensors/temperature", json.dumps(temp_data))
        client.publish("sensors/humidity", json.dumps(hum_data))
        
        print(f"Published record {index+1}/1000: Energy={row['Global_active_power']:.2f} kW, Temp={row['Temperature']:.2f}°C, Hum={row['Humidity']:.2f}%")
        time.sleep(1)  # Simulate real-time delay
except Exception as e:
    print(f"Error publishing data: {e}")
finally:
    client.disconnect()
    print("Disconnected from MQTT broker.")
---

# 🏠 IoT-EnergyPredictor

**IoT-EnergyPredictor** is a smart energy management system that simulates IoT devices for real-time monitoring, anomaly detection, and climate-informed optimization in residential buildings. Built with Python, Streamlit, MQTT, and a machine learning backend, it helps reduce energy consumption and offers actionable insights via a user-friendly dashboard.

![Dashboard Screenshot](images/streamlit_dashboard.png)
*Figure 4.3: Streamlit dashboard displaying real-time energy usage, anomaly alerts, and control options.*

---

## 🔧 Key Features

- **📈 Real-Time Monitoring:** Simulates energy and environmental data (temperature, humidity) via MQTT.
- **⚠️ Anomaly Detection:** Detects high-consumption events using a Random Forest model.

  - _Precision:_ 0.8923
  - _Recall:_ 0.8674
  - _F1 Score:_ 0.8797
  - _Accuracy:_ 0.9456
  - _ROC AUC:_ 0.9234

- **🌦️ Climate-Aware Optimization:** Simulates weather-based load control (future-ready for OpenWeatherMap API).
- **📊 Interactive Dashboard:** Built with Streamlit for live insights, alerts, and user control.
- **📡 Modular Architecture:** Designed for scalability with MQTT and SQLite; compatible with cloud platforms like AWS IoT Core.

---

## 📁 Project Structure

```
IoT-EnergyPredictor/
├── src/
│   ├── iot_data_collection.py          # Collects MQTT sensor data
│   ├── simulate_data.py                # Publishes simulated IoT data
│   ├── dashboard.py                    # Streamlit UI for monitoring and control
│   ├── smart_energy_prediction.ipynb   # ML model training and evaluation
│   ├── model.pkl                       # Trained Random Forest model
│   └── scaler.pkl                      # Feature scaler
├── data/
│   └── household_power_consumption.txt # UCI dataset
├── docs/
│   └── report.md                       # Project report
├── images/
│   ├── streamlit_dashboard.png
│   ├── roc_curve.png
│   └── correlation_heatmap.png
├── tests/
├── env/                                # Virtual environment
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Prerequisites

- Python 3.8+
- Mosquitto MQTT Broker
- UCI Household Power Consumption Dataset
- Git (optional)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Akobabs/IoT-EnergyPredictor.git
cd IoT-EnergyPredictor
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

Activate:

- Windows: `env\Scripts\activate`
- Linux/macOS: `source env/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit paho-mqtt jupyter joblib
```

### 4. Install Mosquitto MQTT Broker

#### Windows:

- Download from [mosquitto.org](https://mosquitto.org/download/)
- Install with all components (broker + clients)
- Add to PATH: `C:\Program Files\mosquitto`

Verify:

```bash
mosquitto -h
```

Start Broker:

```bash
mosquitto
```

#### Linux:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

#### macOS:

```bash
brew install mosquitto
brew services start mosquitto
```

### 5. Download Dataset

Download the file from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption) and save as:

```
data/household_power_consumption.txt
```

---

## 🧪 Usage

### Start the MQTT Broker

```bash
mosquitto
```

(Ensure it runs on port 1883)

### Run Data Collection

```bash
cd IoT-EnergyPredictor
env\Scripts\activate  # or source env/bin/activate
python src/iot_data_collection.py
```

➡ Populates `energy_data.db` with simulated sensor data.

### Train the Model

```bash
jupyter notebook src/smart_energy_prediction.ipynb
```

Then:

- Preprocess the data
- Train Random Forest
- Save `model.pkl`, `scaler.pkl`
- Generate visuals in `images/`

### Simulate IoT Data

```bash
python src/simulate_data.py
```

➡ Publishes data to MQTT topics:
`sensors/energy`, `sensors/temperature`, `sensors/humidity`

### Launch the Dashboard

```bash
streamlit run src/dashboard.py
```

Open: [http://localhost:8501](http://localhost:8501)

Features:

- Live energy usage
- Anomaly alerts
- Weather widgets
- Load control buttons & sliders

---

## 📊 Results

### Anomaly Detection

- Precision: **0.8923**
- Recall: **0.8674**
- F1 Score: **0.8797**
- Accuracy: **0.9456**
- ROC AUC: **0.9234**

### Energy Savings

Up to **15% reduction** in simulated scenarios through adaptive load control.

### Visual Outputs

- **ROC Curve:** `images/roc_curve.png` (Fig. 4.4)
- **Heatmap:** `images/correlation_heatmap.png` (Fig. 4.1)
- **Dashboard:** `images/streamlit_dashboard.png` (Fig. 4.3)

---

## 🛠️ Troubleshooting

### MQTT Not Connecting?

- Ensure Mosquitto is running:

  ```bash
  netstat -an | findstr 1883  # Windows
  sudo netstat -tuln | grep 1883  # Linux/macOS
  ```

- Allow port:

  ```bash
  netsh advfirewall firewall add rule name="MQTT" dir=in action=allow protocol=TCP localport=1883
  sudo ufw allow 1883
  ```

- Test subscription:

  ```bash
  mosquitto_sub -h localhost -t "sensors/#"
  ```

### Dashboard Shows No Data?

- Run `iot_data_collection.py` **before** `simulate_data.py`
- Inspect database:

  ```bash
  sqlite3 energy_data.db "SELECT * FROM sensor_data LIMIT 10"
  ```

### Model Errors?

- Ensure `model.pkl` and `scaler.pkl` exist
- Run all cells in `smart_energy_prediction.ipynb`

### Streamlit Warnings?

Ignore benign `ScriptRunContext` warnings—Streamlit handles them gracefully via a message queue.

---

## 🌐 Future Enhancements

- Integrate OpenWeatherMap API for real-time climate data
- Deploy to AWS IoT Core or Google Cloud IoT
- Use LSTM for sequential modeling of consumption trends
- Build a mobile app for remote monitoring and control

---

## 📚 Documentation

- Full report: `docs/report.md`
- Code Listings: Appendix A (scripts & notebooks)
- Dataset Info: Appendix C (Household Power Dataset, simulated climate data)

---

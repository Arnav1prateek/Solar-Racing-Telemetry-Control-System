# Solar Racing Telemetry & Control System

It is a custom hardware-software integration stack designed for real-time monitoring and safety of solar-powered vehicles. This project was developed as part of the **Etros Solareon Racing (SRMIST)** technical club.

## Key Features
- [cite_start]**Real-Time Geospatial Mapping**: Parses NMEA GPGGA sentences from a GPS module and renders a live location map using Folium[cite: 4, 13].
- [cite_start]**Sensor Telemetry Dashboard**: A RESTful Flask API collects data (Gas, Distance, Temp) and visualizes it via a Streamlit dashboard[cite: 63, 67].
- [cite_start]**Hardware Abstraction Layer**: Physical control modules managed via RPi.GPIO, allowing for manual toggling of system features with a buzzer feedback system[cite: 2, 21].
- **Parking Assist**: Ultrasonic-based rear parking detection with progressive auditory alerts.

## Tech Stack
- **Languages**: Python 3.x
- **Frameworks**: Flask (API), Streamlit (UI)
- **Libraries**: Folium (Mapping), Pandas (Data), RPi.GPIO (Hardware)
- **Hardware**: Raspberry Pi, GPS Module, MQ2 Sensor, Ultrasonic Sensors.

## Setup & Installation

Follow these steps to deploy the system on your Raspberry Pi:

1. **Clone the Repository** ```bash
   git clone [https://github.com/your-username/Solaris-Telemetry-System.git](https://github.com/your-username/Solaris-Telemetry-System.git)
   cd Solaris-Telemetry-System

Install Dependencies Ensure you have a virtual environment active, then install the required Python packages:

Bash
pip install -r requirements.txt
Configuration Open main.py and update the BASE_DIR variable to match your local Raspberry Pi directory. The default path is set to /home/asus/.


Run the System Execute the orchestrator script to start the GPS listener, map generator, and button listener:

Bash
python3 main.py

### GPIO Pin Mapping

The project utilizes the **BCM (Broadcom)** numbering system. Ensure your sensors and buttons are connected to the following pins:

| Component | GPIO Pin (BCM) | Physical Pin | Mode | Description |
| :--- | :---: | :---: | :---: | :--- |
| **Buzzer** | 24 | Pin 18 | Output | [cite_start]System alerts & button feedback [cite: 2, 33] |
| **Rear Park Button** | 17 | Pin 11 | Input (Pull-up) | [cite_start]Toggles Rear Parking Assist script [cite: 2, 33] |
| **Front Park Button** | 27 | Pin 13 | Input (Pull-up) | [cite_start]Toggles Server and Dashboard UI [cite: 2, 33] |
| **Object Detect Button**| 22 | Pin 15 | Input (Pull-up) | [cite_start]Toggles Object Detection script [cite: 2, 33] |
| **Ultrasonic TRIG** | 23 | Pin 16 | Output | Trigger for Parking Assist distance |
| **Ultrasonic ECHO** | 24* | Pin 18* | Input | Echo for Parking Assist distance |

> **?? [cite_start]Note on Hardware Conflict:** In the current configuration, both the **Buzzer** and the **Ultrasonic ECHO** are assigned to GPIO 24[cite: 2, 33]. For stable operation, it is recommended to move one to a different pin (e.g., GPIO 25) and update the code accordingly.

## Project Structure
```text
.
├── main.py                 # Core orchestrator and thread manager
├── car_map.html            # Auto-generated live map file
├── system/
│   ├── rear_parking.py     # Independent parking assist logic
│   ├── server/
│   │   └── server.py       # Flask backend for sensor data
│   └── ui/
│       └── ui.py           # Streamlit frontend dashboard
└── requirements.txt        # Project dependencies

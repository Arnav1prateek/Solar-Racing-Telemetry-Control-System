import threading 
import time
import folium
import subprocess
import socket
import queue
import RPi.GPIO as GPIO
import os

# --- PATH CONFIGURATION ---
# UPDATE THESE PATHS: If you move your project, update 'BASE_DIR'
BASE_DIR = "/home/asus" 
MAP_PATH = os.path.join(BASE_DIR, "car_map.html")
SYSTEM_DIR = os.path.join(BASE_DIR, "system")

# GPIO Setup
GPIO.setmode(GPIO.BCM)
BUTTON_REAR_PARK = 17
BUTTON_FRONT_PARK = 27  # UI + Server
BUTTON_OBJECT_DETECTION = 22
BUZZER = 24  

GPIO.setup(BUTTON_REAR_PARK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_FRONT_PARK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_OBJECT_DETECTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)

# Global variables for subprocesses
rear_process = None
object_process = None
server_process = None
ui_process = None

gps_queue = queue.Queue()
UDP_PORT = 5005

def parse_nmea(nmea_sentence):
    """Parses NMEA GPGGA sentence for lat/lon[cite: 4]."""
    try:
        parts = nmea_sentence.split(',')
        if parts[0] != "$GPGGA" or len(parts) < 10:
            return None, None
        lat_raw, lat_dir = parts[2], parts[3]
        lon_raw, lon_dir = parts[4], parts[5] # [cite: 5]
        if not lat_raw or not lon_raw:
            return None, None
        lat = float(lat_raw[:2]) + float(lat_raw[2:]) / 60
        if lat_dir == 'S': lat = -lat
        lon = float(lon_raw[:3]) + float(lon_raw[3:]) / 60
        if lon_dir == 'W': lon = -lon
        return round(lat, 6), round(lon, 6) # [cite: 6]
    except Exception as e:
        print(f"NMEA Parsing Error: {e}")
        return None, None

def gps_listener():
    """Listens for GPS data via UDP[cite: 8]."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            nmea_sentence = data.decode().strip()
            if nmea_sentence.startswith("$GPGGA"):
                lat, lon = parse_nmea(nmea_sentence)
                if lat and lon:
                    gps_queue.put((lat, lon))
        except Exception as e:
            print(f"GPS Error: {e}")

def generate_map():
    """Generates real-time map with auto-refresh[cite: 13, 16]."""
    if not hasattr(generate_map, 'browser_opened'):
        # ABSOLUTE PATH: Uses Chromium to display the local HTML file
        subprocess.Popen(["chromium-browser", "--kiosk", "--start-fullscreen", MAP_PATH])
        generate_map.browser_opened = True

    lat, lon = 28.6139, 77.2090  
    while True:
        if not gps_queue.empty():
            lat, lon = gps_queue.get_nowait()
        car_map = folium.Map(location=[lat, lon], zoom_start=18)
        folium.Marker([lat, lon], icon=folium.Icon(color="red")).add_to(car_map)
        
        with open(MAP_PATH, "w") as f:
            f.write(f"<html><head><script>setTimeout(()=>{{window.location.reload();}}, 3000);</script></head>"
                    f"<body>{car_map.get_root().render()}</body></html>")
        time.sleep(3)

def beep_buzzer():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER, GPIO.LOW)

def button_listener():
    """Handles logic for physical button toggles[cite: 21, 23, 27]."""
    global rear_process, object_process, server_process, ui_process
    while True:
        # Rear Parking [cite: 23]
        if GPIO.input(BUTTON_REAR_PARK) == GPIO.LOW:
            beep_buzzer()
            if rear_process:
                rear_process.terminate()
                rear_process = None
            else:
                # ABSOLUTE PATH: Ensure the path to rear_parking.py is correct
                path = os.path.join(SYSTEM_DIR, "rear_parking.py")
                rear_process = subprocess.Popen(["python3", path])
            time.sleep(0.5)

        # UI + Server [cite: 27]
        if GPIO.input(BUTTON_FRONT_PARK) == GPIO.LOW:
            beep_buzzer()
            if server_process:
                server_process.terminate()
                ui_process.terminate()
                server_process = ui_process = None
            else:
                # ABSOLUTE PATHS: Adjust paths for server.py and ui.py
                server_path = os.path.join(SYSTEM_DIR, "server", "server.py")
                ui_path = os.path.join(SYSTEM_DIR, "ui", "ui.py")
                server_process = subprocess.Popen(["python3", server_path])
                ui_process = subprocess.Popen(f"source {BASE_DIR}/venv/bin/activate && streamlit run {ui_path}", 
                                            shell=True, executable="/bin/bash")
            time.sleep(0.5)
        time.sleep(0.1)

# Start Threads [cite: 31]
threading.Thread(target=gps_listener, daemon=True).start()
threading.Thread(target=generate_map, daemon=True).start()
button_listener()

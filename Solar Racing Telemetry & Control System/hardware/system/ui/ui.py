import streamlit as st
import requests
import pandas as pd
import time

# CONFIGURATION: Change 'localhost' to your Pi's IP if viewing from another PC
SERVER_URL = "http://localhost:5000/data"

st.set_page_config(page_title="Etros Solareon Dashboard", layout="wide")
st.title("?? Etros Solareon Live Telemetry")

placeholder = st.empty()

while True:
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            data = response.json()[-50:] # Get latest 50 points [cite: 69]
            df = pd.DataFrame(data)
            
            with placeholder.container():
                # Display Metrics [cite: 70]
                m1, m2, m3 = st.columns(3)
                if not df.empty:
                    latest = df.iloc[-1]
                    m1.metric("Gas Level (MQ2)", f"{latest['MQ2']}")
                    m2.metric("Distance", f"{latest['Distance']} cm")
                    m3.metric("Temperature", f"{latest['TempC']} °C")
                    
                    # Graphing [cite: 71]
                    st.line_chart(df.set_index("timestamp")[["MQ2", "TempC"]])
        else:
            st.warning("Waiting for data...")
    except Exception as e:
        st.error(f"Connection Error: {e}")
    
    time.sleep(2)

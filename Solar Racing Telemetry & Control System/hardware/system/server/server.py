from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
sensor_data = []

@app.route('/data', methods=['POST'])
def receive_data():
    """Receives data from hardware sensors[cite: 65, 66]."""
    data = request.get_json()
    if not data: return jsonify({'status': 'no data'}), 400
    
    entry = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'MQ2': int(data.get('MQ2', 0)),
        'Distance': int(data.get('Distance', 0)),
        'TempC': float(data.get('TempC', 0.0))
    }
    sensor_data.append(entry)
    return jsonify({'status': 'success'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    # Runs on all interfaces (0.0.0.0) so the UI can connect via IP
    app.run(host='0.0.0.0', port=5000)

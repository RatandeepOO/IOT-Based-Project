from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ESP32 IP address
ESP32_URL = "http://192.168.137.121"

@app.route('/')
def home():
    is_secure = request.is_secure
    protocol = "HTTPS" if is_secure else "HTTP"
    return jsonify({
        "message": f"Connection using {protocol}",
        "secure": is_secure
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Returns a "No Content" response



# Endpoint to control devices via ESP32
@app.route('/control-device', methods=['POST'])
def control_device():
    data = request.json
    command = data.get("command")

    try:
        # Forward command to ESP32
        esp_response = requests.post(f"{ESP32_URL}{command}")
        return jsonify(esp_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})

# Endpoint to fetch weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        response = requests.get("https://wttr.in/kashipur?format=j1")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Endpoint to fetch news data
@app.route('/news', methods=['GET'])
def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=028c9fc91fd04dd99d86ba3db42db83d"
        response = requests.get(url)
        data = response.json()
        headlines = [article['title'] for article in data['articles'][:5]]
        return jsonify({"news": headlines})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # HTTP only

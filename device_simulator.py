import random
import time
import requests

API_URL = "http://127.0.0.1:8000/upload"

devices = ["tower-001", "tower-002", "weather-001", "base-station-001"]

while True:
    device_id = random.choice(devices)

    data = {
        "device_id": device_id,
        "temperature": round(random.uniform(20, 85), 1),
        "humidity": round(random.uniform(30, 95), 1),
        "voltage": round(random.uniform(2.5, 4.2), 2),
        "location": "lab"
    }

    try:
        response = requests.post(API_URL, json=data)
        print("Uploaded:", data)
        print("Response:", response.json())
    except Exception as error:
        print("Upload failed:", error)

    time.sleep(3)
    
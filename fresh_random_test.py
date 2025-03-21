import requests
import pandas as pd
import numpy as np
import random
import time

# Load test data
X_test = pd.read_csv("X_test_scaled.csv").values
y_test = pd.read_csv("y_test.csv").values.ravel()

# API URL
url = "http://127.0.0.1:5000/predict"

# Function to send a request to the API
def send_test_request():
    index = random.randint(0, len(X_test) - 1)  # Select a random test sample
    features = X_test[index].tolist()  # Convert to list for JSON compatibility
    payload = {"features": [features]}  # Corrected the key to "features"

    try:
        response = requests.post(url, json=payload)
        print(f"➡️  Sent Data: {payload}")

        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Prediction: {result}\n")
            except requests.exceptions.JSONDecodeError:
                print(f"❌ Response not in JSON format: {response.text}")
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
    
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

# Test the API multiple times
for _ in range(10):  # Adjust the number of tests as needed
    send_test_request()
    time.sleep(5)  # Simulate a small delay between requests

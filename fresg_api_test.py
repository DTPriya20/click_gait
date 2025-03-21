import pandas as pd
import requests
import random
import json

# Load test dataset
X_test = pd.read_csv("X_test_scaled.csv")

# Randomly select a row
random_index = random.randint(0, len(X_test) - 1)
sample_features = X_test.iloc[random_index].tolist()

# Define API URL
api_url = "http://127.0.0.1:5000/predict"

# Prepare JSON request payload
payload = {"features": sample_features}

# Send POST request
try:
    response = requests.post(api_url, json=payload)
    response_data = response.json()
    
    # Print the prediction result
    print(f"✅ Sent features from row {random_index}")
    print("🔍 Prediction:", response_data.get("prediction"))
    print("📊 Probabilities:", response_data.get("probabilities"))
except Exception as e:
    print(f"❌ Error calling API: {str(e)}")

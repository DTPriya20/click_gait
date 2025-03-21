import pandas as pd
import numpy as np
import joblib
import logging
import time
import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Preprocessed Data
try:
    logging.info("📥 Loading preprocessed datasets...")
    X_train = pd.read_csv("X_train_scaled.csv").values
    y_train = pd.read_csv("y_train.csv").values.ravel()
    X_test = pd.read_csv("X_test_scaled.csv").values
    y_test = pd.read_csv("y_test.csv").values.ravel()
    logging.info("✅ Data loaded successfully")
except Exception as e:
    logging.error(f"❌ Error loading data: {str(e)}")
    raise

# Define movement labels
movement_labels = {
    1: "Walking",
    2: "Jogging",
    3: "Running",
    4: "Sitting",
    5: "Standing",
    6: "Stair Climbing"
}

# Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking
CORS(app)

# Load Model
try:
    model = joblib.load("gait_model.pkl")
    logging.info("✅ Model loaded successfully")
except Exception as e:
    logging.error(f"❌ Error loading model: {str(e)}")
    raise

def init_session():
    """Ensures session variables are initialized for each request."""
    if "unknown_movements" not in session:
        session["unknown_movements"] = []
    if "movement_durations" not in session:
        session["movement_durations"] = defaultdict(int)
    if "last_movement_time" not in session:
        session["last_movement_time"] = time.time()
    if "last_movement_type" not in session:
        session["last_movement_type"] = None  # To track changes in movement

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Gait Analysis API! Use /predict for predictions."})

@app.route("/predict", methods=["POST"])
def predict():
    """API Endpoint for gait predictions."""
    init_session()  # ✅ Initialize session inside request
    try:
        data = request.get_json()
        if "features" not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400

        input_features = np.array(data["features"]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_features)[0]
        probabilities = model.predict_proba(input_features)[0]
        max_prob = np.max(probabilities)

        # Convert numerical prediction to movement type
        movement_type = movement_labels.get(int(prediction), "Unknown Movement")

        # Track movement duration only if it remains the same for at least 40 seconds
        current_time = time.time()
        elapsed_time = current_time - session["last_movement_time"]

        if session["last_movement_type"] == movement_type:
            session["movement_durations"][movement_type] += elapsed_time
        elif elapsed_time >= 40:  # ✅ Enforce the 40-second rule
            session["movement_durations"][movement_type] += elapsed_time

        session["last_movement_time"] = current_time
        session["last_movement_type"] = movement_type  # Update movement type

        # Handle unknown movements
        warning_message = None
        if max_prob < 0.6:  # Confidence threshold (adjustable)
            movement_type = "Unknown Movement"
            session["unknown_movements"].append(datetime.datetime.now())

        # Clean up old unknown movement timestamps (keep only last 10 minutes)
        ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
        session["unknown_movements"] = [t for t in session["unknown_movements"] if t > ten_minutes_ago]

        # If more than 5 unknown movements in last 10 minutes, send a warning
        if len(session["unknown_movements"]) > 5:
            warning_message = "⚠️ We noticed some irregular movements. Are you okay?"

        return jsonify({
            "prediction": int(prediction),
            "movement_type": movement_type,
            "probabilities": probabilities.tolist(),
            "unknown_movement_count": len(session["unknown_movements"]),
            "warning": warning_message
        })
    except Exception as e:
        logging.error(f"❌ Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/session_summary", methods=["GET"])
def session_summary():
    """Provides a summary of the user's movement session."""
    init_session()  # ✅ Initialize session inside request
    summary = {
        "total_walking_time": session["movement_durations"].get("Walking", 0),
        "total_running_time": session["movement_durations"].get("Running", 0),
        "total_irregular_movements": len(session["unknown_movements"]),
    }
    return jsonify(summary)

@app.route("/reset_session", methods=["GET"])
def reset_session():
    """Resets session data including movement durations and unknown movement count."""
    init_session()  # ✅ Initialize session inside request
    session["unknown_movements"] = []
    session["movement_durations"] = defaultdict(int)
    session["last_movement_time"] = time.time()
    session["last_movement_type"] = None
    return jsonify({"message": "Session data reset successfully!"})

if __name__ == "__main__":
    logging.info("🌐 Starting Flask API... Access it via http://127.0.0.1:5000")
    app.run(debug=True)

import joblib
import pandas as pd

# Load the saved model
model = joblib.load("gait_model.pkl")

# Load test data
X_test = pd.read_csv("X_test_scaled.csv")
y_test = pd.read_csv("y_test.csv").values.ravel()

# Debugging: Check data integrity
print("✅ Data Loaded Successfully")
print("First few rows of X_test:\n", X_test.head())  
print("Shape of X_test:", X_test.shape)  
print("Shape of y_test:", y_test.shape)

# Run inference
y_pred = model.predict(X_test)

# Debugging: Check predictions
print("Unique predictions:", set(y_pred))  
print("Sample Predictions:", y_pred[:10])
print("Actual Labels:     ", y_test[:10])

# Check confidence scores
y_proba = model.predict_proba(X_test)
print("Sample Prediction Probabilities:\n", y_proba[:10])

# Debugging: Count occurrences of each predicted class
print("Prediction Counts:\n", pd.Series(y_pred).value_counts())


import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("gait_model.pkl")

# Streamlit App Title
st.title("Gait Analysis Classifier")
st.write("Upload a CSV file containing gait data to classify activities.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    data = pd.read_csv(uploaded_file)
    
    # Ensure it matches training data format
    if data.shape[1] != model.n_features_in_:
        st.error(f"Incorrect input shape! Expected {model.n_features_in_} features, got {data.shape[1]}.")
    else:
        # Predict
        predictions = model.predict(data)
        print("Raw Predictions:", predictions)  # Debugging step
        
        # Show predictions
        st.write("### Predictions:")
        st.dataframe(pd.DataFrame({"Predicted Class": predictions}))
        
        st.success("✅ Predictions generated successfully!")

# Run the app with: streamlit run fresh_app.py

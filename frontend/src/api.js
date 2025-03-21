import axios from 'axios';

// Set the base URL for your Flask backend
const BASE_URL = 'http://127.0.0.1:5000';

// Function to send data to Flask for prediction
export const getPrediction = async (features) => {
  try {
    const response = await axios.post(`${BASE_URL}/predict`, { features });
    return response.data; // This will return the response from Flask
  } catch (error) {
    console.error('Error getting prediction:', error);
    throw error;
  }
};

// Function to get session summary from Flask
export const getSessionSummary = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/session_summary`);
    return response.data; // This will return session summary
  } catch (error) {
    console.error('Error getting session summary:', error);
    throw error;
  }
};

// Function to reset session data in Flask
export const resetSession = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/reset_session`);
    return response.data; // This will return success message after reset
  } catch (error) {
    console.error('Error resetting session:', error);
    throw error;
  }
};

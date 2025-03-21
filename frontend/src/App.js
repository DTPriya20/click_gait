import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [sensorData, setSensorData] = useState([]);
  const [prediction, setPrediction] = useState("");
  const [movementType, setMovementType] = useState("");
  const [probabilities, setProbabilities] = useState([]);
  const [warning, setWarning] = useState("");
  const [sessionSummary, setSessionSummary] = useState({});
  const [sessionRunning, setSessionRunning] = useState(false);

  // To keep track of the session ID
  const sessionId = "your-session-id"; // If you want to use some session tracking

  const fetchSessionSummary = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/session_summary");
      setSessionSummary(response.data);
    } catch (error) {
      console.error("Error fetching session summary", error);
    }
  };

  const handlePredict = async (features) => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", { features });
      const result = response.data;

      setPrediction(result.prediction);
      setMovementType(result.movement_type);
      setProbabilities(result.probabilities);
      setWarning(result.warning);
    } catch (error) {
      console.error("Error making prediction", error);
    }
  };

  const handleResetSession = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/reset_session");
      setSessionRunning(false);
      setWarning("");
      setMovementType("");
      setPrediction("");
      setProbabilities([]);
      setSessionSummary({});
    } catch (error) {
      console.error("Error resetting session", error);
    }
  };

  // DeviceMotion API Integration
  useEffect(() => {
    if (sessionRunning) {
      const handleMotion = (event) => {
        const { accelerationIncludingGravity } = event;
        const features = [
          accelerationIncludingGravity.x,
          accelerationIncludingGravity.y,
          accelerationIncludingGravity.z,
        ];

        handlePredict(features);
      };

      window.addEventListener("devicemotion", handleMotion);

      return () => {
        window.removeEventListener("devicemotion", handleMotion);
      };
    }
  }, [sessionRunning]);

  // Session start/stop handling
  const handleStartSession = () => {
    setSessionRunning(true);
    fetchSessionSummary();
  };

  const handleEndSession = () => {
    setSessionRunning(false);
    fetchSessionSummary();
  };

  // Use effect to continuously fetch the session summary
  useEffect(() => {
    if (sessionRunning) {
      const interval = setInterval(() => {
        fetchSessionSummary();
      }, 5000); // Fetch every 5 seconds

      return () => clearInterval(interval);
    }
  }, [sessionRunning]);

  return (
    <div className="App">
      <h1>Gait Analysis</h1>

      {!sessionRunning ? (
        <button onClick={handleStartSession}>Start Session</button>
      ) : (
        <div>
          <button onClick={handleEndSession}>End Session</button>
          <button onClick={handleResetSession}>Reset Session</button>
        </div>
      )}

      <div>
        {warning && <p className="warning">{warning}</p>}
        <p><strong>Prediction:</strong> {movementType}</p>
        <p><strong>Confidence:</strong> {probabilities.length > 0 ? `${(Math.max(...probabilities) * 100).toFixed(2)}%` : "N/A"}</p>
      </div>

      <div>
        <h3>Session Summary</h3>
        <p><strong>Walking Time:</strong> {sessionSummary.total_walking_time || 0} seconds</p>
        <p><strong>Running Time:</strong> {sessionSummary.total_running_time || 0} seconds</p>
        <p><strong>Irregular Movements:</strong> {sessionSummary.total_irregular_movements || 0}</p>
        <p><strong>Session Duration:</strong> {sessionSummary.session_duration || 0} seconds</p>
      </div>
    </div>
  );
};

export default App;

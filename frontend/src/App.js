import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = "https://my-click-gait.onrender.com";

const App = () => {
  const [prediction, setPrediction] = useState("");
  const [movementType, setMovementType] = useState("");
  const [probabilities, setProbabilities] = useState([]);
  const [warning, setWarning] = useState("");
  const [sessionSummary, setSessionSummary] = useState({});
  const [unknownMovementCount, setUnknownMovementCount] = useState(0);
  const [persistentWarning, setPersistentWarning] = useState(false);
  const [walkingSessions, setWalkingSessions] = useState(0);
  const [runningSessions, setRunningSessions] = useState(0);
  const [currentWalkTime, setCurrentWalkTime] = useState(0);
  const [currentRunTime, setCurrentRunTime] = useState(0);
  const [isWalking, setIsWalking] = useState(false);
  const [isRunning, setIsRunning] = useState(false);

  // Fetch session summary on page load & every 5 seconds
  const fetchSessionSummary = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/session_summary`);
      const data = response.data;

      setSessionSummary(data);

      setWalkingSessions(data.total_walking_sessions || 0);
      setRunningSessions(data.total_running_sessions || 0);
    } catch (error) {
      console.error("❌ Error fetching session summary:", error);
    }
  };

  // Predict movement based on sensor data
  const handlePredict = async (features) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/predict`, { features });
      const result = response.data;

      setPrediction(result.prediction);
      setMovementType(result.movement_type);
      setProbabilities(result.probabilities);
      setWarning(result.warning);

      // Track unknown movements
      if (result.movement_type.toLowerCase() === "unknown") {
        setUnknownMovementCount((prev) => prev + 1);
      } else {
        setUnknownMovementCount(0);
      }

      // Track running & walking session duration
      if (result.movement_type.toLowerCase() === "running") {
        if (!isRunning) {
          setIsRunning(true);
          setCurrentRunTime(0);
        }
      } else {
        if (isRunning) {
          if (currentRunTime >= 120) {
            setRunningSessions((prev) => prev + 1);
          }
          setIsRunning(false);
        }
      }

      if (result.movement_type.toLowerCase() === "walking") {
        if (!isWalking) {
          setIsWalking(true);
          setCurrentWalkTime(0);
        }
      } else {
        if (isWalking) {
          if (currentWalkTime >= 60) {
            setWalkingSessions((prev) => prev + 1);
          }
          setIsWalking(false);
        }
      }

      // Trigger persistent warning after 40s of unknown movement
      if (unknownMovementCount >= 8) {
        setPersistentWarning(true);
      } else {
        setPersistentWarning(false);
      }
    } catch (error) {
      console.error("❌ Error making prediction:", error);
    }
  };

  // Reset everything (Session + UI)
  const handleResetEverything = async () => {
    try {
      await axios.post(`${BACKEND_URL}/reset_session`);
      setWarning("");
      setMovementType("");
      setPrediction("");
      setProbabilities([]);
      setSessionSummary({});
      setUnknownMovementCount(0);
      setPersistentWarning(false);
      setWalkingSessions(0);
      setRunningSessions(0);
      setCurrentWalkTime(0);
      setCurrentRunTime(0);
      setIsWalking(false);
      setIsRunning(false);
      fetchSessionSummary();
    } catch (error) {
      console.error("❌ Error resetting session:", error);
    }
  };

  // 🔥 DeviceMotion API (Always Active)
  useEffect(() => {
    const handleMotion = (event) => {
      const { accelerationIncludingGravity } = event;
      const features = [
        accelerationIncludingGravity.x || 0,
        accelerationIncludingGravity.y || 0,
        accelerationIncludingGravity.z || 0,
      ];
      handlePredict(features);
    };

    window.addEventListener("devicemotion", handleMotion);
    return () => {
      window.removeEventListener("devicemotion", handleMotion);
    };
  }, []);

  // 🕒 Fetch session summary every 5 seconds
  useEffect(() => {
    fetchSessionSummary();
    const interval = setInterval(fetchSessionSummary, 5000);
    return () => clearInterval(interval);
  }, []);

  // ⏳ Track Running & Walking Time
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setCurrentRunTime((prev) => prev + 1);
      }, 1000);
    } else if (isWalking) {
      interval = setInterval(() => {
        setCurrentWalkTime((prev) => prev + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isRunning, isWalking]);

  return (
    <div className="App">
      <h1>Gait Analysis</h1>

      <button onClick={handleResetEverything}>Reset Everything</button>

      <div>
        {persistentWarning && <p className="warning">⚠️ I'm sensing some unknown persistent movement. Are you okay?</p>}
        {warning && <p className="warning">⚠️ {warning}</p>}
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

      <div>
        <h3>Session Count</h3>
        <p><strong>Walking Sessions:</strong> {walkingSessions}</p>
        {walkingSessions >= 5 && walkingSessions < 10 && <p className="achievement">🎉 Great job! You've completed 5+ walking sessions!</p>}
        {walkingSessions >= 10 && <p className="achievement">🎉 Well done! You've completed more than 10 walking sessions!</p>}

        <p><strong>Running Sessions:</strong> {runningSessions}</p>
        {runningSessions >= 4 && <p className="achievement">🔥 Amazing! More than 4 running sessions completed!</p>}
      </div>
    </div>
  );
};

export default App;

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load Preprocessed Data
X_train = pd.read_csv("X_train_scaled.csv").values
y_train = pd.read_csv("y_train.csv").values.ravel()
X_test = pd.read_csv("X_test_scaled.csv").values
y_test = pd.read_csv("y_test.csv").values.ravel()

# Train Random Forest with optimized hyperparameters
model = RandomForestClassifier(
    n_estimators=75, 
    max_depth=10, 
    min_samples_split=5, 
    min_samples_leaf=2, 
    max_features="sqrt", 
    class_weight="balanced", 
    random_state=42
)
model.fit(X_train, y_train)

# Save Model efficiently
joblib.dump(model, 'gait_model.pkl', compress=3)

# Predictions
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'\n✅ Model Accuracy: {accuracy:.4f}')

# Classification Report
report = classification_report(y_test, y_pred)
print('\n📌 Classification Report:\n', report)

# Confusion Matrix with better visualization
cm = confusion_matrix(y_test, y_pred)
labels = np.unique(y_test)
plt.figure(figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# ✅ Corrected paths
base_path = r"C:\Users\Ditip\Documents\project1\UCI HAR Dataset\UCI HAR Dataset"
X_train_path = os.path.join(base_path, "train", "X_train.txt")
X_test_path = os.path.join(base_path, "test", "X_test.txt")
y_train_path = os.path.join(base_path, "train", "y_train.txt")
y_test_path = os.path.join(base_path, "test", "y_test.txt")

# ✅ Check if files exist before proceeding
for path in [X_train_path, X_test_path, y_train_path, y_test_path]:
    if not os.path.exists(path):
        print(f"❌ ERROR: File not found: {path}")
        exit(1)

# ✅ Load datasets
X_train = pd.read_csv(X_train_path, sep='\s+', header=None)
X_test = pd.read_csv(X_test_path, sep='\s+', header=None)
y_train = pd.read_csv(y_train_path, sep='\s+', header=None)
y_test = pd.read_csv(y_test_path, sep='\s+', header=None)

# ✅ Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ✅ Save processed data
pd.DataFrame(X_train_scaled).to_csv("X_train_scaled.csv", index=False)
pd.DataFrame(X_test_scaled).to_csv("X_test_scaled.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("✅ Data Loaded & Normalized (Mean ~0, Std ~1)")

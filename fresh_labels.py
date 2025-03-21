import pandas as pd
import numpy as np

# Define file paths
X_train_path = r"C:\Users\Ditip\Documents\project1\UCI HAR Dataset\UCI HAR Dataset\train\X_train.txt"
y_train_path = r"C:\Users\Ditip\Documents\project1\UCI HAR Dataset\UCI HAR Dataset\train\y_train.txt"
X_test_path = r"C:\Users\Ditip\Documents\project1\UCI HAR Dataset\UCI HAR Dataset\test\X_test.txt"
y_test_path = r"C:\Users\Ditip\Documents\project1\UCI HAR Dataset\UCI HAR Dataset\test\y_test.txt"

# Load data with whitespace delimiter (since it's space-separated)
X_train = pd.read_csv(X_train_path, delim_whitespace=True, header=None)
y_train = pd.read_csv(y_train_path, delim_whitespace=True, header=None)
X_test = pd.read_csv(X_test_path, delim_whitespace=True, header=None)
y_test = pd.read_csv(y_test_path, delim_whitespace=True, header=None)

# Print shape of datasets
print("✅ X_train shape:", X_train.shape)
print("✅ y_train shape:", y_train.shape)
print("✅ X_test shape:", X_test.shape)
print("✅ y_test shape:", y_test.shape)

# Show first few rows
print("\n🔹 X_train Sample:\n", X_train.head())
print("\n🔹 y_train Sample:\n", y_train.head())

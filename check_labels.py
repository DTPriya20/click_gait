import pandas as pd

df = pd.read_csv("features.csv")
print("Columns in CSV:", df.columns.tolist())

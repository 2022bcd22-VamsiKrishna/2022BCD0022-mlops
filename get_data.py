import pandas as pd
from sklearn.datasets import fetch_california_housing
import os

os.makedirs('data', exist_ok=True)

# Fetch the dataset
california = fetch_california_housing(as_frame=True)
df = california.frame

# VERSION 1: We only save the first 10,000 rows
df_v1 = df.head(10000)
df_v1.to_csv('data/housing.csv', index=False)

print(f"Version 1 saved with {len(df_v1)} rows.")
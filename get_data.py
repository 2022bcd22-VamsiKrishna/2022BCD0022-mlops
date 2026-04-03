import pandas as pd
from sklearn.datasets import fetch_california_housing
import os

os.makedirs('data', exist_ok=True)

# Fetch the dataset
california = fetch_california_housing(as_frame=True)
df = california.frame

# VERSION 2: We saved full data
df_v2 = df
df_v2.to_csv('data/housing.csv', index=False)

print(f"Version 2 saved with {len(df_v2)} rows.")
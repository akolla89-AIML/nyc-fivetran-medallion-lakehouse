#This is a test script to see if parquet file is not corrupt and python can read it

import pandas as pd

file_path = "data/hvfhv_2024-12.parquet"

df = pd.read_parquet(file_path)

print(df.head())
print(df.columns)
#This script will:
# 1.read parquet file
# 2.Extract year/month/day/hour from pickup_datetime
# 3.write hourly parquet files into staging/


import pandas as pd
import os

INPUT_FILE = "data/hvfhv_2024-12.parquet"
OUTPUT_DIR = "staging/incremental/hvfhv"

#load parquet
df = pd.read_parquet(INPUT_FILE)

#Ensure datetime format
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

#extract time components
df["year"] = df["pickup_datetime"].dt.year
df["month"] = df["pickup_datetime"].dt.month
df["day"] = df["pickup_datetime"].dt.day
df["hour"] = df["pickup_datetime"].dt.hour

#Group by hourly partitions 
grouped = df.groupby(["year", "month", "day", "hour"])

for (year, month, day, hour), group in grouped:
    path = f"{OUTPUT_DIR}/year={year}/month={month:02d}/day={day:02d}/hour={hour:02d}"
    os.makedirs(path, exist_ok= True)
    
    file_path = f"{path}/part-{hour:02d}.parquet"

    group.drop(columns = ["year", "month", "day", "hour"]).to_parquet(file_path, index=False)

    print(f"written: {file_path}")
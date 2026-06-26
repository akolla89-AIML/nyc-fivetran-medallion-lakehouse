#This script will:
# 1.read files from staging
# 2.upload 1 file at a time to ADLS
# 3.wait between uploads (simulate hourly sync)
# 4. Preserve folder structure in ADLS
# 5. Simulate real ingestion behavior



import os
import time
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

# ================
# Azure config
# ================

STORAGE_ACCOUNT = "azdbaimlstorage01"
CONTAINER = "lakehouse01" 
LOCAL_DIR = "staging/incremental/hvfhv"

SLEEP_SECONDS = 5 #simulate hourly delay

# =================
# Azure Client
# =================

credential = DefaultAzureCredential()

service_client = DataLakeServiceClient(
    account_url = f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
    credential = credential
)

file_system_client = service_client.get_file_system_client(CONTAINER)

# ================
# GET FILES
# ================
files = []

for root, dirs, filenames in os.walk(LOCAL_DIR):
    for file in filenames:
        if file.endswith(".parquet"):
           full_path = os.path.join(root, file)
           relative_path = full_path.replace(LOCAL_DIR + "/","")
           files.append((full_path, relative_path))

files.sort()

# ========================
# UPLOAD SIMULATION
# ========================

total = len(files)

for i, (local_path, relative_path) in enumerate(files, start=1):

    remote_path = f"landing/hvfhv/{relative_path}"

    print(f"[{i}/{total}] Uploading: {remote_path}")

    file_client = file_system_client.get_file_client(remote_path)

    with open(local_path, "rb") as data:
         file_client.upload_data(data, overwrite=True)

    print(f"[{i}/{total}] Uploaded: {remote_path}")

    if i < total:
         time.sleep(SLEEP_SECONDS)

print("Fivetran simulation is completed.")
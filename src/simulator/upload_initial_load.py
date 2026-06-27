#This script will:
# 1.read files from staging
# 2.upload 1 file for Nov month  to ADLS
# 3. Preserve folder structure in ADLS
# 4. Simulate initial load (historical backfill)




from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

# ================
# Azure config
# ================

STORAGE_ACCOUNT = "azdbaimlstorage01"
CONTAINER = "lakehouse01" 

LOCAL_FILE = Path("data/hvfhv_2024-11.parquet")

REMOTE_DIRECTORY = "landing/hvfhv/initial"




# =================
# Azure Client
# =================

credential = DefaultAzureCredential()

service_client = DataLakeServiceClient(
    account_url = f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
    credential = credential
)

filesystem_client = service_client.get_file_system_client(CONTAINER)



# ========================
# UPLOAD TO ADLS
# ========================

remote_file = f"{REMOTE_DIRECTORY}/{LOCAL_FILE.name}"

print(f"Uploading {LOCAL_FILE}....")
print(f"Destination: {remote_file}....")

file_client = filesystem_client.get_file_client(remote_file)

with open(LOCAL_FILE, "rb") as data:
     file_client.upload_data(data, overwrite=True)

print("Upload completed successfully.")
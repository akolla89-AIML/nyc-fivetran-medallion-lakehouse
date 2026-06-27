#This script will:
# 1.read files from staging
# 2.upload 1 file at a time to ADLS
# 3.wait between uploads (simulate hourly sync)
# 4. Preserve folder structure in ADLS
# 5. Simulate real ingestion behavior

import os
import sys
import time

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from src.common.settings import Settings
from src.common.logger import get_logger



# ==========================================
# Load Environment Configuration
# ==========================================

# Default to DEV if no environment is supplied
environment = sys.argv[1] if len(sys.argv) > 1 else "dev"

settings = Settings(env=environment)

logger = get_logger("fivetran_simulator")

# ================
# Azure config
# ================

STORAGE_ACCOUNT = settings.storage_account
CONTAINER = settings.container

LOCAL_DIR = settings.local_incremental_source

ADLS_INCREMENTAL_PATH = settings.adls_incremental_load

SLEEP_SECONDS = settings.sleep_seconds #simulate hourly delay

# =================
# Azure Authentication
# =================

credential = DefaultAzureCredential()

service_client = DataLakeServiceClient(
    account_url = f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
    credential = credential
)

file_system_client = service_client.get_file_system_client(CONTAINER)

# ================
# Discover Local Files
# ================
files = []

for root, _, filenames in os.walk(LOCAL_DIR):
    for file in filenames:
        if file.endswith(".parquet"):
           full_path = os.path.join(root, file)
           relative_path = os.path.relpath(full_path, LOCAL_DIR)
           files.append((full_path, relative_path))

files.sort()
print(f"Found {len(files)} parquet files.")
print(f"Environment : {environment}")
print(f"Uploading to : {ADLS_INCREMENTAL_PATH}")
print("-" * 60)

# ==========================================
# Simulate Fivetran Hourly Upload
# ==========================================

total = len(files)

for i, (local_path, relative_path) in enumerate(files, start=1):

    remote_path = f"{ADLS_INCREMENTAL_PATH}/{relative_path}"

    print(f"[{i}/{total}] Uploading: {remote_path}")

    file_client = file_system_client.get_file_client(remote_path)

    with open(local_path, "rb") as data:
        file_client.upload_data(data, overwrite=True)

    print(f"[{i}/{total}] Uploaded : {remote_path}")

    # Don't sleep after the last file
    if i < total:
        time.sleep(SLEEP_SECONDS)

print("-" * 60)
print(f"Fivetran simulation completed successfully. {total} files uploaded.")
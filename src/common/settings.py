import os
import yaml
from pathlib import Path

class Settings:
    def __init__(self, env="dev"):
        self.env = env

        # project root = nyc-fivetran-lab/
        BASE_DIR = Path(__file__).resolve().parents[2]

        config_path = BASE_DIR / "config" / f"{env}.yml"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Storage
        self.storage_account = config["storage"]["account"]
        self.container = config["storage"]["container"]

        # Local paths
        self.local_staging_root = config["local"]["staging_root"]
        self.local_initial_source = config["local"]["initial_source"]
        self.local_incremental_source = config["local"]["incremental_source"]

        # ADLS paths
        self.adls_landing_root = config["adls"]["landing_root"]
        self.adls_initial_load = config["adls"]["initial_load"]
        self.adls_incremental_load = config["adls"]["incremental_load"]

        # Simulation
        self.sleep_seconds = config["simulation"]["sleep_seconds"]
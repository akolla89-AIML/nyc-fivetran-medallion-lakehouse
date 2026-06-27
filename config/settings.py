import yaml
import os

class Settings:
    def __init__(self, env="dev"):
        config_path = os.path.join(
            os.path.dirname(__file__),
            f"{env}.yml"
        )

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self.storage_account = config["storage"]["account"]
        self.container = config["storage"]["container"]

        self.landing_path = config["paths"]["landing"]
        self.staging_path = config["paths"]["staging"]

        self.sleep_seconds = config["simulation"]["sleep_seconds"]
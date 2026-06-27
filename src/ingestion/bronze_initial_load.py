# This script will 
# 1. Read the initial load file from the landing zone -> nov 2024 data
# 2. Load into Bronze layer
# 3. Create first dataset snapshot
# 4. Initialize watermark state
from pathlib import Path
import pandas as pd
from src.common.logger import get_logger

logger = get_logger("bronze_initial")

class BronzeInitialLoader:

    def __init__(self, settings):
        self.settings = settings

        self.source_file = Path(
            "landing/hvfhv/initial/hvfhv_2024-11.parquet"
        )

        self.output_dir = Path("output/bronze")

    def run(self):

        logger.info(f"Starting initial load: {self.source_file}")

        if not self.source_file.exists():
            raise FileNotFoundError(f"Missing file: {self.source_file}")

        df = pd.read_parquet(self.source_file)

        logger.info(f"Rows loaded: {len(df)}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.output_dir / "bronze_initial.parquet"

        df.to_parquet(output_file, index=False)

        logger.info(f"Bronze initial load written to: {output_file}")
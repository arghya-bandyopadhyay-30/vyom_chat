import os
import yaml
from dotenv import load_dotenv

from src.ingestion.models.ingestion import Ingestion
from src.pipeline.model.config import Config


class ConfigService:
    def __init__(self, file_path: str):
        load_dotenv()
        self.path = file_path

    def __load_config(self) -> dict:
        with open(self.path, "r") as file:
            raw_config = file.read()

        processed_config = os.path.expandvars(raw_config)
        return yaml.safe_load(processed_config)

    def get_config(self) -> Config:
        config_data = self.__load_config()

        if "ingestion" not in config_data:
            raise ValueError("Ingestion configuration is required in config.yml")

        ingestion = Ingestion.from_dict(config_data["ingestion"])

        return Config(ingestion_config=ingestion)
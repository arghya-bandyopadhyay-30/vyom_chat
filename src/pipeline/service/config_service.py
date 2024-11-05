import os
import yaml
from dotenv import load_dotenv

from src.embedding.models.embedding import Embedding
from src.ingestion.models.ingestion import Ingestion
from src.llm.model.llm import LLMConfig
from src.pipeline.model.config import Config


class ConfigService:
    def __init__(self, file_path: str):
        load_dotenv()
        self.path = file_path

    def __load_config(self) -> dict:
        try:
            with open(self.path, "r") as file:
                raw_config = file.read()
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found at path: {self.path}")

        processed_config = os.path.expandvars(raw_config)
        return yaml.safe_load(processed_config)

    def get_config(self) -> Config:
        config_data = self.__load_config()

        if "ingestion" not in config_data:
            raise ValueError("Ingestion configuration is required in config.yml")

        if "embedding-model" not in config_data:
            raise ValueError("Embedding configuration is required in config.yml")

        if "llm-model" not in config_data:
            raise ValueError("LLM configuration is required in config.yml")

        ingestion = Ingestion.from_dict(config_data["ingestion"])
        embedding = Embedding.from_dict(config_data["embedding-model"])
        llm = LLMConfig.from_dict(config_data["llm-model"])

        return Config(ingestion_config=ingestion, embedding_config=embedding, llm_config=llm)
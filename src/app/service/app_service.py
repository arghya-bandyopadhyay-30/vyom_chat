import os

from dotenv import load_dotenv
import yaml

from src.app.models.app_config import AppConfig
from src.app.models.app_setup_config import AppSetupConfig
from src.llm.model.llm import LLMConfig


class AppService:
    def __init__(self, file_path: str):
        load_dotenv()
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.path = file_path

    def __load_config(self) -> dict:
        try:
            with open(self.path, "r") as file:
                raw_config = file.read()
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found at path: {self.path}")

        processed_config = os.path.expandvars(raw_config)
        return yaml.safe_load(processed_config)

    def get_config(self):
        config_data = self.__load_config()

        if "app" not in config_data:
            raise ValueError("Ingestion configuration is required in config.yml")

        if "llm-model" not in config_data:
            raise ValueError("LLM configuration is required in config.yml")

        app = AppSetupConfig.from_dict(config_data["app"])
        llm = LLMConfig.from_dict(config_data["llm-model"])

        return AppConfig(app_config=app, llm_config=llm)

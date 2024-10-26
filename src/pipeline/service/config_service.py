import os
import yaml
from dotenv import load_dotenv

from src.ingestion.models.ingestion import Ingestion
from src.pipeline.model.config import Config


class ConfigService:
    """
    Service class responsible for loading and parsing configuration data from a YAML file.
    """
    def __init__(self, file_path: str):
        """
        Initializes ConfigService with a file path for the configuration YAML file.

        Parameters:
        - file_path (str): The path to the configuration YAML file.
        """
        load_dotenv()
        self.path = file_path

    def __load_config(self) -> dict:
        """
        Loads and processes the YAML configuration file, expanding environment variables.

        Returns:
        - dict: The processed configuration data as a dictionary.

        Raises:
        - FileNotFoundError: If the specified file path does not exist.
        - yaml.YAMLError: If the YAML file is improperly formatted.
        """
        with open(self.path, "r") as file:
            raw_config = file.read()

        processed_config = os.path.expandvars(raw_config)
        return yaml.safe_load(processed_config)

    def get_config(self) -> Config:
        """
        Retrieves the parsed configuration as a Config object.

        Returns:
        - Config: A Config object containing ingestion configurations.

        Raises:
        - ValueError: If the 'ingestion' section is missing in the configuration data.
        """
        config_data = self.__load_config()

        if "ingestion" not in config_data:
            raise ValueError("Ingestion configuration is required in config.yml")

        ingestion = Ingestion.from_dict(config_data["ingestion"])

        return Config(ingestion_config=ingestion)
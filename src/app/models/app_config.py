from src.app.models.app_setup_config import AppSetupConfig
from src.llm.model.llm import LLMConfig


class AppConfig:
    def __init__(self, app_config: AppSetupConfig, llm_config: LLMConfig):
        self.app_config = app_config
        self.llm_config = llm_config
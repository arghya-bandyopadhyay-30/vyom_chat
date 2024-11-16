import asyncio

from src.app.models.app_config import AppConfig
from src.app.service.app_service import AppService
from src.app.webapp import WebApp

def run(file_path:str):
    config = AppService(file_path).get_config()

    web = WebApp(config.app_config, config.llm_config)
    web.run()

if __name__ == "__main__":
    app_config_path = "app.yml"
    run(app_config_path)
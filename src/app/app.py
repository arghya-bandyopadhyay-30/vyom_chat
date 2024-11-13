import asyncio

from src.app.models.app_config import AppConfig
from src.app.service.app_service import AppService
from src.app.webapp import WebApp


async def run_task(config: AppConfig):
    web = WebApp(config.app_config, config.llm_config)
    web.run()

async def run(file_path:str):
    config = AppService(file_path).get_config()
    await run_task(config)

if __name__ == "__main__":
    app_config_path = "app.yml"
    asyncio.run(run(app_config_path))
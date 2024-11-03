import argparse
import asyncio

from src.tools.loader import Loader
from src.pipeline.model.config import Config
from src.pipeline.service.config_service import ConfigService

async def run_task(config: Config):
    loader = Loader(config.ingestion_config)
    await loader.run()

async def run(file_path:str):
    config = ConfigService(file_path).get_config()
    await run_task(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Configuration Runner")
    parser.add_argument("config_path", type=str, help="Path to the pipeline config YAML file")
    args = parser.parse_args()

    asyncio.run(run(args.config_path))
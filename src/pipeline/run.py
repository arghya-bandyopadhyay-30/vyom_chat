import argparse
import asyncio

from src.ingestion.tools.loader import Loader
from src.llm.service.llm_service import LLMService
from src.pipeline.model.config import Config
from src.pipeline.service.config_service import ConfigService

async def run_task(config: Config):
    loader = Loader(config.ingestion_config, config.embedding_config)
    await loader.run()

    llm_service = LLMService(config.llm_config, config.embedding_config)
    await user_input(llm_service)

async def user_input(llm_service):
    print("Welcome to Vyom! You can ask any question about Arghya. Type 'bye' or 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["bye", "exit"]:
            print("Vyom: Goodbye! Feel free to return anytime.")
            break

        try:
            response = await llm_service.query(user_input)
            print(f"Vyom: {response}")
        except Exception as e:
            print(f"Error: {e}")


async def run(file_path:str):
    config = ConfigService(file_path).get_config()
    await run_task(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Configuration Runner")
    parser.add_argument("config_path", type=str, help="Path to the pipeline config YAML file")
    args = parser.parse_args()

    asyncio.run(run(args.config_path))
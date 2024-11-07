from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from src.embedding.models.embedding import Embedding
from src.embedding.service.embedding_service import EmbeddingService
from src.llm.model.llm import LLMConfig
from src.llm.utilities.prompt import get_agent_prompt


class LLMService:
    def __init__(self, llm_config: LLMConfig, embedding_config: Embedding):
        self.provider = llm_config.provider
        self.groq_api_key = llm_config.api_key
        self.model_name = llm_config.model

        self.embedding_service = EmbeddingService(embedding_config)

        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model_name=self.model_name)

    async def query(self, text: str):
        prompts = self.__generate_prompt(text)
        response = await self.llm.agenerate(messages=[prompts])
        return response.generations[0][0].text

    def __generate_prompt(self, text: str) -> list:
        return get_agent_prompt(text, self.embedding_service)
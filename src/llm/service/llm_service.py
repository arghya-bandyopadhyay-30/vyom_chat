from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from src.llm.model.llm import LLMConfig
from src.llm.model.prompt import get_agent_prompt


class LLMService:
    def __init__(self, llm_config: LLMConfig):
        self.provider = llm_config.provider
        self.groq_api_key = llm_config.api_key
        self.model_name = llm_config.model

        instruction_prompt = get_agent_prompt()
        self.system_message = SystemMessage(content=instruction_prompt["template"])

        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model_name=self.model_name)

    async def query(self, text: str):
        user_message = HumanMessage(content=text)

        messages = [self.system_message, user_message]

        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0].text
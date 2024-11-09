from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq

from src.llm.model.llm import LLMConfig
from src.llm.utilities.prompt_identifier import PromptIdentifier


class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        self.llm = self.__initialize_llm(llm_config)
        prompt = PromptIdentifier().get_prompt_template()
        self.chain = GraphCypherQAChain.from_llm(
            graph=graph_client,
            llm=self.llm,
            cypher_prompt=prompt,
            verbose=True,
            allow_dangerous_requests=True
        )

    def __initialize_llm(self, llm_config: LLMConfig) -> ChatGroq:
        return ChatGroq(groq_api_key=llm_config.api_key, model_name=llm_config.model)

    def query(self, question: str):
        return self.chain.invoke({"query": question})
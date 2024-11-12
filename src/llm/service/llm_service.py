from typing import Dict, Any

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_community.graphs import Neo4jGraph
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq

from src.llm.model.llm import LLMConfig
from src.llm.utilities.prompt_identifier import PromptIdentifier
from src.pipeline.tools.format_response_tool import FormatResponseTool
from src.pipeline.tools.query_neo4j_tool import QueryNeo4jTool


class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        self.llm = self.__initialize_llm(llm_config)
        self.query_tool = QueryNeo4jTool(graph_client)
        self.format_tool = FormatResponseTool()
        self.prompt_identifier = PromptIdentifier().get_prompt_template()

        tools = [
            StructuredTool.from_function(
                name="QueryNeo4j",
                description="Query the Neo4j database using the provided Cypher query.",
                func=self.query_tool.run,
                return_direct=True
            ),
            StructuredTool.from_function(
                name="FormatResponse",
                description="Format the context to present it to the user.",
                func=self.format_tool.run,
                return_direct=True
            ),
        ]

        prompt_with_variables = self.prompt_identifier.partial(
            tool_names=", ".join(tool.name for tool in tools),
            agent_scratchpad="",
            tools=", ".join(tool.name for tool in tools)
        )

        self.agent = create_structured_chat_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt_with_variables,
        )

        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

    def __initialize_llm(self, llm_config: LLMConfig) -> ChatGroq:
        return ChatGroq(groq_api_key=llm_config.api_key, model_name=llm_config.model)

    def query(self, question: str) -> dict[str, Any]:
        initial_thought = {
            "input": question,
            "question": question,
            "agent_scratchpad": "",
            "tool_names": "QueryNeo4j, FormatResponse",
            "tools": self.agent_executor.tools
        }
        return self.agent_executor.invoke(initial_thought)
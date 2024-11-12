from typing import Any

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_community.graphs import Neo4jGraph
from langchain.schema import HumanMessage
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq

from src.llm.model.llm import LLMConfig
from src.llm.utilities.prompt_identifier import PromptIdentifier
from src.llm.tools.query_neo4j_tool import QueryNeo4jTool


class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        self.llm = self.__initialize_llm(llm_config)
        self.query_tool = QueryNeo4jTool(graph_client)
        self.prompt_identifier = PromptIdentifier().get_prompt_template()

        tools = self.__initialize_tools()
        self.agent = self.__initialize_agent(tools)
        self.agent_executor = self.__initialize_agent_executor(tools)

    def __initialize_llm(self, llm_config: LLMConfig) -> ChatGroq:
        return ChatGroq(groq_api_key=llm_config.api_key, model_name=llm_config.model)

    def __initialize_tools(self) -> list[StructuredTool]:
        return [
            StructuredTool.from_function(
                name="QueryNeo4j",
                description="Query the Neo4j database using the provided Cypher query.",
                func=self.query_tool.run,
                return_direct=True
            ),
        ]

    def __initialize_agent(self, tools: list[StructuredTool]) -> Any:
        prompt_with_variables = self.prompt_identifier.partial(
            tool_names=", ".join(tool.name for tool in tools),
            agent_scratchpad="",
            tools=", ".join(tool.name for tool in tools)
        )
        return create_structured_chat_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt_with_variables,
        )

    def __initialize_agent_executor(self, tools: list[StructuredTool]) -> AgentExecutor:
        return AgentExecutor(agent=self.agent, tools=tools, verbose=True)


    def query(self, question: str) -> str | list[str | dict]:
        initial_input = {
            "input": question,
            "question": question,
            "agent_scratchpad": "",
            "tool_names": "QueryNeo4j",
            "tools": ", ".join(tool.name for tool in self.agent_executor.tools)
        }

        raw_response = self.agent_executor.invoke(initial_input)
        query_result = raw_response.get("output", {}).get("result", "No data found")

        formatted_response = self.__format_response(query_result)
        return formatted_response


    def __format_response(self, query_result: Any) -> str:
        formatting_prompt = f"""
                    You are a helpful assistant. Here is the raw data retrieved from the database: {query_result}
                    Please convert this into a well-structured, human-readable response (and do not provide any additional suggestions).
                """
        formatted_response = self.llm.invoke([HumanMessage(content=formatting_prompt)])
        return formatted_response.content
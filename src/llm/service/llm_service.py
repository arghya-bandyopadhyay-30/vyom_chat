from typing import Any

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_community.graphs import Neo4jGraph
from langchain.schema import HumanMessage
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq
from langchain.globals import set_verbose

from src.llm.model.llm import LLMConfig
from src.llm.tools.string_literals import VYOM_LABEL, ARGHYA_LABEL
from src.llm.utilities.prompt_identifier import PromptIdentifier
from src.llm.tools.query_neo4j_tool import QueryNeo4jTool


class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        set_verbose(True)
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
        return AgentExecutor(agent=self.agent, tools=tools)

    def __classify_query(self, question: str) -> str:
        classification_prompt = f"""
            You are an assistant designed to classify user queries. Please classify the following question as either:
            - '{VYOM_LABEL}' if the question is directed towards you, Vyom, or is a general greeting.
            - '{ARGHYA_LABEL}' if the question is directed towards Arghya Bandyopadhyay.

            Question: "{question}"

            Your classification should be either '{VYOM_LABEL}' or '{ARGHYA_LABEL}'.
        """
        response = self.llm.invoke([HumanMessage(content=classification_prompt)])
        return response.content.strip().lower()

    def query(self, question: str) -> str | list[str | dict]:
        query_type = self.__classify_query(question)

        if query_type == VYOM_LABEL:
            return self.__generate_bot_response(question)

        elif query_type == ARGHYA_LABEL:
            return self.__generate_user_response(question)

        return "I'm not sure how to respond to that. Could you clarify your question?"

    def __generate_user_response(self, question):
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

    def __generate_bot_response(self, question: str) -> str:
        introduction_prompt = f"""
        You are Vyom, a virtual assistant created to assist users and provide information about Arghya Bandyopadhyay.
        The user has asked: "{question}"

        Based on the question, introduce yourself in a friendly and professional manner. Describe your role, your purpose, and your connection to Arghya Bandyopadhyay.
        Be concise, helpful, and clear. Include:
        - Your name (Vyom)
        - Your purpose and connection to Arghya Bandyopadhyay
        - How you can assist with questions or information.

        Do not provide any unrelated information, and ensure your response is relevant to the user's question.
        """
        response = self.llm.invoke([HumanMessage(content=introduction_prompt)])
        return response.content.strip()

    def __format_response(self, query_result: Any) -> str:
        formatting_prompt = f"""
                    You are a helpful assistant. Here is the raw data retrieved from the database: {query_result}
                    Please convert this into a well-structured, human-readable response (and do not provide any additional suggestions).
                """
        formatted_response = self.llm.invoke([HumanMessage(content=formatting_prompt)])
        return formatted_response.content
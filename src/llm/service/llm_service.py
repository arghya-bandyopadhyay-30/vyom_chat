from typing import Any
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_community.graphs import Neo4jGraph
from langchain.schema import HumanMessage
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq
from langchain.globals import set_verbose

from src.llm.model.llm import LLMConfig
from src.llm.tools.string_literals import VYOM_LABEL, ARGHYA_LABEL, CATEGORY_IDENTIFIER_TEMPLATE, CLASSIFICATION_PROMPT, \
    BOT_INTRODUCTION_PROMPT, FORMATTING_PROMPT
from src.llm.utilities.prompt_identifier import PromptIdentifier
from src.llm.tools.query_neo4j_tool import QueryNeo4jTool

class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        try:
            set_verbose(True)
            self.llm = self.__initialize_llm(llm_config)
            self.query_tool = QueryNeo4jTool(graph_client)
            self.prompt_identifier = PromptIdentifier().get_prompt_template()

            tools = self.__initialize_tools()
            self.agent = self.__initialize_agent(tools)
            self.agent_executor = self.__initialize_agent_executor(tools, handle_parsing_errors=True)
        except Exception as e:
            raise ValueError(f"Error initializing LLMService: {e}")

    def __initialize_llm(self, llm_config: LLMConfig) -> ChatGroq:
        try:
            return ChatGroq(groq_api_key=llm_config.api_key, model_name=llm_config.model)
        except Exception as e:
            raise ValueError(f"Error initializing LLM: {e}")

    def __initialize_tools(self) -> list[StructuredTool]:
        try:
            return [
                StructuredTool.from_function(
                    name="QueryNeo4j",
                    description="Query the Neo4j database using the provided Cypher query.",
                    func=self.query_tool.run,
                    return_direct=True
                ),
            ]
        except Exception as e:
            raise ValueError(f"Error initializing tools: {e}")

    def __initialize_agent(self, tools: list[StructuredTool]) -> Any:
        try:
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
        except Exception as e:
            raise ValueError(f"Error initializing agent: {e}")

    def __initialize_agent_executor(self, tools: list[StructuredTool], handle_parsing_errors: bool = True) -> AgentExecutor:
        try:
            return AgentExecutor(agent=self.agent, tools=tools, handle_parsing_errors=handle_parsing_errors, verbose=True)
        except Exception as e:
            raise ValueError(f"Error initializing agent executor: {e}")

    def __classify_query(self, question: str) -> str:
        classification_prompt = CLASSIFICATION_PROMPT.format(question=question)
        response = self.llm.invoke([HumanMessage(content=classification_prompt)])
        return response.content.strip().lower()

    def _classify_query_category(self, query: str):
        prompt = CATEGORY_IDENTIFIER_TEMPLATE.format(query=query)

    def query(self, question: str) -> str:
        try:
            query_type = self.__classify_query(question)
            print("Classification Response:", query_type)

            if query_type == VYOM_LABEL:
                print("1")
                return self.__generate_bot_response(question)

            elif query_type == ARGHYA_LABEL:
                print("2")
                return self.__generate_user_response(question)

            return "I'm not sure how to respond to that. Could you clarify your question?"
        except Exception as e:
            raise ValueError(f"An error occurred while processing your request. Error processing query: {e}")

    def __generate_user_response(self, question):
        try:
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
        except Exception as e:
            raise ValueError(f"Error generating user response: {e}")

    def __generate_bot_response(self, question: str) -> str:
        try:
            introduction_prompt = BOT_INTRODUCTION_PROMPT.format(question=question)
            response = self.llm.invoke([HumanMessage(content=introduction_prompt)])
            return response.content.strip()
        except Exception as e:
            raise ValueError(f"Error generating bot response: {e}")

    def __format_response(self, query_result: Any) -> str:
        try:
            formatting_prompt = FORMATTING_PROMPT.format(query_result=query_result)
            formatted_response = self.llm.invoke([HumanMessage(content=formatting_prompt)])
            return formatted_response.content.strip()
        except Exception as e:
            raise ValueError(f"Error formatting response: {e}")

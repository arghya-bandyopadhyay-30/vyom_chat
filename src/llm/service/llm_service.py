from typing import Any
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_community.graphs import Neo4jGraph
from langchain.schema import HumanMessage
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq
from langchain.globals import set_verbose

from src.llm.model.llm import LLMConfig
from src.utilities.string_literals import VYOM_LABEL, ARGHYA_LABEL, CATEGORY_IDENTIFIER_TEMPLATE, CLASSIFICATION_PROMPT, \
    BOT_INTRODUCTION_PROMPT, FORMATTING_PROMPT, PERSON, EDUCATION, EXPERIENCE, SKILLS, CERTIFICATION, LANGUAGE, \
    HONOUR_AND_AWARD_WITHOUT_UNDERSCORE, PROJECTS, RECOMMENDATIONS, BLOG
from src.llm.utilities.prompt_identifier import PromptIdentifier
from src.llm.tools.query_neo4j_tool import QueryNeo4jTool
from src.llm.utilities.query_examples import person, education, experience, skills, certificate, language, projects, \
    honours_and_awards, recommendation, blogs


class LLMService:
    def __init__(self, llm_config: LLMConfig, graph_client: Neo4jGraph):
        try:
            set_verbose(True)
            self.llm = self.__initialize_llm(llm_config)
            self.query_tool = QueryNeo4jTool(graph_client)

            self.tools = self.__initialize_tools()
            self.agent_executor = None
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

    def __initialize_agent(self, tools: list[StructuredTool], prompt_template: Any) -> Any:
        try:
            prompt_with_variables = prompt_template.partial(
                tool_names=", ".join(tool.name for tool in tools),
                agent_scratchpad="",
                tools=", ".join(tool.name for tool in tools)
            )
            print("Prompt sent to LLM:", prompt_with_variables.format(question=""))  # Debugging: Print prompt being used

            return create_structured_chat_agent(
                llm=self.llm,
                tools=tools,
                prompt=prompt_with_variables,
            )
        except Exception as e:
            raise ValueError(f"Error initializing agent: {e}")

    def __initialize_agent_executor(self, agent: Any, tools: list[StructuredTool], handle_parsing_errors: bool = True) -> AgentExecutor:
        try:
            return AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=handle_parsing_errors, verbose=True)
        except Exception as e:
            raise ValueError(f"Error initializing agent executor: {e}")

    def __classify_query(self, question: str) -> str:
        classification_prompt = CLASSIFICATION_PROMPT.format(question=question)
        response = self.llm.invoke([HumanMessage(content=classification_prompt)])
        return response.content.strip().lower()

    def __get_prompt_template_with_examples(self, examples: list[dict]) -> Any:
        prompt_identifier = PromptIdentifier()
        return prompt_identifier.get_prompt_template(examples)

    def query(self, question: str) -> str:
        try:
            query_type = self.__classify_query(question)

            if query_type == VYOM_LABEL:
                return self.__generate_bot_response(question)

            elif query_type == ARGHYA_LABEL:
                categories = self._classify_query_category(question)
                filtered_examples = self.__filter_examples(categories)
                print("Examples:", filtered_examples)

                prompt_template = self.__get_prompt_template_with_examples(filtered_examples)
                self.agent = self.__initialize_agent(self.tools, prompt_template)
                self.agent_executor = self.__initialize_agent_executor(self.agent, self.tools)

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

    def _classify_query_category(self, query: str) -> list[str]:
        category_prompt = CATEGORY_IDENTIFIER_TEMPLATE.format(query=query)
        response = self.llm.invoke([HumanMessage(content=category_prompt)])
        categories = [category.strip().lower() for category in response.content.split(",") if category.strip()]
        return categories

    def __filter_examples(self, categories: list[str]) -> list[dict]:
        filtered_examples = []
        if PERSON in categories:
            filtered_examples.extend(person)
        if EDUCATION in categories:
            filtered_examples.extend(education)
        if EXPERIENCE in categories:
            filtered_examples.extend(experience)
        if SKILLS in categories:
            filtered_examples.extend(skills)
        if CERTIFICATION in categories:
            filtered_examples.extend(certificate)
        if LANGUAGE in categories:
            filtered_examples.extend(language)
        if PROJECTS in categories:
            filtered_examples.extend(projects)
        if HONOUR_AND_AWARD_WITHOUT_UNDERSCORE in categories:
            filtered_examples.extend(honours_and_awards)
        if RECOMMENDATIONS in categories:
            filtered_examples.extend(recommendation)
        if BLOG in categories:
            filtered_examples.extend(blogs)

        return filtered_examples
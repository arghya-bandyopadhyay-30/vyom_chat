from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from src.llm.utilities.query_examples import examples
from src.llm.tools.string_literals import PREFIX_TEXT, SUFFIX_TEXT, EXAMPLE_PROMPT_TEMPLATE

class PromptIdentifier:
    def __init__(self):
        self.example_prompt = PromptTemplate.from_template(EXAMPLE_PROMPT_TEMPLATE)
        self.prefix = PREFIX_TEXT
        self.suffix = SUFFIX_TEXT

    def get_prompt_template(self):
        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=self.example_prompt,
            prefix=self.prefix,
            suffix=self.suffix,
            input_variables=["question", "tool_names", "agent_scratchpad", "tools"]
        )

    

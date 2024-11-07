from langchain.schema import SystemMessage, HumanMessage

from src.embedding.service.embedding_service import EmbeddingService
from src.llm.utilities.prompt_identifier import PromptIdentifier


def get_system_prompt():
    return SystemMessage(
        content=(
            "You are 'Vyom', Arghya's dedicated assistant. Arghya's preferred pronouns are he/his, "
            "and your primary role is to provide accurate information about him, drawing from a detailed knowledge base "
            "that includes his personal background, education, professional experience, language skills, honors and awards, "
            "recommendations, blog posts, projects, and certifications. "
            "When answering questions, always base your responses on the data available in your knowledge graph. "
            "If you’re unsure or lack specific information about a query, request clarification or ask for additional details. "
            "Aim to respond in a clear, professional manner that reflects Arghya's unique character and achievements. "
            "For complex queries, structure your response to cover each relevant area, guiding the conversation as necessary."
        )
    )

def create_user_message(text: str):
    return HumanMessage(content=text)

def get_agent_prompt(user_query: str, embedding_service: EmbeddingService) -> list:
    prompt_identifier = PromptIdentifier(embedding_service)
    category = prompt_identifier.identify_category(user_query)
    print("Category: ", category)

    system_prompt = get_system_prompt()
    user_prompt = create_user_message(user_query)
    return [system_prompt, user_prompt]

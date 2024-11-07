from langchain.schema import SystemMessage, HumanMessage

from src.embedding.service.embedding_service import EmbeddingService
from src.llm.utilities.category_identifier import CategoryIdentifier

category_prompts = {
    "personal_details": (
        "Fetch and display information about Arghya's personal details, including "
        "name, date of birth, nationality, and any other general personal details."
    ),
    "experience": (
        "Retrieve details about Arghya's professional experience, including job titles, "
        "companies, durations, and responsibilities. Organize each experience clearly and chronologically."
    ),
    "projects": (
        "List Arghya's projects, providing the project title, description, technologies used, "
        "and Arghya's role. Highlight any notable achievements or contributions in each project."
    ),
    "education": (
        "Display Arghya's educational background, including degrees obtained, institutions attended, "
        "fields of study, and dates. Mention any academic achievements or relevant coursework."
    ),
    "honours_and_awards": (
        "Fetch any honors and awards Arghya has received, including the award name, "
        "organization, and date awarded. Describe the significance of each award."
    ),
    "recommendations": (
        "Show recommendations provided for Arghya by colleagues or supervisors. "
        "Include the recommender's name, position, and a summary of their feedback."
    ),
    "blog_posts": (
        "List Arghya's blog posts with titles, dates published, and summaries. "
        "Indicate the main topics or themes covered in each post."
    ),
    "certifications": (
        "Fetch certifications obtained by Arghya, including certification titles, "
        "issuing organizations, and completion dates."
    ),
    "languages": (
        "List the languages Arghya speaks, along with proficiency levels (e.g., native, fluent, intermediate)."
    ),
    "general_greetings": (
        "Respond to the user’s greeting or introductory question, introducing yourself as Vyom, "
        "Arghya's assistant. Briefly explain your role and offer to help answer questions about Arghya."
    )
}

def get_category_prompt(category: str) -> str:
    return category_prompts.get(category, "I currently don't have a template for this category.")

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
    prompt_identifier = CategoryIdentifier(embedding_service)
    category = prompt_identifier.identify_category(user_query)
    print("Category: ", category)

    system_prompt = get_system_prompt()
    category_prompt = get_category_prompt(category)
    user_prompt = create_user_message(f"{category_prompt}\nUser Query: {user_query}")

    return [system_prompt, user_prompt]
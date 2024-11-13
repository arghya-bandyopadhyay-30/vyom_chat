import streamlit as st

from src.app.models.app_setup_config import AppSetupConfig
from src.llm.model.llm import LLMConfig
from src.llm.service.llm_service import LLMService
from src.utilities.uuid_provider import UUIDProvider


class WebApp:
    def __init__(self, app_config: AppSetupConfig, llm_config: LLMConfig):
        self.page_title = app_config.page_title
        self.page_icon = app_config.page_icon
        self.title = app_config.title
        self.subtitle = app_config.subtitle
        self.graph = app_config.graph_client.graph
        self.llm_service = LLMService(llm_config, self.graph)

    def run(self):
        if "session_id" not in st.session_state:
            self.__start_new_chat()

        self._initialize_ui()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        self._display_messages()

        self._display_faqs()

        if user_input := st.chat_input("💬 Curious about Arghya? Ask away! I'm ready to help. 🤓"):
            self._handle_user_input(user_input)

    def _initialize_ui(self) -> None:
        st.set_page_config(page_title=self.page_title, page_icon=self.page_icon)
        st.title(self.title)
        st.subheader(self.subtitle)

        st.sidebar.title("Chat Options")
        if st.sidebar.button("New Chat"):
            self.__start_new_chat()

        st.sidebar.subheader("FAQs")

    def __start_new_chat(self):
        st.session_state.session_id = str(UUIDProvider.generate_id())
        st.session_state.messages = []

    def _display_messages(self) -> None:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    def _display_faqs(self):
        faq_queries = [
            "Who is Arghya Bandyopadhyay?",
            "What is Arghya's current role?",
            "Which certifications did Arghya achieve in 2024?",
            "What is Arghya's role at Thoughtworks?",
            "What certifications does Arghya hold?",
            "What skills does Arghya have from his time at Thoughtworks?"
        ]
        for query in faq_queries:
            if st.sidebar.button(query):
                self._handle_user_input(query)

    def _handle_user_input(self, user_input: str) -> None:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        st.chat_message("user").write(user_input)

        with st.spinner("🍳 Wait, we are cooking your response... 🔄"):
            response = self.llm_service.query(user_input)
            if response:
                self._add_message_to_session("assistant", response)
                st.chat_message("assistant").write(response)
            else:
                st.error("Vyom failed to get a valid response. Please try again later.")

    def _add_message_to_session(self, role: str, content: str) -> None:
        st.session_state.messages.append({
            "role": role,
            "content": content
        })

import streamlit as st

from src.app.models.app_setup_config import AppSetupConfig
from src.llm.model.llm import LLMConfig
from src.llm.service.llm_service import LLMService


class Web:
    def __init__(self, app_config: AppSetupConfig, llm_config: LLMConfig):
        self.page_title = app_config.page_title
        self.page_icon = app_config.page_icon
        self.title = app_config.title
        self.subtitle = app_config.subtitle
        self.graph = app_config.graph_client.graph
        self.llm_service = LLMService(llm_config, self.graph)

    def run(self):
        st.set_page_config(page_title=self.page_title, page_icon=self.page_icon)
        st.title(self.title)
        st.subheader(self.subtitle)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if user_input := st.chat_input("Type your question here..."):
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            st.chat_message("user").write(user_input)

            response = self.llm_service.query(user_input)
            if response:
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": response
                })
                st.chat_message("assistant").write(response)
            else:
                st.error("Vyom failed to get a valid response. Please try again.")

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

        if prompt := st.chat_input("Type your question here..."):
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            st.chat_message("user").write(prompt)

            response = self.llm_service.query(prompt)
            if response and 'result' in response:
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": response['result']
                })
                st.chat_message("assistant").write(response['result'])
            else:
                st.error("Vyom failed to get a valid response. Please try again.")

from langchain_huggingface import HuggingFaceEmbeddings

from src.embedding.models.embedding import Embedding


class EmbeddingService:
    def __init__(self, embedding_config: Embedding):
        self.embedding_config = embedding_config
        self.model = self.embedding_config.model
        self.model_name = self.embedding_config.model_name
        self.api_key = self.embedding_config.api_key

        self.embedding = HuggingFaceEmbeddings(model_name=self.model_name)

    def embed_text(self, text: str) -> list[float]:
        embedding_result = self.embedding.embed_documents([text])
        return embedding_result[0] if embedding_result else []

    def embed_text_batch(self, texts: list[str]) -> list[list[float]]:
        return self.embedding.embed_documents(texts)
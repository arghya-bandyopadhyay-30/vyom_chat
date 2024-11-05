from src.embedding.models.embedding import Embedding
from src.ingestion.models.ingestion import Ingestion
from src.llm.model.llm import LLMConfig

class Config:
    def __init__(self, ingestion_config: Ingestion, embedding_config: Embedding, llm_config: LLMConfig):
        self.ingestion_config = ingestion_config
        self.embedding_config = embedding_config
        self.llm_config = llm_config
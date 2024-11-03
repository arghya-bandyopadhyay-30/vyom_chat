from src.embedding.models.embedding import Embedding
from src.ingestion.models.ingestion import Ingestion

class Config:
    def __init__(self, ingestion_config: Ingestion, embedding_config: Embedding):
        self.ingestion_config = ingestion_config
        self.embedding_config = embedding_config
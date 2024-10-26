from src.ingestion.models.ingestion import Ingestion

class Config:
    def __init__(self, ingestion_config: Ingestion):
        self.ingestion_config = ingestion_config
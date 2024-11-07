from src.embedding.service.embedding_service import EmbeddingService
from src.llm.utilities.sample_questions import sample_questions


class SampleQuestionEmbedding:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.embeddings = {}

    def embed_sample_questions(self):
        for category, questions in sample_questions.items():
            embedded_questions = self.embedding_service.embed_text_batch(questions)
            self.embeddings[category] = embedded_questions

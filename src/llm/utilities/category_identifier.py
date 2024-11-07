from sklearn.metrics.pairwise import cosine_similarity

from src.embedding.service.embedding_service import EmbeddingService
from src.llm.utilities.sample_question_embedding import SampleQuestionEmbedding


class CategoryIdentifier:
    def __init__(self, embedding_service: EmbeddingService):
        self.sample_embedding = SampleQuestionEmbedding(embedding_service)
        self.sample_embedding.embed_sample_questions()

    def identify_category(self, query: str) -> str:
        query_embedding = self.sample_embedding.embedding_service.embed_text(query)
        max_similarity, best_category = 0, None

        for category, embeddings in self.sample_embedding.embeddings.items():
            similarity = cosine_similarity([query_embedding], embeddings).max()
            if similarity > max_similarity:
                max_similarity = similarity
                best_category = category

        return best_category

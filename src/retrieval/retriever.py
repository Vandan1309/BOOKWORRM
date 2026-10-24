
from src.embeddings.embedder import Embedder
from src.retrieval.vector_store import VectorStore


class Retriever:
    def __init__(self, book_id: str = "jungle_book"):
        self.embedder = Embedder()
        self.store = VectorStore(book_id=book_id)

    def retrieve(
        self,
        question: str,
        top_k: int = 4,
    ) -> list[dict]:
        question = question.strip()

        if not question:
            return []

        query_embedding = self.embedder.encode_query(question)

        return self.store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

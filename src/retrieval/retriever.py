
from src.retrieval.vector_store import VectorStore


class Retriever:
    def __init__(self, book_id: str = "jungle_book"):
        self.store = VectorStore(book_id=book_id)

    def retrieve(
        self,
        question: str,
        top_k: int = 4,
    ) -> list[dict]:
        question = question.strip()

        if not question:
            return []

        return self.store.search(
            query_text=question,
            top_k=top_k,
        )


from pathlib import Path
import re
import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "chroma_db"


def make_collection_name(book_id: str) -> str:
    """Convert a book ID into a valid, predictable collection name."""
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", book_id.lower())
    safe_id = safe_id.strip("_-")

    if not safe_id:
        raise ValueError("Book ID must contain letters or numbers.")

    return f"book_{safe_id}"[:60]


class VectorStore:
    def __init__(self, book_id: str = "jungle_book"):
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        self.book_id = book_id
        self.collection_name = make_collection_name(book_id)

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self):
        """Rebuild only this book's index."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ):
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must match.")

        batch_size = 100

        for start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[start:start + batch_size]
            batch_embeddings = embeddings[start:start + batch_size]

            self.collection.add(
                ids=[c["chunk_id"] for c in batch_chunks],
                documents=[c["text"] for c in batch_chunks],
                embeddings=batch_embeddings,
                metadatas=[
                    {"page": c["page"], "book_id": self.book_id}
                    for c in batch_chunks
                ],
            )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 4,
    ) -> list[dict]:
        count = self.collection.count()

        if count == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"],
        )

        matches = []

        for i, document in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]

            matches.append({
                "text": document,
                "page": metadata["page"],
                "book_id": metadata.get("book_id", self.book_id),
                "distance": results["distances"][0][i],
            })

        return matches

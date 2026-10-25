
import os
import re
import uuid

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


def make_collection_name(book_id: str) -> str:
    """Create a predictable Qdrant collection name for a book."""
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", book_id.lower())
    safe_id = safe_id.strip("_-")

    if not safe_id:
        raise ValueError("Book ID must contain letters or numbers.")

    return f"book_{safe_id}"[:60]


class VectorStore:
    def __init__(self, book_id: str = "jungle_book"):
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not url or not api_key:
            raise RuntimeError(
                "QDRANT_URL and QDRANT_API_KEY must be configured."
            )

        self.client =  QdrantClient(
    url=url,
    api_key=api_key,
    cloud_inference=True,
)
        self.book_id = book_id
        self.collection_name = make_collection_name(book_id)

        if not self.client.collection_exists(self.collection_name):
            raise ValueError(
                f"Qdrant collection '{self.collection_name}' does not exist."
            )

        info = self.client.get_collection(self.collection_name)
        vector_config = info.config.params.vectors

        if (
            not isinstance(vector_config, dict)
            and vector_config.size != EMBEDDING_DIMENSION
        ):
            raise ValueError(
                f"Collection '{self.collection_name}' must use "
                f"{EMBEDDING_DIMENSION}-dimensional vectors."
            )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ):
        """Add precomputed embeddings; does not run a local model."""
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must match.")

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            if len(embedding) != EMBEDDING_DIMENSION:
                raise ValueError("Embedding must have 384 dimensions.")

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{self.book_id}:{chunk['chunk_id']}",
                )
            )

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"],
                        "page": chunk["page"],
                        "book_id": self.book_id,
                    },
                )
            )

        for start in range(0, len(points), 100):
            self.client.upsert(
                collection_name=self.collection_name,
                points=points[start:start + 100],
                wait=True,
            )

    def search(
        self,
        query_text: str,
        top_k: int = 4,
    ) -> list[dict]:
        """Embed the query through Qdrant inference and retrieve chunks."""
        query_text = query_text.strip()

        if not query_text or top_k <= 0:
            return []

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=models.Document(
                text=query_text,
                model=EMBEDDING_MODEL,
            ),
            limit=top_k,
            with_payload=True,
        ).points

        matches = []

        for point in results:
            payload = point.payload or {}

            matches.append(
                {
                    "text": payload.get("text", ""),
                    "page": payload.get("page"),
                    "book_id": payload.get("book_id", self.book_id),
                    "distance": 1.0 - point.score,
                }
            )

        return matches

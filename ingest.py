
import argparse

from src.book_registry import get_book
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_pages
from src.embeddings.embedder import Embedder
from src.retrieval.vector_store import VectorStore


def ingest_book(book_id: str):
    book = get_book(book_id)
    pdf_path = (
        __import__("pathlib").Path(__file__).resolve().parent
        / "data" / "books" / book["filename"]
    )

    print(f"\nIndexing: {book['title']} by {book['author']}")

    pages = load_pdf(pdf_path)
    print(f"Pages with text: {len(pages)}")

    chunks = chunk_pages(pages)
    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No text chunks were generated.")

    embedder = Embedder()
    embeddings = embedder.encode_documents(
        [chunk["text"] for chunk in chunks]
    )

    store = VectorStore(book_id=book_id)
    store.reset()
    store.add_chunks(chunks, embeddings)

    print(f"Collection: {store.collection_name}")
    print(f"Vectors stored: {store.collection.count()}")
    print(f"SUCCESS: {book['title']} is indexed.")


def main():
    parser = argparse.ArgumentParser(
        description="Index a preloaded book for WildPages."
    )
    parser.add_argument(
        "--book",
        default="jungle_book",
        help="Book ID from src/book_registry.py",
    )
    args = parser.parse_args()

    ingest_book(args.book)


if __name__ == "__main__":
    main()


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
def find_books_dir() -> Path:
    for folder in PROJECT_ROOT.iterdir():
        if folder.is_dir() and folder.name.lower() == "data":
            candidate = folder / "books"
            if candidate.is_dir():
                return candidate

    return PROJECT_ROOT / "data" / "books"


BOOKS_DIR = find_books_dir()

BOOKS = {
    "jungle_book": {
        "title": "The Jungle Book",
        "author": "Rudyard Kipling",
        "filename": "jungle_book.pdf",
        "description": "Explore Mowgli and the laws of the jungle.",
        "available": True,
    },
    "alice_in_wonderland": {
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "filename": "alice_in_wonderland.pdf",
        "description": "Explore Alice's adventures in Wonderland.",
        "available": True,
    },
    "around_the_world": {
        "title": "Around the World in Eighty Days",
        "author": "Jules Verne",
        "filename": "around_the_world_in_80_days.pdf",
        "description": "Follow Phileas Fogg's journey around the world.",
        "available": True,
    },
    "wuthering_heights": {
        "title": "Wuthering Heights",
        "author": "Emily Bronte",
        "filename": "wuthering_heights.pdf",
        "description": "Explore the relationships and conflicts in the novel.",
        "available": True,
    },
}


def get_book(book_id: str) -> dict:
    if book_id not in BOOKS:
        raise KeyError(f"Unknown book ID: {book_id}")

    book = BOOKS[book_id]
    pdf_path = BOOKS_DIR / book["filename"]

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    return book


def get_available_books() -> dict:
    return {
        book_id: book
        for book_id, book in BOOKS.items()
        if book["available"]
        and (BOOKS_DIR / book["filename"]).is_file()
    }

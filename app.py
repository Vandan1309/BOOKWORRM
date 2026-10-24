
from functools import lru_cache
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.book_registry import BOOKS_DIR, get_available_books, get_book
from src.generation.rag_pipeline import RAGPipeline


app = FastAPI(
    title="BOOKWORRM API",
    description="AI reading companion powered by your existing RAG backend.",
    version="1.0.0",
)

# Allow the v0 frontend and local development frontend to call the API.
# Restrict this to your deployed frontend domain before production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    book_id: str = Field(min_length=1)
    question: str = Field(min_length=1, max_length=2000)


@lru_cache(maxsize=4)
def get_pipeline(book_id: str) -> RAGPipeline:
    """Reuse each book's pipeline instead of recreating it per question."""
    return RAGPipeline(book_id=book_id)


@app.get("/")
def root():
    return {
        "name": "BOOKWORRM API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/books")
def list_books():
    books = get_available_books()

    return {
        "books": [
            {
                "id": book_id,
                "title": details["title"],
                "author": details["author"],
                "description": details["description"],
            }
            for book_id, details in books.items()
        ]
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Please enter a question.",
        )

    try:
        book = get_book(request.book_id)
        pipeline = get_pipeline(request.book_id)
        result = pipeline.ask(question)

        return {
            "book_id": request.book_id,
            "book_title": book["title"],
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
        }

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="The selected book is not registered.",
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="The PDF for the selected book could not be found.",
        )

    except Exception:
        # Keep API keys and internal error details out of responses.
        raise HTTPException(
            status_code=500,
            detail=(
                "Something went wrong while generating the answer. "
                "Check the backend terminal for details."
            ),
        )

@app.get("/books/{book_id}/pdf")
def get_book_pdf(book_id: str):
    try:
        book = get_book(book_id)
        pdf_path = BOOKS_DIR / book["filename"]

        if not pdf_path.is_file():
            raise HTTPException(status_code=404, detail="Book PDF not found.")

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=book["filename"],
            content_disposition_type="inline",
        )

    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown book ID.")


@app.get("/books/{book_id}/details")
def get_book_details(book_id: str):
    try:
        book = get_book(book_id)
        pdf_path = BOOKS_DIR / book["filename"]

        if not pdf_path.is_file():
            raise HTTPException(status_code=404, detail="Book PDF not found.")

        import fitz

        with fitz.open(pdf_path) as document:
            page_count = document.page_count

        return {
            "id": book_id,
            "title": book["title"],
            "author": book["author"],
            "page_count": page_count,
            "pdf_url": f"/books/{book_id}/pdf",
        }

    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown book ID.")

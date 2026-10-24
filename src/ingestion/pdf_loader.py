
from pathlib import Path
import fitz

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BOOKS_DIR = PROJECT_ROOT / "data" / "books"


def load_pdf(pdf_path: Path | None = None) -> list[dict]:
    if pdf_path is None:
        pdf_path = BOOKS_DIR / "jungle_book.pdf"

    pdf_path = Path(pdf_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({
                    "page": page_number,
                    "text": text,
                })

    if not pages:
        raise ValueError(
            "No selectable text found. The PDF may require OCR."
        )

    return pages

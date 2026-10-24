
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """
    Split extracted page text into overlapping chunks.
    Each chunk retains its original PDF page number.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size.")

    chunks = []

    for page_data in pages:
        text = page_data["text"].strip()
        page_number = page_data["page"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number,
                    "chunk_id": f"page_{page_number}_chunk_{len(chunks)}",
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks


from src.retrieval.retriever import Retriever
from src.generation.llm_service import LLMService
from src.book_registry import get_book


class RAGPipeline:
    def __init__(self, book_id: str = "jungle_book"):
        self.book_id = book_id
        self.retriever = Retriever(book_id=book_id)
        self.llm = LLMService()

    def ask(self, question: str) -> dict:
        question = question.strip()

        if not question:
            return {
                "answer": "Please enter a question.",
                "sources": [],
            }

        passages = self.retriever.retrieve(question, top_k=4)

        if not passages:
            return {
                "answer": (
                    "I couldn't find relevant passages in the selected "
                    "book to answer that question."
                ),
                "sources": [],
            }

        book = get_book(self.book_id)

        answer = self.llm.generate_answer(
            question,
            passages,
            book_title=book["title"],
            author=book["author"],
        )

        sources = [
            {
                "book_id": passage.get("book_id", self.book_id),
                "page": passage["page"],
                "text": passage["text"],
                "distance": passage["distance"],
            }
            for passage in passages
        ]

        return {
            "answer": answer,
            "sources": sources,
        }

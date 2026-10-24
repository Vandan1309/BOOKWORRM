
from src.generation.rag_pipeline import RAGPipeline

TESTS = [
    (
        "jungle_book",
        "Who is Mowgli?",
    ),
    (
        "alice_in_wonderland",
        "Who does Alice follow down the rabbit hole?",
    ),
    (
        "around_the_world",
        "What is Phileas Fogg trying to accomplish?",
    ),
    (
        "wuthering_heights",
        "Who are Catherine Earnshaw and Heathcliff?",
    ),
]


def main():
    for book_id, question in TESTS:
        print("\n" + "=" * 70)
        print(f"BOOK: {book_id}")
        print(f"QUESTION: {question}")
        print("=" * 70)

        rag = RAGPipeline(book_id=book_id)
        result = rag.ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(
                f"Book: {source['book_id']} | "
                f"PDF page: {source['page']} | "
                f"Distance: {source['distance']:.3f}"
            )
            print(source["text"][:250])
            print("-" * 40)


if __name__ == "__main__":
    main()

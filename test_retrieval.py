
from src.retrieval.retriever import Retriever


def main():
    retriever = Retriever()

    questions = [
        "Who is Mowgli?",
        "What is Shere Khan's relationship with Mowgli?",
        "What does Baloo teach Mowgli?",
    ]

    for question in questions:
        print("\n" + "=" * 65)
        print(f"QUESTION: {question}")
        print("=" * 65)

        results = retriever.retrieve(question, top_k=3)

        for index, result in enumerate(results, start=1):
            print(
                f"\nResult {index} | "
                f"PDF page {result['page']} | "
                f"Cosine distance: {result['distance']:.3f}"
            )
            print(result["text"][:500])


if __name__ == "__main__":
    main()


from src.generation.rag_pipeline import RAGPipeline


def main():
    rag = RAGPipeline()

    questions = [
        "Who is Mowgli?",
        "What does Baloo teach Mowgli?",
        "What is the capital of France?",
    ]

    for question in questions:
        print("\n" + "=" * 60)
        print("QUESTION:", question)
        print("=" * 60)

        result = rag.ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"\nPDF page {source['page']}")
            print(source["text"][:250])


if __name__ == "__main__":
    main()

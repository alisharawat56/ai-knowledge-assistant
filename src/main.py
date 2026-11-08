from src.qa import answer_question


def main():
    print("=" * 60)
    print("AI KNOWLEDGE ASSISTANT")
    print("=" * 60)

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        result = answer_question(question)

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(result["answer"])

        if result["sources"]:
            print("\nSOURCE REFERENCES")

            for source in result["sources"]:
                print(f"\n[{source['source_label']}]")
                print(f"Document: {source['document_name']}")
                print(f"Title: {source['title']}")
                print(f"Source ID: {source['chunk_id']}")
                print(f"URL: {source['source_url']}")

        if result["error"]:
            print(f"\nError: {result['error']}")


if __name__ == "__main__":
    main()
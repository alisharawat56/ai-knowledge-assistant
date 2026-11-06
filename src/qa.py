
import os
import requests
from dotenv import load_dotenv

from src.search import retrieve_documents

load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

LLM_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3.5:0.8b"
)


def generate_answer(question, retrieved_chunks):
    """Ask the local LLM to answer using retrieved evidence."""

    evidence = []

    for number, chunk in enumerate(retrieved_chunks, start=1):
        evidence.append(
            f"""
[S{number}]
Source ID: {chunk['chunk_id']}
Document: {chunk['document_name']}
Title: {chunk['title']}
URL: {chunk['source_url']}

Passage:
{chunk['text']}
"""
        )

    context = "\n".join(evidence)

    prompt = f"""
You are an AI Knowledge Assistant.

Answer the user's question using ONLY the evidence
provided below.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts or sources.
3. If the evidence does not answer the question,
   clearly say that the provided documents do not
   contain enough information.
4. Cite evidence using its source label, such as [S1].
5. Put citations next to the claims they support.
6. Write a clear, direct answer.
7. Every factual claim must be supported by a provided passage.
8. Do not introduce examples, comparisons, or facts from outside
   the provided evidence.
9. If only part of the question is answered by the evidence,
   answer only that part and clearly identify the limitation.
10. Do not cite a source unless its passage supports the claim.
11. Before responding, check that the answer is consistent
    with the provided evidence.

USER QUESTION:
{question}

PROVIDED EVIDENCE:
{context}

ANSWER:
"""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 300
        }
    },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()
    answer = data.get("message", {}).get("content", "").strip()

    if not answer:
        raise ValueError(
            "The LLM returned an empty answer. "
            "Check the Ollama model response."
        )

    return answer


def ask_question(question):
    """Retrieve evidence, generate an answer, and show sources."""

    print("\nSearching your knowledge base...")

    retrieved_chunks, all_results = retrieve_documents(question)

    if not retrieved_chunks:
        print("\nAnswer:")
        print(
            "I couldn't find sufficiently relevant information "
            "in your documents to answer this question."
        )

        if all_results:
            print(
                "\nClosest match score: "
                f"{all_results[0]['score']:.3f}"
            )

        print("\nNo answer was generated because useful evidence "
              "was not found.")
        return

    print(f"Found {len(retrieved_chunks)} relevant passage(s).")
    print("\nGenerating answer with the local LLM...")

    answer = generate_answer(question, retrieved_chunks)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    print("\n" + "=" * 70)
    print("SOURCE REFERENCES")
    print("=" * 70)

    for number, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\n[S{number}]")
        print(f"Source ID: {chunk['chunk_id']}")
        print(f"Document: {chunk['document_name']}")
        print(f"Title: {chunk['title']}")
        print(f"Similarity: {chunk['score']:.3f}")
        print(f"URL: {chunk['source_url']}")


def main():
    print("=" * 60)
    print("       AI KNOWLEDGE ASSISTANT")
    print("=" * 60)
    print("Ask questions about your Python documentation.")
    print("Type 'exit' to quit.")

    while True:
        print()
        question = input("Your question: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            ask_question(question)

        except requests.RequestException as error:
            print(f"\nOllama connection error: {error}")

        except (KeyError, ValueError) as error:
            print(f"\nUnexpected response from Ollama: {error}")

        except FileNotFoundError as error:
            print(f"\n{error}")

        except Exception as error:
            print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()

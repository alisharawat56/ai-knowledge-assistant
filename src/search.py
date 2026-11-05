import json
import math
import os
import sqlite3
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "knowledge.db"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)
EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 5
MIN_SIMILARITY = 0.60


def generate_embedding(text):
    """Convert a question into an embedding."""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "prompt": "search_document: " + text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


def cosine_similarity(vector_a, vector_b):
    """Calculate how similar two vectors are."""

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_documents(question):
    if not DATABASE_FILE.exists():
        print("Vector database not found.")
        print("Run python -m src.build_vector_store first.")
        return

    question_embedding = generate_embedding(question)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        "SELECT * FROM chunks"
    ).fetchall()

    connection.close()

    results = []

    for row in rows:
        stored_embedding = json.loads(row["embedding"])

        score = cosine_similarity(
            question_embedding,
            stored_embedding
        )

        results.append({
            "score": score,
            "chunk_id": row["chunk_id"],
            "document_name": row["document_name"],
            "title": row["title"],
            "source_url": row["source_url"],
            "text": row["text"]
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    print(f"\nQuestion: {question}")
    print("\nMost relevant passages:\n")

    matches = [
        result for result in results
        if result["score"] >= MIN_SIMILARITY
    ][:TOP_K]

    if not matches:
        print("No strong matches found in your documents.")
        if results:
            print(
                f"Closest similarity score: "
                f"{results[0]['score']:.3f}"
            )
        return

    for number, result in enumerate(matches, start=1):
        print("=" * 70)
        print(f"Result {number}")
        print(f"Similarity: {result['score']:.3f}")
        print(f"Source ID: {result['chunk_id']}")
        print(f"Document: {result['document_name']}")
        print(f"Title: {result['title']}")
        print(f"Source URL: {result['source_url']}")
        print("\nPassage:")
        print(result["text"])
        print()


if __name__ == "__main__":
    user_question = input("Enter your question: ").strip()

    if user_question:
        try:
            search_documents(user_question)
        except requests.RequestException as error:
            print(f"Could not contact Ollama: {error}")
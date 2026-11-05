
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

# This is an experimental starting threshold.
# Calibrate it using your relevant and unrelated test questions.
MIN_SIMILARITY = 0.60


def generate_embedding(text):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "prompt": "search_query: " + text
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["embedding"]


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_documents(question):
    """Return relevant document chunks, ranked by similarity."""

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            "Knowledge database not found. "
            "Run: python -m src.build_vector_store"
        )

    question_embedding = generate_embedding(question)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute(
            "SELECT * FROM chunks"
        ).fetchall()
    finally:
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
        key=lambda item: item["score"],
        reverse=True
    )

    # Only return chunks above the relevance threshold.
    matches = [
        item for item in results
        if item["score"] >= MIN_SIMILARITY
    ][:TOP_K]

    return matches, results


def search_documents(question):
    """Keep the Day 3 search command available."""

    matches, all_results = retrieve_documents(question)

    print(f"\nQuestion: {question}")

    if not matches:
        print("\nNo strong matches found.")
        if all_results:
            print(
                "Closest similarity score: "
                f"{all_results[0]['score']:.3f}"
            )
        return

    print("\nMost relevant passages:\n")

    for number, result in enumerate(matches, start=1):
        print("=" * 70)
        print(f"Result: {number}")
        print(f"Similarity: {result['score']:.3f}")
        print(f"Source ID: {result['chunk_id']}")
        print(f"Document: {result['document_name']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['source_url']}")
        print("\nPassage:")
        print(result["text"])


if __name__ == "__main__":
    question = input("Enter your question: ").strip()

    if question:
        try:
            search_documents(question)
        except requests.RequestException as error:
            print(f"Could not contact Ollama: {error}")

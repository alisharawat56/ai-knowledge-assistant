import json
import os
import sqlite3
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHUNKS_FILE = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "knowledge.db"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)
EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text):
    """Convert text into a numerical vector using Ollama."""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "prompt": "search_document: " + text
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    return data["embedding"]


def create_database():
    """Create a local SQLite database for chunks and vectors."""

    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            document_name TEXT,
            title TEXT,
            source_url TEXT,
            topic TEXT,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL,
            embedding_model TEXT NOT NULL
        )
    """)

    connection.commit()
    return connection


def build_vector_store():
    if not CHUNKS_FILE.exists():
        print(f"Chunks file not found: {CHUNKS_FILE}")
        print("Run your Day 2 ingestion script first.")
        return

    connection = create_database()

    total = 0

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            chunk = json.loads(line)
            chunk_text = chunk["text"]

            try:
                embedding = generate_embedding(chunk_text)

                connection.execute(
                    """
                    INSERT OR REPLACE INTO chunks (
                        chunk_id,
                        document_name,
                        title,
                        source_url,
                        topic,
                        text,
                        embedding,
                        embedding_model
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk["chunk_id"],
                        chunk.get("document_name", ""),
                        chunk.get("title", ""),
                        chunk.get("source_url", ""),
                        chunk.get("topic", ""),
                        chunk_text,
                        json.dumps(embedding),
                        EMBEDDING_MODEL
                    )
                )

                total += 1

                if total % 10 == 0:
                    connection.commit()
                    print(f"Embedded {total} chunks...")

            except (requests.RequestException, KeyError, ValueError) as error:
                print(f"Could not embed chunk {chunk.get('chunk_id')}: {error}")

    connection.commit()
    connection.close()

    print("\nVector store build complete!")
    print(f"Chunks stored: {total}")
    print(f"Database: {DATABASE_FILE}")


if __name__ == "__main__":
    build_vector_store()
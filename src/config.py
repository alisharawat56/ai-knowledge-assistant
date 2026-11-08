from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3.5:0.8b"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "knowledge.db"
CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"

TOP_K = 5
MIN_SIMILARITY = 0.60
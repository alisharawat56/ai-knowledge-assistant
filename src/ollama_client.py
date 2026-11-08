import requests

from src.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    EMBEDDING_MODEL
)


class OllamaError(Exception):
    """Raised when communication with Ollama fails."""


def get_embedding(text, is_query=False):
    prefix = "search_query: " if is_query else "search_document: "

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={
                "model": EMBEDDING_MODEL,
                "prompt": prefix + text
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        embedding = data.get("embedding")

        if not embedding:
            raise OllamaError("Ollama returned an empty embedding.")

        return embedding

    except (requests.exceptions.RequestException, ValueError) as exc:
        raise OllamaError(f"Embedding request failed: {exc}") from exc


def generate_response(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 300
                }
            },
            timeout=120
        )

        response.raise_for_status()
        data = response.json()

        answer = data.get("message", {}).get("content", "").strip()

        if not answer:
            raise OllamaError("Ollama returned an empty answer.")

        return answer

    except (requests.exceptions.RequestException, ValueError) as exc:
        raise OllamaError(f"Chat request failed: {exc}") from exc
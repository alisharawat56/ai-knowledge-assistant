
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")


def answer_question(question):

    sources = [
        {
            "title": "Sample University Policy",
            "url": "https://example.com/policy",
            "passage": "University policies provide guidelines for students."
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": question}
                ],
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()
        answer = data["message"]["content"]

        return {
            "answer": answer,
            "sources": sources,
            "error": None
        }

    except requests.exceptions.RequestException as e:
        return {
            "answer": "Unable to generate an answer.",
            "sources": [],
            "error": str(e)
        }

    except (ValueError, KeyError) as e:
        return {
            "answer": "Unable to process the model response.",
            "sources": [],
            "error": str(e)
        }


if __name__ == "__main__":
    question = input("Ask your question: ")
    result = answer_question(question)

    print("\n--- AI KNOWLEDGE ASSISTANT ---")
    print(json.dumps(result, indent=4))

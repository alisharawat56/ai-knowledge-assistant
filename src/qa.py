from src.search import retrieve_documents
from src.ollama_client import generate_response


def answer_question(question):
    """Retrieve evidence and generate an answer."""

    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "error": "empty_question"
        }

    try:
        matches, _ = retrieve_documents(question)

        if not matches:
            return {
                "answer": (
                    "I don't have enough information in the "
                    "available documents to answer this question."
                ),
                "sources": [],
                "error": None
            }

        context = []
        sources = []

        for index, chunk in enumerate(matches, start=1):
            source_label = f"S{index}"

            context.append(
                f"[{source_label}]\n"
                f"Document: {chunk.get('document_name', 'Unknown')}\n"
                f"Title: {chunk.get('title', 'Unknown')}\n"
                f"Passage: {chunk.get('text', '')}"
            )

            sources.append({
                "source_label": source_label,
                "chunk_id": chunk.get("chunk_id"),
                "document_name": chunk.get("document_name"),
                "title": chunk.get("title"),
                "source_url": chunk.get("source_url")
            })

        prompt = f"""
You are a knowledge assistant.

Answer the question using ONLY the evidence below.

Rules:
1. Every factual claim must be supported by the passages.
2. Do not introduce outside information.
3. Do not invent examples or sources.
4. Cite supporting passages using [S1], [S2], etc.
5. If the evidence is insufficient, say so clearly.
6. Do not cite a passage unless it supports the claim.

Evidence:
{chr(10).join(context)}

Question:
{question}

Answer:
"""

        answer = generate_response(prompt)

        return {
            "answer": answer,
            "sources": sources,
            "error": None
        }

    except FileNotFoundError:
        return {
            "answer": "The knowledge base is missing. Please build it first.",
            "sources": [],
            "error": "missing_knowledge_base"
        }

    except Exception as exc:
        return {
            "answer": "An error occurred while processing your question.",
            "sources": [],
            "error": str(exc)
        }
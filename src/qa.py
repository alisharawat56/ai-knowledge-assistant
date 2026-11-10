from src.search import retrieve_documents
from src.ollama_client import generate_response
from src.response_schema import validate_response


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
                "document_name": chunk.get("document_name", "Unknown document"),
                "title": chunk.get("title", "Untitled"),
                "source_url": chunk.get("source_url"),
                "text": chunk.get("text", "")
            })

        prompt = f"""
You are a knowledge assistant.

Answer the user's question using only the supplied evidence.

Rules:
1. Do not use outside knowledge.
2. Cite supporting statements using labels such as [S1] and [S2].
3. Only cite labels that appear in the supplied evidence.
4. If the evidence does not answer the question, say so clearly.
5. Do not invent documents, source labels, or facts.
6. Return only the answer text, not JSON.

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

import json
import hashlib
from pathlib import Path


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_DIR = PROJECT_ROOT / "documents" / "raw"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "documents.jsonl"


# Chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def generate_id(text):
    """Generate a deterministic ID using SHA256."""
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def read_document(file_path):
    """Read a Markdown or TXT document."""

    content = file_path.read_text(encoding="utf-8")

    metadata = {}

    # Extract simple Markdown front matter
    if content.startswith("---"):
        parts = content.split("---", 2)

        if len(parts) == 3:
            metadata_text = parts[1]
            content = parts[2]

            for line in metadata_text.strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)

                    metadata[key.strip()] = (
                        value.strip().strip('"').strip("'")
                    )

    metadata.setdefault("title", file_path.stem)
    metadata.setdefault("topic", "Python Programming")
    metadata.setdefault("source_url", "")
    metadata.setdefault("document_type", "Local Document")

    return content.strip(), metadata


def split_into_chunks(text):
    """Split text into overlapping character-based chunks."""

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + CHUNK_SIZE, len(text))

        # Prefer ending at a word boundary
        if end < len(text):
            boundary = text.rfind(
                " ",
                start + CHUNK_SIZE // 2,
                end
            )

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "text": chunk,
                "char_start": start,
                "char_end": end
            })

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def ingest_documents():

    files = sorted(
        list(DOCUMENTS_DIR.glob("*.md")) +
        list(DOCUMENTS_DIR.glob("*.txt"))
    )

    # Validate document collection size
    if not 10 <= len(files) <= 30:
        raise ValueError(
            f"Expected 10-30 documents, found {len(files)}."
        )

    all_chunks = []

    for file_path in files:

        print(f"Processing: {file_path.name}")

        text, metadata = read_document(file_path)

        if not text:
            print("Skipping empty document.")
            continue

        relative_path = str(
            file_path.relative_to(DOCUMENTS_DIR)
        ).replace("\\", "/")

        document_id = generate_id(relative_path)

        chunks = split_into_chunks(text)

        for index, chunk in enumerate(chunks):

            chunk_id = generate_id(
                f"{document_id}:{index}:{chunk['text']}"
            )

            record = {
                "chunk_id": chunk_id,
                "document_id": document_id,
                "document_name": file_path.name,
                "title": metadata["title"],
                "source_url": metadata["source_url"],
                "topic": metadata["topic"],
                "document_type": metadata["document_type"],
                "chunk_index": index,
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "text": chunk["text"]
            }

            all_chunks.append(record)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save one JSON object per line
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:

        for chunk in all_chunks:
            file.write(
                json.dumps(chunk, ensure_ascii=False) + "\n"
            )

    print("\n--- INGESTION COMPLETE ---")
    print(f"Documents processed: {len(files)}")
    print(f"Chunks generated: {len(all_chunks)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    ingest_documents()

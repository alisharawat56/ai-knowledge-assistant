
# RAG Methodology

## 1. Document Ingestion

The application uses Python programming documentation as its knowledge base.

Ten documentation files are stored in the documents/raw directory. The ingestion process reads the files and extracts their text and metadata.

## 2. Chunking

Documents are divided into smaller overlapping passages.

Configuration:
- Chunk size: 1,000 characters
- Chunk overlap: 150 characters

Overlapping chunks help preserve context between adjacent passages.

Each chunk receives a stable identifier generated using a hash.

## 3. Embedding Generation

The application uses the locally hosted nomic-embed-text model through Ollama.

Each document chunk is converted into a numerical vector representing its semantic content.

Document embeddings use the search_document prefix, while question embeddings use the search_query prefix.

## 4. Vector Storage

The application stores document text, metadata, identifiers, and embeddings in a local SQLite database.

This allows the application to retrieve relevant information without rebuilding embeddings for every question.

## 5. Retrieval

When a user submits a question:

1. The question is converted into an embedding.
2. The system compares it against stored document embeddings.
3. Cosine similarity is used to rank relevant passages.
4. The top five passages are considered for retrieval.
5. A similarity threshold is used to filter weak matches.

The current retrieval configuration uses a minimum similarity threshold of 0.60.

Similarity is a ranking signal, not proof that a passage supports an answer.

## 6. Answer Generation

The retrieved passages are assembled into a prompt with source labels.

The prompt instructs the locally hosted Qwen 3.5 model to answer using the supplied evidence and avoid unsupported claims.

The model runs through Ollama.

## 7. User Interface

Streamlit provides:
- A question input area
- An Ask button
- An answer display area
- Expandable retrieved source passages
- Insufficient-evidence feedback

The entire pipeline runs locally.

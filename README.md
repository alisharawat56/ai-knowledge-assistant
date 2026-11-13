# AI Knowledge Assistant

A local Retrieval-Augmented Generation (RAG) application that answers questions using a collection of Python documentation.

The application retrieves relevant document passages using semantic search and generates answers with a locally hosted language model. Answers include references to retrieved source passages.

## Features

- Document ingestion and text chunking
- Embedding generation using Ollama
- Semantic search using cosine similarity
- Local SQLite knowledge database
- Answer generation using a local LLM
- Source passage display
- Streamlit user interface
- Evaluation and automated tests
- Basic input validation and prompt-injection safeguards

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen 3.5 (0.8B)
- Nomic Embed Text
- SQLite
- Pandas
- Pytest

## Requirements

- Windows 10 or 11
- Python 3.14 (or a compatible Python version)
- Ollama installed and running
- Git

No paid API key or subscription is required.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/alisharawat56/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 2. Run setup

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

### 3. Download the local models

```powershell
ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
```

### 4. Configure the application

Copy `.env.example` to `.env` if `.env` does not already exist.

The default local configuration is:

```dotenv
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:0.8b
```

### 5. Launch the application

Make sure Ollama is running, then execute:

```powershell
.\run_demo.ps1
```

Alternatively, launch Streamlit directly:

```powershell
python -m streamlit run app.py
```

Open the local address shown in the terminal, normally:

http://localhost:8501

## Running Tests

```powershell
python -m pytest -v
```

## How It Works

1. Python documentation is loaded into the application.
2. Documents are split into overlapping text chunks.
3. The embedding model converts chunks into numerical vectors.
4. Vectors and document metadata are stored locally in SQLite.
5. A user submits a question through the Streamlit interface.
6. The system retrieves relevant passages using semantic similarity.
7. The local language model generates an answer using the retrieved context.
8. The interface displays the answer and its source passages.

## Project Structure

```text
app.py
setup.ps1
run_demo.ps1
requirements.txt
README.md
documents/
data/
src/
tests/
```

## Limitations

- The application is designed for a Python documentation knowledge base.
- Answer quality depends on document coverage and retrieval quality.
- A retrieved source does not automatically guarantee that every generated statement is supported.
- Prompt-injection safeguards reduce risk but cannot guarantee complete protection.
- The application requires Ollama and the specified models to be installed locally.
- This is a local demonstration project, not a production-hosted service.

## Privacy and Cost

The application uses locally hosted models through Ollama. It does not require paid model API credits. Questions and document processing are handled through the local application and Ollama setup.

## Author

Developed as an end-to-end AI knowledge management and information retrieval project.

# Failure Cases and Limitations

## 1. Limited Knowledge Base

The current application uses a collection of Python programming documentation.

It cannot reliably answer questions about topics that are not covered by these documents.

## 2. Retrieval Limitations

Semantic similarity does not guarantee that a retrieved passage contains the correct answer.

Relevant passages may be missed or ranked incorrectly.

## 3. Hallucinations

The language model can generate incorrect information even when relevant passages are retrieved.

Retrieved context reduces reliance on general model knowledge but does not eliminate hallucinations.

## 4. Prompt Injection

The application includes basic prompt instructions intended to treat retrieved document content as untrusted data.

These safeguards are not a complete defense against prompt injection.

The application does not intentionally provide the model with arbitrary code execution or external tool access.

## 5. Evaluation Limitations

The initial evaluation used a relatively small dataset of 25 questions.

Automated retrieval checks do not establish factual correctness or complete answer grounding.

Manual review and a larger test dataset are needed for stronger conclusions.

## 6. Local Deployment

The application requires Python, Ollama, and locally downloaded models.

Model inference depends on the user's available memory and hardware.

The current application is a local demonstration, not a production-hosted multi-user service.

## 7. Future Improvements

- Expand the knowledge base.
- Improve retrieval quality.
- Add more comprehensive answer-grounding evaluation.
- Introduce document upload functionality.
- Improve response validation.
- Add authentication and deployment safeguards before any public multi-user release.

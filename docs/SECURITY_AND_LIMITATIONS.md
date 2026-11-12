# Security and Application Limitations

## Security safeguards implemented

1. User questions are validated before retrieval and generation.
2. Question length is limited to 1,000 characters.
3. Retrieved document content is explicitly treated as untrusted data.
4. The prompt instructs the model not to follow embedded document instructions.
5. The model is not given tool access or permission to execute arbitrary code.
6. Model output is validated before being displayed.
7. Source references must correspond to retrieved document chunks.
8. Application errors are presented using user-friendly messages.
9. Environment-specific configuration is stored outside committed source code.
10. Local exceptions can be logged without exposing technical details to users.

## Known limitations

- Prompt injection cannot be completely prevented through prompt instructions alone.
- A language model can still generate inaccurate or misleading answers.
- Source references demonstrate which passages were retrieved, not that every generated claim is supported.
- The application does not perform a complete semantic verification of generated answers.
- Local Ollama availability and performance depend on the user's computer.
- The application is designed for local development, not hardened multi-user production deployment.
- The application does not include authentication, role-based access control, or user-specific document permissions.
- Local documents may contain sensitive information and should be stored and managed appropriately.
- The application does not provide a guarantee against malicious or malformed documents.
- Error handling and input validation reduce common failures but do not replace a full security review.

## Security boundary

The language model is used only to generate text responses. It is not authorized to execute Python code, run shell commands, access environment variables, or invoke external tools based on document content.

Retrieved documents are treated as evidence rather than trusted instructions.

## Future improvements

- Add automated prompt-injection test cases.
- Add semantic answer-grounding evaluation.
- Add file-upload validation and document sanitization.
- Add authentication and access control before supporting multiple users.
- Perform security testing before any public deployment.
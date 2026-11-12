
import re


MAX_QUESTION_LENGTH = 1000


def validate_question(question):
    """
    Validate user input before sending it to retrieval or the LLM.

    Returns:
        (cleaned_question, error_message)
    """
    if not isinstance(question, str):
        return None, "Please enter your question as text."

    cleaned = question.strip()

    if not cleaned:
        return None, "Please enter a question."

    if len(cleaned) > MAX_QUESTION_LENGTH:
        return (
            None,
            f"Your question is too long. Please keep it under "
            f"{MAX_QUESTION_LENGTH} characters."
        )

    # Reject control characters while allowing normal whitespace.
    if any(ord(char) < 32 and char not in "\n\r\t" for char in cleaned):
        return None, "Your question contains unsupported characters."

    # Reject input consisting only of punctuation or symbols.
    if not re.search(r"[a-zA-Z0-9]", cleaned):
        return None, "Please enter a question containing letters or numbers."

    return cleaned, None

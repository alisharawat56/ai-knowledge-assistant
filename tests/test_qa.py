from unittest.mock import patch
from src.qa import answer_question


def test_empty_question():
    result = answer_question("")

    assert result["error"] == "empty_question"
    assert result["sources"] == []
    assert result["answer"] == "Please enter a question."


def test_whitespace_question():
    result = answer_question("   ")

    assert result["error"] == "empty_question"


@patch("src.qa.retrieve_documents")
def test_unsupported_question(mock_retrieve):
    mock_retrieve.return_value = ([], [])

    result = answer_question("How do I bake sourdough bread?")

    assert result["error"] is None
    assert result["sources"] == []
    assert "don't have enough information" in result["answer"]
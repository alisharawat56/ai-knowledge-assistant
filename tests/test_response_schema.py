
from src.response_schema import validate_response


def test_valid_response():
    source = {
        "source_label": "S1",
        "document_name": "data_structures.md",
        "title": "Data Structures",
        "text": "Python lists are mutable.",
        "chunk_id": "chunk123",
    }

    response = {
        "answer": "Lists are mutable [S1].",
        "sources": [source],
        "insufficient_evidence": False,
        "limitations": [],
    }

    is_valid, errors = validate_response(response, [source])

    assert is_valid is True
    assert errors == []


def test_rejects_fake_source():
    retrieved_source = {
        "source_label": "S1",
        "document_name": "data_structures.md",
        "title": "Data Structures",
        "text": "Python lists are mutable.",
        "chunk_id": "chunk123",
    }

    fake_source = {
        "source_label": "S2",
        "document_name": "fake_document.md",
        "title": "Fake Document",
        "text": "This passage was not retrieved.",
        "chunk_id": "fake456",
    }

    response = {
        "answer": "This is an answer [S2].",
        "sources": [fake_source],
        "insufficient_evidence": False,
        "limitations": [],
    }

    is_valid, errors = validate_response(
        response,
        [retrieved_source],
    )

    assert is_valid is False
    assert any("does not match a retrieved document" in e for e in errors)


def test_rejects_invalid_citation():
    source = {
        "source_label": "S1",
        "document_name": "data_structures.md",
        "title": "Data Structures",
        "text": "Python lists are mutable.",
        "chunk_id": "chunk123",
    }

    response = {
        "answer": "Lists are mutable [S9].",
        "sources": [source],
        "insufficient_evidence": False,
        "limitations": [],
    }

    is_valid, errors = validate_response(response, [source])

    assert is_valid is False
    assert any("citations" in e for e in errors)

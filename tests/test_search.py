from unittest.mock import patch
import pytest

from src.search import retrieve_documents


@patch("src.search.DATABASE_PATH")
def test_missing_database(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(FileNotFoundError):
        retrieve_documents("What is Python?")
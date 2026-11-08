import requests
import pytest
from unittest.mock import patch

from src.ollama_client import generate_response, OllamaError


@patch("src.ollama_client.requests.post")
def test_failed_api_request(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError(
        "Ollama is unavailable"
    )

    with pytest.raises(OllamaError):
        generate_response("Explain Python.")
import os
import sys
from unittest.mock import patch

# Ensure backend directory is in sys.path for app imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.routes.query.generate_answer")
@patch("app.api.routes.query.retrieve")
def test_query_happy_path(mock_retrieve, mock_generate):
    mock_retrieve.return_value = [
        {"text": "Paris is the capital of France.", "source": "geo.txt", "distance": 0.1}
    ]
    mock_generate.return_value = "Paris is the capital of France. [geo.txt]"

    response = client.post("/query", json={"question": "What is the capital of France?"})
    assert response.status_code == 200
    body = response.json()
    assert "Paris" in body["answer"]
    assert "geo.txt" in body["sources"]


def test_query_invalid_input():
    # Empty question should fail validation (HTTP 422 Unprocessable Entity)
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 422

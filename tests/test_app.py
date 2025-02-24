from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
import pytest
import requests

# Initialize the TestClient
client = TestClient(app)

# Test the homepage endpoint
def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test the chat endpoint with valid input
def test_chat_valid_input():
    test_message = {"message": "Hello, AI!"}
    response = client.post("/chat", json=test_message)
    assert response.status_code == 200
    assert "message" in response.json()

# Test the chat endpoint with missing message
def test_chat_missing_message():
    test_message = {}  # No message provided
    response = client.post("/chat", json=test_message)
    assert response.status_code == 400
    assert response.json() == {"error": "Message is required"}

# Test the chat endpoint with Ollama API failure (mocked)
def test_chat_ollama_api_failure(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Mocked API failure")

    # Monkeypatch the requests.post method to simulate an API failure
    monkeypatch.setattr("requests.post", mock_post)

    test_message = {"message": "Hello, AI!"}
    response = client.post("/chat", json=test_message)
    assert response.status_code == 500
    assert response.json() == {"error": "Failed to process the request"}
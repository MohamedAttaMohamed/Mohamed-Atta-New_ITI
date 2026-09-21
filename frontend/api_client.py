import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def ask_question(question: str, timeout: int = 60) -> dict:
    """
    Call the backend /query endpoint.
    Returns {"answer": str, "sources": list[str]} or raises requests.RequestException.
    """
    url = f"{API_BASE_URL}/query"
    response = requests.post(
        url,
        json={"question": question},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def check_health() -> bool:
    """
    Call the backend /health endpoint.
    Returns True if health status is ok, False otherwise.
    """
    try:
        url = f"{API_BASE_URL}/health"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

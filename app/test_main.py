from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

@patch("main.client.chat.completions.create")
def test_summarize_contract(mock_create):
    mock_create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="summary"))],
        usage=MagicMock(prompt_tokens=10, completion_tokens=5),
    )
    r = client.post("/summarize", json={"text": "synthetic note"})
    assert r.status_code == 200
    assert "summary" in r.json()


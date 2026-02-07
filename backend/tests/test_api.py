from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_dmg_reference():
    payload = {
        "player_id": "alpha",
        "message": "The rogue wants to hide in dim light behind the pillar.",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "DMG reference" in data["reply"]
    assert data["conversation_id"] == "party-alpha"

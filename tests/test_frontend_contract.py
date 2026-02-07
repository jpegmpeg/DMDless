from pathlib import Path


def test_frontend_contains_expected_ids():
    html = Path("frontend/index.html").read_text(encoding="utf-8")
    assert "id=\"playerId\"" in html
    assert "id=\"message\"" in html
    assert "id=\"send\"" in html
    assert "id=\"response\"" in html


def test_frontend_points_to_chat_endpoint():
    js = Path("frontend/app.js").read_text(encoding="utf-8")
    assert "/api/chat" in js

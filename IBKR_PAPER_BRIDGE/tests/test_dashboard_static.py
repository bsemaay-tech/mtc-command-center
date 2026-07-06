from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from bridge.app import create_app


def test_dashboard_core_static_contract():
    root = Path("IBKR_PAPER_BRIDGE/bridge/static")
    html = (root / "index.html").read_text(encoding="utf-8")
    css = (root / "app.css").read_text(encoding="utf-8")
    js = (root / "app.js").read_text(encoding="utf-8")

    assert "Overview" in html
    assert "Trading" in html
    assert "Strategy & Risk" in html
    assert "Journal" in html
    assert "LLM" in html
    assert "System" in html
    assert "#0d1117" in css
    assert "innerHTML" not in js
    assert "textContent" in js
    assert "decisionDrawer" in html


def test_dashboard_root_serves_html():
    client = TestClient(create_app())
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Crypto Paper Bridge" in response.text

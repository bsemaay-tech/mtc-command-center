from __future__ import annotations

from fastapi.testclient import TestClient

from bridge.app import create_app


def test_api_status_config_state_and_snapshot_roundtrip():
    client = TestClient(create_app())

    status = client.get("/api/status").json()
    assert status["state"] == "DISARMED"
    assert status["network"] == "testnet"
    state_version = status["state_version"]

    config = client.get("/api/config").json()
    assert config["broker"]["coin"] == "BTC"

    stale = client.post("/api/arm", headers={"X-Confirm": str(state_version + 1)})
    assert stale.status_code == 409

    armed = client.post("/api/arm", headers={"X-Confirm": str(state_version)})
    assert armed.status_code == 200
    assert armed.json()["state"] == "ARMED"

    disarmed = client.post("/api/disarm")
    assert disarmed.status_code == 200
    assert disarmed.json()["state"] == "DISARMED"

    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    assert killed.json()["state"] == "KILLED"

    snapshot = client.get("/api/snapshot").json()
    assert snapshot["status"]["state"] == "KILLED"
    assert snapshot["bars"]["bars"] == []


def test_ws_pushes_snapshot_on_connect():
    client = TestClient(create_app())

    with client.websocket_connect("/ws") as ws:
        message = ws.receive_json()

    assert message["topic"] == "snapshot"
    assert message["data"]["status"]["mode"] == "paper"


def test_kill_persists_across_restart(tmp_path):
    db_path = tmp_path / "bridge.db"
    first = TestClient(create_app(store_path=db_path))

    killed = first.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    assert killed.json()["state"] == "KILLED"

    restarted = TestClient(create_app(store_path=db_path))
    assert restarted.get("/api/status").json()["state"] == "KILLED"

    acked = restarted.post("/api/kill/ack")
    assert acked.status_code == 200
    assert acked.json()["state"] == "DISARMED"

    after_ack_restart = TestClient(create_app(store_path=db_path))
    assert after_ack_restart.get("/api/status").json()["state"] == "DISARMED"

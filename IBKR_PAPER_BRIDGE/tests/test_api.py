from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from bridge.app import create_app
from bridge.broker.mock import MockBroker, ScriptedOutcome
from bridge.engine.engine import BridgeEngine
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import ActionOutcome
from bridge.store.db import Store


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


def test_status_exposes_deployment_identity_health_and_fresh_timestamp(monkeypatch):
    release_sha = "a" * 40
    monkeypatch.setenv("MTC_BRIDGE_RELEASE_SHA", release_sha)
    monkeypatch.setattr("socket.gethostname", lambda: "srv1856225")
    client = TestClient(create_app())

    first = client.get("/api/status").json()
    second = client.get("/api/status").json()
    snapshot = client.get("/api/snapshot").json()["status"]

    assert first["host_identity"] == "srv1856225"
    assert first["release_sha"] == release_sha
    assert first["service_health"] == "healthy"
    assert datetime.fromisoformat(first["service_start_ts"]).tzinfo == UTC
    assert datetime.fromisoformat(first["status_ts"]).tzinfo == UTC
    assert datetime.fromisoformat(second["status_ts"]) >= datetime.fromisoformat(first["status_ts"])
    assert second["service_start_ts"] == first["service_start_ts"]
    for field in (
        "host_identity",
        "release_sha",
        "service_health",
        "service_start_ts",
        "status_ts",
    ):
        assert snapshot[field]

    client.post("/api/kill?flatten=false")
    assert client.get("/api/status").json()["service_health"] == "halted"


def test_status_release_sha_defaults_to_unknown(monkeypatch):
    monkeypatch.delenv("MTC_BRIDGE_RELEASE_SHA", raising=False)
    assert TestClient(create_app()).get("/api/status").json()["release_sha"] == "unknown"


def test_ws_pushes_snapshot_on_connect():
    client = TestClient(create_app())

    with client.websocket_connect("/ws") as ws:
        message = ws.receive_json()

    assert message["topic"] == "snapshot"
    assert message["data"]["status"]["mode"] == "paper"


def test_ws_connection_stays_open_for_status_broadcasts():
    client = TestClient(create_app())

    with client.websocket_connect("/ws") as ws:
        assert ws.receive_json()["topic"] == "snapshot"
        client.post("/api/disarm")
        message = ws.receive_json()

    assert message["topic"] == "status"
    assert message["data"]["state"] == "DISARMED"


def test_kill_persists_across_restart(tmp_path):
    db_path = tmp_path / "bridge.db"
    first = TestClient(create_app(store_path=db_path))

    killed = first.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    assert killed.json()["state"] == "KILLED"

    restarted = TestClient(create_app(store_path=db_path))
    assert restarted.get("/api/status").json()["state"] == "KILLED"

    acked = restarted.post("/api/kill/ack")
    assert acked.status_code == 409
    assert restarted.get("/api/status").json()["state"] == "KILLED"

    after_ack_restart = TestClient(create_app(store_path=db_path))
    assert after_ack_restart.get("/api/status").json()["state"] == "KILLED"


class _ApiClock:
    def __init__(self):
        self.now = datetime.now(UTC)

    def __call__(self):
        return self.now

    def advance(self, seconds: float):
        self.now += timedelta(seconds=seconds)


def _v9_api(tmp_path):
    clock = _ApiClock()
    path = tmp_path / "kill-api-v9.db"
    store = Store(path, clock=clock)
    try:
        store.initialize(target_schema_version=9)
    except RuntimeError:
        # RED baseline: exercise the predecessor behavior semantically.
        store.initialize(target_schema_version=8)
    store.create_run("kill-api", "dry_run", "testnet", {})
    clock.now = datetime.now(UTC) + timedelta(milliseconds=10)
    store.set_meta("app_state", "ARMED")
    broker = MockBroker(bars=[])
    broker.full_clock = clock
    engine = BridgeEngine(
        run_id="kill-api",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="ARMED",
        clock=clock,
    )
    app = create_app(store_path=path)
    app.state.bridge_engine = engine
    app.state.bridge_store = store
    app.state.bridge_status["state"] = "ARMED"
    return TestClient(app), store, engine, clock


def test_kill_ack_requires_current_x_confirm_and_rejects_unknown(tmp_path):
    client, store, _engine, _clock = _v9_api(tmp_path)
    broker = _engine.broker
    broker.orders.append({
        "cloid": "owned-entry", "oid": 1, "role": "ENTRY", "status": "OPEN",
        "qty": 0.1, "reduce_only": False, "symbol": "BTC", "direction": "LONG",
    })
    store.insert_order(
        cloid="owned-entry", oid=1, group_id="request", order_ref="owned:ENTRY",
        order_json={"symbol": "BTC", "role": "ENTRY"}, decision_uid="owned",
        trade_id=None, role="ENTRY", status="OPEN", qty=0.1,
    )
    broker.scripted_cancel.append(
        ScriptedOutcome(
            ActionOutcome.UNKNOWN, applied=False, reason_code="TIMEOUT"
        )
    )
    broker.partial_query_available = False

    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    version = killed.json()["state_version"]

    assert client.post("/api/kill/ack").status_code == 409
    assert client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version - 1)}
    ).status_code == 409
    rejected = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version)}
    )
    assert rejected.status_code == 409
    assert client.get("/api/status").json()["state"] == "KILLED"


def test_kill_ack_rejects_stale_safe_checkpoint(tmp_path):
    client, _store, _engine, clock = _v9_api(tmp_path)
    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    clock.advance(_engine.full_reconcile_max_age_s() + 1)
    current = client.get("/api/status").json()["state_version"]

    acked = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(current)}
    )
    assert acked.status_code == 409
    assert client.get("/api/status").json()["state"] == "KILLED"


def test_kill_ack_after_fresh_safe_proof_is_disarmed_never_armed(tmp_path):
    client, store, _engine, _clock = _v9_api(tmp_path)
    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    version = killed.json()["state_version"]

    acked = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version)}
    )
    assert acked.status_code == 200
    assert acked.json()["state"] == "DISARMED"
    assert store.get_meta("kill_request_active") is None
    assert store.get_meta("app_state") == "DISARMED"

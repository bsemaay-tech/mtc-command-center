from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from bridge.app import create_app

STATIC_ROOT = Path(__file__).resolve().parents[1] / "bridge" / "static"
REPO_ROOT = Path(__file__).resolve().parents[2]
HELP_JSON = STATIC_ROOT / "help_map.json"

REQUIRED_TEXT_FIELDS = ("id", "plane", "name", "status", "status_detail", "one_liner", "purpose")
REQUIRED_LIST_FIELDS = ("does", "does_not", "boundaries", "safety", "connections", "sources", "technical")


@pytest.fixture(scope="module")
def help_map() -> dict:
    return json.loads(HELP_JSON.read_text(encoding="utf-8"))


def test_dashboard_core_static_contract():
    root = STATIC_ROOT
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
    assert "unpkg.com" not in html
    assert "LightweightCharts" not in js
    assert "createElementNS" in js


def test_dashboard_root_serves_html():
    client = TestClient(create_app())
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Crypto Paper Bridge" in response.text


# --------------------------------------------------------------------------
# Help / System Map
# --------------------------------------------------------------------------


def test_help_page_present_in_shell():
    html = (STATIC_ROOT / "index.html").read_text(encoding="utf-8")

    assert 'data-page="help"' in html
    assert "Help / System Map" in html
    assert 'id="page-help"' in html
    # Legend, the interactive detail target, the flow view and the
    # built-now/still-required view are all part of the required contract.
    assert 'id="helpLegendStatus"' in html
    assert 'id="helpDetail"' in html
    assert 'id="helpFlows"' in html
    assert 'id="helpReadiness"' in html
    assert 'id="helpDetailToggle"' in html


def test_help_page_keeps_static_safety_contract():
    js = (STATIC_ROOT / "app.js").read_text(encoding="utf-8")
    css = (STATIC_ROOT / "app.css").read_text(encoding="utf-8")
    raw_help = HELP_JSON.read_text(encoding="utf-8")

    # Single machine-readable knowledge source, fetched from the existing mount.
    assert "/static/help_map.json" in js
    # No external UI dependency anywhere in the help surface. The SVG namespace
    # URI is a constant identifier, not a network fetch, so it is the one
    # allowed absolute URL.
    external = [
        url
        for url in re.findall(r"https?://[^\s\"')]+", js)
        if url != "http://www.w3.org/2000/svg"
    ]
    assert not external, f"external reference leaked into app.js: {external}"
    assert not re.findall(r"https?://", raw_help), "help knowledge must not reference a remote host"
    assert "@import" not in css and "url(" not in css

    # Accessibility / responsiveness requirements from the Gate-1 contract.
    assert "aria-pressed" in js
    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert "@media (max-width: 780px)" in css


def test_help_knowledge_parses_and_is_internally_consistent(help_map: dict):
    assert help_map["schema_version"] == 1

    plane_ids = {plane["id"] for plane in help_map["planes"]}
    status_ids = {status["id"] for status in help_map["statuses"]}
    kind_ids = {kind["id"] for kind in help_map["connection_kinds"]}
    component_ids = [component["id"] for component in help_map["components"]]

    # Unique component IDs.
    assert len(component_ids) == len(set(component_ids)), "duplicate component id"
    assert {"research", "execution", "exchange", "control"} <= plane_ids
    assert status_ids == {"current_v1", "planned_v2", "separate_gate", "not_deployed"}

    known = set(component_ids)
    for component in help_map["components"]:
        cid = component["id"]
        for field in REQUIRED_TEXT_FIELDS:
            assert component.get(field), f"{cid}: empty required field {field}"
        for field in REQUIRED_LIST_FIELDS:
            assert component.get(field), f"{cid}: empty required list {field}"
        assert component["plane"] in plane_ids, f"{cid}: unknown plane"
        assert component["status"] in status_ids, f"{cid}: unknown status"
        # Valid internal relationship targets.
        for connection in component["connections"]:
            target = connection["to"]
            assert target in known, f"{cid}: dangling connection to {target}"
            assert target != cid, f"{cid}: self-referential connection"
            assert connection["kind"] in kind_ids, f"{cid}: unknown kind {connection['kind']}"
            assert connection["label"].strip(), f"{cid}: unlabelled connection"

    # Every plane is actually populated, so the rendered map has no empty column.
    populated = {component["plane"] for component in help_map["components"]}
    assert populated == plane_ids

    for flow in help_map["flows"]:
        assert flow["steps"], f"{flow['id']}: empty flow"
        for step in flow["steps"]:
            assert step["component"] in known, f"{flow['id']}: dangling step {step['component']}"
            assert step["state"] in {"current", "planned", "blocked"}

    for row in help_map["readiness"]:
        assert row["status"] in status_ids
        assert row["built_now"] and row["still_required"]

    for identity in help_map["identities"]:
        assert identity["component"] in known


def test_help_knowledge_source_paths_exist(help_map: dict):
    """Every cited source path must resolve, so the map cannot rot silently."""
    for component in help_map["components"]:
        for source in component["sources"]:
            assert (REPO_ROOT / source).exists(), f"{component['id']}: missing source {source}"


def test_help_knowledge_covers_gate1_components(help_map: dict):
    required = {
        "state_machine",
        "risk_engine",
        "order_manager",
        "light_reconciler",
        "full_reconciler",
        "store_wal",
        "hyperliquid_exchange",
        "kvm2_vps",
        "quantlens_research",
        "strategy_promotion",
        "dashboard",
    }
    assert required <= {component["id"] for component in help_map["components"]}


def _component(help_map: dict, cid: str) -> dict:
    return next(component for component in help_map["components"] if component["id"] == cid)


def _blob(component: dict) -> str:
    parts = [component["one_liner"], component["purpose"], component["status_detail"]]
    for field in ("does", "does_not", "boundaries", "safety", "technical"):
        parts.extend(component[field])
    parts.extend(connection["label"] for connection in component["connections"])
    return " ".join(parts).lower()


@pytest.mark.parametrize(
    ("component_id", "needles"),
    [
        # Owner decisions: controls are real, but none of them is what a reader
        # might casually assume.
        (
            "dashboard_controls",
            [
                "permission, not an instruction",
                "flatten=false",
                "does not automatically flatten",
                # The current interface has one KILL endpoint, and the engine's
                # schema-dependent path never broad-cancels protective orders.
                "/api/kill?flatten=false",
                "the engine never calls cancel_all()",
                "without schema-v9 kill evidence",
                "only orders classified risk-increasing are cancelled",
                "qualifying reduce-only protection must be proven to remain",
                # DISARM's real behaviour, and the runtime's own fail-safe path.
                "cancels pending entry orders when it is safe to do so",
                "disarm itself automatically as a fail-safe",
            ],
        ),
        (
            "state_machine",
            [
                "not production-hardened",
                "sticky",
                "conditional permission",
                # KILL's schema-dependent behaviour, stated as mechanisms.
                "engine.kill() never calls cancel_all()",
                "without the v9 kill-evidence contract",
                "it cancels nothing and does not flatten",
                "cancels only orders classified risk-increasing",
                "preserves qualifying reduce-only protection",
                "starts a controlled flatten only when flatten was actually requested",
                # ARMED gates entries only; safety work is not gated by it.
                "armed gates new entries and nothing else",
                "while disarmed or killed",
            ],
        ),
        # Deployment truth: uploaded payload only, never a live-dashboard claim.
        ("kvm2_vps", ["not installed", "uploaded payload", "never do so"]),
        # Private access only; port 8790 is never public.
        ("private_access", ["ssh tunnel", "never expose port 8790", "must never, mean opening port 8790"]),
        ("fastapi_backend", ["127.0.0.1", "no login"]),
        # Exchange plane requirements.
        ("api_wallet", ["cannot withdraw", "cancel the protective stop", "still open damaging trades"]),
        ("native_protection", ["not guarantee the fill price", "no new, tighter level"]),
        ("hyperliquid_exchange", ["mock money", "authoritative for exchange facts"]),
        ("mainnet_gate", ["separate", "real money"]),
        # AI boundary: Codex subscription, explicitly not Hermes, zero authority.
        ("codex_assistant", ["is not hermes", "no arm, disarm or kill authority", "read-only analysis package"]),
        ("dashboard_ai_memory", ["is not the repository _ai_memory"]),
        ("repo_ai_memory", ["coding agents"]),
        # Telegram: code exists, verification does not.
        ("notifier_telegram", ["not a control channel", "not verified on the kvm2", "every individual fill"]),
        # Public sites never touch the Bridge.
        ("public_websites", ["never proxies bridge controls", "separate tenants"]),
        # Reconciler disambiguation. Full reconciliation is read-only towards the
        # exchange only; its evidence is canonically hashed, never signed.
        (
            "full_reconciler",
            [
                "read-only",
                "never cancels",
                "canonically hashed",
                "zero exchange-state mutation",
                "not a cryptographic signature",
            ],
        ),
        ("light_reconciler", ["may mutate owned state", "never mutates exchange state at all"]),
        # Research never trades, and a modelled cost is not a realized one.
        (
            "quantlens_research",
            [
                "does not connect to hyperliquid",
                "does not place, modify or cancel any order",
                "models assumed commission",
                "actual fills, realized slippage",
            ],
        ),
        ("strategy_runtime", ["plumbing subject", "does not size anything"]),
        # Narrowing-only is not the same as economically neutral.
        (
            "llm_gate",
            [
                "cannot widen permission",
                "not running today",
                "cannot originate or enlarge an order",
                "suppress or select otherwise permitted trades",
                "both roles are off in the current configuration",
            ],
        ),
        # Owner-operated control is not the only path to DISARMED.
        ("owner", ["automatic fail-safe action", "runtime can never arm itself"]),
        # The map must not oversell its own test suite.
        ("help_map", ["structural and selected-phrase tripwires", "re-verified"]),
        # Subscription path avoids a separate API bill; it is not cost-free.
        ("codex_assistant", ["separate api bill", "usage limits and terms"]),
    ],
)
def test_help_knowledge_truth_statements(help_map: dict, component_id: str, needles: list[str]):
    """Load-bearing truth claims must survive future edits of the map."""
    blob = _blob(_component(help_map, component_id))
    for needle in needles:
        assert needle.lower() in blob, f"{component_id}: lost truth statement {needle!r}"


def test_help_knowledge_pins_contested_status_values(help_map: dict):
    """Status labels that were argued over must not drift back silently.

    QuantLens is an existing, actively used research component, so it is
    CURRENT V1. Promotion of any research result into the Bridge is a different
    thing and stays behind its own owner gate.
    """
    expected = {
        "quantlens_research": "current_v1",
        "strategy_promotion": "separate_gate",
        "mainnet_gate": "separate_gate",
        "codex_assistant": "planned_v2",
        "kvm2_vps": "not_deployed",
    }
    actual = {
        cid: _component(help_map, cid)["status"] for cid in expected
    }
    assert actual == expected

    # CURRENT V1 on the lab must not be read as "promotion has happened".
    lab = _blob(_component(help_map, "quantlens_research"))
    assert "promotion into the bridge stays behind its own owner gate" in lab


def test_help_flow_step_states_agree_with_component_status(help_map: dict):
    """A flow step may not claim 'current' for a component that does not exist yet."""
    status_by_id = {c["id"]: c["status"] for c in help_map["components"]}
    for flow in help_map["flows"]:
        for step in flow["steps"]:
            status = status_by_id[step["component"]]
            if status in {"planned_v2", "separate_gate", "not_deployed"}:
                assert step["state"] != "current", (
                    f"{flow['id']}: step {step['component']} is {status} "
                    f"but is drawn as current"
                )

    # The specific mapping the review called out.
    blocked_flow = next(flow for flow in help_map["flows"] if flow["id"] == "flow_ai_blocked")
    assistant_step = next(
        step for step in blocked_flow["steps"] if step["component"] == "codex_assistant"
    )
    assert assistant_step["state"] == "planned"


def test_help_knowledge_pins_ai_source_and_onboarding_guards(help_map: dict):
    """The map is canonical Help data, but coding-agent onboarding does not point at it."""
    memory = _component(help_map, "repo_ai_memory")
    edge = next(c for c in memory["connections"] if c["to"] == "help_map")
    assert edge["kind"] == "planned", "coding-agent onboarding does not point at help_map.json"
    assert "canonical ai-readable knowledge source for the help surface is help_map.json" in _blob(
        memory
    )
    assert "live stage handoff.md records reference it historically" in _blob(memory)
    assert "coding-agent onboarding files do not currently direct agents to it" in _blob(memory)

    reverse = next(
        c for c in _component(help_map, "help_map")["connections"] if c["to"] == "repo_ai_memory"
    )
    assert reverse["kind"] == "planned"

    onboarding_paths = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "CONTEXT_MAP.md",
        REPO_ROOT / "DECISIONS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "_AI_MEMORY" / "START_HERE.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "_AI_MEMORY" / "AI_RULES.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "_AI_MEMORY" / "PROJECT_MEMORY.md",
        REPO_ROOT / "IBKR_PAPER_BRIDGE" / "AGENTS.md",
        REPO_ROOT / "mtc_cli" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "00_AGENT_PROTOCOLS" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "02_MTC_BACKTEST" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "08_DASHBOARD_APP" / "AGENTS.md",
        REPO_ROOT / "MTC_COMMAND_CENTER" / "12_PARITY_PINETS" / "AGENTS.md",
    ]
    pointing = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in onboarding_paths
        if path.is_file()
        and "help_map.json" in path.read_text(encoding="utf-8", errors="ignore")
    ]
    assert not pointing, "repo onboarding now points at help_map.json; promote the edge to data"

    handoff = (REPO_ROOT / "IBKR_PAPER_BRIDGE" / "HANDOFF.md").read_text(
        encoding="utf-8", errors="ignore"
    )
    assert "help_map.json" in handoff
    assert "help_map.json retired-KILL-claim correction" in handoff


def test_help_knowledge_avoids_cost_free_and_signature_claims():
    """Two phrasings that overstated the truth must not come back."""
    raw = HELP_JSON.read_text(encoding="utf-8").lower()
    assert "costs nothing extra" not in raw
    assert "signed, immutable" not in raw
    assert "zero mutation" not in raw


def test_help_knowledge_marks_ai_control_link_as_blocked(help_map: dict):
    """The AI->economic-control edge must exist and must be drawn as blocked."""
    assistant = _component(help_map, "codex_assistant")
    blocked = {
        connection["to"]
        for connection in assistant["connections"]
        if connection["kind"] == "blocked"
    }
    assert {"dashboard_controls", "api_wallet"} <= blocked

    blocked_flow = next(flow for flow in help_map["flows"] if flow["kind"] == "blocked")
    assert blocked_flow["steps"][0]["component"] == "codex_assistant"
    assert blocked_flow["steps"][-1]["state"] == "blocked"


def test_help_readiness_covers_every_required_area(help_map: dict):
    areas = {row["area"].lower() for row in help_map["readiness"]}
    for expected in (
        "source implementation",
        "kvm2 deployment",
        "remote security",
        "dashboard v2",
        "phone access",
        "telegram verification",
        "ai assistance",
    ):
        assert expected in areas, f"readiness view is missing {expected!r}"

    deployment = next(row for row in help_map["readiness"] if row["area"] == "KVM2 deployment")
    assert deployment["status"] == "not_deployed"


def test_help_knowledge_is_served_by_static_mount():
    client = TestClient(create_app())
    response = client.get("/static/help_map.json")

    assert response.status_code == 200
    assert "json" in response.headers["content-type"]
    payload = response.json()
    assert payload["doc_id"] == "bridge_help_system_map"
    assert payload["components"]


# --------------------------------------------------------------------------
# Cycle-2 source-truth repairs. Each assertion below was written against a
# specific claim in the inherited map that the source contradicts.
# --------------------------------------------------------------------------


def test_help_knowledge_marks_llm_gate_as_dormant_unwired_scaffolding(help_map: dict):
    """The real gate is never constructed, so it is not a V1 feature.

    ``bridge/app.py`` constructs ``BridgeEngine(...)`` without an ``llm_gate``
    and ``bridge/engine/engine.py`` therefore installs ``NullLLMGate``, whose
    ``check`` always returns SKIPPED. ``LLMGate.refresh_regime`` and
    ``LLMGate.effective_directions`` have no caller anywhere under ``bridge/``.
    Describing the gate as a CURRENT V1 feature that is merely "switched off"
    tells the reader that flipping a YAML switch would turn it on. It would
    not. The converse half of that truth — the ``llm:`` block *is* read, served
    and displayed — is pinned by
    ``test_help_knowledge_separates_llm_config_visibility_from_activation``.
    """
    gate = _component(help_map, "llm_gate")
    blob = _blob(gate)

    assert gate["status"] == "planned_v2", (
        "an unwired gate with no runtime caller is not an operational CURRENT V1 feature"
    )

    for needle in (
        "nullllmgate",
        "does not activate it today",
        "regime_enabled",
        "veto_enabled",
    ):
        assert needle in blob, f"llm_gate: missing dormancy statement {needle!r}"

    # The future-safety boundary must survive the reclassification: an enabled
    # gate would still change outcomes, and still could not create an order.
    assert "cannot originate or enlarge an order" in blob
    assert "suppress or select otherwise permitted trades" in blob

    # Store, logging and directive relationships are planned, not operational.
    kinds = {connection["to"]: connection["kind"] for connection in gate["connections"]}
    assert kinds["store_wal"] == "planned", "nothing writes directives or llm_calls today"
    assert kinds["risk_engine"] == "planned", "no wired path narrows the RiskEngine today"
    assert kinds["dashboard"] == "planned", "no gate output reaches the LLM page today"

    # And the inbound edge must agree: the RiskEngine is not narrowed today.
    inbound = next(
        connection
        for connection in _component(help_map, "risk_engine")["connections"]
        if connection["to"] == "llm_gate"
    )
    assert inbound["kind"] == "planned"

    # The store may not claim to hold records nothing writes.
    store = _component(help_map, "store_wal")
    assert "risk days, directives and events" not in _blob(store), (
        "the directives table exists but has no writer"
    )


def test_help_knowledge_separates_llm_config_visibility_from_activation(help_map: dict):
    """Reading, serving and displaying the ``llm:`` block is not activation.

    ``bridge/api/routes.py`` loads ``config/bridge.yaml``, keeps it on
    ``app.state.bridge_config``, serves it from ``/api/config`` and includes it
    in the dashboard snapshot; ``bridge/static/app.js`` reads
    ``state.snapshot.config`` and renders ``config.llm.veto_enabled`` as the LLM
    page's veto mode. Runtime code therefore demonstrably *does* read the
    ``llm:`` switches. What no runtime path does is construct ``LLMGate``:
    ``bridge/app.py`` builds ``BridgeEngine(...)`` with no ``llm_gate``, so
    ``bridge/engine/engine.py`` installs ``NullLLMGate``. The map must carry
    both halves — visibility and non-activation — without contradiction.
    """
    gate = _component(help_map, "llm_gate")
    blob = _blob(gate)
    raw = HELP_JSON.read_text(encoding="utf-8").lower()

    # The inherited overbroad denials are false against source, anywhere in the
    # map — not merely in the first paragraph that mentions the gate. Checked
    # first so that a run against the inherited wording fails on the defect
    # itself rather than on a missing replacement sentence.
    for banned in (
        "nothing in the running code reads",
        "no code reads those switches",
        "nothing reads those switches",
    ):
        assert banned not in raw, (
            f"{banned!r} is false: bridge/api/routes.py serves config/bridge.yaml "
            "and bridge/static/app.js displays config.llm.veto_enabled"
        )

    # Half one: the read / serve / display path is real and must be stated.
    for needle in (
        "app.state.bridge_config",
        "/api/config",
        "dashboard snapshot",
        "veto_enabled",
    ):
        assert needle in blob, (
            f"llm_gate: configuration visibility not stated ({needle!r}); "
            "routes.py serves the llm: block and app.js displays it"
        )

    # Half two: visibility is not activation, and the null gate is what runs.
    assert "does not activate it today" in blob
    assert "nullllmgate" in blob
    assert "configuration visibility is not activation" in blob, (
        "llm_gate: the distinction must be explicit, not implied"
    )


def test_help_knowledge_separates_skipped_decision_from_llm_artifacts(help_map: dict):
    """A generic ``LLM_SKIPPED`` decision *is* written; LLM artifacts are not.

    ``NullLLMGate.check()`` returns verdict ``SKIPPED`` with reason
    ``llm disabled``. After risk passes, ``BridgeEngine._on_signal`` maps that
    verdict to stage ``LLM_SKIPPED`` and calls ``store.insert_decision(...)``
    with the reason. So "nothing is logged" is false for the LLM stage as a
    whole. What is still true is narrower: no ``directives`` row and no
    ``llm_calls`` row is written. And ``llm_directive_id`` is a column on the
    ``trades`` row — ``bridge/store/db.py`` declares it inside ``CREATE TABLE
    trades`` and ``bridge/engine/orders.py`` passes ``llm_directive_id=None``
    on trade persistence — not a field of a decision row.
    """
    gate = _component(help_map, "llm_gate")
    blob = _blob(gate)
    raw = HELP_JSON.read_text(encoding="utf-8").lower()

    # Negative: whole-stage denials and the wrong-row attribution are false.
    # Checked first so a run against the inherited wording fails on the named
    # defect rather than on a missing replacement sentence.
    for banned in (
        "does not log anything",
        "nothing is written today",
        "every decision records llm_directive_id as null",
    ):
        assert banned not in raw, (
            f"{banned!r} is false: the engine stores a generic LLM_SKIPPED "
            "decision row, and llm_directive_id belongs to trades"
        )

    # Positive: the generic skipped-decision evidence is operational.
    for needle in (
        "llm_skipped",
        "insert_decision",
        "llm disabled",
    ):
        assert needle in blob, (
            f"llm_gate: the generic skipped decision is not stated ({needle!r}); "
            "the engine persists it on every RISK_PASS"
        )

    # Positive: and the genuinely absent artifacts stay named as absent.
    assert "no directive row" in blob
    assert "no model-call row" in blob

    # Positive: llm_directive_id is attributed to the correct row.
    assert "on the trades row, not on the decisions row" in blob, (
        "llm_directive_id is a trades column; the map must not attribute it to "
        "the decisions row"
    )


def test_help_knowledge_store_holds_the_skipped_decision_without_llm_artifacts(
    help_map: dict,
):
    """The Store wording must match the same repair, not only the gate's.

    The ``directives`` and ``llm_calls`` tables genuinely have no writer. But
    the reason offered for that must not be "the gate has no runtime caller":
    ``BridgeEngine`` calls ``self.llm_gate.check(risk.plan)`` on every
    ``RISK_PASS``, and stores the resulting ``LLM_SKIPPED`` decision.
    """
    blob = _blob(_component(help_map, "store_wal"))

    assert "llm_skipped" in blob, (
        "the Store does hold the generic skipped decision row"
    )
    assert "directives and llm_calls tables exist" in blob
    assert "no runtime caller" not in blob, (
        "the null gate is called on every RISK_PASS; what is missing is a "
        "writer for the directives and llm_calls tables"
    )


def test_help_knowledge_describes_the_llm_page_as_partly_config_driven(help_map: dict):
    """The LLM page is not wholly empty: one card is configuration-derived.

    ``renderLlm()`` in ``app.js`` fills the Regime card from
    ``state.status.regime``, the Veto Mode card from
    ``config.llm.veto_enabled``, and a hard-coded Cost card, then renders the
    Directive History table from a literal empty list. Calling the whole page
    empty overstates the gap.
    """
    blob = _blob(_component(help_map, "dashboard"))

    assert "veto_enabled" in blob, (
        "the Veto Mode card is rendered from configuration, not from a gate"
    )
    assert "directive history" in blob, (
        "name the table that is actually empty rather than the whole page"
    )
    for banned in ("renders empty tables", "renders empty placeholder tables"):
        assert banned not in blob, (
            f"{banned!r} overstates the gap: the page already displays "
            "configuration-derived veto state"
        )


def test_help_readiness_does_not_call_the_running_gate_uncalled(help_map: dict):
    """Readiness prose must carry the same corrected distinction."""
    rows = {row["id"]: row for row in help_map["readiness"]}
    built = rows["readiness_source"]["built_now"].lower()

    assert "no runtime caller" not in built, (
        "engine.py calls self.llm_gate.check(...) on every RISK_PASS; what is "
        "absent is any construction of the real LLMGate"
    )
    assert "nullllmgate" in built, (
        "readiness must name what actually runs in place of the real gate"
    )


def test_help_knowledge_describes_dashboard_v1_surface_exactly(help_map: dict):
    """Seven pages, a next-bar UTC time, and no client-side reconnect.

    ``index.html`` carries seven nav buttons: the six original pages plus
    ``data-page="help"``. ``app.js`` renders ``nextBarLabel()`` as ``HH:00
    UTC`` — a time, not a countdown. ``connectWs()`` registers only a
    ``message`` listener, so the snapshot ``ws.py`` sends on connection is the
    only resynchronisation the client ever performs.
    """
    blob = _blob(_component(help_map, "dashboard"))

    # Page count: six originals plus Help, never "six pages total".
    assert "six original pages" in blob
    assert "plus this help page" in blob

    # Next Bar card: a UTC time, not a countdown.
    assert "the next bar countdown" not in blob, "the Next Bar card shows a time, not a countdown"
    assert "next bar's utc time" in blob
    assert "not a live countdown" in blob

    # WebSocket: snapshot on connection, and no automatic reconnect handler.
    assert "whenever the socket reconnects" not in blob, "the client has no reconnect handler"
    assert "full snapshot on connection" in blob
    assert "does not reconnect the websocket automatically" in blob


def test_help_readiness_states_each_gap_in_exactly_one_area(help_map: dict):
    """The Dashboard gap was stated twice; an area row owns its own gaps."""
    rows = {row["id"]: row for row in help_map["readiness"]}
    source_required = rows["readiness_source"]["still_required"].lower()
    dashboard = rows["readiness_dashboard"]
    dashboard_required = dashboard["still_required"].lower()

    for phrase in ("save workflow", "llm page"):
        assert phrase in dashboard_required, f"Dashboard row lost its own gap {phrase!r}"
        assert phrase not in source_required, (
            f"readiness_source duplicates the Dashboard gap {phrase!r}; "
            "each gap belongs to exactly one area row"
        )

    built = dashboard["built_now"].lower()
    assert "six-page" not in built
    assert "six original pages plus this help page" in built


def test_help_knowledge_avoids_repaired_cycle2_phrasings():
    """Four wordings the source contradicts must not return."""
    raw = HELP_JSON.read_text(encoding="utf-8").lower()
    assert "dashboard v1 (six pages)" not in raw
    assert "six-page" not in raw
    assert "next bar countdown" not in raw
    assert "whenever the socket reconnects" not in raw


def test_ai_facing_index_points_at_the_json_without_duplicating_it():
    doc = (REPO_ROOT / "IBKR_PAPER_BRIDGE" / "docs" / "31_HELP_SYSTEM_MAP_INDEX.md").read_text(
        encoding="utf-8"
    )
    help_map = json.loads(HELP_JSON.read_text(encoding="utf-8"))

    assert "bridge/static/help_map.json" in doc
    assert "test_dashboard_static.py" in doc
    # An index, not a copy: it must be far smaller than the source it indexes.
    assert len(doc) < len(HELP_JSON.read_text(encoding="utf-8")) / 2
    # And it must not restate component explanations.
    for component in help_map["components"]:
        assert component["one_liner"] not in doc


def test_ai_facing_index_maintenance_rule_matches_the_repaired_truth():
    """The index's editing rule must not re-teach the claims we just removed.

    Rule 12 tells a future editor to check the constructor rather than the
    class. That is right, but it must not carry the false corollary that
    nothing reads the switches, nor imply that a dormant gate logs nothing.
    """
    doc = (REPO_ROOT / "IBKR_PAPER_BRIDGE" / "docs" / "31_HELP_SYSTEM_MAP_INDEX.md").read_text(
        encoding="utf-8"
    )
    lowered = doc.lower()

    assert "nothing reads" not in lowered, (
        "routes.py serves config/bridge.yaml and app.js displays "
        "config.llm.veto_enabled; the rule must not say nothing reads them"
    )
    assert "/api/config" in lowered, (
        "the rule must state that the configuration is read, served and shown"
    )
    assert "llm_skipped" in lowered, (
        "the rule must not leave a future editor free to write that the "
        "dormant gate logs nothing"
    )

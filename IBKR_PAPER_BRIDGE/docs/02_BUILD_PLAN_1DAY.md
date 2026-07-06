# BUILD PLAN — two days, Opus/Codex (AMENDED 2026-07-06: honest budget per audit consensus —
all 7 auditors flagged the 1-day label; estimates total ~12h before integration friction)

Prereq reading: `00_PREREG.md`, `01_ARCHITECTURE.md`, `05_AUDIT_RESOLUTION.md`. Do NOT redesign;
build to spec. Mock-first so the whole engine is testable without TWS; IBKR adapter is Day 2.
Commit after EVERY task (repo rule: parallel-agent safety). Branch: `feature/ibkr-paper-bridge`
(repo auto-reverts to master between tool calls — use inline
`git checkout <branch>; git add <exact paths>; git commit` in one command).

**Day 1 — mock core (tasks 1-7 + 10a):** acceptance = `pytest IBKR_PAPER_BRIDGE/tests -q` green +
dry-run demo (engine on fixture data, Overview+Trading pages live in browser).
**Day 2 — IBKR hardening + polish (tasks 8, 9, 10b, 11):** acceptance = adapter unit tests green;
P0 smoke only if TWS running AND Barış approves in-session.
**If time runs short, cut in this order:** LLM page → System page → Journal drawer polish →
notifier. NEVER cut: risk tests, state-machine tests, reconciler grace, port allow-list.

| # | Task (est) | Deliverable | Acceptance |
|---|---|---|---|
| 1 | Scaffold (30m) | Tree per §2, requirements.txt, settings.py, empty modules import-clean, `.gitignore` entry | `python -c "import bridge.app"` OK |
| 2 | Types + Store (60m) | types.py pydantic models; db.py schema v2 §7 (decision_uid, perm_id fields, fills, bars, risk_days, meta, indices) + helpers: insert_decision, get_decision_chain(decision_uid), insert_order, update_order_status, insert_fill, create_trade, update_trade_exit, insert_equity, insert_event, get_* | `tests/test_store.py` roundtrip incl. decision-chain reconstruction by decision_uid + schema_version row |
| 3 | MockBroker + fixture (60m) | mock.py per §6.1; `tests/fixtures/AAPL_1h.csv` — builder generates ~2000 bars: pull real AAPL 1h from the QuantLens alpaca bundle (read-only) OR synthesize trending+ranging segments | mock fills deterministic: MKT@next open, SL/TP intra-bar, SL priority |
| 3b | Golden generation (30m) | `tools/generate_golden.py`: run QuantLens engine (read-only) on the FAZ 3B variant AAPL 1h with the SAME bar-alignment policy (RTH 1h, 30-min tail discarded), apply the documented bridge execution transform, emit `tests/fixtures/golden_signals.json` + record `golden_run_id` into strategy YAML | golden file exists; the parity fixture is REAL AAPL 1h bars QuantLens processed — synthetic bars allowed only for MockBroker fill mechanics (audit: Opus F-21) |
| 4 | Strategy port (60m) | keltner_trail_ema8.py + YAML params copied from FAZ 3B artifacts | `test_strategy`: fixture bars → signal timestamps == golden (from 3b) |
| 5 | RiskEngine (45m) | risk.py per §6.3, pure function, incl. gate_results list | `test_risk`: sizing arithmetic, daily-loss reject+DISARM flag, notional clamp, direction intersect (incl. NO_TRADE), qty<1 reject, consecutive-loss stop, cooldown, gate_results ordering |
| 6 | Engine + OrderManager on mock (120m) | engine.py state machine §5 (step-0 fresh position, post-await state gate, preemptive KILL, KILLED persistence), orders.py (trail price-only modify, partial-fill states, PENDING reconciler grace, duplicate-signal guard, stale-data guard, reduce-only close), `NullLLMGate` stub wired NOW so LLM_SKIPPED/fail-open paths are integration-tested before task 9 | `test_engine_dryrun`: full replay → ≥1 complete trade w/ full decision chain; induced reject → pause; naked-position sim → re-protect-then-flatten; same-bar re-delivery (reconnect replay) → exactly one order; DISARM mid-await → no submit; partial-fill + DISARM → children resized; trail modify keeps same order id |
| 7 | API + WS (60m) | routes.py, ws.py per §8 incl. confirm-nonce | httpx TestClient: status/arm/disarm/config roundtrip; WS receives `decision` during replay |
| 8 | IBKRBroker (150m) | ibkr.py per §6.1 AMENDED contract (BarFinalizer w/ session-end force-close + tail-bar discard, delayed-data streaming validation, permId persistence, restart recovery re-protect path, reconnect re-subscribe, port allow-list) + `docs/06_TWS_SETUP.md` checklist (enable API, socket port, **Bypass Order Precautions for API Orders**, trusted IP 127.0.0.1, auto-restart) | Unit: allow-list refuses 7496/4001/custom w/o triple-lock; BarFinalizer fixtures (half-day, session-end, reconnect dup). Integration (TWS paper running): P0 smoke `tools/smoke_p0.py` — connect, account, quote, **bracket transmits with NO TWS popup**, cancel, JSON log — run ONLY with Barış approval |
| 9 | LLM gate (60m) | llm_gate.py: Grok regime (source-block injection mitigation, TTL clamp, expiry hold-then-config-fallback) + Claude veto (async deadline, cost caps, **default OFF**), narrowing-only rule | `test_llm_gate` stubbed HTTP: invalid JSON→config direction, TTL expiry→no silent widen, injection string in source→regime unaffected beyond NO_TRADE, veto path, deadline→LLM_SKIPPED, cost cap→LLM_COST_LIMIT |
| 10a | Dashboard core (Day 1, 120m) | index.html/app.css/app.js — Overview (equity, position, decisions stream, Gate Monitor card w/ empty state "No signal yet + next-bar countdown") + Trading + Strategy&Risk config pages; dark theme; lightweight-charts CDN; WS-driven w/ snapshot-on-open resync; ARM/DISARM/KILL flows (KILL never nonce-blocked); textContent-only rendering | Manual: dry-run replay visible live (equity draws, decisions stream, gate card colors); screenshot into `docs/screenshots/` |
| 10b | Dashboard rest (Day 2, 90m) | Journal (trade table + decision-chain drawer via decision_uid) + LLM + System pages | Journal drawer shows full SIGNAL→RISK→LLM→orders→fills chain for a mock trade |
| 11 | Notifier + polish + docs (45m) | notify.py per §6.7 (Telegram, fail-silent); README quickstart (run TWS → configure API → `python -m bridge.app`), known gaps in `docs/03_STATUS.md` | notifier unit test w/ stubbed HTTP (disabled when env unset; never raises); fresh-clone quickstart works in dry-run mode |

Follow-ups after build day (separate sessions, Barış-gated): P0 smoke live (task 8 integration),
then PREREG gates P1→P2→P3.

Builder guardrails:
- No trading-logic creativity: strategy rules come from FAZ 3B artifacts verbatim; when ambiguous,
  write the ambiguity into `docs/03_STATUS.md` and choose the close-confirmed variant (§6.2).
- Never touch `MTC_COMMAND_CENTER/` except read-only param lookup (task 3/4).
- Never run anything against a broker without explicit Barış approval in-session.
- Keep everything ASCII-safe UTF-8; Windows: set `PYTHONUTF8=1` in run docs.

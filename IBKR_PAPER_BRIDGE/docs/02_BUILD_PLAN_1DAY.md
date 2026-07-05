# BUILD PLAN — one day, Opus/Codex

Prereq reading: `00_PREREG.md`, `01_ARCHITECTURE.md`. Do NOT redesign; build to spec.
Order matters: mock-first so the whole engine is testable without TWS; IBKR adapter is task 8,
not task 1. Commit after EVERY task (repo rule: parallel-agent safety). Branch:
`feature/ibkr-paper-bridge` (repo auto-reverts to master between tool calls — use inline
`git checkout <branch>; git add <exact paths>; git commit` in one command).

Global acceptance for the day: `pytest IBKR_PAPER_BRIDGE/tests -q` green + dry-run mode demo
(engine on fixture data, dashboard live in browser) + P0 smoke against TWS paper if TWS is running
(if not, P0 is a follow-up session — do not block the day on it).

| # | Task (est) | Deliverable | Acceptance |
|---|---|---|---|
| 1 | Scaffold (30m) | Tree per §2, requirements.txt, settings.py, empty modules import-clean, `.gitignore` entry | `python -c "import bridge.app"` OK |
| 2 | Types + Store (45m) | types.py pydantic models; db.py schema §7 + insert/query helpers | `test_store` roundtrip (write decision/trade/event, read back) |
| 3 | MockBroker + fixture (60m) | mock.py per §6.1; `tests/fixtures/AAPL_1h.csv` — builder generates ~2000 bars: pull real AAPL 1h from the QuantLens alpaca bundle (read-only) OR synthesize trending+ranging segments | mock fills deterministic: MKT@next open, SL/TP intra-bar, SL priority |
| 4 | Strategy port (60m) | keltner_trail_ema8.py + YAML params copied from FAZ 3B artifacts; golden signal list | `test_strategy`: fixture bars → signal timestamps == golden |
| 5 | RiskEngine (45m) | risk.py per §6.3, pure function | `test_risk`: sizing arithmetic, daily-loss reject+DISARM flag, notional clamp, direction intersect (incl. NO_TRADE), qty<1 reject |
| 6 | Engine + OrderManager on mock (90m) | engine.py state machine §5, orders.py incl. trail modify, reconciler | `test_engine_dryrun`: full replay on fixture → ≥1 complete trade in DB with full decision chain; induced reject → DISARM; naked-position sim → flatten |
| 7 | API + WS (60m) | routes.py, ws.py per §8 incl. confirm-nonce | httpx TestClient: status/arm/disarm/config roundtrip; WS receives `decision` during replay |
| 8 | IBKRBroker (90m) | ibkr.py per §6.1 notes (delayed data type 3, keepUpToDate bar-close detection, bracket, reconnect backoff, live-port refusal) | Unit: live-port refusal raises w/o ack env. Integration (needs TWS paper running): P0 smoke script `tools/smoke_p0.py` — connect, account, quote, place+cancel bracket, JSON log — run ONLY with Barış approval |
| 9 | LLM gate (60m) | llm_gate.py: Grok regime + Claude veto, strict-JSON parse, TTL, min-confidence, fail-open, narrowing-only rule | `test_llm_gate` with stubbed HTTP: invalid JSON→BOTH, expired TTL→BOTH, veto path, timeout→LLM_SKIPPED |
| 10 | Dashboard (150m) | index.html/app.css/app.js per §9 — all 6 pages, dark theme, lightweight-charts CDN, WS-driven, ARM/DISARM/KILL flows w/ modals | Manual: dry-run replay visible live (equity curve draws, decisions stream, journal drawer shows full chain); screenshot into `docs/screenshots/` |
| 11 | Polish + docs (30m) | README quickstart (run TWS → configure API → `python -m bridge.app`), record known gaps in `docs/03_STATUS.md` | fresh-clone quickstart works in dry-run mode |

Follow-ups after build day (separate sessions, Barış-gated): P0 smoke live (task 8 integration),
then PREREG gates P1→P2→P3.

Builder guardrails:
- No trading-logic creativity: strategy rules come from FAZ 3B artifacts verbatim; when ambiguous,
  write the ambiguity into `docs/03_STATUS.md` and choose the close-confirmed variant (§6.2).
- Never touch `MTC_COMMAND_CENTER/` except read-only param lookup (task 3/4).
- Never run anything against a broker without explicit Barış approval in-session.
- Keep everything ASCII-safe UTF-8; Windows: set `PYTHONUTF8=1` in run docs.

# Execution-surface inventory — what exists today and what data it can show (wayfinder #99)

**Scope:** read-only inventory of our own execution-side surfaces and data: the Dashboard V2
prototype, the KVM2 runkit owner dashboard, the observability toolkit (package 5a), the Bridge's
live read endpoints/API, and which evidence-schema fields (intended/accepted/filled/authorized)
actually have a data source today. No code was run; no server was started. All citations are
against `IBKR_PAPER_BRIDGE/` and `MTC_COMMAND_CENTER/` at master `ab35ca66c574f051ae7f01173eafc1145a3f72cf`
unless a specific other commit/branch is named, from worktree `C:\WFR5B` on branch
`research/execution-surface-inventory`.

**Cross-checked against:** `research/bridge-plan-delta` (ticket #87, worktree `C:\WFB1`), a prior
read-only Gate-1 fold research doc comparing the deployed Bridge against the V2A/V2B plan. That
doc's §2 (reconciliation/evidence-schema) and §6/§7 (per-package MISSING/DIVERGES verdicts) are
treated as settled prior art here and re-verified directly against `db.py`/`routes.py` rather than
re-derived from scratch. Its file is not yet on `master` — it lives only on that research branch —
so this doc quotes and re-confirms the load-bearing lines rather than assuming the reader has it.

---

## 1. Headline finding

There are **two different "dashboards"** in this repo and they are commonly conflated:

1. **The V1 dashboard (`bridge/static/`)** — a real, already-deployed, already-live page served by
   the running Bridge FastAPI process itself. This is what the owner actually sees when he runs
   the KVM2 runkit launcher. It already renders equity, P&L, a gate monitor, a decision stream,
   positions, working orders, a trades journal with a per-trade decision-chain drawer, LLM
   regime/veto/cost panels, and a system/events page — all from data the Bridge already stores and
   already serves over one existing endpoint (`/api/snapshot`) plus a live WebSocket (`/ws`).
2. **The Dashboard V2 prototype (`IBKR_PAPER_BRIDGE/dashboard_v2_prototype/`)** — a static,
   **fixture-only**, file:// HTML mockup built 2026-08-17/18 to make the *proposed* V2 multi-worker
   vocabulary visible (worker identity tuple, Portfolio Guardian veto tiers, desired/accepted/actual
   three-layer model). It has no server, no live data, no network calls of any kind, and nothing in
   it is wired to the real Bridge. Its own README says so explicitly (quoted in §3).

**The "KVM2 runkit owner dashboard" is #1, not #2.** `Start-BridgeDashboard.cmd` /
`Open-BridgeDashboard.ps1` (see §2) do not build or serve a dashboard — they open a pinned SSH
tunnel to the already-running Bridge on the VPS and point a browser at it. What the owner sees
through that tunnel is the V1 page in §1, current as of whatever the deployed Bridge process is
running.

For evidence-schema fields specifically: **intended, accepted, and filled all have real,
already-queried data sources today** (decisions/orders/fills/trades tables in `bridge/store/db.py`,
partly already exposed over REST). **Authorized has none** — there is no Guardian, no Risk
Allocator, no separate authorization step anywhere in `bridge/`; the Bridge computes and submits
its own order quantity in one call (`bridge/engine/risk.py:380-393`), so nothing distinguishes an
"authorized" amount from an "intended" one. This matches `research/bridge-plan-delta`'s finding
verbatim and is re-confirmed directly against the schema in §4 below.

---

## 2. The KVM2 runkit owner dashboard — located, and what it actually is

**Not on `master`.** `git log --all` finds it only on branch `codex/rp7-r1-r4-repair-20260815`
(commit `cd72ea9c`, "feat(runkit): one-click cmd wrapper for the dashboard launcher", 2026-08-17,
not merged). Path: `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_RUNKIT/`:

- `Start-BridgeDashboard.cmd` — 5-line `.cmd` wrapper that runs the `.ps1` beside it with
  `-ExecutionPolicy Bypass` (Windows opens double-clicked `.ps1` files in an editor, not a shell;
  this exists purely to fix that).
- `Open-BridgeDashboard.ps1` (`Open-BridgeDashboard_v4.ps1` per its own header) — a pinned,
  agent-only SSH tunnel opener. Key facts read directly from the script:
  - Opens `ssh -L 127.0.0.1:18790:127.0.0.1:8790` to `baris@152.239.123.231` (the KVM2 host),
    using only an already-loaded Windows ssh-agent identity matched against one hardcoded expected
    fingerprint (`SHA256:8b6bl/srDevzQ1rycf9FcQFgZXblSMddqak/9JsHBC8`) — it opens no key file itself
    and stores no password/passphrase/private-key material.
  - Refuses to proceed (fails closed, with a plain-language message) if: OpenSSH binaries are
    missing, `known_hosts` pin is missing, ssh-agent isn't running, the expected fingerprint isn't
    loaded, the local port is already busy, the tunnel process exits early, or the far end doesn't
    answer HTTP 200 with `<title>Crypto Paper Bridge</title>` within ~10s.
  - On success, opens the default browser at `http://127.0.0.1:18790/`.
  - The remote loopback port `8790` and the page title `Crypto Paper Bridge` are the Bridge's own
    FastAPI static app (`bridge/app.py:94`, `bridge/static/index.html:6`) — confirmed by grep: the
    only place `<title>Crypto Paper Bridge</title>` exists in the repo is `bridge/static/index.html`.

**Conclusion:** the KVM2 runkit is a secure remote-access wrapper around the V1 dashboard described
in §1, not a separate dashboard implementation. There is no dashboard-specific code in this
directory; the entire "dashboard" is whatever `bridge/static/` renders.

---

## 3. Dashboard V2 prototype — located, contents, and reusable UI vocabulary

Path: `IBKR_PAPER_BRIDGE/dashboard_v2_prototype/` (on `master`). Files: `index.html` (142 lines),
`app.js` (845 lines), `app.css` (725 lines), `README.md`, `fixtures/{workers.json, intents.json,
market_context.json, data.js, build_data_js.py}`. Scope source cited in its own README:
`MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE3_DASHBOARD_V2_PROTOTYPE_2026-08-18.md` (present on
`master`).

**What it is, in its own words** (`README.md`): *"A standalone, fixture-backed, read-only prototype
of the proposed V2 multi-worker dashboard... There is no server, no build step and no install. The
page works offline by construction: all data is embedded locally and no request of any kind leaves
the page."* Every fixture file repeats: *"SYNTHETIC FIXTURE DATA. There is no live bridge, no
exchange connection and no worker process behind these values."*

**Five views:** Overview (worker table, Guardian panel, shared-infra REST/WS budget panel),
Worker detail (7-field identity tuple, health/freshness, block reasons, per-worker ledger,
account-label), Market context (context-only, explicitly non-actionable), Three layers
(desired/accepted/exchange-truth swim-lanes per intent, with deliberately-included divergence
cases: superseded stop, freshness reject, Guardian veto, partial fill, `UNKNOWN_SUBMISSION`,
blocked duplicate), Phone monitor (390px small-screen layout).

**Vocabulary confirmed directly in `fixtures/workers.json`** (read in full): worker identity fields
`worker_id`, `strategy_id`, `symbol`, `timeframe`, `strategy_version`, `config_hash`,
`account_label`; a `health` block (`window_state`, `last_evidence_ts`, `last_bar_ts`); a `blocks`
array with `source`/`guardian_tier`/`reason_code`/`detail`/`scope`/`lift`; a `position` block
(`side`/`qty`/`avg_entry`/`mark`); a per-worker `ledger` (`realized_pnl_today`, `ledger_key`). The
Guardian object carries `state`, `global_halt`, three named `veto_tiers` (PER-ORDER VETO /
PER-WORKER PAUSE / GLOBAL HALT), and explicit `mutate_note`/`fail_closed_note` text (veto-not-mutate,
fail-closed-to-no-new-entries-only, exits never blocked).

**Which pieces are reusable UI vocabulary with zero new backend work vs which wait on V2 packages:**

| Prototype element | Reusable today? | Why |
|---|---|---|
| Panel/tab/pill visual language (`app.css`, dark-panel styling) | **Yes** — its own README says it borrowed this *from* the V1 dashboard as reference, so it's already consistent with what's live | Cosmetic only |
| "Three layers: desired / accepted / exchange-truth" labeling convention | **Yes, as a display convention** — could be applied to real columns from `decisions`/`orders`/`fills` (§4) today, dropping the fourth "authorized" column | The *label* is free; the *data* for layer 2 (accepted) needs a new read endpoint, not new capture (§4) |
| Worker identity tuple, per-worker ledger, per-worker window state | **No** — no worker concept exists in the running Bridge (`bridge/settings.py:31-37` is a single hardcoded account/wallet pair; `grep -r "worker_id\|WorkerIdentity"` across `bridge/` returns no real hits) | Requires WP-V2A-02 (worker identity) first |
| Portfolio Guardian panel, veto tiers, block reasons of Guardian origin | **No** — no `Guardian` class or `RiskBucket` type exists anywhere in `bridge/` | Requires WP-V2B-01 |
| Shared IP/WS budget panel | **No new capture needed for the raw numbers** (Hyperliquid's own published limits), but no allocator/registry exists to report *usage* against them | Requires the central allocator (P1 B.8) |
| Market-context (price-only, non-actionable) cards | **Partially** — `/api/bars` already serves real OHLCV per the Bridge's single configured symbol; multi-symbol context cards would need the Bridge to track more than one symbol, which it doesn't today (single-strategy, single-coin) | Data source exists for one symbol only |

---

## 4. Evidence-schema fields — what has a data source today

Directly re-read from `bridge/store/db.py` (not taken on the delta doc's word alone):

- **`decisions` table** (`db.py:942-951`) — columns `decision_uid, run_id, ts, coin, stage,
  trade_id, payload_json, payload_version`. This is the **intended** stage. **Already exposed** via
  `GET /api/decisions` (`bridge/api/routes.py:175-178`, calls `store.get_decisions`,
  `db.py:9824-9834`) and bundled into `GET /api/snapshot`.
- **`orders` table** (`db.py:953-968`) — columns `cloid, oid, group_id, order_ref, order_json,
  decision_uid, trade_id, role, status, qty, filled_qty, avg_fill_px, ts_submit, ts_last`. This is
  the **accepted/submitted** stage. **Stored, but not exposed as history.** `GET /api/orders`
  (`routes.py:165-168`) does *not* read this table — it calls `engine.broker.open_orders()`, i.e.
  only currently-open live orders from the broker adapter, not the persisted historical `orders`
  table. There is no `store.get_orders()` method and no route reads the `orders` table at all. This
  is the one clean, well-scoped gap: the data already exists and is durable, but reaching it today
  requires direct SQLite access (e.g. via the observability toolkit, §5), not a REST call.
- **`fills` table** (`db.py:970-979`) — columns `fill_id, cloid, decision_uid, fill_ts, qty, px,
  fee, funding`. Per-fill granularity for the **filled** stage. **No store method, no route, no
  API exposure at all** — confirmed by grep: no `get_fills` anywhere in `db.py`, no `/api/fills` in
  `routes.py`.
- **`trades` table** (`db.py:981-1007`) — an already-computed aggregate: `expected_px, entry_px,
  entry_ts, exit_px, exit_ts, exit_reason, pnl, slippage_bps_entry, risk_dollars, risk_pct,
  leverage, sl_initial, tp_initial`. **`slippage_bps_entry` is a real column, already populated by
  the write path** — entry-side slippage attribution exists without any new capture code. **Already
  exposed** via `GET /api/trades` (`routes.py:170-173`, `store.get_trades`, `SELECT * FROM trades
  ORDER BY trade_id DESC LIMIT ?`) and bundled into `/api/snapshot`. There is **no symmetric
  `slippage_bps_exit` column** — exit-side slippage is not captured anywhere, so slippage
  attribution is one-sided today.
- **"Authorized" stage** — **no table, no column, no concept**. Confirmed independently of the
  delta doc: `bridge/engine/risk.py:380-393` computes `raw_qty = risk_dollars / stop_distance` and
  the notional/leverage gates in the same call that produces the order the Bridge submits — there
  is no intermediate "here is what was authorized" record distinct from "here is what was
  intended," because nothing sits between intent and submission to authorize anything. A genuine
  4-stage intended/authorized/accepted/filled divergence report cannot be built until a Guardian or
  equivalent authorization step exists and persists its own decision (WP-V2A-03 / WP-V2B-01,
  per `research/bridge-plan-delta` §6–§7, both still MISSING as of that doc's read).

**What this means concretely for a "minimum dashboard today":** a 3-column intended/accepted/filled
view is buildable with **zero new capture** — the columns are `decisions.payload_json` (intended),
`orders.qty/filled_qty/avg_fill_px/status` (accepted — needs one small new read path, not new
storage), and `trades.entry_px/exit_px/slippage_bps_entry` (filled, partially pre-joined already).
A 4-column view including "authorized" is not buildable at all today at any effort level, because
the data literally does not exist yet — that column waits on a Guardian, full stop.

---

## 5. Observability toolkit (package 5a) — located, and its actual shape

Path: `IBKR_PAPER_BRIDGE/tools_v2/observability/` (on `master`). Scope source:
`MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE5A_OBSERVABILITY_TOOLKIT_2026-08-18.md` (present on
`master`). Branch noted in its own README: `feature/bridge-v2-package5a`.

Contents, per its own README (quoted, since this is the load-bearing scope statement):

- `export_audit_pack.py` — *"Stdlib-only, **read-only** CLI that builds one Markdown audit/export
  pack from an **explicitly supplied** bridge-format SQLite store path... schema version from
  `meta`, table list with row counts, `app_state` and key meta values, bounded most-recent
  orders/events... Never invents data. Never a default path."*
- `fixtures/build_fixture_store.py` — builds a synthetic v4-shaped SQLite store for testing only;
  no real `.db` is committed.
- `readiness_checklist.html` — a standalone, static, in-page-only pre-flight checklist; *"this page
  controls nothing."*
- `CHAOS_DRILLS_DESIGN.md` — **design only**, explicitly deferred: *"Chaos-drill implementation is
  deferred. Only the design document ships here."*
- `tests/test_export_audit_pack.py` — pytest coverage for the export tool.

**Boundaries, per the README:** no bridge code is imported by any tool here, no network, the store
path is always caller-supplied and opened SQLite read-only (`mode=ro`) — **there is no default live
path**, so this tool cannot point itself at the running Bridge's actual database without an operator
explicitly supplying that path each time. It produces a one-shot Markdown report, not a live or
refreshable dashboard view, and it approves/authorizes nothing.

**Conclusion:** package 5a is real, tested, read-only tooling for offline/ad-hoc store inspection
(e.g. a health/row-count sanity check before a schema-version rehearsal) — it is not a live
dashboard data source and was never scoped to become one. It is a useful escape hatch for reaching
the `orders`/`fills` tables that have no REST route (§4), but only as a manual, one-shot export
against an explicitly named store file, not as something a dashboard could poll.

---

## 6. Bridge read endpoints/API — complete current surface

Read directly from `IBKR_PAPER_BRIDGE/bridge/api/routes.py` (258 lines, read in full):

| Route | Method | Reads from | Notes |
|---|---|---|---|
| `/api/status` | GET | `engine.status()` + in-memory `app.state.bridge_status` | Includes `window_status()` (evidence-derived RUNNING/DOWN/INTERRUPTED/RESET) |
| `/api/config` | GET | `app.state.bridge_config` (loaded from `config/bridge.yaml`) | |
| `/api/bars` | GET | `store.get_bars(n)` | OHLCV, default last 300 |
| `/api/snapshot` | GET | `make_snapshot()` — bundles status, config, live positions/orders, `trades`(50), `decisions`(50), `events`(100), `latest_gates`, `equity`, `bars`(300) | **This is the one call the V1 dashboard actually uses on load** (`bridge/static/app.js:31`) |
| `/api/gates/latest` | GET | `store.get_latest_gates()` | |
| `/api/positions` | GET | `engine.broker.positions()` | Live broker state, not stored history |
| `/api/orders` | GET | `engine.broker.open_orders()` | **Live open orders only — not the `orders` table** (§4 gap) |
| `/api/trades` | GET | `store.get_trades(limit)` | Full `trades` row incl. `slippage_bps_entry` |
| `/api/decisions` | GET | `store.get_decisions(trade_id)` | Full `decisions` row incl. decoded `payload_json` |
| `/api/equity` | GET | `store.get_equity()` | |
| `/api/events` | GET | `store.get_events(severity)` | |
| `/api/runs/{run_id}` | GET | `store.get_run(run_id)` | 404 if absent |
| `/ws` (WebSocket, per `bridge/api/ws.py`) | — | broadcast hub, bumped on `/api/config`\|`arm`\|`disarm`\|`kill`\|`kill/ack` | Push channel the V1 page also opens (`app.js:241`) |

Write/action routes exist too (`PUT /api/config`, `POST /api/arm`, `POST /api/disarm`,
`POST /api/kill`, `POST /api/kill/ack`) but are out of scope for this read-only inventory beyond
noting `_require_confirm` (`routes.py:227-230`) is a stale-`state_version` confirmation header, not
authentication — consistent with `research/bridge-plan-delta` §7 (V2B-06: no WebAuthn/step-up
auth anywhere in `routes.py`).

**No `/api/fills` route, no `/api/orders/history` or equivalent route exists.** These are the only
two gaps in the read surface relative to what's in the schema (§4).

---

## 7. What a minimum dashboard could show TODAY with zero new plumbing

Everything below is already computed, already stored, and already served by an existing GET route
— a new dashboard page could be built purely as a *view* over `/api/snapshot` (or the individual
routes) with no backend change at all:

- Bridge state machine: ARMED/DISARMED/KILLED, evidence-derived window state (RUNNING/DOWN/
  INTERRUPTED/RESET with `stale_after_s`), connection/mode/regime pills (`/api/status`).
- Live equity curve and day P&L (`/api/equity`, already rendered in V1 Overview).
- Gate monitor / decision stream — the most recent gate evaluation and decision payloads
  (`/api/gates/latest`, `/api/decisions`).
- A trades journal with entry/exit price, entry-side slippage in bps, exit reason, realized P&L,
  and per-trade linkage back to its originating decision via `decision_uid` (`/api/trades` +
  `/api/decisions?trade_id=`) — i.e. an **intended-vs-filled** (2 of 4 stages) divergence view is
  buildable today with literally zero new code, just new front-end wiring against endpoints that
  already exist and are already used elsewhere in the same page.
- Live positions and live working orders (broker-sourced, not historical).
- Recent system events by severity (`/api/events`).
- Price chart (`/api/bars`).

**One small, well-scoped addition (not a V2 package, a same-tier read-path fix)** would complete
the picture to 3-of-4 stages with no new *storage*: a `store.get_orders()` method plus a
`GET /api/orders/history` (or similarly named) route reading the existing `orders` table, giving
the **accepted** stage its own history endpoint instead of only current open orders. This is
capture-complete already (§4) — it is purely a missing read path, the same shape of gap as
`/api/fills` (also missing, also capture-complete).

**What is genuinely blocked and waits on V2 packages, not on plumbing:**

- Any **authorized**-stage column or divergence view — blocked on a Guardian/Risk Allocator
  existing at all (§4).
- Any per-**worker** view (identity tuple, per-worker ledger, per-worker window state) — blocked on
  WP-V2A-02 worker identity; today's Bridge is single-account, single-strategy, single-symbol
  (`bridge/settings.py:31-37`).
- The Guardian panel, veto tiers, and any "block reason: Guardian" row — blocked on WP-V2B-01.
- Multi-symbol market-context cards — blocked on the Bridge tracking more than one symbol at once.
- Shared IP/WS budget *usage* panel (the raw limits are public facts, but there is no allocator to
  report consumption against them) — blocked on the central allocator (P1 B.8).
- Any authenticated/step-up-gated view — blocked on WP-V2B-06; today's only access control is the
  SSH tunnel pinning in the KVM2 runkit script (§2) plus the `X-Confirm` header on mutating calls,
  neither of which is a login/session system.

---

## 8. Concrete reusable-pieces list

1. **`/api/snapshot` + `/ws`** — the existing bundled-read-plus-push mechanism the V1 page already
   uses. Any new dashboard view should be built as an additional consumer of this pair, not a
   parallel polling scheme.
2. **V1 page structure and CSS** (`bridge/static/index.html`, `app.css`) — sidebar nav + page
   sections + card/panel/pill visual language. The Dashboard V2 prototype's own README confirms it
   borrowed this as its reference, so the two are already visually consistent.
3. **`trades` + `decisions` join by `decision_uid`/`trade_id`** — already queryable, already served,
   gives a real (not fixture) intended-vs-filled view including one-sided (entry-only) slippage
   attribution today.
4. **Three-layer labeling convention from the V2 prototype** (desired/accepted/actual naming,
   per-layer "owner" and "never contains" framing) — reusable as a *display convention* now, to be
   applied to real `decisions`/`orders`/`trades` data as soon as the `orders`-table read gap (§7) is
   closed, without waiting for any V2 backend package.
5. **The observability toolkit's `export_audit_pack.py`** — not a dashboard component, but a
   ready-made manual fallback for reaching `orders`/`fills` history today (offline, one-shot,
   explicit store path) until a proper `/api/orders/history` route exists.
6. **The KVM2 runkit's access model (SSH-agent + pinned fingerprint + pinned host key, no stored
   credentials)** — reusable as-is for reaching any future dashboard revision on the same host; it
   is a transport wrapper, not tied to what's on the other end.
7. **Worker identity tuple / Guardian veto-tier vocabulary from the V2 prototype fixtures** — reusable
   as target *field names* for whichever package eventually builds WP-V2A-02/WP-V2B-01, but has zero
   real data behind it today and cannot be wired to anything live yet.

---

*Read-only investigation. No bridge process, server, or test suite was executed. Citations against
`IBKR_PAPER_BRIDGE/` and `MTC_COMMAND_CENTER/` at master `ab35ca66c574f051ae7f01173eafc1145a3f72cf`,
plus one file read from branch `codex/rp7-r1-r4-repair-20260815` (KVM2 runkit, §2, not yet merged)
and one prior research doc read from branch `research/bridge-plan-delta` (§0 cross-check, also not
yet merged), from worktree `C:\WFR5B` on branch `research/execution-surface-inventory`.*

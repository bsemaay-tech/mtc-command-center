# Package 5a — Local Observability Toolkit (first increment)

Branch: `feature/bridge-v2-package5a` · Tier: **T1**
Scope authority: `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE5A_OBSERVABILITY_TOOLKIT_2026-08-18.md`
(the Gate-1 record is the complete scope contract; this README restates it,
it does not replace it).

## What is here

| Path | What it is |
| --- | --- |
| `export_audit_pack.py` | Stdlib-only, **read-only** CLI that builds one Markdown audit/export pack from an **explicitly supplied** bridge-format SQLite store path (+ optional log files): schema version from `meta`, table list with row counts, `app_state` and key meta values, bounded most-recent orders/events, and explicit `**[REPORTED]**` gaps for anything missing or malformed. Never invents data. Never a default path. |
| `fixtures/build_fixture_store.py` | Builds a small **synthetic v4-shaped** SQLite store (own CREATE statements, clearly fake `SYNTH`/`synth-*` values). The store is built at test time; **no `.db` binary is committed**. |
| `readiness_checklist.html` | Standalone static pre-flight checklist (state safety / schema / contracts / environment), each row with plain + technical explanation and a contract citation (`path:lines`). In-page check state only — no persistence, no network — under a permanent **"this page controls nothing"** banner. |
| `CHAOS_DRILLS_DESIGN.md` | Design-only matrix of MockBroker chaos drills (disconnect, partial fill, stale ack, restart mid-lifecycle × lifecycle stages) with expected invariants, contract citations, and evidence format. **Implementation deferred** (see Trim). |
| `tests/test_export_audit_pack.py` | pytest suite: builds the fixture at test time, runs the export, asserts schema-version reporting, row counts, bounds, and graceful `REPORTED` missing-table/malformed handling. |

## Trim statement (recorded, not silent)

- **Chaos-drill implementation is deferred.** Only the design document ships
  here. Wiring drills into the live test harness approaches protected
  behavior surfaces and gets its own increment and Gate-1 slot (Gate-1 record
  §1 item 4).
- Fixture DDL is a **minimal shape replica** of the v4 baseline (tables and
  columns mirror `bridge/store/db.py`; indexes and triggers are omitted, CHECK
  constraints kept only where cheap and characteristic). It is not a migration
  path and never substitutes for bridge code.
- The export tool reports what IS there. Absent tables/keys are gaps, not
  zero-filled guesses.

## Boundaries

- Files in this directory only. Zero modifications to any existing file
  anywhere (nothing under `bridge/`, no test-harness changes).
- **No bridge code is imported** by any tool here; no network; stdlib only.
- The store path is always caller-supplied (`--store` is required); there is
  **no default live path** and the store is opened SQLite read-only
  (`mode=ro`) — the tool cannot create, modify, or delete a store.
- All broker/exchange interaction is out of scope entirely.
- Approvals/flip/order-changing tools are OUT (T0 surfaces, per the standing
  prohibition list).

## Non-authority

Everything here is **observational evidence tooling and reading aids**:

- The audit pack describes a store; it approves nothing.
- The checklist page controls nothing — its checks are in-page only, unsaved,
  and reset on reload.
- The drill design executes nothing.

No file in this package arms, disarms, approves, trades, or authorizes
anything. Deployment/redeploy remains a separate owner gate.

## Usage

```bash
# build a synthetic fixture store (explicit path only)
python IBKR_PAPER_BRIDGE/tools_v2/observability/fixtures/build_fixture_store.py \
    --out /tmp/synth_fixture.db

# export an audit pack from it (explicit store path only)
python IBKR_PAPER_BRIDGE/tools_v2/observability/export_audit_pack.py \
    --store /tmp/synth_fixture.db \
    --timestamp 2026-08-18T01:00:00Z \
    --recent-n 50 \
    --out /tmp/audit_pack.md            # omit --out to print to stdout

# run the tests
python -m pytest IBKR_PAPER_BRIDGE/tools_v2/observability/tests -q
```

Open `readiness_checklist.html` directly in a browser — it is fully
self-contained (works from `file://`, no external resources).

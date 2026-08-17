# Gate-1 Scope Record — Package 5a: Local Observability Toolkit (first increment)

**Date:** 2026-08-18 (overnight) · **Lead:** Claude (Fable) · **Tier: T1**
**Owner authorization:** 2026-08-17/18 night, in chat: explicit "devam" on the Lead's stated
default path (Packages 3, 4, 5a), after Decision 5; full autonomy reiterated (Decision 6).
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 5a (T1
observational: audit/export pack, MockBroker chaos drills, readiness-checklist UI);
kickoff skeleton in `BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md`.

## Frozen scope (first increment) — explicit in-package trim, no silent caps

NEW directory `IBKR_PAPER_BRIDGE/tools_v2/observability/` (isolated worktree `C:\P5AOBS`,
branch `feature/bridge-v2-package5a`):

1. **Audit/export pack tool** `export_audit_pack.py` — stdlib-only, read-only. Input: an
   explicit path to a bridge-format SQLite store file (fixtures provided; never a live default
   path) plus optional log files. Output: one Markdown audit pack — schema version read from the
   store, table row counts, app_state/meta values, recent orders/events (bounded row caps),
   integrity notes (e.g. missing tables reported, not invented). Works against the FIXTURE store
   only in tests.
2. **Fixture store builder** `fixtures/build_fixture_store.py` — creates a small synthetic
   SQLite store mimicking the v4 baseline shape (its own CREATE statements; independent of live
   code so no bridge imports are needed). The built `.db` artifact is produced at TEST TIME in
   a temp path and is never committed.
3. **Readiness-checklist UI** `readiness_checklist.html` — standalone static page; the
   pre-flight checklist items derived from the accepted contracts (docs/21/22/23 highlights,
   DISARMED default, loopback-only, schema-version expectations), each row check-off-able
   locally (state in-page only, no persistence, no network), with a plain-language explanation
   per item and an explicit "this page controls nothing" banner.
4. **Chaos-drill DESIGN document** `CHAOS_DRILLS_DESIGN.md` — specification only for MockBroker
   drills (disconnect, partial fill, stale acknowledgment, restart mid-lifecycle): drill matrix,
   expected invariants, evidence format. **Implementation of the drills is explicitly deferred
   to a later increment** — recorded trim, because wiring drills into the live test harness
   approaches protected behavior surfaces and deserves its own slot.
5. `tests/test_export_audit_pack.py` — pytest: runs the export against the built fixture store,
   asserts bounded output, correct schema-version reporting, and graceful missing-table
   handling.
6. `README.md` — scope, trim statement, boundaries, non-authority.

## Hard boundaries

- New directory only; zero modifications to existing files (no edits under `bridge/`, no test
  harness changes). All broker/exchange interaction is out of scope entirely in this increment
  (export tool reads local files only). No network imports. Approvals/flip/order-changing tools
  are OUT (T0). Standing prohibition list applies.

## Roles, review, acceptance

- Implementer: GLM-5.3. Review: DeepSeek `deepseek-v4-pro` + Gemini cross-check + Lead
  inspection with pytest executed locally by the Lead.
- Done means: pytest green under the Lead's own run, checklist page renders standalone, drill
  design complete, trim recorded, review findings resolved, committed on the package branch.

# P0-31 Milestone 1 — frozen G1 scope and engineering contract

Date: 2026-09-12
Lead branch/worktree: `feature/p031-m1-20260912` / `C:/tmp/P031_M1_20260912`
Base: `42f99571e6abb5222744d9345e1c8a9e19c23c15` (`origin/master` at start)
Tier: T0. This is a fixture-only early build and cannot be accepted before WP-P0-04 and WP-P0-13 acceptance evidence is pinned.

## Authority and boundaries

- Implement only Milestone 1: a new local lifecycle ledger, one append route, deterministic replay/current view, Registrar funnel operations, integrity checks, backup/restore, and a read-only report.
- Reuse the current `LifecycleEvent` and all four `LifecycleWriterClass` values from `MTC_COMMAND_CENTER/contracts/mtc_contracts/execution.py`; do not edit shared contracts.
- No legacy import, consumer cutover, registry retirement/deletion, deployment, host contact, credentials, exchange activity, ARM/orders, Pine/trading/parity behavior, threshold choice, or acceptance claim.
- The legacy reader at commit `c068de32c5fb868c0409ab8a8e8f649b068cbeee` is a separate read-only projection. It is not ledger state and is reused only after its behavior is independently checked.
- WP-P0-14 stays OPEN and deferred until after core Bridge engineering. The interim report is provenance-first and read-only; it is not the Explorer or an eligibility/admission surface.

## Public seams fixed for implementation and tests

The exact spelling may be minimally adjusted by the implementer only if tests and this file are updated before parallel work consumes it. Do not add a service or dependency.

1. `LifecycleLedger(path, writer_allowlist, active_check_sets=None, accepted_evaluation_catalog=None)` *(amended 2026-09-17 — see the amendment log; the pre-batch spelling was `LifecycleLedger(path, writer_allowlist, active_check_sets=())`)*
   - standard-library SQLite, schema/version literal `p031.lifecycle-ledger.v1`;
   - default/empty writer allowlist fails closed;
   - creates or opens one local ledger and validates its schema/version.
2. `append(event: LifecycleEvent, *, check_set_version=None, evaluation_run_hash=None, failing_checks=(), check_set_purpose=None, catalog_backed=False, source_kind="FIXTURE")` *(amended 2026-09-17 — see the amendment log; the pre-batch spelling had no `check_set_purpose` / `catalog_backed`)*
   - the sole normal write route;
   - strict `LifecycleEvent` validation, exact `(writer_class, writer_id)` allowlisting, prior-state match, writer/state authority, identity depth and event-specific evidence validation happen inside one `BEGIN IMMEDIATE` transaction;
   - every append has a global sequence, per-writer sequence, canonical event bytes, previous digest and digest; the derived current view updates in the same commit;
   - any repeated event id is rejected; same bytes are `DUPLICATE_EVENT`, different bytes are `CONFLICTING_EVENT`;
   - no API edits or deletes event history.
3. `Registrar(ledger, writer_id)`
   - public operation seam is `Registrar.append(event, **evidence)`, which rejects non-Registrar events and delegates to the ledger's sole `append` route;
   - may produce only research-funnel events through `append`;
   - current permitted structural paths: initial `CAPTURED`; `CAPTURED -> TRIAGED`; `TRIAGED -> CANDIDATE`; `CANDIDATE -> FROZEN|PARKED|REJECTED`; triage may end `DECLINED`; and `REJECTED|DECLINED|PARKED -> CANDIDATE` only as `RE_ENTRY` with one of the five ratified triggers;
   - `CAPTURED -> TRIAGED` is operationally BLOCKED unless an exact active owner-ratified worthiness `check_set_version` is configured. The current v0.1 draft is inactive and must not be treated as ratified;
   - `REJECTED` requires check-set version, evaluation-run hash and non-empty failing-check evidence. Re-entry preserves candidate id, requires a fresh evaluation-run hash and never re-counts prior evidence.
4. Other writer classes
   - admitted by the common route only when explicitly allowlisted;
   - fixture tests cover their distinct authority and identity depth, but no real admission/promotion/tail producer is created;
   - Registrar attempts to issue ladder/tail events are rejected.
5. `replay()` / `current_state(candidate_id)` / `rebuild_current_view()`
   - ordered only by committed ledger sequence;
   - replay revalidates the chain, writer sequences, contract bytes, transitions and derived state;
   - destroying and rebuilding the derived view is lossless and deterministic.
6. `verify_integrity(expected_event_ids=(), expected_writer_sequences=None)`
   - detects SQLite corruption, sequence gaps, chain changes, invalid canonical payloads, derived-view drift, missing externally expected event ids and gaps against externally supplied writer checkpoints;
   - explicitly does not claim that application-written hashes independently resist a writer with database access, or that an event never declared by an external authority can be discovered.
7. `backup_to(destination)` and restore onto a new destination
   - use SQLite's consistent backup primitive, refuse overwrite/symlink ambiguity, and verify source and restored copy;
   - ledger history is never deleted or rewritten.
8. `render_status_report()` plus a small CLI report command
   - read-only, deterministic ordering;
   - shows candidate id, source kind (`FIXTURE` versus future authoritative source), writer authority, prior/current state, reason/trigger, package/deployment identity, evidence references, timestamp and unresolved dependencies;
   - never labels a candidate eligible/admitted/live because tests passed.

## Required counterfactuals and runtime checks

- RED/GREEN or equivalent mutation evidence for unauthorized writer, illegal transition, duplicate/conflicting event id, update/delete guard, missing expected append, and corrupted/edited chain.
- Restart, interrupted uncommitted append, two concurrent writers, deterministic replay, derived-view destruction/rebuild, backup/restore and corrupted backup refusal.
- Malformed/naive-time/identity-mismatch/evidence-mismatch cases use public seams and independently fixed literals.
- Run `py_compile`, the focused unittest module, the reader self-check, `git diff --check`, repo guard, and any current package tests that exercise `LifecycleEvent`.

## Exclusive write lanes

| Lane | Provider/model | Writes | Dependency | Stop condition |
|---|---|---|---|---|
| Core builder | included subscription, cheapest capable | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` only | this contract + current shared contract bytes | module compiles and self-checks; no other paths touched |
| Test/fixture worker | separate included subscription | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py` only | this contract and frozen public seams | focused tests exercise required behaviors; no implementation edits |
| Legacy reuse | Lead | `read_candidate_history.py` only through verified commit reuse | candidate commit behavior verified | file imported unchanged or rejected with reason |
| Admin/handoff | later separate writer | scope/status, decisions, handoff and two planning amendments only | frozen implementation/test evidence | factual status and P0-14 exception recorded without acceptance overclaim |

## Current upstream state and exact open dependency

- Current base contains the P0-04 `LifecycleEvent` and four writer classes; acceptance provenance is not inferred from source presence.
- WP-P0-13 is actively being built/reviewed in its own task and is not treated as accepted. No real TrialRecord bytes are consumed in this slice.
- Exact missing definition: no owner-ratified worthiness checklist version exists, so `CAPTURED -> TRIAGED` stays fail-closed. Engineering may prove the configurable guard with fixtures but may not invent or activate a version.

## Amendment log (this file's own rule at the head of "Public seams": the spelling may be minimally adjusted only if tests and this file are updated)

- **2026-09-17 (Lead, session 6):** the two seam spellings above are updated to the bytes of `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` at candidate `61c56148` (constructor `:321-327`, `append` `:848-858`), which the M1 batch changed under the owner's twelve answers `OD-20260914-P031-LIFECYCLE-1` (`C:/CT13/DECISIONS.md`): OD-1 (active check-set enforcement — `active_check_sets` is a mapping of check-set version → purposes, default `None`, enforced when supplied), OD-5 (`check_set_purpose` on `append`), OD-11 (`catalog_backed` on `append` and `accepted_evaluation_catalog` on the constructor: a catalog-backed claim fails closed without an accepted catalog and without an evaluation hash). The tests that consume these spellings are in `tests/test_p031_lifecycle_ledger.py` at the same candidate (112 tests). This amendment answers NIT N-7 of the first exact-Opus read (2026-09-16) and the second read's note that the file still showed the pre-batch signatures; it changes no other sentence. Pre-amendment sha256 `1752290cb9dd81d75ce5ca65a1dd5510584151101e088ce08c638fadb8195d8a` (copy kept as `G1_SCOPE_AND_CONTRACT_pre_amendment_1752290c.md` in the P031_FIX records).
- **2026-09-17 correction (Lead, after the third exact-Opus read, N-17):** two sentences of the entry above are wrong and are corrected here rather than rewritten: (a) `active_check_sets` is a mapping of **purpose → versions** (`_normalize_active_check_sets` iterates `for purpose, versions in active_check_sets.items()`, ledger `:374`), not version → purposes; (b) the spelling `active_check_sets=None` was already the base's (`c76043b9` ledger `:269`), so that part of the seam was stale before this batch and OD-1 (a worthiness-ratification answer) changes no signature. The amendment stands on OD-5 (`check_set_purpose`) and OD-11 (`catalog_backed`, `accepted_evaluation_catalog`), both correctly cited; the amended spellings themselves are byte-correct at `61c56148`.

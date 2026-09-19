# WP-P0-31 — post-Milestone-1 scope packet, DRAFT 1 (2026-09-15 night) — for the owner after the M1 roster

Prepared by the Claude Opus 5 Lead (session 5, `03c6c8`). **Nothing in this draft is authorized, started or accepted.** It is the packet the owner will be asked to answer once Milestone 1's candidate has been through its flagship roster (exact Opus: Wednesday lane 1 on `48bd70de`; exact Sol: Fri 2026-09-19). Sources: plan `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:647-663` (package + three milestones), lifecycle fold `WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md` §3-§4c (map #54), the P031 decision packet V4 (`P031_LIFECYCLE_DECISIONS_20260913_V4.md`, twelve answers `OD-20260914-P031-LIFECYCLE-1`, batch `OD-20260914-P031-BATCH-GO-1`), `P031_HANDOFF.md`, and the candidate records `P031_BATCH_CANDIDATE_20260914/` + `P031_FIX_20260915/`.

## 0. Where Milestone 1 stands (facts; verify identities before acting)
| Item | State |
|---|---|
| Candidate | `48bd70de` on `feature/p031-m1-20260913-refresh` (`C:/tmp/P031_M1_20260913`): reviewed base `c76043b9` + owner batch (OD-2 1B, OD-5 4A, OD-6 5C, OD-7 6A, OD-9 5a-C, OD-10 5b-A, OD-11 2C, OD-1 3D doc amendment, OD-4/OD-8 recordings) + P31FIX + P31FIX2 (Lead-authored RED test, disclosed) |
| Roster | Gemini detection RC → delta PASS-WITH-NITS (J-01..J-05 resolved; K-D-02 NIT = Lead authorship → standard review); Lead ✔; **exact Opus Wed lane 1; exact Sol Sep 19**; Grok not required for the batch (capped anyway) |
| What M1 is, by construction | fixture-only: `source_kind` refused unless `"FIXTURE"`, derived view `CHECK authoritative = 0` — every report says `authoritative_records = 0`; no P0-13 symbol is consumed; Registrar research transitions, replay, current view, backup/restore, integrity guards proven on fixtures |
| What blocks M1 **acceptance** even after the roster (packet V4 §4) | (1) exact accepted **WP-P0-04** lifecycle/identity/writer provenance and exact accepted **WP-P0-13** TrialRecord/catalog provenance "actually consumed" — neither exists; (2) envelope 2 (`CHALLENGE`) needs a challenged-incumbent identity field that only WP-P0-04 may add; envelope 3 enforces the blunt global rule until `family_id` sits on `LifecycleEvent` (P0-04); (3) P0-13's chain sits behind P0-20 (B-01 not satisfied) |
| Consequence | the roster can return "accepted for the fixture-only milestone scope"; **package-level M1 acceptance waits on P0-04/P0-13**. The next packet must therefore split "M1 completion" from "M2 SEED_IMPORT", and say which parts need no upstream acceptance. |

## 1. Two different "next" things — do not merge them
| Track | What it is | Depends on | Tier |
|---|---|---|---|
| **A — M1 completion (the consumption seam)** | make the ledger consume real provenance: (a) widen `source_kind` beyond `FIXTURE` under an explicit authority record; (b) the OD-11 (2C) optional configured catalog: refuse an `evaluation_run_hash` absent from an accepted catalog; fail closed when a record claims catalog-backed evidence and no catalog is configured; (c) the P0-13 consumption seam (constructor seam `G1_SCOPE_AND_CONTRACT.md:20`, adjustable under `:18`); (d) P0-04 fields for envelopes 2/3 (owned by WP-P0-04, not P031) | **P0-13 accepted interface** (which waits on P0-20 acceptance → Sep 18 measurement → Opus/Sol) and a **WP-P0-04 amendment** (challenged-incumbent identity; `family_id` on `LifecycleEvent`) | T0 (lifecycle/admission identity) |
| **B — Milestone 2 `SEED_IMPORT`** | read the legacy lifecycle-bearing stores **read-only**, write one `SEED_IMPORT` record per seeded item into the ledger marked `migrated_2026` with provenance (source store, field, value, mapping row), `migrated-conflict` carrying **both** values where two writers disagree, a reconciliation report accounting for every source row (seeded / deliberately-not-seeded + reason / unresolved), idempotent re-run, `UNKNOWN` rather than a guess for unmappable rows | **Milestone 1 accepted** (plan: "Inputs: Milestone 1 accepted") — but the **design half** (source-row census, mapping-table application on a scratch copy, the reconciliation-report shape, D026 fixtures) needs no acceptance and no upstream package | T0 + milestone-scoped G1-IA |
Track A cannot start tonight or this week (upstream). Track B's design half can start on an owner word; its build waits for M1 acceptance.

## 2. Milestone 2 — scope as the plan states it, made concrete
### 2.1 Inputs (read-only; nothing here is edited, retired or deleted — plan non-goal)
| Legacy store (fold §4c) | Rows (fold count, to be **re-measured** before the import) | Disposition rule |
|---|---|---|
| `STRATEGY_RESEARCH_REGISTRY.json.current_status` (old 7-stage ladder) | all strategies | table 4a: `REJECTED`→`REJECTED` (marked `migrated-no-identity`); `KEEP_AS_RESEARCH_NOTE`→`PARKED` + `legacy:research_note`; five `PROMOTE_*`/`MTC_ENGINE_VALIDATED`/`APPROVED_*` values → `CANDIDATE` + their legacy tag; composite `A\|B` → highest component's row + every component's tag |
| `producer_spec.json.promotion_status` (44/63 filled; two independent writers) | 63 files | seed via 4a; disagreement with the registry → `migrated-conflict`, both values retained |
| `VARIANT_LOG_REGISTRY.json.promotable` | — | tag `legacy:promotable` on the variant's family record; never a state |
| `TRIAGE_CANDIDATE_REGISTRY.json` | 172 candidates | extract-or-decline decision recorded → `TRIAGED`; otherwise `CAPTURED`; `eligible_for_retriage` → `legacy:retriage_eligible` |
| `AI_QUANTLENS_VERDICT_REGISTRY.json.decision` | — | advisory tags only (`advisory:needs_clarification` / `research_only` / `salvage`) |
| `scorecard_v2` files | — | **not migrated** (evidence artifacts, stay readable in place) |
| The nine diagnostic labels (fold §4b) | — | `label:<lowercased>` tags, never states; label `REJECTED` ≠ ladder `REJECTED` |
Governing principle (fold §4, #59): **no retroactive hash blessing** — the highest state a migrated record may hold is `CANDIDATE`; no seed lands on the Evidence Ladder; seeds count toward no gate. This is also why Track A's `source_kind` widening must distinguish `MIGRATED_2026` from any future authoritative producer.

### 2.2 Outputs
1. `SEED_IMPORT` records in the ledger (one per seeded item; `source_kind = MIGRATED_2026` or equivalent authority label; provenance fields verbatim; tags per §4a/§4b/§4c; `migrated-conflict` with both values; `migrated-no-identity` for `REJECTED`).
2. The **reconciliation report**: every source row → seeded / not-seeded (reason) / unresolved (`UNKNOWN`); balanced against a **freshly measured** source-row count; the enumeration shown capable of finding a source row it was not told about (a planted row in a scratch copy is found).
3. The idempotence proof: a second identical run appends nothing (record count and derived view byte-identical).
4. D026 fixtures: conflicting pair → `migrated-conflict` with both values (RED without the rule); planted-row detection (RED without the enumeration check); `UNKNOWN`-on-ambiguity (RED if a guess is produced).
5. `UNKNOWN` targets listed by exact identity — they **block Milestone 3 for that target** (plan).

### 2.3 Acceptance (plan, verbatim intent)
Reconciliation balances against a freshly measured count; enumeration finds a planted row; deliberately conflicting pair produces `migrated-conflict` carrying both values (D026 RED/GREEN); a second identical run appends nothing; unmappable/ambiguous rows are `UNKNOWN`, never guessed. Roster: T0 (exact Opus + exact Sol + Gemini + Lead reproduction) on the frozen candidate; milestone-scoped G1-IA recorded before dispatch.

### 2.4 Non-goals (plan)
Reads the legacy stores and writes only into the ledger; edits, retires, de-tracks, deletes nothing; changes no consumer and no `read_model`. Milestone 3 (retirement, consumer repair for `WP-P0-14`, `WP-V2A-01`, `WP-V2A-10`, `WP-V2B-03`, `WP-V3-03`, sole-writer proof; any deletion under G8 against an exact enumerated list) stays unauthorized by this packet.

## 3. Questions for the owner (packet style — recommended answer first; nothing runs on a default)
| # | Question | Options | Recommended | Why |
|---|---|---|---|---|
| Q1 | May the Lead run the **M2 design half now** (source-row census on a scratch copy of the five stores; mapping-table dry application producing the reconciliation-report shape; the three D026 fixture designs), while M1 waits for its roster and upstream? | A: yes, documentary + scratch only, no ledger write, no code on the P031 branch; B: wait for M1 acceptance | **A** | it depends on nothing that is pending; it produces the measured row counts the plan demands "freshly" (they will be re-measured at import time anyway); it costs ~3 h of Lead time and no review slot |
| Q2 | Authority label for migrated records in the ledger's `source_kind` (today only `FIXTURE` is accepted) | A: add exactly one new value `MIGRATED_2026` with `authoritative = 0` kept for it; B: reuse `FIXTURE`; C: defer to Track A | **A** | B would make migrated history indistinguishable from test fixtures; C couples M2 to the P0-13 seam it does not need; A keeps "counts toward no gate" enforceable by the same SQL `CHECK` pattern |
| Q3 | Composite legacy values (`A\|B`) | A: fold §4 rule as written (highest-ranked component's row; all component tags); B: `UNKNOWN` for every composite | **A** | the fold already decided it; B would push avoidable rows into the M3 blocker list |
| Q4 | Two-writer disagreement (`producer_spec.promotion_status` vs registry `current_status`) | A: `migrated-conflict`, both values, state = the **lower** of the two mapped states; B: `migrated-conflict`, both values, state = `UNKNOWN` | **A** for the state, **B** if the owner prefers zero inference | the plan requires both values retained and neither winning silently; the *state* still needs a rule — taking the lower state never over-claims; the choice is recorded in the provenance field either way |
| Q5 | Rows whose source file is unparseable or whose value is outside tables 4a/4b/4c | A: `UNKNOWN` + listed (plan) | **A** (no alternative offered) | plan text |
| Q6 | Sequencing: may M2's **build** be dispatched as soon as M1's roster accepts the fixture-only scope, before P0-04/P0-13 provenance lands (M2 does not consume P0-13)? | A: yes — M2 depends on "Milestone 1 accepted" and the roster's fixture-scope acceptance is what exists; record the provenance gap as an M1 open item; B: no — wait for full M1 package acceptance | **B by the plan's letter**, with **A offered as an amendment the owner may make** | the plan says "Milestone 1 accepted"; the packet V4 shows package-level M1 acceptance is blocked upstream for weeks; the owner may amend the dependency explicitly — the Lead does not infer it |

## 4. Estimates (Lead planning estimates, not promises)
Design half (Q1 A): ~3 h Lead + one Gemini corroboration. Build (after the word): ~2 Codex lanes (importer + fixtures) + 1 Lead reproduction + full T0 roster (~2 h Opus/Sol slots + adjudication). Milestone 3: not estimated here (needs the M2 reconciliation report first).

## 5. Files
- This draft: run root `P031_M2_SCOPE_PACKET_DRAFT_20260915.md` → CT13 `QUEUED_PACKAGES_20260915/`.
- To be produced by Q1 A: `P031_M2_SOURCE_CENSUS_<date>.md` (row counts per store, measured), `P031_M2_MAPPING_DRY_RUN_<date>/` (scratch), `P031_M2_FIXTURE_DESIGN_<date>.md`.

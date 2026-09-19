# WP-P0-31 Milestone 2 — MAPPING DRY RUN and the reconciliation-report SHAPE (design half, Q1 A) — 2026-09-16 11:5x UTC+3

Prepared by the Claude Opus 5 Lead (session 6, `4a8233`) under `OD-20260916-P031-M2-Q1-Q6-1`. `m2_dry_run.py` applies the fold's one-time mapping table (§4a/§4b/§4c of `WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md`) under the owner's answers Q2 A (`MIGRATED_2026`, `authoritative = 0`), Q3 A (composite → highest-ranked component's row, all tags), Q4 A (`migrated-conflict`, both values, the LOWER state) and Q5 A (`UNKNOWN` + listed) to the scratch copies, and writes the report SHAPE. **No ledger record is written; no repository file is touched.** Every artifact is labelled `DESIGN_DRY_RUN_NOT_A_LEDGER_WRITE` (or `WHAT_IF_NOT_RULED` for the extension run).

## 1. The reconciliation report — shape (what the M2 build must emit)
```
report_kind         P031_M2_RECONCILIATION_REPORT_V1 (this dry run: _SHAPE_V0)
label               MIGRATED_2026 import | DESIGN_DRY_RUN_NOT_A_LEDGER_WRITE | WHAT_IF_NOT_RULED
ruling              OD-20260916-P031-M2-Q1-Q6-1 (+ the rows that answer Q7..Q13)
sources             per store: path, sha256 of the bytes read, blob OID at the checkout HEAD, generated_at
balance             per store: rows measured NOW by the importer's own enumeration, rows disposed, rows
                    censused (the design census) — every_row_disposed and matches_census as booleans
balanced            true only if every store has every row disposed AND the fresh count equals the census
dispositions        ONE row per source row (Pattern 13, terminal disposition): source, row id, field, value,
                    disposition ∈ {SEEDED, NOT_SEEDED, UNKNOWN}, and for SEEDED the state/tags/host, for the
                    others the reason; the second writer's value travels on the same row (`also`, `also_value`)
seeds               the SEED_IMPORT records the build would write: candidate_id, record=SEED_IMPORT, state,
                    tags (legacy:* / advisory:* / migrated-conflict / migrated-no-identity), provenance
                    {source_kind: MIGRATED_2026, authoritative: 0, <store>: {row, field, value, alias}}, conflict
conflicts           the seeds carrying migrated-conflict, both values retained, the resolved (lower) state
unknown_targets     every UNKNOWN disposition with its reason — these BLOCK Milestone 3 for that target
totals / seed_state_counts / conflict_count / unknown_target_count
statement           what the artifact is not
```
Idempotence (plan): a second identical run appends nothing — the build proves it by record count + derived-view digest equality; the dry run proves determinism only (identical input → identical `reconciliation_report.json` sha256; run twice: `0fc6a0a6…` both times).

## 2. Disposition rules as implemented (one per store; both producers named)
| Source row | Rule applied | Producers | Disposition when the rule cannot decide |
|---|---|---|---|
| registry `current_status` | components = split on `\|`; each must be in 4a (or 4a′); state = highest-ranked component's row; tags = every component's tag; `REJECTED` adds `migrated-no-identity`; joined producer_spec (by folder `STG###`) mapped the same way; disagreement → `migrated-conflict`, both values, lower state | A = the two store values verbatim; B = table 4a rows (rank = row order) + `STATE_RANK` | any unmapped component on either side → `UNKNOWN` (Q5 A wins over Q4 A) |
| producer_spec `promotion_status` | disposed INSIDE its registry row (JSON list = composite); a folder without a registry row → `UNKNOWN` (none today) | as above | — |
| variants `promotable` | `True` → tag `legacy:promotable` on the FAMILY record (no family identity exists → `UNKNOWN`); `False` → `NOT_SEEDED` "no tag, never a state" (20/20 today) | A = the flag; B = table 4c | — |
| triage candidates | recorded extract-or-decline decision → `TRIAGED`, else `CAPTURED`; `eligible_for_retriage` True → `legacy:retriage_eligible`; identity = `candidate_id` (`QLR_…`), never `stg_code` | A = the store; B = table 4c (+ Q9 if the owner admits a proxy) | — |
| verdicts `decision` | `NEEDS_CLARIFICATION`/`RESEARCH_ONLY`/`SALVAGE` → advisory tag on the host seed with the same id; no host → `NOT_SEEDED` "tag without host" (43 today); other decision → `UNKNOWN` (none) | A = the store; B = table 4c | — |
| 4b labels | not read (outside the five stores; Q11) | — | — |

## 3. The three runs (scratch; `C:/tmp/P031_M2_DESIGN_20260916/`)
| Run | Command | Result | sha256 of `reconciliation_report.json` |
|---|---|---|---|
| as ruled | `m2_dry_run.py --out run_as_ruled --census census.json` | `balanced=true`; 175 seeds (`CANDIDATE` 3, `CAPTURED` 172); 0 conflicts; **60 UNKNOWN** (registry values outside 4a); 63 NOT_SEEDED (20 variants, 43 advisory orphans); 344 SEEDED dispositions (3 + 172 + 169 advisory tags on hosts) | `0fc6a0a6c2af8115f57bcc71b25f0ec730237b6cbdd1f3015eb3094a9c6cdebb` |
| planted row | `… --out run_planted --census census.json --plant` (one synthetic registry row `STG999`) | `balanced=false`: registry measured 64 vs censused 63 — the enumeration finds a row the census was not told about (plan acceptance: "enumeration finds a planted row") | `d0a5bf8decf6dc7a0b280cbcf1b2e6931494cc873b0332cbe49f488d8941196c` |
| what-if 4a′ (NOT RULED) | `… --out run_whatif_4a_prime --census census.json --table-extension table_4a_prime_PROPOSED.json` | `balanced=true`; 235 seeds (`CANDIDATE` 3, `CAPTURED` 232); **28 `migrated-conflict`** (all registry→`TRIAGED` vs producer_spec→`CAPTURED`, resolved to `CAPTURED`, both values retained); 0 UNKNOWN | `9fbd9b7fb40b167e2c75848a1c80cd3072686988e8e96050834db26b1956318f` |

## 4. What the build must add beyond this dry run (for the G1-IA packet after M1 acceptance; Q6 = B)
1. Read the stores from the checkout at a pinned commit (blob OIDs in the report), never from a scratch copy; re-measure; refuse if the count differs from the census the owner saw without a fresh owner word.
2. Widen the M1 schema `CHECK (source_kind = 'FIXTURE')` to `IN ('FIXTURE', 'MIGRATED_2026')` (Q2 A) with `authoritative = 0` unchanged; add the `(None, SEED_IMPORT, <state>)` initial registrar transition (Q13) — both inside the P031 branch under its own roster, NOT here.
3. Write one `SEED_IMPORT` event per seed through `LifecycleLedger` (writer class REGISTRAR, writer id `p031-m2-seed-import`), idempotent on `candidate_id` + provenance digest; the reconciliation report as the run's single output beside the ledger.
4. Case-sensitive exact joins only; `stg_code` never an identity; refuse any candidate_id that collides across stores.
5. The D026 fixtures of `P031_M2_FIXTURE_DESIGN_20260916.md`.
6. One disposition record per producer_spec FILE as well (joined to its registry seed by reference), not only through the parent registry row — Gemini NIT-03 on the dry run's balance counting; Pattern 13 auditing wants every admitted member visible on its own line.

## 5. What this dry run is not
Not a ledger write; not an import; not an acceptance of M1 (which waits on the roster and upstream P0-04/P0-13); not an authorization of the M2 build (Q6 = B: waits for full M1 acceptance); not an owner decision on Q7..Q13 — the what-if run exists only to show the owner what each choice does.

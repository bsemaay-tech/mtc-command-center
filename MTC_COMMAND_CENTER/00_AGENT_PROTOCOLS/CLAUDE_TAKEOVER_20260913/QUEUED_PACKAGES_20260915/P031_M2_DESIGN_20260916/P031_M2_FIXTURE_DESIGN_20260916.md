# WP-P0-31 Milestone 2 — D026 FIXTURE DESIGNS (design half, Q1 A) — 2026-09-16 12:0x UTC+3

Prepared by the Claude Opus 5 Lead (session 6, `4a8233`) under `OD-20260916-P031-M2-Q1-Q6-1`. Designs only: no fixture file, no test and no code is created on the P031 branch (Q6 = B). Each fixture names the defect it falsifies, the RED arm (the check removed or the mutant applied) with its expected wrong output, the GREEN arm, and the exact observable that discriminates — so the build's tests cannot pass for the wrong reason (Pattern 10, "evidence that cannot fail"). The dry-run script already behaves as the GREEN arm for #1-#3 on real-shaped rows.

## Fixture 1 — conflicting pair → `migrated-conflict` carrying BOTH values (plan acceptance)
- **Input (scratch stores, real-shaped):** one registry row `STG9A1` with `current_status = "PROMOTE_TO_FORWARD_PAPER_TRADE"` and its producer_spec folder `03_QUANTLENS/strategies/STG9A1_fixture/producer_spec.json` with `promotion_status = ["KEEP_AS_RESEARCH_NOTE"]` (both values inside table 4a, so Q5 cannot pre-empt Q4).
- **GREEN:** exactly one seed `STG9A1`, `state = PARKED` (the lower of `CANDIDATE`/`PARKED` under Q12 A), tags `{legacy:forward_paper_aspirant, legacy:research_note, migrated-conflict}`, provenance carrying BOTH verbatim values with their store and field, `conflict = {registry: [value, CANDIDATE], producer_spec: [value, PARKED]}`; reconciliation row `disposition = SEEDED, conflict = true`.
- **RED (mutant A — "first writer wins"):** drop the disagreement branch → state `CANDIDATE`, no `migrated-conflict` tag, producer_spec value absent from provenance → the assertion on the tag AND on the retained second value fails (two independent observables; both must be asserted).
- **RED (mutant B — "higher wins"):** replace `min` by `max` in the lower-state rule → state `CANDIDATE` with the tag present → the state assertion alone catches it (this is why the tag assertion is not enough).
- **Also asserted:** a pair that AGREES (`PROMOTE_TO_FORWARD_PAPER_TRADE` on both sides) produces no `migrated-conflict` tag (the three real rows are that case) — guards against a mutant that tags every joined pair.

## Fixture 2 — planted-row detection (plan acceptance: "enumeration finds a planted row")
- **Input:** the census JSON the owner saw (`rows.STRATEGY_RESEARCH_REGISTRY.json = 63`) and a scratch registry with ONE appended row `STG999` (`PROMOTE_TO_SANDBOX`).
- **GREEN:** the importer's own enumeration reports `measured_now = 64`, `matches_census = false`, `balanced = false`; the run REFUSES to write (exit non-zero, report staged, zero ledger records); the planted row appears in `dispositions` (it is enumerated, not hidden).
- **RED (mutant — "count from the census"):** replace the fresh enumeration by the census number → `balanced = true` and 64 seeds written → the refusal assertion fails.
- **RED (mutant — "skip unknown-shaped rows"):** plant a row missing `strategy_id` → a mutant that `continue`s over malformed rows reports 63 → must instead dispose it `UNKNOWN` (Pattern 13: every admitted member gets a terminal disposition) and still unbalance the count.
- **Measured today:** `run_planted/` shows exactly this (`balanced=false`, 64 vs 63).

## Fixture 3 — `UNKNOWN` on ambiguity, never a guess (plan acceptance)
- **Inputs (three rows):** (a) registry value `RESEARCH_BATCH` (outside table 4a as ruled); (b) composite `PROMOTE_TO_SANDBOX|NOT_A_LADDER_VALUE` (one component unmapped); (c) a producer_spec `promotion_status` that is a JSON object `{"status": "x"}` (unparseable shape).
- **GREEN:** three `UNKNOWN` dispositions, each with the offending value/component quoted in `reason`, listed in `unknown_targets`; zero seeds for those ids; the report's `unknown_target_count = 3`; the run still `balanced` (UNKNOWN is a disposition, not a gap).
- **RED (mutant — "closest match"):** a mutant mapping unknown values by prefix (`RESEARCH_*` → `CAPTURED`) or by ignoring the unmapped component seeds (a)/(b) → the `UNKNOWN` count assertion fails; (c) a mutant that `str()`-coerces the object seeds nothing but also lists nothing → the `unknown_targets` membership assertion fails.
- **Measured today:** the as-ruled run lists 60 such targets; the what-if run shows how an OWNER-RULED extension (not a guess in code) removes them.

## Fixture 4 (proposed addition) — identity collision across stores is refused, never merged
- **Input:** triage candidate `QLR_fixture1` with `stg_code = "Stg001"` and registry strategy `STG001`.
- **GREEN:** two distinct seeds (`QLR_fixture1` → `CAPTURED`; `STG001` → per its ladder value); no provenance of one carries the other's store; an advisory verdict with `strategy_id = "STG001"` attaches to the registry seed and one with `"Stg001"` attaches to nothing (`NOT_SEEDED`, tag without host).
- **RED (mutant — case-insensitive join):** `casefold()` on either side merges the two into one seed (or attaches the advisory tag to the wrong host) → the seed-count and host assertions fail.
- **Why:** the census measured 62 such case-folded collisions between DIFFERENT items (`Stg001` = a CANSLIM intake transcript; `STG001` = `ql_alpha_ada_two_candle_sr_1h`).

## Fixture 5 (proposed addition) — idempotent re-run appends nothing (plan acceptance)
- **GREEN:** run the import twice on the same pinned stores: ledger record count and the derived view's canonical digest are byte-identical after the second run; the second reconciliation report equals the first except `run_id`.
- **RED (mutant — "append on every run"):** drop the `(candidate_id, provenance digest)` idempotence key → the second run doubles the record count.

## Roster note
All five fixtures are T0 by the package's tier (lifecycle identity/admission); they run in the M2 build's own test module on the P031 branch under its G1-IA, after M1 acceptance (Q6 = B). The dry-run script is design scaffolding and is NOT the importer.

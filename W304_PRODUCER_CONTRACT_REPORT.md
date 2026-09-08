# W304 producer-contract report

## Verdict

**PARTIAL / CANONICAL CLAIM REFUSED.** Six authorized producer outcomes are implemented in six
separate commits and match the sealed corrected expectations. Outcome 7 is stopped as an
`INPUT/GOLDEN-OVER` owner item because the repository's sealed RULE2-08 setup cannot reach its
funding event without first attempting a pre-window fill for which the same sealed input supplies no
cost schedule. The canonical receipt labels the result
`BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` (`W304_GATE_RECEIPT.json:594-600`).

Finding count: **2**.

1. Rows 1-6 are implemented and locally verified; their former closed-set and expectation refusals
   are absent from the new receipt (`W284R_GATE_RECEIPT.json:1001-1150`;
   `W304_GATE_RECEIPT.json:778-886`).
2. Row 7 is not safely implementable from the sealed input as written. The gate still records the
   two RULE2-08 expectation mismatches and the missing conditional result member
   (`W304_GATE_RECEIPT.json:860-886`).

This is implementation evidence, not independent acceptance. Independent Gate-5/Gate-6 review is
**NOT VERIFIED**: the lane's C-1 clause forbids another assistant, agent, or model
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

## Lane and safety record

- Gate-1 classification: **T0**, because this lane changes economic result/event serialization; the
  repository defines economic work as T0 (`AGENTS.md:38-39`).
- Worktree: `C:\WP012BUILD`; branch: `feature/wp-p0-12-corrected-vnext-20260831`; start commit:
  `8e966c88d0a5dc6b6ccf0c99964067ccf6d16c46`. The required predecessor marker contained `exit=0`
  (`C:\tmp\LANE_PROMPTS_20260828\W303C_DONE.txt:1`).
- The only current ownership-table row on this branch was already released and recorded no tracked
  live/scheduled dependency (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:33-37`). W304's exact
  write paths are listed below; no foreign edit was included.
- The lane expressly forbids golden, catalog, input, baseline, seal, probe, and design changes
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:7-9`). None is in the substantive
  commit diff.
- No push, PR, merge, backtest, optimization, server, launcher, broker, venue, host, or network write
  was performed. The applicable clauses allow only local tests and verifiers
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`).

## Design bindings used

The result contract says, verbatim in its conditional table:

> `order_notional` | DEF-P012-01, DEF-P012-02, or DEF-P012-05 declares the
> entry-sizing/notional projection

It also requires `admitted` when DEF-P012-02 terminates in admission, `guards` when a declared guard
projection is evaluated, and `cumulative_funding` on both DEF-P012-08 results
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1190-1197`). The notional is the floored
quantity times final fill times contract multiplier, and equality is admitted
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:210-216,235-244`). The closed guard object
has four base members and conditionally adds `last_closed_guard_pnl`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1205-1214`).

The exit schema requires a `reason` member (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1152-1161`),
and the RULE2-07 binding is quoted exactly as `MARKET_EXIT/TIME_STOP/time_stop`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:923-928`).

## Outcome commits and evidence

The prior receipt is the RED evidence: it records the missing members and invalid old reason tokens
at `W284R_GATE_RECEIPT.json:1001-1058`, and the old manifest/reason/guard mismatches at
`W284R_GATE_RECEIPT.json:1117-1150`. Each implementation outcome has its own commit as required by
the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:27-33`).

| Row | Commit | Disposition and GREEN evidence |
|---|---|---|
| 1 | `de3c1d8e` | `corrected_surfaces` emits `order_notional` only for declared DEF-P012-01/02/05, deriving it from the final entry fill and instrument multiplier or the kernel decision trail (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:927-948`). Focused tests bind the five measured values to `1000, 100, 100, 0, 100` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1531-1573`). |
| 2 | `bf6d7923` | The serializer emits positive `admitted` only when the declared DEF-P012-02 run's kernel decision trail contains `MIN_NOTIONAL_ADMITTED`; the producer no longer accepts an authored boolean (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:978-981`). RED absence and GREEN `true` are checked at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1576-1588`. |
| 3 | `cbac9569` | A declared DEF-P012-07 projection requires the runner's computed guard snapshot, which is serialized through the closed guard projector (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:974-977`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1403-1415`). Exact RED/GREEN computed objects are checked at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1496-1528`. |
| 4 | `e49b514e` | Only `PROTECTIVE_STOP_EXIT` changed from `STOP` to the closed token `PROTECTIVE_STOP`; the other class mappings remain unchanged (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:655-664`). Both named scenarios are checked at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1204-1218`. |
| 5 | `7bc9e0ec` | A real `MARKET_EXIT` whose kernel `exit_id` is `TIME_STOP` serializes `time_stop`; no other market-exit token is rewritten (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:666-677`). The exact binding is checked at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1221-1230`. |
| 6 | `ef9ce894` | The run manifest receives the runner's actual `same_bar_collision_policy_id` only for declared DEF-P012-06 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1419-1426`). All three DEF-P012-06 scenarios check `TARGET_FIRST` at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1233-1247`. |
| 7 | no commit | **STOP — INPUT/GOLDEN-OVER.** See Finding 2 and Discrepancy D1. No seed, input, golden, catalog, schedule, or result-shaping switch was added. The carried no-seed test still observes empty cash/funding rows and no cumulative member (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1601-1616`). |

The harness supplies only declaration identity and the computed guard snapshot; it does not supply
outcome values or membership switches. The self-test explicitly rejects the former `guards`,
`include_order_notional`, `admitted`, and `include_cumulative_funding` authoring arguments
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1180-1201`).

## Verification

### Legacy replay after every outcome commit

The local legacy replay was run after each commit. Captured outputs were:

| Commit | Measured result |
|---|---|
| `de3c1d8e` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| `bf6d7923` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| `cbac9569` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| `e49b514e` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| `7bc9e0ec` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| `ef9ce894` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |

The final canonical receipt independently records producer `KERNEL_1`, status `MATCH`, 17 scenarios,
and 34 surfaces (`W304_GATE_RECEIPT.json:671-675`).

### Contract and verifier self-tests

Command:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
```

Measured output: `292 passed in 4.41s`.

Command:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
```

Measured output: 18 checks, each `PASS` or `DETECTED`; claim label `NON_ACCEPTING_SELFTEST`.

### Canonical gate — invoked once at the end

Command:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN --output C:\WP012BUILD\W304_GATE_RECEIPT.json
```

Invocation count: **1**. It returned nonzero and persisted a 69,746-byte receipt with SHA-256
`4444DD65BF2F984427FD0D4659C89B14E9B6EFFEFB6FC0AA4FDEB2E75F2897F8`. The receipt declares
`full-gate` mode and the refused claim label (`W304_GATE_RECEIPT.json:594-600,671-677`). Scenario
families RULE2-01 through RULE2-07 have `corrected_expectation: MATCH` and no first corrected mismatch in their scenario records
(`W304_GATE_RECEIPT.json:890-892,954-956,1018-1020,1081-1083,1283-1285,1410-1412,1483-1485,1523-1525,1621-1623,1730-1732,1806-1808,1914-1916`). RULE2-08 does not
(`W304_GATE_RECEIPT.json:1990-2014,2017-2019,2076-2078`).

Full refusal list, preserving receipt order (`W304_GATE_RECEIPT.json:778-886`):

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` — `semantic_coverage_review.json`.
2. `EXPECTED_PATH_CHANGED_AFTER_BASE` — RULE2-01-GREEN expected path.
3. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-01-A`.
4. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-01-B`.
5. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-02-A`.
6. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-04-A`.
7. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-05-A`.
8. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-05-B`.
9. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-06-A`.
10. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-07-A`.
11. `PROBE_COULD_NOT_EVALUATE` / `PROBE_BASE_TREE_OID_MISMATCH` — `PROBE-P012-08-A`.
12. `CLOSED_SET_VIOLATION` — RULE2-08-RED missing `/RESULT_SURFACE/cumulative_funding`.
13. `CLOSED_SET_VIOLATION` — RULE2-08-GREEN missing `/RESULT_SURFACE/cumulative_funding`.
14. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-08-RED `/EVENT_SURFACE/cash_events`.
15. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-08-RED `KeyError: 'cumulative_funding'`.
16. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-08-GREEN `/EVENT_SURFACE/decision_events`.

## Finding 2 — row 7 stop

Both sealed catalog rows point to sealed input files and pin their digests
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:649-676,692-719`).
Each input does contain `funding_tick_event_id: TEST-FUND-1`, but also binds
`cost_schedule_id` and `cost_schedule_sha256` to null while its ordinary bars construct lifecycle
state (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/inputs/RULE2-08-RED.json:1`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/inputs/RULE2-08-GREEN.json:1`).

The harness already gives the runner those records and executes the sealed bars
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1380-1402`).
The runner itself reads the funding schedule events and submits `FUNDING_TICK` intents between bars
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:671-746,770-777`). The failure is
therefore not an omitted harness feed. The preceding state-building OPEN is refused whenever the
cost record is absent (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:616-626`).
The current receipt consequently observes no cash/funding result and stops on the RULE2-08 nodes
(`W304_GATE_RECEIPT.json:860-886,1989-2014,2016-2078`).

Owner action is required to reconcile the sealed lifecycle construction with the no-cost-schedule
contract. Adding a state seed is expressly prohibited by this lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:24-25`) and conflicts with the owner
binding that GREEN lifecycle state be built by ordinary price bars with nothing injected
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:218-230`).

## Discrepancies

### D1 — the row-7 prompt diagnosis is not the repository's failure

The prompt says live execution supplies no funding event and directs the harness to feed it if the
sealed input contains it (`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:24-25`). The
sealed input does contain the event id, and the runner already consumes funding schedule events as
described above. The repository's own derivation record explicitly identifies the real conflict:
RULE2-08's owner-bound pre-window fills require a cost schedule, while the design binds the schedule
absent/`NOT_CONSUMED`; a strict run therefore refuses the pre-window entry
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:1731-1741`).
That repository evidence wins under C-2 (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).

The design itself exposes the same tension: it says neither RULE2-08 vector contains a fill intent
and consumes no `CostSchedule` (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:441-445`),
but its later scenario binding builds RED with a pre-window open and GREEN with a pre-window closed
lifecycle while keeping C absent/`NOT_CONSUMED`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:923-930`).

### D2 — the prompt's two-refusal gate prediction was stale

The prompt predicts only the review and provenance refusals if earlier lanes landed
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:27-32`). The measured receipt contains
16 refusal records: those two, nine probe base-tree OID mismatches, and five RULE2-08 records
(`W304_GATE_RECEIPT.json:778-886`). The kernel edits necessarily changed the base tree after the
sealed probe identities, so the probe set could not evaluate; probe/catalog/seal bytes were outside
this lane's authorized scope (`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:7-9`).

### D3 — conditional kernel membership needs sealed declaration metadata

The prompt labels rows 1-5 `KERNEL` and says harness bytes may change only on a row named harness
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W304_PRODUCER_CONTRACT.md:7-9,17-25`). The repository's
`PortfolioState` contains computed economic state but no scenario or owning-DEF declaration
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:400-447`), while the design makes
`order_notional` and `guards` membership conditional on the *declared* projection
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1190-1203`). The producer therefore cannot
choose the closed member set from computed state alone without guessing from values or record names.

The implementation transports only the sealed catalog's existing `owning_def_ids` and, for the
declared guard projection, the runner's computed guard snapshot
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1403-1415`).
No value or positive/negative outcome is passed. This generic declaration transport required a
harness call-site edit for rows 1-3 even though their economic logic and serialization remain in the
kernel. The discrepancy is disclosed here rather than hidden under the row-owner label.

## Exact changed paths

Substantive commits changed only:

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`

Evidence output adds only:

- `W304_GATE_RECEIPT.json`
- `W304_PRODUCER_CONTRACT_REPORT.md`

The evidence commit containing this report and receipt is the final lane commit; its immutable hash
is reported in the handoff chat because a commit cannot truthfully contain its own hash.

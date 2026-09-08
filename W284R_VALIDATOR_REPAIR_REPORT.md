# W284R Validator Repair Report

Path convention: shortened citations below expand as follows. `verify_bceg.py` means
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`;
`test_verify_bceg.py` means that directory's
`contracts/selftests/test_verify_bceg.py`; `core/results.py` means
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py`; corrected golden, observed,
and catalog citations are relative to `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`;
root report/receipt citations are relative to `C:\WP012BUILD`; and lane/W301/design citations are
relative to `C:\tmp\LANE_PROMPTS_20260828` unless an absolute path is shown.

## Verdict

**BLOCKED -- no validator repair was made.** The repository evidence contradicts the lane premise:
the canonical gate validates freshly executed `KERNEL_2` surfaces, and those live surfaces really do
omit the members or carry the tokens that the validator reports. The pipeline executes the scenario
and passes that exact result to the closed-set validator
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3297-3306`).
W301 instead triaged the committed observed artifacts and warned that they may predate the latest
kernel repairs (`C:\tmp\LANE_PROMPTS_20260828\_packets_W301\W301_REPORT.md:5-13,181-192`). C-2 says
the repository wins when it disagrees with the prompt
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).

The current validator already satisfies all four requested behaviors: it accepts a present required
member, refuses an absent required member, accepts the design tokens `PROTECTIVE_STOP` and
`time_stop`, and refuses a token outside the domain. Its member checks are direct dictionary-set
checks, not JSON-pointer lookup (`verify_bceg.py:595-615`), and its exit-reason domain already contains
`PROTECTIVE_STOP`, `TARGET`, and `time_stop` (`verify_bceg.py:843-854`). Therefore no honest RED
exists on the pre-edit validator, and changing it to make the live refusals disappear would weaken
the W284 check or substitute stale committed observations for live kernel bytes. The lane expressly
forbids weakening and requires preservation of the shaping removal
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W284R_VALIDATOR_REPAIR.md:29-34`).

The one permitted canonical gate was still run once. It refused with 42 records: 24 KERNEL/producer
records, 17 HARNESS/process/package records, and 1 GOLDEN provenance record. The exact receipt is
`W284R_GATE_RECEIPT.json`; its refusal label is persisted at `W284R_GATE_RECEIPT.json:739`, its
legacy reproduction is `MATCH` for 17 scenarios and 34 surfaces at
`W284R_GATE_RECEIPT.json:811-815`, and its complete refusal array is at
`W284R_GATE_RECEIPT.json:918-1167`.

## Scope and preflight

- The lane authorizes only `verify_bceg.py`, its corrected-vNext selftests/validators, the receipt,
  and this report; kernel, golden, catalog, input, baseline, seal, probe, and design bytes are
  forbidden (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284R_VALIDATOR_REPAIR.md:3-9,39-44`).
- `W299_DONE.txt` existed and contained `exit=0` (`C:\tmp\LANE_PROMPTS_20260828\W299_DONE.txt:1`);
  the worktree was clean and the branch was
  `feature/wp-p0-12-corrected-vnext-20260831` before the first write, as required by the lane
  (`LANE_W284R_VALIDATOR_REPAIR.md:4-7`).
- The W299 write lane is recorded as released with no tracked-file live/scheduled dependency at
  `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:33-37`. This lane has no broker, venue, host,
  deployment, credential, Pine, or live-trading dependency.
- Gate-1 tier is T1: the potential write was a non-economic verifier/harness script, while every
  economic/kernel path remained read-only. No other assistant, agent, model, or CLI was invoked,
  as C-1 requires (`N_COMMON_CLAUSES.md:3-7`).
- Starting HEAD was `caef68562a0227aa6a2d6c563a297938030c1128`; local and remote-tracking
  `master` were both `4ca0e5e85b5b2e070fe5a3798a84214d36060f8c`, and the merge base was
  `108ea066a710ff7ef5c09246903fe3d523da1d56` (measured before the report write).

## Byte diagnosis

### The actual document flow

The decisive source line is:

```text
corrected = execute_corrected_scenario(root, row)
```

That live document is immediately sliced to `EVENT_SURFACE` and `RESULT_SURFACE` and validated
(`verify_bceg.py:3297-3306`). `execute_corrected_scenario` runs the current `Runner`, calls the core
serializer, and returns those surfaces as producer `KERNEL_2`
(`verify_bceg.py:1357-1425`). This is also the invariant W284 was ordered to enforce: "observed =
kernel output bytes, expected = sealed bytes, nothing in between"
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:21-24`). The carried regression
requires the comparison pipeline to execute each row and observe its changed output
(`test_verify_bceg.py:730-857`).

By contrast, the three committed observed files sampled below were last produced by the older
observation path. They still contain now-forbidden old shapes such as `details` and
`funding_included_in_guard_basis` on their single JSON line
(`tests/corrected_vnext/observed/2.0.0/RULE2-01-RED.json:1`;
`tests/corrected_vnext/observed/2.0.0/RULE2-07-GREEN.json:1`). W301 explicitly based its triage on
those committed files (`W301_REPORT.md:5-13`).

### Three token-by-token traces

The following is the measured output of one read-only diagnostic command. Each token was resolved
against the sealed golden, W301's committed observed artifact, and the live document actually passed
to the validator. The source paths come from each catalog row; the live source is the execution path
at `verify_bceg.py:3297-3306`.

```text
RULE2-01-RED /RESULT_SURFACE/order_notional
  GOLDEN:             RESULT_SURFACE present -> order_notional present -> 1000
  COMMITTED_OBSERVED: RESULT_SURFACE present -> order_notional present -> 1000
  LIVE_GATE_DOCUMENT: RESULT_SURFACE present -> order_notional ABSENT
  validator(golden): ACCEPTED
  validator(live):   REFUSED missing member order_notional

RULE2-04-RED /EVENT_SURFACE/exit_events/0/reason
  GOLDEN:             EVENT_SURFACE present -> exit_events present -> [0] present -> reason PROTECTIVE_STOP
  COMMITTED_OBSERVED: EVENT_SURFACE present -> exit_events present -> [0] present -> reason PROTECTIVE_STOP
  LIVE_GATE_DOCUMENT: EVENT_SURFACE present -> exit_events present -> [0] present -> reason STOP
  validator(golden): ACCEPTED
  validator(live):   REFUSED unknown reason 'STOP'

RULE2-07-GREEN /RESULT_SURFACE/guards
  GOLDEN:             RESULT_SURFACE present -> guards present -> object with 4 members
  COMMITTED_OBSERVED: RESULT_SURFACE present -> guards present -> obsolete object with 6 members
  LIVE_GATE_DOCUMENT: RESULT_SURFACE present -> guards ABSENT
  validator(golden): ACCEPTED
  validator(live):   REFUSED missing member guards
```

The golden values are persisted at `golden/corrected_vnext/RULE2-01-RED.json:40`,
`golden/corrected_vnext/RULE2-04-RED.json:41`, and
`golden/corrected_vnext/RULE2-07-GREEN.json:37-42`. The live findings are persisted in the gate
receipt at `W284R_GATE_RECEIPT.json:1001-1006,1025-1030,1055-1060`. The core serializer itself maps
protective-stop and market-exit classes to `STOP` and `MARKET_EXIT`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:655-674`), while carried tests
prove the raw harness path does not inject guards and does not rewrite `STOP`
(`test_verify_bceg.py:1202-1215,1458-1467`).

### Minimized present/missing and token-domain checks

The lane-requested test seam was already fixed by the prompt, so no additional seam confirmation was
needed (`LANE_W284R_VALIDATOR_REPAIR.md:27-34`). A minimized read-only check copied sealed goldens in
memory and produced:

```text
ACCEPTED present member /RESULT_SURFACE/order_notional value=1000
DETECTED missing member at /RESULT_SURFACE/order_notional
ACCEPTED design token RULE2-04-RED reason='PROTECTIVE_STOP'
ACCEPTED design token RULE2-07-RED reason='time_stop'
DETECTED outside token at /EVENT_SURFACE/exit_events/0/reason
```

The independent expected values are in `RULE2-01-RED.json:40`, `RULE2-04-RED.json:41`, and
`RULE2-07-RED.json:44`; the validator implementation is at `verify_bceg.py:595-625,843-875`.
Deleting the first golden member and replacing the reason with `OUTSIDE_DESIGN_DOMAIN` were the two
modified-copy arms. Both were DETECTED at the exact pointer. The unmodified controls were accepted.

## Root cause

**The root cause is an artifact-source error in W301/the W284R premise, not a validator defect.**
W301 resolved pointers against old committed observation artifacts, while the gate resolves and
validates freshly executed output. The prompt then attributed the committed-file values to the
validator's live document (`LANE_W284R_VALIDATOR_REPAIR.md:12-22`). The live document differs because
W284 deliberately removed harness shaping, and the carried tests explicitly require the raw output
to omit conditional result members and preserve raw exit reasons
(`test_verify_bceg.py:1166-1221,1388-1421,1458-1519`).

This diagnosis falsifies the three proposed validator causes:

1. JSON-pointer resolution is not involved in the closed-member decision; the validator compares
   dictionary key sets directly (`verify_bceg.py:595-615`).
2. The closed-set table admits the design tokens and required scenario-conditioned members
   (`verify_bceg.py:843-875`).
3. The gate loads the intended live producer through `execute_corrected_scenario`; substituting the
   unsealed, stale observed artifact would violate W284 item 5 and the live-execution regression
   (`verify_bceg.py:1357-1425,3297-3314`; `test_verify_bceg.py:730-857`).

## Diff

No code or selftest byte changed. In particular, `verify_bceg.py`, provenance predicates, legacy
reproduction, blocked-node accounting, shaping-removal tests, kernel, golden, catalog, input,
baseline, seal, probe, and design files are unchanged. The only lane outputs are:

- `W284R_GATE_RECEIPT.json` -- exact JSON emitted by the one canonical gate.
- `W284R_VALIDATOR_REPAIR_REPORT.md` -- this report.

A code change was withheld because the requested behavior is already green and the repository
requires real RED-before-GREEN evidence for a closure claim
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/TESTS.md:3-6`).

## RED/GREEN and verification

### Requested new regressions

No new regression was committed. The pre-edit validator accepted both positive controls and detected
both modified copies, so a pre-fix RED could not be shown honestly. A test added now would be green
before and after and therefore would not be defect-closure evidence. This is the required STOP under
the lane's "Show RED on the pre-fix validator" rule
(`LANE_W284R_VALIDATOR_REPAIR.md:29-34`) and the stage's RED/GREEN requirement
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/TESTS.md:3-6`).

### Carried suite

Commands ran from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`; package tests and verifiers are
expressly allowed (`N_COMMON_CLAUSES.md:33-36`).

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
281 passed in 4.57s

python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
18/18 checks passed or detected their declared refusal
claim_label=NON_ACCEPTING_SELFTEST
```

The non-weakening regressions that refuse an extra member and a missing member remain at
`test_verify_bceg.py:1106-1163`; raw-output/shaping-removal fences remain at
`test_verify_bceg.py:1166-1221,1405-1519`.

### Canonical gate -- exactly one invocation

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate \
  --baseline-root C:\tmp\P012_BASELINE_RUN \
  --output C:\WP012BUILD\W284R_GATE_RECEIPT.json
```

Measured receipt identity:

```text
sha256=73557864ca50688094ea6629cfaafd22fd0fa663b9435c4c40a152234b02affe
bytes=73641
lines=2166
claim_label=BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
refusals=42
acceptance_blockers=41
blocked_node_skips=96
legacy_reproduction=MATCH; scenarios=17; surfaces=34
```

The claim label and legacy counts are persisted at `W284R_GATE_RECEIPT.json:739,811-815`; the
blocked-node accounting starts at `W284R_GATE_RECEIPT.json:249`; the refusal list starts at
`W284R_GATE_RECEIPT.json:918`. The shell wrapper surfaced a non-zero status as exit 1; the exact
Python process exit code is NOT VERIFIED because `main()` returns 2 for a refusing full gate at
`verify_bceg.py:3555-3561`.

## Full refusal list before

W284 recorded 42 refusals grouped without omission at
`W284_HARNESS_FLAGSHIP2_REPORT.md:102-149`:

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` -- `semantic_coverage_review.json`.
2. `EXPECTED_PATH_CHANGED_AFTER_BASE` -- RULE2-01-GREEN golden path.
3. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-01-A.
4. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-01-B.
5. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-02-A.
6. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-04-A.
7. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-05-A.
8. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-05-B.
9. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-06-A.
10. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-07-A.
11. `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH` -- PROBE-P012-08-A.
12. `CLOSED_SET_VIOLATION` -- RULE2-01-RED `/RESULT_SURFACE/order_notional`.
13. `CLOSED_SET_VIOLATION` -- RULE2-01-GREEN `/RESULT_SURFACE/order_notional`.
14. `CLOSED_SET_VIOLATION` -- RULE2-02-RED `/RESULT_SURFACE/order_notional`.
15. `CLOSED_SET_VIOLATION` -- RULE2-02-GREEN `/RESULT_SURFACE/admitted`.
16. `CLOSED_SET_VIOLATION` -- RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`, `STOP`.
17. `CLOSED_SET_VIOLATION` -- RULE2-05-RED `/RESULT_SURFACE/order_notional`.
18. `CLOSED_SET_VIOLATION` -- RULE2-05-GREEN `/RESULT_SURFACE/order_notional`.
19. `CLOSED_SET_VIOLATION` -- RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`, `STOP`.
20. `CLOSED_SET_VIOLATION` -- RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`, `MARKET_EXIT`.
21. `CLOSED_SET_VIOLATION` -- RULE2-07-GREEN `/RESULT_SURFACE/guards`.
22. `CLOSED_SET_VIOLATION` -- RULE2-08-RED `/RESULT_SURFACE/cumulative_funding`.
23. `CLOSED_SET_VIOLATION` -- RULE2-08-GREEN `/RESULT_SURFACE/cumulative_funding`.
24. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-01-RED `/RESULT_SURFACE/order_notional`.
25. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-01-GREEN `/RESULT_SURFACE/order_notional`.
26. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-02-RED `/RESULT_SURFACE/order_notional`.
27. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-02-GREEN `/RESULT_SURFACE/admitted`.
28. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`.
29. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-05-RED `/RESULT_SURFACE/order_notional`.
30. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-05-GREEN `/RESULT_SURFACE/order_notional`.
31. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
32. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-EQUAL-PRICE-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
33. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`.
34. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`.
35. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-07-GREEN `/RESULT_SURFACE/guards`.
36. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-08-RED `/EVENT_SURFACE/cash_events`.
37. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-08-GREEN `/EVENT_SURFACE/decision_events`.
38. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-01-RED `KeyError: 'order_notional'`.
39. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-01-GREEN `KeyError: 'order_notional'`.
40. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-07-RED `KeyError: 'guards'`.
41. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-07-GREEN `KeyError: 'guards'`.
42. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-08-RED `KeyError: 'cumulative_funding'`.

## Full refusal list after

The following is the exact emitted order from `W284R_GATE_RECEIPT.json:918-1167`:

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` -- `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json`.
2. `EXPECTED_PATH_CHANGED_AFTER_BASE` -- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`.
3. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-01-A.
4. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-01-B.
5. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-02-A.
6. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-04-A.
7. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-05-A.
8. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-05-B.
9. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-06-A.
10. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-07-A.
11. `PROBE_COULD_NOT_EVALUATE / PROBE_CATALOG_DIGEST_MISMATCH` -- PROBE-P012-08-A.
12. `CLOSED_SET_VIOLATION` -- RULE2-01-RED `/RESULT_SURFACE/order_notional`, missing.
13. `CLOSED_SET_VIOLATION` -- RULE2-01-GREEN `/RESULT_SURFACE/order_notional`, missing.
14. `CLOSED_SET_VIOLATION` -- RULE2-02-RED `/RESULT_SURFACE/order_notional`, missing.
15. `CLOSED_SET_VIOLATION` -- RULE2-02-GREEN `/RESULT_SURFACE/admitted`, missing.
16. `CLOSED_SET_VIOLATION` -- RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`, `STOP` unknown.
17. `CLOSED_SET_VIOLATION` -- RULE2-05-RED `/RESULT_SURFACE/order_notional`, missing.
18. `CLOSED_SET_VIOLATION` -- RULE2-05-GREEN `/RESULT_SURFACE/order_notional`, missing.
19. `CLOSED_SET_VIOLATION` -- RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`, `STOP` unknown.
20. `CLOSED_SET_VIOLATION` -- RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`, `MARKET_EXIT` unknown.
21. `CLOSED_SET_VIOLATION` -- RULE2-07-GREEN `/RESULT_SURFACE/guards`, missing.
22. `CLOSED_SET_VIOLATION` -- RULE2-08-RED `/RESULT_SURFACE/cumulative_funding`, missing.
23. `CLOSED_SET_VIOLATION` -- RULE2-08-GREEN `/RESULT_SURFACE/cumulative_funding`, missing.
24. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-01-RED `/RESULT_SURFACE/order_notional`.
25. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-01-RED `KeyError: 'order_notional'`.
26. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-01-GREEN `/RESULT_SURFACE/order_notional`.
27. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-01-GREEN `KeyError: 'order_notional'`.
28. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-02-RED `/RESULT_SURFACE/order_notional`.
29. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-02-GREEN `/RESULT_SURFACE/admitted`.
30. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`.
31. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-05-RED `/RESULT_SURFACE/order_notional`.
32. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-05-GREEN `/RESULT_SURFACE/order_notional`.
33. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
34. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-EQUAL-PRICE-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
35. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`.
36. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`.
37. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-07-RED `KeyError: 'guards'`.
38. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-07-GREEN `/RESULT_SURFACE/guards`.
39. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-07-GREEN `KeyError: 'guards'`.
40. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-08-RED `/EVENT_SURFACE/cash_events`.
41. `RULE2_PROJECTION_COULD_NOT_EVALUATE` -- RULE2-08-RED `KeyError: 'cumulative_funding'`.
42. `CORRECTED_EXPECTATION_MISMATCH` -- RULE2-08-GREEN `/EVENT_SURFACE/decision_events`.

The only before/after movement is the nine probe inner refusals:
`PROBE_BASE_TREE_OID_MISMATCH` became `PROBE_CATALOG_DIGEST_MISMATCH`. The other 33 records remained
the same, as the W284 report and the new receipt show
(`W284_HARNESS_FLAGSHIP2_REPORT.md:128-149`; `W284R_GATE_RECEIPT.json:918-1167`).

## Residual classification

### Summary by refusal record

| Class | Count | Records |
|---|---:|---|
| KERNEL / producer | 24 | 10 closed-set, 10 corrected-expectation, 4 projection-could-not-evaluate |
| HARNESS / process / package | 17 | 1 review missing, 9 probe catalog pins, 2 closed-set, 4 corrected-expectation, 1 projection-could-not-evaluate |
| GOLDEN | 1 | RULE2-01-GREEN expected-path provenance |
| **Total** | **42** | Exact list at `W284R_GATE_RECEIPT.json:918-1167` |

The 31 corrected-output records collapse to the following 14 independently measured first
outcomes. `ABSENT` is a missing JSON member; `A:n` and `O:n` are the verifier's canonical array and
object cardinality forms (`verify_bceg.py:495-512`). Required conditional result membership is fixed
by the design extract at `C:\tmp\LANE_PROMPTS_20260828\_packets_W301\DESIGN_EXTRACT_22_23.md:84-140`.

| Scenario | Pointer | Golden | Live gate document | Class | Why |
|---|---|---|---|---|---|
| RULE2-01-RED | `/RESULT_SURFACE/order_notional` | `1000` | `ABSENT` | KERNEL | The raw producer omits a required conditional result member; core serialization is conditional at `core/results.py:837-850,924-944`. |
| RULE2-01-GREEN | `/RESULT_SURFACE/order_notional` | `100` | `ABSENT` | KERNEL | Same producer-schema defect; golden value at `RULE2-01-GREEN.json:40`. |
| RULE2-02-RED | `/RESULT_SURFACE/order_notional` | `100` | `ABSENT` | KERNEL | Same producer-schema defect; golden value at `RULE2-02-RED.json:34`. |
| RULE2-02-GREEN | `/RESULT_SURFACE/admitted` | `true` | `ABSENT` | KERNEL | Core emits `admitted` only when supplied by the producer owner at `core/results.py:970-973`; W284 forbids the verifier from authoring it. Golden values are at `RULE2-02-GREEN.json:40-41`. |
| RULE2-04-RED | `/EVENT_SURFACE/exit_events/0/reason` | `PROTECTIVE_STOP` | `STOP` | KERNEL | Core mapping is literal at `core/results.py:655-674`; golden value at `RULE2-04-RED.json:41`. |
| RULE2-05-RED | `/RESULT_SURFACE/order_notional` | `0` | `ABSENT` | KERNEL | The live value is not W301's stale `101`; the carried raw-output test requires absence at `test_verify_bceg.py:1470-1491`. |
| RULE2-05-GREEN | `/RESULT_SURFACE/order_notional` | `100` | `ABSENT` | KERNEL | Same producer-schema defect; the validator correctly reports absence. |
| RULE2-06-RED | `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id` | `TARGET_FIRST` | `ABSENT` | HARNESS | The harness constructs the manifest without passing the runner's actual policy at `verify_bceg.py:1402-1410`; no golden or kernel byte was changed. |
| RULE2-06-EQUAL-PRICE-RED | `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id` | `TARGET_FIRST` | `ABSENT` | HARNESS | Same manifest pass-through omission. |
| RULE2-06-GREEN | `/EVENT_SURFACE/exit_events/0/reason` | `PROTECTIVE_STOP` | `STOP` | KERNEL | Same core token mapping at `core/results.py:655-674`. |
| RULE2-07-RED | `/EVENT_SURFACE/exit_events/0/reason` | `time_stop` | `MARKET_EXIT` | KERNEL | The design scenario binds `MARKET_EXIT/TIME_STOP/time_stop` at `P012_FRESH_DESIGN_V1.md:927`; core serializes the class token at `core/results.py:660-674`. |
| RULE2-07-GREEN | `/RESULT_SURFACE/guards` | `O:4` | `ABSENT` | KERNEL | The raw producer omits guards, proven by the carried test at `test_verify_bceg.py:1458-1467`; golden object starts at `RULE2-07-GREEN.json:37`. |
| RULE2-08-RED | `/EVENT_SURFACE/cash_events` | `A:1` | `A:0` | HARNESS | The live scenario setup produces no funding/cash event; the carried no-seed test pins that raw outcome at `test_verify_bceg.py:1504-1519`. Restoring the deleted state seed would violate W284 shaping removal. |
| RULE2-08-GREEN | `/EVENT_SURFACE/decision_events` | `A:2` | `A:1` | HARNESS | Same corrected scenario-execution setup mismatch; the sealed artifact records its second funding-eligibility row at `RULE2-08-GREEN.json:24-26`. |

These 14 outcomes generate 12 closed-set records, 14 first corrected mismatches, and 5 projection
evaluation records in the receipt (`W284R_GATE_RECEIPT.json:1001-1167`). They are not false reports
of members present in the live document.

### W299 probe catalog values

W299 re-derived the nine modified copies but explicitly left the catalog and sealed manifest at the
old digest pairs pending Lead steps 3-6 (`W299_PROBE_REPIN_REPORT.md:5-6,21-27,74-77`). The validator
compares catalog pins to the actual tree and modification-manifest digests at
`verify_bceg.py:2311-2337`. Thus all nine new `PROBE_CATALOG_DIGEST_MISMATCH` refusals are honest
HARNESS/package-pin findings, not probe OID findings.

| Probe | Pointer | Catalog value | Actual W299 value |
|---|---|---|---|
| PROBE-P012-01-A | `/17/modified_copy_digest`; `/17/modification_manifest_digest` | `0f956819c8b5d2a3a9c1776420f117b050b662fb1ff0aa1f63d819a382b84aca`; `50fc3ce1da1ca51feafc44dcd3c537e31d5547eec8c6f854f7260f80f8b8c4c8` | `7b93a0dd06421ae979d0dc6736402d778cada45d2fc7aba4767ebb029093d12a`; `a2329ab11a87751862453cad8942332b3b54108c9f294656635a7eb9f849c87e` |
| PROBE-P012-01-B | `/18/modified_copy_digest`; `/18/modification_manifest_digest` | `e5fc81ec6bac4b93e490ffc538586a253423003f2cd3930331b67e61a5d82f08`; `8686e9c8f5a8af557f9ecae1b0cf6ba81e6b0af9ee50af303f5ea48c4efef07a` | `d8eae81dbcc4648a1a8dafa65c890e713eed965129002118c14330abb6c9aad6`; `cab810b62324678258bea30250788bb8f4c6097d75d50bdf3ad075664beff762` |
| PROBE-P012-02-A | `/19/modified_copy_digest`; `/19/modification_manifest_digest` | `34e963a8b75209f7a8ab77aeb3d3834251f1bc6847cc2875ec6ba36275e3df25`; `80a66bec7ea77b64897820c4a429e687a2c20e2b90c4860c34ac01ad98de5d5e` | `ff4592347f00b7187513665a07c02d4d7108909de9796cb6fd7527da2d4d941f`; `eebbcde982c72aec02584714cfbba0bf10468249576411649a2bbb0617d1240f` |
| PROBE-P012-04-A | `/21/modified_copy_digest`; `/21/modification_manifest_digest` | `d6082460482da78706d50b3c52176f0bba8fadbc1492456b721178daa84196f8`; `e2c09190b4e32c0f9605d5cc54ad26957b5292e9e8cef49d097070e85892b5dc` | `dc313ee4328eecaad6ef34408cd4ab4838254589e213e4448c3540f71cf5ba92`; `9f44a7cd0ed4b6984232455bfe118904d05eefa7976f96127caf67a4cdc64102` |
| PROBE-P012-05-A | `/22/modified_copy_digest`; `/22/modification_manifest_digest` | `1336f129f33de9ea1c4866fce91077e8a55e03e30266e56e9ca20dc5b178ed54`; `7862007188811445a3a7df11063e36dd5048f924c1af9259e246afd0256ae494` | `216152ca35050558068fc24e1d64df7473296a6b7048c1b3515720dbf8f8d294`; `684637b72cf10ceaf740452b46878427bce8dd33855c64ec23670e9e5b9cc81c` |
| PROBE-P012-05-B | `/23/modified_copy_digest`; `/23/modification_manifest_digest` | `b06895e2543d4f768563d618fe99669f788a1fbaddf317d81d5553c84f71900b`; `4bd13c499516a61c12313da4fdaba2c122b37782911893f0a81fcb0ee794d67e` | `009890b989aeba839d40585a6b1a489a1e26ae0928d543fbba56a7b449ac1b79`; `ecb0bc2559c65ed920128adb085ff1c97726f7595ca002748e5c70563c7824da` |
| PROBE-P012-06-A | `/24/modified_copy_digest`; `/24/modification_manifest_digest` | `ad1ec938b0654ba58bc8bc90e9fad1a9781a2070b7f3951794181deb7fb6450c`; `427b29ce60b21ce0a261f35c468392b050d38366b3c986c676adeea43f8e13d7` | `fa51d604ef31863ae91f932ef32e95b2a9d72a0a924acdb0406fcadc4f371841`; `f54132eda453169414d4e7c16e70edfe257f55ccb3f1ec1c7bfc2f1e59610902` |
| PROBE-P012-07-A | `/25/modified_copy_digest`; `/25/modification_manifest_digest` | `dbef7fad26afb8c40beb049770bf867f4a492cb10025a629341eb3fef1b1b1bb`; `f9897b826a9657e3937bcb794a0d59df0c6021a4e729edad3e3608f6f7c34914` | `ea91b62f48edbb9ff15072a763f7255daf88c067bcab9645e7d3b4fc5b63e4da`; `c9f81cec21a789f4131f333a501b8260ef8ca3ede884df6b197eef3ab9a6a1e5` |
| PROBE-P012-08-A | `/26/modified_copy_digest`; `/26/modification_manifest_digest` | `f97ce0655b57fee069a161b6584534e299d19253eac4c56aa5da0197f03a62c6`; `e466e79458bcc5368b2f9c2ecb0b314bc0825f71638d39327a1842031f446a9f` | `48e63ab55bbd160d0d5f2b50747aac65674af91893dc35ce796d6bd1cfc8b95a`; `d976769490645ea5fefefbe7e44b0921807bdc561b3f9e77293601f8068823c9` |

The full catalog values are at `scenario_catalog.json:735-748,756-769,777-790,819-832,840-853,
861-874,882-895,903-916,924-937`; the full actual pairs are at
`W299_PROBE_REPIN_REPORT.md:29-39`. Catalog/probe edits were forbidden in this lane.

### Known review and golden records

- `SEMANTIC_COVERAGE_REVIEW_MISSING` is a HARNESS/process refusal and is still first in the receipt
  (`W284R_GATE_RECEIPT.json:918-922`). The lane prediction expected it
  (`LANE_W284R_VALIDATOR_REPAIR.md:35-38`).
- `EXPECTED_PATH_CHANGED_AFTER_BASE` remains the one GOLDEN provenance record for
  RULE2-01-GREEN (`W284R_GATE_RECEIPT.json:923-929`). W301 classifies it as an owner decision about
  the design-directed W156/W167/W172 revisions (`W301_REPORT.md:91-147`). No golden or provenance
  predicate was changed.

## Findings

1. **W284R-F01 -- W301 artifact-source misclassification.** W301 used committed observed files,
   while the gate validates fresh execution; this made 31 live-output records look like false
   validator positives (`W301_REPORT.md:5-13,198-203`; `verify_bceg.py:3297-3342`).
2. **W284R-F02 -- live corrected producer still disagrees with the closed contract.** Ten unique
   KERNEL/producer outcomes generate 24 refusal records; the exact pointers and both values are in
   the residual table above and in `W284R_GATE_RECEIPT.json:1001-1167`.
3. **W284R-F03 -- W299 re-pin is intentionally incomplete at the catalog boundary.** Nine probe
   rows now refuse on old catalog digest pins, exactly as W299's report says they should until Lead
   steps 3-6 (`W299_PROBE_REPIN_REPORT.md:74-77`; `scenario_catalog.json:735-937`).
4. **W284R-F04 -- four additional harness outcomes remain outside a validator repair.** The two
   RULE2-06 manifest-policy omissions and two RULE2-08 execution-setup mismatches generate seven
   refusal records; fixing them by restoring scenario-shaped output is forbidden by W284 item 5
   (`LANE_W284_HARNESS_FLAGSHIP2.md:21-24`; `test_verify_bceg.py:1166-1221,1504-1519`).

## Discrepancies

1. **The "30 HARNESS false positives" premise is false for the live gate document.** The prompt says
   the nodes/tokens are present in both documents (`LANE_W284R_VALIDATOR_REPAIR.md:12-22`), but the
   gate passes freshly executed output at `verify_bceg.py:3297-3306`, and the receipt records the
   live absences/tokens at `W284R_GATE_RECEIPT.json:1001-1167`. W301 used committed artifacts and
   explicitly warned they might be stale (`W301_REPORT.md:5-13,181-192`).
2. **The requested pre-fix RED does not exist.** The current direct member/domain validator already
   satisfies every behavior in the prompt (`verify_bceg.py:595-625,843-875`). Both negative modified
   copies were DETECTED and both positive controls were accepted, so no code or test was changed.
3. **RULE2-05-RED is not currently golden `0` versus live `101`.** The prompt states that pair at
   `LANE_W284R_VALIDATOR_REPAIR.md:21-22`; the current raw executor produces quantity `0` and omits
   the top-level member, as the carried test requires at `test_verify_bceg.py:1470-1491`. The new
   receipt therefore reports missing/ABSENT, not value `101` (`W284R_GATE_RECEIPT.json:1031-1036,
   1108-1112`).
4. **W299 completion does not imply zero probe refusals.** The prompt predicts zero after re-pin
   (`LANE_W284R_VALIDATOR_REPAIR.md:35-38`), while W299 says the live catalog deliberately retains
   old digest pairs pending independent Lead work (`W299_PROBE_REPIN_REPORT.md:74-77`). The gate
   honestly reports nine `PROBE_CATALOG_DIGEST_MISMATCH` records
   (`W284R_GATE_RECEIPT.json:930-999`).
5. **The gate still has the same total count but not the predicted composition.** Before and after
   are both 42 records; nine probe inner codes moved, while all 31 corrected-output records remained
   (`W284_HARNESS_FLAGSHIP2_REPORT.md:110-149`; `W284R_GATE_RECEIPT.json:918-1167`).
6. **The stage normally carries accepted current state in `HANDOFF.md`, but this lane does not
   authorize that path.** The exact whitelist and required outputs are at
   `LANE_W284R_VALIDATOR_REPAIR.md:7-9,39-44`; `HANDOFF.md` was left unchanged.
7. **Independent acceptance is unavailable inside this lane.** Repository policy separates
   implementer QA from independent acceptance, while C-1 forbids invoking any other model
   (`N_COMMON_CLAUSES.md:3-7`). This report makes no G5/G6 acceptance claim.

## Commits and handoff

- W284 closed-set validator commit:
  `7f659fd5e0b6e37ee30079288f37633a85799356` (`W284_HARNESS_FLAGSHIP2_REPORT.md:48-56`).
- W284 shaping-removal commit:
  `213875dfc0a6ffc707dd060a16abefa71652ad5c` (`W284_HARNESS_FLAGSHIP2_REPORT.md:68-76`).
- W299 substantive re-pin commit:
  `28606f2f7a32bc87b8fe8fe4b2f94e688f97a49e`
  (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:37`).
- W284R starting parent:
  `caef68562a0227aa6a2d6c563a297938030c1128`.
- This report and `W284R_GATE_RECEIPT.json` are committed together; the resulting commit SHA is the
  lane's final HEAD and is reported in chat because a Git commit cannot contain its own SHA.

No push, merge, pull request, backtest, optimization, server, launcher, registry rebuild, host,
broker, venue, credential, Pine, golden, catalog, input, baseline, seal, probe, design, or kernel
write occurred. A later lane must not "repair" the validator by reading the stale committed observed
artifacts. The owner/Lead must instead disposition the live producer findings, the four harness
execution/pass-through findings, the W299 catalog reseal sequence, and the one golden provenance
question under their existing protected-scope gates.

## NOT VERIFIED

- Independent G5/G6 acceptance is NOT VERIFIED and was not attempted because C-1 prohibits another
  assistant/model (`N_COMMON_CLAUSES.md:3-7`).
- The exact Python child-process exit code from the refusing gate is NOT VERIFIED; the shell wrapper
  surfaced exit 1 while `main()` returns 2 for a non-accepting full-gate receipt
  (`verify_bceg.py:3555-3561`). Receipt content and identity are persisted and verified.
- No claim is made that any KERNEL, GOLDEN, catalog, probe, or review finding is repaired. Those
  paths were outside this lane's write authority (`LANE_W284R_VALIDATOR_REPAIR.md:7-9`).

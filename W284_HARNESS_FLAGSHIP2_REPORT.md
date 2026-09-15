# W284 Harness Flagship-2 Repair Report

## Verdict

The seven ordered repair items are implemented in seven commits, their regression tests were run RED then GREEN, and the final contract suite passes 281 tests. The one permitted canonical full-gate run refused with `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED`: 42 refusal records across six check classes. This is an honest non-accepting result, not a request to relax the new checks. The lane requires findings from new checks to be reported rather than weakened (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:28-34`).

The work stayed on `feature/wp-p0-12-corrected-vnext-20260831`; the guard passed before each commit and after the seventh commit. No push, merge, pull request, backtest, server, artifact generation, or external writer was used. Those boundaries are required by `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`.

## Scope and preflight

- `C:\tmp\LANE_PROMPTS_20260828\W285_DONE.txt` existed before edits, the starting tree was clean, and the branch was not `master`, satisfying the lane precondition (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:3-7`).
- The primary tier was T0 because item 0 changed the economic kernel; the remaining changes were harness, verifier self-tests, gate-side validation, the exact manifest copy, and this required report. The lane expressly authorizes the item-0 kernel/harness pair and fences every other non-harness byte (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:8-12,18-24`).
- No golden, catalog, input, baseline, seal, or design byte changed. The only non-harness data change is `contracts/CONTRACT_TABLES_MANIFEST.json`, as item 6 permits (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:9,24`).
- No other assistant, model, or CLI was invoked, per C-1 (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

## Item-by-item implementation and RED/GREEN evidence

### 0 - Remove the corrected-contract constructor

Design cite: section 18 enumerates `core/runner.py` work but declares no fixture constructor (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:646-665`).

Diff: removed `Runner.for_corrected_contract` and its four economic override fields/branches from the protected kernel. The remaining constructor initializes ordinary corrected records/state only (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:133-165`). The harness now creates `EconomicIntent` directly and applies the resulting transition (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1204-1275`), including harness-owned entry and target scenarios (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1279-1315`).

RED/GREEN: `test_runner_exposes_no_economic_input_bearing_constructor` failed before removal because the attribute existed, then passed (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:76-77`). The item suite finished at 268 passed. The frozen replay then matched 17/17 scenarios and 34/34 event/result surfaces byte-exact; the in-gate implementation now measures the same pair (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1626-1675`).

Commit: `7a23a1cd0f279d7e3b27073c781732a89888a422` (`fix(mtc-v2): remove corrected contract constructor`). This was the required atomic kernel-plus-harness commit (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:18`).

### 1 - Perform legacy reproduction inside the gate

Design cite: `KERNEL_1` is actual exact-`1.0.0` output, and the legacy row requires all nodes on both surfaces to equal `BASELINE_BYTES`; its fail input is one actual float changed by one ULP (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:453-461,547-556`).

Diff: the verifier loads the digest-bound frozen driver, executes the live legacy `Runner`, and labels provenance `EXECUTED_KERNEL_1` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1525-1577,1580-1623`). It compares canonical actual bytes to each frozen baseline file and records both SHA-256 values; a mismatch returns `LEGACY_REPRODUCTION_MISMATCH` at the first differing node (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1626-1675`).

RED/GREEN: the one-ULP actual mutation was not detected by the parent harness; after the repair, `test_legacy_reproduction_refuses_one_ulp_actual` passed with `/RESULT_SURFACE/account/equity` as the exact pointer (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:860-888`). The item suite finished at 269 passed.

Commit: `1f18841b25e3591795d2acce73430ae5b31e5bac` (`fix(mtc-v2): enforce legacy reproduction gate`).

### 2 - Account for every blocked expected node

Design cite: section 15.5 says what an accepting receipt means, including the prior unbounded “every node” sentence (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:575-588`).

Diff: every skipped `BLOCKED-` value now produces `{scenario_id, pointer, expected_marker}` accounting; the receipt records its count and declares `comparison_claim_scope=ALL_NON_BLOCKED_EXPECTED_NODES` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1705-1728,1775-1783`). Both accepting/refusal labels were narrowed to `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_*` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:53-54`).

RED/GREEN: the regression initially failed because the receipt had no `blocked_node_skips` accounting and retained the over-broad label. It then passed exact shape, count, marker, and claim-scope checks (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:890-918`). The item suite finished at 270 passed.

Commit: `5aa84aae359d7f00583e4f393aba227c6ed0b4a9` (`fix(mtc-v2): account for blocked comparison nodes`).

### 3 - Validate corrected closed sets on the gate side

Design cite: section 23.3 closes fill and exit members and refuses unknown/wrongly conditional members (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1121-1161`); section 23.4 closes result, trade, guard, refusal, and conditional top-level members (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1163-1234`).

Diff: `validate_corrected_closed_sets` independently validates the six event containers, decision/fill/cash/fee/funding/exit objects, result conditionals, trades including v1.12 quantity, guards, refusals, and discriminator domains (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:630`). The comparison pipeline invokes it before expected-value comparison and records `CLOSED_SET_VIOLATION` blockers (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3297-3310`).

RED/GREEN: an injected observed-only fill member and a deleted required `warnings` member both produced “DID NOT RAISE” before the validator. They now refuse at `/EVENT_SURFACE/fill_events/0/observed_only` and `/RESULT_SURFACE/warnings` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1106-1163`). The item suite finished at 272 passed.

Commit: `7f659fd5e0b6e37ee30079288f37633a85799356` (`fix(mtc-v2): validate corrected closed sets`).

### 4 - Enforce expected-source provenance

Design cite: section 15.4 requires independent method, implementation-base ancestry, and no expected-path changes after the base (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:558-566`).

Diff: the gate requires `INDEPENDENT_DERIVATION` and `not_method=COPY_OBSERVED`, refuses base/anchor disagreement or a non-ancestor base, and computes a Git diff over every expected member from implementation base to observed HEAD (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1818-1929`). Typed codes are `EXPECTED_PROVENANCE_METHOD_INVALID`, `IMPLEMENTATION_BASE_ANCESTRY_MISMATCH`, and `EXPECTED_PATH_CHANGED_AFTER_BASE` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1821-1842,1871-1923`).

RED/GREEN: the three regression inputs—`COPY_OBSERVED`, a non-ancestor base, and real post-base expected-path changes—failed to produce the required typed refusals before implementation, then all passed (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:554-594`). The item suite finished at 275 passed.

Commit: `ee534b7c81c89aa8e292d89f1fcb4093a33460db` (`fix(mtc-v2): enforce expected source provenance`).

### 5 - Stop verifier authoring and rewriting of observations

Design cite: `KERNEL_2` is actual corrected-adapter output and `GATE_READER` owns no expected values (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:453-462`); the version-shaped surfaces forbid reader synthesis or rewriting (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:501-509`).

Diff: removed `_refusal_surfaces`, `_normalize_exit_surface`, and `_prepare_rule2_08_observation`; removed scenario-string serializer arguments for refusals, guards, order notional, admitted, cumulative funding, and collision-policy manifest membership. `execute_corrected_scenario` now runs the chosen kernel path and returns the kernel serializer result without post-production rewriting (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1357-1425`). Gate-side schema validation and comparison remain outside that producer path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3297-3342`).

RED/GREEN: five parameterized checks first failed on forbidden serializer arguments, the rewritten stop reason, and the three literal/legacy-seed helpers. They now pass (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1169-1221`). Carried tests were updated to assert raw-kernel membership rather than the deleted harness shaping; the gate, not the observed producer, now reports design-shape failures. The item suite finished at 280 passed.

Commit: `213875dfc0a6ffc707dd060a16abefa71652ad5c` (`fix(mtc-v2): stop shaping observed surfaces`).

### 6 - Refresh the manifest and bind the live design pin

Design/task cite: item 6 requires the bundle manifest copied byte-for-byte and the live file's SHA-256 plus line count checked (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:24`). The copied manifest pins v1.12, SHA-256 `1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75`, and 1419 lines (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17`).

Diff: copied `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json` exactly. Source and repository SHA-256 both measured `21a77d2e8e06746597f7cb82c332ccef01cc427de53694f991311d8103029af6`; source and staged Git blob OIDs both measured `9f7eff1d6bb283965bc3b91b5ad32e670a0db167`. `validate_design_pin` reads the named bytes, measures SHA-256 and `splitlines()` count, and refuses `DESIGN_PIN_MISMATCH` for a malformed, missing, or unequal pin (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1933-1973`).

RED/GREEN: changing one byte in a same-line-count design copy initially produced “DID NOT RAISE”; it now produces `DESIGN_PIN_MISMATCH` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:513-525`). The item suite finished at 281 passed.

Commit: `d9484af3f81d325a5175c71e98ef142b94956406` (`fix(mtc-v2): bind refreshed design manifest`).

## Final verification counts

All commands ran from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`; the lane permits package tests and the verifier (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
281 passed in 4.46s

python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
18/18 checks passed or detected their declared refusal; claim_label=NON_ACCEPTING_SELFTEST
```

The final comparison code records legacy scenario and surface counts in the receipt (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3390-3395`) and blocked-node accounting immediately beside them (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3396-3409`).

## Canonical gate - single invocation

Command, run exactly once after all seven commits:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
```

Measured receipt summary:

```text
claim_label: BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable: true
catalog_counts: RED=9, GREEN=8, PROBE=10
legacy_reproduction: MATCH, scenarios=17, surfaces=34
comparison_claim_scope: ALL_NON_BLOCKED_EXPECTED_NODES
blocked_node_skips: 96
design pin: sha256=1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75, total_lines=1419
acceptance_blockers: 41
refusals: 42 (the 41 blockers plus SEMANTIC_COVERAGE_REVIEW_MISSING inserted by full-gate)
```

The full-gate wrapper inserts the missing-review refusal ahead of pipeline blockers and selects the refusal label whenever that combined list is non-empty (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3523-3552`).

### Exact refusal list, grouped without omission

1. One `SEMANTIC_COVERAGE_REVIEW_MISSING`: `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json`.
2. One `EXPECTED_PATH_CHANGED_AFTER_BASE`: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`. The check emits the first changed expected path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1898-1923`).
3. Nine `PROBE_COULD_NOT_EVALUATE`, each containing `PROBE_BASE_TREE_OID_MISMATCH`: `PROBE-P012-01-A`, `PROBE-P012-01-B`, `PROBE-P012-02-A`, `PROBE-P012-04-A`, `PROBE-P012-05-A`, `PROBE-P012-05-B`, `PROBE-P012-06-A`, `PROBE-P012-07-A`, and `PROBE-P012-08-A`. The verifier refuses when the stored base tree OID differs from the current core tree (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2351-2352`).
4. Twelve `CLOSED_SET_VIOLATION` records, emitted by the gate-side call at `verify_bceg.py:3297-3310`:
   - `RULE2-01-RED` and `RULE2-01-GREEN`: missing `/RESULT_SURFACE/order_notional`.
   - `RULE2-02-RED`: missing `/RESULT_SURFACE/order_notional`; `RULE2-02-GREEN`: missing `/RESULT_SURFACE/admitted`.
   - `RULE2-04-RED`: unknown `STOP` at `/EVENT_SURFACE/exit_events/0/reason`.
   - `RULE2-05-RED` and `RULE2-05-GREEN`: missing `/RESULT_SURFACE/order_notional`.
   - `RULE2-06-GREEN`: unknown `STOP` at `/EVENT_SURFACE/exit_events/0/reason`.
   - `RULE2-07-RED`: unknown `MARKET_EXIT` at `/EVENT_SURFACE/exit_events/0/reason`; `RULE2-07-GREEN`: missing `/RESULT_SURFACE/guards`.
   - `RULE2-08-RED` and `RULE2-08-GREEN`: missing `/RESULT_SURFACE/cumulative_funding`.
5. Fourteen `CORRECTED_EXPECTATION_MISMATCH` records, produced by `verify_bceg.py:3311-3326`:
   - `RULE2-01-RED`, `RULE2-01-GREEN`, and `RULE2-02-RED`: `/RESULT_SURFACE/order_notional`.
   - `RULE2-02-GREEN`: `/RESULT_SURFACE/admitted`.
   - `RULE2-04-RED`: `/EVENT_SURFACE/exit_events/0/reason`.
   - `RULE2-05-RED` and `RULE2-05-GREEN`: `/RESULT_SURFACE/order_notional`.
   - `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED`: `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
   - `RULE2-06-GREEN` and `RULE2-07-RED`: `/EVENT_SURFACE/exit_events/0/reason`.
   - `RULE2-07-GREEN`: `/RESULT_SURFACE/guards`.
   - `RULE2-08-RED`: `/EVENT_SURFACE/cash_events`.
   - `RULE2-08-GREEN`: `/EVENT_SURFACE/decision_events`.
6. Five `RULE2_PROJECTION_COULD_NOT_EVALUATE` records, produced by `verify_bceg.py:3327-3342`: `RULE2-01-RED` and `RULE2-01-GREEN` with `KeyError: 'order_notional'`; `RULE2-07-RED` and `RULE2-07-GREEN` with `KeyError: 'guards'`; `RULE2-08-RED` with `KeyError: 'cumulative_funding'`.

The 42 records therefore comprise six finding classes: missing mandatory review, changed expected provenance, stale kernel-probe bindings, corrected closed-set violations, corrected expected mismatches, and unevaluable RULE-2 projections. The receipt had no legacy-reproduction mismatch: actual legacy execution remained byte-exact (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3283-3296`). It also reported 96 explicitly bounded `BLOCKED-` skips, not silent equality (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3311-3318,3396-3399`).

## Discrepancies

1. **The external design still names the old unbounded accepting label and says every node matched.** Design section 15.5 names `BOUNDED_CORRECTION_EVIDENCE_ACCEPTED` and “every node” (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:575-582`), while item 2 explicitly requires the claim to be bounded to non-blocked nodes (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:20`). The design was forbidden scope, so the implementation uses the narrower labels and explicit scope/accounting (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:53-54,3396-3399`). The design text remains unsynchronized.
2. **Section 15.4 asks Git ancestry of a content digest.** `EXPECTED_SEAL_SHA` is a SHA-256 content seal, not a Git commit, yet the design says Git proves that seal equal to or ancestral to `IMPLEMENTATION_BASE_SHA` (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:564`). The machine-evaluable implementation instead verifies the independent method, agreement of the manifest/anchor `IMPLEMENTATION_BASE_SHA`, ancestry of that Git base to observed HEAD, and no expected member changes across that range (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1818-1929`). The unevaluable seal-to-commit phrase remains a design defect.
3. **Item 0 removes the constructor from the live core, but cataloged kernel variants still contain old copies.** For example, `tests/corrected_vnext/probes/PROBE-P012-08-A/kernel/runner.py:371` still defines `for_corrected_contract`. The lane authorized live kernel bytes only for item 0 and made the manifest copy the only item-6 non-harness byte (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:8-10,18,24`), so no probe variant or modification manifest was rewritten. The canonical gate consequently reported nine base-tree-OID mismatches. A later authorized probe refresh is required; relaxing the check would be wrong.
4. **The repository audit contract requires independent T0 review, but C-1 forbids this lane from invoking another assistant/model.** T0 normally requires two flagship reviews plus Gemini (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:24-31`), while this lane's incorporated clause prohibits any other assistant/model (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`). I performed implementation and self-verification only; no independent acceptance verdict is claimed. This report and the refusing gate must go to a separately authorized Lead/audit stage.
5. **The stage normally writes current state to `HANDOFF.md`, but the lane's exact whitelist does not include it.** The stage output rule is at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/OUTPUTS.md:3-9`; the lane limits writes to the named harness/validator areas, item-0 kernel, exact manifest, and the root report (`C:\tmp\LANE_PROMPTS_20260828\LANE_W284_HARNESS_FLAGSHIP2.md:8-12,24,36-40`). I left `HANDOFF.md` unchanged and used this required report as the handoff artifact.

## NOT VERIFIED

- The exact Python process exit code is NOT VERIFIED. The execution wrapper surfaced a non-zero command result as exit code 1, while the gate's own `main()` returns 2 for any non-accepting full-gate receipt (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3559-3561`). The receipt content and refusal status were printed and measured.
- Independent G5/G6 acceptance is NOT VERIFIED and was not attempted; the stage separates implementation QA from independent audit (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:12-20`).

## Commands and hygiene

The regression workflow followed the repository requirement to execute RED before GREEN and to inspect the exact staged set before each commit (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14,21-22`). Commands used were scoped variants of:

```text
python -m pytest -q <new regression selection>
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN  # once
git diff --check
git diff --cached --check
git add -- <explicit paths only>
MTC_COMMAND_CENTER\tools\repo_guard.ps1
git commit -m <item-specific message>
```

No `git add .`, `git add -A`, `--no-verify`, push, merge, or pull-request command was used, matching both C-5 and stage QA rules (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:21-22`).

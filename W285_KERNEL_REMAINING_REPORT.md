# W285 Kernel Remaining Report

## Verdict

Six authorized kernel findings were repaired: W279-F13, W279-F16, W279-F19, W279-F20,
W279-F21, and the W279-F17 kernel half. V283R2 D-1 was closed with a discriminating assurance
test and no kernel change. W279-F06 stopped because its required consumer move is absent and that
consumer is explicitly outside this lane's write fence; W279-F18 stopped DESIGN-BOUND because the
design makes JSON numeric node kind depend on the serialized token (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:10-13,19,22,26-27`;
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:501-535,646-668`).

The corrected row measurement is **17/17 MATCH**. Probe mode is **1/10 DETECTED** and
**9/10 COULD_NOT_EVALUATE** because the nine immutable kernel probes pin an older core tree.
The canonical gate ran exactly once, returned exit 1, and emitted the expected missing-review
refusal plus those nine `PROBE_BASE_TREE_OID_MISMATCH` refusals. No protected probe, catalog,
golden, input, baseline, seal, design, or verifier byte was changed, as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:10-13,36-40`).

## Scope and preflight

- The four predecessor markers existed and contained `exit=0`:
  `C:\tmp\LANE_PROMPTS_20260828\W283_DONE.txt:1`,
  `W283R_DONE.txt:1`, `W283R2_DONE.txt:1`, and `W283R3_DONE.txt:1`.
- The initial worktree was clean, `git rev-parse --show-toplevel` returned `C:/WP012BUILD`, and
  the branch was `feature/wp-p0-12-corrected-vnext-20260831`, matching the lane precondition
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:3-7`).
- Owner decisions 123 and 126 authorize exactly the listed kernel work
  (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:799-810,822-828`).
- No push, merge, rebase, baseline generation, backtest, broker, exchange, network, credential,
  deployment, Pine, adapter, or live-trading action occurred. The lane authorizes tests and the
  canonical gate only (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:3-13,29-40`).

## Disposition summary

| Order | Finding | Disposition | Commit |
|---|---|---|---|
| 1 | W279-F06 | STOPPED - required harness move is forbidden and absent | none |
| 2 | W279-F13 | FIXED | `207ce228b26760deffad6f99bfc655e4ed77ee5d` |
| 3 | W279-F16 | FIXED | `62d064ae93088f0a2215e56f7b723bc54e55b126` |
| 4 | W279-F18 | STOPPED DESIGN-BOUND | none |
| 5 | W279-F19 | FIXED | `ec1fea3d4c24557e79d63fccdefb6c31a407b214` |
| 6 | W279-F20 | FIXED | `4ff29de234e1e7b03a3c35635de42f8de7cbeddf` |
| 7 | W279-F21 | FIXED | `7ab355bed458954283f5440505f3eb16c1749afc` |
| 7b | W279-F17 kernel half | FIXED | `4d88c2b24641cb76995d9a4f52599fca5c6d2c0b` |
| 8 | V283R2 D-1 | ASSURANCE; NO KERNEL DEFECT | `e022c56267b3469426c1e899a6d2a17af528f468` |

## Item 1 - W279-F06 - STOPPED

Design section 18 assigns corrected economics to the economics seam and runner consumption but
declares no economic-input-bearing runner constructor (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:646-668`).
The finding is still present: `Runner.for_corrected_contract` and its override-bearing state remain
in `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:145-147,374-401,462,587`.
The canonical consumer still invokes that classmethod and supplies those override values at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:938-952`.

The lane requires the harness to construct `EconomicIntent` or equivalent directly, but also
forbids any `verify_bceg.py` edit (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:10-13,19`).
Removing the classmethod from core without moving that consumer would break the required canonical
gate. Therefore this item was stopped with no edit, test, commit, or legacy replay. This is the
required no-expansion disposition, not a claim that the finding is absent.

## Item 2 - W279-F13 - FIXED

The controlling discipline compares finite float nodes as exact IEEE-754 binary64 values and fixes
no epsilon for these state transitions (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:513-535`).
The change removes the corrected-path absolute epsilon decisions: exit closure now uses `<= 0.0`
in `core/economics.py:986,1097`; position joins use `_same_binary64` and exact zero closure in
`core/position_manager.py:175-179,243,276,412-425`; completed-trade detection is exact at
`core/results.py:707-710`. A source fence proves no `1e-12` remains in corrected economics or
results and only the frozen legacy close threshold remains in the manager
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py:210-217`).

The four state-deciding disagreements are pinned at
`test_w285_kernel_remaining.py:106-207`: price exit, market exit, and position application each
use `1.0 - 0.9999999999995`, a positive binary64 remainder below `1e-12` that the old tolerance
closed but the exact rule preserves; the trade test uses the same incomplete exit quantity, which
the old `exit_qty + 1e-12` rule accepted but the exact rule rejects.

- RED command: `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py -q`
- RED result: `5 failed in 0.14s` (all four disagreement tests plus the epsilon source fence).
- GREEN result after the fix: `5 passed in 0.07s`.
- Full contract result at this commit: `261 passed`.
- Post-commit legacy replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.
- Diff: `core/economics.py` +2/-2; `core/position_manager.py` +10/-6;
  `core/results.py` +1/-1; new W285 self-test file +158.

Commit: `207ce228b26760deffad6f99bfc655e4ed77ee5d`
(`fix(mtc-v2): remove corrected epsilon tolerances`).

## Item 3 - W279-F16 - FIXED

The design says a fee joined to fill `F<n>` has `cash_event_id=CE-FEE-<n>`, where the fill id is
itself derived from that fill row's sequence (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:75-81,1132-1138`).
`_fee_rows` now receives `fill_sequence` and derives the cash id from it at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:283-295,311-320`; both exit
paths pass the fill sequence at `core/economics.py:930-967,1042-1076`.

The regression separates fill sequence 7 from fee sequence 2 and requires `CE-FEE-7` on both
joined rows (`test_w285_kernel_remaining.py:220-243`).

- RED: `1 failed`; exact assertion difference: `'CE-FEE-2' == 'CE-FEE-7'`.
- GREEN: `1 passed in 0.06s`.
- Full contract result: `262 passed`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: `core/economics.py` +5/-1; W285 self-test +26.

Commit: `62d064ae93088f0a2215e56f7b723bc54e55b126`
(`fix(mtc-v2): derive fee cash ids from fills`).

## Item 4 - W279-F18 - STOPPED DESIGN-BOUND

The current serializer converts a finite integral-valued float to an integer JSON token at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:356-364`. The design explicitly
makes node kind follow the serialized JSON token: `100` is an integer node while `100.0` is a float
node (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:513-535`). It supplies no per-field
numeric token-kind schema from which a different structural choice can be derived.

The targeted probe required Python `101.0` to remain a float token and failed on the current
integer result: `1 failed`. A temporary, uncommitted serializer that preserved Python runtime type
made that probe pass, but the full contract suite then failed twice: the identity-copy probe
measured `CORRECTED_EXPECTATION` instead of no failed check, and RULE2-05 expected an integer zero
cash delta but received float `0.0`. That temporary edit and probe were removed. Per the lane's
explicit DESIGN-BOUND branch, no code, test, golden, or design change was retained
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:22,31-38`).

There is no commit for this item. The later final suite (`267 passed`) and clean diff confirm that
the temporary experiment did not remain.

## Item 5 - W279-F19 - FIXED

The design requires the caller to apply each returned transition once
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:75-83`). Previously two distinct empty
transitions collapsed to the same event-derived key. `EconomicTransition` now has a private,
non-comparing, non-repr application identity (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:160-178`),
and `_transition_key` uses it only when all five event collections are empty
(`core/position_manager.py:116-155`). Non-empty transition identity is unchanged.

The regression constructs two distinct no-op market-exit transitions, applies both, then proves a
second application of the same first object still refuses (`test_w285_kernel_remaining.py:246-284`).

- RED: `1 failed`; second distinct object refused with
  `REFUSED_INVALID_CASH_LEDGER_JOIN: transition already applied`.
- GREEN: `1 passed in 0.06s`.
- Full contract result: `263 passed`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: `core/position_manager.py` +14; `core/types.py` +5; W285 self-test +67/-1.

Commit: `ec1fea3d4c24557e79d63fccdefb6c31a407b214`
(`fix(mtc-v2): distinguish empty transitions`).

## Item 6 - W279-F20 - FIXED

The funding formula has exactly two payer branches and the sealed schedule value is `LONG`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:414-424,867-879`). The adapter now checks
`positive_rate_payer` against the closed set `{LONG, SHORT}` immediately after selecting the one
event and raises typed `REFUSED_ECONOMIC_INPUT` before eligibility arithmetic
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:1128-1146`).

The regression replaces the admitted event value with `TYPO`
(`test_w285_kernel_remaining.py:287-321`).

- RED: `1 failed`; `DID NOT RAISE EconomicsRefusal`.
- GREEN: `1 passed in 0.06s`.
- Full contract result: `264 passed`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: `core/economics.py` +7/-2; W285 self-test +40.

Commit: `4ff29de234e1e7b03a3c35635de42f8de7cbeddf`
(`fix(mtc-v2): refuse unknown funding payer`).

## Item 7 - W279-F21 - FIXED

Decision 71 requires each trade row's `exit_ids` to be exactly the lifecycle's `exit_events[]`
members in exit-surface sequence order (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1176-1188`).
`_joined_exit_fills` is now the single ordered source predicate, selecting exit fills with their
gross-realization cash join (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:639-652`).
Both `_exit_surface` and `_closed_lifecycle_trades` consume that list at
`core/results.py:655-710,883-911`.

The regression supplies an apparent exit fill without its required gross cash join and requires
both the exit surface and trade surface to remain empty
(`test_w285_kernel_remaining.py:324-352`).

- RED: `1 failed`; `exit_events == []` but trades contained `UNJOINED-EXIT`.
- GREEN, run with the carried F13 trade regression: `2 passed in 0.06s`.
- Full contract result: `265 passed`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: `core/results.py` +29/-14; W285 self-test +63/-5.

Commit: `7ab355bed458954283f5440505f3eb16c1749afc`
(`fix(mtc-v2): share exit row derivation`).

## Item 7b - W279-F17 kernel half - FIXED

The closed override refusal object has exactly `code`, `field`, `record_value`, `runtime_value`,
and `stage`, with `stage="PRE_EVALUATION"`; free-form `detail` is forbidden
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1223-1234`). `_state_refusals` now requires
the three decision-detail inputs and emits the four members beyond `code` itself at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:770-796`.

The regression provides a real override refusal decision and requires the exact closed object
(`test_w285_kernel_remaining.py:354-391`).

- RED: `1 failed`; actual `{'code': ...}` differed from the required five-member object.
- GREEN: `1 passed in 0.06s`.
- Full contract result: `266 passed`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: `core/results.py` +10; W285 self-test +41.

Commit: `4d88c2b24641cb76995d9a4f52599fca5c6d2c0b`
(`fix(mtc-v2): serialize override refusal details`).

## Item 8 - V283R2 D-1 - ASSURANCE, NO KERNEL FIX

Design line 426 delegates eligibility and same-timestamp ordering to the frozen schedule; the
admitted schedule selects `END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:426,854-879`). The current rules per actual
runner call site are:

1. Before every bar, `run()` calls `(previous, current, include_current=False)`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:823-827`). On the first bar
   this selects every event strictly earlier than `current`; later it selects
   `previous < event < current` (`core/runner.py:758-772`).
2. After evaluating each bar, `run()` calls `(None, current)` with the default
   (`core/runner.py:1627-1632`). This selects only `event == current`, so an exact-timestamp event
   observes the post-bar position as the admitted schedule requires (`core/runner.py:753-765`).
3. After the loop, `run()` calls `(previous, None)` (`core/runner.py:1633-1634`). This selects
   `previous < event` and dispositions post-window events outside the corrected curve
   (`core/runner.py:766-767`).

Therefore the default-path loss of the strictly-earlier disjunct is not a defect: the explicit
pre-bar call already handled that disjoint set. Restoring it in the post-bar default repeats an
earlier event under a changed position snapshot.

The new first-bar test carries one strictly-earlier and one same-timestamp event. It requires the
strictly-earlier event to be dispositioned once as ineligible, the same-timestamp event once as
eligible, and only the latter to reach `funding_events[]`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py:394-462`).

- RED against the exact equivalent mutation that restored `< current` in the default branch:
  `1 failed in 0.16s`; the decision list contained an extra
  `('STRICTLY-EARLIER', True)` before `('SAME-TIMESTAMP', True)`.
- GREEN after removing the mutation: `1 passed in 0.08s`.
- Full contract result: `267 passed in 3.91s`.
- Post-commit legacy replay: `17/17` scenarios, `34/34` surfaces, exact.
- Diff: W285 self-test +69; no kernel byte.

Commit: `e022c56267b3469426c1e899a6d2a17af528f468`
(`test(mtc-v2): pin first-bar funding partition`).

## Seventeen-row direct measurement

The final in-memory measurement used the canonical executor immediately followed by the scoped
expected comparator, the W246 seam documented at `W246_GATE_RERUN_REPORT.md:106-122`. It wrote no
observed artifact.

| Scenario | Result | First differing pointer | Observed | Golden | Classification |
|---|---|---|---|---|---|
| RULE2-01-RED | MATCH | - | - | - | MATCH |
| RULE2-01-GREEN | MATCH | - | - | - | MATCH |
| RULE2-02-RED | MATCH | - | - | - | MATCH |
| RULE2-02-GREEN | MATCH | - | - | - | MATCH |
| RULE2-03-RED | MATCH | - | - | - | MATCH |
| RULE2-03-GREEN | MATCH | - | - | - | MATCH |
| RULE2-04-RED | MATCH | - | - | - | MATCH |
| RULE2-04-GREEN | MATCH | - | - | - | MATCH |
| RULE2-05-RED | MATCH | - | - | - | MATCH |
| RULE2-05-GREEN | MATCH | - | - | - | MATCH |
| RULE2-06-RED | MATCH | - | - | - | MATCH |
| RULE2-06-EQUAL-PRICE-RED | MATCH | - | - | - | MATCH |
| RULE2-06-GREEN | MATCH | - | - | - | MATCH |
| RULE2-07-RED | MATCH | - | - | - | MATCH |
| RULE2-07-GREEN | MATCH | - | - | - | MATCH |
| RULE2-08-RED | MATCH | - | - | - | MATCH |
| RULE2-08-GREEN | MATCH | - | - | - | MATCH |

Measured summary: **17/17 MATCH, 0 mismatch, 0 KERNEL-SHORT, 0 GOLDEN-OVER, 0 DESIGN-GAP**.

## Ten-probe measurement

Exact command:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe --baseline-root C:\tmp\P012_BASELINE_RUN
exit=0
claim_label=NON_ACCEPTING_PROBE_EVIDENCE
```

| Probe | Status | Digest status | Refusal / measured check |
|---|---|---|---|
| PROBE-P012-01-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-01-B | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-02-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-03-A | DETECTED | PROBE_DIGEST_MATCH | RECORD_IDENTITY_PREFLIGHT |
| PROBE-P012-04-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-05-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-05-B | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-06-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-07-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |
| PROBE-P012-08-A | COULD_NOT_EVALUATE | PROBE_ARTIFACT_INVALID | PROBE_BASE_TREE_OID_MISMATCH |

Measured summary: **1 DETECTED, 0 NOT_DETECTED, 9 COULD_NOT_EVALUATE; 9 probe blockers**.
The current `core` Git tree is `35fcd0ede6bd264edc9218d2fb5d6eb0076f0029`; every failed
kernel probe pins `base_tree_oid=2c749345ed9be5186659369f091ce77a2e42d61a`, for example
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1`.
The one input-record probe pins a different, unaffected subtree and therefore evaluates
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1`).

## Canonical full gate

The canonical command ran exactly once, after all commits and final test/measurement commands:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=1
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
catalog_counts={"GREEN":8,"PROBE":10,"RED":9}
scenario_receipts=17
probe_receipts=10
acceptance_blockers=9
refusal_count=10
```

Exact refusal list in emitted order:

```text
SEMANTIC_COVERAGE_REVIEW_MISSING | C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-01-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-01-B
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-02-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-04-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-05-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-05-B
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-06-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-07-A
PROBE_COULD_NOT_EVALUATE | PROBE_BASE_TREE_OID_MISMATCH | PROBE-P012-08-A
```

The scenario receipt section reported `first_corrected_mismatch: null` for all 17 rows. The
manifest declares the semantic review pending at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:679-682`.

## Final tests and counts

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
267 passed in 3.86s
exit=0
```

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
18 checks: 3 PASS, 14 DETECTED, 1 DETECTED:/a/1
exit=0
claim_label=NON_ACCEPTING_SELFTEST
```

```text
PYTHONPATH=00_PYTHON python -m pytest 00_PYTHON/mtc_v2/tests --ignore=00_PYTHON/mtc_v2/tests/corrected_vnext -q
142 passed in 1.53s
exit=0
```

Every one of the seven commits was followed by the W249 frozen replay and returned
`LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`; the method is recorded at
`W249_KERNEL_ORDERED_EQUITY_REPORT.md:206-260`. Net committed implementation/test movement before
this report is 547 insertions and 32 deletions across seven commits. Four kernel files and one
self-test file changed; the itemized diffs above sum to those counts. `git diff --check` was clean
before this report.

## Commits and exact paths

1. `207ce228b26760deffad6f99bfc655e4ed77ee5d` -
   `core/economics.py`, `core/position_manager.py`, `core/results.py`, W285 self-test.
2. `62d064ae93088f0a2215e56f7b723bc54e55b126` - `core/economics.py`, W285 self-test.
3. `ec1fea3d4c24557e79d63fccdefb6c31a407b214` - `core/position_manager.py`,
   `core/types.py`, W285 self-test.
4. `4ff29de234e1e7b03a3c35635de42f8de7cbeddf` - `core/economics.py`, W285 self-test.
5. `7ab355bed458954283f5440505f3eb16c1749afc` - `core/results.py`, W285 self-test.
6. `4d88c2b24641cb76995d9a4f52599fca5c6d2c0b` - `core/results.py`, W285 self-test.
7. `e022c56267b3469426c1e899a6d2a17af528f468` - W285 self-test only.

All abbreviated paths above are beneath
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`; the self-test is
`tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py`. Every commit staged only
the exact listed paths. No `git add .`, `git add -A`, push, or merge was used, preserving the lane's
commit and Git constraints (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:29-40`).

## Discrepancies

1. **Item 1's required predecessor consumer move is absent.** The lane says the harness constructs
   an intent directly and simultaneously forbids editing that harness
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W285_KERNEL_REMAINING_SEVEN.md:10-13,19`). The repository
   instead still calls `Runner.for_corrected_contract` at
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:938-952`.
   Removing only the core half would leave a broken canonical consumer, so W279-F06 stopped.
2. **The item 7b premise that W284-5 removed the harness override is not true in this checkout.**
   The premise appears at `LANE_W285_KERNEL_REMAINING_SEVEN.md:26`, while the override remains at
   `verify_bceg.py:938-952`. The independently authorized kernel writer half was still reproducible
   and was repaired without touching the harness or observed artifact.
3. **F18's proposed structural-node direction is not derivable from the current design.** The lane
   explicitly allows DESIGN-BOUND stop (`LANE_W285_KERNEL_REMAINING_SEVEN.md:22`), and the design
   binds integer versus float node kind to the actual JSON token at
   `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:513-535`. A runtime-type serializer breaks
   two sealed contract expectations, so no schema was invented.
4. **The predicted 10/10 probe result is stale after authorized kernel movement.** The prediction
   and artifact write prohibition coexist at `LANE_W285_KERNEL_REMAINING_SEVEN.md:10-13,36-38`.
   Nine probe manifests still pin core tree `2c749345...`, for example
   `tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1`, while the final core
   tree is `35fcd0ed...`. The honest result is 1/10, and refreshing those protected artifacts is a
   later owner-gated operation.
5. **The expected gate refusal list of “review only” is consequently false.** That expectation is
   at `LANE_W285_KERNEL_REMAINING_SEVEN.md:39`; the canonical gate also emitted the nine exact
   probe base-tree refusals listed above. No bypass or out-of-scope refresh was attempted.

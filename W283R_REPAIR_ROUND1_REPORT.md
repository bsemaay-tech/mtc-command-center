# W283R Repair Round 1 Report

## Verdict

All seven V283a findings have a bounded disposition: R1, R2, R3, R5, and R6 are repaired with
focused regression evidence; R4 is refuted by a runner probe; R7 is cleared by a full-tree grep and
the frozen legacy replay. Final package self-tests and the one authorized canonical gate are still
pending at this report revision.

This work ran in `C:\WP012BUILD` on
`feature/wp-p0-12-corrected-vnext-20260831`. Before the first edit,
`C:\tmp\LANE_PROMPTS_20260828\W283_DONE.txt` existed, the branch matched the lane, and
`git status --porcelain` was empty, as required by the repair prompt
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R_REPAIR_ROUND1.md:3-7`). Owner decisions 80-81 authorize
the bounded kernel findings with failing-then-passing tests and byte-exact legacy replay
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:695-715`).

No golden, catalog, input, baseline, seal, probe artifact, `verify_bceg.py`, design, schema, Pine,
adapter, broker, venue, host, credential, deployment, backtest, optimization, launcher, or live
trading path was edited or invoked. No push or history rewrite was performed.

## Design citations

| Finding group | Design cite | Controlling reading |
|---|---|---|
| R1-R2 / item 1 | `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:75,1107-1108` | There is no literal runtime-equity accumulation line. The runtime rule is derived from line 75, which makes `cash_events[]` the caller-applied equity ledger, plus lines 1107-1108, which require array-order accumulation. This is the required V283a Discrepancy 1 record. |
| R3-R7 / item 2 | `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412-439` | Line 439 states: "Duplicate `(funding_event_id,lifecycle_id)` is refused." It does not add an eligibility qualifier. |

## R1 - Runner regression and ordered `realized_equity`

**Disposition: REPAIRED by assurance tests.** Commit
`70d0f6f844ef374d175ae639cee3e23eb5f81b29` (`test(mtc-v2): cover ordered runtime equity folds`).

- Diff: two self-test files, 34 insertions and 1 deletion. No kernel byte changed in this commit.
- The existing manager regression now begins with an internally consistent
  `initial_capital=0`, `equity=1e16`, `realized_equity=1e16` state and asserts both ordered fields
  equal `1.0` after `[-1e16, +1.0]`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py:125-166`).
- The new Runner-level regression executes the real corrected market-exit path, whose transition
  emits fee/gross cash `[-1e16, +1.0]`, and asserts runtime equity `1.0`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:121-146`).
- RED, exact old sum/reconstruction variant:
  `python -m pytest ...::test_w276_f01_runtime_equity_applies_cash_events_in_order ...::test_w276_f01_runner_applies_exit_cash_events_in_order -q`
  -> `2 failed`; quoted assertions were `realized_equity 0.0 == 1.0` and Runner `equity 0.0 == 1.0`.
- GREEN, restored ordered fold: the same command -> `2 passed in 0.08s`. The implementation folds
  each row into both fields at
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:426-429`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R2 - Runner equity seed

**Disposition: REPAIRED by the verifier's allowed construction proof.** Commit
`35c9daef0dfa8103cbc73ad1d68a5cdff670deb9` (`test(mtc-v2): pin runner equity seed`).

- `PortfolioState` has independent zero defaults for `initial_capital`, `equity`, and
  `realized_equity`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:395-400`). A targeted core grep
  found exactly one live construction path, the Runner constructor, which passes
  `initial_capital=self.initial_capital` and `equity=self.initial_capital`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:190-195`).
- Diff: one Runner self-test, 11 insertions. It constructs `Runner` exactly as production does and
  checks exact `equity == initial_capital + realized_equity`, with no tolerance
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:149-159`).
- RED, seed-removal variant (`equity=0.0`): quoted failure
  `assert 0.0 == (1234.5 + 0.0)`.
- GREEN, actual constructor: `1 passed in 0.07s`; full corrected Runner file: `30 passed in 0.16s`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

The checked invariant is deliberately a construction invariant. Recomputing
`initial_capital + realized_equity` after each fold would reintroduce the R1 association defect for
binary64 sequences such as `1e16, -1e16, +1.0`.

## R3 - Ineligible duplicate refusal

**Disposition: REPAIRED.** Shared R3/R4 commit
`1a88695c8837a9eca1e4de4726ce081650945540`
(`fix(mtc-v2): refuse ineligible funding duplicates`).

- Design line 439 contains the unconditional pair rule quoted above; no line in 412-439 permits an
  eligibility gate.
- Diff: `core/economics.py` plus two self-test files, 50 insertions and 1 deletion. The adapter now
  forms the pair whenever a lifecycle exists and checks it independently of the quantity-derived
  `eligible` boolean
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:1130-1136`).
- The RED test uses lifecycle `1`, quantity `0.0`, and applied key `("TEST-FUND-1", 1)`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py:381-413`).
- RED before the source change: `FAILED: DID NOT RAISE EconomicsRefusal`.
- GREEN after the source change, together with the R4 probe: `2 passed in 0.07s`; the exact refusal
  code is asserted as `REFUSED_DUPLICATE_FUNDING_EVENT`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R4 - Runner skip qualifier

**Disposition: REFUTED by probe; no runner source change.** The probe is committed with R3 at
`1a88695c8837a9eca1e4de4726ce081650945540`.

The runner check is not gated on funding eligibility (`quantity > 0`). It derives the lifecycle from
the position and checks the exact pair before invoking the adapter
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:783-791`). The focused probe uses
a present lifecycle-1 position with quantity `0.0` and the same applied pair; it records the event as
evaluated and emits no duplicate decision/funding row
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:315-325`).

Quoted probe result on the pre-R3 runner and repaired tree: `1 passed`. Therefore the runner's pair
skip was already independent of quantity eligibility. A state with no lifecycle has no
`(funding_event_id,lifecycle_id)` pair to compare; design lines 412-439 do not define a substitute
identity for that case.

## R5 - Persisted key-set and both lifecycle cases

**Disposition: REPAIRED by an integration regression.** Commit
`1f3f71b7dbfcd537dafc5548b0d32024b67f659f` (`test(mtc-v2): pin funding lifecycle keys`).

- Diff: one manager self-test, 54 insertions.
- The test begins with `{("TEST-FUND-1", 1)}`, resolves/applies the same venue ID for lifecycle 2,
  and asserts the persisted set is exactly both pairs. It then resolves the same pair again and
  asserts the typed duplicate refusal
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py:433-482`).
- RED variant 1, bare-event-ID comparison: distinct lifecycle 2 raised
  `REFUSED_DUPLICATE_FUNDING_EVENT` at the first resolve.
- RED variant 2, reversed pair `(lifecycle_id,funding_event_id)`: quoted failure
  `FAILED: DID NOT RAISE EconomicsRefusal` for the same pair.
- GREEN, exact pair order: `1 passed in 0.05s`; full manager self-test file: `10 passed in 0.07s`.
- The actual persisted update is pair-shaped at
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:327-333,437-440`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R6 - Runner lifecycle identity

**Disposition: REPAIRED by a Runner-level regression.** Commit
`f7ca024338fcf6c8420422a6788470f2647b2f74`
(`test(mtc-v2): cover runner funding lifecycle identity`).

- Diff: one Runner self-test, 15 insertions.
- The test starts the real Runner path on lifecycle 2 with prior key `("TEST-FUND-1", 1)`, applies
  the scheduled event, asserts both persisted pairs, and asserts the emitted funding row belongs to
  lifecycle 2
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:328-343`).
- RED, runner skip changed to bare event ID: the actual set remained `{("TEST-FUND-1", 1)}` and the
  assertion reported missing `("TEST-FUND-1", 2)`.
- GREEN, pair-shaped runner check: `1 passed in 0.08s`; full Runner file: `32 passed in 0.12s`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R7 - Shared-field blast radius and legacy replay

**Disposition: CLEARED by repository-wide probes; no active reader repair required.**

The required full-tree command was:

```text
rg -n --no-heading "applied_funding_event_ids" .
```

Measured result: **72 lines in 36 files**, all under nine immutable kernel-copy probe directories.
Each of `PROBE-P012-01-A`, `01-B`, `02-A`, `04-A`, `05-A`, `05-B`, `06-A`, `07-A`, and `08-A`
contains 8 lines across `economics.py`, `position_manager.py`, `runner.py`, and `types.py`.
`PROBE-P012-03-A` is the tenth probe directory but is a record-only variant and has no kernel copy.

The exclusion probe quoted exactly:

```text
rg -n --no-heading "applied_funding_event_ids" . -g '!**/probes/**'
NO_NON_PROBE_MATCHES
core/results.py: NO_MATCHES
contract selftests: NO_MATCHES
```

Thus no active core reader, `core/results.py`, artifact/report writer, ordinary self-test, or other
non-probe repository path retains the old member. The remaining hits are frozen probe bytes and are
outside the authorized write fence. The current shared field is pair-shaped at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:395-434`.

The W249 replay method loads the frozen driver, imports the current branch's real kernel modules,
and compares canonical bytes for both surfaces of all catalog rows
(`W249_KERNEL_ORDERED_EQUITY_REPORT.md:206-252`). Quoted R7 result:

```text
LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact
```

## Legacy replay after each finding commit

| Finding | Commit | Result |
|---|---|---|
| R1 | `70d0f6f8` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| R2 | `35c9daef` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| R3 + R4 | `1a88695c` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| R5 | `1f3f71b7` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| R6 | `f7ca0243` | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` |
| R7 evidence | pending report commit | `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact` before commit |

## Final verification

Pending at this report revision. The repair prompt permits the canonical gate exactly once at the
end (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R_REPAIR_ROUND1.md:40-45`).

## Commits

| Findings | Commit | Subject |
|---|---|---|
| R1 | `70d0f6f844ef374d175ae639cee3e23eb5f81b29` | `test(mtc-v2): cover ordered runtime equity folds` |
| R2 | `35c9daef0dfa8103cbc73ad1d68a5cdff670deb9` | `test(mtc-v2): pin runner equity seed` |
| R3 + R4 | `1a88695c8837a9eca1e4de4726ce081650945540` | `fix(mtc-v2): refuse ineligible funding duplicates` |
| R5 | `1f3f71b7dbfcd537dafc5548b0d32024b67f659f` | `test(mtc-v2): pin funding lifecycle keys` |
| R6 | `f7ca024338fcf6c8420422a6788470f2647b2f74` | `test(mtc-v2): cover runner funding lifecycle identity` |
| R7 | pending | report evidence commit |

## Discrepancies

1. **No literal runtime-equity design line exists.** The item-1 runtime rule is derived from design
   line 75 plus lines 1107-1108; the latter literally govern the serialized observation window.
   A design amendment is a Lead/owner action, so no design byte was changed.
2. **R4's stated eligibility narrowing is not present in the runner.** The adapter was gated on
   `eligible`; the runner was gated only on whether a lifecycle existed so it could form the design's
   pair. The zero-quantity same-pair probe passes before and after R3.
3. **An exact pre-fix bare-ID implementation cannot make the same-pair half of R5 RED.** Bare-ID
   code already refuses a same pair; it is wrong only for a different lifecycle. The report therefore
   records the exact bare-ID RED for the distinct-lifecycle half and a separate reversed-pair RED for
   the same-pair assurance half, without claiming the latter reproduces the old behavior.
4. **The prompt calls the set "ten pinned probe copies".** The repository has ten probe directories,
   but only nine contain kernel copies; `PROBE-P012-03-A` is record-only. The measured full-tree old
   identifier hits are therefore nine copies, 72 lines, and 36 files. The repository measurement
   controls under C-2.

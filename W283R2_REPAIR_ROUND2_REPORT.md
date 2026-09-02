# W283R2 Repair Round 2 Report

## Verdict

All eleven V283b findings have a bounded disposition. The five MEDIUM findings are repaired in
five separate commits. LOW F-1, F-5, F-9, and F-10 are repaired in four further commits; F-8 is
refuted as a defect by the closed owner-approved snapshot rule and a quoted valid/invalid probe;
F-11 is refuted as an implementation defect and reported as a `DESIGN-GAP`, because the design
requires the capital check but defines no capital/margin receipt and forbids adding a new refusal
shape without a schema amendment (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:104,1065-1066,1190-1200,1223-1234`).

Package verification is green at **255 contract self-tests**, **18/18 verifier self-check
dispositions**, and **142 legacy tests**. Frozen legacy replay remained **17/17 scenarios and
34/34 surfaces byte-exact after every finding commit**. The canonical gate was run exactly once at
the end and correctly remained non-accepting with the missing semantic review plus the nine known
immutable-probe tree-identity refusals required to remain untouched by this lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R2_REPAIR_ROUND2.md:27-31`).

This work ran in `C:\WP012BUILD` on
`feature/wp-p0-12-corrected-vnext-20260831`. Before the first edit,
`C:\tmp\LANE_PROMPTS_20260828\W283R_DONE.txt` existed and `git status --short` was empty, matching
the lane preconditions (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R2_REPAIR_ROUND2.md:3-9`). Owner
decisions 80-81 authorize exactly the bounded kernel repairs with failing-then-passing tests and
byte-exact legacy replay
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:695-715`).

No golden, catalog, input, baseline, seal, probe manifest, verifier harness, design, schema, Pine,
adapter, broker, venue, host, credential, deployment, backtest, optimization, launcher, or live
trading path was edited or invoked. No push or history rewrite was performed. The repair diff is
limited to `core/economics.py`, `core/runner.py`, and the runner contract self-test, within the exact
write fence at lane lines 7-9.

## Controlling design and owner ruling

- Funding applies once per schedule event to each eligible position; the duplicate identity is
  exactly `(funding_event_id,lifecycle_id)`, and missing required interval data uses
  `REFUSED_MISSING_FUNDING_EVENT`
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412-439`).
- The closed eligibility receipt is `FUNDING_ELIGIBILITY` with boolean `eligible`; false is the
  skipped disposition (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1071,1099`).
- Out-of-window schedule events do not invent or apply a rate
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:854-865`).
- Window-scoped equity includes only cash rows inside the closed observation window
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1102-1119`).
- Same-timestamp ordering is read from the schedule rule
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:426`), whose exact frozen value is
  `END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1`
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:867-872`). Owner decision 46 resolves the
  meaning: a fill at the exact payment timestamp counts for that payment
  (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:303-311`).

## R1 / F-2 MEDIUM - whole-event runner key

**REPAIRED.** Commit `73ff500a667e5b59c9f6c6fc631d7232422318dc`
(`fix(mtc-v2): remove runner funding id memo`).

The runner no longer owns a bare event-id memo. Its disjoint pre-window, between-bar,
same-timestamp, and post-window selections evaluate an event without a whole-event skip, then the
adapter checks the exact lifecycle pair at `core/economics.py:1131-1140`; state and manager retain
the shared pair shape at `core/types.py:13-16,427-434` and
`core/position_manager.py:327-333,437-440`. The runner regression applies `TEST-FUND-1` first to
lifecycle 1 and then lifecycle 2 and requires both stored pairs and both funding rows
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:338-351`).

- RED, old whole-event memo: `1 failed`; quoted difference:
  `assert {('TEST-FUND-1', 1)} == {('TEST-FUND-1', 1), ('TEST-FUND-1', 2)}`.
- GREEN, repaired runner plus same-pair and distinct-pair checks: `4 passed in 0.11s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

The same commit corrected the stale prior assurance test: an exact duplicate pair now reaches the
adapter and produces `REFUSED_DUPLICATE_FUNDING_EVENT`, rather than being silently skipped
(`test_runner_corrected.py:309-320`).

## R2 / F-3 MEDIUM - pre-window funding equity effect

**REPAIRED.** Commit `9c55d1d7873adc5146935654d1a261f04064d937`
(`fix(mtc-v2): disposition pre-window funding`).

`EconomicIntent` now carries the runner-measured window fact
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:73-92`). The adapter combines
that fact with lifecycle and quantity eligibility, emits one `FUNDING_ELIGIBILITY` decision, and
returns an empty transition when false (`core/economics.py:1124-1157`). The runner supplies false
for events before the first executed bar (`core/runner.py:760-765,778-790`).

The regression requires one `eligible=false` decision, no funding or cash rows, equity `1000.0`,
and curve `[1000.0]` (`test_runner_corrected.py:370-385`).

- RED: `1 failed`; quoted assertion: `assert True is False`.
- GREEN, pre-window plus still-open tail fixture: `2 passed in 0.08s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R3 / F-4 MEDIUM - post-window funding and curve

**REPAIRED.** Commit `ede8789d959699f6848ee74143c0723287a68bab`
(`fix(mtc-v2): disposition post-window funding`).

The runner now marks the post-loop `current is None` event as outside the observation window before
adapter resolution (`core/runner.py:766-790,1630-1634`). The adapter therefore emits the typed false
eligibility transition without cash. The regression requires no funding/cash row, zero equity
effect, and exact equality between the final state and the terminal corrected curve point
(`test_runner_corrected.py:388-403`).

- RED: `1 failed`; quoted assertion: `assert True is False`.
- GREEN, post-window and pre-window cases: `2 passed in 0.07s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R4 / F-6 MEDIUM - same-timestamp order

**REPAIRED AS ASSURANCE, WITH THE REPOSITORY/OWNER ORDER PRESERVED.** Commit
`a55f8dd80d3ca40d51ddd0ee3eef8fa63e6a09ff`
(`test(mtc-v2): pin funding snapshot order`).

The runner evaluates strictly earlier funding before the bar, evaluates the bar and its entry, then
evaluates an event equal to the bar timestamp before appending the curve point
(`core/runner.py:823-839,1630-1632`). This implements owner decision 46, not the misleading old test
name. The replacement regression opens a position on the funding timestamp and distinguishes the
orders using `funding_events.lifecycle_id`, `FUNDING_ELIGIBILITY.eligible`, and decision ordering,
not equity (`test_runner_corrected.py:281-306`).

- RED, equivalent pre-bar mutation: `1 failed`; quoted failure:
  `IndexError: list index out of range` at `runner.state.funding_events[0]`.
- GREEN, restored owner-approved post-bar snapshot: `1 passed in 0.07s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## R5 / F-7 MEDIUM - refusal precedence

**REPAIRED.** Commit `6172c916e6fa03eea76e7863c48c4deb0fa70fb5`
(`fix(mtc-v2): preserve missing funding refusal precedence`).

The runner validates the event collection before either rule field, so `events: null` retains the
item-3 token even when both rule values are unsupported (`core/runner.py:721-752`). The regression
constructs exactly that combined-invalid record and asserts the specific missing-event code
(`test_runner_corrected.py:486-503`).

- RED: `1 failed`; quoted mismatch:
  `REFUSED_ECONOMIC_INPUT != REFUSED_MISSING_FUNDING_EVENT`.
- GREEN, precedence plus production-record regression: `2 passed in 0.07s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## LOW dispositions

### F-1 - absent `events` member

**REPAIRED.** Commit `24da05176257c8e7c67e73c69129c6e7fbba5ed1`
(`fix(mtc-v2): refuse absent funding events`). The runner no longer defaults an absent member to an
empty tuple; absent and non-list values reach the typed refusal while a present empty list remains
valid (`core/runner.py:731-736`). The modified-copy test removes the key and asserts the exact token
(`test_runner_corrected.py:506-523`).

- RED: `1 failed`; quoted failure: `Failed: DID NOT RAISE EconomicsRefusal`.
- GREEN, absent-key and null-record cases: `2 passed in 0.07s`; full runner file `35 passed` at that
  commit.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

### F-5 - instance-scoped memo

**REPAIRED/ASSURED.** Commit `bcae0b372bd22868b0abf1819d1d762579637b15`
(`test(mtc-v2): cover reused runner funding`). R1 removed the instance memo; this separate commit
pins reuse by calling `run()` twice on the same instance with lifecycle 1 then lifecycle 2 and
requiring both pair keys/rows (`test_runner_corrected.py:354-367`). The final active-code grep
quoted `NO_ACTIVE_MEMO_MATCHES` for `_evaluated_funding_event_ids`.

- RED, equivalent old instance-memo mutation: `1 failed`; the right side contained the missing
  `('TEST-FUND-1', 2)` pair.
- GREEN: `1 passed in 0.07s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

### F-8 - closed snapshot rule

**REFUTED AS A DEFECT; NO COMMIT.** The design and owner ruling admit exactly one snapshot rule,
`END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1`, and explicitly make an exact-timestamp fill count
(`P012_FRESH_DESIGN_V1.md:426,867-872`;
`OWNER_DECISIONS_2026-08-29_EVENING.md:303-311`). There is no second allowed rule whose boolean
could vary. The runner consumes the exact value, refuses an unsupported value, and places the
same-timestamp evaluation after bar entry processing (`core/runner.py:737-756,823-839,1630-1632`).

Quoted probe:

```text
F8_VALID rule=END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1 funding_rows=1 eligible=True
F8_INVALID refusal=REFUSED_ECONOMIC_INPUT detail=REFUSED_ECONOMIC_INPUT: unsupported position_snapshot_rule 'UNSUPPORTED_SNAPSHOT'
```

The focused valid-order plus rule-validation tests also measured `2 passed in 0.06s`
(`test_runner_corrected.py:281-306,406-438`).

### F-9 - invented `HOURLY_INTERVAL_END_V1` arithmetic

**REPAIRED; `DESIGN-GAP` REPORTED.** Commit
`77ac1662532d06f3d98c5578ee5c83335f797c67`
(`fix(mtc-v2): remove invented funding alignment`). The design names the convention but supplies no
line defining minute/second/microsecond validation (`P012_FRESH_DESIGN_V1.md:867-872`). The runner
therefore continues to validate the closed convention token but no longer invents timestamp
arithmetic (`core/runner.py:745-759`). The regression uses an actual supplied schedule event at
`00:00:30Z` and requires its real timestamp and pair key to survive
(`test_runner_corrected.py:441-462`).

- RED: `1 failed`; quoted refusal:
  `REFUSED_ECONOMIC_INPUT: funding event does not satisfy HOURLY_INTERVAL_END_V1`.
- GREEN, modified timestamp plus existing boundary test: `2 passed in 0.08s`; full runner file
  `37 passed` at that commit.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

### F-10 - pending-open arm coverage

**REPAIRED AS ASSURANCE.** Commit `2f3d4737f77ce932d8cdddba2adae89f1f4fb084`
(`test(mtc-v2): cover pending margin admission`). The pending corrected arm calls
`_apply_corrected_entry` (`core/runner.py:1925-1945`), and that common helper applies the final-fill
capital/margin check before state mutation (`core/runner.py:594-610`). The test selects the pending
arm with `margin_long_pct=2000`, requires no position/fill, and requires the pending marker to be
consumed (`test_runner_corrected.py:742-764`).

- RED, exact capital-check removal mutation: `1 failed`; quoted assertion showed a live LONG
  position where `None` was required.
- GREEN: `1 passed in 0.07s`.
- Post-commit replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

### F-11 - capital-block receipt

**REFUTED AS AN IMPLEMENTATION DEFECT; `DESIGN-GAP`; NO COMMIT.** Design step 8 requires the
capital/margin check (`P012_FRESH_DESIGN_V1.md:94-109`), which the runner performs
(`core/runner.py:603-609`). The closed receipt/result language names only minimum-notional
admission/refusal (`P012_FRESH_DESIGN_V1.md:1065-1066,1190-1200,1223-1234`); adding a capital
receipt would require the schema/design bytes this lane forbids
(`LANE_W283R2_REPAIR_ROUND2.md:7-9`).

Quoted probe after clearing the unrelated instrument-validation receipt:

```text
F11_PROBE opened=False decision_events=[] fill_events=0 position_qty=10.0
```

That confirms the verifier's observation while also confirming no entry mutation. It is a missing
design vocabulary, not authority to invent a receipt.

## Commit and replay ledger

| Finding | Commit | Subject | Frozen replay |
|---|---|---|---|
| F-2 | `73ff500a667e5b59c9f6c6fc631d7232422318dc` | `fix(mtc-v2): remove runner funding id memo` | 17/17, 34/34 exact |
| F-3 | `9c55d1d7873adc5146935654d1a261f04064d937` | `fix(mtc-v2): disposition pre-window funding` | 17/17, 34/34 exact |
| F-4 | `ede8789d959699f6848ee74143c0723287a68bab` | `fix(mtc-v2): disposition post-window funding` | 17/17, 34/34 exact |
| F-6 | `a55f8dd80d3ca40d51ddd0ee3eef8fa63e6a09ff` | `test(mtc-v2): pin funding snapshot order` | 17/17, 34/34 exact |
| F-7 | `6172c916e6fa03eea76e7863c48c4deb0fa70fb5` | `fix(mtc-v2): preserve missing funding refusal precedence` | 17/17, 34/34 exact |
| F-1 | `24da05176257c8e7c67e73c69129c6e7fbba5ed1` | `fix(mtc-v2): refuse absent funding events` | 17/17, 34/34 exact |
| F-5 | `bcae0b372bd22868b0abf1819d1d762579637b15` | `test(mtc-v2): cover reused runner funding` | 17/17, 34/34 exact |
| F-9 | `77ac1662532d06f3d98c5578ee5c83335f797c67` | `fix(mtc-v2): remove invented funding alignment` | 17/17, 34/34 exact |
| F-10 | `2f3d4737f77ce932d8cdddba2adae89f1f4fb084` | `test(mtc-v2): cover pending margin admission` | 17/17, 34/34 exact |

F-8 and F-11 are probe-backed no-commit dispositions, so the one-finding/one-commit rule does not
create empty commits (`LANE_W283R2_REPAIR_ROUND2.md:14-15,27-31`).

## Final verification

Commands ran from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` unless stated otherwise.

| Command | Exit | Measured result |
|---|---:|---|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | **255 passed in 3.82s** |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | **18/18 declared dispositions**: 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1`; `NON_ACCEPTING_SELFTEST` |
| `$env:PYTHONPATH='00_PYTHON'; python -m pytest 00_PYTHON/mtc_v2/tests --ignore=00_PYTHON/mtc_v2/tests/corrected_vnext -q` from the stage root | 0 | **142 passed in 1.31s** |
| `git diff --check 511496da..HEAD` before the gate | 0 | clean |

Before the canonical gate, `git status --short` was empty. The repair diff from prior report commit
`511496da` contained exactly:

```text
MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py
MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py
MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py
```

### Canonical gate - run exactly once

The single authorized invocation was:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=2
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
catalog_counts: RED=9 GREEN=8 PROBE=10
acceptance_blockers=9
refusal_count=10
```

Complete refusal list:

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` - `mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.json`.
2. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
3. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
4. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-02-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
5. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-04-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
6. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
7. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
8. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-06-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
9. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-07-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
10. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-08-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.

The nine probe refusals are the known immutable-manifest condition the lane assigns to a later Lead
act; no probe manifest was touched (`LANE_W283R2_REPAIR_ROUND2.md:29-31`). The gate was not rerun.

## Discrepancies

1. **R4 cites the wrong design lines for ordering.** The prompt cites design lines 437-438
   (`LANE_W283R2_REPAIR_ROUND2.md:22`), but line 437 defines the funding-to-cash projection and line
   438 is blank. The controlling same-timestamp sentence is line 426
   (`P012_FRESH_DESIGN_V1.md:426,437-439`).
2. **R4's “inverted” characterization conflicts with the binding owner ruling.** Owner decision 46
   says an entry fill at the exact payment timestamp counts (`OWNER_DECISIONS_2026-08-29_EVENING.md:303-311`).
   Therefore funding must snapshot after that bar's entry evaluation, not before it. The repair
   preserves the owner-approved order and replaces the misleading equity-only test with a
   lifecycle/eligibility regression.
3. **No design line defines `HOURLY_INTERVAL_END_V1` timestamp arithmetic.** The design supplies the
   exact token at lines 867-869 but no minute/second/microsecond rule. Per the prompt's explicit
   `DESIGN-GAP` instruction (`LANE_W283R2_REPAIR_ROUND2.md:24`), the invented check was removed and
   no new interpretation was substituted.
4. **F-11 cannot be repaired inside the authorized byte fence.** The implementation correctly
   blocks the entry, but the closed design has no capital/margin receipt; adding one requires a
   later schema amendment (`P012_FRESH_DESIGN_V1.md:1223-1234`). The prompt forbids schema/design
   changes (`LANE_W283R2_REPAIR_ROUND2.md:7-9`), so this is reported as `DESIGN-GAP` rather than
   silently inventing a receipt.

The report-containing commit cannot include its own stable SHA; that SHA is supplied in the final
chat close.

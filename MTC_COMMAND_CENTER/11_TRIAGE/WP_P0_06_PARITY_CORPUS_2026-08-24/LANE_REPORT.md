# Lane C Report — WP-P0-06 Parity Corpus Inventory

Date: 2026-08-24
Audit tier: T1
Status: READY FOR LEAD ACCEPTANCE

## Result

The lane objective is complete. The inventory establishes that Corpus A and Corpus B exercised different Pine labels, different Python implementations, different case/data scopes, and different comparison contracts. Therefore, the March 99.54% and April 47% figures are not a temporal-regression comparison. Corpus C is recorded as unavailable after a worktree-wide and all-Git-object search. Corpus D is pinned as an exact 858-entry-signal comparison, not exit/lifecycle parity.

No repository-wide parity percentage is authorized by this work package.

## Deliverables

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/SEARCH_LOG.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/LANE_REPORT.md`

## Self-QA

- [x] Read the lane specification in full before acting.
- [x] Verified isolated worktree, expected branch, clean starting state, and base/`origin/master` at `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`.
- [x] Read brief section F-7 before searching corpus artifacts.
- [x] Swept all four corpora and their referenced call chains/results.
- [x] Separated independent executions from reuse counts.
- [x] Named every unresolved Corpus A overall failure and both Corpus B mismatches.
- [x] Marked absent evidence with the required `UNKNOWN — <what was searched>` form.
- [x] Confirmed Corpus C reports are absent from the worktree and every Git ref; did not read the frozen legacy checkout.
- [x] Did not run a backtest, parity harness, test, fixture generation, deploy, host, WSL, Docker, network, broker, exchange, testnet, or live-trading action.
- [x] Did not invoke Claude, another AI CLI, or a subagent.
- [x] Did not modify Pine, parity implementation, `MTC_V2`, Bridge runtime, schema, tests, fixtures, or any evidence corpus.
- [x] Wrote only the three new files in the lane's allowed directory.
- [ ] Lead-owned Gate 5 T1 audit and acceptance (outside implementer authority).

## Exact staged file list

The pre-commit cached-name verification must contain exactly:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/SEARCH_LOG.md
```

## Commit

Required message:

```text
docs(wp-p0-06): parity corpus inventory closing O-13 (T1, lane C 2026-08-24)
```

Commit SHA(s): reported in the final lane handoff after commit. A commit cannot embed its own SHA because changing this file changes the Git object ID.

## Open issues

1. Corpus A does not pin its generation-time Pine/Python source hashes, exact chart timeframe/date window, or full `tw_*` vector.
2. Corpus B does not pin its generation-time Pine/Python source hashes, final aggregate timestamp, or `tw_*` vector; its named Pine source is absent.
3. Corpus C's Markdown and JSON reports are unavailable; all claimed counts remain unverified.
4. Corpus D has no exit/lifecycle comparison.
5. Lead acceptance/audit remains required before downstream Git sequencing.

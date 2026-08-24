# Lane B Report — WP-P0-15 Branch Freshness

## Status

Implementation and implementer self-QA are complete. Audit tier is **T1**, fixed by the accepted
lane contract. Independent Gate 5 acceptance remains owned by the Claude Fable Lead.

No Pine, parity, MTC_V2, Bridge runtime, schema, deployment, host, credential, network, Docker,
WSL, broker, testnet, live, or trading surface was touched. No command accessed or mutated the
dirty `C:\LAB\Tradingview_LAB_CLEAN` checkout or any other lane worktree.

## Delivered

- `MTC_COMMAND_CENTER/tools/repo_guard.ps1`: offline freshness check against local
  `origin/master`; prints local tip commit age; default stale threshold is more than 30 commits
  behind; `-MaxBehindCommits` overrides the threshold explicitly and
  `MTC_REPO_GUARD_MAX_BEHIND_COMMITS` overrides the default; blocking is the default and
  `-WarnOnlyStaleBranch` is the diagnostic opt-out.
- `CLEAN_WORKTREE_PROCEDURE.md`: verify target, create isolated worktree, verify clean status and
  exact HEAD, run the freshness guard, and follow non-destructive teardown/preservation
  instructions. Invalid commit resolution now reaches the procedure's friendly error.
- `RED_GREEN_EVIDENCE.md`: literal D026 RED/GREEN/control commands and real output.
- `MTC_REPO_GUARD_USAGE.md` and `MTC_REPO_GUARD_PROTOCOL.md`: concise freshness configuration,
  warn-only, and stale-branch remedy documentation.
- This report.

The threshold uses commit distance because it is deterministic from the locally known refs and
does not require wall-clock policy guesses. The local origin tip's commit age is always printed so
an old local reference is visible; the guard never fetches.

## Commands and self-QA

- Verified initial branch, cleanliness, `HEAD`, and local `origin/master`; all pointed to the
  accepted start `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`.
- Ran the unmodified guard before editing: `RESULT: PASS`, rc 0.
- Confirmed Windows PowerShell version `5.1.26100.9168` and executed the modified guard with it.
- Ran `git diff --check` and `git diff --cached --check`: no errors.
- D026 RED: exact guard blob `75ff5e3b3afb030291bfeb95ff4c0312af6a3ea1` from
  `fbb05d7f` passed the 528-behind branch without a stale warning, rc 0.
- D026 GREEN: modified guard flagged `STALE BRANCH`, set `RESULT: BLOCKED`, rc 1, on the same
  worktree.
- Control after substantive commit: empty `git status --porcelain`, zero commits behind,
  `[dirty] clean`, `RESULT: PASS`, rc 0.
- Canonical `powershell.exe -File` checks on the 528-behind fixture: default mode emitted
  `RESULT: BLOCKED`, rc 1; `-WarnOnlyStaleBranch` emitted the STALE warning and `RESULT: PASS`,
  rc 0; environment threshold 600 and parameter threshold 600 each emitted `RESULT: PASS`, rc 0.
  The parameter run used a conflicting environment threshold of zero and still selected 600.
- Falsified the merge-base probe in a PowerShell 5.1 child: the guard emitted
  `[freshness] unavailable`, `RESULT: BLOCKED`, rc 1 instead of terminating at `.Trim()`.
- Exercised the procedure's invalid-target snippet: it emitted the friendly
  `Target is not a valid local commit: definitely-not-a-local-commit` message.
- Ran the full repaired guard on this zero-behind worktree: `RESULT: PASS`, rc 0.
- Removed `C:\WPP015_TMP_STALE` only after clean-status verification; deleted only
  `tmp/wp-p0-15-stale-demo-20260824`; verified path absent and branch lookup rc 1.

Acceptance-gate self-QA: **PASS**. The old guard failed to detect the deliberately stale branch;
the new guard detected and blocked it; the new guard passed a clean fresh worktree; and the dirty
canonical checkout remained untouched.

Parity/Pine/MTC impact: none. The only executable change is the repo preflight guard; it remains
read-only and offline.

## Branch commit inventory and repair staged paths

All commits on this branch after its `origin/master` base, with one-line contents:

- `37b055b6702cb04d089ff4b5a989129b61c3d93b` — branch-freshness guard and clean-worktree
  procedure.
- `6dcdd0591624a471aebcd405c7a5b41f15312250` — D026 RED/GREEN evidence and lane report.
- `10876fb9eb818b00141e8b808fe6a4d706ffc06e` — finalized evidence metadata.
- `HEAD` — repair round 1: warn-only switch, reachable fail-closed paths, executable override
  evidence, procedure fixes, protocol docs, and this complete branch inventory. `HEAD` is used
  because a commit cannot embed its own SHA without changing that SHA; the exact hash is printed
  in the implementer handoff.

Exact paths staged for the repair commit:

```text
MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md
MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_15_FRESHNESS_2026-08-24/CLEAN_WORKTREE_PROCEDURE.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_15_FRESHNESS_2026-08-24/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_15_FRESHNESS_2026-08-24/RED_GREEN_EVIDENCE.md
MTC_COMMAND_CENTER/tools/repo_guard.ps1
```

## Open issues

- No implementation or self-QA issue is open.
- Lead-owned T1 Gate 5 review/acceptance and any later git sequencing remain pending.
- Nothing was pushed or merged.

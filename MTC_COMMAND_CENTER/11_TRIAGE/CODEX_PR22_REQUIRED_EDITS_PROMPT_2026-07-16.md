# CODEX PROMPT — PR #22 Gate-5 REQUIRED EDITS round (2026-07-16)

## Ordering — do NOT start this before Task B

Task B (bridge `data_restore_timeout_s` 60→300s) from
`11_TRIAGE/CODEX_GATE5_PR22_AND_BRIDGE_TIMEOUT_PROMPT_2026-07-16.md` is approved, time-sensitive
(P2 sits DISARMED waiting on it), and comes FIRST. Finish Task B, STOP for Fable audit, and only
then start this prompt.

## Context

Your independent Gate-5 (`11_TRIAGE/CODEX_GATE5_FINDINGS_PR22_2026-07-16.md`, `cc59c931`)
returned BLOCK with 10 REQUIRED EDITS. Fable audited your report on real code and confirmed
every finding (`11_TRIAGE/FABLE_AUDIT_CODEX_GATE5_PR22_2026-07-16.md`): the BLOCK stands and
your edit list is adopted as binding. This prompt is the build order for those edits.

Work in worktree `C:\G5R` on `feature/exit-aware-gauntlet` (PR #22). The repo hook flips HEAD to
master between tool calls in the MAIN worktree only; in a dedicated worktree commit normally,
with explicit paths (never `git add .`/`-A`).

## Scope (hard rails — identical to the previous round)

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/` (new/changed tools + tests) and
  `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md`
  ONLY.
- `mega_walk_forward.py` stays BYTE-IDENTICAL (self-parity anchor). No Pine, MTC_V2, parity,
  schema, broker, bridge, or live-runtime path.
- NO real-data execution of any kind: no backtest, download, smoke, gauntlet-on-real-data,
  runner, server, paper, broker action. Mocked unit tests only.
- Secret grep `[0-9a-fA-F]{64,}` = 0 before every commit.

## The 10 edits (authority: your findings doc §"REQUIRED EDITS"; details there are binding)

1. **Frozen confirmation manifest** — machine-readable JSON: exact symbols + acceptance rules,
   primary + four literal stars, timeframe, ordered exits, window, job keys/count, data-manifest
   path + SHA-256, approved engine commit, CPCV/PBO geometry; plus a digest of the manifest
   itself. Runner and gauntlet both verify against it.
2. **DSR post-processor** — a tested tool that computes `du_cell`/`du_family` with exact
   equations, primary and secondary N, pool-row manifest, exclusions, `ddof`, missing-value
   policy, rounding. NEVER uses engine DSR at `grid_n=1`.
3. **Historical ledger** — replace the N=5,795 summary with an artifact-level ledger
   (path/date/window/symbol/TF/exit/config/inspection/include-exclude reason) + deterministic
   dedup rule.
4. **Freeze gauntlet geometry** — exactly 5 configs, 6 periods, 15 CPCV splits, 10 CSCV
   combinations, exact thresholds and cell stamps asserted in `verdict()`/`run_cell`; any
   mismatch = GAUNTLET_FAIL/STOP.
5. **Remove mutable knobs** — confirmation path rejects `--n-groups`/`--max-combinations`
   overrides; PBO truncation that changes the combination count for a confirmation cell is a
   failure, not OK; add a library-level approval boundary around real-data orchestration (not
   just the CLI flag).
6. **Strict runner parser** — runner-owned argparse that REJECTS all strategy/symbol/timeframe
   overrides including equals-forms; asserts accepted manifest + digest, approved engine commit
   (hash, not just cleanliness), empty isolated output dir, exact pre-run job set, exact
   post-run row/job-key/stamp set.
7. **Exit-blind post-processors** — thread + stamp `exit_mode` in `finalize_bootstrap_bh.py`
   and `reference_producer.py` or make them refuse non-`fixed_2R` rows; add explicit
   confirmation-ineligible refusals to `single_strategy_backtest.py` and both rigorous runners.
8. **Decision precedence rewrite (pre-reg §10)** — E/STOP evaluated first and overrides all;
   A requires secondary PASS and ≥2 fully-passing groups; every other exit-incremental outcome
   maps to A′; then B/B′/C/D. Remove the §8-vs-§10 contradiction.
9. **Acceptance-drop arithmetic (pre-reg §§5-9)** — freeze the accepted list pre-smoke; derive
   `expected_rows = 2 × accepted_count`, `m`, the BH family, and the secondary-ledger treatment
   from it; fix §11's overstated "applied" claims (old edits 5/7/10/11/14 were NOT applied).
10. **Adversarial tests** — argv forms (separated + equals), arbitrary manifest/commit,
    missing/extra rows and job keys, wrong stars/groups, truncated PBO, missing DSR, secondary
    failure, partial-group gauntlet, STOP precedence. Each test must FAIL on the pre-edit code
    (prove it by running the new tests against `f72b377a` and pasting the failures), then pass
    on the edited code.

Also apply the A2 claim-narrowing from Fable's audit: keep the file-level byte-identity claim
for `mega_walk_forward.py`, narrow output claims to "legacy fixed_2R numeric fields unchanged;
schema adds a stamp", and add a frozen legacy golden-output test comparing all pre-existing
numeric fields, classifications, and ordering.

## Definition of done

- All 10 edits + A2 narrowing implemented; full tools suite green from `03_QUANTLENS/tools/`
  (`python -m pytest tests/ -q`, PYTHONUTF8=1); adversarial tests proven to fail pre-edit.
- `mega_walk_forward.py` byte-identity re-proven (`git diff master -- ...` empty for that file).
- Evidence-rich report in `11_TRIAGE/CODEX_PR22_EDITS_REPORT_2026-07-16.md`: commands + pasted
  outputs + file:line for every edit.
- Commit(s) on `feature/exit-aware-gauntlet` with explicit paths; push.
- **STOP for Fable re-review.** Do not touch the run-approval question, acquisition, smoke, or
  any real data. D016 stays unspent.

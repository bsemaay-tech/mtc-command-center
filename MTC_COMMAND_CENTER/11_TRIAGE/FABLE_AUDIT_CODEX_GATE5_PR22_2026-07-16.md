# Fable Audit — Codex Independent Gate-5 of PR #22 (2026-07-16)

Auditor: Claude Fable 5 (designer/implementer of PR #22 — this audit verifies the REVIEW, not
the design; the review's independence is the point of the exercise).

Audited artifact: `11_TRIAGE/CODEX_GATE5_FINDINGS_PR22_2026-07-16.md`, committed by Codex GPT-5
at `cc59c931` on `feature/exit-aware-gauntlet` (worktree `C:\G5R`), reviewing PR #22 at
`f72b377a` against master `8721bce0`.

## Verdict on the Codex report: VERIFIED — the BLOCK stands

Every load-bearing claim was re-checked against real code in `C:\G5R` (not against the report's
prose). No fabricated line references, no overstated findings, no invented test results found.
The suite claim reproduces: `python -m pytest tests/ -q` → **108 passed** (independently re-run
by Fable, 2026-07-16).

PR #22 is **BLOCKED at Gate-5**. No run-approval question goes to Barış until the REQUIRED
EDITS are applied and independently re-reviewed. D016 remains unspent.

## Per-finding verification (all on real code)

| Finding | Codex verdict | Fable check | Result |
|---|---|---|---|
| A1 virginity | OK (local corpus) | not re-scanned (Codex reproduced Fable's own scan + broadened to pickles/xlsx) | accepted; limitation honestly stated |
| A2 parity claim | FINDING | `cpcv_validator.py:45-50`, `multiwindow_oos.py:58-62` read; test 88-94 is a spy, not a golden compare | **CONFIRMED** — see nuance below |
| A3 exit-blind tools | FINDING | `finalize_bootstrap_bh.py:83` calls `M.simulate_slice(...)` with NO `exit_mode`; `reference_producer.py` has zero exit threading | **CONFIRMED** |
| A4 statistics | FATAL | `deflated_sharpe_pvalue` returns `nan` at `n_trials <= 1` (`mega_walk_forward.py:~1517`); `grid_n = len(GRIDS[strat])`; runner `apply()` injects exactly ONE config → every row `dsr_p_value=None`, `dsr_robust=False`; grep `du_cell|du_family` over `03_QUANTLENS/tools/` = **zero hits** — the pre-reg's primary statistic has NO executable implementation | **CONFIRMED FATAL** |
| A5 gauntlet geometry | FATAL | `run_cell` keyword args expose `n_groups/test_groups/max_combinations`; accepts ≥1 star (contract: exactly 4); `verdict()` asserts thresholds only — never `splits==15`, `candidate_count==5`, `cscv_combinations==10`; CLI exposes `--n-groups/--max-combinations`; approval check is CLI-only (`run_cell` importable ungated); `test_run_cell_end_to_end_stamped` PASSES with `n_groups=3` + 2 stars; `estimate_pbo` keeps `status=OK` under truncation | **CONFIRMED FATAL** |
| A6 runner guards | FATAL | `assert_scope` checks only separated `--tf/--timeframe` tokens (equals-forms skip the check); `main()` suppresses the frozen-universe injection on an exact `--symbol`/`--strategy` token (so `--symbol BAD` runs ONLY BAD); engine argparse uses `action="append"` so equals-forms merge with injected values; manifest check = existence only; engine check = dirtiness of one file, not the approved commit; NO post-run row/job verification | **CONFIRMED FATAL** |
| A7 power | OK (plausible) | arithmetic checked (8,850/6≈1,475; 2 groups ≈2,950 bars); Stage-1 trade counts are from other configs/symbols — "plausible, not proven" is the correct strength | accepted |
| A8 downloader | OK | AST-compare methodology sound; `alpaca_download_dataset.py:65-75,228-253` supplies every `find_ds`/`load_df` field | accepted |
| A9 decision table | FATAL | Pre-reg §10 row A does NOT require secondary PASS while §8 says secondary failure "caps at A′" and §10 precedence `A > A′` — internal contradiction; the ≥2-groups-span/1-group-passes outcome maps to NO row; E absent from the precedence sentence; §5 drops (≥8 floor) conflict with fixed 32-row / `m=16` / `EXPECTED_ROWS=32` wording | **CONFIRMED FATAL** |

### Nuance the next editor must keep (A2)

The handoff claim "engine `mega_walk_forward.py` byte-identical" is TRUE at file level (PR #22
does not touch the file) and remains the self-parity anchor. Codex is right that OUTPUT
byte-identity is impossible (the exit stamp is a new field) and that no golden numeric-parity
test exists. Correct fix: keep the file-level claim, narrow the output claim to "legacy fixed_2R
numeric fields unchanged; schema adds a stamp", and add the frozen golden-output test.

## What this changes

1. Codex's 10 REQUIRED EDITS are adopted as the binding edit list (superset of Fable's
   self-review; items 5/7/10/11/14 of the ORIGINAL 15 edits were wrongly marked applied in the
   pre-reg §11 — that overstatement is itself confirmed).
2. Sequencing: Codex executes **Task B (bridge timeout fix) FIRST** — P2 sits DISARMED waiting
   on it and it is fully approved; the PR #22 edit round follows
   (`11_TRIAGE/CODEX_PR22_REQUIRED_EDITS_PROMPT_2026-07-16.md`).
3. After the edit round: independent re-review (Fable audits Codex's edits on real code), THEN
   the single formal run-approval question to Barış. Not before.

## Execution statement

No backtest, download, smoke, gauntlet, runner, server, paper, broker, or real-data execution
was performed in this audit. Verification = code reading + the mocked unit suite (108 passed)
+ SQLite reads of the P2 monitoring DB (read-only).

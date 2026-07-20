# Codex Independent Gate-5 Findings — PR #22 (2026-07-16)

Reviewer: Codex GPT-5, independent of Claude Fable 5 (designer, implementer, and self-reviewer).

Target: PR #22, `feature/exit-aware-gauntlet`, reviewed at `f72b377a` against `master`
`8721bce0` in dedicated worktree `C:\G5R`.

## Overall verdict: BLOCK

PR #22 is not Gate-5 clear and does not support a run-approval decision. The held-out-symbol
scan is clean in the local artifact corpus, the downloader override is additive, and the mocked
unit suites pass. Those facts do not close the blocking defects:

1. the one-config runner makes the engine DSR undefined and no PR tool computes the pre-reg's
   proposed replacement `du_cell`;
2. the gauntlet accepts mutable group/config/combinations geometry and arbitrary cell specs;
3. the runner accepts non-frozen symbols, strategies, timeframe forms, and arbitrary manifests;
4. the N=5,795 table is arithmetic-correct but is not the required artifact-level historical
   ledger; and
5. the decision table can select A when the secondary check fails and leaves mixed gauntlet
   outcomes unmapped.

The D-decision remains Barış's only after the required edits are applied and independently
re-reviewed. This report does not make or spend D016.

## Review evidence and allowed tests

- Full diff: 9 paths, 1,221 insertions / 21 deletions; no Pine, MTC_V2, parity, schema, broker,
  or live-runtime path changed.
- Targeted mocked suite: `python -m pytest tests/test_exit_aware_gauntlet.py -q` -> **29 passed**.
- Full mocked tools suite: `python -m pytest tests/ -q` -> **108 passed**.
- Unit-level legacy comparison against detached `master`: normalized CPCV, multi-window, and
  legacy candidate-ID outputs were equal (`CURRENT_EQ_MASTER True`).
- No backtest, download, smoke, gauntlet, runner, server, paper, broker, or real-data execution
  was performed.

## A1 — Symbol virginity: OK (current local corpus; reproducibility limitation)

The self-review's exact 145-file pattern was reproduced from the local ignored artifacts:
`^MEGA.*\.json$` across `03_QUANTLENS/05_BACKTEST_RESULTS/` and `research/`.

- Parsed files: 145; parse errors: 0.
- `GEN_KELTNER_BREAKOUT` result rows: 10,417.
- Distinct Keltner symbols: 68, matching the self-review.
- Frozen-symbol Keltner rows: 0/10,417.
- Frozen-symbol rows under other strategies in the same 145 MEGA artifacts: 0.
- Filename scan for `KELTNER` plus a frozen symbol: 0.
- All five local `dataset_manifest.json` files: none contains any frozen symbol, so no other
  local bundle was found to have already exposed these names.

Coverage was broadened beyond Fable's scan. Raw content found 426 Keltner-bearing artifacts
(348 JSON, 50 Markdown, 28 pickle). Safe `pickletools` opcode inspection found Keltner strings
but no exact frozen-symbol string in all 28 pickles; raw `PG`/`JNJ`/`JPM` byte hits were binary
coincidences. Five XLSX files were inspected through their XML; none contains Keltner.

Limitation: the 145-file corpus and nearly all result artifacts are git-ignored and absent from
the fresh PR worktree (which has only one tracked `05_BACKTEST_RESULTS` JSON). The claim is
reproducible on this machine's current local artifact store, not from PR #22 alone. Deleted,
external, or differently stored historical artifacts cannot be disproved by a repo scan.

## A2 — Parity claims: FINDING

Code reading supports fixed-2R numeric continuity: `cpcv_validator.py:45-50` and
`multiwindow_oos.py:58-62` resolve a missing exit to `DEFAULT_EXIT_MODE`, and the PR does not
change `mega_walk_forward.py`. The independent mocked comparison to `master` produced identical
normalized numeric outputs.

The tests do not pin the stated "byte-identical" claim. `test_exit_aware_gauntlet.py:88-94`
checks that new code passes `fixed_2R` to a spy and adds an `exit_mode` field; it does not compare
a complete pre-change artifact or golden byte stream. Output cannot literally be byte-identical
because the stamp is new. `test_faz3b_self_parity_module_present` at lines 257-259 checks only
that a file exists. Against pre-change modules the new suite would fail because the new
arguments/helpers are absent; that proves feature coverage, not numerical parity.

Required fix: narrow the claim to "legacy fixed_2R numerical behavior is unchanged; the output
schema intentionally adds an exit stamp," and add a frozen legacy golden-output test comparing
all pre-existing numeric fields, classifications, and ordering.

## A3 — Exit-threading completeness: FINDING

The direct confirmation path is exit-aware at the visible calls: engine worker
`mega_walk_forward.py:1311-1314,1355`; CPCV `cpcv_validator.py:45-50,108`; config matrix
`exit_aware_gauntlet.py:44-65`; multi-window/neighbours `multiwindow_oos.py:58-62,98-126`.

Exit-blind tools remain and are plausibly mistaken for confirmation-capable:

- `finalize_bootstrap_bh.py:67-118` selects PASS rows, recomputes lockbox returns at line 83
  without `exit_mode`, then overwrites BH and `robust_final`. On trail rows it silently uses
  fixed-2R evidence.
- `reference_producer.py:38-112` recognizes trail only from a special strategy ID and calls the
  engine without row/spec `exit_mode`; it is unsafe for swept Keltner trail rows.
- `single_strategy_backtest.py:32-60` exposes no exit argument and still feeds CPCV rows into
  the legacy row-as-candidate PBO path; it is not a replacement confirmation runner.
- `rigorous_walk_forward.py:266,405-408` and `rigorous_walk_forward_parallel.py:254,431-434`
  have separate fixed-exit simulators and no exit stamp.

Required fix: every generic post-processor that can consume a swept row must thread and stamp
`exit_mode`, or refuse non-`fixed_2R` input. Add an explicit confirmation-ineligible refusal to
`single_strategy_backtest.py`.

## A4 — Statistics: FATAL

### Bonferroni arithmetic

The one-sided bound is correct. With `p_cell = 1 - du_cell`, Bonferroni gives
`p_family <= min(1, m*p_cell)`, hence
`du_family = 1 - min(1, m*(1-du_cell))`. At `m=16`, `du_family >= 0.95` requires:

`16*(1-du_cell) <= 0.05` -> `du_cell >= 1 - 0.05/16 = 0.996875`.

But `m` and the row family are not immutable after acceptance drops. Section 5 permits drops,
section 6 says BH uses 32 rows, section 8 says `m` is cells actually scored, and section 9 says
row count must be 32 "after documented acceptance drops" (`...PREREG...md:100-107,116-125,
162-170,213-218`). Expected count must be `2 * accepted_symbol_count`, frozen before smoke.

### The primary DSR is not executable

The runner injects one config (`faz3b_newsymbol_runner.py:53-55,93-95`). The engine sets
`grid_n = len(GRIDS[strat])` (`mega_walk_forward.py:1682-1694`), while DSR returns `NaN` when
`n_trials <= 1` (`mega_walk_forward.py:1507-1517`). Thus this runner yields
`dsr_p_value=None` and `dsr_robust=False` for every row. No PR file computes the proposed
`du_cell`, `du_family`, or historical N=5,795 diagnostic.

Section 8 also omits the promised equations, exact primary `N`, pool-row manifest, and executable
post-processor (`...PREREG...md:148-170`). Prior REQUIRED EDIT 7 is not applied.

### N=5,795: listed arithmetic correct, ledger incomplete

The June-29 artifact shows 357 Keltner cells = 51 symbols * 7 timeframes, each with
`trial_count=16`; `51*7*16 = 5,712`. The displayed sum is correct:

`16 + 15 + 20 + 5,712 + 32 = 5,795`.

It is not a historical-union ledger. The local 145-file corpus contains 10,417 Keltner result
rows across 68 symbols. Many are duplicates/resumes/superseded, but section 8 does not enumerate,
deduplicate, or give include/exclude reasons. Its three-column table at `...PREREG...md:177-184`
does not satisfy prior REQUIRED EDIT 5's path/date/window/symbol/TF/exit/config/inspection/reason
contract. N=5,795 is a listed-component total, not a re-derived complete union.

### Downgrade-only is not airtight

Section 8 says secondary failure caps the outcome at A-prime (`...PREREG...md:187-189`). Row A
does not require secondary PASS, row A-prime includes its failure, and precedence is
`A > A-prime` (`...PREREG...md:224-232`). Both match and precedence selects A.

Required fix: implement/test an explicit DSR post-processor with frozen inputs; attach the full
ledger/deduplication policy; define accepted-family arithmetic; and make A require secondary
PASS (or make secondary failure override A before evaluation).

## A5 — Gauntlet wiring: FATAL

The happy path is structurally correct: CPCV scores only the primary
(`exit_aware_gauntlet.py:118-129`), PBO is built from one cell/exit (lines 131-145), and missing
PBO data maps to GAUNTLET_FAIL. Dataset/load or unexpected exceptions abort rather than pass.

The approved geometry is not enforced:

- `run_cell` accepts any strategy, symbol, timeframe, exit, primary config, and >=1 star
  (`exit_aware_gauntlet.py:98-116`); the contract freezes one primary plus four exact stars.
- `n_groups`, `test_groups`, thresholds, and `max_combinations` are caller-controlled (lines
  98-101); CLI exposes mutable `--n-groups` and `--max-combinations` (lines 179-198).
- Verdict does not require `splits == 15`, `candidate_count == 5`,
  `cscv_combinations == 10`, exact stars, or exact cell identity (lines 69-95,160-174).
- The passing end-to-end test uses only two stars and `n_groups=3`
  (`test_exit_aware_gauntlet.py:323-343`), proving a non-pre-registered gauntlet can PASS.
- `--max-combinations 1` leaves PBO status `OK` with one record because every nonempty truncated
  set is valid (`probabilistic_pbo.py:99-164`).
- The CLI approval check is bypassable by import: tests call `run_cell` directly and the function
  has no approval check. It is an accidental-execution gate, not an approval boundary.

Required fix: assert exact frozen values; bind the cell spec to a prereg manifest digest; require
exactly 5 configs, 6 periods, 15 CPCV splits, and 10 CSCV combinations before PASS; separate
pure unit primitives from an explicitly approval-gated real-data library entry.

## A6 — Runner scope guards: FATAL

The guard does not inspect the actual strategy/symbol set and recognizes only separated
timeframe flags (`faz3b_newsymbol_runner.py:58-86`). `main` suppresses frozen injection merely
when an exact token exists (lines 98-120). Mocked direct checks proved these were accepted:

- `--symbol BAD`
- `--symbol=BAD`
- `--tf=4h`
- `--strategy GEN_DONCHIAN_BREAKOUT`
- `--strategy=GEN_DONCHIAN_BREAKOUT`

The engine uses repeatable append arguments (`mega_walk_forward.py:1606-1638`), so equals-form
values combine with appended approved values, while separated `--symbol BAD` suppresses the
frozen universe. Extra strategies also run after `apply()` mutates the Keltner grid.

Additional omissions:

- any existing JSON is accepted as manifest; exact path, symbol set, validation fields, and
  pre-registered digest are not checked (`faz3b_newsymbol_runner.py:70-73,89-90`);
- only dirtiness of one engine file is checked, not approved commit (lines 79-86);
- expected rows are printed but post-run job keys/count/stamps are never checked (lines 110-120);
- accepted pre-launch drops cannot be represented safely because universe/expected rows remain
  fixed at 16/32.

Required fix: use a strict runner-owned parser; reject all strategy/symbol/timeframe overrides,
including equals forms; verify accepted manifest+digest, approved commit, exact pre-run job set,
and exact post-run row/job-key set before success.

## A7 — Power / feasibility: OK (plausible, not proven)

At about 8,850 bars, six groups are `8,850/6 = 1,475` bars; each two-group test covers about
`2*1,475 = 2,950` bars. Stage-1 selected trail rows had 63, 60, 49, 39, 52, 49, and 50 lockbox
trades across SPY/QQQ/AAPL/MSFT/NVDA/AMZN/TSLA. This makes >=30 plausible, but most rows used
other selected configs and none proves low-volatility held-out ETFs.

The >=8-cell/>=2-group floor coherently makes underpower VOID/E rather than C/D. The table must
state E overrides all, and A4/A9 family-count contradictions must be fixed first.

## A8 — Downloader override: OK

An AST comparison to `master` showed default `build_universe()` exactly equals the old ordered
equity-plus-crypto list (51 entries), and global universes are unchanged. Explicit symbols keep
order and exclude crypto (`alpaca_download_dataset.py:65-75`).

Registration supplies every `mw.find_ds`/`mw.load_df` field: `symbol`,
`timeframe_normalized`, `ohlcv_validation_status`, `normalized_path`, plus source/provider, bar
count, timestamps, validation, session, adjustment, and SHA (`alpaca_download_dataset.py:228-253`;
`mega_walk_forward.py:886-895`).

## A9 — Gate hygiene: FATAL

Header/acquisition/execution/sign-off correctly say draft, unapproved, no run
(`...PREREG...md:3-13,84-107,192-218,261-279`). New-symbol is correctly primary; 2028 forward
remains fallback; design acceptance is distinguished from run approval.

Outcome mechanics are incomplete:

1. Secondary failure matches A and A-prime, while `A > A-prime` selects A.
2. If raw exit-incremental cells span >=2 groups but gauntlet passes only one group, A is false,
   "only 1 group" is false, and "gauntlet fails on every cell" is false: no row maps it.
3. E/STOP is VOID but omitted from the precedence sentence.
4. Pre-acceptance drops conflict with the 32-row STOP, fixed runner, BH wording, and N ledger.
5. Section 11 claims all prior edits applied, but 5, 7, 10, 11, 14 are not; 6, 8, 9, 12
   are partial.

Required fix: evaluate `STOP/E` first; define A only when fully passed exit-incremental cells
exist in >=2 groups and secondary passes; map every other exit-incremental outcome to A-prime;
then B/B-prime/C/D. Freeze adjusted counts after acceptance and before smoke.

## Verification of the 15 prior REQUIRED EDITS

| # | Status | Independent result |
|---:|---|---|
| 1 | OK | Draft/unapproved status explicit. |
| 2 | OK | Old six removed; current 16 clean in local corpus. |
| 3 | OK | Four groups frozen; >=2 required. |
| 4 | OK | One decision config plus four literal stars. |
| 5 | **FATAL** | No artifact ledger/deduplication; N=5,795 not established as union. |
| 6 | PARTIAL | Formula correct; `m`, BH family, row count, drops conflict. |
| 7 | **FATAL** | Exact N/pool/equations/tool missing; engine DSR undefined at grid_n=1. |
| 8 | PARTIAL | Cell truth table correct; aggregate A/A-prime incomplete. |
| 9 | PARTIAL | Main path threads exits; mutable geometry/exit-blind tools remain. |
| 10 | **FATAL** | Exact CPCV geometry is mutable and unchecked. |
| 11 | **FATAL** | Exact 5x6/10-combination matrix contract is unenforced. |
| 12 | PARTIAL | No substitution text exists; drops conflict with runner/rows. |
| 13 | OK | Non-evidentiary two-mode smoke and `ceil(1.5*16*smoke_seconds)`. |
| 14 | **FATAL** | Runner bypasses and manifest/commit/post-run checks missing. |
| 15 | OK | Earlier report, table, re-review checkbox, D016 unspent. |

## REQUIRED EDITS before another Gate-5

1. Add a frozen machine-readable confirmation manifest: exact symbols/acceptance, primary/four
   stars, timeframe, ordered exits, window, job keys/count, data manifest path+SHA, approved
   engine commit, CPCV/PBO geometry, and its digest.
2. Implement a tested DSR post-processor with exact equations, primary/secondary N, pool-row
   manifest, exclusions, `ddof`, missing policy, and rounding. Do not use engine DSR at grid_n=1.
3. Replace N=5,795 summary with the artifact ledger and deterministic dedup/include/exclude rule.
4. Freeze gauntlet geometry: 5 configs, 6 periods, 15 CPCV splits, 10 CSCV combinations, exact
   thresholds/cell stamps. Mismatch = GAUNTLET_FAIL/STOP.
5. Remove/reject mutable confirmation `--n-groups` and truncating `--max-combinations`; add a
   library-level approval boundary around real-data orchestration.
6. Strictly parse runner args; assert accepted manifest/digest, commit, empty isolated output,
   exact pre-run jobs, and exact post-run keys/count/stamps.
7. Thread/refuse swept exits in `finalize_bootstrap_bh.py` and `reference_producer.py`; mark
   single-strategy and rigorous runners confirmation-ineligible.
8. Rewrite decision precedence so E overrides all, A requires secondary PASS and >=2 fully
   passing groups, and all other exit-incremental combinations map to A-prime.
9. Freeze accepted list pre-smoke and derive `expected_rows=2*accepted_count`, `m`, BH family,
   and secondary-ledger treatment from it.
10. Add adversarial tests for argv forms, arbitrary manifest/commit, missing/extra rows/job keys,
    wrong stars/groups, truncated PBO, missing DSR, secondary failure, partial group gauntlet,
    and STOP precedence.

## NICE-TO-HAVE

1. Commit a deterministic virginity-scan script plus scanned-path digest/list.
2. Rename CPCV as a combinatorial temporal-placement test unless it refits purged training data.
3. Add a glossary for result row, config trial, decision/accepted cell, DSR N, BH m, Bonferroni m,
   and independent evidence unit.
4. Report held-out group correlations descriptively, never to add/drop cells post hoc.

## Could not verify without running (and therefore not verified)

- Held-out bar availability, validation, counts, timestamps, and provider behavior.
- Frozen-config trades, CPCV sufficiency, returns, DSR, BH-FDR, PBO, multi-window stability,
  runtime, disk behavior, or any decision outcome.
- Empirical group correlations and current Alpaca symbol/window availability.
- Corrected runner/gauntlet behavior on real artifacts.

## Execution statement

**No real-data run was performed.** No download, smoke, backtest, optimization, gauntlet,
runner, server, paper-trading, broker, or live action was performed. These findings authorize
none. PR #22 remains BLOCKED at Gate-5 until required edits are applied and independently
re-reviewed; the D-decision remains Barış's after that review.

# Lane P — BOM-tolerant reads in dashboard readers (D14)

Scope: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/{pipeline_reader.py,
audit_reader.py, optimization_reader.py, backtest_reader.py}` plus one new regression
test per file in the matching `apps/api/tests/test_*.py`. Follows up lane K's finding
#8 (`OVERNIGHT_LANE_K_NONPROTECTED_STATIC_HUNT_2026-09-07.md`): `heartbeat_reader.py`
and `mtc_v2_reader.py` already read with `encoding="utf-8-sig"` (the latter untouched
here — lane N owns it), but `pipeline_reader.py`, `audit_reader.py`,
`optimization_reader.py` and `backtest_reader.py` read the same PowerShell-produced
artifact family with plain `encoding="utf-8"`. A UTF-8 BOM (`﻿`) decodes fine
under plain `"utf-8"`, but `json.loads` then raises `JSONDecodeError: Expecting value:
line 1 column 1 (char 0)` on the BOM-prefixed string — every one of these call sites
already wraps that in `except Exception: ...` (or an outer caller does), so the file is
silently treated as unreadable/missing/error instead of being parsed. Fix: every
JSON/CSV/text **read** call (`Path.read_text`, `Path.open("r", ...)`,
`csv.DictReader` inputs) in these four modules now uses `encoding="utf-8-sig"`
(BOM-tolerant; still reads non-BOM files identically since `utf-8-sig` only strips a
BOM if present). No write path exists in any of the four modules (`mode="w"`,
`write_text`, `.write(` — none found). `errors=` arguments (`errors="replace"`,
`errors="ignore"`) are untouched. `mtc_v2_reader.py` was not opened.

## Changed lines

| File | Line | Before | After |
|---|---|---|---|
| `pipeline_reader.py` | 226 | `p.read_text(encoding="utf-8")` | `p.read_text(encoding="utf-8-sig")` |
| `pipeline_reader.py` | 236 | `p.read_text(encoding="utf-8")` | `p.read_text(encoding="utf-8-sig")` |
| `pipeline_reader.py` | 282 | `path.read_text(encoding="utf-8")` | `path.read_text(encoding="utf-8-sig")` |
| `pipeline_reader.py` | 324 | `p.open("r", encoding="utf-8", newline="")` | `p.open("r", encoding="utf-8-sig", newline="")` |
| `pipeline_reader.py` | 376 | `path.read_text(encoding="utf-8")` | `path.read_text(encoding="utf-8-sig")` |
| `pipeline_reader.py` | 418 | `path.open("r", encoding="utf-8", newline="")` (csv.DictReader input) | `path.open("r", encoding="utf-8-sig", newline="")` |
| `pipeline_reader.py` | 445 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `pipeline_reader.py` | 461 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `pipeline_reader.py` | 622 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `pipeline_reader.py` | 749 | `path.read_text(encoding="utf-8", errors="ignore")` | `path.read_text(encoding="utf-8-sig", errors="ignore")` |
| `audit_reader.py` | 866 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `audit_reader.py` | 1051 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `audit_reader.py` | 1095 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `audit_reader.py` | 1111 | `path.open("r", encoding="utf-8", newline="")` (csv.DictReader input) | `path.open("r", encoding="utf-8-sig", newline="")` |
| `audit_reader.py` | 1139 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `optimization_reader.py` | 196 | `path.open("r", encoding="utf-8", newline="")` (csv.DictReader input) | `path.open("r", encoding="utf-8-sig", newline="")` |
| `optimization_reader.py` | 261 | `summary_path.open("r", encoding="utf-8", newline="")` (csv.DictReader input) | `summary_path.open("r", encoding="utf-8-sig", newline="")` |
| `optimization_reader.py` | 357 | `path.read_text(encoding="utf-8", errors="replace")` | `path.read_text(encoding="utf-8-sig", errors="replace")` |
| `optimization_reader.py` | 380 | `path.read_text(encoding="utf-8")` | `path.read_text(encoding="utf-8-sig")` |
| `backtest_reader.py` | 356 | `path.read_text(encoding="utf-8")` | `path.read_text(encoding="utf-8-sig")` |

20 lines changed across 4 files (10 + 5 + 4 + 1), matching every `encoding="utf-8"`
occurrence found in the four modules (`grep -n 'utf-8'` before the change showed
exactly these 20 sites and no others; none are writes). `json_io.py`'s
`read_json_file` (plain `"utf-8"`) is a separate module not imported by any of the
four readers and was left alone — out of this lane's scope.

## Tests added (D026)

One regression test per reader, in its existing test file, each writing a
BOM-prefixed fixture (`"﻿" + json.dumps(...)`) into the same temp-directory
layout the file's other tests already build, and asserting the reader parses it
exactly like the non-BOM case:

- `tests/test_backtest_reader.py::test_reads_bom_prefixed_candidate_results_json` —
  BOM-prefixed `candidate_results.json`; asserts the resulting run has
  `status == "COMPLETED"` (not `"ERROR"`) and correct `symbols`/`trades` sums.
- `tests/test_optimization_reader.py::test_reads_bom_prefixed_run_config_json` — BOM-prefixed
  `run_config.json`; asserts `run_id`, `max_workers`, `warning` come from the file
  itself, not the `{}`-on-parse-failure fallback.
- `tests/test_audit_reader.py::test_source_index_counts_bom_prefixed_jsonl_record` —
  BOM-prefixed `AUDITED_CANDIDATE_EXTRACTION.jsonl` line; asserts
  `audit["source_record_count"] == 1` (the record is counted, not silently dropped).
- `tests/test_pipeline_reader.py::test_discovers_bom_prefixed_producer_spec` —
  BOM-prefixed `producer_spec.json` under `06_PROMOTED_TO_PARITY/<id>/`; asserts the
  candidate row exists at all (before the fix the row is missing entirely, not just
  missing a field, because `_iter_producer_specs` silently `continue`s past the
  unparseable file).

### RED (all 4 failing before the fix, reader files reverted to plain `"utf-8"`, test files as committed)

```
$ PYTHONUTF8=1 python -m pytest tests -q -p no:cacheprovider -k "bom"
...
E           AssertionError: 0 != 1
tests/test_audit_reader.py:102: AssertionError
______ BacktestReaderTests.test_reads_bom_prefixed_candidate_results_json ______
(fails inside build_backtest_status / candidate_results.json — run classified "ERROR")
________ OptimizationReaderTests.test_reads_bom_prefixed_run_config_json _______
E           AssertionError: 'bom_run_dir' != 'bom_run'
E           - bom_run_dir
E           ?        ----
E           + bom_run
tests/test_optimization_reader.py:88: AssertionError
________ PipelineReaderTests.test_discovers_bom_prefixed_producer_spec _________
E           AssertionError: 'QL_BOM_PROMOTED_SPEC' not found in {}
tests/test_pipeline_reader.py:245: AssertionError
=========================== short test summary info ============================
FAILED tests/test_audit_reader.py::CandidateAuditTests::test_source_index_counts_bom_prefixed_jsonl_record
FAILED tests/test_backtest_reader.py::BacktestReaderTests::test_reads_bom_prefixed_candidate_results_json
FAILED tests/test_optimization_reader.py::OptimizationReaderTests::test_reads_bom_prefixed_run_config_json
FAILED tests/test_pipeline_reader.py::PipelineReaderTests::test_discovers_bom_prefixed_producer_spec
4 failed, 122 deselected in 0.31s
```

All four regression tests fail before the fix (task required at least two; all four
failed here).

### GREEN (after restoring `encoding="utf-8-sig"` in the four readers)

```
$ PYTHONUTF8=1 python -m pytest tests -q -p no:cacheprovider -k "bom"
....                                                                     [100%]
4 passed, 122 deselected in 0.16s
```

### Full suite

```
$ PYTHONUTF8=1 python -m pytest tests -q -p no:cacheprovider
....................................................................... [ 56%]
.......................................................                  [100%]
126 passed, 1 subtests passed in 4.01s
```

122 pre-existing collected tests (one carries a `subTest`) + the 4 new BOM regression
tests = 126 passed, 0 failed.

### Static checks

```
$ ruff check --isolated --no-cache --select E9,F821,F811 \
    mcc_readonly/pipeline_reader.py mcc_readonly/audit_reader.py \
    mcc_readonly/optimization_reader.py mcc_readonly/backtest_reader.py \
    tests/test_pipeline_reader.py tests/test_audit_reader.py \
    tests/test_optimization_reader.py tests/test_backtest_reader.py
All checks passed!

$ git diff --check -- <same 8 files>
(no output, exit 0)
```

## Deviation: worktree isolation recovery

Mid-task, the four reader edits (`sed -i ... encoding="utf-8-sig" ...`) were first
run against the shared checkout `/home/user/mtc-command-center/...` via a `cd
/home/user/mtc-command-center && sed ...` command instead of this isolated worktree
(`/home/user/mtc-command-center/.claude/worktrees/agent-ae2fdbd09311de92a`), because
the very first read/grep passes on these files had also been pointed at the shared
checkout by mistake before the isolation boundary was noticed. The coordinator's
correction landed after self-correction was already underway. Recovery performed:
1. Confirmed via `pwd` that this session's persisted working directory is in fact the
   worktree, and that `git log --oneline -1` there was unaffected (still showed the
   correct `6babb341` post-merge commit) — only the four reader files' *working-tree
   bytes* in the shared checkout had been touched, nothing was staged or committed
   there.
2. Reverted the shared-checkout files with the exact inverse substitution
   (`sed -i 's/encoding="utf-8-sig"/encoding="utf-8"/g'` on the same 4 paths),
   verified with `grep -c 'utf-8-sig'` → `0` on all four and `grep -c
   'encoding="utf-8"'` → `10/5/4/1` (matching the pre-edit counts) — a lossless
   round-trip since no other line in those files matched either substitution target.
   No `git` command was run against the shared checkout at any point (add/commit/
   stash); the sandbox itself hard-refuses any `git` invocation that targets the
   shared checkout — via `cd` or via `-C` — from this worktree-isolated session, so a
   `git status`/`git diff --check` confirmation *in the shared checkout* could not be
   run by this agent. Textual re-inspection (`grep`) is the verification on record.
3. Re-applied the identical `sed` fix using relative paths with **no** `cd`, confirmed
   `pwd` was the worktree, and verified the resulting `git diff --stat` (run from the
   worktree) showed exactly the intended 4 files / 20 lines.
4. Fast-forwarded the worktree twice more as other lanes landed commits on the shared
   branch while this was in flight: `6babb341` → `607bf8fb` (picked up lane O's
   `ds_agent.py` report-path fix and lane N's `mtc_v2_reader.py`/
   `test_mtc_v2_reader.py` changes, confirmed via `git diff --name-only` first that
   neither touched any of this lane's 4 files) before finishing tests and committing.

No other content in the shared checkout was read from or written to beyond the initial
mistaken sed/revert on these same 4 files; no other lane's files were touched.

## NEXT ACTION

None required for D14/D026 — fix and tests are complete and green. Optional follow-up
(not done here, out of scope): `json_io.py:28` (`read_json_file`, used by
`read_model.py`) still reads with plain `"utf-8"` and would have the same BOM
fail-closed behavior if a BOM-prefixed artifact ever reaches it; a future lane could
apply the same one-line `-sig` fix there if `read_model.py`'s consumers are shown to
touch PowerShell-produced artifacts.

## WAITING FOR OWNER

Nothing.

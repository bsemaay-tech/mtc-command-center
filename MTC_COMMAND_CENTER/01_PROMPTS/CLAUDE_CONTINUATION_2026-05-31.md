# Claude Continuation — 2026-05-31

You are Claude continuing MCC + QuantLens triage work. The previous session completed an overnight v2 backtest sweep, manual reclassification, MCC audit, and DSR-relaxed analysis. This prompt is **token-efficient**: pointers > prose. Read referenced files, do not re-explain.

## CRITICAL — Read these FIRST (in order)

1. **`MTC_COMMAND_CENTER/PROJECT_HANDOFF.md`** — full state, pending work priority order
2. **`MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LESSONS_2026-05-31.md`** — every mistake and lesson (don't repeat them)
3. **`MTC_COMMAND_CENTER/11_TRIAGE/morning_report_2026-05-31.md`** — overnight aggregated results
4. **`MTC_COMMAND_CENTER/11_TRIAGE/focused_validation_report_2026-05-31.md`** — Tier-2 robust candidates (DSR ≥ 0.50)
5. **`MTC_COMMAND_CENTER/11_TRIAGE/mcc_audit_2026-05-31.md`** — MCC end-to-end audit (8.5/10)

## Git state

- Branch: `main`
- Latest commits (top 5):
  ```
  ae97a8ed docs(mcc): focused validation results + MCC end-to-end audit
  2e22255f feat(mcc): overnight v2 sweep — 19 iters, 6M case-folds, 3 BH-FDR survivors
  5b9f39f2 feat(mcc): overnight backtest orchestrator + 1.05M case plan
  9fc90418 docs(mcc): promotion packets, split spec, and Deepak corpus comparison
  d235b07c docs(mcc): reclassification decisions for 18 REVIEW_HUMAN candidates
  ```
- `git status --short` may show 3 untracked-as-modified file diffs in QuantLens lab + `Claude.md` — IGNORE these (lab is git-ignored, `Claude.md` predates session).

## First commands to run

```bash
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
python -m pytest tests/                 # should show 29 passed
python -m mcc_readonly health           # should be overall_ok=true

# Verify audit picked up overnight data
python -c "from mcc_readonly.audit_reader import build_candidate_audit; s = build_candidate_audit()['summary']; print(f'eligible={s.get(\"eligible_for_backtest_rows\")} blocked={s.get(\"blocked_rows\")}')"
# Expected: eligible=128, blocked=65
```

## Pending Work (priority order)

### P1 — Process embedded transcripts in 21 stg files (~30-60 min)

**Background**: User pasted transcripts for stg001-008 + stg082-094 directly into the .md body **without** the `## Transcript` heading. File sizes 90KB-168KB confirm content present. `ingest.py` current heuristic misses these.

**Action**:
1. Read `MTC_COMMAND_CENTER/11_TRIAGE/ingest.py`, find `parse_stg_md()`.
2. Add a heuristic: if file size > 5KB AND `re.findall(r"\d+:\d+", text)` count > 30 AND no `## Transcript` heading present, treat all body text after `Video Url:` (until next `##` heading) as transcript.
3. Verify on stg001 (90KB) first → should detect embedded transcript.
4. Run `python 11_TRIAGE/ingest.py` (dry-run) → expect 15-18 new transcripts.
5. `python 11_TRIAGE/ingest.py --apply`
6. Verify: `python -m mcc_readonly audit | grep transcript` → eligible count should increase.

**Don't touch**: stg files with file_size < 5KB (stg003, stg005) — those don't have transcripts.

### P2 — URL hint dossier for 11 NO_URL candidates (~30 min)

**Background**: 11 candidates have no URL anywhere (9 × `QL_2026-05-01_*` UNKNOWN_URL + ADA/LTC). Previous session started a cross-reference scan (intake titles vs existing Transcrips corpus + source_map titles) but hit `UnicodeEncodeError: cp1254 can't encode '▶'` (the `▶` emoji on Windows stdout).

**Action**:
1. Read previous attempt context (last session message, near end). Reconstruct the Python script.
2. **Fix**: add `import sys; sys.stdout.reconfigure(encoding='utf-8')` at top, OR replace `▶` with `>>`.
3. For each of the 11 candidates, output a dossier: title, speaker hint, intake file path, top-3 transcript filename matches by keyword overlap, top-3 source_map title matches.
4. The 11 candidates are listed in `PROJECT_HANDOFF.md`. Intake files at `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/00_INBOX_REPORTS/QL_2026-05-01_*_intake.md`.
5. Save dossier as `11_TRIAGE/url_hints_dossier_2026-05-31.md`. Commit.

**Some titles are likely direct YouTube video titles** (e.g., "The ONLY Pattern I've Used for 7 Years - Nothing Else (Full Strategy)" — matches existing `Transcrips/The ONLY Pattern I've Used for 7 Years - Nothing Else (Full Strategy).md`). Cross-ref against Transcrips/ filenames is the highest-yield search.

### P3 — Christian Open Range 5% Stop deeper validation (~1 hour)

**Background**: The single strongest finding from the overnight sweep — `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` survives BH-FDR OR DSR≥0.50 in **6 cells** across OP/ETH/NEAR/TRX/BTC with DSR p 0.53-0.65. This is the most credible cross-symbol edge.

**Action**:
1. Read `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/04_PYTHON_PROTOTYPES/QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M_prototype.py` to see current rule.
2. Write `11_TRIAGE/block_bootstrap_christian_or.py`:
   - Use the 6 surviving (sym × TF) cells
   - Block bootstrap with block_size = sqrt(trades) (handle serial correlation)
   - 10,000 resamples per cell
   - Rolling-origin OOS (4-6 folds, expanding window)
3. Output: `11_TRIAGE/christian_or_validation_2026-05-31.md` — per-cell p-values + aggregate metric (6 cells passing block_bootstrap p ≤ 0.10 = strong recommendation to promote to parity).
4. Decision: if ≥ 4/6 cells pass → propose promotion to PineTS parity stage.

### P4 — Wire 19 new candidates into dashboard pipeline (~1-2 hours)

**Background**: 19 new candidates have `producer_spec.json` files under `06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY/QL_*/` but `pipeline_reader.py` doesn't scan them, so they don't appear as dashboard pipeline rows.

**Action**:
1. Read `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`, locate `build_candidate_pipeline()` (~L624, 264 LOC — see audit doc).
2. Find where `06_PROMOTED_TO_PARITY/<id>/producer_spec.json` files are read for the EXISTING 3 candidates (LINK/ADA/LTC).
3. Extend the glob/read to pick up the 19 new candidates. They follow the same schema (have `candidate_id`, `source_url`, `kind`, `direction`).
4. Add a new test case in `tests/test_pipeline_reader.py`.
5. Run `pytest tests/`, then `python -m mcc_readonly serve` and check `/dashboard` Pipeline tab shows 22 promoted (3 existing + 19 new).

### P5 — Fix backtest_reader MEGA matrix metadata (~1 hour)

**Background**: Dashboard backtest tab shows MEGA run as COMPLETED but `symbols`, `timeframes`, `trade_count` fields are empty/None for matrix runs. Reader detects status but doesn't extract matrix aggregate.

**Action**:
1. Read `backtest_reader.py`, find the MEGA / RIGOROUS matrix parser.
2. From `MEGA_walk_forward_results.json`:
   - `symbols_tested` = unique `r['symbol']` across `results[]`
   - `timeframes_tested` = unique `r['timeframe']`
   - `trade_count` = sum of `r.summary.lockbox_oos.num_trades`
3. Add test in `test_backtest_reader.py`.
4. Verify in `/api/snapshot` → `backtest_status.runs[mega].symbols_tested` should be a list.

### P6 (deferred) — Refactor candidates

Per MCC audit (`mcc_audit_2026-05-31.md`):
- `pipeline_reader.build_candidate_pipeline` 264 LOC → break into 5-6 sub-functions
- `audit_reader.py` 1231 LOC procedural → extract `CandidateAuditBuilder` class
- HTTP integration test missing
- Audit reader per-snapshot file scan → TTL memoization

Not urgent. Do after P1-P5.

## Critical gotchas (don't repeat these)

1. **Time estimates from startup overhead are wrong**. Mega runner finished in 11.5 min (I said 5-6h). Focused finished in 72s (I said 3-5 min). Use steady-state hız (1.5-2 jobs/sec measured) for tahmin.

2. **Multiprocessing PermissionError on Windows sandbox**: pass `dangerouslyDisableSandbox: true` to Bash for backtest runs. PermissionError spam in log is non-fatal — workers restart automatically. Real error sign: Traceback + non-zero exit.

3. **Background process cleanup**: killing Python proc'larını won't stop bash loop wrapper. Always `Get-Process` listing after kill to verify nothing left. Loop iterations overwrite output files — give each isolated run its own `OUTPUT_DIR` subdir.

4. **DSR threshold**: p≥0.95 too strict for crypto. Use p≥0.50 for research. Cross-symbol consistency (6 cells at DSR p≈0.55) > single cell at p≥0.95.

5. **mega_walk_forward.py is hardcoded**: no auto-discovery. To add strategies, monkey-patch via `mw.GRIDS.update()` + `mw.build_signals = patched`. See `overnight_v2_runner.py` for pattern.

6. **stg files have unique structure**: `# StgNNN — <candidate_id>\n\nVideo name: ...\nVideo Url: ...` (mandatory). Optional `## Transcript`, `## Alternative Source N`, `## Notes`. User may paste transcripts WITHOUT `## Transcript` heading — heuristic needed.

7. **stg_code_map.json is sacred**: `_stg_code_map.json` persists `candidate_id → Stg###` mapping across runs. Never overwrite; only append.

## Important paths cheatsheet

```
MTC_COMMAND_CENTER/
├── PROJECT_HANDOFF.md                      # read first
├── CURRENT_STATUS.md                       # short status
├── CHANGELOG.md
├── 01_PROMPTS/CLAUDE_CONTINUATION_2026-05-31.md  # this file
├── 08_DASHBOARD_APP/apps/api/mcc_readonly/ # all read-only modules
│   ├── server.py                           # HTTP (read-only enforced)
│   ├── read_model.py                       # snapshot aggregator
│   ├── pipeline_reader.py                  # 946 LOC, needs refactor
│   ├── audit_reader.py                     # 1231 LOC, needs refactor
│   ├── backtest_reader.py                  # MEGA metadata fix needed
│   └── writer.py                           # controlled write gate
├── 08_DASHBOARD_APP/apps/api/tests/        # 29 tests pass
└── 11_TRIAGE/                              # this session's workspace
    ├── README.md
    ├── generate_worklist.py                # xlsx + stg*.md generator
    ├── ingest.py                           # P1: needs transcript heuristic
    ├── extract_urls_from_intakes.py
    ├── analyze_transcripts.py              # heuristic scanner
    ├── sample_for_review.py                # 18 REVIEW_HUMAN sampler
    ├── deep_sample.py                      # per-candidate deep context
    ├── aggregate_overnight_iters.py        # cross-iter robustness
    ├── overnight_orchestrator.py           # spec+prototype materializer
    ├── overnight_v2_runner.py              # monkey-patches mega
    ├── overnight_loop.sh                   # 7.5h wrapper
    ├── focused_validation.py               # narrow grid re-run
    ├── morning_report_2026-05-31.md        # overnight aggregated
    ├── reclassification_decisions_2026-05-30.md
    ├── promotion_packets_2026-05-30.md
    ├── split_packet_2026-05-30.md
    ├── deepak_comparison_2026-05-30.md
    ├── andrew_connell_deep_read_2026-05-30.md
    ├── focused_validation_report_2026-05-31.md
    ├── mcc_audit_2026-05-31.md
    ├── OVERNIGHT_LESSONS_2026-05-31.md     # read this!
    └── strategies/                         # gitignored
        ├── _stg_code_map.json              # SACRED — never overwrite
        └── stg001.md ... stg172.md
```

```
01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/    # gitignored
├── 00_INBOX_REPORTS/
│   ├── Transcrips/                         # canonical transcript home
│   └── *_intake.md                         # intake reports (UNKNOWN_URL hints)
├── 04_PYTHON_PROTOTYPES/                   # 19 new + existing prototypes
├── 06_PROMOTED_TO_PARITY/                  # producer_spec.json files
├── 05_BACKTEST_RESULTS/
│   ├── MEGA_walk_forward_results.json      # overnight result
│   ├── FOCUSED_VALIDATION_2026-05-31/      # focused subdir
│   └── FOCUSED_DSR_RELAXED_2026-05-31/     # (may be empty — script failed)
├── 12_LLM_WIKI/
│   └── manual_backfill/<date>/             # ingest target for new URLs
└── tools/
    ├── mega_walk_forward.py                # the runner
    ├── overnight_v2_runner.py              # extends mega
    ├── overnight_loop.sh                   # bash wrapper
    ├── focused_validation.py
    ├── overnight_runs/                     # gitignored, 19 iter results
    └── aggregate_overnight_iters.py
```

## Workflow templates

### Add a new strategy to the runner (~30 min)

1. Copy a similar strategy block from `mega_walk_forward.py:build_signals` (e.g., `GEN_DONCHIAN_BREAKOUT`).
2. Define a `grid_X()` function returning list-of-dicts.
3. In `overnight_v2_runner.py`, add to `NEW_GRIDS` dict AND `signals_new()` dispatcher.
4. Smoke test: `timeout 90 python overnight_v2_runner.py 2>&1 | grep "elapsed="` (should see progress in 60-90s).
5. Full run: `nohup python overnight_v2_runner.py > run.log 2>&1 &` (use `dangerouslyDisableSandbox: true`).

### Re-run focused validation (~1 min)

```bash
cd 01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/tools
timeout 180 python focused_validation.py  # writes to FOCUSED_VALIDATION_<date>/
```

### Cross-iteration aggregation (~5 sec)

```bash
cd 01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/tools
python aggregate_overnight_iters.py  # writes OVERNIGHT_AGGREGATED_REPORT.md
```

## Final notes

- User is Turkish-speaking; respond in Turkish unless they switch to English.
- User wants **honesty over polish** — admit estimation errors immediately; don't paper over background-process mismanagement.
- User explicitly authorized `dangerouslyDisableSandbox: true` for backtest runs.
- User does NOT want gece boyu notification spam — Monitor sparingly.
- Commit work in small focused commits with `Co-Authored-By: Claude Opus 4.7` trailer.
- The lab directory (`01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/`) is git-ignored; commit only MCC-side artifacts.

When in doubt → read the OVERNIGHT_LESSONS file, then PROJECT_HANDOFF, then act.

# Lane S — QuantLens report scripts: computed-but-unwritten summaries (D16)

Scope: the two computed-but-unwritten-value defects Lane K flagged (findings #4 and #5 in
`11_TRIAGE/OVERNIGHT_LANE_K_NONPROTECTED_STATIC_HUNT_2026-09-07.md`) in
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/generate_morning_report.py` (`strong`, line 34) and
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/heavy_night_report.py` (`passcells`, lines 77/80). Each
was independently re-read in full and judged against a strict rule: fix only if the report
already has an obvious, unfilled slot for the value (a placeholder line, a table missing exactly
that column, or a docstring promising it); otherwise leave the script untouched and write a
proposal. Nothing else in either script was changed.

## `heavy_night_report.py` — FIXED

**The variable.** `passcells` (lines 77 and 80, pre-fix) is a list of MEGA-sweep rows whose
`classification` is `"PASS"` or `"STRONG_PASS"`, computed identically in *both* arms of the
`if mega: / else:` block in section "## 1. Sweep" — the `else` arm sets it to `[]` purely so the
name stays defined. Grep confirmed it is never read again anywhere in the file.

**Why this one is unambiguous.** Section 1 already prints, immediately above the dead
assignment, a strict run of sibling lines in one consistent style — each computes a filtered
collection and immediately reports its `len()`:
```python
L.append(f"- cells: **{len(rows)}** | strategies: {cfg.get('strategy_count')} ...")
L.append(f"- classification: " + ", ".join(f"{k}={v}" for k, v in sorted(cls.items())))
L.append(f"- robust_final: **{robust}** | DSR p≥0.50: **{dsr_ge_50}**")
passcells = [r for r in rows if r.get("classification") in ("PASS", "STRONG_PASS")]
# <- pattern breaks here: no L.append for the value just computed
```
Every other computed-collection-then-report pair in this file (section 6 "Alpha vs Buy&Hold":
`prem`/`dma`/`ranked`; section 2 CPCV: `surv70`/`surv80`) is immediately followed by an
`L.append` using its `len()`. `passcells` is the one exception, and the fact that both branches
of the `if/else` bother to define it (the `else` arm has no other use for an empty list) is
itself strong evidence a report line was meant to follow but was dropped. The combined
PASS+STRONG_PASS count is also genuinely new information — the existing `classification:` line
reports PASS and STRONG_PASS as *separate* keys (e.g. `PASS=1, STRONG_PASS=1`), never their sum.

**Fix applied** (`MTC_COMMAND_CENTER/03_QUANTLENS/tools/heavy_night_report.py`):
```diff
         L.append(f"- robust_final: **{robust}** | DSR p≥0.50: **{dsr_ge_50}**")
         passcells = [r for r in rows if r.get("classification") in ("PASS", "STRONG_PASS")]
+        L.append(f"- pass cells (PASS+STRONG_PASS): **{len(passcells)}**")
     else:
         L.append("- MEGA results: **MISSING**")
         passcells = []
```
One line, inside the existing `if mega:` branch, using the value that was already there. Nothing
else in the function was touched.

**Regression test**: `MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py`
(stdlib + pytest only). Loads `heavy_night_report.py` by path via `importlib`, builds a synthetic
`MEGA_walk_forward_results.json` (3 rows: STRONG_PASS/PASS/FAIL) in `tmp_path`, calls
`heavy_night_report.main([...])` directly (no subprocess, no real run dir), and asserts the
written report contains a "pass cells" line with the count `2`. A second test covers the
MEGA-missing branch (`passcells = []`) to confirm it still runs cleanly with the new line only
appended on the `mega` branch.

RED (test written against the pre-fix file, fix temporarily stashed):
```
MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py::test_pass_cells_count_is_written_to_report FAILED
MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py::test_pass_cells_zero_when_mega_results_missing PASSED
E       assert 'pass cells' in "# heavy-validation tier — morning report ...
1 failed, 1 passed in 0.06s
```

GREEN (fix restored):
```
MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py::test_pass_cells_count_is_written_to_report PASSED
MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py::test_pass_cells_zero_when_mega_results_missing PASSED
2 passed in 0.04s
```
Command (both runs): `PYTHONUTF8=1 <venv>/bin/python -m pytest -p no:cacheprovider MTC_COMMAND_CENTER/03_QUANTLENS/tools/test_heavy_night_report_summary.py -v`

`ruff check --isolated --no-cache --select E9,F821,F811` on both changed/added files: **All
checks passed!** `git diff --check` on the modified script: clean (no whitespace errors).

## `generate_morning_report.py` — PROPOSAL, no change made

**The variable.** `strong` (line 34): `[r for r in passes if r.get("classification") ==
"STRONG_PASS"]`, where `passes` is every result classified `PASS` or `STRONG_PASS`. Grep confirms
`strong` is never referenced again anywhere in the file.

**Why this one is ambiguous — the strict rule is not met.** The obvious candidate slot is the
"## Sınıflandırma Özeti" (Classification Summary) table (lines 136–150), which already prints a
`STRONG_PASS` row with its own count and description:
```python
for k in ["STRONG_PASS","PASS","FAIL", ...]:
    ...
    md.append(f"| {k} | {cls_counts.get(k,0)} | {desc} |")
```
`cls_counts` is built independently, over *all* `results` (not `passes`), counting raw
`classification` values. Because a result's `classification` can only be `STRONG_PASS` if it is
also in `{"PASS","STRONG_PASS"}`, `cls_counts.get("STRONG_PASS", 0)` is mathematically identical
to `len(strong)` — verified by tracing both derivations by hand. **The count `strong` would
produce is already on the page.** Lane K's own proposed diff (`md.append(f"- STRONG_PASS
candidates: **{len(strong)}**")`) would print a second, redundant restatement of a number the
report already shows two sections earlier, and — as Lane K flagged themselves — the proposed
insertion point sits before `md = []` is even created, so it isn't a literally applicable patch.

Two genuinely different things the owner could have meant are indistinguishable from the code
alone:
1. `strong` was meant purely as a scratch/step variable toward `cls_counts`-equivalent output
   that already exists — i.e. it is truly dead and safe to delete, not "unwritten."
2. `strong` was meant to drive a **new, distinct STRONG_PASS detail table** (e.g. one more Tier
   section listing symbol/timeframe/lockbox-return for each STRONG_PASS row, parallel to the
   existing `robust_final` / `bh_full` / `bh_pass` / `nonrobust_pass` Tier tables) — a much
   bigger content decision (columns, sort key, cap on rows, placement among the existing Tier
   1/2/2b/3 sections) that this task's minimal-diff mandate should not guess at.

Per the task's strict rule ("if ambiguous: change nothing... write a precise proposal"), no edit
was made to `generate_morning_report.py` and no test was added for it.

**Proposal for the owner:**
- The variable: `strong` at `03_QUANTLENS/tools/generate_morning_report.py:34` — list of results
  with `classification == "STRONG_PASS"` (a subset of `passes`).
- Where it could be emitted: either (a) delete it as genuinely-dead scratch code (its count
  duplicates the existing classification-summary row and needs no restatement), or (b) if a
  dedicated STRONG_PASS detail table is actually wanted, add a new Tier-style section (own
  heading, column set, and sort key — likely by `lockbox_oos.net_return_pct` like the sibling
  Tier tables) somewhere between "## Sınıflandırma Özeti" and "## Üç Bağımsız Doğrulama Kapısı".
- What the owner must decide: (a) vs (b) above — i.e. whether `STRONG_PASS` needs a
  count-only restatement (redundant, likely not wanted), a full detail table (new design work),
  or nothing (delete the dead variable). This lane made no guess and left the file untouched.

## NEXT ACTION

None required from this lane — the `heavy_night_report.py` fix is complete, tested (RED/GREEN),
lint-clean, and ready to review/merge as-is.

## WAITING FOR OWNER

`generate_morning_report.py`: decide whether the dead `strong` variable at line 34 should be (a)
deleted as redundant scratch code, or (b) turned into a new STRONG_PASS detail table (and if so,
its columns/sort/placement) — see the "PROPOSAL" section above. No script change was made
pending that decision.

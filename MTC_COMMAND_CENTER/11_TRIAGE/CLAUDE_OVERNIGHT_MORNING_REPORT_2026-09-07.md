# Claude Overnight Lane — Morning Report (2026-09-07)

**Recorded:** DRAFT 2026-09-06 22:58 +03 — finalized section at the end states the close time
**Class:** T3 factual report; self-verified; no acceptance, promotion, or live implication
**Branch:** `claude/overnight-autonomous-work-e94x3q` from `origin/master`
`afe52ea89473300e25555325def111cac599bdf1`
**Checkpoint record:** `CLAUDE_OVERNIGHT_CHECKPOINTS_2026-09-06.md` (same directory)
**Executor:** Claude remote Linux container (claude.ai/code). The owner's
`HANDOFF_CLAUDE_P0_20260906_2200/HANDOFF.md`, every `C:/` packet, `pwsh`, the Codex launcher and
the Gemini launcher are on the Windows host and were unreachable; nothing in this report derives
from them.

## 1. Owner decisions needed

None are required for anything this lane did. Eleven findings (D1–D11 in §4); D1–D5 are already repaired on the branch as NONACCEPTED candidates, the rest are dispatch decisions
are batched here; each is a stage-owned repair with a verified patch attached, and none was
applied to the tree.

## 2. Verified facts

| # | Fact | Evidence |
|---|---|---|
| F1 | `master` head `afe52ea` passes the protected `Bridge suite (Python 3.12)` on GitHub (run 76, `33998308281`, SUCCESS) and locally as a non-root user: **1393 passed, exit 0**, 63 s, Python 3.12.3, hash-locked deps (`pip --require-hashes`, exit 0), `compileall` exit 0. | checkpoint 2; `ci_run3` log |
| F2 | The same tree run **as root** fails exactly 3 tests in `tests/test_wal_state_bundle.py` (1390 passed). Cause: SQLite 3.45.1's unix VFS calls `fchown(fd, 0, 0)` on `-wal`/`-shm` when `geteuid()==0` (strace), and `chown` always refreshes `ctime`; `_stable_metadata()` includes `ctime_ns`, so the arrival→before snapshot shows `wal` drift (+4 ms ctime, no content/mtime/size/inode change) and `create` fails closed with `source_changed_during_capture`. | checkpoint 1–2 |
| F3 | F2 has no documented operational path: Linux units run as `User=mtc-bridge`; the Stage E capture runs on the old Windows writer. Failure direction is safe. | `deploy/linux/systemd/*.template`, `deploy/linux/COMMANDS.md` |
| F4 | Pine Defang Guard: `PASS files=21 matches=0 allowlist=0`. | checkpoint 1 |
| F5 | All other executable, non-protected Python suites pass: `mtc_cli` 8, `_deepseek_driver` 20, `tools_v2/observability` 19, `tools_v2/analysis_package` 11, `contracts` 50 (+ `ruff==0.16.4` clean), 25 QuantLens strategy test dirs (all green). Dashboard API: 120 passed, 1 failed (D1). | checkpoint 2 |
| F6 | Not executed by policy: `02_MTC_BACKTEST`, `12_PARITY_PINETS`, any backtest/optimization/server/launcher. | AGENTS.md invariants |
| F7 | Governance/link hygiene: 0 broken links in 66 root/governance/_AI_MEMORY docs and 43 stage-contract files; all 8 stages carry their five files; every stage `HANDOFF.md` ≤ 4 KiB. | checkpoint 1 |
| F8 | `11_TRIAGE/INDEX.md` was 73 files stale (last generated 2026-08-25). Regenerated on this branch with a validated Python port of `generate_index.ps1` (reproduces all 1,374 prior rows and their order byte-for-byte; deterministic across two runs). Rows added only. | commit `93828d9` |
| F9 | Credential-pattern sweep: only labelled fakes in fixtures/tests. EOL: 0 mixed. 120 tracked `.sh` parse except 4 intentional `sec102_r7` malformed fixtures. 2,202/2,203 JSON and 108/115 YAML tracked files parse (exceptions are D3/D4). | checkpoint 2 |
| F10 | Open PRs at start, untouched: #26 (draft), #22, #21, #20 — all last updated July 2026. GitHub reports `mergeable_state: unknown`. Measured locally on the full (unshallowed) history: #26 `feature/two-tier-policy` merge-base `008e065e`, 1 ahead / 1,014 behind, **conflicts**; #22 `feature/exit-aware-gauntlet` merge-base `8721bce0`, 10 ahead / 1,023 behind, merges clean (`git merge-tree`); #21 and #20 merge-base `8721bce0`, 1 ahead / 1,023 behind, **conflicts**. #26 also names the superseded auditor `claude-opus-4-8` (D022 fixed `claude-opus-5`). All predate the 2026-08-23 Map 97 fold; rebase-or-close candidates. (An earlier draft of this row was measured on a shallow clone and wrongly said "no merge base"; corrected here.) | local `git merge-base` / `merge-tree` |
| F11 | Static sweeps: `ast.parse` over all 1,003 tracked `.py` files finds one syntax error (D2 artifact); `ruff --select F821,F811,F823,E9` over every Python tree (protected trees read-only, `--no-cache`) finds product hits D6, D7, D8 below, plus two benign local re-imports in `tests/test_engine_dryrun.py:3798` (F811); `shellcheck 0.11.0 -S warning` on `deploy/linux/{install,package,rollback,verify}.sh` is clean. | checkpoint 3 |

| F12 | Relative Markdown links across 1,971 non-history docs: 7 broken, all legacy references in owner-gated scopes — `02_MTC_BACKTEST/README.md` → `../00_MASTER_TEMPLATE/`, `../20_MODULES_REUSABLE/`; `02_MTC_BACKTEST/parity_suite_350/{OPTIMIZATION_EXECUTION_SUMMARY,SUPERTREND_OPTIMIZATION_GUIDE}.md` → `../../src/modules/signals/supertrend.py#L110/#L147`; `04_SHARED/modules/#00 README_Pine_Module_Pack_v2.md` → `../../.github/copilot-instructions.md`, `../20_MODULES_REUSABLE/LIB_ConfirmationLayer.pine`. T2 doc repairs for those stages; untouched here. | link sweep |
| F13 | Read-only dashboard commands `mcc_readonly {health,read-model,snapshot,parity-status,backtest-status}` and `mtc_cli --help` all run without traceback against this checkout (snapshot: 2.2 MB JSON, exit 0). `mtc_cli audit repo` exits 2 by design of its stale path list (D9). | checkpoint 3 |
## 3. What this lane changed (work branch only; nothing pushed elsewhere, no PR)

After the owner's 23:05 +03 instruction ("authorized for everything to keep the work running",
4–6 lanes until 06:30), non-protected findings were repaired by isolated worker lanes and
integrated by the lead with `cherry-pick -x` after diff inspection and re-testing. Every code
commit is a NONACCEPTED candidate: the exact T0–T2 audits (Codex/Gemini launchers) were
unreachable from this container and remain required before merge.

| Commit | Scope | What | Lead re-verification |
|---|---|---|---|
| `6a25e23a` | dashboard tests (D1, D5) | Path-built expectation; temp-dir fixtures | 121 passed, no stray `C:` dir |
| `5c617b3f` | `11_TRIAGE/overnight_orchestrator.py` + regenerated `03_QUANTLENS/tools/overnight_extended_run.py` (D2) | dedent-safe import join; artifact regenerated (no run) | `py_compile` + ruff E9/F821 clean |
| `91ccbba6` | `01_MTC_PROJECT/tools/extract_parameter_library_seeds.py` + 7 YAML (D3) | warning emitted as `# ` comment | 8/8 YAML parse |
| `151e1700` | `03_QUANTLENS/tools/night_runs/AGGREGATE_night_2026-06-02.{json→md}` (D4) | `git mv`, bytes unchanged | content starts `# OVERNIGHT AGGREGATED REPORT` |
| T3 records | `11_TRIAGE/CLAUDE_OVERNIGHT_*`, lane records, `INDEX.md`, stage `HANDOFF.md` notes, governance `HANDOFF.md` + history rotation | evidence and status | index regenerated deterministically |

Still owner-gated and NOT changed: D7 (`02_MTC_BACKTEST`), D8 (MTC_V2), plus anything Pine,
parity, adapters, schemas. Lanes for D6, D9, D10 and the index tool were in flight at the time of
this draft; the close-out section lists what landed.

## 4. Findings with verified patches (not applied)

Each patch was applied to a scratch copy only. RED/GREEN below means: RED = current tree
behaviour reproduced by execution; GREEN = patched copy passes; mutant = patched assertion still
fails on a deliberately wrong output (discriminating power, per `00_AGENT_PROTOCOLS/TESTS.md`).

### D1 — dashboard test hard-codes a Windows path separator (T1, `08_DASHBOARD_APP`)

RED: `test_pipeline_reader.py::test_discovers_extra_quantlens_jsonl_candidates` fails on Linux
(`'research/batch/…' != 'research\\batch\\…'`). Product code returns native
`str(path.relative_to(root))`, so only the assertion is platform-bound. GREEN: 1 passed with the
patch. Mutant: reader prefixed with `"X/"` → 1 failed with the patch (assertion still bites).

```diff
--- a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_pipeline_reader.py
+++ b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_pipeline_reader.py
@@ -201,7 +201,10 @@
             self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["stages"]["discovered"]["status"], "done")
             self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["stages"]["backtested"]["status"], "na")
             self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["source_url"], "https://www.youtube.com/watch?v=abc123")
-            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["discovery_source"], "research\\batch\\FINAL_LLM_KNOWLEDGE_BASE.jsonl")
+            self.assertEqual(
+                rows["QLR_EXTRA_PULLBACK"]["discovery_source"],
+                str(Path("research") / "batch" / "FINAL_LLM_KNOWLEDGE_BASE.jsonl"),
+            )
             self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["classification"]["kind"], "wiki")
             self.assertIn("QLR_BLOCKED", rows)
             self.assertEqual(rows["QLR_BLOCKED"]["stages"]["backtested"]["status"], "na")
```

### D2 — overnight runner generator emits an unimportable file (T1, `11_TRIAGE`)

RED: importing the real `overnight_orchestrator.py` and calling `write_runner_extension(True)`
into a scratch dir emits a file whose line 1 is `        """Auto-generated…` →
`compile()` raises `SyntaxError: unexpected indent (line 1)`; the committed
`03_QUANTLENS/tools/overnight_extended_run.py` is byte-identical to that output apart from the
timestamp, which is why `compileall` fails on it today. GREEN: with the patch the emitted runner
compiles and carries all 19 `from PYTHON_PROTOTYPES import …` lines. Regenerating the committed
artifact is a separate, execution-gated step (it is a runner for a backtest sweep).

```diff
--- a/MTC_COMMAND_CENTER/11_TRIAGE/overnight_orchestrator.py
+++ b/MTC_COMMAND_CENTER/11_TRIAGE/overnight_orchestrator.py
@@ -565,7 +565,10 @@
     """Emit overnight_extended_run.py at the tools dir that imports all
     new prototypes + delegates to mega_walk_forward's existing infrastructure."""
     runner_path = TOOLS_DIR / "overnight_extended_run.py"
-    imports = "\n".join(
+    # Indent every generated line to the template depth so textwrap.dedent
+    # below can strip the common prefix; a bare multi-line block would leave
+    # the whole runner indented and unimportable (IndentationError).
+    imports = "\n        ".join(
         f"from PYTHON_PROTOTYPES import {c.id}_prototype  # noqa: F401"
         for c in CANDIDATES
     )
```

### D3 — parameter-library YAML files are not parseable (T1, `01_MTC_PROJECT`)

RED: 7 of 8 files under `optimization/parameter_library/**/*.yml` fail `yaml.safe_load`
(`mapping values are not allowed here`, line 4) because line 2 is the bare, unquoted research
warning sentence; the 8th file (`range_filter/range_filter_seed_regions.yml`) already uses the
intended commented form `# Research seeds only; …` and parses. GREEN: prefixing line 2 with `# `
in each of the 7 files makes all of them parse (top keys `regions`, `rejected_or_caution_regions`,
`purpose`…). No tracked consumer parses these files as YAML today (`run_12h_backtesting_session.py`
only writes CSV), so impact is latent. Writer fix: in
`01_MTC_PROJECT/tools/extract_parameter_library_seeds.py` lines 93, 146 and 171 emit
`f"# {RESEARCH_WARNING}"` instead of the bare `RESEARCH_WARNING`; the five hand-written
`*.template.yml` files and the two generated `supertrend_*` files need the same one-line change.

### D4 — Markdown report stored under a `.json` name (T3, `03_QUANTLENS`)

`03_QUANTLENS/tools/night_runs/AGGREGATE_night_2026-06-02.json` (40,534 B) begins with
`# OVERNIGHT AGGREGATED REPORT — cross-iteration…`; `write_overnight_morning_report.py` refers to
the aggregate as `AGGREGATE_night_<id>.md`. Proposed: `git mv` to `.md` (history-preserving), or
delete if it duplicates an existing `.md`. No content change.

### D5 — dashboard test writes a fixture to a fixed absolute path (T1, `08_DASHBOARD_APP`)

`tests/test_audit_reader.py::test_audit_classifies_duplicate_blocked_and_eligible_rows` creates
`Path("C:/TEMP/MTC_COMMAND_CENTER/11_TRIAGE/strategies")` and writes `_stg_code_map.json` there,
then passes `Path("C:/TEMP/MTC_COMMAND_CENTER")` as the root. On Windows that is a real write
outside both the repo and pytest's temp dir; on Linux it created a literal
`08_DASHBOARD_APP/apps/api/C:/TEMP/…` directory inside the checkout during this lane's run
(inspected: one 24 KB generated JSON; removed, never staged). Sibling tests already use
`tempfile.TemporaryDirectory()`; the same pattern fixes this one. Discovered after the dashboard
suite run, so it is reported without a scratch-verified patch.

### D6 — `Any` used without import in the Hyperliquid broker (T1, `IBKR_PAPER_BRIDGE`, latent)

`bridge/broker/hyperliquid.py:1643` annotates a local `rich_rows: dict[str, dict[str, Any]]` but
the module never imports `Any` (ruff F821). With `from __future__ import annotations` (line 7) and
because local-variable annotations are never evaluated at runtime (verified on 3.12.3), there is
no runtime effect today; it becomes a `NameError` only if the annotation is ever evaluated
(e.g. by `typing.get_type_hints`) or the future import is dropped. One-line fix: add `Any` to the
module's `typing` import. Protected-adjacent Bridge scope; owner-gated.

### D7 — Streamlit operator page raises `NameError` on "Generate Run Plan" (T1, `02_MTC_BACKTEST`, protected)

`02_MTC_BACKTEST/app.py:190` inside `show_operator_page()` evaluates `pd.Timestamp.now()` when the
"Generate Run Plan" button is pressed, but `pandas` is imported only locally inside other
functions (lines 308, 391, 661, 682, 830) and never at module scope or in this function
(ruff F821, confirmed by reading the enclosing `def`). Static finding only; the app was not
launched (owner-gated scope, no server execution). One-line fix: `import pandas as pd` at module
scope or at the top of the button branch.

### D8 — MTC_V2 runner references an unimported constant when `debug_mode` is on (T1, `MTC_V2`, protected)

`01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1052` builds `_debug_metadata` with
`EXECUTION_PROFILE_RAW_CLOSE_ONLY`, but the module imports only `SIGNAL_MODE_RANGE_FILTER`,
`SIGNAL_MODE_SUPERTREND`, `resolve_config` from `mtc_v2.core.config` (line 8), where the constant
is defined. The branch runs only when `config["debug_mode"]` is true (default `False`,
`config.py:36`); no tracked test or config enables it, so production numerics are untouched, but
`debug_mode=True` raises `NameError` at the first bar. The portable copy
`handoff/MTC_V2_PORTABLE_HANDOFF/.../runner.py` carries the same line (files otherwise differ at
line 1197). Static finding only; nothing in MTC_V2 was executed. Fix is an import-list addition.

Related lint-only (no runtime effect, annotation strings under `from __future__ import
annotations`): `mtc_v2/core/gates.py:524,569` reference `"datetime"` without a `TYPE_CHECKING`
import; same class as D6.

### D9 — `mtc_cli audit repo` has failed on every `master` since the 2026-08-25 routing fold (T1, `mtc_cli`)

`python -m mtc_cli audit repo` (the D002 agent-native, read-only health command) returns
`[audit repo] FAIL`, exit 2, with `missing: MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
and `missing: …/_AI_MEMORY/NEXT_STEPS.md`. `mtc_cli/commands/audit.py:27-28,97` still requires
those paths, but commit `552a41ec` (2026-08-25, "feat(context): add stage-local routing") moved
both files to `_AI_MEMORY/history/` (255 KB and 344 KB there today), as root `AGENTS.md` records.
The 8 `mtc_cli` tests pass because they use fixtures. Whether the audit should read the history
files, the router files (`AGENTS.md`/`DECISIONS.md`/stage `HANDOFF.md`), or be retired is a
D002-level decision; the command is unusable until one is made.

### D10 — dashboard path examples still point at the frozen legacy checkout (T2, `08_DASHBOARD_APP`)

`00_CONFIG/paths.example.json` and `paths.local.example.json` (10 values) resolve every root to
`C:/LAB/tradingview-lab/…` and the pre-migration `01_MASTER TEMPLATE_V2` layout. Root `AGENTS.md`
declares that checkout frozen and forbids reading it, and `PATHS_RESOLUTION.md` loads the example
first, so `mcc_readonly health` on a machine without `paths.local.json` reports
`mtc_v2_root_reachable: false` against the legacy path (observed here: `overall_ok: false`).
Read-only run; no config was written. Fix is a values-only update to the canonical
`C:/LAB/Tradingview_LAB_CLEAN/…` layout (or relative roots), owner-confirmed.

### D11 — orchestrator default `TOOLS_DIR` still names the legacy layout (T1, `11_TRIAGE`)

Found by lane B while regenerating the runner: `11_TRIAGE/overnight_orchestrator.py` derives
`TOOLS_DIR` from `REPO_ROOT / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB" / "tools"`, a
pre-migration path that does not exist in this checkout (migrated to
`MTC_COMMAND_CENTER/03_QUANTLENS/tools`). Any real `--apply` run would create the legacy tree
instead of writing into QuantLens. Out of D2's scope; queued as a refill lane.

## 5. Suggested Bridge-stage doc note (T2, optional)

`IBKR_PAPER_BRIDGE/TESTS.md`: "On Linux run the suite as a non-root user; as root SQLite
`fchown`s the WAL/SHM on read-only open, which the capture drift guard correctly reports."
The existing "two recorded baseline failures may exist" sentence did not reproduce on Linux
(both named tests pass); it is conditional wording and was left alone.

## 6. Reproduction commands (Linux, from repo root)

```bash
/usr/bin/python3.12 -m venv .venv312 && .venv312/bin/python -m pip install --require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock
PYTHONUTF8=1 .venv312/bin/python -m compileall -q IBKR_PAPER_BRIDGE
PYTHONUTF8=1 .venv312/bin/python -m pytest IBKR_PAPER_BRIDGE/tests -q          # as non-root: 1393 passed
# root-only RED, three WAL tests:
strace -f -e trace=fchown .venv312/bin/python -c 'import sqlite3;sqlite3.connect("file:<db>?mode=ro",uri=True).execute("select name from sqlite_master limit 1")'
python3 MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
```

## 7. Appendix — index generator port used for F8

Cross-platform equivalent of `11_TRIAGE/generate_index.ps1` (row format, dotfile extension
semantics, and .NET word-sort order all validated against the committed index). Kept out of the
tree because adding a tool is not authorized; reproduce from here if needed.

```python
"""Python port of MTC_COMMAND_CENTER/11_TRIAGE/generate_index.ps1 (row generation only)."""
import os, re, sys, subprocess
ROOT = 'MTC_COMMAND_CENTER/11_TRIAGE'
def clean(v, limit):
    if v is None: return ''
    c = re.sub(r'\s+', ' ', v.replace('|', '\\|')).strip()
    return c[:limit-3] + '...' if len(c) > limit else c
def fdate(name):
    m = re.search(r'(20\d{2})[-_](\d{2})[-_](\d{2})', name)
    if m: return f"{m[1]}-{m[2]}-{m[3]}"
    m = re.search(r'(20\d{2})(\d{2})(\d{2})', name)
    if m: return f"{m[1]}-{m[2]}-{m[3]}"
    return '-'
TEXT = {'.md','.txt','.json','.ps1','.py','.sh','.yaml','.yml'}
def row(rel):
    full = os.path.join(ROOT, rel)
    name = os.path.basename(rel)
    stem, ext = os.path.splitext(name)
    if name.startswith('.') and name.count('.') == 1:
        stem, ext = '', name  # .NET GetExtension semantics for dotfiles
    topic = re.sub(r'[_-]+', ' ', stem)
    if not topic.strip(): topic = name
    summary = f"{ext.lstrip('.').upper()} file"
    if ext in TEXT:
        try:
            with open(full, encoding='utf-8-sig', errors='strict') as fh:
                content = fh.read().splitlines()
            heading = next((l for l in content if re.match(r'^#{1,6}\s+\S', l)), None)
            if heading: topic = re.sub(r'^#{1,6}\s+', '', heading)
            body = None
            for l in content:
                v = l.strip()
                if v and not re.match(r'^(#|>|\||```|---$)', v):
                    body = l; break
            if body: summary = body
        except Exception as e:
            summary = f"Unreadable during index generation: {type(e).__name__}"
    return '| `' + clean(rel,180) + '` | ' + fdate(name) + ' | ' + clean(topic,120) + ' | ' + clean(summary,180) + ' |'
# --- driver ---
def net(x):
    t = x.replace('-', '')
    return ([(0, c) if c in '_/\\.' else (1, c) if c.isdigit() else (2, c.lower()) for c in t], x)
files = [f for f in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'], cwd=ROOT, text=True).split('\n') if f and f != 'INDEX.md']
files.sort(key=net)
lines = ['# 11_TRIAGE index', '', '> Generated search index. Do not read triage history by default; grep this file, then open at most the relevant record.', '', '| Path | Date | Topic | One-line summary |', '|---|---|---|---|']
lines += [row(f) for f in files]
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'INDEX.md')
with open(out, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(lines) + '\n')
print(f"Indexed {len(files)} files into {out}")
```

## 8. Close-out

- **Heartbeat checkpoints:** see the checkpoint record; the last entry states the close time.
- **NEXT ACTION (owner):** triage the open findings to their stage owners and route the branch through the normal audit/PR/CI gate; optionally merge this branch's two
  T3 triage records through the normal PR/CI route.
- **WAITING FOR OWNER:** Nothing for this lane's authorized work.

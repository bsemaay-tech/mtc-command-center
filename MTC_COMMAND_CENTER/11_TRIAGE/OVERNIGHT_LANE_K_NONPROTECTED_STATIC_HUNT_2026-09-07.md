# Lane K — non-protected static defect hunt (read-only)

Scope: `mtc_cli`, `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly`,
`MTC_COMMAND_CENTER/03_QUANTLENS/tools`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/tools`,
`_deepseek_driver`, `MTC_COMMAND_CENTER/tools`, `MTC_COMMAND_CENTER/contracts/mtc_contracts`.
`tests/` dirs and all owner-gated trees (`02_MTC_BACKTEST`, `07_ADAPTERS`, `06_SCHEMAS`,
`12_PARITY_PINETS`, `01_MTC_PROJECT/00_PYTHON/mtc_v2`) excluded.

## Summary table

| Tree | Rule | Count | Class |
|---|---|---|---|
| 03_QUANTLENS/tools | F401 unused import | 46 | c |
| 03_QUANTLENS/tools | F541 f-string, no placeholder | 15 | c |
| 03_QUANTLENS/tools | F841 unused local | 18 | 14c / 4a |
| 03_QUANTLENS/tools | B007 unused loop var | 10 | c |
| 03_QUANTLENS/tools | B905 zip without strict | 5 | c |
| 03_QUANTLENS/tools | PLW0603 global | 5 | c |
| 03_QUANTLENS/tools | B023 late-bound closure | 2 | c (false positive) |
| 03_QUANTLENS/tools | B904 no `raise…from` | 1 | c |
| 03_QUANTLENS/tools | B028 no stacklevel | 1 | c |
| 01_MTC_PROJECT/tools | F401 unused import | 10 | c |
| 01_MTC_PROJECT/tools | B905 zip without strict | 5 | c |
| 01_MTC_PROJECT/tools | F541 f-string, no placeholder | 6 | c |
| 01_MTC_PROJECT/tools | B007 unused loop var | 1 | c |
| 08_DASHBOARD_APP/mcc_readonly | F401 unused import | 1 | c |
| 08_DASHBOARD_APP/mcc_readonly | F841 unused local | 1 | b |
| 08_DASHBOARD_APP/mcc_readonly | B007 unused loop var | 2 | c |
| 08_DASHBOARD_APP/mcc_readonly | B905 zip without strict | 2 | b |
| _deepseek_driver | B033 duplicate set item | 1 | **a** |
| mtc_cli | F401 unused import | 2 | c |
| MTC_COMMAND_CENTER/tools | — | 0 | — |
| contracts/mtc_contracts | — | 0 | — |
| **Total ruff hits** | | **134** | 5a / 3b / 126c |

Manual review (rules outside `--select`, see below) surfaces 3 more findings not counted in
the 134 above: 1 more (a) (hard-coded Windows fallback path) and 2 more (b) (dead-code
ternary already flagged as F841 above is finding #6; BOM-handling inconsistency and broad
`except: pass` are new). Grand total flagged for owner attention: **6 (a) + 5 (b)** (3 of the
b's are ruff-level, 2 are manual-only); everything else is (c) style/false-positive noise
typical of long-lived research scripts.

## Ranked (a) — real runtime/logic defects

**1. `_deepseek_driver/ds_agent.py:56-62` — duplicate entry in the write-guard denylist (security-relevant)**
```python
_BANNED_ATTRS = {"write", "writelines", "write_text", "write_bytes", "unlink", "rename",
                 "replace", "rmtree", "remove", "removedirs", "mkdir", "makedirs",
                 "rmdir", "truncate", "chmod", "system", "popen", "spawn", "fdopen",
                 "remove", "move", "copy", "copyfile", "copytree", "symlink_to"}
```
`"remove"` appears twice (line 60 and 62). A Python `set` literal silently drops the
duplicate, so this line effectively contributes nothing — strongly suggesting an intended
attribute name (e.g. `"delete"`, `"rmdir"` variant, `"kill"`) was dropped by a copy/paste
and never added. `check_run_python()` uses this set as the sole AST-level guard against a
sandboxed model calling dangerous file/process attributes; a missing entry narrows the
guard's coverage (the code's own comment calls it "cooperative … not adversarial", but it
should still list every attribute it claims to block).
Proposed diff (needs owner to confirm the intended name):
```diff
-                 "rmdir", "truncate", "chmod", "system", "popen", "spawn", "fdopen",
-                 "remove", "move", "copy", "copyfile", "copytree", "symlink_to"}
+                 "rmdir", "truncate", "chmod", "system", "popen", "spawn", "fdopen",
+                 "move", "copy", "copyfile", "copytree", "symlink_to"}  # TODO: confirm
+                 # whether a second attribute (distinct from "remove" above) was intended here
```

**2. `_deepseek_driver/ds_agent.py:240` — hard-coded Windows-only fallback path**
```python
report_path = Path(task.get("report_out") or (Path(r"C:\tmp") / f"ds_{slug}_report.md"))
```
`task["report_out"]` is caller-supplied and not validated anywhere else in the file. If a
task omits it, the fallback `Path(r"C:\tmp")` is used — on POSIX (this session's own
platform is Linux) a backslash is not a separator, so this resolves to a literal relative
path segment `C:\tmp` under the current working directory, not a temp directory; the parent
almost certainly doesn't exist and `_dump()`'s `write_text()` raises `FileNotFoundError`,
silently caught and only logged as `[warn] could not write report file: …` — the run
"succeeds" with the transcript/report lost. The `# avoid cp1254 crash` comment two lines up
confirms this driver already had to work around a Windows Turkish-codepage bug, i.e. it
already runs in mixed environments.
Proposed diff:
```diff
-    report_path = Path(task.get("report_out") or (Path(r"C:\tmp") / f"ds_{slug}_report.md"))
+    report_path = Path(task.get("report_out") or (Path(tempfile.gettempdir()) / f"ds_{slug}_report.md"))
```
(with `import tempfile` added to the top-level imports).

**3. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_all_gate_evidence.py:126-127` — dead `symbol`/`timeframe` locals in the Gate1 evidence builder**
```python
    symbol = ev.get("symbol", "")
    timeframe = ev.get("timeframe", "")
    metrics = ev.get("metrics", {})
```
The function's own docstring says the intake block is "evidenced by … symbol/timeframe …",
but `symbol`/`timeframe` are computed and then never read anywhere in `build_intake()`
(confirmed by full-function read) — no `symbol_defined`/`timeframe_defined` field is ever
populated from them. This is a real gap between documented and implemented behavior in a
gate-evidence generator that feeds promotion decisions: the intake block silently omits a
check the docstring promises.
Proposed diff (illustrative; exact field name needs owner sign-off since this is gate logic):
```diff
+    intake_block["symbol_timeframe_present"] = (
+        OK(True, source_eval, f"symbol={symbol!r} timeframe={timeframe!r}")
+        if symbol and timeframe
+        else NOT_COMPUTED(None, "symbol/timeframe missing from evidence row")
+    )
```

**4. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/generate_morning_report.py:34` — computed `STRONG_PASS` list never reported**
```python
    passes = [r for r in results if r.get("classification") in {"PASS","STRONG_PASS"}]
    strong = [r for r in passes if r.get("classification") == "STRONG_PASS"]
    robust_final = [r for r in passes if r.get("robust_final")]
```
`strong` is built and never referenced again in the file (confirmed by `grep -n strong`
returning only this line). The morning report silently drops a STRONG_PASS breakdown that
the code was clearly written to surface.
Proposed diff:
```diff
     bh_full.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
+    md.append(f"- STRONG_PASS candidates: **{len(strong)}**")
```
(exact insertion point/format left to the report's owner — this only demonstrates that the
value is usable).

**5. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/heavy_night_report.py:77,80` — computed `passcells` never reported**
```python
        passcells = [r for r in rows if r.get("classification") in ("PASS", "STRONG_PASS")]
    else:
        L.append("- MEGA results: **MISSING**")
        passcells = []
```
Both branches assign `passcells`; the name never appears again in the file. Same class of
bug as #4 — a night-report generator that computes a pass-cell count and drops it.
Proposed diff:
```diff
         passcells = [r for r in rows if r.get("classification") in ("PASS", "STRONG_PASS")]
+        L.append(f"- pass cells: **{len(passcells)}**")
```

## Ranked (b) — latent

**6. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py:187`**
```python
    run_id = run_dir.name if run_dir != path.parent.parent else run_dir.name
    base = {
        "run_id": run_dir.name if run_dir.name else "(root)",
```
Both arms of the ternary evaluate to `run_dir.name` — the comparison is a no-op, and the
result is discarded anyway (F841); `base["run_id"]` is computed independently two lines
later with different (truthiness) logic. Reads as a refactor leftover where the author
meant to special-case `run_dir == path.parent.parent` but wired the wrong expression into
each branch. Currently harmless only because the value is unused — a future edit that starts
reading `run_id` would inherit dead logic.

**7. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py:180-189` — unchecked `zip` in a CSV repair path**
```python
def _candidate_csv_row(header: list[str], fields: list[str]) -> dict[str, Any]:
    if len(fields) <= len(header):
        return dict(zip(header, fields))
    repaired = fields[:12]
    repaired.append(",".join(field.strip() for field in fields[12:-4]))
    repaired.extend(fields[-4:])
    return dict(zip(header, repaired))
```
This is the one `B905` hit that is *not* provably length-safe (every other `zip()` in scope
pairs `keys`/`itertools.product(*values)` or two views of the same DataFrame column, which
are safe by construction — see Commands section). Here `fields` is externally-sourced CSV
data reconstructed with a fixed `[:12]` / `[12:-4]` / `[-4:]` split; if a malformed row
doesn't reduce to exactly `len(header)` columns after the repair, `zip` silently truncates
and the dashboard shows a row missing trailing (or shifted) columns with no warning. Given
the function's own comment ("historical rows contain unquoted commas") this repair path is
exercised on real, messy data.
Minimal robustness diff:
```diff
     repaired.extend(fields[-4:])
-    return dict(zip(header, repaired))
+    if len(repaired) != len(header):
+        return dict(zip(header, fields))  # give up on repair, fall back to raw truncation
+    return dict(zip(header, repaired))
```

**8. Inconsistent UTF-8-BOM handling across `mcc_readonly` readers**
`heartbeat_reader.py:127` and `mtc_v2_reader.py:253` explicitly read with
`encoding="utf-8-sig"`, and the former even comments why: `# some heartbeat writers
(PowerShell-launched) emit a UTF-8 BOM`. But `pipeline_reader.py` (5 sites),
`audit_reader.py` (5), `optimization_reader.py` (4) and `backtest_reader.py` (1) read
adjacent pipeline/audit artifact JSON with plain `encoding="utf-8"` — a BOM-prefixed file
from the same PowerShell-launched producer family the comment warns about would raise
`json.decoder.JSONDecodeError: Expecting value: line 1 column 1` in those readers instead
of being read. No crash observed in this static pass (no BOM files were sampled), so this
is latent, not currently firing — same-package precedent for `-sig` already exists, so
picking it up in the other readers is a same-pattern fix, not new design.

**9. Broad `except Exception: pass` (17 sites across `mcc_readonly` + `03_QUANTLENS/tools` + `_deepseek_driver`)**
See the full list under "Manual review results" below. Each is individually defensible
(best-effort optional-data reads), but every one silently discards the *type* of failure —
a permissions error, a schema change, and a truly-missing file are all indistinguishable to
the caller. Flagged as a class, not line-by-line diffed, since fixing needs per-site
judgement on what should actually be logged.

## Manual review results

- **Mutable default arguments** — none found. `--select B` (covers B006) also confirms
  this: zero `B006` hits in the ruff run, corroborating the regex sweep.
- **Bare `except:`** — none found (`grep -rnE "^\s*except\s*:\s*$"` returned nothing).
- **`except Exception: pass`** (broad-catch silencer) — 17 sites:
  `mcc_readonly/optimization_reader.py:363`, `liveops_reader.py:137`,
  `pipeline_reader.py:467`, `heartbeat_reader.py:68`, `03_QUANTLENS/tools/{generate_producer_specs.py:389 (JSONDecodeError only), score_all_gates.py:139, score_gate2.py:571, score_gate3.py:589, score_gate1b.py:326, score_gate1.py:588, heavy_night_report.py:92, vbt_enrichment.py:292, markitdown_ingest.py:59 (narrow, FileNotFoundError/SubprocessError)}`,
  `01_MTC_PROJECT/tools/{run_worker_scaling_benchmark.py:125 (JSONDecodeError only), extract_parameter_library_seeds.py:72 (narrow)}`,
  `_deepseek_driver/ds_agent.py:233`, `mcc_readonly/writer.py:225 (FileNotFoundError only)`.
  Most narrow ones (`JSONDecodeError`, `FileNotFoundError`, `SubprocessError`) are fine;
  the `except Exception: pass` sites are the ones worth a follow-up pass — logged under
  finding #9.
- **`open()` without `encoding=` on text files, checked against the repo's confirmed
  Turkish-text files** — searched for Turkish-specific characters (`çşğüöıİÇŞĞÜÖ`) across
  all `.py` files in scope; found genuine Turkish report strings in
  `03_QUANTLENS/tools/generate_morning_report.py` (e.g. `"GERÇEK NİHAİ"`, `"varlığı"`) and
  22 other files. Every one of those files reads/writes via `Path.read_text(encoding=
  "utf-8")` / `.write_text(..., encoding="utf-8")` — **no defect found** on the
  Turkish-text-bearing files; classify (c). The only bare `open()` calls without
  `encoding=` in scope are on plain-ASCII financial data (`alpaca_download_dataset.py:122,
  172, 237, 252`, `alpaca_download_us_equities_10m.py:175, 206`) — low-risk portability nit,
  classified (b) since these inherit the platform default encoding rather than pinning
  UTF-8 explicitly, inconsistent with the rest of the codebase's careful `encoding=`
  discipline.
- **`os.path`/`Path` joins assuming Windows separators or hard-coded `C:/` roots outside
  config** — one real hit, `_deepseek_driver/ds_agent.py:240` (finding #2 above). The other
  `C:\...` literals found by `grep` in scope (`ds_agent.py:204`, the `SYSTEM` prompt string)
  are prose describing the *target* repo path to the LLM, not a filesystem operation — no
  defect. (Other `C:\LAB\...` hits from the broader grep — `apply_migration.py`,
  `WP_P0_11_GATE_*` — are outside the seven scoped trees and out of this lane's remit.)
- **`json.load`/`json.loads` on files that may carry a UTF-8 BOM** — 01_MTC_PROJECT/tools
  is already careful: 13 sites explicitly use `encoding="utf-8-sig"`. The gap is in
  `mcc_readonly` (finding #8) and in `03_QUANTLENS/tools/mega_walk_forward.py:1234` /
  `rigorous_walk_forward_parallel.py:391`, both of which do
  `json.load(open(BUNDLE_MANIFEST, encoding="utf-8"))` (no `-sig`, and the file handle is
  also never explicitly closed — CPython refcounting closes it in practice, low severity,
  noted but not diffed).

## Commands executed

```
export PYTHONUTF8=1
ruff check --isolated --no-cache --output-format concise \
  --select F,B,PLE,PLW0602,PLW0603,S102,S307,S602,S605 --exclude tests \
  mtc_cli \
  MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly \
  MTC_COMMAND_CENTER/03_QUANTLENS/tools \
  MTC_COMMAND_CENTER/01_MTC_PROJECT/tools \
  _deepseek_driver \
  MTC_COMMAND_CENTER/tools \
  MTC_COMMAND_CENTER/contracts/mtc_contracts
```
Trimmed output (full 134-line output kept in scratch, not committed):
```
...
MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:1234:12: PLW0603 Using the global statement to update `_MANIFEST` is discouraged
...
_deepseek_driver/ds_agent.py:62:18: B033 [*] Sets should not contain duplicate item "remove"
mtc_cli/commands/audit.py:16:8: F401 [*] `time` imported but unused
mtc_cli/contract.py:13:8: F401 [*] `sys` imported but unused
Found 134 errors.
[*] 83 fixable with the `--fix` option (36 hidden fixes can be enabled with the `--unsafe-fixes` option).
```
Ancillary greps used for manual review (ripgrep semantics, run from repo root):
```
grep -rnE "def [a-zA-Z_0-9]+\([^)]*=\s*(\[\]|\{\})" <dirs> --include=*.py   # mutable defaults: 0 hits
grep -rnE "^\s*except\s*:\s*$" <dirs> --include=*.py                        # bare except: 0 hits
grep -rnA1 -E "^\s*except\b" <dirs> --include=*.py | grep -B1 "pass$"       # except-pass: 17 hits
grep -rlP "[çşğüöıİÇŞĞÜÖ]" <dirs> --include=*.py                            # Turkish-text files: 23 hits
grep -rn "utf-8-sig" <dirs> --include=*.py                                  # BOM-safe readers: 21 hits (01_MTC_PROJECT/tools + 2 mcc_readonly files)
grep -rn "open(" <dirs> --include=*.py | grep -v encoding= | grep -vE "['\"][rwax]?b['\"]"  # non-binary open() w/o encoding: 6 real hits
```

No source file changed; nothing executed beyond ruff/python static checks.

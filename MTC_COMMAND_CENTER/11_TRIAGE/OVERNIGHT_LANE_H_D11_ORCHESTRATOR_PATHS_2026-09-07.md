# Lane H — orchestrator path constants (D11)

**Defect:** T1 script defect. `MTC_COMMAND_CENTER/11_TRIAGE/overnight_orchestrator.py`
derived its QuantLens paths from the pre-migration layout
(`01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/...`), which does not exist in this checkout. A
real `--apply` run would have created a legacy tree instead of writing into the migrated
`MTC_COMMAND_CENTER/03_QUANTLENS/` layout.

**Scope:** path constants only, in `overnight_orchestrator.py`, lines ~22-28. No other
file touched. No orchestrator run, backtest or launcher executed.

## Before / after constants

```python
# BEFORE
THIS = Path(__file__).resolve()
MCC_ROOT = THIS.parent.parent
REPO_ROOT = MCC_ROOT.parent
QLAB_ROOT = REPO_ROOT / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"
PROTO_DIR = QLAB_ROOT / "04_PYTHON_PROTOTYPES"
PROMOTED_DIR = QLAB_ROOT / "06_PROMOTED_TO_PARITY"
TOOLS_DIR = QLAB_ROOT / "tools"

# AFTER
THIS = Path(__file__).resolve()
MCC_ROOT = THIS.parent.parent
REPO_ROOT = MCC_ROOT.parent
# Post-migration layout (see repo-root .gitignore header): 06_QUANTLENS_LAB/ ->
# MTC_COMMAND_CENTER/03_QUANTLENS/. QuantLens now lives directly under MCC_ROOT,
# not nested under 01_MTC_PROJECT.
QLAB_ROOT = MCC_ROOT / "03_QUANTLENS"
PROTO_DIR = QLAB_ROOT / "04_PYTHON_PROTOTYPES"
PROMOTED_DIR = QLAB_ROOT / "06_PROMOTED_TO_PARITY"
TOOLS_DIR = QLAB_ROOT / "tools"
```

`THIS`, `MCC_ROOT`, and `REPO_ROOT` derivation logic is unchanged. `PROTO_DIR`,
`PROMOTED_DIR`, and `TOOLS_DIR` keep the same relative sub-paths under `QLAB_ROOT`;
only `QLAB_ROOT` itself moved off the legacy two-level `REPO_ROOT / "01_MASTER
TEMPLATE_V2" / "06_QUANTLENS_LAB"` construction onto `MCC_ROOT / "03_QUANTLENS"`,
matching the repo-root `.gitignore` migration mapping
(`06_QUANTLENS_LAB/ -> MTC_COMMAND_CENTER/03_QUANTLENS/`; QuantLens is not nested
under `01_MTC_PROJECT`).

## Rationale for using `MCC_ROOT` instead of `REPO_ROOT / "MTC_COMMAND_CENTER"`

`MCC_ROOT` (`THIS.parent.parent`) already resolves to the `MTC_COMMAND_CENTER`
directory in this checkout, so `MCC_ROOT / "03_QUANTLENS"` is equivalent to
`REPO_ROOT / "MTC_COMMAND_CENTER" / "03_QUANTLENS"` without re-hardcoding the
`MTC_COMMAND_CENTER` segment a second time. `REPO_ROOT` derivation itself is
untouched.

## Existence checks (this worktree)

| Path | Exists |
|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS` | yes |
| `MTC_COMMAND_CENTER/03_QUANTLENS/04_PYTHON_PROTOTYPES` (new `PROTO_DIR`) | yes |
| `MTC_COMMAND_CENTER/03_QUANTLENS/06_PROMOTED_TO_PARITY` (new `PROMOTED_DIR`) | yes |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools` (new `TOOLS_DIR`) | yes |
| `01_MASTER TEMPLATE_V2` (legacy root) | missing (confirms pre-fix defect) |

## Legacy path embedded in generated text — checked, left alone

`write_runner_extension()` emits `overnight_extended_run.py` into `TOOLS_DIR`
containing:

```python
ROOT = Path(__file__).resolve().parent.parent / "04_PYTHON_PROTOTYPES"
```

This is relative to the emitted file's own location (`TOOLS_DIR`), i.e.
`TOOLS_DIR.parent / "04_PYTHON_PROTOTYPES"` = `QLAB_ROOT / "04_PYTHON_PROTOTYPES"`
= `MTC_COMMAND_CENTER/03_QUANTLENS/04_PYTHON_PROTOTYPES`, which **exists** in this
checkout (see table above). Per task instructions this relative logic was left
unchanged since the target directory it resolves to is present.

## Commands + output

RED (before fix, on the pre-edit module):

```
$ python -c "import overnight_orchestrator as m; print(m.TOOLS_DIR, m.TOOLS_DIR.exists())"
QLAB_ROOT = .../01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB
TOOLS_DIR = .../01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/tools
TOOLS_DIR.exists() = False
PROTO_DIR = .../01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/04_PYTHON_PROTOTYPES False
PROMOTED_DIR = .../01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY False
```

GREEN (after fix):

```
$ python -c "import overnight_orchestrator as m; print(m.TOOLS_DIR, m.TOOLS_DIR.exists())"
QLAB_ROOT = .../MTC_COMMAND_CENTER/03_QUANTLENS
TOOLS_DIR = .../MTC_COMMAND_CENTER/03_QUANTLENS/tools
TOOLS_DIR.exists() = True
PROTO_DIR = .../MTC_COMMAND_CENTER/03_QUANTLENS/04_PYTHON_PROTOTYPES True
PROMOTED_DIR = .../MTC_COMMAND_CENTER/03_QUANTLENS/06_PROMOTED_TO_PARITY True
MATCHES EXPECTED: True
```

Compile check:

```
$ python -m py_compile MTC_COMMAND_CENTER/11_TRIAGE/overnight_orchestrator.py
PY_COMPILE_OK
```

Lint check:

```
$ ruff check --isolated --no-cache --select E9,F821 MTC_COMMAND_CENTER/11_TRIAGE/overnight_orchestrator.py
All checks passed!
```

Dry-emit test (module's `TOOLS_DIR` monkey-patched to a scratch dir under
`/tmp/claude-0/.../scratchpad/dryemit_tools`, `write_runner_extension(True)` called
directly — confirms lane B's dedent fix (`5c617b3f`) still holds):

```
$ python -c "m.TOOLS_DIR = Path('.../scratchpad/dryemit_tools'); p = m.write_runner_extension(True); print(p, p.exists())"
EMITTED: .../scratchpad/dryemit_tools/overnight_extended_run.py True
"""Auto-generated overnight runner — extends mega_walk_forward.py
with 19 additional strategy entries from the 2026-05-30 triage.
Generated: 2026-09-06T21:09:39
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent / "04_PYTHON_PROTOTYPES"
...

$ python -m py_compile .../scratchpad/dryemit_tools/overnight_extended_run.py
EMITTED_PY_COMPILE_OK
```

`git diff --check` on the changed file: clean (no whitespace errors).

Scratch emit directory removed after the check; nothing written outside the
allowed paths.

No orchestrator run, backtest or launcher executed.

## Deviations

None. Diff is limited to the six-line comment + one-line constant change described
above; `REPO_ROOT`/`MCC_ROOT` derivation, `PROTO_DIR`/`PROMOTED_DIR`/`TOOLS_DIR`
relative sub-paths, and the emitted-runner template body are unchanged.

## NEXT ACTION

None required for D11 — path constants now resolve to the migrated QuantLens
layout and are verified to exist. A future `--apply` run should be exercised in a
disposable environment before any real backtest launch, per governance's
no-execution-without-approval rule.

## WAITING FOR OWNER

Nothing.

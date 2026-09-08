# Lane G — cross-platform 11_TRIAGE index generator

Adds `MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py`, a self-contained, stdlib-only,
cross-platform port of `generate_index.ps1` (PowerShell, unavailable on Linux/CI), plus
`test_generate_index.py` (pytest + stdlib). No changes to `generate_index.ps1` or `INDEX.md`.

## Usage

```bash
# Regenerate the index in place (default root: script's own directory,
# default output: <root>/INDEX.md):
python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py

# Point at a different tree / output path:
python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --root <dir> --output <path>

# CI / pre-commit style verification only — writes nothing, exits 1 on any
# difference (existing INDEX.md missing, or added/removed/changed rows):
python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --check
```

Row format, header lines, UTF-8-no-BOM/LF/single-trailing-newline output, cell cleaning (pipe
escaping, whitespace collapse, 180/120/180 truncation with `...`), date regexes, the text-extension
set, heading/first-body-line extraction, and the `Unreadable during index generation: <ExceptionType>`
fallback are all preserved exactly from `generate_index.ps1`.

Two intentional differences (documented in the module docstring):

1. **File set** — indexes `git ls-files --cached --others --exclude-standard` run inside `--root`
   (tracked + untracked-but-not-ignored files) instead of every file `Get-ChildItem -Recurse` finds
   on disk, so generated/ignored/scratch files never enter the index and the set is deterministic.
2. **Sort order** — `Sort-Object FullName` is a culture-aware .NET string comparison with no exact
   Python equivalent, so this tool sorts with an explicit key function, `dotnet_word_sort_key`,
   reproducing the same relative order (see its docstring): `-` is ignored entirely; among the rest,
   `_ / \ .` sort before digits, digits before letters (case-insensitive); ties break on the raw path.

Also carries the same .NET `Path.GetExtension` semantics for pure-leading-dot dotfiles as the
validated reference port: `.gitignore` -> stem `""`, extension `.gitignore` -> topic `.gitignore`,
summary `GITIGNORE file` (the opposite of Python's default `os.path.splitext`, which would treat it
as extension-less).

## Validation against the real index

Run in this worktree, `MTC_COMMAND_CENTER/11_TRIAGE/` as the (default) root, against the committed
`INDEX.md`:

```
$ python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --check
MISMATCH: .../MTC_COMMAND_CENTER/11_TRIAGE/INDEX.md differs from the regenerated index.
added=75 removed=0 changed=0
```

`removed=0` and `changed=0` — every one of the 1375 existing rows reproduces byte-for-byte. The 75
"added" rows are exactly:

- `generate_index.py` and `test_generate_index.py` — this lane's two new files.
- 73 pre-existing files under `11_TRIAGE/` that were never indexed (added by earlier
  lanes/campaign work after the last `INDEX.md` regeneration), e.g.
  `AI_PROVIDER_ROUTING_RECOMMENDATION_2026-08-29.md`, `HOURS_AND_COST_2026-08-28_NIGHT2.md`,
  the `GC_REFERENT_TEST_FIX_2026-08-25/`, `WAL_CAPTURE_FIX_2026-08-25/`,
  `WP_P0_09_CAPABILITY_TABLE_2026-08-25/`, `WP_P0_10_GOLDEN_SUITE_2026-08-25/` (including its
  `fixtures/` subtree), `WP_P0_11_GATE_2026-08-28/` (including `evidence/` and `profiles/`
  subtrees), `WP_P0_23_PINE_DEFANG_2026-08-25/`, and `WP_P0_27_CI_HOME_2026-08-25/` directories.

No existing row differs and nothing was removed, so the port's row generation is validated
byte-for-byte against the live, PowerShell-produced `INDEX.md`.

### Determinism (write mode run twice)

```
$ python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --output <scratch>/laneG_index_1.md
Indexed 1450 files into <scratch>/laneG_index_1.md
$ python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --output <scratch>/laneG_index_2.md
Indexed 1450 files into <scratch>/laneG_index_2.md
$ cmp <scratch>/laneG_index_1.md <scratch>/laneG_index_2.md
(no output — files identical)
```

### Diff of a scratch-output run against the committed `INDEX.md`

```
$ diff MTC_COMMAND_CENTER/11_TRIAGE/INDEX.md <scratch>/laneG_index_1.md
76 lines added, 0 lines removed
```

76 rather than 75 because this run's `--output` pointed outside `--root`, so the real, git-tracked
`INDEX.md` file itself is no longer excluded from its own regeneration and appears as one more
indexed row (`| \`INDEX.md\` | - | 11_TRIAGE index | MD file |`) — expected, not a defect: the tool
only excludes whatever the *current* `--output` path resolves to. The other 75 added lines are the
same set reported by `--check` above. Zero rows were removed or changed in either comparison.

## Test evidence

```
$ python -m pytest MTC_COMMAND_CENTER/11_TRIAGE/test_generate_index.py -q -p no:cacheprovider
31 passed
```

Covers dotfile `.NET GetExtension` semantics, the `dotnet_word_sort_key` ordering rule on a crafted
list (expected order derived by hand from the documented rule and checked against the implementation),
cell truncation/escaping, heading/first-body-line extraction (including the unreadable-file fallback
and the non-text-extension path), and a `--check` round-trip against a temporary `git init` repo
(never the real repository) covering: missing index, clean round-trip, drift detection after a
tracked file changes, write-mode determinism, output-file self-exclusion, and UTF-8/no-BOM/LF/
single-trailing-newline framing.

```
$ ruff check --isolated --no-cache MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py MTC_COMMAND_CENTER/11_TRIAGE/test_generate_index.py
All checks passed!
```

`git diff --check`: clean (no whitespace errors).

## Deviations from the reference ports

None in row-generation logic — `build_row`/`clean_cell`/`file_date`/`dotnet_word_sort_key` reproduce
`gen_index_port.py`/`regen_index.py` exactly (validated byte-for-byte above). Additions beyond the
reference scripts, all within the T1 tool scope: `--root`/`--output`/`--check` CLI, the write-mode
`Indexed N files into <path>` message, the added/removed/changed `--check` report, and the pytest
suite.

## NEXT ACTION

Lead regenerates `INDEX.md` with this tool (`python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py`)
whenever ready to fold in the 73 currently-unindexed files; this lane does not touch `INDEX.md`
itself. A CI `--check` step is a proposal only — not wired into any workflow by this change.

## WAITING FOR OWNER

Nothing.

# WP-P0-01 repository inventory

Inventory timestamp: 2026-08-24T19:56:34+03:00
Canonical fixed point: `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`
Dirty checkout (strictly read-only): `C:\LAB\Tradingview_LAB_CLEAN`
Audit tier: **T2**

## Census

- Tracked fixed-point files: **8120** (the dated plan snapshot of 8,031 was not reused).
- Fresh untracked dirty-checkout artefacts: **305**.
- Human porcelain output rows, including modified tracked files: **313**.
- Refs classified: **317** (174 evidence-bearing, 143 not evidence-bearing, 0 unknown).

## Exact enumeration commands

- Tracked: `git -C "C:\WPP001_20260824" ls-tree -r -l -z fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`
- Required human-readable untracked/status listing: `git -C "C:\LAB\Tradingview_LAB_CLEAN" status --porcelain=v1 --untracked-files=all`
- Machine-safe untracked parsing: `git -C "C:\LAB\Tradingview_LAB_CLEAN" status --porcelain=v1 -z --untracked-files=all`
- Last-commit dates: `git -C "C:\WPP001_20260824" log --pretty=tformat:%x1e%cI%x00 --name-only -z --no-renames fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`
- Branch refs: `git -C "C:\LAB\Tradingview_LAB_CLEAN" for-each-ref --sort=refname --format=... refs/heads refs/remotes`

The NUL-delimited form is authoritative for machine counts because porcelain paths may be quoted and PowerShell's `?` is a wildcard. Only records whose two-byte status is exactly `??` become untracked-inventory rows.

## Referenced-by methodology

`referenced_by_count` is the number of distinct tracked text files that contain either the target's case-folded full repository-relative path (forward- or backslash form) or, for basenames of at least four characters, the case-folded basename. The builder creates one Aho-Corasick automaton and scans each eligible tracked text file once; self-references are excluded. Files over 4 MiB, known binary extensions, and files with a NUL in the first 8 KiB are not scanned as reference sources.

Known behaviour: basename matching intentionally finds short-form references but over-counts when many tracked files share a basename (for example `README.md`). Path spelling variants beyond slash direction and case folding under-count. Generated references inside skipped binary/large files are not counted. The metric is therefore a bounded navigation-risk signal, not an exact dependency graph.

## Classification semantics

- `CANONICAL`: tracked at the fixed point with no explicit legacy/evidence marker; a working inventory label, not a cleanup or canonicalization decision.
- `LEGACY`: path explicitly identifies itself as archive/legacy/retired/old/backup.
- `DUPLICATE`: untracked bytes normalize through Git attributes to a blob tracked at the fixed point; the canonical twin is mandatory and recorded.
- `EVIDENCE`: audit, research, parity, run, decision, or verification-bearing path.
- `UNKNOWN`: owner/purpose/classification cannot safely be established; this is explicit classification, not an empty/unclassified row.

Tier A contains every tracked/untracked path except paths captured by the explicit Tier-B rules. Tier B is limited to local agent-skill installation state, caches/bytecode, and OS/editor temporaries. No evidence-marker path is intentionally placed in Tier B.

## Reproduction

From the lane worktree root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_01_INVENTORY_2026-08-24\build_inventory.py
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_01_INVENTORY_2026-08-24\qa_inventory.py
```

Both scripts are standard-library-only and make no network, host, deployment, broker, Docker, WSL, backtest, Pine, parity-logic, MTC, Bridge-runtime, or schema mutation.

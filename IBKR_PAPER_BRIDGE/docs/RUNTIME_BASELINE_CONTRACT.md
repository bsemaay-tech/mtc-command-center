# Runtime Baseline Contract (TS-P0-001)

Contract for `tools/check_runtime_baseline.py` — the read-only repository/runtime
baseline manifest and drift checker.

- **Schema version:** `1.0.0` (manifest field `schema_version`; bump on any field
  addition/removal/semantic change).
- **Governing ADRs:** ADR-0019 (research/validation/paper/live separation),
  ADR-0027 (supply-chain & secret security). Supports ADR-0018/0025 evidence.
- **Hash-scope owner:** Barış — the scope below is proposed and pending his
  confirmation (TS-P0-001 human-review requirement).

## Purpose

Make it mechanically obvious whether the source tree being reviewed matches the
isolated runtime (`C:\P2RT`) and an expected release commit — without touching
either tree, the network, the scheduler, the database, or any process.

## Invocation

```
python IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py \
    --repo-root <path> --runtime-root <path> --expected-commit <7-40 hex> \
    [--timestamp YYYY-MM-DDTHH:MM:SSZ] [--json-out <file>] [--md-out <file>]
```

- Both roots must be given explicitly; there are no defaults and no discovery.
- The JSON manifest is always printed to stdout; `--json-out` / `--md-out`
  additionally write files at those explicit paths (never inside either root).
- `--timestamp` sets the single declared-variable field for reproducible
  evidence; when omitted the current UTC time is used.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Exact clean match: repo HEAD == runtime HEAD, both match `--expected-commit`, both worktrees clean, source-tree hash and config hash equal, no runtime scope entry missing. |
| 2 | Drift: any commit mismatch, dirty repo, dirty runtime, hash mismatch, missing runtime root (`verdict: RUNTIME_MISSING`), or runtime missing a scope entry. |
| 3 | Invalid evidence input: missing/non-git `--repo-root`, repo root missing a required scope entry, malformed git output (non-40-hex HEAD, git failure/timeout), invalid `--expected-commit`, invalid `--timestamp`, bad CLI arguments. |

Failure mode is safe: exit 3 prints a single `check_runtime_baseline: ...` line
to stderr — no traceback, no partial manifest.

## Manifest fields (JSON, sorted keys, LF, 2-space indent)

| Field | Meaning |
| --- | --- |
| `schema_version` | This contract's version, `1.0.0`. |
| `tool` | Constant `check_runtime_baseline`. |
| `generated_at_utc` | Declared timestamp — the ONLY field allowed to vary between otherwise-identical runs. |
| `repo` / `runtime` | `root` (resolved posix path), `commit` (40-hex HEAD), `dirty` (porcelain non-empty), `dirty_entries` (sorted porcelain lines); `runtime` adds `present`. |
| `expected.commit` | The `--expected-commit` input (lowercased). |
| `hash_scope` | Echo of the source scope, config scope, excluded dir names, and secret denylist patterns in force. |
| `hashes.repo` / `hashes.runtime` | `files` (relpath → SHA-256, sorted), `excluded` (denylisted files by path+reason, never read), `missing_scope_entries`, `source_tree_hash`, `config_hash`. |
| `comparison` | Booleans: `repo_commit_matches_expected`, `runtime_commit_matches_expected`, `commits_equal`, `source_tree_hash_equal`, `config_hash_equal`, `repo_clean`, `runtime_clean`. |
| `drift_reasons` | Sorted stable strings (below); empty on MATCH. |
| `verdict` | `MATCH` \| `DRIFT` \| `RUNTIME_MISSING`. |
| `exit_code` | The exit code the process returns. |

Drift reason strings: `repo_commit_mismatch_expected`,
`runtime_commit_mismatch_expected`, `repo_runtime_commit_mismatch`,
`source_tree_hash_mismatch`, `config_hash_mismatch`, `repo_dirty`,
`runtime_dirty`, `runtime_missing`, `runtime_scope_entry_missing:<rel>`.

## Hash scope — what is hashed and why

All hashes are SHA-256. File hashes normalize CRLF to LF for text files
(files with no NUL byte in the first 8KB) before hashing; binary-looking files
are hashed raw. Rationale: the repo and runtime worktrees are checked out under
different git line-ending smudge behavior — git reports both clean and
identical while raw bytes differ only in line endings (observed on the real
`C:\TSP0` vs `C:\P2RT` pair). The hash comparison therefore matches git's own
clean-filter equality; a line-ending-only difference is not drift. Aggregate
hashes are SHA-256 over the sorted sequence of `<relpath>\n<filehash>\n` lines.

**Source scope** (`source_tree_hash`):

| Entry | Why |
| --- | --- |
| `IBKR_PAPER_BRIDGE/bridge/**` | The entire operational bridge package — engine, risk, orders, broker, api, store, settings. Any behavior difference between reviewed source and runtime lives here. |
| `IBKR_PAPER_BRIDGE/requirements.txt` | Dependency declaration; a runtime with different pins is a different system. |
| `IBKR_PAPER_BRIDGE/tools/run_bridge_p2.ps1` | The deployment/launch wrapper actually used by the P2RT scheduled task; a modified wrapper changes what runs. |

**Config scope** (`config_hash`):

| Entry | Why |
| --- | --- |
| `IBKR_PAPER_BRIDGE/config/**` | `bridge.yaml` + strategy YAMLs — operational thresholds and strategy parameters; config drift is release drift even at an identical commit. |

**Deliberately NOT hashed:** `tests/`, `docs/`, other `tools/` scripts (do not
affect runtime behavior); `data/`, `*.db`, logs (runtime-local mutable state);
anything outside `IBKR_PAPER_BRIDGE/` (out of bridge scope). Git commit + dirty
flags already cover whole-repo identity; the hash scope exists to pinpoint
*which* operational content drifted.

**Excluded directory names** (never traversed): `.git`, `__pycache__`,
`.pytest_cache`.

## Secret safety

Files whose basename matches the denylist are **never opened and never
hashed** — they appear in `excluded` by path + reason only:

- `.env`, `.env.*`, `*.env`, `*.env.*` (any case)
- `secret` / `secrets` with optional suffixes, plus `*.secret` / `*.secrets`
- `key` with any optional extension (including `key.txt`)
- `*.key`, `*.pem`, `*.p12`, `*.pfx`
- `*.db`, `*.sqlite`, `*.sqlite3`, `*.log`

The tool reads no environment secrets and emits no file contents anywhere in
JSON, Markdown, stdout, or stderr. `tests/test_runtime_baseline.py::test_secret_safe_output`
proves a planted fake secret is neither read, hashed, nor leaked.

## Determinism

- File lists and all maps are sorted; JSON uses `sort_keys=True`, 2-space
  indent, LF newlines, UTF-8.
- Two runs over identical trees with the same `--timestamp` produce
  byte-identical JSON and Markdown
  (`test_deterministic_file_ordering`, `test_byte_stable_json_and_md_outputs`).

## Non-action guarantees (default operation)

No HTTP, no exchange call, no Task Scheduler access, no database access, no
process control, no writes inside either root (`test_no_mutation`). Git usage is
limited to read-only `rev-parse HEAD` and `status --porcelain` with a 60s
timeout.

# Release Evidence Contract (TS-P0-002)

> **DRAFT — pending Barış approval.** The card requires owner approval of this
> contract before it is binding. Tooling and tests exist; the contract is a
> proposal until Barış signs off.

Contract for `tools/release_evidence.py` — the release/rollback evidence
manifest tool. Builds on the TS-P0-001 hashing primitives
(`tools/check_runtime_baseline.py`, see `RUNTIME_BASELINE_CONTRACT.md`);
hash scope, line-ending normalization, and secret denylist are inherited
from that contract, not redefined here.

- **Schema version:** `1.0.0` (manifest field `schema_version`).
- **Governing ADRs:** ADR-0019, ADR-0027; supports ADR-0029 promotion-gate
  evidence.

## Purpose

Give every deploy a mechanical identity: what exactly was released (commit +
content hashes + dependency pin + DB schema), what the runtime actually holds,
and which commit is the pre-approved rollback target — so a later session can
verify or roll back without archaeology. **The tool never deploys and never
checks anything out.**

## Subcommands

```
python IBKR_PAPER_BRIDGE/tools/release_evidence.py create \
    --repo-root <path> --runtime-root <path> \
    --release-commit <40 hex> --rollback-commit <40 hex> \
    [--timestamp YYYY-MM-DDTHH:MM:SSZ] --out <manifest.json>

python IBKR_PAPER_BRIDGE/tools/release_evidence.py validate \
    --manifest <manifest.json> --repo-root <path> --runtime-root <path>
```

`create` rules:

- `--release-commit` MUST equal the repo root's current HEAD — evidence is
  created from the checked-out release, never synthesized for some other
  commit (violation → exit 3).
- `--rollback-commit` MUST exist in the repository and differ from the
  release commit (violation → exit 3).
- Output is deterministic: two `create` runs over identical trees with the
  same `--timestamp` are byte-identical.

`validate` checks, in order:

1. Required fields all present and structurally typed before any live-state
   dereference (`missing_field:<name>` / `invalid_type:<name>` failures).
   `hashes` must be an object and every required hash value must be a string.
2. `schema_version` equals the supported version
   (`unsupported_schema_version:<v>` — old manifests are rejected, not
   silently reinterpreted).
3. Integrity: SHA-256 over the canonical manifest payload (sorted keys,
   compact separators, `integrity_sha256` field excluded) must equal the
   recorded `integrity_sha256` (`integrity_hash_mismatch` — tamper
   detection).
4. Live comparison (only when 1–3 pass): rollback commit still known to the
   repo; repo HEAD equals the recorded release commit; repo clean; source
   tree/config/lock/schema hashes recomputed and equal; runtime present with
   recorded runtime hashes (`*_mismatch`, `repo_head_not_release_commit`,
   `repo_dirty`, `rollback_commit_unknown:<sha>`, `runtime_missing`).

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | `create`: manifest written. `validate`: VALID — every check passed. |
| 2 | `validate`: INVALID — one or more failures (tamper, missing/wrong-type field, old version, unknown rollback, drift). |
| 3 | Invalid evidence input: bad roots, malformed git output, non-hex commits, corrupt/absent manifest file, bad CLI arguments. Single stderr line, no traceback. |

## Manifest fields

| Field | Meaning |
| --- | --- |
| `schema_version` | `1.0.0`. |
| `tool` | Constant `release_evidence`. |
| `generated_at_utc` | Declared timestamp; the only run-variable field. |
| `repo_root` / `runtime_root` | Resolved posix paths the evidence was built from. |
| `release_commit` | 40-hex commit actually deployed (equals repo HEAD at create time). |
| `rollback_commit` | 40-hex pre-approved rollback target, verified to exist. |
| `hashes.source_tree_hash` | Aggregate hash of the bridge source scope (TS-P0-001 scope) in the repo. |
| `hashes.config_hash` | Aggregate hash of the config scope in the repo. |
| `hashes.lock_hash` | Hash of `IBKR_PAPER_BRIDGE/requirements.txt` — the dependency pin set. No separate lockfile exists today; when TS-P1-011 introduces one, this field moves to it with a schema-version bump. |
| `hashes.schema_hash` | Hash of `IBKR_PAPER_BRIDGE/bridge/store/db.py` — the module that defines the persisted SQLite schema. Proxy until a dedicated migration/schema file exists (TS-P2-006); documented limitation. |
| `hashes.runtime_source_tree_hash` / `runtime_config_hash` | Same aggregates computed over the runtime root at create time. |
| `integrity_sha256` | Self-integrity hash (step 3 above). |

## Proposed artifact layout (no deploy performed by this task)

```
IBKR_PAPER_BRIDGE/docs/releases/<release_commit_short>/
    release_manifest.json      # create output
    validate_report.json       # validate output at deploy + at each audit
```

Layout is a proposal; the deploy procedure that would populate it stays a
separate, Barış-gated action (ADR-0029 promotion gates).

## Non-action guarantees

Same as TS-P0-001: offline, read-only toward both roots, no HTTP/exchange/
scheduler/database/process action, git usage limited to read-only
`rev-parse`, `status --porcelain`, `cat-file -t`.

# Codex TS-P0 BLOCK repair report — 2026-07-19

- Builder/orchestrator: Codex GPT-5
- Worktree: `C:\TSP0`
- Branch: `feature/ts-p0-baseline`
- HEAD: `7777273fc49317cb5572b3399d8daa17c92a2251`
- Status: **THREE BLOCK FINDINGS REPAIRED LOCALLY — INDEPENDENT RE-AUDIT REQUIRED**
- Commit/push/PR/deploy: **none**

## Scope

Exactly nine TSP0 files are modified:

1. `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py`
2. `IBKR_PAPER_BRIDGE/tests/test_runtime_baseline.py`
3. `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md`
4. `IBKR_PAPER_BRIDGE/tools/release_evidence.py`
5. `IBKR_PAPER_BRIDGE/tests/test_release_evidence.py`
6. `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md`
7. `IBKR_PAPER_BRIDGE/bridge/engine/window.py`
8. `IBKR_PAPER_BRIDGE/tests/test_window_state.py`
9. `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md`

No `engine.py`, `routes.py`, config, schema, strategy, Pine, parity, adapter,
runtime, or protected-scope file changed.

## Repairs

### A — secret filename denial

The basename policy now excludes and never opens/hashes:

- `.env`, `.env.*`, `*.env`, `*.env.*`
- `secret`/`secrets` with suffixes and `*.secret`/`*.secrets` variants
- `key` with any optional extension, including `key.txt`
- the pre-existing key/certificate/database/log extensions

The spy/no-leak regression covers `.env`, `secrets.key`, `prod.env`,
`my.secrets`, and `key.txt`. Independent direct probes also verified
`.env.prod`, `prod.env.local`, `my.secrets.local`, and `key` are denied while
`environment.py`, `secretary.py`, `monkey.txt`, `hockey.txt`, and
`prod.environment` remain in normal scope.

### B — release manifest structural validation

`release_evidence._validate_manifest` now checks all required top-level string
fields, the `hashes` container, and each required hash value before any live
dereference. Correctly re-signed wrong-shape manifests return structured
`INVALID`, exit 2, with `invalid_type:<field>` and no traceback.

Regression coverage includes subprocess-level `"hashes": []`, a wrong-type
`release_commit`, and a wrong-type nested `hashes.config_hash`.

### C — monitoring-window fail-closed metadata

`window_status` now distinguishes absent meta from malformed non-empty meta.
Malformed values for each of the four persisted window timestamp keys return
DOWN with `error=invalid_meta:<exact-key>`. Future-dated liveness returns DOWN
with `error=future_liveness`; `compute_window_state` also rejects negative age.
The exact 300-second boundary remains RUNNING, preserving the documented rule.

## TDD and verification evidence

Pre-fix RED after adding the B/C regressions:

```text
6 failed, 37 passed
```

Failures included the wrong-type release commit, all four invalid-meta cases,
and future liveness. The earlier Codex audit already supplied RED evidence for
the secret-name gap; the delegated helper applied the A test and code together
before its stalled run was terminated.

Post-fix evidence, all with `PYTHONUTF8=1`, Python 3.14.2:

| Command/probe | Result |
| --- | --- |
| Three focused test files | **54 passed** in 23.08s |
| Root CWD full suite | **218 passed**, 1 pre-existing warning, exit 0 |
| Bridge CWD full suite | **218 passed**, 1 pre-existing warning, exit 0 |
| Five secret edge names | all denied (`true`) |
| Re-signed `hashes=[]` subprocess | exit 2, `invalid_type:hashes`, no traceback |
| Four malformed window meta keys | all DOWN with exact `invalid_meta:<key>` |
| Future liveness | DOWN with `future_liveness` |
| `git diff --check` | pass (only line-ending conversion notices) |

## Real-pair integration and no-mutation proof

The read-only comparison against `C:\P2RT` exited 2. Because this repair is
intentionally uncommitted, the exact reasons are:

```text
repo_commit_mismatch_expected
repo_dirty
repo_runtime_commit_mismatch
source_tree_hash_mismatch
```

`runtime_commit_matches_expected=true`, `runtime_dirty=false`,
`config_hash_equal=true`, and `source_tree_hash_equal=false`. The source
mismatch remains correct: TS-P0-003 plus this window repair are not deployed to
P2RT. Do not weaken the hash scope to hide it.

P2RT before and after:

```text
008e065e8e0ffa68f46134da6698d58f91ef2dcb
porcelain empty
```

## Delegation record

Repo-mandated Cline was attempted first but failed with hub close code 1006 and
wrote nothing. `_deepseek_driver` fallback partially wrote the A repair and the
start of B, then stalled. Its orphan process was identified by exact command
line and stopped. Codex reviewed the partial diff, removed duplicate tests,
completed the repair, and independently reran all verification above.

## Remaining gates

This build report is not an independent PASS. Next action is the fresh-reviewer
prompt `TSP0_BLOCK_REPAIR_REAUDIT_PROMPT_2026-07-19.md`.

After a non-BLOCK re-audit, remaining TS-P0 closeout items are:

1. N3: append the final-HEAD three-reason integration correction to the old
   Fable handoff.
2. N4: clean the three residual present-tense “Proposed status” ADR sentences.
3. N5: document the in-scope symlink digest-oracle limitation.
4. Barış decisions: hash scope, DRAFT release contract, PROPOSED reset policy.
5. Push/PR only after a separate explicit owner gate.

## Safety confirmation

- New commit: **NO**.
- Push/PR/merge/deploy: **NO**.
- P2RT write/checkout/restart/stop: **NO**.
- Scheduler/task/runtime-DB/ARM/DISARM/KILL action: **NO**.
- Threshold/strategy/Pine/parity/schema/config change: **NO**.
- Network/exchange action: **NO** (delegated model API calls only; product code
  and tests remained offline).


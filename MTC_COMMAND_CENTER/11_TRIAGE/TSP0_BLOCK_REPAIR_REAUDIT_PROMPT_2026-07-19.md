# PROMPT — TS-P0 BLOCK repair independent re-audit

Use this in a fresh reviewer session. To satisfy the repo's cross-model Gate 5,
prefer Grok 4 or another capable model that was not Codex or DeepSeek, because
Codex orchestrated the repair and DeepSeek partially edited it. If this is run
by Codex, label the result **same-model verification**, not strict cross-model
independence.

## Objective

Independently audit the uncommitted nine-file repair of the three BLOCK
findings in `C:\TSP0`. Trust neither the Codex repair report nor prior audit
claims until reproduced. Issue PASS / PASS-WITH-NITS / BLOCK. Do not repair
findings in the same session.

## Read first

1. `C:\TSP0\AGENTS.md`
2. `C:\TSP0\MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. Main-worktree evidence, as claims only:
   - `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP0_AUDIT_2026-07-19.md`
   - `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0_AUDIT_VERIFICATION_2026-07-19.md`
   - `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`

## Expected target facts — verify

- Worktree: `C:\TSP0`
- Branch: `feature/ts-p0-baseline`
- HEAD remains `7777273fc49317cb5572b3399d8daa17c92a2251`
- Exactly nine uncommitted modified files:
  - `tools/check_runtime_baseline.py`
  - `tests/test_runtime_baseline.py`
  - `docs/RUNTIME_BASELINE_CONTRACT.md`
  - `tools/release_evidence.py`
  - `tests/test_release_evidence.py`
  - `docs/RELEASE_EVIDENCE_CONTRACT.md`
  - `bridge/engine/window.py`
  - `tests/test_window_state.py`
  - `docs/21_WINDOW_STATE_CONTRACT.md`
- `C:\P2RT` remains detached, clean, and read-only at `008e065e`.

If HEAD or file scope differs, stop and report before executing tests.

## Hard boundaries

- Read-only audit of TSP0 source: do not edit, restore, reset, stash, commit,
  stage, push, open a PR, merge, or deploy.
- P2RT is strictly read-only: no checkout, process control, scheduler/task/DB,
  ARM/DISARM/KILL, config, threshold, or status-changing action.
- No dependency installs and no protected-scope edits.
- Tests and temp fixture repositories only; no exchange/network calls.

## Mandatory scope and code review

1. Run `git diff --check`, `git diff --stat`, `git diff --name-status`, and
   inspect the entire nine-file diff.
2. Confirm no `engine.py`, `routes.py`, schema, config, strategy, Pine, parity,
   or adapter change.
3. Check contracts exactly match implementation and tests.
4. Look for over-broad secret patterns, structural-validation bypasses, and
   alternate malformed/future timestamp encodings.

## Mandatory tests

Set `PYTHONUTF8=1`; record raw exits and exact counts.

```powershell
cd C:\TSP0
python -m pytest IBKR_PAPER_BRIDGE/tests/test_runtime_baseline.py IBKR_PAPER_BRIDGE/tests/test_release_evidence.py IBKR_PAPER_BRIDGE/tests/test_window_state.py -q
# expect 54 passed

python -m pytest IBKR_PAPER_BRIDGE/tests -q
# expect 218 passed

cd C:\TSP0\IBKR_PAPER_BRIDGE
python -m pytest tests -q
# expect 218 passed
```

## Mandatory adversarial probes

### A — denylist

- Spy `_hash_file`; plant sentinel content in `.env`, `secrets.key`,
  `prod.env`, `prod.env.local`, `my.secrets`, `my.secrets.local`, `key`, and
  `key.txt`. Every file must be excluded, never opened, and the sentinel must
  appear nowhere in stdout/stderr/JSON/Markdown.
- Near misses `environment.py`, `secretary.py`, `monkey.txt`, `hockey.txt`,
  and `prod.environment` must remain normal hashed files.
- Confirm release evidence inherits the same policy.

### B — release manifest shapes

- Create a valid manifest, then correctly re-sign each mutation:
  `hashes=[]`, `hashes=null`, `hashes.config_hash=[]`,
  `release_commit=[]`, `rollback_commit={}`, and
  `integrity_sha256=[]`.
- Every structurally invalid JSON object must produce structured INVALID,
  exit 2, an exact `invalid_type:<field>` failure, and no traceback.
- Re-run the prior re-sign attack: change `config_hash` to another string and
  recompute integrity. Integrity must pass, but live comparison must still
  fail with `config_hash_mismatch`.

### C — window state

- With ARMED + valid start + fresh liveness, set each of
  `window_started_ts`, `window_last_alive_ts`, `window_interrupted_ts`, and
  `window_reset_ts` to: garbage string, integer, list, and timezone-valid
  string. Malformed forms must be DOWN with exact `invalid_meta:<key>`;
  timezone-valid forms must parse consistently.
- Liveness one microsecond and one day in the future must be DOWN with
  `future_liveness`.
- Exact 300s remains RUNNING; 300.001s is DOWN.
- Store exception remains DOWN/store_unreadable; re-arm remains sticky
  INTERRUPTED until reset; engine-less no_store remains DOWN.

## Real-pair no-mutation check

Capture P2RT HEAD and porcelain before/after, then run:

```powershell
cd C:\TSP0
python IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py --repo-root C:/TSP0 --runtime-root C:/P2RT --expected-commit 008e065e
```

If the repair is still uncommitted, expect exit 2 with exactly:

- `repo_commit_mismatch_expected`
- `repo_dirty`
- `repo_runtime_commit_mismatch`
- `source_tree_hash_mismatch`

If an owner has committed the exact repair before this audit, `repo_dirty`
must disappear; do not treat that single expected difference as failure.
Runtime commit must still match expected, runtime dirty must be false, config
hash equal true, source hash equal false.

## Output

Write
`MTC_COMMAND_CENTER\11_TRIAGE\TSP0_BLOCK_REPAIR_REAUDIT_2026-07-19.md`
in the main worktree and update `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and
`ACTIVE_FILES.md` only after the verdict. TSP0 stays untouched.

For each finding include severity, file:line, exact reproduction, expected vs
actual, and required repair. BLOCK requires a reproducible violation. End with
the safety block and P2RT before/after proof.

After a non-BLOCK verdict, list—but do not execute in the audit session—the
remaining closeout sequence: N3 integration correction, N4 ADR wording, N5
symlink limitation, three Barış contract/policy decisions, then separately
approved commit/push/PR.


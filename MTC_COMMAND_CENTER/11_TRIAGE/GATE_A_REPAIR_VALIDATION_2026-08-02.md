# GATE A — REPAIR AND END-TO-END VALIDATION (2026-08-02)

Repairs defects 1, 2 and 5 from `GATE_A_RECON_DEFECT_LIST_2026-08-02.md` and validates them on the
staging host. **Not merged.** Branch `codex/gate-a-build-determinism` @ `a1dd5b46`, based on
`origin/master` `637307e8`.

Implementer: Codex `gpt-5.6-sol`. Lead audit and all Git operations: `claude-opus-5`.

> **This is a repair validation, not a Gate A run.** It uses a *new* release SHA built from the fix
> branch, not the accepted WP-I candidate. Gate A must still re-run from A-0 against a properly
> rebuilt candidate. What this establishes is that the repair is correct and sufficient for A-2.

## 1. The change — two files, 3 hunks

**`deploy/linux/package.sh`**

```bash
-git -C "${REPO}" archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"
+git -c core.autocrlf=false -c core.eol=lf -C "${REPO}" \
+  archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"
```

plus a post-export assertion that fails the build if any CR byte survives in a file that must be LF
on Linux (everything under `deploy/linux/`, plus `*.sh` anywhere in the payload).

Per-invocation `-c` is deliberate: the builder's repository and global configuration are never
modified as a side effect.

**`deploy/linux/lib/common.sh:98`**

```bash
-offenders="$(find "$root" -perm /222 -print -quit 2>/dev/null || true)"
+offenders="$(find "$root" \( -type f -o -type d \) -perm /222 -print -quit 2>/dev/null || true)"
```

`.gitattributes` was deliberately **not** touched — its correct scope interacts with the unresolved
owner decision on defect 4.

## 2. Lead audit of the implementation

| Check | Result |
|---|---|
| Shebang | `#!/usr/bin/env bash` — process substitution valid, so `die` inside the loop really exits the script |
| `bash -n` | both files clean |
| `set -Eeuo pipefail` | present; `grep -q` as an `if` condition is exempt from `set -e` |
| `$?` inside `else` | verified empirically `= 1` — it does capture the condition's status |
| `grep -U` | detects CR, returns 1 on clean files |

## 3. Evidence

### 3.1 The build is now deterministic

```
git archive (repo default, core.autocrlf=true)   install.sh -> 20,342 bytes   [before the fix]
fixed package.sh                                 install.sh -> 19,908 bytes   = the blob size exactly
```

Rebuilt a second time with `core.autocrlf` forced to `input` via `GIT_CONFIG_*`:

```
payload 1 manifest : d25d4464b0644c42aab2e07df3f98a917618b2b47eedcbf1305257104b40f820
payload 2 manifest : d25d4464b0644c42aab2e07df3f98a917618b2b47eedcbf1305257104b40f820
                     IDENTICAL
```

The same `RELEASE_SHA` now yields byte-identical output regardless of the builder's line-ending
configuration. That is the property defect 5 was about.

Payload file sizes now equal their committed blob sizes exactly:

```
install.sh          blob 19908  payload 19908   diff 0
lib/common.sh       blob  8178  payload  8178   diff 0
ledger_schema.json  blob   867  payload   867   diff 0   <- the value EVIDENCE_LEDGER.jsonl records
```

### 3.2 The new guard can actually fail — proved, not assumed

A check that cannot fail is not evidence, so the assertion was falsified deliberately. A temporary
commit carrying a genuine CRLF blob (stored with a `-text` attribute so the CR survives `git add`,
and written to the worktree so the earlier dirty-worktree guard was satisfied and could not mask the
result):

```
blob CR bytes : 2
worktree clean: 0 entries
[mtc-bridge] FATAL: archive contains CR byte in LF-required file:
             IBKR_PAPER_BRIDGE/deploy/linux/_crlf_probe.sh
build exit=1
```

The probe commit was then removed; `HEAD` restored to `a1dd5b46` with 0 dirty entries.

*(First attempt at this test died at the earlier "worktree is dirty" guard and therefore proved
nothing — recorded because that is exactly the kind of vacuous pass this programme keeps paying for.)*

### 3.3 The fixed payload installs on Ubuntu — first attempt, no host edits

Host cleaned of the reconnaissance install first (release, venv, unit, env, state, log dirs, service
user all removed). Payload transferred as a single tar and verified after transfer:

```
RELEASE_SHA : a1dd5b467b12421f632bf3d8462a7244b39b2287
manifest    : d25d4464…  == expected          files: 7,059
install.sh CR bytes: 0    sha256sum -c over the whole manifest: rc=0
```

`install.sh` then completed unaided:

```
verify_lock: PASS: lock; packages=56
verify_lock: PASS: lock+installed; packages=56
PASS  immutable tree carries no write bit (releases/a1dd5b46…)
PASS  immutable tree carries no write bit (venvs/a1dd5b46…)      <- defect 2 fixed
PASS  ufw active, default-deny inbound, SSH-only
PASS  entrypoint binds 127.0.0.1:8790 only
unit sha256=dcd8cb52… state=masked
NOT started, NOT enabled, NO secret provisioned, NO firewall change.
EXIT=0
```

`verify.sh` returned **VERIFY PASS**, exit 0 — installed, masked, unstarted, unarmed.

**No file on the host was edited to make any of this work.** That was A-2's FAIL condition, and it is
now satisfied.

### 3.4 Test results

```
tests/test_linux_deployment.py
   broken payload : 4 failed, 30 passed
   fixed payload  : 34 passed, 0 failed
```

All four failures cleared — including `test_canonical_ledger_and_all_three_row_fixtures_validate`,
which the programme has carried as an accepted "pre-existing failure". It was never a defect; it was
this build bug.

```
full Bridge suite on the fixed payload:  25 failed, 1281 passed
```

This matches the prediction recorded before the run (26 minus the ledger failure). The remaining 25
are **not** addressed by this repair and are correctly out of its scope:

- ~21 `test_wal_state_bundle.py` — defect 3b, the Stage E cutover tool
- 2 `test_order_state.py` gc-referents — defect 3a, Python 3.12 vs 3.14
- the `schema_version == "2"` case

### 3.5 No Windows regression

Validating only on Linux would have been half the job. The full suite was re-run on Windows
(Python 3.14) from the fix branch worktree:

```
2 failed, 1304 passed, 1 warning in 134.16s
```

**Exactly the recorded floor.** The repair changes nothing for Windows.

It also names the two known failures precisely, which the programme had only described loosely:

```
FAILED tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
FAILED tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history
```

And it confirms the scope warning the `gpt-5.6-sol` audit raised: **the ledger test still fails on
Windows.** The `package.sh` fix cures the *payload*, not the Windows *working copy*, which
`core.autocrlf=true` still checks out as CRLF. Curing that would need an `.gitattributes` `eol=lf`
decision — deliberately out of scope here, because that decision interacts with defect 4 and belongs
to the owner. So on Linux the ledger test passes; on Windows it does not.

## 4. What this does NOT do

- **Does not repair defect 3a or 3b.** The Linux floor is still 25, not 2. `wal_state_bundle` remains
  broken on Linux, and it is the Stage E cutover tool.
- **Does not repair defect 4.** The service still cannot start without broker credentials, so **A-4
  is still unexecutable** and the ARM-refusal path is still untested. That needs the owner's decision.
- **Is not merged**, and has had no Gate 5 audit. Acceptance requires the canonical floor — both
  flagship auditors accepting.
- **Is not a Gate A pass.** Different release SHA, not the accepted candidate.

## 5. Safety

No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet action, no credential
value. The env file was created empty (`0600 root:root`, zero definitions) and never populated;
`HL_LIVE_ACK` never set. The service was never started. All work confined to the disposable
`GATEA-STAGING` VM. KVM2 untouched.

## 6. Codex takeover — build repair round 2 closure

The temporary Codex Lead collected the exited implementer's two-file result, independently reviewed
the actual diff, reproduced its tests on the target stack, and froze the candidate as:

- branch: `codex/gate-a-build-determinism`
- candidate: `c5a4070a4836bbb9ee010dc63db69313066667c4`
- pushed: yes; branch and origin matched `0 0`
- changed by round 2: `deploy/linux/package.sh` and `tests/test_linux_deployment.py`
- complete branch scope from `origin/master`: those two files plus the previously accepted
  `deploy/linux/lib/common.sh`

Lead execution on `GATEA-STAGING` (Ubuntu 24.04, Python 3.12.3, SQLite 3.45.1):

- `bash -n`: PASS for `package.sh` and `lib/common.sh`
- focused deployment file: **46 passed, 0 failed**
- D026 candidate GREEN: **7 passed**
- D026 deliberate mutations: all seven guards turned RED with pytest exit 1 — writable FIFO,
  missing-root fail-open, disabled CR guard at a metacharacter output path, locale-dependent
  manifest collation, unpinned `tar.umask`, bypassed export-inventory comparison, and late EXIT
  trap leaking partial `mktemp` allocations
- full Linux floor: **25 failed, 1293 passed, 1 warning** across 1,318 tests; failures were only the
  known 23-test defect-3b cascade plus two Python-3.12 `order_state` GC-referent cases
- full Windows Python 3.14.2 floor: **2 failed, 1316 passed, 1 warning**; exactly the known ledger
  working-copy CRLF and stale schema-version assertions

Audit disposition:

- round-2 GLM execution exceeded the 15-minute wrapper ceiling before returning a verdict and was
  classified **BLOCK** under D025; its orphaned child exited and its exact scratch was absent
- fresh isolated secondary-account Codex `gpt-5.6-sol` xhigh was supplemental only and returned
  **BLOCK** because the managed sandbox downgraded to read-only and rejected Git/Hyper-V commands;
  it executed no acceptance tests and raised no product finding
- final permitted round-3 GLM-5.2 executing audit returned **PASS** on the frozen SHA after
  independently reproducing 46/46 GREEN, all seven behavioral RED mutations, the exact
  25/1293/1 Linux floor, hashes, Bash syntax, local cleanliness, and exact scratch removal

**Acceptance provenance:**

`TEMPORARY OWNER-AUTHORIZED CODEX+GLM ACCEPTED — CLAUDE RETROSPECTIVE AUDIT OWED`

This accepts the build branch only. It is not a Gate A pass, is not merged to `master`, and does
not authorize KVM2. A fresh `claude-opus-5` xhigh retrospective audit of frozen
`c5a4070a4836bbb9ee010dc63db69313066667c4` remains mandatory before any master merge or KVM2 action.

Safety remained DISARMED and source/test-only. No service, deployment, credential lookup/value,
broker connection, ARM, order, TESTNET, mainnet, wallet, KVM2, or economic action occurred.

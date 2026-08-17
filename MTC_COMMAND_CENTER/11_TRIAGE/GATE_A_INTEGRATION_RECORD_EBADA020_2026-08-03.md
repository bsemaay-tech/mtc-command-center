# Gate A integration record — `ebada020` (2026-08-03)

**Status: NOT AN ACCEPTANCE.** Everything below is first-hand Lead verification against the frozen
tree. **Both platform floors are now closed** (§7) — the locked-Linux floor was executed on
`GATEA-STAGING` on 2026-08-03 and the candidate introduces no new failure. What remains open is the
D025 auditor requirement (§8): one auditor returned a qualified Windows-only accept, the second
flagship has not run. Do not read this record as Queue D acceptance.

Closes gap 2 of `GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md` in full.

---

## 1. Where this record lives, and why

This record is committed on the records branch `feature/donchian-crypto-ladder`, **not** on
`codex/gate-a-integration`. The deployment artifact was built from `ebada020`, which is currently
that branch's head. Adding a commit there would advance the head past the artifact's SHA and break
the one-to-one artifact↔branch-head provenance that Gate A A-0 depends on. **Leave
`codex/gate-a-integration` frozen at `ebada020`.**

## 2. Frozen identity

| Item | Value |
|---|---|
| Integrated commit | `ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| Branch | `codex/gate-a-integration`, pushed, worktree `C:\GATEAINTEGRATION` clean |
| Baseline | `origin/master` `637307e83951ffe23e768ed8e50ddaf8712b0660` |
| Artifact built from it | `C:\WPI_ARTIFACTS\ebada020…`, manifest `8FC30864…4700C9` |

## 3. Merge structure — four merges, first-parent chain from `origin/master`

```
ebada020  parents f6478e53 ebb750da   merge(gate-a): integrate accepted residual evidence tests
f6478e53  parents 499ae639 17402a58   merge(gate-a): integrate accepted credential-free DISARMED mode
499ae639  parents 20f44b8f 7aad0377   merge(gate-a): integrate accepted WAL capture repair
20f44b8f  parents 637307e8 82e92c98   merge(gate-a): integrate accepted build determinism
```

All four accepted product SHAs — `82e92c98`, `7aad0377`, `17402a58`, `ebb750da` — are ancestors of
`ebada020`. Each merge brings in exactly one accepted line; no squash, no rewrite, no cherry-pick.

## 4. Exact scope — nine files, no creep

`git diff --name-status origin/master..ebada020`:

```
M .gitattributes
M IBKR_PAPER_BRIDGE/bridge/api/routes.py
M IBKR_PAPER_BRIDGE/bridge/app.py
M IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
M IBKR_PAPER_BRIDGE/deploy/linux/package.sh
A IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py
M IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
M IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
M IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
```

This is exactly the union of the four accepted scopes. Nothing else entered the tree.

## 5. The single conflict, and why the resolution is correct

One textual conflict, in `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`, at the manifest
schema-version assertion. Both sides had independently touched the same line for different accepted
reasons.

Before — 3b (`7aad0377`), line 890:

```python
    # The merged TS-P1 chain moved the operational baseline from v2 to v4;
    # this assertion was never updated with Store.initialize()'s default.
    assert inv["schema_version"] == "4"
```

Before — residual repair (`ebb750da`), line 321, plus a new import:

```python
from bridge.store.db import SCHEMA_VERSION_BASELINE, Store
...
    assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)
```

After — integrated (`ebada020`), line 890, with the import carried to line 20:

```python
    # The merged TS-P1 chain moved the operational baseline from v2 to v4;
    # this assertion was never updated with Store.initialize()'s default.
    assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)
```

Verified: `SCHEMA_VERSION_BASELINE = 4` at `IBKR_PAPER_BRIDGE/bridge/store/db.py:268`, so the two
sides agree on today's value and the merge changes no behaviour. Keeping 3b's comment preserves the
reason the assertion exists; taking the residual branch's derived constant removes a literal that
would silently go stale the next time the baseline moves — which is precisely the class of defect
the residual repair was accepted for.

**Correction, 2026-08-08 (flagship NIT 2, reproduced).** This record originally claimed the derived
form was *strictly more robust* and that keeping `"4"` was *strictly weaker*. That overstates it. The
`claude-opus-5` xhigh flagship mutation-tested both: raising `SCHEMA_VERSION_BASELINE` 4→5 while
leaving the producer literal at `"4"` makes the derived form **and** the WAL branch's literal fail
identically, ERRORing at fixture setup with `MigrationError: MIGRATION_FAILED: v4-to-v5 requires
schema_version=4` (`db.py:1477`) before line 890 is ever evaluated. No mutation was found where the
derived form fails and the literal passes. The resolution is correct either way and better for
maintenance — it auto-follows a coordinated bump instead of needing a stale-literal edit — but it is
**not stronger at detection**. Only the justification was wrong, not the resolution. The assertion is
separately proven non-vacuous: mutating the producer literal at `db.py:896` to `"5"` makes it FAIL.

Read-only pairwise `git merge-tree` probes found this conflict in exactly one file pair
(3b × residual) and zero conflicts in every other pair. Reproduced here: the conflict occurs at this
site and nowhere else in the nine-file scope.

## 6. Ledger line-ending refresh — a real trap, recorded

The residual repair adds one rule to `.gitattributes`:

```
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

**A `.gitattributes` rule does not retroactively renormalise a file that is already checked out.**
The merge produced a correct LF blob while the working tree still held the CRLF copy inherited from
`text=auto`, and the ledger evidence check hashes working-tree bytes. The fix was to refresh that
one tracked path through Git's filters — not to edit the blob, and not a repository renormalisation.

Verified now, in `C:\GATEAINTEGRATION`:

| Check | Value |
|---|---|
| Blob SHA-256 at `ebada020` | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Working-tree file SHA-256 | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` — equal |
| CR bytes in the working-tree file | 0 |

## 7. Platform floors

| Platform | Result | Evidence |
|---|---|---|
| Windows full suite | **`1359 passed, 1 warning`** — Lead-reproduced | original `C:\tmp\gatea_integration_windows_full_ebada020.txt` (`136.91s`); independent Lead rerun in fresh detached worktree `C:\GAAUD_INT_GLM` gave `1359 passed, 1 warning in 130.09s` |
| Locked Linux full suite | **`2 failed, 1357 passed, 1 warning` — CLOSED 2026-08-03** | `C:\tmp\LINUX_FULL_EBADA020_LEAD_2026-08-03.log` |
| Locked Linux parent floor | `25 failed, 1281 passed, 1 warning` | `C:\tmp\LINUX_FULL_PARENT_637307E8_LEAD_2026-08-03.log` |

### Locked-Linux execution — Lead, on `GATEA-STAGING`

Host verified before use: `gatea-staging`, Ubuntu 24.04.4 LTS, **Python 3.12.3, SQLite 3.45.1** —
the locked runtime. KVM2 was not touched.

Provenance of the source under test: the corrected LF snapshot
`gatea-integration-ebada020-lf2.tar` was already on the host and hashes **byte-identical** to the
local copy (`1f1a7531…79fce8`). A **fresh** workspace was extracted from that verified tar rather
than trusting any pre-existing directory. Verified on Linux after extraction:

| Check | Result |
|---|---|
| `deploy/linux/{install,package,rollback,verify}.sh` + `lib/common.sh` | **CR = 0** on all five |
| `ledger_schema.json` SHA-256 | `f4cdece5…bda90e` — canonical |
| Conflict site line 890 | `str(SCHEMA_VERSION_BASELINE)` |

Interpreter: the existing hash-locked venv on the host,
`/opt/mtc-bridge/venvs/a1dd5b467b12421f632bf3d8462a7244b39b2287/bin/python`, pytest 9.1.1. It is
root-owned and read-only; nothing was installed and the host was not modified. Note that this venv's
SHA is an earlier installed release, **not** `ebada020` — it is the fixed interpreter, while the
source under test is the `ebada020` snapshot. Candidate and parent ran on the **same** interpreter,
which is the only thing that makes the floor comparison meaningful.

```
python3 -m pytest IBKR_PAPER_BRIDGE/tests -q -p no:randomly -p no:cacheprovider --basetemp=...
candidate ebada020 → 2 failed, 1357 passed, 1 warning in 132.90s
parent    637307e8 → 25 failed, 1281 passed, 1 warning in 131.76s
```

**Failure node ID comparison — the actual bar:**

- **New failures in the candidate: NONE.** `comm -23 candidate parent` is empty.
- Failures **fixed** by the candidate: **23**, all in `test_wal_state_bundle.py`.
- The 2 remaining candidate failures are present on the parent too and are the known pre-existing
  Python-3.12 order-state GC assertions:
  `test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container` and
  `::test_gc_referents_of_raw_aliases_contain_no_mutable_container`.

The candidate therefore introduces no new locked-Linux failure and removes 23. The superseded log
`C:\tmp\gatea-integration-linux-full-ebada020.log` (`16 failed, 1343 passed`) remains what it always
was — the deliberate bare-`git archive` falsification run — and must never be cited as a floor.

## 8. Audit status

The four input lines were each independently audited and accepted. **The integrated SHA `ebada020`
is still NOT ACCEPTED**, because D025 acceptance needs both flagships and only one auditor has run.

- **Round 1 (GLM-5.2): BLOCK** — environmental. Its session could not execute `pytest` or read the
  artifact directory. **Zero required findings, zero nits.**
- **Round 2 (GLM-5.2, permissions granted): `PASS-WINDOWS-ONLY-WITH-NITS`** — it executed the
  Windows suite and reproduced `1359 passed, 1 warning`, verified the artifact identity and the
  absence of the A-2 CR defect, and completed the silent-merge analysis with **zero required
  findings** and one cosmetic nit. It correctly declined to claim the Linux floor.
- **Second flagship `gpt-5.6-sol` xhigh: not run.** This is the only remaining acceptance blocker.

Record: `GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md`.

## 9. Related evidence

- Artifact identity + secret scan: `GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`
  — manifest hash recomputed and matching, nine-category content-redacted scan 0 hits, built payload
  shell scripts 0 CR bytes.
- Owner decision **2026-08-03 — option (a) ACCEPTED:** the rebuilt artifact ships without
  `deploy/linux/SECURITY_BASELINE.md` and `11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md`. Both live
  on the records branch and never landed on `origin/master`; neither is referenced by Bridge source
  or the Gate A runbook. **The drift is accepted, no rebuild will be performed, and `ebada020`
  remains the frozen build SHA.** The security baseline is authoritative on the records branch.

## 10. Boundary

Read-only inspection and doc authoring only. `origin/master` unchanged, `codex/gate-a-integration`
head unchanged at `ebada020`, artifact bytes untouched, no host contacted. No merge, deployment,
service or runtime change, credential handling, broker call, ARM, order, TESTNET, mainnet,
Pine/parity/MTC/trading change or economic action.

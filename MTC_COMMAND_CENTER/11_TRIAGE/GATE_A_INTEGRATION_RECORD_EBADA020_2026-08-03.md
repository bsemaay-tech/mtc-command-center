# Gate A integration record — `ebada020` (2026-08-03)

**Status: PARTIAL — NOT AN ACCEPTANCE.** Everything below is first-hand Lead verification against
the frozen tree. Two items are deliberately left open and are called out as `PENDING`: the
locked-Linux floor (§6) and the D025 executing audit of the integrated SHA (§8). Do not read this
record as Queue D acceptance.

Closes gap 2 of `GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md` for its Linux-independent part.

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
the residual repair was accepted for. **The strictly weaker option would have been keeping `"4"`.**

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
| Windows full suite | **`1359 passed, 1 warning in 136.91s`** | `C:\tmp\gatea_integration_windows_full_ebada020.txt` |
| Locked Linux full suite | **PENDING — no valid evidence exists** | see below |

**The Linux floor is open and must not be treated as satisfied.** The only Linux log on disk,
`C:\tmp\gatea-integration-linux-full-ebada020.log` (`16 failed, 1343 passed`), was written at
05:04:45, which is *before* the corrected LF snapshot `gatea-integration-ebada020-lf2.tar` was
created at 05:05:28. That log therefore belongs to the deliberate bare-`git archive` falsification
run, which reproduces the historical CRLF defect on purpose. It is falsification evidence, not
candidate evidence, and citing it as a candidate floor would be wrong.

Required to close: build a corrected snapshot with `git -c core.eol=lf archive`, verify zero CR
bytes in `deploy/linux/*.sh`, run the complete suite on the locked runtime, **persist the log**, and
compare failure node IDs against the `637307e8` parent floor. No new failure node ID is the bar.

## 8. Audit status

The four input lines were each independently audited and accepted. **The integrated SHA `ebada020`
itself has not been audited.** D025 applies to the merged result: canonical executing auditors, and
an auditor that cannot execute the suite must BLOCK.

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

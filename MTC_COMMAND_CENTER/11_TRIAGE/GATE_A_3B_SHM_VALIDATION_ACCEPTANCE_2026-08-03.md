# Gate A defect 3b SHM validation — owner-waiver acceptance

Date: 2026-08-03

## Disposition

**ACCEPTED** for source-candidate purposes at
`7aad0377106c7bb1ebcf79990051806d2e6ce0d7`, direct parent
`df00634fc2e5fb19cddb34a6ad16d9764c4779a4`.

This is not Queue D authorization, integration approval, a rebuilt artifact, a Gate A execution
pass, deployment approval, or permission for any runtime/broker/economic action.

## Owner waiver

Barış explicitly directed on 2026-08-03 that Claude credit is unavailable, audits must continue
through Codex itself or other available models, work must not pause for the unavailable Claude route,
and this decision overrides the repository's model-roster dependency. This satisfies the roster's
explicit owner-waiver clause. It does not waive reproduced required findings, D026, platform
execution, evidence integrity, or the previously stated Queue D/live-action hard stop.

## Scope and integrity

- Product commit changes exactly:
  - `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`
  - `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`
- Tool blob: `26c077e650ab88ba2086efa3a80790769bc055b1`.
- Test blob: `c6e2e18c6e56d5ed7924c34cc5400eb152d5dbec`.
- `git diff --check` passed; product worktree and all auditor worktrees were clean.
- No schema, Pine, parity, MTC strategy, broker, runtime, service, or deployment file changed.

## D026 and platform evidence

| Evidence | Candidate | Exact parent / falsification |
|---|---:|---:|
| Windows focused SHM set | `30 passed` | — |
| Windows complete module | `74 passed` | — |
| D026 usable-SHM guard bypass | restored GREEN `9 passed, 65 deselected` | RED `9 failed, 65 deselected` |
| Windows full Bridge/KVM2 | `1 failed, 1338 passed` | `1 failed, 1309 passed` |
| Locked Linux full Bridge/KVM2 | `2 failed, 1337 passed` | `2 failed, 1308 passed` |
| 2026-08-03 fresh module recheck | `74 passed` | Windows and locked Linux |

The Windows failure is the same KVM2 ledger artifact-hash mismatch on both revisions. The two Linux
failures are the same Python-3.12 `order_state` GC-referent assertions on both revisions. The repair
adds 29 passing tests on each platform and no new full-suite failure.

The D026 falsification bypassed only the new usable-SHM guard. All nine behavioral cases failed,
then passed after byte-for-byte restoration. The restored file hashes and clean status matched the
frozen candidate.

## Independent audit evidence

| Auditor | Execution | Verdict |
|---|---|---|
| Codex `gpt-5.6-sol` xhigh | full Windows/Linux, exact-parent baselines, D026, final clean proof | **PASS** |
| GLM-5.2 | independent full executing audit and final clean proof | **PASS-WITH-NITS** |
| DeepSeek V4 Flash | exact ClinePass route unavailable | BLOCK on route availability; no finding |
| Claude `claude-opus-5` xhigh | credit/session route unavailable | Replaced only by the explicit owner waiver above |

GLM's only nit was wording: the source preflight is required before source connections, not the
writable destination connection. No code repair was required. The Lead independently inspected the
complete diff and reproduced the product behavior and platform evidence.

## Safety and next boundary

The accepted commit may be published on its feature branch. It must not be merged or used to rebuild
artifacts under this record. The next authorized source work is repair of the independently reproduced
build-candidate findings, followed by Queue C. Queue D remains stopped.

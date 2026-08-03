# Gate A residual evidence-test repair — owner-waiver acceptance

Date: 2026-08-03

## Disposition

**ACCEPTED** for source-candidate purposes at
`ebb750dafd71c5d1293a9524846a00cd33b212bc`, a single direct child of
`637307e83951ffe23e768ed8e50ddaf8712b0660`.

This record closes the two pre-existing Windows-only evidence-test failures observed while auditing
the Gate A candidates. It is not Queue D authorization, integration approval, artifact rebuild
approval, deployment approval, or permission for runtime, broker, trading, or economic action.

## Owner waiver and exact scope

Barış explicitly waived the unavailable-Claude dependency on 2026-08-03 and directed continued
Codex/alternative-model audit. The candidate changes exactly two files:

- `.gitattributes`
- `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`

No runtime, product, ledger-content, schema, Pine, parity, MTC, broker, order, or economic behavior
changed.

## Repaired findings

1. The canonical ledger row expects SHA-256
   `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e`, the hash of the committed
   LF bytes. Windows checkouts under the repository-wide `text=auto` policy produced CRLF working
   bytes and hash `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a`.
   The exact evidence path is now pinned to `text eol=lf`; the ledger blob itself is unchanged.
2. `test_invariants_preserve_risk_and_history` expected stale schema literal `"2"`, while ordinary
   `Store.initialize()` uses `SCHEMA_VERSION_BASELINE = 4`. The test now derives its expectation
   from that production baseline constant.

## D026 falsification evidence

Against an exact fresh checkout of parent `637307e8`, the two named tests were **RED: exactly
`2 failed`** — the ledger artifact-hash mismatch and actual schema `"4"` versus literal `"2"`.
Against exact candidate `ebb750da`, they were **GREEN: exactly `2 passed`**.

Independent archive/checkout falsification also reproduced the line-ending defect: the parent
produced CRLF and `b6580e31...` on Windows, while the candidate produced LF and the canonical
`f4cdece5...` hash. Both tests therefore have demonstrated pre-fix failure and fixed behavior.

## Platform evidence

| Platform | Focused / ledger | Complete `IBKR_PAPER_BRIDGE/tests` |
|---|---:|---:|
| Windows candidate | `2 passed` | `1306 passed` |
| Locked Linux candidate | ledger node `1 passed` | `25 failed, 1281 passed` |
| Locked Linux parent | canonical LF ledger | `25 failed, 1281 passed` |

The candidate and parent Linux failure node IDs are identical. The 25 retained Linux failures are
pre-existing platform/baseline failures; this candidate adds no full-suite regression.

## Independent executing audits

- Fresh `gpt-5.6-sol` xhigh: **PASS**, no required findings. It independently executed D026,
  Windows full-suite validation, candidate/parent Linux validation, archive behavior, blob/scope,
  ancestry, and final-clean proofs.
- Fresh execution-enabled GLM-5.2: **PASS**, no required findings, after independently executing
  the same required Windows, Linux, D026, scope, and cleanliness evidence.
- Lead independently reproduced the defects, exact two-file diff, unchanged ledger blob, D026
  transition, platform counts, Linux failure-name equality, ancestry, and clean state.

## Safety and next boundary

The repaired branch may be published for source-candidate evidence. It must not be merged or used
for artifact rebuild under this record. Queue D, integration, Gate A rerun, deployment, runtime,
credentials, broker access, ARM/orders, TESTNET/mainnet, Pine/parity/MTC/trading changes, and all
economic action remain stopped.

# Gate A build-determinism repair — owner-waiver acceptance

Date: 2026-08-03

## Disposition

**ACCEPTED** for source-candidate purposes at
`82e92c98fdc24cfc1632960460d3ac7e4131db25`, direct parent
`c5a4070a4836bbb9ee010dc63db69313066667c4`.

This is not Queue D authorization, integration approval, artifact rebuild approval, a Gate A
execution pass, deployment approval, or permission for runtime/broker/economic action.

## Owner waiver and scope

Barış explicitly waived the unavailable-Claude dependency on 2026-08-03 and directed continued
Codex/alternative-model implementation and audit. The repair changes exactly
`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`; deployment product blobs remain unchanged.

The original cycle from `637307e83951ffe23e768ed8e50ddaf8712b0660` through the repaired candidate
still changes exactly `deploy/linux/lib/common.sh`, `deploy/linux/package.sh`, and the test file.

## Repaired findings

1. The locale comparison now skips only when `en_US.UTF-8` is not actually available. The manifest
   comparison still executes unchanged when the locale exists.
2. The assertion coupled to the comment text `` `* text=auto` `` was removed. A new behavioral test
   forces repository `core.eol=crlf` under `* text=auto`, runs the real package builder, and requires
   the exported file to remain byte-exact LF.

## D026

- Removing only `-c core.eol=lf` from `package.sh` makes the behavioral test RED because exported
  size/content changes under CRLF conversion. Exact restoration makes it GREEN.
- Locked Linux with empty `LOCPATH`: parent test RED on `ANSI_X3.4-1968`; repaired test SKIP instead
  of a false failure; normal generated locale GREEN.
- The D026 mutation was restored to product blob `add6478d33cce8d929d58f895407abe01d51da20`.

## Platform evidence

| Platform | Focused/file | Full Bridge/KVM2 |
|---|---:|---:|
| Windows | repaired focus `3 passed`; file `1 failed, 46 passed` | `2 failed, 1317 passed` |
| Locked Linux | file `47 passed` | `25 failed, 1294 passed` |
| Locked Linux parent | file `46 passed` | `25 failed, 1293 passed` |

All parent/candidate Linux failure node IDs match exactly. Windows failures are the unchanged KVM2
ledger artifact-hash mismatch and stale WAL-bundle schema expectation. Linux failures remain the
same two Python-3.12 order-state GC assertions and 23 pre-existing WAL-bundle failures. The repair
adds one passing test and no new failure.

## Independent audits

- GLM-5.2 executing audit: **PASS-WITH-NITS**. Optional skip-message wording nit only.
- Fresh `gpt-5.6-sol` xhigh executing audit: **PASS**, no required findings.
- Lead independently reproduced scope, D026, platform counts, and failure-name equality.

Both audit worktrees ended at the frozen SHA with empty status. `codeburn` reported no external API
spend for the subscription-routed GLM execution.

## Safety and next boundary

The repaired branch may be published. It must not be merged or used for an artifact rebuild under
this record. Next source task is Queue C repair/audit closure; Queue D remains stopped.

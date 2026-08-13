# RP7 cap-override T0 audit - Claude flagship

Dispatch only after every `PENDING-FILL-AFTER-REPAIR` field is replaced from
the frozen committed bytes. Any unfilled field is a dispatch BLOCK.

Auditor: fresh independent `claude-opus-5`, effort `xhigh`, T0. Read-only
except one verdict file. Do not read the Codex verdict for this same round. No
resume/continue, sub-delegation, Git mutation, host/network contact, deployment,
credentials, ARM, orders, TESTNET, mainnet, Pine, parity, or trading action.

Owner authority: `WPI_OWNER_DECISIONS_2026-08-13.md` section 4 authorizes this
single extra repair/audit cycle; it waives no acceptance standard.

Frozen subject commit: `PENDING-FILL-AFTER-REPAIR`

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | `PENDING-FILL-AFTER-REPAIR` | `PENDING-FILL-AFTER-REPAIR` |
| `SELF_QA_RP7.md` | `PENDING-FILL-AFTER-REPAIR` | `PENDING-FILL-AFTER-REPAIR` |
| `STATUS_RP7.md` | `PENDING-FILL-AFTER-REPAIR` | `PENDING-FILL-AFTER-REPAIR` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | `PENDING-FILL-AFTER-REPAIR` | `PENDING-FILL-AFTER-REPAIR` |

Read the prior Claude T0 verdict, supplemental findings, repair report sections,
and frozen artifacts. Re-derive identities before execution.

Mandatory audit:

1. Execute the exact rows-1-9 fence sequentially with a run-owned scratch root.
   Require exact transcript reproduction, clean syntax, unchanged identities,
   and no harness-abort/capture-collision/ERR-trap contamination.
2. Verify CRLF and LF continuation semantics against the actual production
   parser. Confirm the fix removes trailing `\r` only and preserves the real
   trailing-space-after-backslash boundary.
3. Verify package-owned two-subject D026: actual round-4 blob and repaired bytes
   run in separate processes, with exact per-pair heterogeneous rc and terminal
   output assertions. Sourcing both subjects in one shell is non-evidence.
4. Reproduce the row-9 partial/mid-name quote attack and verify it can no longer
   normalize into the protected target. Confirm a fully quoted valid assignment
   remains accepted and the duplicate-key policy is explicit and tested.
5. Search adjacent row-6/row-9 grammar boundaries for false PASS, false FAIL,
   or ambiguous STOP, and verify every claimed new test under D026.
6. Verify no audit-attributable repository delta except the verdict file.

Write only
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_CLAUDE_T0_AUDIT_2026-08-13.md`.

Verdict must be exactly PASS, PASS-WITH-NITS, REQUEST_CHANGES, or BLOCK.
PASS-WITH-NITS may contain no required repair. This auditor alone cannot accept
T0; both mandatory flagship verdicts are required.

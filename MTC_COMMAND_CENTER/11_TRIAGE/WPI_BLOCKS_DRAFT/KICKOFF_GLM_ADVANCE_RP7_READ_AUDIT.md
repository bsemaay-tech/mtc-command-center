# KICKOFF — GLM-5.2 ADVANCE read-audit: RP7-WPI-RO.sh round 9

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## What this dispatch is, and honestly is not
An **ADVANCE, SUPPLEMENTAL read-audit**, not the second-flagship audit. RP7 holds a Codex
flagship acceptance (`RP7_CODEX_T0_AUDIT_R9`, PASS); the required second flagship is Claude
`claude-opus-5`, running tonight. **Your verdict cannot close that slot and must not claim to.**
Prefix your verdict line `ADVANCE-SUPPLEMENTAL`. Unattended GLM is execution-gated on this host:
if you cannot run the harness, mark those steps `PENDING-LEAD-EXECUTION` and keep your opinion
source-level — **never fabricate a green run.**

## Bytes
`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — per the acceptance matrix, 108301 B, SHA-256
`0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`. Re-derive and confirm.
Evidence: `STATUS_RP7.md`, `SELF_QA_RP7.md` (§ROUND 9), `RP7_R9_REPORT`, and the Codex chain
`RP7_CODEX_T0_AUDIT_R8_PART_B` → `R9`.

## The r9 headline you must independently re-establish
Round 6 recorded a residual and round 8 restated it: `ro.status.body` was create-once allocated
and then handed to curl, to the digest and to the parser **by NAME**. Codex then executed both
halves of what that note admitted — a hard link at that name made curl overwrite an object
**outside the evidence tree** at capture rc 0, and replacing that name between the digest and the
parser turned a child-produced ARMED body into an accepting DISARMED result carrying the ARMED
body's digest. **The note was true and the block's own unqualified sentences were false beside
it.** That is the lesson this round is built on: an accurate disclosure is not a safety control.

Round 9's design change: the leaf is opened by `wpi_open_leaf`, which keeps the descriptor its
`O_CREAT|O_EXCL` open returned; that descriptor is duplicated into the capture child at fd 3 and
curl is given `--output /dev/fd/3` — a path resolving through the process's descriptor table, not
through the evidence directory. The read descriptor derives from the same open **at creation
time**, before the child exists. The parser is given no path: its stdin is that descriptor.
`wpi_alloc_leaf`, the name-only allocator, is **deleted** rather than left available.

## Priority reading targets
1. **Attack the descriptor binding.** Is there ANY remaining site where an evidence leaf is
   created and later addressed by a rebindable name? Any second reader of a name? Any place a
   caller-declared rc literal survives instead of the measured child status? (Round 8 let every
   caller write `rc=0` into its own reason while a child exited 7 — the rc field is now filled
   from the measured status.)
2. **Rows 20–21 scope.** The rows 10–23 read-only claim was false *inside* rows 20–21, where the
   rows 10–19 scope boundary does not reach. Verify it now holds there.
3. **Row 22's `detail` field** on both nonzero namespace-read branches.
4. **Claim wording.** `does_not_establish` must keep `identity_of_the_manager_that_answered` in
   substance — every claim sentence stays about *the manager that answered in the attested
   execution domain*, never about "the host". Row 24 stays operator-side only.
5. **Cross-check today's freeze-input ledger** (`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`): it
   states RP7 rejects a marker evidence root and requires `EV_DIR` to descend under it
   (`RP7-WPI-RO.sh:916-921`), and that `WPI_FIXED_EVIDENCE_ROOT` must be filled from the
   allocated evidence root **before** RP7 bytes are frozen. That ledger came from a weaker model
   (gpt-5.5) and needs independent confirmation.

## Verdict
Grammar: `PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK`, prefixed `ADVANCE-SUPPLEMENTAL`.
State plainly what you executed and what you did not.

Write ONE new file: `RP7_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` in `WPI_BLOCKS_DRAFT`.

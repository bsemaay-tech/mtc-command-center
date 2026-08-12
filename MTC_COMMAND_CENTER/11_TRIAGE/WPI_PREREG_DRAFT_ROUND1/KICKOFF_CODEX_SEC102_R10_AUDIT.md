# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 10 (executed-byte binding — closes the slot if PASS)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r10; independent
cross-model check. Fresh session, read-only: edit nothing except your verdict file, no git
mutation, no host, no network. T1. Your only repository delta must be the verdict file.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only summary/`CASES=`/`FAILED_COUNT=`/
`BLOCKS=`/`PINNED_ALL=`/`WINERROR=`/`REBOUND_UNDER_R9=`/`OUTER_WRAPPER_RC=` lines. Refer to
fixtures by class name; never reproduce a sensitive body. Do NOT author new attack fixtures.
Verdict first.

## Bytes — commit `a0ebac7b`. `composite_pathproof.py` UNTOUCHED (r10 is harness-only — confirm
its worktree object equals the r8/r9 commit; expected 129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`). NEW `SELF_QA_SEC102_R10.md`,
`SEC102_R10_REPORT_2026-08-12.md`. `STATUS_SEC102.md` updated. This is the LAST finding before
SEC102's Codex flagship slot closes.

## Your r9 finding (MEDIUM, Pattern 11 / Pattern 9 overlay) — TOCTOU
The pre-launch byte comparison was not bound to the object `powershell.exe -File <pathname>`
later reopens by name; a same-principal concurrent writer in the check→launch window could
execute bytes never compared while `SCRIPT_BYTES_IDENTICAL=1` stood.

## Round-10 disposition (Lead ran the §13c wrapper verbatim from outside the repo:
`OUTER_WRAPPER_RC=0`, `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 NAME_BOUND_ALL=11
POST_NAME_BOUND_ALL=11 POST_BYTES_UNCHANGED_ALL=11 MISMATCHED=0 REJECTED=0`, §13d transcript
EXACT match). Route A object pinning:
1. Temp `.ps1` created via `CreateFileW` with `FILE_SHARE_READ` only (write+delete sharing
   withheld); bytes read back THROUGH the held handle, never by reopening the name.
2. The exclusion is MEASURED, not assumed: the wrapper asks Windows for the write-open and the
   delete-open the pin should forbid and requires `ERROR_SHARING_VIOLATION` (32) on both, once
   per block × 11.
3. Pathname re-resolved to the pinned object by volume-serial + file-index; EVERY path
   component (script dir → volume root) pinned so the name cannot be diverted at any step;
   incomplete pin → no child launched.
4. Handle held across the child's whole lifetime; binding + bytes re-measured AFTER exit,
   before stdout is read.
D026 deterministic (not raced): `rebind_certified` R9 ACCEPTED (`R9_ASSERTED_IDENTITY=1` +
`REBOUND_UNDER_R9=1` in one run) / R10 REJECTED with real OS refusal (`INPLACE_WRITE=DENIED
WINERROR=32`, `ENTRY_REPLACE=DENIED`); `rebind_honest` inverse; `M2` (share-mode opened)
caught before the child by the measured exclusion; `M3` (post-run gate) lets the rewrite
succeed, child runs unproved bytes, gate 4 refuses with stdout unread; `M1` byte gate carried;
`CONSERVED_R9_VERDICTS=6`.

## New disclosed residuals (STATUS items 45-49; item 43 names the closed temporal-rebinding
class): the sub-filesystem rebind (volume/drive-letter redefinition) is NOT prevented by any
share mode but is DETECTED by the post-run re-resolution and is terminal with stdout never
interpreted; unpinned interpreter binary; availability surface (the wrapper denies other
processes a write/delete-open on ancestor dirs for the run duration, released on exit —
disclosed for the Lead's re-run); Windows/NTFS scope; no new module property. Residual 41
carried.

## Audit contract
1. Confirm `composite_pathproof.py` byte-identical to the r8/r9 commit and re-run the 58-case
   matrix VERBATIM → no regression.
2. Extract the §13c fence AS BYTES per §13d, run it from outside the repository, confirm the
   binding gates precede the child and the post-run re-measurement precedes stdout, and the
   full transcript reproduces (all eleven blocks, `PINNED_ALL=11`).
3. Run §13b VERBATIM: confirm `rebind_certified` flips R9→R10 with a REAL `WINERROR=32` denial,
   `rebind_honest` inverse, M2/M3/M1 all exercised and terminal, the 6 R9 verdicts conserved.
4. The core test: is there STILL a path where the executed bytes differ from the compared bytes
   without rejection? Attack the pin (share-mode widening, path-component swap, post-run
   divergence, handle-reuse). Judge whether the volume/drive-letter residual is honestly
   DETECTED (terminal, stdout uninterpreted) rather than silently admitted.
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. **If PASS/
   PASS-WITH-NITS, state that this closes the SEC102 Codex flagship slot** — both original
   CRITICALs, R3-F2/F3, the command-word whitelist fixpoint, the r7 child-completion gate, the
   r8 byte-identity gate, and now the r9 executed-byte binding are all closed; the sole
   remaining items are the owner-ratified interpreter-vocabulary production-gate decision and
   the GLM-5.2 T1 second opinion, which the Lead dispatches next.

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md`.

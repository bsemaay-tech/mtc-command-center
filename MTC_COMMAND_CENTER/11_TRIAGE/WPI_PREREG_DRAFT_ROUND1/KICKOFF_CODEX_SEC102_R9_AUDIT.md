# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 9 (byte-identity fix — closes the slot if PASS)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r9; independent
cross-model check. Fresh session, read-only: edit nothing except your verdict file, no git
mutation, no host, no network. T1. Prove your only repository delta is the verdict file.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only summary/`CASES=`/`FAILED_COUNT=`/
`BLOCKS=`/`SCRIPT_BYTES_IDENTICAL`/`FALSE_ACCEPT_UNDER_R8=`/`OUTER_WRAPPER_RC=` lines. Refer to
fixtures by class name; never reproduce a sensitive body. Do NOT author new attack fixtures.
Verdict first.

## Bytes — commit `ba929abc`. `composite_pathproof.py` UNTOUCHED (r9 is harness-only — confirm
its worktree object equals the r8 commit; expected 129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`). NEW `SELF_QA_SEC102_R9.md`,
`SEC102_R9_REPORT_2026-08-12.md`. `STATUS_SEC102.md` updated. This is the LAST finding before
SEC102's Codex flagship slot closes.

## Your r8 finding (MEDIUM, Pattern 10/11)
The §13 paste-run wrapper rewrote every LF-only block to CRLF before execution
(`NamedTemporaryFile("w", encoding="utf-8")`, text-mode read) while claiming byte-for-byte
extraction and execution — a 110-LF block was written as 110 CRLF; the executed instrument was
not the published instrument.

## Round-9 disposition (Lead ran the §13c wrapper verbatim from outside the repo:
`OUTER_WRAPPER_RC=0`, `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 REJECTED_ON_BYTES=0
STATUS_PROVED_COMPLETE=11 MISMATCHED=0 REJECTED=0`, per-block transcript EXACT match to §13d)
1. Wrapper reads the Markdown with `read_bytes`, matches fences on bytes, writes each temp
   `.ps1` with `write_bytes`, and asserts the on-disk script bytes equal the fence bytes
   BEFORE `subprocess.run` exists (`SCRIPT_BYTES_MISMATCH` → `CHILD_NOT_LAUNCHED`). The r8
   status/stderr/subset gates are conserved verbatim BEHIND the byte gate (order 0→1→2→3).
2. §13b D026 both directions: a line-ending-sensitive sentinel (LF fence, CRLF-only transcript)
   is ACCEPTED by the exact r8 wrapper and REJECTED by r9 (`FALSE_ACCEPT_UNDER_R8=1`); the honest
   LF sentinel is REJECTED by r8 and ACCEPTED by r9 (`FALSE_REJECT_UNDER_R8=1`); the 4 r8
   controls conserved; an M1 mutant restoring the r8 write path inside the r9 instrument fires
   the byte gate (`M1_GATE_FIRED=1`). Your 110-LF numbers reproduced
   (`R8_TEXTMODE … WRITTEN_CRLF=110 BYTE_IDENTICAL=0` vs `R9_BYTEMODE … WRITTEN_CRLF=0
   BYTE_IDENTICAL=1`).
3. §13d/e: all eleven blocks re-run from exact published bytes with per-block
   `FENCE_BYTES=SCRIPT_BYTES`, `LF/CRLF/NONASCII` counts, SHA-256, rc 0, zero stderr.
4. New DISCLOSED residual (STATUS item 41 / §11 residual 1): byte identity is asserted against
   the document as it exists on disk, not a pinned checkout — repo `text=auto`+`autocrlf` could
   materialize a fresh clone as CRLF, in which case block 11 reports a LOUD `MISMATCH` (not a
   silent pass); per-block LF/CRLF/SHA are published as the cross-check. Judge honesty, do not
   demand a `.gitattributes` change outside the r9 fence.

## Audit contract
1. Confirm `composite_pathproof.py` byte-identical to the r8 commit (harness-only round) and
   re-run the 58-case matrix VERBATIM → no regression.
2. Extract the §13c fence AS BYTES per §13d, run it from outside the repository, and confirm
   the full transcript reproduces (byte gate ahead of the r8 gates; all eleven blocks).
3. Run §13b VERBATIM: confirm the false-accept and false-reject both flip r8→r9, the 4 controls
   conserve, and the M1 mutant proves the byte gate is exercised (not an unexercised branch).
4. Any residual: is there still a path where the executed bytes can differ from the published
   fence bytes without rejection? Judge disclosed residual 41's honesty (loud vs silent).
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. **If PASS/
   PASS-WITH-NITS, state that this closes the SEC102 Codex flagship slot** — both original
   CRITICALs, R3-F2/F3, the command-word whitelist fixpoint, the r7 child-completion gate, and
   now byte-identity are all closed; the sole remaining items are the disclosed
   interpreter-vocabulary production-gate decision (owner-ratified 2026-08-12) and the GLM-5.2
   T1 second opinion, which the Lead dispatches next.

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R9_2026-08-12.md`.

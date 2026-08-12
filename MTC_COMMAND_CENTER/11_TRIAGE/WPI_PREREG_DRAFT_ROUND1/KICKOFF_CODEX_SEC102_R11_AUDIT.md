# KICKOFF — Codex T1 audit: SEC102 round 11, the executed-byte-binding FIXPOINT (closes the slot if PASS)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Claude Max implemented r11; independent
cross-model check. Fresh session, read-only: edit nothing except your verdict file, no git
mutation, no host, no network. T1. Your only repository delta must be the verdict file.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only summary/`CASES=`/`FAILED_COUNT=`/
`BLOCKS=`/`NAMELESS_EXEC_ALL=`/`CHAIN_LINKS=`/`FALSE_ACCEPT_UNDER_R10=`/`OUTER_WRAPPER_RC=`
lines. Refer to fixtures by class name; never reproduce a sensitive body. Do NOT author new
attack fixtures. Verdict first.

## Bytes — commit `5f87cbc2`. `composite_pathproof.py` UNTOUCHED (r11 is harness-only — confirm
its worktree object equals the r8/r9/r10 commits; expected 129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`). NEW `SELF_QA_SEC102_R11.md`,
`SEC102_R11_REPORT_2026-08-12.md`. `STATUS_SEC102.md` updated.

## Your r10 findings (both MEDIUM, Pattern 11) — both claimed CLOSED BY CONSTRUCTION
1. Transient volume/drive-letter rebind restored before the post-run sample escaped the
   two-sample detector.
2. Leaf-to-root pin acquisition counted handles without proving one coherent current chain.

## Round-11 disposition — this is a FIXPOINT claim, not another patch
**The interpreter is no longer given a name.** The wrapper runs
`powershell.exe … -Command "& ([scriptblock]::Create([Console]::In.ReadToEnd()))"` and writes
it the IDENTICAL in-memory object that was read through the pinned handle and compared with the
fence (`EXEC_BUFFER_IS_PINNED_READ=1`, `ARGV_PATH_SEPARATORS=0`). No directory entry, drive
letter, DOS device, mount or volume sits between the compared bytes and the executed bytes, so
**no post-run sample is load-bearing** — the transient-rebind class is removed rather than
detected. The component chain is additionally built by relative `NtOpenFile` from a volume-GUID
identity read out of the held handle (`CHAIN_LINKS=7 CHAIN_RELATIVE_OPENS=6
CHAIN_TERMINATES_AT_PINNED_DIR=1`, identity + disposition per link).

Evidence published: both r10 findings reproduced RED against the exact r10 wrapper first
(F1 `FALSE_ACCEPT_UNDER_R10=1` with `R10_TWO_SAMPLE_DETECTOR=CLEAN/1`; F2
`R10_PATH_PIN_COMPLETE=1` with `R10_CHAIN_MIXED=1`), GREEN under r11
(`TRANSIENT_CLOSED_UNDER_R11=2`); `M4_named_channel` flips one constant back to `-File` and the
false acceptance RETURNS (channel proved load-bearing, not decorative); channel contract
conservation MEASURED (`CHANNEL_CONTRACT_CONSERVED=10 SELF_EXCLUDED=1`; `-Command -` was
measured to produce nothing and rejected as a trap); all r10 gates conserved as reject-only.

Lead ran the §13c wrapper VERBATIM from outside the repo: `OUTER_WRAPPER_RC=0`, stderr 0 bytes,
`BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 LEAF_ON_CHAIN_ALL=11 NAMELESS_EXEC_ALL=11
MISMATCHED=0 REJECTED=0`, §13d transcript 45/45 EXACT match.

## The honest residual the implementer discloses (report §5, STATUS item 51)
For the SCRIPT BYTES there is no same-session in-model divergence path left — structural, not
measured. **But `powershell.exe` itself is still located by name from `PATH`**, so an actor who
can change that resolution can have a different program receive the bytes. Neither prevented nor
detected; disclosed as an OUT-OF-MODEL residual with an explicit accept-with-disclosure
recommendation (closing it needs section-handle launching, well outside this scope fence).
**Adjudicate this disclosure**: is it honestly scoped (an explicitly-labelled weaker claim a
harness at this layer genuinely cannot reach further), or is it presented as if it were a
control? Judge whether the interpreter-binary residual is materially different in kind from the
script-byte class you closed.

## Audit contract
1. Confirm `composite_pathproof.py` byte-identical to the r8/r9/r10 commits; re-run the 58-case
   matrix VERBATIM → no regression.
2. Extract the §13c fence AS BYTES per §13d, run it from outside the repository, confirm the
   full transcript reproduces and that the executed buffer is provably the compared object
   (`EXEC_BUFFER_IS_PINNED_READ`, `ARGV_PATH_SEPARATORS=0`) for all eleven blocks.
3. Run §13b VERBATIM: confirm both r10 findings reproduce RED under the published r10 wrapper
   and are GREEN under r11, and that `M4_named_channel` restores the false acceptance (proving
   the nameless channel is load-bearing rather than incidental).
4. The core test: with the name removed from the execution path, is there ANY remaining
   same-session, in-model path on which executed bytes differ from compared bytes? Attack the
   stdin channel (buffer reuse, partial write, encoding, scriptblock construction semantics,
   child reading beyond the buffer) and the relative-open chain. Verify the measured channel
   contract conservation (10 blocks + self-exclusion) is real, not asserted.
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. **If PASS/
   PASS-WITH-NITS, state that this closes the SEC102 Codex flagship slot** — both original
   CRITICALs, R3-F2/F3, the command-word whitelist fixpoint, r7 child-completion, r8
   byte-identity, r9 direct-object binding, and now the r10 temporal/chain class are all closed;
   the remaining items are the owner-ratified interpreter-vocabulary production-gate decision,
   the disclosed residuals (41, 51), and the GLM-5.2 T1 second opinion the Lead dispatches next.
   **If you find another variant of the same executed-byte class, say so plainly — the Lead's
   standing rule is to STOP harness hardening at that point and bring an accept-with-disclosure
   recommendation to the owner rather than open round 12.**

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md`.

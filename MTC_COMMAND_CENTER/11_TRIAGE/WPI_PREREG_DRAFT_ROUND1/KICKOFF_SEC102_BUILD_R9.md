# KICKOFF — SEC102 composite pathproof round 9: §13 wrapper byte-identity (Codex r8, the last finding)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r9. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch ONLY
`SELF_QA_SEC102_R9.md` (new — carry forward the r8 self-QA content and fix the §13 wrapper),
`STATUS_SEC102.md`, the round-9 report `SEC102_R9_REPORT_2026-08-12.md`, and the scoped
`.gitattributes` (add r9 fixtures if any). You MAY touch `composite_pathproof.py` ONLY if the
fix genuinely requires it (it should not — this is an evidence-harness fix). Do NOT touch
`pathscope_prover.py`, block files, RP6/RP7, prereg drafts. Never git checkout/reset/stash any
tracked file.

## Context — commit `3f2c22ca` audited, verdict at `ef2585bb`
Codex r8 audit (`SEC102_CODEX_T1_AUDIT_R8_2026-08-12.md`) CLOSED the r7 child-completion
finding (status/stderr gates confirmed sound; word-bounded MISMATCH detector confirmed).
Both original CRITICALs, the command-word whitelist fixpoint, R3-F2/F3, and the r7 finding
are all closed. The interpreter-vocabulary residual stays disclosed (owner-ratified
production-gate item — do NOT open it). **This one MEDIUM is the last finding before SEC102's
Codex flagship slot closes.**

## The single finding (Codex r8 — MEDIUM, Pattern 10/11)
`SELF_QA_SEC102_R8.md:1660,1899-1900`: the §13 paste-and-run wrapper rewrites every LF-only
PowerShell block to CRLF before execution while claiming byte-for-byte extraction and
execution. It reads the Markdown through newline-translating text I/O and writes each
temporary `.ps1` through `NamedTemporaryFile(..., "w", encoding="utf-8")` without disabling
newline translation. On this Windows host a published block containing 110 LF and zero CRLF
was written with 110 CRLF — written bytes != extracted bytes. The declared instrument is the
published LF byte sequence; the executed instrument is a different CRLF byte sequence. The
current eleven blocks pass under both encodings (Codex re-ran from exact bytes), but the
reusable verifier could falsely certify a future line-ending-sensitive block.

## Required repair (Codex's spec, verbatim intent)
1. Preserve the document's fence bytes through extraction and temporary-file creation
   (binary extraction/write is the clearest route: read the Markdown as bytes, write the
   temp `.ps1` as bytes or with `newline=''`), and assert immediately before launch that the
   temporary script bytes equal the extracted fence bytes.
2. Keep the existing process-status and stderr gates ahead of stdout interpretation —
   unchanged from r8.
3. Under D026, demonstrate RED against the exact round-8 wrapper and GREEN after the repair
   with a harmless line-ending-sensitive sentinel or an equivalent direct byte-identity
   falsification. Record the real commands, status, and output summary; do NOT author an
   attack fixture or reproduce a sensitive body.
4. Re-run all eleven published blocks plus the outer wrapper from the exact published bytes;
   record real per-block child rc + stderr + the byte-identity assertion result.

## Deliverables
`SELF_QA_SEC102_R9.md` (the r8 self-QA carried forward with the §13 wrapper writing exact
bytes + the byte-identity pre-launch assertion + the new RED/GREEN evidence + the eleven-block
re-run) + `STATUS_SEC102.md` (note the r8 LF/CRLF finding closed; keep the
interpreter-vocabulary residual disclosed as the owner-ratified production-gate item) +
`SEC102_R9_REPORT_2026-08-12.md`. Keep the 58-case matrix and all carried fences passing.
If you touched `composite_pathproof.py`, re-derive its size + SHA-256 and justify why
(expected identity: 129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a` — UNCHANGED is the goal).
No commit — the Lead commits and reproduces the matrix + the RED/GREEN + the eleven-block
wrapper verbatim.

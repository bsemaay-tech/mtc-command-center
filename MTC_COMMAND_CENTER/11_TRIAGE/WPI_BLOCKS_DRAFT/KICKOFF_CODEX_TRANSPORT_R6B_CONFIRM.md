# KICKOFF — Codex T0 bounded confirm: transport r6 line-2665 fix

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network.

## Context

Your r6 re-audit (`TRANSPORT_CODEX_R6_AUDIT_2026-08-11.md`) closed R5-F1/F2/F3 and gave a
single "Minimum required repair": correct the `SELF_QA_TRANSPORT.md:2665` byte-identity claim
so it does not assert the whole nine-file set is unchanged when the QA/status docs changed.

The Lead applied exactly that at commit `7e4b5e9f`. The line now reads (in substance): "No
byte of the seven executable/plan transport targets changed in round 6 … the QA and status
documents in the nine-file set did change — they carry the R5-F2/R5-F3 corrections — so the
unchanged claim is scoped to the seven targets, not the whole nine-file set."

## Task — bounded confirm ONLY

1. Read the corrected `SELF_QA_TRANSPORT.md` around line 2665 at commit `7e4b5e9f`.
2. Confirm the claim is now accurate: the seven executable/plan targets are byte-identical to
   round 5 (re-derive their SHA-256 via `git cat-file blob` if you wish), and the text no
   longer asserts the nine-file set is wholly unchanged.
3. Confirm no OTHER byte-identity or "nine-file set unchanged" overclaim remains elsewhere in
   `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`, or `TRANSPORT_R6_REPORT_2026-08-11.md`.
4. Do NOT re-open R5-F1/F2/F3 or F1 (F1 stays honestly OPEN — not an acceptance blocker for
   this Codex slot). Do not re-run the WSL fixture unless you want to; your r6 run already
   reproduced it.

Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK — scoped to whether the line-2665
repair is complete and correct. If accepting, state explicitly that this closes the Codex
flagship slot for the current transport bytes (the Claude flagship audit is separately
required and awaits a Claude session that did not implement these rounds).

Write ONE new file: `TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`.

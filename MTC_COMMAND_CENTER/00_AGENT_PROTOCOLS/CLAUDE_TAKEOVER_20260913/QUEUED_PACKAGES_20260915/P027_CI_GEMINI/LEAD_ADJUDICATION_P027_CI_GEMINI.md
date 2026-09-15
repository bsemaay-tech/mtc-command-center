# LEAD_ADJUDICATION — P027_CI_GEMINI (gemini-3.8-flash-high T2 read-only corroboration of the PR #193 workflow diff and the WP-P0-27 acceptance packet) — 2026-09-15 14:40Z

**Formal outcome: NO COUNTED ATTEMPT YET.** Two attempts, each producing a complete report (sentinel + fenced JSON), were both VOIDED by the wrapper because the Gemini CLI envelope returned `status: ERROR`, `error: "API error (attempt 1): UNAVAILABLE (code 503): No capacity available for model gemini-3.8-flash-high on the server"` *after* the report text. Both reports are recovered from `%TEMP%\gemini_wrapper_failures\` and kept as **SUPPLEMENTAL**; they are concordant. A counted re-run remains due (rule: count only a clean run); the Lead will retry once more in a later quiet window tonight rather than a third time back-to-back (budget: 2× wall clock per call already spent — 663 s + 907 s).

| Attempt | Window | CLI outcome | Recovered report | Native reads (`native_read_audit.py`) |
|---|---|---|---|---|
| 1 | 14:03:11-14:14:26Z (663 s model time) | `launch.exit` exit=1; envelope ERROR 503; conversation `9971f2c0-7a5a-4b20-b613-1e1d265ddb4a`; usage in 427 482 / out 28 972 / thinking 15 961 | 24 000 chars, sha256 `ffe3d23c…`; sentinel present; JSON present — `RECOVERED_RESPONSE_attempt1_VOIDED.md` | 26 reads, 0 outside the packet, 0 failures, all displayed content matches (`NATIVE_READ_AUDIT_attempt1_VOIDED.json`) |
| 2 (prompt annotated "review afresh"; packet unchanged, same `PACKET_SHA256SUMS.txt`) | 14:17:34-14:32:52Z (907 s) | same failure shape; conversation `067c7e5c-9cce-4b56-9571-1f6e7dd12bb1`; usage in 434 481 / out 33 183 / thinking 21 336 | 20 807 chars, sha256 `d24dda17…`; sentinel + JSON — `RECOVERED_RESPONSE_attempt2_VOIDED.md` | 26 reads, 0 outside, 0 failures, all match (`NATIVE_READ_AUDIT_attempt2_VOIDED.json`) |
Both attempts read all 22 REQUIRED files completely (the 176-line after-workflow and the 177-line CI policy in two ranges each) plus the checksum file and both OPTIONAL files. `required_scope_unread: []` in both JSON blocks matches the audits.

## Verdicts (both attempts identical)
- Object 1, the PR #193 workflow diff: **PASS-WITH-NITS** (0 REQUIRED, 2 NITs). A1-A5 CORROBORATED.
- Object 2, the acceptance packet: **PASS-WITH-NITS** (0 REQUIRED, 1 NIT). B1-B6 CORROBORATED; the four day-one gate clauses (a)-(d) each CORROBORATED from the evidence copies; B3 and B5 carry the expected NOT VERIFIED (the 08-25 audit records are outside the packet; the R19 sweep cannot be executed by Gemini).

## Findings — Lead disposition (every citation grepped in the packet)
| # (attempt 1 / attempt 2 id) | Finding | Lead check | Disposition |
|---|---|---|---|
| NIT-WD-01 / F-01 | `research-gates_a3325836.yml:170` installs `ruff==0.16.4` by version string, without `--require-hashes`, unlike the Bridge lock install at `:162`; the claim that it equals `contracts/constraints.txt` is unverifiable from the packet | Line 170 confirmed (`python -m pip install ruff==0.16.4`); `constraints.txt` at `a3325836` does carry `ruff==0.16.4` (Lead `git show`, outside the packet — Gemini's NOT VERIFIED stands as Gemini's) | **CORRECT, NIT.** Recorded as an open nit on PR #193 for its T1 review: before the job could ever become a *required* context, pin Ruff by hash (`--require-hashes` with a hash line) or install it from a hash-locked constraints file. No change to the PR tonight (the PR is the owner's "go" artifact awaiting T1; a Lead edit would re-open it). |
| NIT-WD-02 / F-02 | `:115` `git config --system core.longpaths true` (system scope; `--global` conventional); functional on hosted runners (run 34963602576 SUCCESS) | Confirmed | **CORRECT, NIT, no action** (ephemeral runner; the step ran before checkout as required). |
| NIT-AP-01 / F-03 | Packet E5 cites `CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md`; the packet copy is `sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md` (same Gmail id `1a0a4d879a3c386d`) | Confirmed — the staging renamed the copy and masked the mailbox addresses on purpose | **CORRECT, NIT — applied 14:40Z**: E5 now names both the repository record and the masked packet copy. |

## What the corroboration does and does not establish
- It corroborates, from the copies, every claim the packet makes about runs, rules, states and histograms, and the diff's scope/conventions. It is `SUPPLEMENTAL_UNEXECUTED` and, as of this record, **uncounted**.
- It is **not** the T1 flagship review of the workflow file that `CI_POLICY.md` requires before merge; PR #193 stays open.
- It does not touch the acceptance itself — the owner's act (§7 of the packet).

## Route note (for the ledger)
Same failure shape as 08:43Z and 11:35Z today: complete report, then a CLI-level 503. Tonight it recurred twice in a row on the same packet. The probe before each attempt was OK. Recorded in the route lessons; the counted re-run is queued for a later window (not before 16:00Z).

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).

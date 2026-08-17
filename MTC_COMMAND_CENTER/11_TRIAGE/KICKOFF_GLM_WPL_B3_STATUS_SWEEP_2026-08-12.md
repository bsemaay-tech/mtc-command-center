# KICKOFF — GLM status-vs-bytes sweep of the closed WP-L / B3 records

You are GLM, running unattended with `-PermissionMode acceptEdits`. **Do not ask for approval of
anything; there is no human watching. Never fabricate a green run or any execution result.** You
are source-level only: no harness execution, no host or network access, no git mutation. Verdict
label: `ADVANCE-SUPPLEMENTAL`.

## Mission

Same method as `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`
(a sibling sweep that succeeded today): take closed-record prose, re-derive its checkable claims
from current bytes, and classify each defect found as **stale** (understated/outdated but not
false) or **wrong** (false identity, false attribution, broken cross-reference).

## Scope — EXACTLY these, in this order (bounded on purpose; scope-limited is a feature)

Base: `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/`

1. `EVIDENCE_INDEX.md` (21777 B)
2. `UNIT_CLOSURE_RECORD.md` (7190 B)
3. `INTEGRITY_VERIFICATION_2026-08-10.md` (2976 B)
4. `FINAL_HANDOFF.md` (2637 B)
5. Then, only if context allows: the record/status markdown files at the TOP level of
   `06_B3_REPAIR/`, then `08_PREREG_B3B/`, then `09_TRANSPORT_B3B/` — one directory at a time.

**Stop when context runs low and write the report with an honest coverage boundary** — an exact
list of what you verified and what you did not reach. A partial with honest coverage beats a
timeout that produces nothing. Do NOT recurse into `operator_record/evidence/` blobs or the
runkit directories.

## What to check per claim

- Byte sizes and SHA-256 values quoted in prose → recompute from the file on disk.
- Cross-references (file exists at the cited path; cited line still carries the claim).
- Attribution claims (which model/lane produced what) → against the named run logs' headers.
- Counts and absolutes ("all", "every", "N files") → re-derive where cheap.

## Output — the ONLY file you may write

`MTC_COMMAND_CENTER/11_TRIAGE/WPL_B3_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`

Format: files swept; identities re-derived (match/mismatch); findings by class (stale/wrong) with
exact citations; coverage boundary; closing statement that you ran nothing and mutated no git
state.

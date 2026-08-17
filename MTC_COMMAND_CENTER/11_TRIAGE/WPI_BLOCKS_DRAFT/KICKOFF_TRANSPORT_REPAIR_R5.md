# KICKOFF — Transport round 5: four findings from the two-band Codex r4 audit

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex is auditor of record
and re-audits your bytes, so separation holds. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host contact, no network, no commit. UNIX LF only, zero CR bytes. `transport_runner.ps1`
stays PowerShell 5.1-compatible. Files here carry uncommitted work from prior agents — never
run git checkout/reset/stash on any tracked file.

## Input bytes

Transport nine-file set at commit `12d7bb6e` (round-4 bytes). Close script frozen SHA-256
`29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef`.

## Binding findings — both audits REQUEST_CHANGES

Read both in full; their text binds:
- `TRANSPORT_CODEX_R4_AUDIT_BAND_A_2026-08-11.md` — BA-1, BA-2, BA-3.
- `TRANSPORT_CODEX_R4_AUDIT_BAND_B_2026-08-11.md` — F1.

### F1 (from Band B) — the "closed on the composition" claim is an overclaim
The frozen `env -i` sanitizes the CHILD, but a server-supplied startup file (`BASH_ENV`/
`ENV`) is processed by the outer SSH account shell BEFORE that child runs and can forge the
record. A command inside the same shell string cannot close this.
**Required:** mark F1 OPEN (wording: "inner child closed; outer SSH account-shell boundary
open") and remove EVERY claim that the residual is unreachable or that F1 is closed on the
composition — align report, self-QA §R4-4 + status table, runner comments, wrapper comments,
draft, and any mirrored status text. Do NOT invent a client-side control that cannot act
before the account shell. If you believe closure is achievable, state the exact enforcement
point that acts before account-shell startup and give D026 RED/GREEN through the real
top-level path; otherwise leave F1 honestly OPEN with the boundary named. **A disclosure is
not a control.**

### BA-1 (HIGH) — cleanup armed after a post-creation STOP branch leaves residue
`remote_close_tree_wpi.sh:401` creates the work dir; `:402` can `stop` on any mkdir
diagnostic; the cleanup trap is not installed until `:424`. Codex reproduced
`SCRIPT_RC=3 ... RESIDUE_PRESENT=yes`.
**Required:** capture mkdir rc + diagnostics WITHOUT stopping; on rc 0 arm cleanup BEFORE
adjudicating diagnostics or any later check. Narrow any every-exit-path claim that cannot
hold for a nonzero tool result (lines 58, 404–410, 441; report :126-130; draft :357-360).
Add a D026 RED/GREEN fixture: current bytes leave the residue, repaired bytes remove it and
keep the reasoned STOP.

### BA-2 (MEDIUM) — the claimed second `declare -F` defect is FALSE
Bare no-argument `declare -F` returns rc 0; it does not exit 1 under `set -Eeuo pipefail`.
The round-4 `|| :` is harmless but the "second, independent defect" disposition and the
repeated source comments asserting it are wrong (report :305; `run_p0.sh:29-33`,
`run_ro.sh:23-27`, `remote_setup_wpi.sh:62-66`, `remote_extract_verify_wpi.sh:53-57`,
`remote_close_tree_wpi.sh:114-118`).
**Required:** correct the report and all repeated comments. Keep the guard as explicit no-op
hardening OR remove it — but do not claim a RED the actual command cannot produce. This is
the inverse of the usual failure: an overclaimed DEFECT is still a false evidence claim.

### BA-3 (MEDIUM) — T8 overstates the two prerequisite reason tokens
The classifier returns kind/status reasons (`scp_transfer_did_not_complete` rc-nonzero,
`operation_reported_stop` rc-3) BEFORE the prerequisite-based rc-1 branch; only rc-1 cleanup
yields `cleanup_after_unestablished_prerequisite` / `cleanup_after_earlier_deviation`. The
prose (`WPI_PREREGISTRATION_DRAFT.md:688-691`; `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:570,678`;
report T8) claims every broken-branch `always` failure names one of the two.
**Required:** narrow all mirrored prose to the rc-1 outcomes that actually produce those two
tokens, or change the classifier so the claim becomes true — say which, per file.

## Deliverables

Repaired nine-file set (only what the findings require) + `TRANSPORT_R5_REPORT_2026-08-11.md`
with per-finding dispositions (F1, BA-1, BA-2, BA-3), each with executed D026 evidence where
a byte changed, `PENDING-LEAD-EXECUTION` only where your session truly cannot execute. Do not
weaken any carried fence without a per-change discriminating-power proof (old + new assertion
executed against the same deviant output, both quoted). No commit — the Lead commits.

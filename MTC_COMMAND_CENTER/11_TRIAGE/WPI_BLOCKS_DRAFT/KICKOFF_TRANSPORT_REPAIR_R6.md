# KICKOFF — Transport round 6: two findings from the Codex r5 re-audit (R5-F1 already Lead-fixed)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex is auditor of record.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF only,
zero CR bytes. Files here carry uncommitted concurrent-lane work — never git
checkout/reset/stash any tracked file. Touch ONLY the transport nine-file set +
`SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`, `TRANSPORT_R5_REPORT_2026-08-11.md`,
`_r5_wsl_fixtures.sh`, and the new report. Do NOT touch `WPI_PREREG_DRAFT_ROUND1/` — the Lead
owns those drafts and has already applied R5-F1 there.

## Binding scope

`TRANSPORT_CODEX_R5_AUDIT_2026-08-11.md` — REQUEST_CHANGES. Codex confirmed the BA-1 CODE
repair itself works (it independently reran both blobs through one common subject + argv:
RED retained the residue, GREEN removed it) and the carried fence keeps discriminating power.
Only the evidence provenance and two stale-status items are wrong.

**R5-F1 (HIGH) — ALREADY FIXED BY THE LEAD, do not repeat.** The main draft's derivation
class 5 and remote-launch-domain section, and the successor draft's inherited "cleared launch
domain" clauses, now state the OPEN disposition explicitly. Do not touch the prereg drafts.
Your report should reference this as Lead-applied.

### R5-F2 (HIGH) — the published BA-1 D026 arms do not use the claimed same argv
`_r5_wsl_fixtures.sh:145-148` runs the RED bytes through `RED_SUBJECT` with `RED_BASE` args;
`:155-158` runs GREEN through `GREEN_SUBJECT` with `GREEN_BASE`. So the recorded refusals
(`SELF_QA_TRANSPORT.md:2667-2668`) differ in their path field, falsifying the report's
"same instrument, launch, and argv → delivered bytes the only variable" and "byte-identical
refusal" claims (Pattern 10; D026 requires literal reproducibility as closure evidence).
**Repair:** make `_r5_wsl_fixtures.sh` use ONE common subject pathname and ONE common
EV/RUNID/`WORK_ROOT` argv for both arms, resetting the common tree between runs and replacing
ONLY the subject bytes (RED = pre-repair blob `29b6412a…`, GREEN = repaired bytes). Re-run on
the WSL kernel; replace the BA-1 transcript, the same-argv claim, and the byte-identical-refusal
claim in `SELF_QA_TRANSPORT.md` §R5-1 and `TRANSPORT_R5_REPORT_2026-08-11.md` with the real
output. Keep the carried assertion unchanged — it retained discriminating power.

### R5-F3 (MEDIUM) — final status/evidence still say the committed draft edits are pending
`STATUS_TRANSPORT.md:154-162` (and any matching report/self-QA lines) say the three BA-3
draft edits and the F1 draft mirror "still need to land." They have landed — the Lead applied
BA-1/BA-3 draft edits (commit `37a87046`) and R5-F1 (this round). **Repair:** update
`STATUS_TRANSPORT.md`, the report, and self-QA so they state the draft edits are applied and
committed, citing the commits, and remove `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`'s "pending"
framing (or mark that file superseded — do not delete it, note it as historical).

## Deliverables

Repaired `_r5_wsl_fixtures.sh` + corrected `SELF_QA_TRANSPORT.md` / `STATUS_TRANSPORT.md` /
`TRANSPORT_R5_REPORT_2026-08-11.md` + `TRANSPORT_R6_REPORT_2026-08-11.md` (per-finding
disposition; the BA-1 re-run's real RED/GREEN transcript with the common argv shown). No
commit — the Lead commits and re-runs the BA-1 fixture verbatim.

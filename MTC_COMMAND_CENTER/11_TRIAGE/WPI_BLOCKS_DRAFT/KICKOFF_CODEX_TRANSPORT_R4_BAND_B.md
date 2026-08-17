# KICKOFF — Codex T0 transport round-4 audit, BAND B (F1 residual, descriptive judgement only)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing, no git mutation, no host, no network, and — for this band specifically — DO
NOT construct, run, or reproduce any startup-environment plant. Judge from the frozen bytes
and the report's own description. T0 surface.

## The single question

The round-4 report claims F1 (remote interpreter outside the pinned program domain) is
"closed on the composition," with one disclosed residual: a server-supplied `BASH_ENV`
startup file is read before the first byte of a stdin-delivered script, so `--norc`/
`--noprofile` do not disable it, and a startup file that EXITS could forge the record before
any in-script attestation runs. The report says this is closed ONLY plan-side: the plan/
runner launches the remote interpreter via `env -i` with a complete explicit variable list,
which does not include `BASH_ENV`, so no server-set `BASH_ENV` survives to the frozen child.

Your job is a text-and-bytes judgement, not a reproduction:

1. Read the frozen launch bytes in `run_p0.sh`, `run_ro.sh`, and the runner. Confirm the
   `env -i` invocation is actually what launches the remote interpreter on the frozen path,
   that its variable list is explicit and complete, and that `BASH_ENV` (and any other
   startup-influencing variable: `ENV`, `BASH_ENV`, `SHELLOPTS`, `PROMPT_COMMAND`) cannot
   reach the child through it.
2. Decide whether the report's F1 status wording is honest. "Closed on the composition"
   with a disclosed residual is acceptable ONLY if the residual is genuinely unreachable
   from the frozen plan. If a reachable path remains, F1 is an overclaim — a disclosure is
   not a control (defect pattern; RP7 `ro.status.body` precedent).
3. Check the boundary claim: does the closure depend on the SERVER honoring anything, or is
   it enforced entirely by the client-side frozen command? A closure that needs remote good
   behavior is not a control.

Inputs: `TRANSPORT_R4_REPORT_2026-08-11.md` (§ the F1 residual), `SELF_QA_TRANSPORT.md`
§R4-4 "The one residual this section measures rather than repairs", and the frozen bytes at
commit `99f33c33`. Reference the plant by description; do not rebuild it.

Verdict grammar: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK, scoped to F1 only.
Write ONE new file: `TRANSPORT_CODEX_R4_AUDIT_BAND_B_2026-08-11.md`.

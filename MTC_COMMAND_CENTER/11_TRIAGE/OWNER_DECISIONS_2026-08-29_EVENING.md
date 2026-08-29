# Owner decisions — 2026-08-29 evening session

Recorded by the Lead (Claude Fable 5, evening session). Owner verbatim reply to the six-question
message: **"all defaults / increase the number of paralel lanes to 10"**.

The six questions and the defaults the owner thereby adopted:

| # | Question | Ruling (default adopted) |
|---|---|---|
| 1 | P0-11 residual `run_1`/`run_2`/`run_1_sha256`/`run_2_sha256` receipt names | **Repair 8 — label only** now (same class and scope shape as repair 7), then delta audits, then stage 3 |
| 2 | Bridge fail-closed corrected config | **Yes — prepare a corrected `bridge.yaml` candidate** and present it; the owner approves the exact bytes separately before any build uses it |
| 3 | Migration runbook execution | Owner reads the runbook when he has time; the supervised migration run is **scheduled after P0-11 fully closes**; execution still needs his explicit go |
| 4 | P0-11 v3 second-actor rebuild | **Claude Pro** performs the clean-checkout rebuild (different model family from all Codex builders) |
| 5 | Promotion decision package | **Parked** until the owner has reading time; no lane spends on it |
| 6 | Budget (month ~$5,186 vs ~$800–1,200 ceiling, surfaced again) | **Continue** at current burn; owner explicitly re-confirmed maximum parallel speed |

Additional owner order, same message: **parallel lanes increased to 10.**

## Addendum — later the same evening (owner verbatim: "1. Done / 2. bridge yes / 3. ı have red the files.")

1. **Secondary Codex account re-login: DONE** (Lead probe confirmed "Logged in using ChatGPT").
2. **BRIDGE CONFIG APPROVED:** the owner approves the exact 350-byte
   `BRIDGE_YAML_CANDIDATE_V1.yaml`, SHA-256
   `58f67c8233df8eb92f43be81c09ab665cbe0a17e75b43eccc2f67ad90c040629`, for a later separately
   authorized W10 build targeting schema 4 + paper mode. Per the terms the approval was asked
   under, it takes effect only when the independent candidate audit (lane P21) returns
   CONFIRMED; if P21 finds defects, the candidate returns to the owner instead.
3. **Runbook and promotion package: READ by the owner.** The promotion package still awaits his
   explicit ruling on its single question (approve the report-only rule + vocabulary for the
   four checks; builds nothing; building later is a separate ~18-26 route-hour decision).

Same message thread also ordered parallel design work on P0-13/21/22 (dispatched as drafts,
design-only, serial build chain unchanged).

## Addendum 2 — late evening (owner verbatim: "promotion yes / speed up the godd work. ı want real progress until the morning")

4. **PROMOTION REPORT-ONLY DECISION: APPROVED.** The owner approves the report-only rule and
   vocabulary of `PROMOTION_REPORT_ONLY_DECISION.md`: the four checks (DSR, BH-FDR,
   `robust_final`, positive raw lockbox excess) may be computed and DISPLAYED as
   PASS / FAIL / STOP in a separate report artifact only. Nothing that decides promotion,
   queue placement, or registry status changes. Building the diagnostic display is a separate,
   separately costed future decision (the document's planning estimate: 18-26 route-hours) and
   is NOT authorized by this approval.
5. **Overnight order:** maximum real progress until morning under the standing rules.

## Interpretation notes (Lead)

- Ruling 1 authorizes exactly the repair-7 pattern: rename the published labels that assert
  unperformed acts, sweep the class by shape, rerun the existing probe, full tests green,
  one commit. Nothing beyond the label class.
- Ruling 2 authorizes PREPARATION only. The candidate file and its per-key rationale go to the
  owner; his approval of the exact bytes (hash-pinned) is a separate future decision, and the
  build lane starts only after that approval.
- Ruling 6 is recorded as the explicit owner answer to the standing budget flag
  (model-routing ceiling); the flag remains open as a fact, closed as a question.

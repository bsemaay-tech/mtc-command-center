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
| 6 | Budget (CodeBurn banner at evening session start read $5,186.30 month spend vs the ~$800–1,200 owner ceiling; the Lead measures no USD itself) | **Continue** at current burn; owner explicitly re-confirmed maximum parallel speed |

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

## Addendum 3 — 2026-08-30 ~06:00 (owner verbatim: "bridge v2 yes, papers a, p012 hold" / "continue working with 10 lanes. it's not morning yet")

6. **BRIDGE CONFIG V2 APPROVED — exact bytes.** `BRIDGE_YAML_CANDIDATE_V2.yaml`, 324 bytes,
   SHA-256 `a96fecd10d6966c3e93a829ec4d75869a0851f0136a06e85ab45c255ee0f5842`, P21b-CONFIRMED.
   With the design CONFIRMED and the bytes approved, the fail-closed BUILD lane is authorized
   under the standing ask-10 terms: build + tests + PR only; NO deployment to any host.
7. **P0-20 papers: option (a).** The owner's words were "papers a"; option (a)'s content —
   ONE narrowing edit, relabel falsifier #5 a unit-level probe with injected `trail_atr`,
   nothing else — is the Lead's question wording (sourced from N63-F1's minimal correction),
   which the reply adopted.
8. **P0-12 design: HOLD** at its round cap until P0-11 v3 lessons fold in.
9. Ten concurrent lanes remain the standing order.

## Addendum 4 — 2026-08-30 morning (owner answered four questions, all recommended defaults)

10. **Dashboard scope EXTENDED:** the bridge build may repair the three dashboard files
    outside the original design write-set (`bridge/static/app.js`,
    `bridge/static/help_map.json`, `tests/test_dashboard_static.py`) so the dashboard matches
    the fail-closed config. Same branch/PR, auditable.
11. **v3 merge cadence:** after the owner signs, the whole P0-11 package merges to master as
    ONE unit the same day (signature -> final audit pass -> PR -> merge).
12. **Gemini launcher fix AUTHORIZED:** one-line ignore-list addition for the `.impeccable`
    plugin-cache churn in `Invoke-GeminiProReadOnly.ps1`'s integrity check; edit recorded.
13. **Small items:** papers' three open MEDIUMs stay recorded (folded into P0-20's build
    phase later); a 30-minute OpenCode auto-approve investigation is authorized.

## Interpretation notes (Lead) — these notes refer to the ORIGINAL six-question table rows
above (its rows 1, 2 and 6), not to the addendum numbering (6-9); addendum 3's rulings
supersede row 2's "preparation only" edge for the bridge (the bytes are now approved and the
build authorized) and answer row 6's budget question for the night.

- Ruling 1 authorizes exactly the repair-7 pattern: rename the published labels that assert
  unperformed acts, sweep the class by shape, rerun the existing probe, full tests green,
  one commit. Nothing beyond the label class.
- Ruling 2 authorizes PREPARATION only. The candidate file and its per-key rationale go to the
  owner; his approval of the exact bytes (hash-pinned) is a separate future decision, and the
  build lane starts only after that approval.
- Ruling 6 is recorded as the explicit owner answer to the standing budget flag
  (model-routing ceiling); the flag remains open as a fact, closed as a question.

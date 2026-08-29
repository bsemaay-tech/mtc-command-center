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

## Interpretation notes (Lead)

- Ruling 1 authorizes exactly the repair-7 pattern: rename the published labels that assert
  unperformed acts, sweep the class by shape, rerun the existing probe, full tests green,
  one commit. Nothing beyond the label class.
- Ruling 2 authorizes PREPARATION only. The candidate file and its per-key rationale go to the
  owner; his approval of the exact bytes (hash-pinned) is a separate future decision, and the
  build lane starts only after that approval.
- Ruling 6 is recorded as the explicit owner answer to the standing budget flag
  (model-routing ceiling); the flag remains open as a fact, closed as a question.

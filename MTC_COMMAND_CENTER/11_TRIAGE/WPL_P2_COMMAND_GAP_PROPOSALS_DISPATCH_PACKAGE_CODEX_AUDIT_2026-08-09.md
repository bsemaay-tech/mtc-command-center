# WP-L P2 dispatch package — Codex fourth-account audit (2026-08-09)

> **SUPERSEDED (2026-08-09):** a later candidate-source audit found and Lead reproduced an incorrect
> no-rebind-field expectation missed by this audit. This historical verdict cannot authorize dispatch of
> the repaired package. Fresh GLM and Codex re-audits are required. See
> `WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_POST_ACCEPTANCE_REPAIR_2026-08-09.md`.

## Verdict

**PASS-WITH-NITS. Zero required findings.** Fresh `gpt-5.6-sol` xhigh review accepted the audited Claude
repair prompt plus byte-exact Lead checklist as a safe future proposal-repair dispatch package.

This accepts documentation contracts only. It does not accept rejected proposal `779bd038`, consume a
proposal repair round, authorize a secondary implementation, extract scripts, or grant host/trading/
deployment authority.

## Execution and reproduction

The audit used the isolated fourth Codex subscription route through `Invoke-CodexForClaude.ps1`, exact
model `gpt-5.6-sol`, xhigh effort, fresh ephemeral session, and read-only sandbox. It completed in 446
seconds. Final `git status --short` was empty.

Executed checks included:

- read governing `AGENTS.md`, `START_HERE.md`, and `AI_RULES.md`;
- confirmed candidate/spec/prompt/checklist commits with Git;
- proved prompt byte-equal to `fbb5ca61`, checklist byte-equal to `456968bb`, and spec byte-equal to
  `9ac60ac6`;
- reproduced candidate connection-based invariant API, `/222`, exact `0555`, manifest binding,
  rollback/no-rebind behavior, and first-start systemd anchors;
- inspected rejected `779bd038` only as RED baseline;
- ran `git diff --check`; no proposed script, host, network, service, reboot, rollback or mutation ran.

## Optional nit

Checklist line 87 could explicitly say an equivalent Python subprocess fixture must exercise the real
candidate predicate/tool under stub control, not reimplement its logic. This is the same optional wording
nit already recorded by GLM-5.2. Existing D026 and non-execution=`BLOCK` language prevents false
acceptance, so the nit remains unapplied to preserve byte-exact accepted checklist `456968bb`.

## Non-executing precursor

The first fourth-account attempt returned `BLOCK` before file reads because `do not run host commands`
was interpreted as forbidding local read-only inspection. It made no edit and produced no package
finding. A fresh corrected prompt explicitly allowed local read-only Git/file commands and forbade remote
host plus mutation; only that second session supplies the accepting verdict.

## Next steps

1. At first exact Claude account capacity, run the audited prompt as proposal repair round 1/3.
2. Freeze the returned one-file diff before another agent touches it.
3. Lead executes byte-exact accepted checklist `456968bb` and preserves genuine RED/GREEN evidence.
4. If Lead accepts the repaired proposal, begin fresh canonical protected-scope audits; this package audit
   is not that future proposal audit.
5. Keep all host, budget, credential, broker/TESTNET, ARM/order, WP-V/KVM2/master/old-payload, economic,
   and `C:\PGRK` holds unchanged.

# Claude counterpart prompt — repair WP-L P2 command-gap proposals (2026-08-09)

You are the counterpart flagship implementer. Perform one bounded documentation repair in
`C:\LAB\Tradingview_LAB_CLEAN`.

## Frozen authority

- Accepted repair-spec commit: `9ac60ac652f4a221316465cdbc24516aa391f5ce`
- Specification:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_2026-08-09.md`
- Rejected source proposal commit: `779bd038957a192db47ff7ad68eb51304a2fba46`
- Reproduced findings:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md`
- Candidate authority: `2ce41e34bceb599d80af24c5c33d835820ec321b`
- Spec audit:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_AUDIT_2026-08-09.md`

Read `AGENTS.md`, the specification, the reproduced-findings audit, the rejected proposal, and only the
candidate source anchors named by the specification/audit. Treat the live branch HEAD as continuity only;
the accepted specification above is the repair contract.

## Writable scope — exact

Edit only:

`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`

Do not edit product, deployment, runtime, tool, test, schema, prompt, handoff, or AI-memory files. Do not
stage, commit, push, stash, reset, checkout, restore, or rewrite Git history. Do not contact any host, use
SSH, transfer or run scripts, load credentials, construct a broker, use TESTNET, ARM, place orders, touch
WP-V/KVM2/master/old payloads, or take economic action. Do not edit, supersede, or reopen `C:\PGRK`.

These repository files may contain work from other agents. Never discard or rewrite unrelated changes.
If the exact writable file is already modified before your edit, stop and report the observed status.

## Required repair

Implement the accepted specification RP0-RP6 exactly in the one proposal document. The result remains a
proposal/design artifact, not host authorization and not extracted runnable files.

1. RP0: replace fixed evidence-log destinations with the preregistered run-ID, operator-captured
   pre-allocation transport evidence, canonical non-link parent check, one-shot `mkdir -m 0700`, and
   create-once leaf design. Every path/process/systemd/pipeline predicate must have true, false, and
   could-not-evaluate outcomes; the third is STOP. Include the six required RED/GREEN falsifications.
2. RP1/B3: require exact `0555 root:root`, candidate `/222` any-write-bit semantics, an honestly bounded
   or explicitly budgeted sweep, candidate/payload manifest binding, exact ancillary path checks, and
   fail-closed reads. Include all required fixtures and also one ancillary-path mode/owner drift fixture.
3. RP2/C1: C1 MUST remain explicitly BLOCKED. Remove/quarantine any runnable stop block or wording that
   implies readiness. State both open gaps: the exact successful shutdown tuple and the independently
   accepted safe active-writer invariant baseline. Preserve the future requirements only as non-runnable
   design. Include a deferred explicit C1 falsification list that becomes mandatory if both gaps close.
4. RP3/C2: retain the two preregistered branches without post-reboot branching. Scenario A is terminal;
   Scenario B depends on RP2's baseline method. Require real pre-mutation invariant baselines and exact
   post-reboot equality, exact systemd token/status handling, exact mask target, and all required
   falsifications. Do not turn blocked dependencies into commands.
5. RP4/C3: use a read-only `sqlite3.Connection`; restore through the exact primitive
   `src_conn.backup(dst_conn)` into a fresh destination; run checks on the restored connection; call
   `collect_invariants(restored_connection)` and candidate `invariants_hash(invariants)`; require protected
   equality, identity separation, sidecar absence, and external manifest-file SHA. Preserve both success
   and failure evidence; never delete partial artifacts. Include every required RED/GREEN case.
6. RP5/C4: enforce rollback-manifest object-and-link no-clobber, accepted C3 evidence, exact starting
   state, a mutation-free dry run, then one stop+mask-only invocation. Pass no rebind SHA arguments and
   state explicitly that the resulting rollback-manifest no-rebind fields must be empty. Require exact
   mask/link/status/process outcomes and fresh post-rollback protected-invariant equality. Filename/size
   equality is diagnostic only. Include every required RED/GREEN case.
7. RP6/C5: keep only the authority statement. Add no executable credential, network, broker, alternate
   start, TESTNET, ARM, or order procedure.

The repaired document must visibly mark which blocks are executable proposals and which are blocked
future design. No acknowledged assumption may remain on a PASS path. Do not claim acceptance, closure of
`C:\PGRK`, permission to extract scripts, exact 50-hour reproducibility, or server readiness.

## Self-QA and response contract

Before returning:

1. Run `git diff --check -- MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`.
2. Run `git status --short` and prove only the exact writable file changed during your task.
3. Re-read the edited document against RP0-RP6 and F1-F9.
4. Re-check every candidate API/mode/status/hash claim against the exact named candidate anchors.
5. Do not execute proposed shell/Python blocks on a host. Local static inspection only.

Return a compact implementation report containing: changed file, RP0-RP6 mapping, self-QA commands and
results, any unresolved blocker, and the exact final `git status --short`. Do not claim PASS; the Lead and
fresh auditors own acceptance. This is repair round 1 of at most 3 for this new proposal-repair cycle.

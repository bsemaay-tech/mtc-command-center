# Codex WP-L P2 staging implementation kickoff (2026-08-09, evening) — self-contained

Authorized test-infrastructure verification work on a private, disposable staging VM the team owns
(`GATEA-STAGING`, Ubuntu 24.04). Everything runs against a deliberately credential-free, DISARMED,
loopback-only service installation. No live trading system, no real credentials, no third-party
targets are involved.

Do NOT read `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`, or any `GATE_A_A*` file.
This file plus the three named documents below carry all required context.

## Authority (complete)

1. `11_TRIAGE/WPL_PHASE2_DISPATCH_PROMPT_2026-08-09.md` — owner authorization for WP-L Phase 2 +
   WP-I staging verification on the retained host; every hard constraint there binds.
2. `11_TRIAGE/WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` — the command designs are ACCEPTED
   at commit `4c0d5fc5` (chain of custody inside).
3. `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` at `4c0d5fc5` — the accepted designs.
   Blocks marked BLOCKED stay blocked (C1, C2 baseline-dependent scenarios, C5).

## Your unit

1. Extract the ACCEPTED executable proposal blocks (by `BLOCK-ID`, documented convention) into a
   frozen run-kit; record each block's identity (must equal the §8.1 table); checksum the bundle.
2. Preregister the run (RUNID, expected hashes) per the RP0 design; transfer the kit to the
   staging host over the recorded SSH route; verify remote hashes before anything executes.
3. Execute in order with first-FAIL stopping and the RP0 evidence contract: B3 (read-only
   permissions admission) first; then only the non-BLOCKED read-only checks. On the Linux host,
   also run the one BLOCKED-on-Windows local fixture R4-5 (dangling restore-destination link) in a
   fresh temp root — it needs only real symlinks, no service interaction — and record RED/GREEN.
4. Any mutating step (service stop, reboot, rollback rehearsal) requires the per-step
   prerequisites in the accepted designs to hold, including their preregistered baselines; where a
   baseline method is BLOCKED, the step stays unexecuted — do not improvise closures.
5. Checkpoint evidence + a concise record to `11_TRIAGE/` after each stage (commit exactly the
   files you create, branch `feature/donchian-crypto-ladder`, push). First FAIL: stop, preserve
   evidence, record, and end the unit with a handoff note in your final commit.

## Boundaries (unchanged, binding)

Bridge stays DISARMED, credential-free, loopback-only (`127.0.0.1:8790`). Forbidden: credential
loading, ARM, orders, broker/exchange contact, TESTNET/mainnet, master merge, WP-V/KVM2, deleting
the old payload archive, host reprovisioning. Evidence no-clobber per RP0. Book actual hours at
unit close per the ratified ledger (baseline 20.5 h used / 29.5 h remaining).

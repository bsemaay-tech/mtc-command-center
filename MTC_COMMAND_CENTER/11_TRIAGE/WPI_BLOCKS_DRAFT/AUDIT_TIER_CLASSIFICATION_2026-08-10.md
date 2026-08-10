# Gate-1 audit-tier classification — WP-I block set (Lead, 2026-08-10)

Per `AGENTS.md` §AUDIT TIER POLICY — PERMANENT DEFAULT, recorded before the next audit
dispatch.

| Artifact | Tier | Reason |
|---|---|---|
| `RP6-P0.sh` | **T0** | run-kit script intended to execute on `GATEA-STAGING` |
| `RP7-WPI-RO.sh` | **T0** | same |
| `run_p0.sh`, `run_ro.sh`, `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh` | **T0** | ssh-stdin scripts executing on the staging host |
| `transport_runner.ps1`, `TRANSPORT_PLAN.tsv` | **T0** | drives host contact; carries the op list |
| `WPI_PREREGISTRATION_DRAFT.md` and successor prereg | T2 (identity escalations to T1 per policy) | prereg text |
| Kickoffs, status notes, this file | T3 | process artifacts |

**T0 contract:** two independent fresh flagships — `claude-opus-5` xhigh + `gpt-5.6-sol`
xhigh — accepting verdicts on the FINAL bytes; max 3 repair/re-audit rounds per cycle.

## Slot ledger (updated as audits land)

- RP7 round 1: `claude-opus-5` **xhigh** fresh (`--no-session-persistence`, dispatch
  command recorded in the session transcript and kickoff) → BLOCK 13. Round counts;
  effort attested by the dispatching Lead (report text omitted it).
- RP7 round 2 re-audit: `claude-opus-5` xhigh fresh — IN FLIGHT.
- RP7 Codex xhigh slot: NOT YET RUN — dispatch on green round-2 bytes.
- RP6-P0 C13 cycle: GLM implement → Codex `gpt-5.6-sol` **high** audit (BLOCK 3) →
  Claude Pro repair → Codex **high** re-audit IN FLIGHT. The high-effort Codex rounds
  predate this classification; they stand as cycle-closure checks. Both T0 acceptance
  slots (`claude-opus-5` xhigh + `gpt-5.6-sol` xhigh, fresh sessions) run on the final
  RP6-P0 bytes before freeze.
- Transport set: no audit yet. First audit dispatches directly at the T0 contract.

Earlier non-flagship rounds (GLM reviews) are supplemental detection per the roster
rules, never acceptance.

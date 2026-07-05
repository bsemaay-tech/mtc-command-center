# LIVE TRADING GATE

> Status: DRAFT.
> Track: SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
> Purpose: convert "live trading is forbidden" into "live trading is gated."
> Binding status: not binding until Baris signs this document.

Live trading remains blocked. No AI may recommend going live, imply live
readiness, or treat this gate as satisfied. Every item below requires dated
evidence for one specific strategy and explicit Baris sign-off.

The SYSTEM_TEST_ONLY vertical slice satisfies none of these requirements and
can never be cited as live-readiness evidence.

## Hard Preconditions

All items are required. There is no partial credit.

1. Strategy robustness:
   `robust_final = 1`, at least 30 lockbox trades, positive excess alpha versus
   buy-and-hold, CPCV/PBO reports, and multi-window stability, regenerated on a
   frozen tagged commit.
2. Reference lock:
   frozen parameters, tagged commit, hashed signal file, and deterministic
   rerun reproducing the same signal file.
3. Parity proof, if Pine participates in monitoring or signaling:
   dated artifact, at least 99 percent signal-flag agreement over full history,
   and trade-list diff within the approved tolerance. A parity artifact older
   than the last code change on either side is void.
4. Paper soak:
   pre-registered plan, immutable start date, 8 to 16 weeks minimum and at
   least 30 new forward trades, zero unexplained reconciliation breaks, and no
   restarted window unless a new plan is approved.
5. Testnet proof:
   executor or bridge soaked on exchange testnet, including duplicate-signal
   injection and kill-process-mid-open-position restart/reconcile behavior.
6. Reconciliation:
   daily three-way diff across expected signals, bridge or executor log, and
   exchange statement throughout the paper/testnet period. Unexplained orphan
   count must be zero.
7. Kill switch:
   three layers documented and drilled with timing evidence: signal source
   pause, bridge/executor halt, and API key revocation. Full flatten target:
   under five minutes. An un-rehearsed kill switch is not a kill switch.
8. Idempotency:
   every payload carries an idempotency key and dedup behavior is proven by
   deliberate duplicate delivery.
9. Failure drills:
   documented behavior for duplicate signal, dropped signal, malformed payload,
   wrong environment, and exit-with-no-position.
10. Capital limit:
    dedicated sub-account funded with pilot capital only. The hard number is
    signed by Baris before any live pilot.
11. Key security:
    withdrawal disabled, IP restricted, least privilege permissions, rotation
    schedule, and secrets stored outside the repo.
12. Incident response:
    one-page runbook for reconciliation break, exchange halt, runaway-signal
    alarm, open-position emergency, and broker/exchange support path.
13. Monitoring:
    MTC Command Center may render read-only heartbeat, position summary, and
    last reconciliation status. It must not send orders or mutate execution
    state.
14. Human approval:
    explicit written Baris sign-off on this checklist, per strategy and per
    capital increase. Never AI-recommended, never implied.

## Standing Rules

- Dashboard visibility is not gate evidence.
- Scorecard scores are not live-readiness evidence.
- Board/model consensus is not live-readiness evidence.
- SYSTEM_TEST_ONLY artifacts are not strategy evidence.
- Any attempt to bypass this checklist is a stop-everything incident.

## Per-Strategy Sign-Offs

None exist.

## Signature

- [ ] Baris accepted this draft gate on: ____________


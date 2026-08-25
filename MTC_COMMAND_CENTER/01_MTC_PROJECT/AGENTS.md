# MTC build stage rules

This stage owns MTC V2 Pine/Python build work and its parity-first integration. Pine logic, MTC
strategy behavior, parity files/corpora, and TradingView parity are protected: no change without
explicit owner approval naming the exact behavior and files.

- MTC V2 is the active build target; V1 and the legacy backtest engine are reference-only.
- Keep Pine and Python layers behaviorally aligned. Never recapture or weaken a golden to make a
  change pass. Do not advance to the next layer until current-layer parity passes. A mismatch is
  evidence to diagnose, not a reason to alter the oracle silently.
- MTC-Engine Validation is an additive shortlist-only funnel in `02_MTC_BACKTEST`: reuse
  `MTCRunner`, `src/config/profiles/light_risk.py`, and one manual `SignalPlugin` per promoted
  producer. It is not a new engine, live trading, or permission to edit `MTC_V2.pine`.
- Standalone Pine producer adapters may be used for raw-signal parity; final controller integration
  remains a separate gate.
- Pine is physically one file. `LIB_*` names are logical module families, not separate Pine
  libraries; inputs, strategy declaration, orchestration, and final wiring stay in the main file.
- Do not commit generated report trees or root parity bridge outputs unless the exact evidence
  refresh is authorized. Update `MTC_V2_PORTABLE_HANDOFF/` only deliberately.
- `mtc_backtest/` is legacy and not the MTC V2 parity target.
- Build means changing code; validate means execution/test/parity/audit. When validation is outside
  scope, do not run or imply run commands.
- Add no unrequested feature, redesign, duplicated logic, or second state owner. If behavior is
  ambiguous, do not invent it—record the ambiguity and block. Avoid broad refactors without tests.
- Use targeted case/symbol reads. User-supplied TradingView exports and compile output follow the
  canonical intake protocol; do not fabricate or reconstruct them.
- Any regression claim requires D026 RED/GREEN execution. Note parity risk explicitly in G4 and
  route the accepted current state into this stage's capped handoff.

# Bugs Found

- MISSING: sample sufficiency - Only 17 prior best-set trades; high PF does not satisfy enough-trades gate.
- POSSIBLE_EXECUTION_BUG: same-bar entry/exit ambiguity - Stop/target logic can evaluate full OHLC of the entry bar; this is deterministic but not market-sequence-realistic.
- IMPLEMENTED_DIFFERENTLY: exit-before-entry ordering - Previous code generally advances index after exit, but no shared invariant test existed.
- POSSIBLE_EXECUTION_BUG: gap fill realism - Prior code does not consistently distinguish stop trigger price from next open gap fills.
- IMPLEMENTED_DIFFERENTLY: trigger price vs next open fill - Most candidates enter next open; Crabel enters trigger price on same bar.
- POSSIBLE_EXECUTION_BUG: intrabar high/low ordering - Stop-first rule is conservative but not proven against real intrabar sequence.
- IMPLEMENTED_DIFFERENTLY: asset silently skipped - Previous harness logs some asset failures but continues.
- POSSIBLE_EXECUTION_BUG: gross vs net confusion - Previous reports emphasized compounded net return values that became numerically misleading.
- IMPLEMENTED_DIFFERENTLY: drawdown calculation - Compounded drawdown is sensitive to extreme compounding; non-compounded return is included here.
- POSSIBLE_EXECUTION_BUG: compounding overflow - Compounding status: SAFE.

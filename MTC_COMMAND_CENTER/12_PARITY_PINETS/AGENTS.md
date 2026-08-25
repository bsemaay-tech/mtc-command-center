# PineTS parity stage rules

This stage owns PineTS parity tooling/corpora outside the MTC-project-local cases. Parity artifacts,
oracles, tolerances, and behavior are protected; explicit owner approval is required before changes.

- Never quote a corpus number repository-wide until its exact implementations/versions, generation
  date, data/case scope, oracle, tolerance, and executed/skipped/not-comparable counts are established.
- Separate reused evidence from newly executed evidence. Missing dependencies or inability to run is
  BLOCK/not comparable, never acceptance.
- Do not recapture goldens or weaken tolerances/assertions to make a change pass. Carried fences change
  only with same-deviant discriminating-power proof.
- A regression claim requires D026 RED on pre-fix/equivalent mutation and GREEN on fixed behavior.
- Keep Pine, Python, PineTS, and TradingView identities distinct. Agreement between two does not prove
  the others.
- Parity code changes are protected and default to the highest applicable tier; audit against the
  frozen SHA and real suite.

# MTC Sandbox Architecture Review

## 1. Should all strategies be put into MTC_V2 at once?
**Decision:** NO.
**Antigravity Assessment:** Strongly agree. Putting untested candidates into MTC_V2 violates production isolation rules and will pollute the core engine with unverified state logic.

## 2. Should each strategy be standalone first?
**Decision:** YES.
**Antigravity Assessment:** Agree. An isolated sandbox (`standalone_pine_visual_review.pine`) guarantees that a strategy's edge is evaluated independently before integration complexities are introduced.

## 3. Is using MTC money management through a shared harness reasonable?
**Decision:** YES.
**Antigravity Assessment:** Agree, provided the harness remains external to `MTC_V2.pine`. The shared harness should only accept boolean pulses (long/short) and handle sizing/exits identically to Python to prevent duplicated maintenance.

## 4. What are the risks of copying MTC risk logic into standalone Pine?
**Antigravity Assessment:** Code drift is the primary risk. If MTC risk logic (e.g., ATR calculations, partial exits) is copied, any updates to MTC_V2 will instantly desync the sandbox. The sandbox should ideally use a minimal representation of MTC risk or rely exclusively on the Python harness for complex money management parity.

## 5. What minimal harness should be used for manual visual review?
**Antigravity Assessment:** The visual review harness must be a standalone Pine file that plots ONLY the raw setup, entry pulse, exit pulse, invalidation levels, and standard stop/target lines. It must NOT contain trade execution logic (`strategy.entry`, `strategy.close`) unless necessary for TradingView visual tester rendering.

## 6. What should be required before real MTC integration?
**Antigravity Assessment:** Agree with Codex's list. Specifically:
1. Manual visual review approval.
2. Source-faithful rule specification.
3. Strict Pine/Python signal parity.
4. Repaint elimination.
5. Verification of proxy data availability across target assets.
6. Owner's explicit approval.

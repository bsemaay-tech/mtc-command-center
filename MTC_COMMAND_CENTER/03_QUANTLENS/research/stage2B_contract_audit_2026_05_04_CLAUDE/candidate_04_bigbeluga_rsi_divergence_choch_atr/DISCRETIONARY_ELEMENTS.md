# DISCRETIONARY_ELEMENTS — BigBeluga

The strategy is **indicator-defined**, so most logic is mechanical. Discretionary elements are minimal.

| Element | Mechanical? | Safe approximation | Previous LLM choice |
|---|---|---|---|
| Pivot detection | Fully | `pivothigh(10,10)` with confirmed-shift | DANGEROUS (centered rolling = leak) |
| RSI divergence | Mechanical per Pine | Replicate Pine pivot-pair comparison | DANGEROUS (rolling-min substitute) |
| Direction latching | Mechanical | Boolean state machine | MISSING (stateless) |
| ATR trailing | Mechanical | Chandelier from extreme since entry | MISSING (static stop) |
| Ladder TPs | Mechanical | Three TPs at ATR×{2,4,6} | MISSING (single 1×ATR target) |
| Multi-asset application | None (asset-agnostic) | OK | OK |

## Producer / filter / process classification
- **Producer candidate** with FSM (latched direction).
- Should be tested with full indicator-faithful re-implementation. Until then, all Stage-2 numbers are misleading.

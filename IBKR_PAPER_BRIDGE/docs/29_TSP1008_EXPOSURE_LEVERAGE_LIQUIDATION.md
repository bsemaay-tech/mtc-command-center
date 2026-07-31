# TS-P1-008 Exposure, Leverage, and Liquidation Controls

Status: opt-in schema-v8 / snapshot-v3 capability. Default schema remains v4.
No operational migration or runtime activation is included.

The v3 position row retains `positionValue`, reported leverage, and
`liquidationPx` from the same Hyperliquid `clearinghouseState` observation as
equity and margin. Mark is derived as `position_value / abs(size)`. Missing,
nonfinite, negative, zero-for-nonzero, or wrong-side evidence fails closed.

Owner policy: symbol gross 20% of equity; portfolio gross 40%; wallet margin
utilization 25%; effective leverage 1x; minimum directional liquidation
distance 15%. Values are configuration-backed and hashed into an immutable
policy version. Offsetting and foreign positions are never netted away.

Gates run before the existing `NO_OPEN_POSITION` gate, which remains active.
Any failure vetoes and DISARMS before submission. ARM checks current v3 wallet
risk without projecting an order. Recovery requires a fresh safe checkpoint
and explicit human ARM. No automatic broker mutation is added.

Schema v8 adds no business-evidence table. It preserves v7 objects, stores v3
rows in immutable checkpoint JSON, and binds the exposure-policy version into
the canonical hash. v1/v2 evidence remains retained but cannot authorize v8.

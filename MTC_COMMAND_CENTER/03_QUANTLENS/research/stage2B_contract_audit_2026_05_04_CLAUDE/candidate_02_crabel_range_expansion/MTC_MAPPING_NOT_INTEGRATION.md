# MTC_MAPPING_NOT_INTEGRATION — Crabel

## MTC role
**SIGNAL_PRODUCER_POSSIBLE** but **AWKWARD**:
- Crabel is session-anchored with **pre-placed stop orders at open**, not bar-close producer.
- MTC's typical model is "bar-close → signal → next-bar entry". Crabel needs "session open → place two pending stops → walk intraday".
- Better MTC fit: a **pending order owner** module that runs once per session, not a continuous producer.

## Producer raw signal definition
On session open (with prior day NR7 confirmed):
- `pending_long_stop = O + Stretch * mult`
- `pending_short_stop = O − Stretch * mult`

## Non-repaint requirements
- Stretch and NR pattern computed using only prior-session data → safe.
- Stop fills determined intra-session → must be replayed identically in Python and Pine.

## Stateful transform
- Per-session state machine: `awaiting_fill → filled_long | filled_short | session_end_no_fill`.
- Once filled, normal SL/TP logic applies.

## Filters needed
- NR pattern (mandatory).
- Optional EMA200 trend, news blackout, half-day skip.

## SL/TP compatibility
- Initial SL = opposite pending stop level. Direct fit.
- TP options: 1×Stretch from entry, prior-day H/L, none. All compatible.
- Time stop = session close. Compatible if MTC supports session-end exit.

## UI complexity
- Medium: one pane shows Stretch, two horizontal pending levels, NR-flag indicator.

## Parity risks
- The intra-bar fill order (which stop hits first) is the main parity risk. Use minimum 5m bars to disambiguate; prefer 1m for fill-quality.

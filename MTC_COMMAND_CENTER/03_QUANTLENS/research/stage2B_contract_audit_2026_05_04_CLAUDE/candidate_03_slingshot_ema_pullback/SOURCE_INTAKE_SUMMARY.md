# SOURCE_INTAKE_SUMMARY — Slingshot 4-EMA-of-Highs Pullback

## Source files
- `06_QUANTLENS_LAB/00_INBOX_REPORTS/3 Mayıs/2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake.md` (canonical — Codex's batch run also pointed here)
- AUDITED card pointed here too. CLEAN candidate card incorrectly cited `-JyH5PAJ4-Y` (Nick Schmidt). Inconsistency between AUDITED and CLEAN provenance flagged.

## Source URL
- https://youtu.be/c7ZSb2wNcOc (Icarus to Atlas / Slingshot / Fishhook)

## Speaker / context
- Anonymous educator (intake gives `UNKNOWN_CHANNEL`). Discusses three setups: Slingshot (codable), Fishhook (catalyst-dependent), and Icarus/Atlas (auction-level structural framework).

## Native market
- Equities (and earnings-gap-friendly names). Crypto adaptation is **explicitly marked exploratory** in the intake.

## Native timeframe
- Daily primary; optional 1h/4h/weekly.

## Core thesis (intake §5.1)
- Slingshot is a **pullback resumption**, NOT a breakout.
- Sequence: prior strength → pullback / weakness → tightening / lower-risk area → fresh reclaim of EMA(high,4) → trend resumption.
- The phrase the speaker used: "strength after weakness".
- Speaker explicitly warns: "simply being above the 4-EMA-of-highs is not enough" — context (prior strength + a real pullback) is required.

## Stated indicator math
- `ema_high_4 = EMA(high, 4)`.
- Fresh signal: `close > ema_high_4 today` AND `close[1] <= ema_high_4[1]`.

## Stated objective rule (paraphrased intake §5.4)
- Prior-strength filter: `close > SMA50` OR `close > SMA200` OR 20d return > 10% OR near 20/60-day high.
- Pullback filter: at least one of last N bars closed below `ema_high_4`; depth not catastrophic; price still above structural support / HTF trend filter.
- Trigger: close crosses above `ema_high_4`.
- Entry: next bar open.
- Initial stop: trigger-bar low / pullback-window low / ATR(14) stop / structural support.
- Exits: close below `ema_high_4` / ATR trail / fixed R / time stop.

## Intake's own warnings
- Designed for equities; crypto test is exploratory.
- Raw cross alone over-triggers; needs context.
- Universe / volume / RS filters not specified in transcript — must be added.

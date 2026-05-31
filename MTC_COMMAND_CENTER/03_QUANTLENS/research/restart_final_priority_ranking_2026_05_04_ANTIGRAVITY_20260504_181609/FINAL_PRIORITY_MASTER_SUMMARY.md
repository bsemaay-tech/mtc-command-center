# Final Priority Master Summary

This document synthesizes the final rankings for the top QuantLens candidates. The goal is to move the highest quality, most testable, and most structurally sound trading concepts into the isolated visual sandbox phase.

## High-Level Findings

- **Day Trade:** Lance Breitstein's Trend Trading strategy holds the highest promise for intraday testing.
- **Swing Trade:** Mark Minervini, Larry Williams, and Gon Gajala represent the strongest, most mechanical edge candidates.
- **Position Trade:** Currently empty, as previously identified candidates were properly reclassified to Swing based on their 1-week to 30-day time horizons.
- **Filters/Exits:** Brian Shannon's AVWAP (Filter) and Linda Raschke's Sell Rules (Exit) are critical modules that should be prioritized for their respective tasks.

## Sandbox Protocol
Candidates must be tested one at a time in standalone Pine files and isolated Python harnesses. They must not pollute `MTC_V2.pine` until explicitly verified.

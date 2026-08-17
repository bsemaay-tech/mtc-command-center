# Day/Swing Trading Bot Dashboard — UI Architecture (v0.1 prototype)

**Status:** UI prototype with mock data only. No broker/exchange/VPS connection,
no live controls, nothing armed. This document is the full UI schema requested
by Barış (2026-08-17): which card goes where, the menu/page structure, and the
data contract each panel expects.

It deliberately incorporates the accepted Bridge V2 dashboard direction
(`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`,
Part B) — single execution dashboard + drill-down, block-reason visibility
("Why No Trade?"), viewing never trades, loopback-first access — while adding
the trader-facing content spec (signals, journal, scanner, performance,
backtest-vs-live) that Part B leaves open.

## Design principles

1. **5-second rule.** The Overview answers, without scrolling past the fold:
   is the bot running · is it making money · what is it doing now · how much
   risk is on · is anything broken.
2. **Viewing never trades.** Every control that could change trading state is
   a separate, gated, explicitly-confirmed action (B2 in the V2 decisions).
   The prototype's buttons are inert by design.
3. **"Quiet" must be explainable.** No-trade states always carry a reason —
   the AI panel's *Why No Trade?* feed and the risk-manager veto log make a
   blocked system distinguishable from a quiet market (B3).
4. **One axis per chart, validated palette, no color-alone meaning.** Colors
   come from the validated dark dataviz palette; LONG/SHORT, P&L and status
   always pair color with a sign, word, or icon. The app commits to a single
   dark terminal look (documented choice; tokens live in `styles.css :root`).

## Global chrome (every page)

```
┌──────────────────────────────────────────────────────────────────────┐
│ TOPBAR  BOT ● RUNNING [PAPER] Strategy:Hybrid  Broker ● Data ● VPS ● │
│         Market ● OPEN     …      last data · last trade · clock      │
├──────────────────────────────────────────────────────────────────────┤
│ ⚠ HIGH IMPACT EVENT banner (only when an event restricts trading)    │
├──────────────────────────────────────────────────────────────────────┤
│ TABS: Overview · Positions&Orders · Signals · Risk · Performance ·   │
│       Journal · Scanner · AI Engine · News · System                  │
└──────────────────────────────────────────────────────────────────────┘
```

Topbar = spec §1 + §14 top line. It is sticky: bot state, mode badge
(LIVE green / PAPER yellow / BACKTEST blue), broker, data feed, VPS, market
session, freshness stamps, clock. Any red dot here outranks everything else
on screen.

## Page map (spec § → page)

| Page | Spec sections | Cards, in order |
|---|---|---|
| **Overview** | 18 (composition), 1,2,3,5,6,7,10,12,14 (summaries) | KPI row (Equity · Day P&L · Open Risk · Drawdown · Cash/BP · Margin) → Main chart → Open Positions (compact) + AI Market View → Top Signals + Scanner top-5 → Performance mini + Risk mini → System Health strip |
| **Positions & Orders** | 3, 4 | Full positions table (adds value, trail, risk $, %, opened, duration, strategy) → order blotter (status chips, fills, slippage, commission, latency, broker ID) |
| **Signals** | 5 | Signal cards: side, strength meter, entry zone/stop/target, R/R, validity, per-condition ✓/✗ checklist, plain-language reason |
| **Risk** | 6 | Utilization meters (per-trade, daily, portfolio, DD, loss budgets, positions, exposure, leverage, margin) → sector exposure vs caps + correlation note → armed guards list → manual controls (CLOSE ALL / PAUSE, confirmation-gated) |
| **Performance** | 7, 9, 17 | Period filter (Today/Week/Month/3M/YTD/All) → 16 stat tiles → equity curve vs buy&hold → strategy table → backtest-vs-live comparison |
| **Journal** | 8 | Full trade history incl. entry/exit reasons (auto-journal) |
| **Scanner** | 10 | Watchlist ranked by opportunity score (gap, RVOL, ATR, RSI, trend, note) |
| **AI Engine** | 12 | Market view (regime, volatility, risk mode, bias, confidence) → **Why No Trade?** veto feed |
| **News** | 13 | Economic calendar + earnings with impact chips → headlines; HIGH impact also raises the global banner |
| **System** | 14, 15, 16 | CPU/RAM/disk/network meters, uptime, restarts, latencies → service health (bot, DB, feed, broker API, strategy, risk) → log center (INFO/WARNING/ERROR/CRITICAL) → notification history + channels |

## Data contract (what a real backend must serve)

Each panel binds to one key of the `MOCK` object in `mock_data.js`; the shape
of that object **is** the read-model contract for a future
`/api/bot-dashboard` endpoint (same pattern as `apps/api` read-model):

`status, portfolio, equityCurve, positions, orders, signals, risk,
performance, journal, strategies, scanner, ai, news, system, logs,
notifications, btVsLive, chart`

Rules for the real integration (not implemented here):

- **Read-only snapshot API first** (existing `apps/api` direction); poll or
  SSE. WebSocket only when latency actually matters.
- Freshness: every payload carries a timestamp; the UI renders staleness, it
  never hides it (a frozen feed must not look like a quiet market).
- Controls (PAUSE, CLOSE ALL, arm/disarm) are **not** part of the read model —
  they are a separate authenticated write surface, gated per V2 B2/B5
  (loopback-first, login/2FA before any exposure), and out of scope for this
  prototype.

## Charting

- Main chart: canvas candlesticks + volume subpane, EMA20/EMA50/VWAP
  overlays, dashed SL/TP/SR levels, ▲ entry / ▼ exit markers from the bot's
  own trades, crosshair tooltip (OHLC, volume, indicator values, trade label).
  A production build could swap this for TradingView's lightweight-charts;
  the panel contract (candles + overlays + trades + levels) stays the same.
- Equity curve: bot equity vs buy&hold, hover tooltip. One y-axis; the
  benchmark is drawn on the same scale by design.

## Palette

Dark terminal, tokens in `styles.css`: surfaces `#0d0d0d/#1a1a19`, series
blue `#3987e5` / orange `#d95926` / aqua `#199e70` (validated dark
categorical slots 1–3), status good/warn/serious/critical
`#0ca30c/#fab219/#ec835a/#d03b3b`. P&L uses good/critical paired with
+/- signs and words, never color alone.

## Open points for a v1

- Real read-model endpoint + staleness handling (reuse `apps/api` core).
- Per-strategy drill-down route (V2 B4) once multiple workers exist.
- Alert thresholds → notification channels wiring (spec §16).
- Auth model before any non-loopback exposure (V2 B5 — hard gate).

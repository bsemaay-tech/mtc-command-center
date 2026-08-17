/* Trading Bot Dashboard — MOCK DATA ONLY.
 * No broker, exchange, VPS or live connection. All values are synthetic and
 * generated with a seeded PRNG so every load renders the same demo state.
 */
"use strict";

// Deterministic PRNG (mulberry32) so the demo is stable across reloads.
function seededRng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const MOCK = (() => {
  const rng = seededRng(20260817);

  /* ---------- 1. Status ---------- */
  const status = {
    bot: "RUNNING",            // RUNNING | PAUSED | ERROR
    mode: "PAPER",             // LIVE | PAPER | BACKTEST
    strategyMode: "Hybrid",    // Day | Swing | Hybrid
    broker: { name: "IBKR Paper", state: "CONNECTED" },
    market: "OPEN",
    lastDataUpdate: "2026-08-17 21:59:58",
    lastTradeTime: "2026-08-17 19:42:11",
    vps: { state: "ONLINE", uptime: "27d 14h", pingMs: 12 },
    ws: { state: "LIVE", latencyMs: 9 },
    apiLatencyMs: 41,
  };

  /* ---------- 2. Portfolio ---------- */
  const portfolio = {
    totalEquity: 64280, availableCash: 21740, buyingPower: 86960,
    investedCapital: 42540, marginUsed: 8300, marginAvailable: 34700,
    dayPnl: 842, totalPnl: 14280, realizedPnl: 11930, unrealizedPnl: 2350,
    returnDay: 1.33, returnWeek: 2.9, returnMonth: 6.4,
  };

  // Equity curve: 130 sessions of a gently rising random walk + benchmark.
  const equityCurve = [];
  let eq = 50000, bh = 50000;
  for (let i = 0; i < 130; i++) {
    eq *= 1 + (rng() - 0.46) * 0.012;
    bh *= 1 + (rng() - 0.487) * 0.010;
    equityCurve.push({ i, equity: Math.round(eq), benchmark: Math.round(bh) });
  }
  // Pin the endpoint to the headline equity figure.
  const scale = portfolio.totalEquity / equityCurve[equityCurve.length - 1].equity;
  equityCurve.forEach(p => { p.equity = Math.round(p.equity * scale); });

  /* ---------- 3. Open positions ---------- */
  const positions = [
    { symbol: "NVDA", side: "LONG",  entry: 182.40, last: 186.10, qty: 60,  sl: 178.20, tp: 196.00, trail: null,   riskUsd: 252, opened: "2026-08-15 16:32", strategy: "Swing Trend",    setup: "EMA pullback" },
    { symbol: "TSLA", side: "SHORT", entry: 244.80, last: 246.15, qty: 40,  sl: 251.00, tp: 228.00, trail: 249.4,  riskUsd: 248, opened: "2026-08-17 17:05", strategy: "Mean Reversion", setup: "VWAP fade" },
    { symbol: "AMD",  side: "LONG",  entry: 168.90, last: 170.85, qty: 72,  sl: 164.70, tp: 181.50, trail: null,   riskUsd: 302, opened: "2026-08-14 18:20", strategy: "Breakout",       setup: "Range break + RVOL" },
    { symbol: "META", side: "LONG",  entry: 611.20, last: 609.70, qty: 12,  sl: 598.00, tp: 648.00, trail: null,   riskUsd: 158, opened: "2026-08-17 15:48", strategy: "Swing Trend",    setup: "Higher-low continuation" },
  ];
  positions.forEach(p => {
    const dir = p.side === "LONG" ? 1 : -1;
    p.value = +(p.last * p.qty).toFixed(0);
    p.uPnl = +((p.last - p.entry) * p.qty * dir).toFixed(0);
    p.uPnlPct = +(((p.last - p.entry) / p.entry) * 100 * dir).toFixed(2);
    p.riskPct = +((p.riskUsd / portfolio.totalEquity) * 100).toFixed(2);
  });

  /* ---------- 4. Orders ---------- */
  const orders = [
    { id: "BRK-88412", time: "21:58:12", symbol: "AMD",  type: "LIMIT",  role: "TP",    side: "SELL", qty: 72, price: 181.50, status: "PENDING",   fill: null,   slippage: null,  commission: null, latencyMs: 38 },
    { id: "BRK-88409", time: "21:58:11", symbol: "AMD",  type: "STOP",   role: "SL",    side: "SELL", qty: 72, price: 164.70, status: "PENDING",   fill: null,   slippage: null,  commission: null, latencyMs: 36 },
    { id: "BRK-88395", time: "19:42:11", symbol: "META", type: "MARKET", role: "ENTRY", side: "BUY",  qty: 12, price: null,   status: "FILLED",    fill: 611.20, slippage: 0.04,  commission: 1.02, latencyMs: 52 },
    { id: "BRK-88374", time: "17:05:03", symbol: "TSLA", type: "LIMIT",  role: "ENTRY", side: "SELL", qty: 40, price: 244.80, status: "FILLED",    fill: 244.80, slippage: 0.00,  commission: 1.10, latencyMs: 47 },
    { id: "BRK-88361", time: "16:22:40", symbol: "MSFT", type: "LIMIT",  role: "ENTRY", side: "BUY",  qty: 15, price: 512.00, status: "CANCELLED", fill: null,   slippage: null,  commission: null, latencyMs: 41 },
    { id: "BRK-88342", time: "15:48:19", symbol: "QQQ",  type: "LIMIT",  role: "ENTRY", side: "BUY",  qty: 30, price: 484.20, status: "PARTIAL",   fill: 484.20, slippage: 0.00,  commission: 0.55, latencyMs: 44, note: "18/30 filled" },
    { id: "BRK-88318", time: "15:31:02", symbol: "AAPL", type: "MARKET", role: "ENTRY", side: "BUY",  qty: 25, price: null,   status: "REJECTED",  fill: null,   slippage: null,  commission: null, latencyMs: 61, note: "Sector exposure limit" },
  ];

  /* ---------- 5. Signals ---------- */
  const signals = [
    { symbol: "NVDA", action: "LONG",  strength: 87, entryZone: "184.8 – 186.4", stop: 181.9, target: 197.6, rr: "1:3.2", time: "21:41", validFor: "45m", strategy: "Breakout",
      checks: [["Trend", true], ["EMA Cross", true], ["Volume Confirmation", true], ["RSI", true], ["Breakout", true]],
      reason: "Range break above 185.2 on 2.4× relative volume with rising 20-EMA; RSI 61 leaves headroom." },
    { symbol: "AMD",  action: "LONG",  strength: 81, entryZone: "170.2 – 171.3", stop: 167.4, target: 179.9, rr: "1:2.7", time: "21:36", validFor: "40m", strategy: "Breakout",
      checks: [["Trend", true], ["EMA Cross", true], ["Volume Confirmation", true], ["RSI", true], ["Breakout", false]],
      reason: "Coiling under 171.4 resistance; volume building, breakout not yet triggered — armed." },
    { symbol: "META", action: "LONG",  strength: 76, entryZone: "608.5 – 612.0", stop: 601.0, target: 634.0, rr: "1:2.9", time: "21:20", validFor: "60m", strategy: "Swing Trend",
      checks: [["Trend", true], ["EMA Cross", true], ["Volume Confirmation", false], ["RSI", true], ["Breakout", true]],
      reason: "Higher-low continuation above rising 50-EMA; waiting on volume confirmation." },
    { symbol: "XOM",  action: "SELL",  strength: 68, entryZone: "118.9 – 119.6", stop: 121.2, target: 113.8, rr: "1:2.3", time: "20:55", validFor: "90m", strategy: "Mean Reversion",
      checks: [["Trend", false], ["EMA Cross", true], ["Volume Confirmation", true], ["RSI", true], ["Breakout", false]],
      reason: "Extended 3.1 ATR above 20-EMA into weekly supply; RSI 78 overbought fade." },
  ];

  /* ---------- 6. Risk ---------- */
  const risk = {
    perTradePct: 0.5, perTradeMaxPct: 1.0,
    dailyRiskPct: 1.8, dailyRiskMaxPct: 3.0,
    portfolioRiskPct: 3.2, portfolioRiskMaxPct: 6.0,
    maxDrawdownPct: -8.4, currentDrawdownPct: -2.1, ddKillPct: -10.0,
    dailyLossLimitUsd: 1900, dailyLossUsedUsd: 0,   // positive day so far
    weeklyLossLimitUsd: 4500, weeklyLossUsedUsd: 620,
    maxOpenPositions: 6, openPositions: positions.length,
    maxExposurePct: 75, exposurePct: 66,
    leverage: 1.35, marginUtilPct: 19.3,
    sectorExposure: [
      { sector: "Technology", pct: 38, cap: 40 },
      { sector: "Comm. Services", pct: 11, cap: 25 },
      { sector: "Consumer Disc.", pct: 9, cap: 25 },
      { sector: "Energy", pct: 4, cap: 20 },
      { sector: "Cash", pct: 38, cap: 100 },
    ],
    correlation: { pairs: [["NVDA", "AMD", 0.81]], note: "NVDA–AMD 0.81 — treated as one risk unit" },
    killSwitches: [
      { name: "Daily Loss Kill Switch", state: "ARMED", detail: "Flatten + pause at -$1,900 day P&L" },
      { name: "Max Drawdown Kill Switch", state: "ARMED", detail: "Flatten + pause at -10% from equity high" },
      { name: "Consecutive Loss Limit", state: "ARMED", detail: "Pause new entries after 4 straight losses (now 1)" },
      { name: "API Failure Protection", state: "ARMED", detail: "Cancel entries if broker API down > 30s" },
      { name: "Data Feed Failure Protection", state: "ARMED", detail: "Freeze signals if feed stale > 15s" },
    ],
  };

  /* ---------- 7. Performance (per period) ---------- */
  const performance = {
    Today:  { trades: 5,   winRate: 60, pf: 1.71, sharpe: null, sortino: null, expectancy: 0.42, avgWin: 310, avgLoss: -168, avgR: 0.61, best: 520,  worst: -240,  maxDd: -0.8, recovery: null, winStreak: 2, lossStreak: 1, avgDuration: "2h 10m" },
    Week:   { trades: 21,  winRate: 62, pf: 1.86, sharpe: 1.91, sortino: 2.60, expectancy: 0.47, avgWin: 342, avgLoss: -175, avgR: 0.66, best: 940,  worst: -410,  maxDd: -1.9, recovery: 2.1,  winStreak: 5, lossStreak: 2, avgDuration: "3h 05m" },
    Month:  { trades: 88,  winRate: 63, pf: 1.90, sharpe: 1.82, sortino: 2.48, expectancy: 0.49, avgWin: 355, avgLoss: -182, avgR: 0.68, best: 1240, worst: -560,  maxDd: -3.4, recovery: 2.6,  winStreak: 7, lossStreak: 3, avgDuration: "3h 40m" },
    "3M":   { trades: 236, winRate: 62, pf: 1.85, sharpe: 1.76, sortino: 2.39, expectancy: 0.46, avgWin: 348, avgLoss: -186, avgR: 0.65, best: 1610, worst: -720,  maxDd: -5.6, recovery: 2.9,  winStreak: 8, lossStreak: 4, avgDuration: "4h 05m" },
    YTD:    { trades: 402, winRate: 64, pf: 1.92, sharpe: 1.74, sortino: 2.31, expectancy: 0.50, avgWin: 351, avgLoss: -179, avgR: 0.69, best: 1610, worst: -890,  maxDd: -8.4, recovery: 3.1,  winStreak: 9, lossStreak: 4, avgDuration: "3h 55m" },
    All:    { trades: 402, winRate: 64, pf: 1.92, sharpe: 1.74, sortino: 2.31, expectancy: 0.50, avgWin: 351, avgLoss: -179, avgR: 0.69, best: 1610, worst: -890,  maxDd: -8.4, recovery: 3.1,  winStreak: 9, lossStreak: 4, avgDuration: "3h 55m" },
  };

  /* ---------- 8. Trade journal ---------- */
  const journal = [
    { date: "2026-08-17", symbol: "MSFT", side: "LONG",  entry: 508.4, exit: 514.9, qty: 15, pnl: 97,   pnlPct: 1.28,  r: 1.3,  commission: 1.9, slippage: 0.06, strategy: "Swing Trend",    entryReason: "50-EMA bounce + market breadth green", exitReason: "First target hit, runner stopped at BE" },
    { date: "2026-08-17", symbol: "QQQ",  side: "LONG",  entry: 484.2, exit: 482.1, qty: 18, pnl: -38,  pnlPct: -0.43, r: -0.5, commission: 1.1, slippage: 0.02, strategy: "Breakout",       entryReason: "Opening range break",                 exitReason: "Failed break — hard stop" },
    { date: "2026-08-16", symbol: "NVDA", side: "LONG",  entry: 178.1, exit: 183.6, qty: 55, pnl: 303,  pnlPct: 3.09,  r: 2.4,  commission: 2.1, slippage: 0.05, strategy: "Breakout",       entryReason: "Break of 3-day base on 2× RVOL",      exitReason: "Trailing stop (chandelier)" },
    { date: "2026-08-16", symbol: "TSLA", side: "SHORT", entry: 249.9, exit: 244.3, qty: 35, pnl: 196,  pnlPct: 2.24,  r: 1.8,  commission: 1.8, slippage: 0.08, strategy: "Mean Reversion", entryReason: "3 ATR VWAP extension fade",           exitReason: "Target at VWAP" },
    { date: "2026-08-15", symbol: "AMD",  side: "LONG",  entry: 165.2, exit: 163.4, qty: 60, pnl: -108, pnlPct: -1.09, r: -1.0, commission: 1.6, slippage: 0.04, strategy: "Swing Trend",    entryReason: "Pullback to rising 20-EMA",           exitReason: "Full stop-out" },
    { date: "2026-08-15", symbol: "META", side: "LONG",  entry: 596.0, exit: 607.8, qty: 10, pnl: 118,  pnlPct: 1.98,  r: 1.6,  commission: 1.4, slippage: 0.07, strategy: "Swing Trend",    entryReason: "Higher low above 50-EMA",             exitReason: "Swing target 1" },
    { date: "2026-08-14", symbol: "XOM",  side: "SHORT", entry: 117.8, exit: 118.9, qty: 50, pnl: -55,  pnlPct: -0.93, r: -0.7, commission: 1.5, slippage: 0.03, strategy: "Mean Reversion", entryReason: "Overbought fade at supply",           exitReason: "Time stop — thesis stale" },
    { date: "2026-08-14", symbol: "NVDA", side: "LONG",  entry: 172.5, exit: 177.9, qty: 50, pnl: 270,  pnlPct: 3.13,  r: 2.2,  commission: 2.0, slippage: 0.05, strategy: "Breakout",       entryReason: "Gap-and-go continuation",             exitReason: "Partial at 2R, rest trailed" },
  ];

  /* ---------- 9. Strategy performance ---------- */
  const strategies = [
    { name: "Breakout",       trades: 82, winRate: 61, pnl: 4250, pf: 1.84, dd: -4.2 },
    { name: "Mean Reversion", trades: 54, winRate: 57, pnl: 1820, pf: 1.42, dd: -6.1 },
    { name: "Swing Trend",    trades: 31, winRate: 68, pnl: 5310, pf: 2.12, dd: -3.8 },
  ];

  /* ---------- 10. Scanner ---------- */
  const scanner = [
    { symbol: "NVDA", score: 92, last: 186.10, gapPct: 1.8,  rvol: 2.4, atr: 4.9, rsi: 61, trend: "UP",   momentum: "STRONG", note: "Breakout above 185.2" },
    { symbol: "META", score: 88, last: 609.70, gapPct: 0.9,  rvol: 1.9, atr: 11.2, rsi: 58, trend: "UP",   momentum: "STRONG", note: "Higher-low continuation" },
    { symbol: "AMD",  score: 84, last: 170.85, gapPct: 1.2,  rvol: 2.1, atr: 4.3, rsi: 59, trend: "UP",   momentum: "BUILDING", note: "Coiling under 171.4" },
    { symbol: "MSFT", score: 77, last: 514.20, gapPct: 0.4,  rvol: 1.3, atr: 7.8, rsi: 55, trend: "UP",   momentum: "STEADY", note: "50-EMA reclaim" },
    { symbol: "TSLA", score: 71, last: 246.15, gapPct: -0.6, rvol: 1.7, atr: 8.9, rsi: 42, trend: "DOWN", momentum: "FADING", note: "Below VWAP, short bias" },
    { symbol: "AAPL", score: 66, last: 233.40, gapPct: 0.2,  rvol: 0.9, atr: 3.6, rsi: 51, trend: "FLAT", momentum: "STEADY", note: "Inside day, no edge" },
    { symbol: "XOM",  score: 63, last: 119.20, gapPct: 0.7,  rvol: 1.4, atr: 2.1, rsi: 78, trend: "UP",   momentum: "OVEREXTENDED", note: "3 ATR over 20-EMA" },
    { symbol: "QQQ",  score: 61, last: 486.80, gapPct: 0.3,  rvol: 1.0, atr: 5.2, rsi: 56, trend: "UP",   momentum: "STEADY", note: "Index tailwind intact" },
  ];

  /* ---------- 12. AI decision engine ---------- */
  const ai = {
    regime: "BULL", volatility: "MEDIUM", riskMode: "NORMAL",
    confidence: 78, bias: "LONG",
    summary: "Breadth positive (68% above 20-EMA), index trend up, vol contained. Favor long breakouts; fade only extremes.",
    whyNoTrade: [
      { time: "21:44", symbol: "AAPL", reason: "Setup detected but volume confirmation missing (RVOL 0.9 < 1.5) and tech exposure already 38% (cap 40%)." },
      { time: "20:31", symbol: "QQQ",  reason: "Signal strength 58 below 65 threshold; correlation with open NVDA/AMD positions 0.85." },
      { time: "19:12", symbol: "XOM",  reason: "Short signal valid but CPI print in < 18h — risk mode restricts new energy shorts pre-event." },
    ],
  };

  /* ---------- 13. News & calendar ---------- */
  const news = {
    highImpact: { active: true, label: "HIGH IMPACT EVENT — CPI (Aug) tomorrow 15:30 — new entries restricted 15:00–16:00" },
    calendar: [
      { date: "2026-08-18 15:30", event: "CPI (Aug)", impact: "HIGH" },
      { date: "2026-08-19 21:00", event: "FOMC Minutes", impact: "HIGH" },
      { date: "2026-08-20 22:05", event: "NVDA Earnings (AMC)", impact: "HIGH" },
      { date: "2026-08-21 15:30", event: "Initial Jobless Claims", impact: "MEDIUM" },
      { date: "2026-08-22 17:00", event: "Fed Chair speech (Jackson Hole)", impact: "HIGH" },
    ],
    headlines: [
      { time: "21:12", source: "Wire", text: "Chip sector extends gains ahead of NVDA earnings; SOX +1.9%." },
      { time: "19:48", source: "Analyst", text: "META raised to Overweight, PT $700 (prev $640)." },
      { time: "18:05", source: "Wire", text: "Crude slips 1.2% as supply talks progress; energy names fade." },
      { time: "16:30", source: "Macro", text: "10Y yield steady at 3.92% into CPI; futures hold gains." },
    ],
  };

  /* ---------- 14. System telemetry ---------- */
  const system = {
    topbar: { vps: "ONLINE", broker: "CONNECTED", data: "LIVE", latencyMs: 12, bot: "RUNNING" },
    metrics: { cpuPct: 23, ramPct: 41, diskPct: 57, netMbps: 3.4 },
    services: [
      { name: "Bot process", state: "OK", detail: "pid 4183 · 27d" },
      { name: "Database", state: "OK", detail: "WAL healthy · 41ms" },
      { name: "Market Data Feed", state: "OK", detail: "9ms · 0 gaps today" },
      { name: "Broker API", state: "OK", detail: "41ms · 0 rejects (conn)" },
      { name: "Strategy engine", state: "OK", detail: "3 strategies loaded" },
      { name: "Risk manager", state: "OK", detail: "5 guards armed" },
    ],
    lastHeartbeat: "2s ago", uptime: "27d 14h 22m", restarts30d: 1,
  };

  /* ---------- 15. Logs ---------- */
  const logs = [
    { time: "21:59:58", level: "INFO",     source: "feed",     msg: "Bar close 5m processed for 8 symbols (9ms)" },
    { time: "21:58:12", level: "INFO",     source: "orders",   msg: "OCO bracket placed for AMD (TP 181.50 / SL 164.70)" },
    { time: "21:44:03", level: "INFO",     source: "risk",     msg: "AAPL entry vetoed: sector exposure 38% near 40% cap" },
    { time: "20:14:47", level: "WARNING",  source: "feed",     msg: "Quote latency spike 240ms (1 tick), recovered" },
    { time: "19:42:11", level: "INFO",     source: "orders",   msg: "META BUY 12 filled @ 611.20 (slip 0.04)" },
    { time: "18:03:29", level: "ERROR",    source: "broker",   msg: "Order BRK-88318 rejected: sector exposure limit" },
    { time: "15:31:02", level: "WARNING",  source: "risk",     msg: "Tech exposure crossed 35% advisory threshold" },
    { time: "13:00:00", level: "INFO",     source: "system",   msg: "Session start — guards armed, feeds green" },
  ];

  /* ---------- 16. Notifications ---------- */
  const notifications = {
    channels: [
      { name: "Telegram", enabled: true }, { name: "Discord", enabled: false },
      { name: "Push", enabled: true }, { name: "Email", enabled: true },
    ],
    recent: [
      { time: "19:42", kind: "Trade opened", text: "META LONG 12 @ 611.20 (SL 598, TP 648)" },
      { time: "17:05", kind: "Trade opened", text: "TSLA SHORT 40 @ 244.80 (SL 251, TP 228)" },
      { time: "16:41", kind: "Target hit", text: "MSFT partial exit +$97 (1.3R)" },
      { time: "15:31", kind: "Risk", text: "Tech exposure 35% advisory threshold crossed" },
      { time: "13:00", kind: "System", text: "Bot started — PAPER mode, 3 strategies" },
    ],
  };

  /* ---------- 17. Backtest vs Live ---------- */
  const btVsLive = [
    { metric: "Win Rate", backtest: "61%", live: "64%", verdict: "OK" },
    { metric: "Profit Factor", backtest: "1.78", live: "1.92", verdict: "OK" },
    { metric: "Max Drawdown", backtest: "-9.8%", live: "-8.4%", verdict: "OK" },
    { metric: "Avg Slippage / trade", backtest: "$0.05", live: "$0.05", verdict: "OK" },
    { metric: "Trades / month", backtest: "96", live: "88", verdict: "WATCH" },
    { metric: "Avg R multiple", backtest: "0.72", live: "0.69", verdict: "OK" },
  ];

  /* ---------- 11. Chart candles (NVDA 5m demo) ---------- */
  const candles = [];
  let px = 181.0;
  for (let i = 0; i < 96; i++) {
    const drift = i > 60 ? 0.64 : 0.53;                 // late-session breakout
    const chg = (rng() - (1 - drift)) * 0.9;
    const open = px;
    const close = +(px + chg).toFixed(2);
    const high = +(Math.max(open, close) + rng() * 0.5).toFixed(2);
    const low = +(Math.min(open, close) - rng() * 0.5).toFixed(2);
    const vol = Math.round(40 + rng() * 60 + (i > 60 ? 45 : 0));
    candles.push({ i, open: +open.toFixed(2), high, low, close, vol });
    px = close;
  }
  // Rescale so the last close matches the NVDA position's live price.
  const pxScale = 186.10 / candles[candles.length - 1].close;
  candles.forEach(c => {
    c.open = +(c.open * pxScale).toFixed(2); c.close = +(c.close * pxScale).toFixed(2);
    c.high = +(c.high * pxScale).toFixed(2); c.low = +(c.low * pxScale).toFixed(2);
  });
  // EMA helpers for overlay lines.
  function ema(period) {
    const k = 2 / (period + 1); const out = []; let e = candles[0].close;
    candles.forEach(c => { e = c.close * k + e * (1 - k); out.push(+e.toFixed(2)); });
    return out;
  }
  const chart = {
    symbol: "NVDA", tf: "5m",
    candles, ema20: ema(20), ema50: ema(50),
    vwap: candles.map((c, i) => {
      const slice = candles.slice(0, i + 1);
      const pv = slice.reduce((s, x) => s + ((x.high + x.low + x.close) / 3) * x.vol, 0);
      const v = slice.reduce((s, x) => s + x.vol, 0);
      return +(pv / v).toFixed(2);
    }),
    trades: [
      { i: 22, kind: "ENTRY", side: "LONG", price: candles[22].close, label: "Entry 60 @ " + candles[22].close },
      { i: 47, kind: "EXIT",  side: "LONG", price: candles[47].close, label: "Partial exit @ " + candles[47].close },
      { i: 68, kind: "ENTRY", side: "LONG", price: candles[68].close, label: "Add on breakout @ " + candles[68].close },
    ],
    levels: [
      { kind: "SL", price: 178.20 }, { kind: "TP", price: 196.00 },
      { kind: "SR", price: 185.20, label: "Resistance → support" },
    ],
  };

  return { status, portfolio, equityCurve, positions, orders, signals, risk,
           performance, journal, strategies, scanner, ai, news, system, logs,
           notifications, btVsLive, chart };
})();

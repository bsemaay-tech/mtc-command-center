/* Trading Bot Dashboard prototype — renders MOCK into the page.
 * Plain DOM + canvas, no dependencies. Everything is read-only demo state.
 */
"use strict";

const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function fmtUsd(v, withSign) {
  const sign = v < 0 ? "-" : (withSign ? "+" : "");
  return sign + "$" + Math.abs(v).toLocaleString("en-US");
}
function pnlCls(v) { return v >= 0 ? "pnl-up" : "pnl-down"; }
function pnlCell(v, suffix) {
  return `<span class="num ${pnlCls(v)}">${fmtUsd(v, true)}${suffix || ""}</span>`;
}

/* ============ Top bar, banner, tabs ============ */
function renderTopbar() {
  const s = MOCK.status, t = MOCK.system.topbar;
  const dot = (state) => {
    const ok = ["RUNNING", "ONLINE", "CONNECTED", "LIVE", "OPEN", "OK"].includes(state);
    const warnS = ["PAUSED", "PARTIAL", "CLOSED"].includes(state);
    return `<span class="dot ${ok ? "good" : warnS ? "warn" : "crit"}"></span>`;
  };
  $("#topbar").innerHTML = `
    <span class="brand">MTC BOT TERMINAL<span class="sub">prototype</span></span>
    <span class="statusitem">${dot(s.bot)}<b>BOT ${esc(s.bot)}</b></span>
    <span class="badge mode-${s.mode.toLowerCase()}">${esc(s.mode)}</span>
    <span class="statusitem"><span class="muted">Strategy</span><b>${esc(s.strategyMode)}</b></span>
    <span class="statusitem">${dot(s.broker.state)}<b>${esc(s.broker.name)}</b></span>
    <span class="statusitem">${dot(s.ws.state)}Data <b>${esc(s.ws.state)}</b> ${s.ws.latencyMs}ms</span>
    <span class="statusitem">${dot(s.vps.state)}VPS <b>${esc(s.vps.state)}</b> ${s.vps.pingMs}ms</span>
    <span class="statusitem">${dot(s.market)}Market <b>${esc(s.market)}</b></span>
    <span class="spacer"></span>
    <span class="statusitem muted">last data ${esc(s.lastDataUpdate.slice(11))} · last trade ${esc(s.lastTradeTime.slice(11))}</span>
    <span class="clock num" id="clock"></span>`;
}
function tickClock() {
  const el = $("#clock");
  if (el) el.textContent = new Date().toLocaleTimeString("en-GB");
}

function renderBanner() {
  const hi = MOCK.news.highImpact;
  if (hi.active) { $("#impact-banner").hidden = false; $("#impact-text").textContent = hi.label; }
}

const PAGES = [
  ["overview", "Overview"], ["positions", "Positions & Orders"], ["signals", "Signals"],
  ["risk", "Risk"], ["performance", "Performance"], ["journal", "Journal"],
  ["scanner", "Scanner"], ["ai", "AI Engine"], ["news", "News"], ["system", "System"],
];
function renderTabs() {
  $("#tabs").innerHTML = PAGES.map(([id, label]) =>
    `<button data-tab="${id}">${label}</button>`).join("");
  $("#tabs").addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-tab]");
    if (btn) activateTab(btn.dataset.tab);
  });
  activateTab("overview");
}
function activateTab(id) {
  document.querySelectorAll(".tabs button").forEach(b => b.classList.toggle("active", b.dataset.tab === id));
  document.querySelectorAll(".page").forEach(p => p.classList.toggle("active", p.dataset.page === id));
  if (id === "overview") drawMainChart();
  if (id === "performance") drawEquityChart();
}

/* ============ KPI tiles (overview) ============ */
function renderKpis() {
  const p = MOCK.portfolio, r = MOCK.risk;
  const tiles = [
    ["Total Equity", fmtUsd(p.totalEquity), `<span class="${pnlCls(p.returnDay)}">${p.returnDay > 0 ? "+" : ""}${p.returnDay}% today</span>`],
    ["Day P&L", `<span class="${pnlCls(p.dayPnl)}">${fmtUsd(p.dayPnl, true)}</span>`, `realized ${fmtUsd(p.realizedPnl)} · unrealized ${fmtUsd(p.unrealizedPnl)}`],
    ["Open Risk", `${r.dailyRiskPct}%`, `daily cap ${r.dailyRiskMaxPct}%`],
    ["Drawdown", `<span class="${pnlCls(r.currentDrawdownPct)}">${r.currentDrawdownPct}%</span>`, `max ${r.maxDrawdownPct}% · kill at ${r.ddKillPct}%`],
    ["Cash / Buying Power", fmtUsd(p.availableCash), `BP ${fmtUsd(p.buyingPower)}`],
    ["Margin", fmtUsd(p.marginUsed), `available ${fmtUsd(p.marginAvailable)}`],
  ];
  $("#kpi-row").innerHTML = tiles.map(([l, v, d]) =>
    `<div class="tile"><div class="label">${l}</div><div class="value num">${v}</div><div class="delta muted">${d}</div></div>`).join("");
}

/* ============ Positions ============ */
function positionsTable(full) {
  const rows = MOCK.positions.map(p => `
    <tr>
      <td class="left"><b>${p.symbol}</b> <span class="muted">${esc(p.setup)}</span></td>
      <td class="side-${p.side.toLowerCase()}">${p.side}</td>
      <td class="num">${p.entry.toFixed(2)}</td>
      <td class="num">${p.last.toFixed(2)}</td>
      <td class="num">${p.qty}</td>
      ${full ? `<td class="num">${fmtUsd(p.value)}</td>` : ""}
      <td>${pnlCell(p.uPnl)} <span class="muted num">(${p.uPnlPct > 0 ? "+" : ""}${p.uPnlPct}%)</span></td>
      <td class="num">${p.sl.toFixed(2)}</td>
      <td class="num">${p.tp.toFixed(2)}</td>
      ${full ? `<td class="num">${p.trail ? p.trail.toFixed(1) : "—"}</td>
      <td class="num">${fmtUsd(p.riskUsd)} <span class="muted">(${p.riskPct}%)</span></td>
      <td class="muted">${esc(p.opened)}</td>
      <td class="left muted">${esc(p.strategy)}</td>` : ""}
    </tr>`).join("");
  return `<table>
    <thead><tr>
      <th class="left">Symbol</th><th>Side</th><th>Entry</th><th>Last</th><th>Size</th>
      ${full ? "<th>Value</th>" : ""}<th>Unrl P&L</th><th>SL</th><th>TP</th>
      ${full ? "<th>Trail</th><th>Risk</th><th>Opened</th><th class='left'>Strategy</th>" : ""}
    </tr></thead><tbody>${rows}</tbody></table>`;
}

/* ============ Orders ============ */
function ordersTable() {
  const chip = (st) => ({
    PENDING: "pending", FILLED: "ok", PARTIAL: "warn", CANCELLED: "muted", REJECTED: "bad",
  }[st] || "muted");
  const rows = MOCK.orders.map(o => `
    <tr>
      <td class="left muted num">${o.time}</td>
      <td class="left"><b>${o.symbol}</b></td>
      <td>${o.side} ${o.type}</td>
      <td class="muted">${o.role}</td>
      <td class="num">${o.qty}</td>
      <td class="num">${o.price != null ? o.price.toFixed(2) : "MKT"}</td>
      <td><span class="chip ${chip(o.status)}">${o.status}</span>${o.note ? ` <span class="muted">${esc(o.note)}</span>` : ""}</td>
      <td class="num">${o.fill != null ? o.fill.toFixed(2) : "—"}</td>
      <td class="num">${o.slippage != null ? o.slippage.toFixed(2) : "—"}</td>
      <td class="num">${o.commission != null ? "$" + o.commission.toFixed(2) : "—"}</td>
      <td class="num">${o.latencyMs}ms</td>
      <td class="muted">${o.id}</td>
    </tr>`).join("");
  return `<table>
    <thead><tr><th class="left">Time</th><th class="left">Symbol</th><th>Order</th><th>Role</th><th>Qty</th>
    <th>Price</th><th>Status</th><th>Avg Fill</th><th>Slip</th><th>Comm</th><th>Latency</th><th>Broker ID</th></tr></thead>
    <tbody>${rows}</tbody></table>`;
}

/* ============ Signals ============ */
function signalCard(s) {
  const checks = s.checks.map(([name, ok]) =>
    `<li class="${ok ? "" : "no"}">${ok ? "✓" : "✗"} ${esc(name)}</li>`).join("");
  return `<div class="signal">
    <div class="head">
      <span class="sym">${s.symbol}</span>
      <span class="${s.action === "LONG" ? "side-long" : "side-short"}">${s.action}</span>
      <span class="muted">${esc(s.strategy)}</span>
      <span class="strength num">${s.strength}%</span>
    </div>
    <div class="meter"><i style="width:${s.strength}%"></i></div>
    <div class="meta num">Entry ${esc(s.entryZone)} · Stop ${s.stop} · Target ${s.target} · R/R ${esc(s.rr)} · ${s.time} · valid ${esc(s.validFor)}</div>
    <ul class="checks">${checks}</ul>
    <div class="why">${esc(s.reason)}</div>
  </div>`;
}

/* ============ Risk ============ */
function riskMeters() {
  const r = MOCK.risk;
  const row = (name, used, cap, unit) => {
    const pct = Math.min(100, Math.abs(used) / Math.abs(cap) * 100);
    const fmt = (v) => unit === "$" ? fmtUsd(v) : v + unit;
    return `<div class="riskrow"><span class="name">${name}</span>
      <span class="meter risk"><i style="width:${pct.toFixed(0)}%"></i></span>
      <span class="val num">${fmt(used)} / ${fmt(cap)}</span></div>`;
  };
  return [
    row("Risk per Trade", r.perTradePct, r.perTradeMaxPct, "%"),
    row("Daily Risk", r.dailyRiskPct, r.dailyRiskMaxPct, "%"),
    row("Portfolio Risk", r.portfolioRiskPct, r.portfolioRiskMaxPct, "%"),
    row("Drawdown", Math.abs(r.currentDrawdownPct), Math.abs(r.ddKillPct), "%"),
    row("Daily Loss Budget", r.dailyLossUsedUsd, r.dailyLossLimitUsd, "$"),
    row("Weekly Loss Budget", r.weeklyLossUsedUsd, r.weeklyLossLimitUsd, "$"),
    row("Open Positions", r.openPositions, r.maxOpenPositions, ""),
    row("Exposure", r.exposurePct, r.maxExposurePct, "%"),
    `<div class="riskrow"><span class="name">Leverage</span><span class="meter risk"><i style="width:${(r.leverage / 3 * 100).toFixed(0)}%"></i></span><span class="val num">${r.leverage}× (max 3×)</span></div>`,
    `<div class="riskrow"><span class="name">Margin Utilization</span><span class="meter risk"><i style="width:${r.marginUtilPct}%"></i></span><span class="val num">${r.marginUtilPct}%</span></div>`,
  ].join("");
}
function sectorRows() {
  return MOCK.risk.sectorExposure.map(s => `
    <div class="riskrow"><span class="name">${esc(s.sector)}</span>
    <span class="meter"><i style="width:${(s.pct / s.cap * 100).toFixed(0)}%"></i></span>
    <span class="val num">${s.pct}% / ${s.cap}%</span></div>`).join("");
}
function guardRows() {
  return MOCK.risk.killSwitches.map(k => `
    <div class="guard">
      <div><b>${esc(k.name)}</b><div class="detail">${esc(k.detail)}</div></div>
      <span class="chip ${k.state === "ARMED" ? "ok" : k.state === "TRIGGERED" ? "bad" : "muted"}">${k.state}</span>
    </div>`).join("");
}

/* ============ Performance ============ */
let perfPeriod = "YTD";
function renderPerfFilters() {
  const el = $("#perf-filters");
  el.innerHTML = Object.keys(MOCK.performance).map(p =>
    `<button data-period="${p}" class="${p === perfPeriod ? "active" : ""}">${p}</button>`).join("");
  el.onclick = (e) => {
    const b = e.target.closest("button[data-period]");
    if (!b) return;
    perfPeriod = b.dataset.period;
    renderPerfFilters(); renderPerfTiles();
  };
}
function perfTiles(P) {
  const t = [
    ["Trades", P.trades], ["Win Rate", P.winRate + "%"], ["Profit Factor", P.pf],
    ["Sharpe", P.sharpe ?? "—"], ["Sortino", P.sortino ?? "—"], ["Expectancy (R)", P.expectancy],
    ["Avg Win", fmtUsd(P.avgWin)], ["Avg Loss", fmtUsd(P.avgLoss)], ["Avg R", P.avgR],
    ["Best Trade", fmtUsd(P.best, true)], ["Worst Trade", fmtUsd(P.worst)], ["Max DD", P.maxDd + "%"],
    ["Recovery Factor", P.recovery ?? "—"], ["Win Streak", P.winStreak], ["Loss Streak", P.lossStreak],
    ["Avg Duration", P.avgDuration],
  ];
  return t.map(([l, v]) =>
    `<div class="tile"><div class="label">${l}</div><div class="value num" style="font-size:18px">${v}</div></div>`).join("");
}
function renderPerfTiles() { $("#pg-perf-tiles").innerHTML = perfTiles(MOCK.performance[perfPeriod]); }

function strategiesTable() {
  const rows = MOCK.strategies.map(s => `
    <tr><td class="left"><b>${esc(s.name)}</b></td><td class="num">${s.trades}</td>
    <td class="num">${s.winRate}%</td><td>${pnlCell(s.pnl)}</td>
    <td class="num">${s.pf}</td><td class="num pnl-down">${s.dd}%</td></tr>`).join("");
  return `<table><thead><tr><th class="left">Strategy</th><th>Trades</th><th>Win Rate</th><th>P&L</th><th>PF</th><th>Max DD</th></tr></thead><tbody>${rows}</tbody></table>`;
}
function btLiveTable() {
  const rows = MOCK.btVsLive.map(r => `
    <tr><td class="left">${esc(r.metric)}</td><td class="num">${esc(r.backtest)}</td><td class="num"><b>${esc(r.live)}</b></td>
    <td><span class="chip ${r.verdict === "OK" ? "ok" : "warn"}">${r.verdict}</span></td></tr>`).join("");
  return `<table><thead><tr><th class="left">Metric</th><th>Backtest</th><th>Live</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table>`;
}

/* ============ Journal ============ */
function journalTable() {
  const rows = MOCK.journal.map(t => `
    <tr>
      <td class="left muted">${t.date}</td><td class="left"><b>${t.symbol}</b></td>
      <td class="side-${t.side.toLowerCase()}">${t.side}</td>
      <td class="num">${t.entry.toFixed(1)}</td><td class="num">${t.exit.toFixed(1)}</td><td class="num">${t.qty}</td>
      <td>${pnlCell(t.pnl)}</td>
      <td class="num ${pnlCls(t.pnlPct)}">${t.pnlPct > 0 ? "+" : ""}${t.pnlPct}%</td>
      <td class="num ${pnlCls(t.r)}">${t.r > 0 ? "+" : ""}${t.r}R</td>
      <td class="num">$${t.commission.toFixed(1)}</td><td class="num">${t.slippage.toFixed(2)}</td>
      <td class="left muted">${esc(t.strategy)}</td>
      <td class="left muted">${esc(t.entryReason)}</td>
      <td class="left muted">${esc(t.exitReason)}</td>
    </tr>`).join("");
  return `<table><thead><tr>
    <th class="left">Date</th><th class="left">Symbol</th><th>Dir</th><th>Entry</th><th>Exit</th><th>Qty</th>
    <th>P&L</th><th>P&L %</th><th>R</th><th>Comm</th><th>Slip</th>
    <th class="left">Strategy</th><th class="left">Entry Reason</th><th class="left">Exit Reason</th>
  </tr></thead><tbody>${rows}</tbody></table>`;
}

/* ============ Scanner ============ */
function scannerTable(limit) {
  const list = limit ? MOCK.scanner.slice(0, limit) : MOCK.scanner;
  const rows = list.map(s => `
    <tr><td class="left"><b>${s.symbol}</b></td><td class="num"><b>${s.score}</b></td>
    <td class="num">${s.last.toFixed(2)}</td>
    <td class="num ${pnlCls(s.gapPct)}">${s.gapPct > 0 ? "+" : ""}${s.gapPct}%</td>
    <td class="num">${s.rvol}×</td><td class="num">${s.atr}</td><td class="num">${s.rsi}</td>
    <td>${s.trend}</td><td class="left muted">${esc(s.note)}</td></tr>`).join("");
  return `<table><thead><tr><th class="left">Symbol</th><th>Score</th><th>Last</th><th>Gap</th>
    <th>RVOL</th><th>ATR</th><th>RSI</th><th>Trend</th><th class="left">Note</th></tr></thead><tbody>${rows}</tbody></table>`;
}

/* ============ AI ============ */
function aiView() {
  const a = MOCK.ai;
  return `<dl class="kv">
      <dt>Market Regime</dt><dd>${a.regime}</dd>
      <dt>Volatility</dt><dd>${a.volatility}</dd>
      <dt>Risk Mode</dt><dd>${a.riskMode}</dd>
      <dt>Trade Bias</dt><dd>${a.bias}</dd>
      <dt>AI Confidence</dt><dd class="num">${a.confidence}%</dd>
    </dl>
    <div class="meter" style="margin-top:8px"><i style="width:${a.confidence}%"></i></div>
    <p class="muted" style="margin:8px 0 0">${esc(a.summary)}</p>`;
}
function aiVetoList() {
  return MOCK.ai.whyNoTrade.map(v =>
    `<li><span class="t num">${v.time}</span><b>${v.symbol}</b> — ${esc(v.reason)}</li>`).join("");
}

/* ============ News ============ */
function calendarTable() {
  const rows = MOCK.news.calendar.map(c => `
    <tr><td class="left muted num">${esc(c.date)}</td><td class="left">${esc(c.event)}</td>
    <td><span class="chip ${c.impact === "HIGH" ? "bad" : "warn"}">${c.impact}</span></td></tr>`).join("");
  return `<table><thead><tr><th class="left">When</th><th class="left">Event</th><th>Impact</th></tr></thead><tbody>${rows}</tbody></table>`;
}
function headlineList() {
  return MOCK.news.headlines.map(h =>
    `<li><span class="t num">${h.time}</span><span class="muted">[${esc(h.source)}]</span> ${esc(h.text)}</li>`).join("");
}

/* ============ System ============ */
function sysMetrics() {
  const m = MOCK.system.metrics;
  const row = (name, pct, txt) => `
    <div class="riskrow"><span class="name">${name}</span>
    <span class="meter"><i style="width:${pct}%"></i></span>
    <span class="val num">${txt}</span></div>`;
  return row("CPU", m.cpuPct, m.cpuPct + "%") + row("RAM", m.ramPct, m.ramPct + "%") +
         row("Disk", m.diskPct, m.diskPct + "%") + row("Network", Math.min(100, m.netMbps * 10), m.netMbps + " Mbps") +
         `<p class="muted" style="margin:8px 0 0">Restarts (30d): ${MOCK.system.restarts30d} · API latency ${MOCK.status.apiLatencyMs}ms · WS latency ${MOCK.status.ws.latencyMs}ms</p>`;
}
function servicesList() {
  return MOCK.system.services.map(s => `
    <div class="guard"><div><b>${esc(s.name)}</b><div class="detail">${esc(s.detail)}</div></div>
    <span class="chip ${s.state === "OK" ? "ok" : "bad"}">${s.state}</span></div>`).join("");
}
function logsTable() {
  return `<thead><tr><th class="left">Time</th><th class="left">Level</th><th class="left">Source</th><th class="left">Message</th></tr></thead><tbody>` +
    MOCK.logs.map(l => `
    <tr><td class="left num">${l.time}</td><td class="left lvl ${l.level}">${l.level}</td>
    <td class="left muted">${esc(l.source)}</td><td class="left">${esc(l.msg)}</td></tr>`).join("") + "</tbody>";
}
function notifList() {
  return MOCK.notifications.recent.map(n =>
    `<li><span class="t num">${n.time}</span><b>${esc(n.kind)}</b> — ${esc(n.text)}</li>`).join("");
}
function healthStrip() {
  return MOCK.system.services.map(s =>
    `<span class="statusitem"><span class="dot ${s.state === "OK" ? "good" : "crit"}"></span>${esc(s.name)}</span>`).join("");
}

/* ============ Canvas: main candlestick chart ============ */
function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || canvas.parentElement.clientWidth;
  const h = +canvas.getAttribute("height");
  canvas.width = w * dpr; canvas.height = h * dpr;
  canvas.style.height = h + "px";
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, w, h };
}
const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

function drawMainChart() {
  const canvas = $("#main-chart");
  if (!canvas || !canvas.offsetParent) return;
  const { ctx, w, h } = setupCanvas(canvas);
  const C = MOCK.chart, candles = C.candles;
  const padL = 8, padR = 52, padT = 10;
  const volH = 52, priceH = h - volH - 26 - padT;
  const n = candles.length;
  const xw = (w - padL - padR) / n;

  // Scale to the candles only — a far-away TP/SL must not flatten the price action.
  let lo = Math.min(...candles.map(c => c.low));
  let hi = Math.max(...candles.map(c => c.high));
  const pad = (hi - lo) * 0.05; lo -= pad; hi += pad;
  const y = (p) => padT + priceH - ((p - lo) / (hi - lo)) * priceH;
  const x = (i) => padL + i * xw + xw / 2;

  ctx.clearRect(0, 0, w, h);

  // gridlines + right axis labels
  ctx.strokeStyle = css("--grid"); ctx.fillStyle = css("--muted");
  ctx.font = "11px system-ui"; ctx.textAlign = "left"; ctx.lineWidth = 1;
  const steps = 5;
  for (let i = 0; i <= steps; i++) {
    const p = lo + (hi - lo) * i / steps, yy = y(p);
    ctx.beginPath(); ctx.moveTo(padL, yy); ctx.lineTo(w - padR, yy); ctx.stroke();
    ctx.fillText(p.toFixed(1), w - padR + 6, yy + 4);
  }

  // levels: SL / TP / SR (off-scale levels get an edge label instead of a line)
  C.levels.forEach(l => {
    const col = l.kind === "SL" ? css("--crit") : l.kind === "TP" ? css("--good") : css("--muted");
    if (l.price < lo || l.price > hi) {
      ctx.save();
      ctx.fillStyle = col; ctx.textAlign = "left";
      const yy = l.price > hi ? padT + 10 : padT + priceH - 4;
      ctx.fillText(`${l.kind} ${l.price.toFixed(1)} ${l.price > hi ? "↑" : "↓"}`, padL + 4, yy);
      ctx.restore();
      return;
    }
    const yy = y(l.price);
    ctx.save();
    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = l.kind === "SL" ? css("--crit") : l.kind === "TP" ? css("--good") : css("--muted");
    ctx.beginPath(); ctx.moveTo(padL, yy); ctx.lineTo(w - padR, yy); ctx.stroke();
    ctx.fillStyle = ctx.strokeStyle;
    ctx.fillText(`${l.kind} ${l.price.toFixed(1)}`, padL + 4, yy - 4);
    ctx.restore();
  });

  // volume bars
  const maxV = Math.max(...candles.map(c => c.vol));
  candles.forEach((c, i) => {
    const vh = (c.vol / maxV) * volH;
    ctx.fillStyle = c.close >= c.open ? "rgba(12,163,12,0.45)" : "rgba(208,59,59,0.45)";
    ctx.fillRect(x(i) - Math.max(1, xw * 0.35), padT + priceH + 8 + (volH - vh), Math.max(2, xw * 0.7), vh);
  });

  // candles (2px gap between bodies via 0.7 width)
  candles.forEach((c, i) => {
    const up = c.close >= c.open;
    const col = up ? css("--good") : css("--crit");
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x(i), y(c.high)); ctx.lineTo(x(i), y(c.low)); ctx.stroke();
    const bw = Math.max(2, xw * 0.7);
    const yo = y(c.open), yc = y(c.close);
    ctx.fillRect(x(i) - bw / 2, Math.min(yo, yc), bw, Math.max(1.5, Math.abs(yc - yo)));
  });

  // overlays: EMA20, EMA50, VWAP
  const line = (arr, col, dash) => {
    ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = 2;
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    arr.forEach((v, i) => i ? ctx.lineTo(x(i), y(v)) : ctx.moveTo(x(i), y(v)));
    ctx.stroke(); ctx.restore();
  };
  line(C.ema20, css("--s1"));
  line(C.ema50, css("--s2"));
  line(C.vwap, css("--s3"), [2, 3]);

  // trade markers
  C.trades.forEach(t => {
    const xx = x(t.i), yy = y(t.price);
    ctx.fillStyle = t.kind === "ENTRY" ? css("--good") : css("--s1");
    ctx.strokeStyle = css("--surface"); ctx.lineWidth = 2;
    ctx.beginPath();
    if (t.kind === "ENTRY") { ctx.moveTo(xx, yy + 14); ctx.lineTo(xx - 6, yy + 24); ctx.lineTo(xx + 6, yy + 24); }
    else { ctx.moveTo(xx, yy - 14); ctx.lineTo(xx - 6, yy - 24); ctx.lineTo(xx + 6, yy - 24); }
    ctx.closePath(); ctx.fill(); ctx.stroke();
  });

  $("#main-chart-title").textContent = `${C.symbol} · ${C.tf}`;
  $("#main-chart-legend").innerHTML = `
    <span class="key"><span class="swatch" style="background:${css("--s1")}"></span>EMA 20</span>
    <span class="key"><span class="swatch" style="background:${css("--s2")}"></span>EMA 50</span>
    <span class="key"><span class="swatch" style="background:${css("--s3")}"></span>VWAP</span>
    <span class="key"><span class="swatch" style="background:${css("--good")}"></span>▲ entry</span>
    <span class="key"><span class="swatch" style="background:${css("--s1")}"></span>▼ exit</span>`;

  // crosshair tooltip
  const tip = $("#main-chart-tip");
  canvas.onmousemove = (e) => {
    const rect = canvas.getBoundingClientRect();
    const i = Math.max(0, Math.min(n - 1, Math.round((e.clientX - rect.left - padL - xw / 2) / xw)));
    const c = candles[i];
    tip.style.display = "block";
    tip.style.left = Math.min(e.clientX - rect.left + 14, rect.width - 170) + "px";
    tip.style.top = (e.clientY - rect.top + 12) + "px";
    const trade = C.trades.find(t => t.i === i);
    tip.innerHTML = `<b>${C.symbol}</b> bar ${i} <span class="num">O ${c.open} H ${c.high} L ${c.low} C <b>${c.close}</b></span><br>` +
      `<span class="num">Vol ${c.vol} · EMA20 ${C.ema20[i]} · VWAP ${C.vwap[i]}</span>` +
      (trade ? `<br><b>${esc(trade.label)}</b>` : "");
  };
  canvas.onmouseleave = () => { tip.style.display = "none"; };
}

/* ============ Canvas: equity curve ============ */
function drawEquityChart() {
  const canvas = $("#equity-chart");
  if (!canvas || !canvas.offsetParent) return;
  const { ctx, w, h } = setupCanvas(canvas);
  const data = MOCK.equityCurve;
  const padL = 8, padR = 58, padT = 10, padB = 18;
  const lo = Math.min(...data.map(d => Math.min(d.equity, d.benchmark))) * 0.99;
  const hi = Math.max(...data.map(d => Math.max(d.equity, d.benchmark))) * 1.01;
  const x = (i) => padL + (i / (data.length - 1)) * (w - padL - padR);
  const y = (v) => padT + (h - padT - padB) - ((v - lo) / (hi - lo)) * (h - padT - padB);

  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = css("--grid"); ctx.fillStyle = css("--muted"); ctx.font = "11px system-ui";
  for (let i = 0; i <= 4; i++) {
    const v = lo + (hi - lo) * i / 4, yy = y(v);
    ctx.beginPath(); ctx.moveTo(padL, yy); ctx.lineTo(w - padR, yy); ctx.stroke();
    ctx.fillText("$" + Math.round(v / 1000) + "k", w - padR + 6, yy + 4);
  }
  const line = (key, col) => {
    ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.beginPath();
    data.forEach((d, i) => i ? ctx.lineTo(x(i), y(d[key])) : ctx.moveTo(x(i), y(d[key])));
    ctx.stroke();
  };
  line("benchmark", css("--s2"));
  line("equity", css("--s1"));

  $("#equity-legend").innerHTML = `
    <span class="key"><span class="swatch" style="background:${css("--s1")}"></span>Bot equity</span>
    <span class="key"><span class="swatch" style="background:${css("--s2")}"></span>Buy &amp; hold</span>`;

  const tip = $("#equity-tip");
  canvas.onmousemove = (e) => {
    const rect = canvas.getBoundingClientRect();
    const i = Math.max(0, Math.min(data.length - 1, Math.round((e.clientX - rect.left - padL) / (w - padL - padR) * (data.length - 1))));
    const d = data[i];
    tip.style.display = "block";
    tip.style.left = Math.min(e.clientX - rect.left + 14, rect.width - 160) + "px";
    tip.style.top = (e.clientY - rect.top + 12) + "px";
    tip.innerHTML = `<b>Session ${d.i}</b><br><span class="num">Equity <b>${fmtUsd(d.equity)}</b><br>Buy&amp;hold ${fmtUsd(d.benchmark)}</span>`;
  };
  canvas.onmouseleave = () => { tip.style.display = "none"; };
}

/* ============ Overview mini panels ============ */
function ovPerf() {
  const P = MOCK.performance.YTD;
  return `<dl class="kv">
    <dt>Win Rate</dt><dd class="num">${P.winRate}%</dd>
    <dt>Profit Factor</dt><dd class="num">${P.pf}</dd>
    <dt>Sharpe</dt><dd class="num">${P.sharpe}</dd>
    <dt>Expectancy</dt><dd class="num">${P.expectancy}R</dd>
    <dt>Trades (YTD)</dt><dd class="num">${P.trades}</dd></dl>`;
}
function ovRisk() {
  const r = MOCK.risk;
  return `<dl class="kv">
    <dt>Portfolio Risk</dt><dd class="num">${r.portfolioRiskPct}% / ${r.portfolioRiskMaxPct}%</dd>
    <dt>Daily Loss Limit</dt><dd class="num">${fmtUsd(r.dailyLossLimitUsd)}</dd>
    <dt>Drawdown</dt><dd class="num pnl-down">${r.currentDrawdownPct}%</dd>
    <dt>Exposure</dt><dd class="num">${r.exposurePct}%</dd>
    <dt>Guards</dt><dd>${r.killSwitches.length} armed</dd></dl>`;
}

/* ============ Wire it all up ============ */
function renderAll() {
  renderTopbar(); renderBanner(); renderTabs(); renderKpis();

  $("#ov-positions").innerHTML = positionsTable(false);
  $("#pos-count").textContent = `${MOCK.positions.length} open · ${MOCK.risk.maxOpenPositions} max`;
  $("#ov-ai").innerHTML = aiView();
  $("#ov-signals").innerHTML = MOCK.signals.slice(0, 3).map(signalCard).join("");
  $("#ov-scanner").innerHTML = scannerTable(5);
  $("#ov-perf").innerHTML = ovPerf();
  $("#ov-risk").innerHTML = ovRisk();
  $("#ov-health").innerHTML = healthStrip();
  $("#hb-hint").textContent = `heartbeat ${MOCK.system.lastHeartbeat} · uptime ${MOCK.system.uptime}`;

  $("#pg-positions").innerHTML = positionsTable(true);
  $("#pg-orders").innerHTML = ordersTable();
  $("#pg-signals").innerHTML = MOCK.signals.map(signalCard).join("");

  $("#pg-risk-meters").innerHTML = riskMeters();
  $("#pg-sector").innerHTML = sectorRows();
  $("#pg-corr").textContent = "Correlation risk: " + MOCK.risk.correlation.note + ".";
  $("#pg-guards").innerHTML = guardRows();
  $("#btn-closeall").onclick = () => { $("#ctl-msg").textContent = "Prototype: CLOSE ALL would require typed confirmation — no order sent."; };
  $("#btn-pause").onclick = () => { $("#ctl-msg").textContent = "Prototype: PAUSE would stop new entries only — no action taken."; };

  renderPerfFilters(); renderPerfTiles();
  $("#pg-strategies").innerHTML = strategiesTable();
  $("#pg-btlive").innerHTML = btLiveTable();
  $("#pg-journal").innerHTML = journalTable();
  $("#pg-scanner").innerHTML = scannerTable();

  $("#pg-ai-view").innerHTML = aiView();
  $("#pg-ai-veto").innerHTML = aiVetoList();
  $("#pg-calendar").innerHTML = calendarTable();
  $("#pg-headlines").innerHTML = headlineList();

  $("#pg-sysmetrics").innerHTML = sysMetrics();
  $("#sys-uptime").textContent = "uptime " + MOCK.system.uptime;
  $("#pg-services").innerHTML = servicesList();
  $("#pg-logs").innerHTML = logsTable();
  $("#pg-notifs").innerHTML = notifList();
  $("#notif-channels").textContent = MOCK.notifications.channels
    .map(c => `${c.name} ${c.enabled ? "on" : "off"}`).join(" · ");

  tickClock(); setInterval(tickClock, 1000);
  drawMainChart();
}

window.addEventListener("resize", () => { drawMainChart(); drawEquityChart(); });
document.addEventListener("DOMContentLoaded", renderAll);

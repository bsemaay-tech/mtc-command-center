const state = {
  status: null,
  snapshot: null,
  bars: [],
};

const byId = (id) => document.getElementById(id);

function setText(id, value) {
  const node = byId(id);
  if (node) node.textContent = value;
}

function activatePage(page) {
  document.querySelectorAll(".page").forEach((node) => node.classList.remove("active"));
  document.querySelectorAll(".nav").forEach((node) => node.classList.remove("active"));
  const pageNode = byId(`page-${page}`);
  const navNode = document.querySelector(`[data-page="${page}"]`);
  if (pageNode) pageNode.classList.add("active");
  if (navNode) navNode.classList.add("active");
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) throw new Error(`${path} ${response.status}`);
  return response.json();
}

async function refresh() {
  state.snapshot = await api("/api/snapshot");
  const barsPayload = await api("/api/bars?n=300");
  state.bars = barsPayload.bars || [];
  state.status = state.snapshot.status;
  renderAll();
}

function renderAll() {
  renderStatus();
  renderConfig();
  renderGates();
  renderTables();
  renderDecisionStream();
  renderJournal();
  renderLlm();
  renderSystem();
  renderPriceChart();
}

function renderStatus() {
  if (!state.status) return;
  const latestEquity = state.snapshot && state.snapshot.equity.length ? state.snapshot.equity[0] : null;
  const equity = typeof state.status.equity === "number" ? state.status.equity : latestEquity && latestEquity.equity;
  const dayPnl = typeof state.status.day_pnl === "number" ? state.status.day_pnl : latestEquity && latestEquity.realized_today;
  setText("connPill", state.status.exchange_conn || "mock");
  setText("modePill", (state.status.mode || state.status.network || "testnet").toUpperCase());
  setText("regimePill", state.status.regime || "BOTH");
  setText("stateText", state.status.state || "DISARMED");
  setText("equityValue", formatMoney(equity));
  setText("pnlValue", formatMoney(dayPnl));
  setText("nextBar", state.status.next_bar || nextBarLabel());
}

function renderConfig() {
  const config = state.snapshot ? state.snapshot.config : null;
  if (!config) return;
  byId("coinInput").value = config.broker.coin;
  byId("riskInput").value = config.risk.risk_pct_per_trade;
  byId("leverageInput").value = config.broker.leverage;
}

function renderGates() {
  const list = byId("gateList");
  if (!list) return;
  list.replaceChildren();
  const gates = state.snapshot.latest_gates.gate_results;
  if (!gates.length) {
    const item = document.createElement("li");
    item.textContent = "No signal yet - next bar pending";
    list.appendChild(item);
    return;
  }
  gates.forEach((gate) => {
    const item = document.createElement("li");
    item.textContent = `${gate.name}: ${gate.status}`;
    list.appendChild(item);
  });
}

function renderTables() {
  renderRows("positionsBody", state.snapshot.positions);
  renderRows("ordersBody", state.snapshot.orders);
}

function renderJournal() {
  renderRows("tradesBody", state.snapshot.trades);
  setText("decisionChain", "Select a trade");
}

function renderDecisionStream() {
  const list = byId("decisionStream");
  if (!list || !state.snapshot) return;
  list.replaceChildren();
  const decisions = state.snapshot.decisions || [];
  if (!decisions.length) {
    const item = document.createElement("li");
    item.textContent = "No decisions yet";
    list.appendChild(item);
    return;
  }
  decisions.slice(0, 10).forEach((decision) => {
    const item = document.createElement("li");
    item.textContent = `${decision.stage} - ${decision.coin} - ${decision.ts}`;
    list.appendChild(item);
  });
}

function renderLlm() {
  const config = state.snapshot.config;
  setText("llmRegime", state.status.regime || "BOTH");
  setText("vetoMode", config.llm.veto_enabled ? "ON" : "OFF");
  setText("llmCost", "$0.00");
  renderRows("directivesBody", []);
}

function renderSystem() {
  setText("systemNetwork", state.status.network || "testnet");
  setText("stateVersion", String(state.status.state_version));
  setText("dbStatus", "runtime");
  setText("hostIdentity", state.status.host_identity || "unknown");
  setText("releaseSha", state.status.release_sha || "unknown");
  setText("serviceHealth", state.status.service_health || "unknown");
  setText("serviceStartTs", state.status.service_start_ts || "--");
  setText("statusTs", state.status.status_ts || "--");
  renderRows("eventsBody", state.snapshot.events);
}

function renderRows(id, rows) {
  const body = byId(id);
  if (!body) return;
  body.replaceChildren();
  if (!rows.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.textContent = "No rows";
    tr.appendChild(td);
    body.appendChild(tr);
    return;
  }
  const keys = visibleKeys(rows);
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    keys.forEach((key) => {
      const td = document.createElement("td");
      td.textContent = formatCell(row[key]);
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
}

function visibleKeys(rows) {
  const seen = [];
  rows.forEach((row) => {
    Object.keys(row).forEach((key) => {
      if (!seen.includes(key) && seen.length < 6) seen.push(key);
    });
  });
  return seen;
}

function formatCell(value) {
  if (value === null || value === undefined || value === "") return "--";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(4);
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function formatMoney(value) {
  if (typeof value !== "number") return "--";
  return `$${value.toFixed(2)}`;
}

function renderPriceChart() {
  const box = byId("chartBox");
  if (!box || !state.bars.length) return;
  renderFallbackCandles(box);
}

function renderFallbackCandles(box) {
  const width = Math.max(box.clientWidth - 32, 320);
  const height = 230;
  const bars = state.bars.slice(-80);
  const highs = bars.map((bar) => bar.high);
  const lows = bars.map((bar) => bar.low);
  const max = Math.max(...highs);
  const min = Math.min(...lows);
  const span = Math.max(max - min, 1);
  box.replaceChildren();
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", String(height));
  bars.forEach((bar, index) => {
    const x = 8 + (index * (width - 16)) / Math.max(bars.length - 1, 1);
    const yHigh = scalePrice(bar.high, min, span, height);
    const yLow = scalePrice(bar.low, min, span, height);
    const yOpen = scalePrice(bar.open, min, span, height);
    const yClose = scalePrice(bar.close, min, span, height);
    const color = bar.close >= bar.open ? "#3fb950" : "#f85149";
    const wick = document.createElementNS("http://www.w3.org/2000/svg", "line");
    wick.setAttribute("x1", String(x));
    wick.setAttribute("x2", String(x));
    wick.setAttribute("y1", String(yHigh));
    wick.setAttribute("y2", String(yLow));
    wick.setAttribute("stroke", color);
    wick.setAttribute("stroke-width", "1");
    svg.appendChild(wick);
    const body = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    body.setAttribute("x", String(x - 3));
    body.setAttribute("y", String(Math.min(yOpen, yClose)));
    body.setAttribute("width", "6");
    body.setAttribute("height", String(Math.max(Math.abs(yClose - yOpen), 2)));
    body.setAttribute("fill", color);
    svg.appendChild(body);
  });
  box.appendChild(svg);
}

function scalePrice(value, min, span, height) {
  return 10 + ((maxPrice(min, span) - value) / span) * (height - 20);
}

function maxPrice(min, span) {
  return min + span;
}

function nextBarLabel() {
  if (!state.bars.length) return "--:--:--";
  const next = new Date((state.bars[state.bars.length - 1].time + 3600) * 1000);
  return `${String(next.getUTCHours()).padStart(2, "0")}:00 UTC`;
}

function connectWs() {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${scheme}://${window.location.host}/ws`);
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.topic === "snapshot") {
      state.snapshot = message.data;
      state.status = state.snapshot.status;
      state.bars = state.snapshot.bars ? state.snapshot.bars.bars : state.bars;
      renderAll();
      return;
    }
    if (message.topic === "status") {
      state.status = message.data;
      renderStatus();
      renderSystem();
      return;
    }
    window.clearTimeout(state.refreshTimer);
    state.refreshTimer = window.setTimeout(() => refresh().catch(() => {}), 50);
  });
}

async function sendState(path, confirmRequired = false) {
  const headers = {};
  if (confirmRequired && state.status) headers["X-Confirm"] = String(state.status.state_version);
  await api(path, { method: "POST", headers });
  await refresh();
}

document.querySelectorAll(".nav").forEach((button) => {
  button.addEventListener("click", () => activatePage(button.dataset.page));
});

byId("armButton").addEventListener("click", () => sendState("/api/arm", true));
byId("disarmButton").addEventListener("click", () => sendState("/api/disarm"));
byId("killButton").addEventListener("click", () => sendState("/api/kill?flatten=false"));

refresh().then(connectWs).catch((error) => {
  setText("stateText", `ERROR: ${error.message}`);
});

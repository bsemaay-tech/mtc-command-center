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
  if (page === "help") ensureHelp();
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
  setText("llmRegime", state.status.regime || "BOTH");
  setText("vetoMode", "N/A");
  setText("llmCost", "$0.00");
  renderRows("directivesBody", []);
}

function renderSystem() {
  setText("systemNetwork", state.status.network || "testnet");
  setText("stateVersion", String(state.status.state_version));
  setText("dbStatus", "runtime");
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

/* ---------------------------------------------------------------------------
 * Help / System Map
 *
 * Everything below renders from ONE machine-readable knowledge source
 * (/static/help_map.json), which is also what a future AI agent reads. No
 * explanatory fact is hardcoded here: this file only decides layout. Every
 * value reaches the document through textContent, never through markup, which
 * keeps the existing static safety contract intact.
 * ------------------------------------------------------------------------- */

const HELP_SOURCE = "/static/help_map.json";

const help = {
  data: null,
  status: "idle", // idle | loading | ready | failed
  technical: false,
  selected: null,
  inbound: new Map(),
};

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function helpComponent(id) {
  if (!help.data) return null;
  return help.data.components.find((component) => component.id === id) || null;
}

function helpStatusMeta(id) {
  const found = help.data.statuses.find((status) => status.id === id);
  return found || { id, label: id, tone: "muted", meaning: "" };
}

function helpKindMeta(id) {
  const kinds = help.data.connection_kinds || [];
  const found = kinds.find((kind) => kind.id === id);
  return found || { id, label: id, meaning: "" };
}

function helpStatusBadge(statusId) {
  const meta = helpStatusMeta(statusId);
  const badge = el("span", `help-badge tone-${meta.tone}`, meta.label);
  badge.title = meta.meaning;
  return badge;
}

function ensureHelp() {
  if (help.status === "loading" || help.status === "ready") return;
  help.status = "loading";
  setText("helpSubtitle", "Loading the system map...");
  fetch(HELP_SOURCE)
    .then((response) => {
      if (!response.ok) throw new Error(`${HELP_SOURCE} ${response.status}`);
      return response.json();
    })
    .then((payload) => {
      help.data = payload;
      help.status = "ready";
      buildHelpIndex();
      renderHelp();
    })
    .catch((error) => {
      help.status = "failed";
      setText(
        "helpSubtitle",
        `The system map could not be loaded (${error.message}). The rest of the dashboard is unaffected.`,
      );
    });
}

function buildHelpIndex() {
  help.inbound = new Map();
  help.data.components.forEach((component) => {
    (component.connections || []).forEach((connection) => {
      if (!help.inbound.has(connection.to)) help.inbound.set(connection.to, []);
      help.inbound.get(connection.to).push({
        from: component.id,
        label: connection.label,
        kind: connection.kind,
      });
    });
  });
}

function renderHelp() {
  setText("helpSubtitle", help.data.subtitle);
  setText("helpUpdated", `updated ${help.data.updated}`);
  setText("helpCount", `${help.data.components.length} components`);
  renderHelpLegend();
  renderHelpNotes();
  renderHelpIdentities();
  renderHelpPlanes();
  renderHelpFlows();
  renderHelpReadiness();
  renderHelpGlossary();
}

function renderHelpLegend() {
  const statusBox = byId("helpLegendStatus");
  statusBox.replaceChildren();
  help.data.statuses.forEach((status) => {
    const row = el("div", "help-legend-row");
    row.appendChild(helpStatusBadge(status.id));
    row.appendChild(el("span", "help-legend-text", status.meaning));
    statusBox.appendChild(row);
  });

  const kindBox = byId("helpLegendKinds");
  kindBox.replaceChildren();
  (help.data.connection_kinds || []).forEach((kind) => {
    const row = el("div", "help-legend-row");
    row.appendChild(el("span", `help-kind kind-${kind.id}`, kind.label));
    row.appendChild(el("span", "help-legend-text", kind.meaning));
    kindBox.appendChild(row);
  });
}

function renderHelpNotes() {
  fillList("helpHowTo", help.data.how_to_read);
  fillList("helpTruthRules", help.data.truth_rules);
}

function fillList(id, items) {
  const list = byId(id);
  if (!list) return;
  list.replaceChildren();
  (items || []).forEach((item) => list.appendChild(el("li", null, item)));
}

function renderHelpIdentities() {
  const box = byId("helpIdentities");
  box.replaceChildren();
  (help.data.identities || []).forEach((identity) => {
    const card = el("article", "help-identity");
    card.appendChild(el("strong", null, identity.name));
    card.appendChild(el("p", null, identity.authority));
    card.appendChild(helpLinkButton(identity.component, "Open this component"));
    box.appendChild(card);
  });
}

function helpLinkButton(componentId, label) {
  const target = helpComponent(componentId);
  const button = el("button", "help-link", label || (target ? target.name : componentId));
  button.type = "button";
  button.addEventListener("click", () => selectHelpComponent(componentId, true));
  return button;
}

function renderHelpPlanes() {
  const box = byId("helpPlanes");
  box.replaceChildren();
  help.data.planes.forEach((plane) => {
    const section = el("section", "help-plane");
    section.appendChild(el("h2", null, plane.name));
    section.appendChild(el("p", "help-plane-summary", plane.summary));
    section.appendChild(el("p", "help-plane-boundary", `Boundary: ${plane.boundary}`));
    const grid = el("div", "help-grid");
    help.data.components
      .filter((component) => component.plane === plane.id)
      .forEach((component) => grid.appendChild(helpComponentButton(component)));
    section.appendChild(grid);
    box.appendChild(section);
  });
}

function helpComponentButton(component) {
  const meta = helpStatusMeta(component.status);
  const button = el("button", `help-node tone-${meta.tone}`);
  button.type = "button";
  button.dataset.component = component.id;
  button.setAttribute("aria-pressed", String(help.selected === component.id));
  button.setAttribute("aria-controls", "helpDetail");
  const head = el("span", "help-node-head");
  head.appendChild(el("span", "help-node-name", component.name));
  head.appendChild(helpStatusBadge(component.status));
  button.appendChild(head);
  button.appendChild(el("span", "help-node-line", component.one_liner));
  button.addEventListener("click", () => selectHelpComponent(component.id, true));
  return button;
}

function selectHelpComponent(componentId, moveFocus) {
  const component = helpComponent(componentId);
  if (!component) return;
  help.selected = componentId;
  document.querySelectorAll(".help-node").forEach((node) => {
    node.setAttribute("aria-pressed", String(node.dataset.component === componentId));
  });
  renderHelpDetail(component);
  if (moveFocus) {
    const panel = byId("helpDetail");
    panel.focus();
    panel.scrollIntoView({ block: "nearest" });
  }
}

function renderHelpDetail(component) {
  const empty = byId("helpDetailEmpty");
  if (empty) empty.hidden = true;
  const body = byId("helpDetailBody");
  body.replaceChildren();

  const header = el("header", "help-detail-head");
  const title = el("h2", null, component.name);
  header.appendChild(title);
  header.appendChild(helpStatusBadge(component.status));
  body.appendChild(header);

  const plane = help.data.planes.find((item) => item.id === component.plane);
  body.appendChild(el("p", "help-detail-plane", plane ? plane.name : component.plane));
  body.appendChild(el("p", "help-detail-line", component.one_liner));

  body.appendChild(detailSection("Current status", null, [component.status_detail]));
  body.appendChild(detailSection("What it is for", component.purpose, null));
  body.appendChild(detailSection("What it does", null, component.does));
  body.appendChild(detailSection("What it does NOT do", null, component.does_not, "help-negative"));
  body.appendChild(renderHelpConnections(component));
  body.appendChild(detailSection("Responsibility boundaries and overlaps", null, component.boundaries));
  body.appendChild(detailSection("Safety notes", null, component.safety, "help-safety"));
  body.appendChild(detailSection("Source paths", null, component.sources, "help-paths"));
  if (help.technical) {
    body.appendChild(detailSection("Technical detail", null, component.technical, "help-technical"));
  }
}

function detailSection(heading, paragraph, items, className) {
  const section = el("section", className ? `help-section ${className}` : "help-section");
  section.appendChild(el("h3", null, heading));
  if (paragraph) section.appendChild(el("p", null, paragraph));
  if (items && items.length) {
    const list = el("ul");
    items.forEach((item) => list.appendChild(el("li", null, item)));
    section.appendChild(list);
  }
  return section;
}

function renderHelpConnections(component) {
  const section = el("section", "help-section");
  section.appendChild(el("h3", null, "What connects to it"));

  const outgoing = component.connections || [];
  section.appendChild(el("h4", null, "From this component"));
  section.appendChild(connectionList(outgoing.map((connection) => ({
    other: connection.to,
    label: connection.label,
    kind: connection.kind,
  }))));

  const inbound = help.inbound.get(component.id) || [];
  section.appendChild(el("h4", null, "Toward this component"));
  section.appendChild(connectionList(inbound.map((connection) => ({
    other: connection.from,
    label: connection.label,
    kind: connection.kind,
  }))));
  return section;
}

function connectionList(entries) {
  if (!entries.length) return el("p", "help-empty", "None recorded.");
  const list = el("ul", "help-connections");
  entries.forEach((entry) => {
    const target = helpComponent(entry.other);
    const item = el("li", `help-connection kind-${entry.kind}`);
    item.appendChild(el("span", "help-kind", helpKindMeta(entry.kind).label));
    item.appendChild(el("span", "help-connection-label", entry.label));
    item.appendChild(helpLinkButton(entry.other, target ? target.name : entry.other));
    list.appendChild(item);
  });
  return list;
}

function renderHelpFlows() {
  const box = byId("helpFlows");
  box.replaceChildren();
  help.data.flows.forEach((flow) => {
    const article = el("article", `help-flow kind-${flow.kind}`);
    article.appendChild(el("h3", null, flow.title));
    const chain = el("div", "help-flow-chain");
    flow.steps.forEach((step, index) => {
      if (index > 0) {
        chain.appendChild(el("span", "help-flow-arrow", flow.kind === "blocked" ? "X" : "->"));
      }
      const chip = el("button", `help-chip state-${step.state}`);
      chip.type = "button";
      chip.appendChild(el("span", "help-chip-label", step.label));
      if (step.state !== "current") {
        chip.appendChild(el("span", "help-chip-state", step.state === "blocked" ? "NO AUTHORITY" : "NOT IN PLACE"));
      }
      chip.addEventListener("click", () => selectHelpComponent(step.component, true));
      chain.appendChild(chip);
    });
    article.appendChild(chain);
    article.appendChild(el("p", "help-flow-note", flow.note));
    box.appendChild(article);
  });
}

function renderHelpReadiness() {
  const box = byId("helpReadiness");
  box.replaceChildren();
  help.data.readiness.forEach((row) => {
    const card = el("article", "help-readiness-card");
    const head = el("div", "help-readiness-head");
    head.appendChild(el("strong", null, row.area));
    head.appendChild(helpStatusBadge(row.status));
    card.appendChild(head);
    const built = el("div", "help-readiness-cell");
    built.appendChild(el("h4", null, "Built now"));
    built.appendChild(el("p", null, row.built_now));
    card.appendChild(built);
    const todo = el("div", "help-readiness-cell help-negative");
    todo.appendChild(el("h4", null, "Still required"));
    todo.appendChild(el("p", null, row.still_required));
    card.appendChild(todo);
    box.appendChild(card);
  });
}

function renderHelpGlossary() {
  const box = byId("helpGlossary");
  box.replaceChildren();
  (help.data.glossary || []).forEach((entry) => {
    box.appendChild(el("dt", null, entry.term));
    box.appendChild(el("dd", null, entry.plain));
  });
}

function toggleHelpTechnical() {
  help.technical = !help.technical;
  const button = byId("helpDetailToggle");
  button.setAttribute("aria-pressed", String(help.technical));
  button.textContent = `Technical detail: ${help.technical ? "on" : "off"}`;
  if (help.selected) {
    const component = helpComponent(help.selected);
    if (component) renderHelpDetail(component);
  }
}

byId("helpDetailToggle").addEventListener("click", toggleHelpTechnical);

document.querySelectorAll(".nav").forEach((button) => {
  button.addEventListener("click", () => activatePage(button.dataset.page));
});

byId("armButton").addEventListener("click", () => sendState("/api/arm", true));
byId("disarmButton").addEventListener("click", () => sendState("/api/disarm"));
byId("killButton").addEventListener("click", () => sendState("/api/kill?flatten=false"));

refresh().then(connectWs).catch((error) => {
  setText("stateText", `ERROR: ${error.message}`);
});

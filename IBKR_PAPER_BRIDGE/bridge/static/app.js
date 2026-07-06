const state = {
  status: null,
  snapshot: null,
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
  state.status = state.snapshot.status;
  renderStatus();
  renderConfig();
  renderGates();
  renderTables();
}

function renderStatus() {
  if (!state.status) return;
  setText("connPill", state.status.exchange_conn || "mock");
  setText("modePill", (state.status.network || "testnet").toUpperCase());
  setText("regimePill", state.status.regime || "BOTH");
  setText("stateText", state.status.state || "DISARMED");
  setText("equityValue", "--");
  setText("pnlValue", "--");
  setText("nextBar", "--:--:--");
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
  }
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

refresh().catch((error) => {
  setText("stateText", `ERROR: ${error.message}`);
});

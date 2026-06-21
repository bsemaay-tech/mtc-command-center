/* ============================================================
   MTC Strategy Intelligence Command Center — read-only frontend
   Ports the Google / Lovable dark Strategy Intelligence reference
   into a vanilla SPA over the read-only snapshot API.
   Read-only: no run-trigger, write-back, or trading logic lives here.
   ============================================================ */

const state = {
  snapshot: null,
  health: null,
  currentRoute: "home",
  selectedStrategyId: null,
  detailSection: "all",
  explorerScope: "global",
  explorerStrategyId: null,
  selectedReportPath: null,
  detailCards: {},
};

const NIGHT_CONTRACT = [
  "run_plan.json", "run_status.json", "progress.json", "heartbeat.json",
  "artifact_index.json", "summary.json", "backtest_profile_result.json",
  "top_results.json", "leaderboard_delta.json", "benchmark_update_candidate.json",
  "morning_report.md",
];

const PROFILES = ["SOURCE_NAKED", "RISK_NORMALIZED", "MTC_LIGHT", "FULL_MTC_CANDIDATE"];

const NAV = [
  { id: "home", label: "Home / Command Center", icon: "home", title: "Command Center Home", sub: "Monitor pipeline, benchmarks, backtest evidence, and next actions." },
  { id: "pipeline", label: "Strategy Pipeline", icon: "layers", title: "Strategy Pipeline", sub: "Full strategy journey and gate status." },
  { id: "registry", label: "Strategy Registry", icon: "file", title: "Strategy Registry", sub: "Searchable strategy and source catalog." },
  { id: "intelligence", label: "Strategy Intelligence", icon: "cpu", title: "Strategy Intelligence", sub: "Per-strategy evaluation dossier." },
  { id: "backtest-planner", label: "Backtest Planner", icon: "beaker", title: "Backtest Planner", sub: "Prepare run_plan.json (read-only review)." },
  { id: "backtest-runs", label: "Backtest Runs", icon: "settings", title: "Backtest Runs", sub: "Run history and heartbeat." },
  { id: "result-explorer", label: "Backtest Result Explorer", icon: "bar", title: "Backtest Result Explorer", sub: "Bucketed results and benchmark analysis." },
  { id: "leaderboard", label: "Strategy Leaderboard", icon: "trend", title: "Strategy Leaderboard", sub: "Best strategies by category / profile / timeframe." },
  { id: "paper-trading", label: "Paper Trading", icon: "activity", title: "Paper Trading", sub: "Readiness and locked candidates." },
  { id: "ai-knowledge", label: "AI Knowledge Base", icon: "cpu", title: "AI Knowledge Base", sub: "Reusable components and insights." },
  { id: "artifacts", label: "Advanced Artifacts", icon: "db", title: "Advanced Artifacts", sub: "Data and artifact health." },
  { id: "diagnostics", label: "Diagnostics", icon: "shield", title: "Diagnostics", sub: "System health and coverage." },
  { id: "reports", label: "Reports", icon: "info", title: "Reports", sub: "Morning summaries and audits." },
  { id: "read-model", label: "Read Model / Data Model", icon: "db", title: "Read Model / Data Model", sub: "Data contracts and snapshot keys." },
];
const NAV_BY_ID = Object.fromEntries(NAV.map((n) => [n.id, n]));

const DETAIL_SECTIONS = [
  { id: "all", label: "All Document Sections", icon: "layers", anchor: null },
  { id: "overview", label: "1. Strategy Overview", icon: "file", anchor: "sec-overview" },
  { id: "gate1", label: "2. Gate 1 / Gate 1B Assessment", icon: "shield", anchor: "sec-gate1" },
  { id: "verdict", label: "3. AI Verdict & Reuse Notes", icon: "cpu", anchor: "sec-verdict" },
  { id: "evidence", label: "4. Backtest Plan & Evidence", icon: "beaker", anchor: "sec-evidence" },
  { id: "explorer", label: "5. Backtest Result Explorer", icon: "bar", anchor: "sec-explorer" },
  { id: "paper", label: "6. Paper Trading Readiness", icon: "activity", anchor: "sec-paper" },
  { id: "advanced", label: "7. Advanced Technical Details", icon: "settings", anchor: "sec-advanced" },
];

const PAGE_FEEDS = [
  ["Home / Command Center", "candidate_pipeline, scorecards, backtest_status, report_manifest, file_diagnostics"],
  ["Strategy Pipeline", "candidate_pipeline.rows"],
  ["Strategy Registry", "strategy_registry.candidates"],
  ["Strategy Intelligence", "candidate_pipeline.rows[].scorecard_v2, expert_quantlens_verdict, canonical, strategy_registry"],
  ["Backtest Planner", "night_artifacts.run_plans, candidate_pipeline"],
  ["Backtest Runs", "night_artifacts.run_status, backtest_status.runs, overnight_heartbeat"],
  ["Backtest Result Explorer", "night_artifacts.profile_results, scorecards.cards"],
  ["Strategy Leaderboard", "night_artifacts.profile_results, night_artifacts.leaderboard_delta, scorecards.cards"],
  ["Paper Trading", "candidate_pipeline.rows, scorecards.gate_summary"],
  ["AI Knowledge Base", "strategy_registry.candidate_kind, strategy_research"],
  ["Advanced Artifacts", "night_artifacts (run_plans, run_status, artifact_index, profile_results, top_results, leaderboard_delta, benchmark_update_candidates)"],
  ["Diagnostics", "healthz, file_diagnostics, night_artifacts.summary"],
  ["Reports", "report_manifest.reports"],
  ["Read Model / Data Model", "all snapshot top-level keys"],
];

const ICON = {
  home: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
  layers: '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
  file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
  cpu: '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
  beaker: '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-2.82 1.17V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 8 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 3.6 14H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 8.6l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 10 3.6V3a2 2 0 1 1 4 0v.09A1.65 1.65 0 0 0 16 4.6l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 20.4 10H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
  bar: '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
  trend: '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
  activity: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
  db: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  info: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
  back: '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
  target: '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
  lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
};
function icon(name) {
  return `<svg class="ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICON[name] || ICON.info}</svg>`;
}

/* ---------------- bootstrap ---------------- */
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));

document.addEventListener("DOMContentLoaded", () => {
  renderSidebar();
  loadDashboard(false);
});

async function loadDashboard(forceRefresh) {
  setNotice("");
  try {
    const [health, snapshot] = await Promise.all([
      fetchJson("/healthz"),
      fetchJson(forceRefresh ? "/api/snapshot?refresh=1" : "/api/snapshot"),
    ]);
    state.health = health;
    state.snapshot = snapshot;
    const modeEl = $("#modeLabel");
    if (modeEl) modeEl.textContent = snapshot.mode || "read_only";
    renderSidebar();
    renderCurrentView();
  } catch (error) {
    setNotice(error.message || String(error));
    renderHeader();
  }
}

async function fetchJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `${url} returned ${response.status}`);
  return payload;
}

/* ---------------- navigation ---------------- */
function navigate(route, params = {}) {
  state.currentRoute = route;
  if (params.strategyId) state.selectedStrategyId = params.strategyId;
  if (route === "intelligence") state.detailSection = "all";
  if (route === "result-explorer" && !params.keepScope) {
    state.explorerScope = "global";
    state.explorerStrategyId = null;
  }
  renderSidebar();
  renderCurrentView();
  window.scrollTo({ top: 0 });
}
window.navigate = navigate;

function openStrategy(id) { navigate("intelligence", { strategyId: id }); }
window.openStrategy = openStrategy;

/* Lazy-load full scorecard gate detail (sub_scores/notes) for one strategy on open.
   The default snapshot ships summary cards only; full detail comes from the read-only
   /api/scorecard-detail endpoint. Failures degrade gracefully to summary-only. */
function loadStrategyDetail(id) {
  if (!id) return;
  const entry = state.detailCards[id];
  if (entry && (entry.status === "loading" || entry.status === "ok" || entry.status === "empty")) return;
  state.detailCards[id] = { status: "loading", cards: [] };
  // Read the JSON body even on 404: the detail endpoint returns count=0/cards=[] for an
  // unknown strategy, which is an *empty* detail (summary-only), not a hard server error.
  fetch("/api/scorecard-detail?strategy_id=" + encodeURIComponent(id), { cache: "no-store" })
    .then((res) => res.json().then((body) => ({ res, body })))
    .then(({ res, body }) => {
      const cards = Array.isArray(body.cards) ? body.cards : [];
      const emptyDetail = body && Number(body.count || 0) === 0 && cards.length === 0;
      if ((res.status === 404 && emptyDetail) || (res.ok && emptyDetail)) {
        state.detailCards[id] = { status: "empty", cards: [] };
      } else if (res.ok) {
        state.detailCards[id] = { status: "ok", cards };
      } else {
        state.detailCards[id] = { status: "error", cards: [] };
      }
    })
    .catch(() => {
      state.detailCards[id] = { status: "error", cards: [] };
    })
    .finally(() => {
      if (state.currentRoute === "intelligence" && state.selectedStrategyId === id) {
        renderCurrentView();
      }
    });
}

/* Best full detail card for a strategy (highest gate2 score), or null if not loaded. */
function detailBestCard(id) {
  const entry = state.detailCards[id];
  if (!entry || entry.status !== "ok" || !entry.cards.length) return null;
  return entry.cards.slice().sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0))[0] || null;
}

function openExplorerForStrategy(id) {
  state.explorerScope = "strategy";
  state.explorerStrategyId = id;
  state.currentRoute = "result-explorer";
  renderSidebar();
  renderCurrentView();
  window.scrollTo({ top: 0 });
}
window.openExplorerForStrategy = openExplorerForStrategy;

function scrollToSection(sectionId) {
  state.detailSection = sectionId;
  renderSidebar();
  const sec = DETAIL_SECTIONS.find((s) => s.id === sectionId);
  if (!sec || !sec.anchor) { window.scrollTo({ top: 0, behavior: "smooth" }); return; }
  const el = document.getElementById(sec.anchor);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}
window.scrollToSection = scrollToSection;

/* ---------------- sidebar ---------------- */
function renderSidebar() {
  const nav = $("#sidebarNav");
  if (!nav) return;
  if (state.currentRoute === "intelligence") {
    const sel = state.selectedStrategyId || defaultStrategyId();
    nav.innerHTML = `
      <button class="route back-btn" type="button" onclick="navigate('home')">${icon("back")}<span class="label">Back to Main Menu</span></button>
      <div class="nav-caption teal">Strategy Intelligence</div>
      <div class="nav-sub">Selected: ${esc(sel || "—")}</div>
      ${DETAIL_SECTIONS.map((s) => `
        <button class="route ${state.detailSection === s.id ? "is-active" : ""}" type="button" onclick="scrollToSection('${s.id}')">
          ${icon(s.icon)}<span class="label">${esc(s.label)}</span>
        </button>`).join("")}
    `;
  } else {
    nav.innerHTML = `
      <div class="nav-caption">Main Menu</div>
      ${NAV.map((n) => `
        <button class="route ${state.currentRoute === n.id ? "is-active" : ""}" type="button" onclick="navigate('${n.id}')">
          ${icon(n.icon)}<span class="label">${esc(n.label)}</span>
        </button>`).join("")}
    `;
  }
}

/* ---------------- header ---------------- */
function renderHeader() {
  const bar = $("#topbar");
  if (!bar) return;
  const meta = NAV_BY_ID[state.currentRoute] || NAV_BY_ID.home;
  let title = meta.title;
  let sub = meta.sub;
  if (state.currentRoute === "intelligence") {
    const id = state.selectedStrategyId || defaultStrategyId();
    sub = `${id || "No strategy selected"} · evaluation dossier`;
  }
  const healthy = state.health && state.health.overall_ok;
  bar.innerHTML = `
    <div>
      <div class="topbar-title">
        <h2>${esc(title)}</h2>
        <span class="status-pill ${state.health ? (healthy ? "ok" : "bad") : "neutral"}">${state.health ? (healthy ? "System Healthy" : "Check Health") : "checking"}</span>
      </div>
      <p class="topbar-sub">${esc(sub)}</p>
    </div>
    <div class="topbar-actions">
      <span class="status-pill neutral">Local Engine: Idle</span>
      <span class="status-pill neutral">Token Mode: Local / AI optional</span>
      <button class="btn mini" type="button" onclick="loadDashboard(true)">Refresh Snapshot</button>
    </div>
  `;
}

/* ---------------- render dispatch ---------------- */
function renderCurrentView() {
  renderHeader();
  const c = $("#viewContainer");
  const renderers = {
    home: renderHome,
    pipeline: renderPipeline,
    registry: renderRegistry,
    intelligence: renderIntelligence,
    "backtest-planner": renderPlanner,
    "backtest-runs": renderRuns,
    "result-explorer": renderResultExplorer,
    leaderboard: renderLeaderboard,
    "paper-trading": renderPaperTrading,
    "ai-knowledge": renderKnowledge,
    artifacts: renderArtifacts,
    diagnostics: renderDiagnostics,
    reports: renderReports,
    "read-model": renderReadModel,
  };
  (renderers[state.currentRoute] || renderHome)(c);
}

function setNotice(msg) {
  const n = $("#notice");
  if (!n) return;
  if (!msg) { n.hidden = true; n.textContent = ""; return; }
  n.hidden = false; n.textContent = msg;
}

function toast(msg) {
  const t = $("#toast");
  if (!t) return;
  t.innerHTML = `<div class="tt">System Notification</div><div class="tm">${esc(msg)}</div>`;
  t.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { t.hidden = true; }, 3800);
}
window.toast = toast;

/* ---------------- generic helpers ---------------- */
function esc(v) {
  if (v === null || v === undefined) return "";
  const d = document.createElement("div");
  d.textContent = String(v);
  return d.innerHTML;
}
function spaced(v) { return String(v || "").replace(/_/g, " "); }
function titleCase(v) { return spaced(v).replace(/\b\w/g, (c) => c.toUpperCase()); }
function num(v) { const n = Number(v); return Number.isFinite(n) ? n.toLocaleString() : String(v); }
function baseId(v) { return String(v || "").split("|")[0]; }

/* Explicit, contextual empty-state markup. */
function missing(kind) { return `<span class="value-muted">${esc(kind)}</span>`; }
const M = {
  meta: "Missing source metadata",
  artifact: "Artifact missing",
  reader: "Reader not implemented",
  snapshot: "Not present in current snapshot",
  rulefreeze: "Pending rule freeze",
  runplan: "Pending run_plan.json",
  notextracted: "Not extracted from source",
};

function infoCard(label, value, opts = {}) {
  const v = (value === null || value === undefined || value === "" ) ? missing(opts.empty || M.snapshot) : esc(value);
  return `<div class="info-card ${opts.span2 ? "span-2" : ""}"><span>${esc(label)}</span><strong>${v}</strong></div>`;
}
function defRow(k, v, empty) {
  const val = (v === null || v === undefined || v === "") ? missing(empty || M.snapshot) : esc(v);
  return `<div class="def-row"><span class="k">${esc(k)}</span><span class="v">${val}</span></div>`;
}
function emptyState(msg) { return `<div class="empty-state">${esc(msg)}</div>`; }

function badge(text, cls = "neutral") { return `<span class="badge ${cls}">${esc(text)}</span>`; }

function gateTone(status) {
  const t = String(status || "").toLowerCase();
  if (t.includes("ok") || t.includes("pass") || t.includes("certified") || t.includes("done")) return "ok";
  if (t.includes("fail")) return "bad";
  if (t.includes("incomplete") || t.includes("absent") || t.includes("locked") || t.includes("pending") || t.includes("review")) return "locked";
  return "neutral";
}
function scoreClass(s) {
  const n = Number(s);
  if (!Number.isFinite(n)) return "na";
  return n >= 85 ? "hi" : n >= 65 ? "mid" : "lo";
}

/* ---------------- snapshot accessors ---------------- */
function snap() { return state.snapshot || {}; }
function pipelineRows() { const p = snap().candidate_pipeline || {}; return Array.isArray(p.rows) ? p.rows : []; }
function registryEntries() {
  const r = snap().strategy_registry || {};
  return [].concat(Array.isArray(r.candidates) ? r.candidates : [], Array.isArray(r.strategies) ? r.strategies : []);
}
function scorecardCards() { const s = snap().scorecards || {}; return Array.isArray(s.cards) ? s.cards : []; }
function backtestRuns() { const b = snap().backtest_status || {}; return Array.isArray(b.runs) ? b.runs : []; }
function reportItems() { const m = snap().report_manifest || {}; return Array.isArray(m.reports) ? m.reports : []; }
function diagnosticItems() {
  const d = snap().file_diagnostics || {};
  return Object.entries(d).map(([key, v]) => ({ key, ...(v || {}) }));
}
function nightArtifacts() { return snap().night_artifacts || {}; }
function naList(key) { const v = nightArtifacts()[key]; return Array.isArray(v) ? v : []; }
function profileRows() { return naList("profile_results"); }
function profileRowsFor(profile) { return profileRows().filter((r) => r.profile === profile); }
function profileRowsForStrategy(id) { const t = baseId(id); return profileRows().filter((r) => baseId(r.strategy_id) === t); }
function usableRunPlans() { return naList("run_plans").filter((r) => r.state === "usable" || r.state === "incomplete"); }
function runPlanForStrategy(id) {
  const t = baseId(id);
  return usableRunPlans().find((r) => {
    const d = r.data || {};
    const ids = Array.isArray(d.strategy_ids) ? d.strategy_ids : (d.strategy_id ? [d.strategy_id] : []);
    return ids.some((x) => baseId(x) === t);
  }) || null;
}
function usableRunStatus() { return naList("run_status").filter((r) => r.state === "usable" || r.state === "incomplete"); }
function rowId(r) { return r.id || r.strategy_id || r.candidate_id || r.base_strategy_id || ""; }
function findRow(id) {
  const t = String(id || "");
  const rows = pipelineRows();
  return rows.find((r) => rowId(r) === t) || rows.find((r) => baseId(rowId(r)) === baseId(t)) || null;
}
function findRegistry(id) {
  const t = baseId(id);
  return registryEntries().find((r) => baseId(rowId(r)) === t) || null;
}
function cardsForStrategy(id) {
  const t = baseId(id);
  return scorecardCards().filter((c) => baseId(c.base_strategy_id || c.strategy_id) === t);
}
function defaultStrategyId() {
  const r = pipelineRows()[0];
  return r ? rowId(r) : (registryEntries()[0] ? rowId(registryEntries()[0]) : "");
}

/* Build a normalized strategy model from the pipeline row (richest source). */
function strategyModel(id) {
  const row = findRow(id) || {};
  const reg = findRegistry(id) || {};
  const v2 = row.scorecard_v2 || bestCardV2(id) || {};
  const canonical = row.canonical || {};
  const desc = row.description || {};
  const statuses = (v2.gate_summary && v2.gate_summary.statuses) || {};
  const detailCard = detailBestCard(id);
  const detailEntry = state.detailCards[id];
  const gate = (key, scoreObj) => {
    const full = detailCard && detailCard[key];
    return {
      status: statuses[key] || "INCOMPLETE",
      score: scoreObj && scoreObj.score != null ? scoreObj.score : null,
      max: (scoreObj && scoreObj.max) || 100,
      // Full sub_scores come from the lazy-loaded detail card; fall back to any inline
      // sub_scores still present, else empty (UI shows loading/summary-only state).
      sub: (full && full.sub_scores) || (scoreObj && scoreObj.sub_scores) || [],
    };
  };
  return {
    id: rowId(row) || id,
    baseId: baseId(rowId(row) || id),
    row, reg, v2, canonical, desc,
    displayName: row.strategy_display_name || v2.strategy_display_name || desc.family || reg.title || titleCase(baseId(id)),
    thesis: desc.what || row.notes || M.notextracted,
    family: desc.family || null,
    sourceUrl: row.source_url || reg.source_url || null,
    sourceTitle: reg.title || reg.name || row.name || null,
    sourceType: reg.market_type || row.source_type || null,
    transcript: reg.transcript_path || row.transcript_path || null,
    marketCondition: row.market_condition || reg.market_condition || null,
    definedTf: canonical.defined_tf || row.timeframe || reg.timeframe || null,
    testedTf: canonical.tested_tf || null,
    tfMismatch: !!canonical.tf_mismatch,
    symbol: row.symbol || v2.symbol || canonical.symbol || null,
    rules: { entry: desc.entry, exit: desc.exit, avoid: desc.avoid },
    score: row.score != null ? row.score : (row.scorecard && row.scorecard.total),
    scoreBand: (row.scorecard && row.scorecard.band) || row.score_band,
    scorecard: row.scorecard || null,
    classification: row.classification || {},
    expert: row.expert_quantlens_verdict || null,
    directional: row.directional_research || null,
    candidateKind: Array.isArray(reg.candidate_kind) ? reg.candidate_kind : [],
    nextAction: row.next_action || (row.classification && row.classification.next_action) || null,
    blocking: Array.isArray(canonical.blocking) ? canonical.blocking : (v2.gate_summary && v2.gate_summary.blocking) || [],
    promotable: !!(v2.gate_summary && v2.gate_summary.promotable),
    casesCount: Array.isArray(row.scorecard_v2_cases) ? row.scorecard_v2_cases.length : (typeof row.scorecard_v2_cases === "number" ? row.scorecard_v2_cases : null),
    gates: { g1: gate("gate1", v2.gate1), g1b: gate("gate1B", v2.gate1B), g2: gate("gate2", v2.gate2), g3: gate("gate3", v2.gate3) },
    detailStatus: detailEntry ? detailEntry.status : null,
    detailEmpty: !!(detailEntry && detailEntry.status === "empty"),
    detailCard,
  };
}
function bestCardV2(id) {
  const cs = cardsForStrategy(id);
  return cs.slice().sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0))[0] || null;
}

/* ---------------- strategy-level aggregation (deduplicated by base id) ----------------
   Strategy counts dedup by canonical base strategy id. Each metric is a per-id boolean
   over the strategy universe, so no strategy-level count can exceed Total Strategies.
   Raw scorecard/backtest row counts are computed separately and labelled "Rows". */
function isPassStatus(s) {
  const t = String(s || "").toLowerCase();
  return t.includes("pass") || t === "ok" || t === "accepted" || t === "certified" || t === "done";
}
function isFailStatus(s) { return String(s || "").toLowerCase().includes("fail"); }

/* Canonical strategy universe: pipeline rows (primary), registry candidates (fallback
   only when pipeline rows are unavailable). Scorecard-only ids are NOT added here — they
   are orphan evidence (see orphanScorecardIds). */
function canonicalStrategyIds() {
  const ids = new Set();
  pipelineRows().forEach((r) => { const b = baseId(rowId(r)); if (b) ids.add(b); });
  if (ids.size === 0) {
    registryEntries().forEach((r) => { const b = baseId(rowId(r)); if (b) ids.add(b); });
  }
  return Array.from(ids);
}
/* Backwards-compatible alias; strategy-level metrics use the canonical universe. */
function strategyUniverse() { return canonicalStrategyIds(); }
/* Unique base ids present in scorecard cards but absent from the canonical universe. */
function orphanScorecardIds() {
  const canon = new Set(canonicalStrategyIds());
  const orphans = new Set();
  scorecardCards().forEach((c) => {
    const b = baseId(c.base_strategy_id || c.strategy_id);
    if (b && !canon.has(b)) orphans.add(b);
  });
  return Array.from(orphans);
}
/* Every known status for one gate across the pipeline-row scorecard_v2 + all scorecard cards. */
function gateStatusesForStrategy(id, gateKey) {
  const out = [];
  const row = findRow(id);
  const rowSt = row && row.scorecard_v2 && row.scorecard_v2.gate_summary && row.scorecard_v2.gate_summary.statuses;
  if (rowSt && rowSt[gateKey] != null) out.push(rowSt[gateKey]);
  cardsForStrategy(id).forEach((c) => {
    const st = c.gate_summary && c.gate_summary.statuses && c.gate_summary.statuses[gateKey];
    if (st != null) out.push(st);
  });
  return out;
}
function strategyGatePass(id, gateKey) { return gateStatusesForStrategy(id, gateKey).some(isPassStatus); }
function strategyGate2Pass(id) {
  if (strategyGatePass(id, "gate2")) return true;
  return cardsForStrategy(id).some((c) => c.gate2 && Number(c.gate2.score) >= 80); // benchmark candidate
}
function strategyGate2Failed(id) {
  const sts = gateStatusesForStrategy(id, "gate2");
  if (!sts.length || strategyGate2Pass(id)) return false; // need evidence + no pass anywhere
  return sts.some(isFailStatus);
}
function strategyPromotable(id) {
  const row = findRow(id);
  if (row && row.scorecard_v2 && row.scorecard_v2.gate_summary && row.scorecard_v2.gate_summary.promotable) return true;
  return cardsForStrategy(id).some((c) => c.gate_summary && c.gate_summary.promotable);
}
function strategyNeedsAttention(id) {
  const row = findRow(id);
  if (!row) return false;
  const t = [row.next_action, row.notes, JSON.stringify(row.canonical || {})].join(" ").toLowerCase();
  return t.includes("pending") || t.includes("missing") || t.includes("fail") || t.includes("define") || t.includes("freeze");
}
function strategyMetrics() {
  const ids = strategyUniverse();
  const out = { total: ids.length, g1: 0, g1b: 0, g2: 0, g2f: 0, paper: 0, attn: 0 };
  ids.forEach((id) => {
    if (strategyGatePass(id, "gate1")) out.g1++;
    if (strategyGatePass(id, "gate1B")) out.g1b++;
    if (strategyGate2Pass(id)) out.g2++;
    if (strategyGate2Failed(id)) out.g2f++;
    if (strategyPromotable(id)) out.paper++;
    if (strategyNeedsAttention(id)) out.attn++;
  });
  return out;
}
/* Best Gate 1 passing scorecard/version row for a strategy, else null. */
function bestGate1PassingVersion(id) {
  const cs = cardsForStrategy(id).filter((c) => c.gate_summary && c.gate_summary.statuses && isPassStatus(c.gate_summary.statuses.gate1));
  if (!cs.length) return null;
  return cs.slice().sort((a, b) => {
    const ga = a.gate1 && a.gate1.score != null ? Number(a.gate1.score) : -1;
    const gb = b.gate1 && b.gate1.score != null ? Number(b.gate1.score) : -1;
    return gb - ga;
  })[0];
}

/* ============================================================
   PAGE: Command Center Home
   ============================================================ */
function renderHome(c) {
  const rows = pipelineRows();
  const cards = scorecardCards();
  const runs = backtestRuns();
  const diags = diagnosticItems();
  const reports = reportItems();
  const pipeline = snap().candidate_pipeline || {};
  const stageCounts = (pipeline.summary && pipeline.summary.stage_done_counts) || {};
  const stages = pipeline.stages || [];

  // Strategy-level metrics (deduplicated by base id).
  const sm = strategyMetrics();
  // Evidence / system row metrics (raw rows/runs/artifacts — may exceed strategy count).
  const scorecardRows = cards.length;
  const gate1PassRows = cards.filter((c) => c.gate_summary && c.gate_summary.statuses && isPassStatus(c.gate_summary.statuses.gate1)).length;
  const benchmarkRows = cards.filter((c) => c.gate2 && Number(c.gate2.score) >= 80).length;
  const gate2FailRows = cards.filter((c) => c.gate_summary && c.gate_summary.statuses && isFailStatus(c.gate_summary.statuses.gate2)).length;
  const orphanIds = orphanScorecardIds().length;
  const artifactErrs = diags.filter((d) => !d.ok).length;

  const attention = rows.filter((r) => {
    const t = [r.next_action, r.notes, JSON.stringify(r.canonical || {})].join(" ").toLowerCase();
    return t.includes("pending") || t.includes("missing") || t.includes("fail") || t.includes("define") || t.includes("freeze");
  }).slice(0, 5);

  const topCards = cards.slice().sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0)).slice(0, 5);

  const metric = (label, value, cls = "", title = "") => `<article class="metric ${cls}"${title ? ` title="${esc(title)}"` : ""}><span>${esc(label)}</span><strong>${num(value)}</strong></article>`;

  c.innerHTML = `
    <div class="metric-group">
      <div class="metric-group-head"><h3>Strategy Universe</h3><span>deduplicated by strategy_id</span></div>
      <div class="metric-grid">
        ${metric("Total Strategies", sm.total, "teal")}
        ${metric("Gate 1 Passed Strategies", sm.g1, "blue")}
        ${metric("Gate 1B Passed Strategies", sm.g1b, "blue")}
        ${metric("Gate 2 Passed Strategies", sm.g2, "emerald")}
        ${metric("Gate 2 Failed Strategies", sm.g2f, "red")}
        ${metric("Paper Ready Strategies", sm.paper, "teal")}
        ${metric("Needs Review Strategies", sm.attn, "amber", "Broad heuristic: canonical strategies whose pipeline next_action / notes / canonical block mentions pending, missing, fail, define, or freeze. Indicates review/rule-freeze needed, not necessarily broken.")}
      </div>
    </div>

    <div class="metric-group">
      <div class="metric-group-head"><h3>Evidence / System Volume</h3><span>raw rows · runs · artifacts</span></div>
      <div class="metric-grid">
        ${metric("Scorecard Rows", scorecardRows)}
        ${metric("Gate 1 Passed Rows", gate1PassRows)}
        ${metric("Benchmark Candidate Rows", benchmarkRows)}
        ${metric("Gate 2 Failed Rows", gate2FailRows)}
        ${metric("Backtest Runs", runs.length)}
        ${metric("Reports Indexed", reports.length)}
        ${metric("Scorecard-only Strategy IDs", orphanIds, orphanIds ? "amber" : "")}
        ${metric("Artifact Errors", artifactErrs, artifactErrs ? "red" : "")}
      </div>
    </div>
    <p class="metric-note">Strategy counts use the canonical pipeline/registry universe. Scorecard-only IDs are treated as orphan evidence until promoted into the strategy registry/pipeline. Row counts refer to scorecard/backtest evidence rows and may exceed strategy count. "Needs Review" is a broad heuristic (pending/missing/fail/define/freeze in pipeline metadata), not a strict blocker count.</p>

    <div class="dashboard-grid">
      <div class="stack">
        <section class="panel">
          <div class="panel-heading"><h3>Today's Action Queue</h3><span>${attention.length} items</span></div>
          ${attention.length ? attention.map((r) => actionRow(r)).join("") : emptyState("No pending action items in current snapshot.")}
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Benchmark Board</h3><span>read-only</span></div>
          <p class="same-profile-warning">Only compare results within the same profile, timeframe, market universe, and score method. Do not compare SOURCE_NAKED directly with MTC_LIGHT, or 15m results with 1D results.</p>
          <div class="info-grid">
            ${topCards.length ? topCards.map((c) => infoCard(`${esc(baseId(c.base_strategy_id || c.strategy_id))} / ${esc(c.timeframe || "tf")}`, `Gate 2: ${c.gate2 && c.gate2.score != null ? c.gate2.score : "—"}`)).join("") : infoCard("Benchmark data", null, { empty: M.artifact })}
          </div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Strategy Pipeline Overview</h3><span>${stages.length} stages</span></div>
          <div class="grid-4">
            ${stages.length ? stages.map((s) => `<div class="lc-kpi"><span class="k">${esc(s.label || s.key)}</span><span class="v">${num(stageCounts[s.key] || 0)}</span></div>`).join("") : emptyState("Pipeline stage data missing.")}
          </div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Strategy Watchlist / Needs Attention</h3><span>read-only</span></div>
          ${attention.length ? attention.slice(0, 3).map((r) => watchRow(r)).join("") : emptyState("No watchlist items.")}
        </section>
      </div>

      <div class="stack">
        <section class="panel">
          <div class="panel-heading"><h3>Official Gate System</h3><span>reference</span></div>
          <div class="def-rows">
            ${defRow("Gate 1", "Intake — deterministic, codable, testable")}
            ${defRow("Gate 1B", "MTC feasibility — signal/module convertible")}
            ${defRow("Gate 2", "Backtest evidence — performance & robustness")}
            ${defRow("Gate 3", "Production readiness — alerts, monitoring, fail-safe")}
          </div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Backtest Activity</h3><span>${runs.length} runs</span></div>
          <div class="def-rows">
            ${defRow("Total runs", (snap().backtest_status && snap().backtest_status.summary && snap().backtest_status.summary.total_runs) || runs.length)}
            ${defRow("Latest run", (snap().backtest_status && snap().backtest_status.summary && snap().backtest_status.summary.last_run_id) || null, M.artifact)}
            ${defRow("Failed runs", (snap().backtest_status && snap().backtest_status.summary && snap().backtest_status.summary.failed_runs) || 0)}
          </div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Artifact Health</h3><span>${diags.length} checks</span></div>
          <div class="def-rows">
            ${defRow("Files OK", `${diags.filter((d) => d.ok).length} / ${diags.length}`)}
            ${defRow("Read-only API", state.health && state.health.overall_ok ? "OK" : "Check")}
            ${defRow("Reports", `${reports.length} indexed`)}
          </div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Leaderboard Preview</h3><span>top ${topCards.length}</span></div>
          <div class="table-wrap"><table class="grid-table">
            <thead><tr><th>#</th><th>Strategy</th><th class="num">Score</th></tr></thead>
            <tbody>${topCards.length ? topCards.map((c, i) => `<tr><td>${i + 1}</td><td>${esc(baseId(c.base_strategy_id || c.strategy_id))}</td><td class="num">${c.gate2 && c.gate2.score != null ? c.gate2.score : "—"}</td></tr>`).join("") : `<tr><td colspan="3" class="empty-cell">No leaderboard data.</td></tr>`}</tbody>
          </table></div>
        </section>

        <section class="panel">
          <div class="panel-heading"><h3>Result Explorer</h3><span>global</span></div>
          <p class="summary">Open the global result explorer, or open a strategy dossier for strategy-scoped results.</p>
          <button class="btn purple" type="button" onclick="navigate('result-explorer')">Open Backtest Result Explorer</button>
        </section>
      </div>
    </div>
  `;
}

function actionRow(r) {
  const id = rowId(r);
  const sev = String(r.next_action || "").toLowerCase().includes("fail") ? "HIGH" : "MED";
  return `
    <div class="readiness-row">
      <div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
          ${badge(sev, sev === "HIGH" ? "bad" : "warn")}
          <span class="rk">${esc(r.strategy_display_name || (r.description && r.description.family) || titleCase(baseId(id)))}</span>
        </div>
        <span style="font-size:11.5px;color:var(--muted);">${esc(r.next_action || r.notes || "Pending review")}</span>
      </div>
      <button class="btn blue mini" type="button" onclick="openStrategy('${esc(id)}')">Open Strategy Intelligence</button>
    </div>`;
}
function watchRow(r) {
  const id = rowId(r);
  const m = strategyModel(id);
  return `
    <div class="readiness-row">
      <div>
        <div class="rk" style="margin-bottom:5px;">${esc(m.displayName)}</div>
        <div class="sc-gates">
          ${badge("G1 " + spaced(m.gates.g1.status), gateTone(m.gates.g1.status))}
          ${badge("G1B " + spaced(m.gates.g1b.status), gateTone(m.gates.g1b.status))}
          ${badge("G2 " + spaced(m.gates.g2.status), gateTone(m.gates.g2.status))}
        </div>
      </div>
      <button class="btn mini" type="button" onclick="openStrategy('${esc(id)}')">Open</button>
    </div>`;
}

/* ============================================================
   PAGE: Strategy Pipeline
   ============================================================ */
const PIPELINE_FILTERS = [
  { id: "all", label: "All" },
  { id: "g1", label: "Gate 1 Passed" },
  { id: "g1b", label: "Gate 1B Passed" },
  { id: "g2fail", label: "Gate 2 Failed" },
  { id: "freeze", label: "Rule-Freeze Needed" },
  { id: "backtested", label: "Backtested" },
  { id: "paperlock", label: "Paper Locked" },
];
let pipelineFilter = "all";
let pipelineSearch = "";

function renderPipeline(c) {
  const rows = pipelineRows();
  const models = rows.map((r) => ({ m: strategyModel(rowId(r)), r }));
  const kpi = {
    total: rows.length,
    g1: models.filter((x) => x.m.gates.g1.status === "OK").length,
    g1b: models.filter((x) => x.m.gates.g1b.status === "OK").length,
    g2fail: models.filter((x) => x.m.gates.g2.status === "FAIL").length,
    freeze: models.filter((x) => (x.m.directional && x.m.directional.status === "DIRECTION_UNKNOWN") || !x.m.rules.exit || x.m.gates.g1.status !== "OK").length,
    paperlock: models.filter((x) => !x.m.promotable).length,
  };
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>Strategy Pipeline</h3><span>${rows.length} strategies</span></div>
      <p class="summary">Workflow status from candidate_pipeline. Filter, search, then open any strategy to enter its Strategy Intelligence dossier.</p>
      <div class="grid-4" style="margin-bottom:16px;grid-template-columns:repeat(6,1fr);">
        <div class="lc-kpi"><span class="k">Total</span><span class="v">${kpi.total}</span></div>
        <div class="lc-kpi"><span class="k">Gate 1 OK</span><span class="v">${kpi.g1}</span></div>
        <div class="lc-kpi"><span class="k">Gate 1B OK</span><span class="v">${kpi.g1b}</span></div>
        <div class="lc-kpi"><span class="k">Gate 2 Failed</span><span class="v">${kpi.g2fail}</span></div>
        <div class="lc-kpi"><span class="k">Rule Freeze Needed</span><span class="v">${kpi.freeze}</span></div>
        <div class="lc-kpi"><span class="k">Paper Locked</span><span class="v">${kpi.paperlock}</span></div>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px;">
        <input id="pipeSearch" class="btn" style="flex:1;min-width:220px;cursor:text;" placeholder="Search strategy id, name, family…" value="${esc(pipelineSearch)}">
      </div>
      <div class="chip-row" id="pipeChips" style="margin-bottom:16px;">
        ${PIPELINE_FILTERS.map((f) => `<span class="chip ${pipelineFilter === f.id ? "is-active" : ""}" data-filter="${f.id}">${esc(f.label)}</span>`).join("")}
      </div>
      <div class="strategy-card-grid" id="pipeGrid"></div>
    </section>
  `;
  $("#pipeSearch").addEventListener("input", (e) => { pipelineSearch = e.target.value; paintPipeline(); });
  $("#pipeChips").addEventListener("click", (e) => {
    const chip = e.target.closest("[data-filter]");
    if (!chip) return;
    pipelineFilter = chip.dataset.filter;
    $$("#pipeChips .chip").forEach((x) => x.classList.toggle("is-active", x.dataset.filter === pipelineFilter));
    paintPipeline();
  });
  paintPipeline();
}

function pipelineMatches(m, r) {
  const q = pipelineSearch.trim().toLowerCase();
  if (q) {
    const hay = [m.id, m.displayName, m.family, m.sourceTitle].join(" ").toLowerCase();
    if (!hay.includes(q)) return false;
  }
  switch (pipelineFilter) {
    case "g1": return m.gates.g1.status === "OK";
    case "g1b": return m.gates.g1b.status === "OK";
    case "g2fail": return m.gates.g2.status === "FAIL";
    case "freeze": return (m.directional && m.directional.status === "DIRECTION_UNKNOWN") || !m.rules.exit || m.gates.g1.status !== "OK";
    case "backtested": return (r.stages && r.stages.backtested && r.stages.backtested.status === "done");
    case "paperlock": return !m.promotable;
    default: return true;
  }
}

function paintPipeline() {
  const grid = $("#pipeGrid");
  if (!grid) return;
  const rows = pipelineRows();
  const filtered = rows.filter((r) => pipelineMatches(strategyModel(rowId(r)), r));
  if (!filtered.length) { grid.innerHTML = emptyState("No strategies match this filter / search."); return; }
  grid.innerHTML = filtered.map((r) => {
    const m = strategyModel(rowId(r));
    return strategyCard(m);
  }).join("");
  grid.onclick = (e) => {
    const card = e.target.closest("[data-sid]");
    if (card) openStrategy(card.dataset.sid);
  };
}

function strategyCard(m) {
  const sc = scoreClass(m.score);
  return `
    <article class="strategy-card clickable" data-sid="${esc(m.id)}">
      <div class="sc-head">
        <div><code>${esc(m.id)}</code><h4>${esc(m.displayName)}</h4></div>
        <span class="score-chip ${sc}">${m.score != null ? esc(m.score) : "—"}</span>
      </div>
      <div class="sc-meta">
        ${infoCard("Horizon / Category", [m.definedTf, m.classification.label].filter(Boolean).join(" · ") || null, { empty: M.notextracted })}
        ${infoCard("Instrument", m.symbol, { empty: M.snapshot })}
        ${infoCard("Source", m.sourceUrl ? hostOf(m.sourceUrl) : null, { empty: M.meta })}
        ${infoCard("Family", m.family, { empty: M.notextracted })}
      </div>
      <div class="sc-gates">
        ${badge("Gate 1 " + spaced(m.gates.g1.status), gateTone(m.gates.g1.status))}
        ${badge("Gate 1B " + spaced(m.gates.g1b.status), gateTone(m.gates.g1b.status))}
        ${badge("Gate 2 " + spaced(m.gates.g2.status), gateTone(m.gates.g2.status))}
        ${badge("Gate 3 " + spaced(m.gates.g3.status), gateTone(m.gates.g3.status))}
      </div>
      <div class="sc-foot">
        <span>${esc(m.nextAction || "Pending review")}</span>
        <button class="btn mini" type="button" onclick="event.stopPropagation();openStrategy('${esc(m.id)}')">Open</button>
      </div>
    </article>`;
}

function hostOf(url) { try { return new URL(url).hostname.replace("www.", ""); } catch { return url; } }

/* ============================================================
   PAGE: Strategy Registry
   ============================================================ */
let registrySearch = "";
function renderRegistry(c) {
  const entries = registryEntries();
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>Strategy Registry</h3><span>${entries.length} entries</span></div>
      <p class="summary">Source catalog distinct from the workflow pipeline. Search the catalog, then open a strategy for its generic Strategy Intelligence dossier.</p>
      <input id="regSearch" class="btn" style="width:100%;cursor:text;margin-bottom:16px;" placeholder="Search by id, title, source type…" value="${esc(registrySearch)}">
      <div class="stack" id="regList"></div>
    </section>
  `;
  $("#regSearch").addEventListener("input", (e) => { registrySearch = e.target.value; paintRegistry(); });
  paintRegistry();
}
function paintRegistry() {
  const list = $("#regList");
  if (!list) return;
  const q = registrySearch.trim().toLowerCase();
  const entries = registryEntries().filter((r) => {
    if (!q) return true;
    return [rowId(r), r.title, r.name, r.market_type, r.source_url].join(" ").toLowerCase().includes(q);
  });
  if (!entries.length) { list.innerHTML = emptyState("No registry entries match."); return; }
  list.innerHTML = entries.map((r) => {
    const id = rowId(r);
    const m = strategyModel(id);
    return `
      <details class="acc">
        <summary>
          <span style="display:flex;flex-direction:column;gap:2px;">
            <code style="color:var(--teal);font-size:11px;">${esc(id)}</code>
            <strong style="font-size:13.5px;color:var(--text-strong);">${esc(r.title || r.name || m.displayName)}</strong>
          </span>
          <span style="display:flex;gap:6px;align-items:center;">
            ${badge(r.status || "—", gateTone(r.status))}
            <button class="btn mini" type="button" onclick="event.preventDefault();openStrategy('${esc(id)}')">Open Strategy</button>
          </span>
        </summary>
        <div class="acc-body">
          <div class="info-grid">
            ${infoCard("Source Title", r.title || r.name, { empty: M.meta })}
            ${infoCard("Source Type", r.market_type, { empty: M.meta })}
            ${infoCard("Source URL", m.sourceUrl ? hostOf(m.sourceUrl) : null, { empty: M.meta })}
            ${infoCard("Horizon / TF", r.timeframe, { empty: M.notextracted })}
            ${infoCard("Method", null, { empty: "Method extraction reader not implemented" })}
            ${infoCard("Market Condition", m.marketCondition, { empty: M.notextracted })}
            ${infoCard("Defined Frame", m.definedTf, { empty: M.notextracted })}
            ${infoCard("Tested Frame", m.testedTf, { empty: M.artifact })}
            ${infoCard("Gate Status", `${spaced(m.gates.g1.status)} / ${spaced(m.gates.g2.status)}`)}
            ${infoCard("Evidence Level", r.evidence_level, { empty: M.snapshot })}
            ${infoCard("Reusable Components", m.candidateKind.length ? m.candidateKind.join(", ") : null, { empty: M.snapshot, span2: true })}
            ${infoCard("Transcript", m.transcript ? "Linked" : null, { empty: "Transcript not linked" })}
          </div>
          ${m.sourceUrl ? `<div class="chip-row" style="margin-top:12px;"><a class="chip" href="${esc(m.sourceUrl)}" target="_blank" rel="noopener">View Source ↗</a></div>` : ""}
        </div>
      </details>`;
  }).join("");
}

/* ============================================================
   PAGE: Strategy Intelligence (detail dossier)
   ============================================================ */
function renderIntelligence(c) {
  const id = state.selectedStrategyId || defaultStrategyId();
  state.selectedStrategyId = id;
  if (!id) { c.innerHTML = emptyState("No strategy selected and no pipeline rows in snapshot."); return; }
  loadStrategyDetail(id);
  const m = strategyModel(id);

  c.innerHTML = `
    ${heroBlock(m)}
    ${constraintNotice(m)}
    <div class="si-layout">
      <div class="si-main">
        ${gateSummaryBlock(m)}
        ${overviewSection(m)}
        ${gate1Section(m)}
        ${verdictSection(m)}
        ${evidenceSection(m)}
        ${explorerPreviewSection(m)}
        ${paperReadinessSection(m)}
        ${advancedSection(m)}
      </div>
      <aside class="si-rail">
        ${railBlock(m)}
      </aside>
    </div>
  `;
}

function constraintNotice(m) {
  const blockers = [];
  if (!m.rules.entry) blockers.push("entry rule not extracted");
  if (!m.rules.exit) blockers.push("exit logic not extracted");
  if (!m.sourceUrl) blockers.push("source metadata missing");
  if (m.gates.g2.status !== "OK") blockers.push("Gate 2 evidence not validated");
  if (m.directional && m.directional.status === "DIRECTION_UNKNOWN") blockers.push("trade direction undefined");
  if (Array.isArray(m.blocking) && m.blocking.length) blockers.push("blocking: " + m.blocking.map(spaced).join(", "));
  if (!blockers.length) return "";
  return `
    <section class="constraint-notice">
      <div class="banner-icon">${icon("shield")}</div>
      <div>
        <h4>Research Constraint Notice</h4>
        <p>Undefined or missing rule, risk, source, or artifact fields remain blockers. This strategy stays read-only until source rules, risk model, and Gate 2 evidence are validated.</p>
        <p class="cn-list">Detected blockers: ${esc(blockers.join(" · "))}.</p>
      </div>
    </section>`;
}

function heroVal(g, opts = {}) {
  const tone = gateTone(g.status);
  if (opts.score && g.score != null) return `<span class="val ${tone === "bad" ? "bad" : tone === "ok" ? "ok" : ""}">${g.score}<span style="font-size:10px;color:var(--faint);"> / ${g.max}</span></span>`;
  if (tone === "ok") return `<span class="val ok">Certified</span>`;
  if (tone === "bad") return `<span class="val bad">Failed</span>`;
  return `<span class="val locked">${spaced(g.status) || "Pending"}</span>`;
}

function heroBlock(m) {
  const paper = m.promotable ? "Ready (review)" : "Locked";
  return `
    <section class="si-hero" id="top">
      <div class="si-hero-top">
        <div>
          <span class="eyebrow">Active Evaluation Candidate</span>
          <h2 class="si-hero-id">${esc(m.displayName)}</h2>
          <p class="si-hero-thesis">${esc(m.thesis)}</p>
          <p class="si-hero-meta">${esc(m.id)}</p>
        </div>
        <div class="si-gate-panel">
          <div class="si-gate-cell"><span class="lbl">Gate 1 / Intake</span>${heroVal(m.gates.g1)}</div>
          <div class="si-gate-cell"><span class="lbl">Gate 1B / MTC</span>${heroVal(m.gates.g1b)}</div>
          <div class="si-gate-cell"><span class="lbl">Gate 2 Evidence</span>${heroVal(m.gates.g2, { score: true })}</div>
          <div class="si-gate-cell"><span class="lbl">Paper Trading</span><span class="val locked">${esc(paper)}</span></div>
        </div>
      </div>
      <div class="workflow-bar">
        ${workflowCard("Stage 1", "Strategy Overview", "Done", "overview", false)}
        ${workflowCard("Stage 2", "Gate 1 / Gate 1B", m.gates.g1b.status === "OK" ? "Done" : "Review", "gate1", m.gates.g1b.status !== "OK")}
        ${workflowCard("Stage 3", "Backtest Plan & Evidence", m.gates.g2.status === "FAIL" ? "Needs Review" : (m.gates.g2.status === "OK" ? "Done" : "Pending"), "evidence", m.gates.g2.status !== "OK")}
        ${workflowCard("Stage 4", "Paper Trading", m.promotable ? "Pending approval" : "Locked", "paper", !m.promotable)}
      </div>
    </section>`;
}
function workflowCard(stage, label, status, section, dim) {
  return `<div class="workflow-card ${dim ? "dim" : ""}" onclick="scrollToSection('${section}')">
    <span class="stg">${esc(stage)}</span><span class="ttl">${esc(label)}</span><span class="st">${esc(status)}</span>
  </div>`;
}

function sectionHead(n, title, subtitle, iconName) {
  return `<div class="si-section-head"><div class="si-section-icon">${icon(iconName)}</div><div><span class="eyebrow">Section ${n}</span><h3>${esc(title)}</h3><p>${esc(subtitle)}</p></div></div>`;
}

function gateCard(title, desc, g, opts = {}) {
  const tone = gateTone(g.status);
  const cls = opts.locked ? "locked" : tone === "ok" ? "ok accent" : tone === "bad" ? "bad accent" : "";
  const badgeCls = opts.locked ? "neutral" : tone;
  const label = g.score != null ? `${g.score}/${g.max} — ${spaced(g.status)}` : spaced(g.status);
  return `
    <div class="gate-card ${cls}">
      ${(tone === "ok" || tone === "bad") && !opts.locked ? '<span class="bar"></span>' : ""}
      <div class="gate-card-head">
        <div><h4>${esc(title)}</h4><p>${esc(desc)}</p></div>
        ${badge(label, badgeCls)}
      </div>
    </div>`;
}

function gateSummaryBlock(m) {
  return `
    <section class="si-section">
      <h3 class="section-title">Gate Status Summary</h3>
      <div class="gate-summary-grid">
        ${gateCard("Gate 1 Intake", "Checks whether source rules are deterministic, codable, and testable.", m.gates.g1)}
        ${gateCard("Gate 1B MTC Feasibility", "Checks whether the strategy can be converted into an MTC-compatible signal or module.", m.gates.g1b)}
        ${gateCard("Gate 2 Backtest Evidence", "Checks historical performance, robustness, trade sample quality, and benchmark comparison.", m.gates.g2)}
        ${gateCard("Gate 3 Production Readiness", "Checks paper-trading readiness, alert contracts, fail-safe behavior, and controls.", m.gates.g3, { locked: m.gates.g3.status !== "OK" })}
      </div>
    </section>`;
}

function ruleBlock(label, value, warn) {
  const v = value || null;
  return `<div class="rule-block ${warn && !v ? "warn" : ""}"><div class="rb-label">${esc(label)}</div><div class="rb-val">${v ? esc(v) : missing(warn || M.notextracted)}</div></div>`;
}

function overviewSection(m) {
  return `
    <section class="si-section" id="sec-overview">
      ${sectionHead(1, "Strategy Overview", "Plain-English thesis, mechanism, core rules, taxonomy, and source.", "file")}
      <div class="panel">
        <div class="rule-grid">
          ${ruleBlock("Plain-English Thesis", m.thesis)}
          ${ruleBlock("Best Market Condition", m.marketCondition, M.notextracted)}
        </div>
        <div class="rule-grid" style="margin-top:12px;">
          ${ruleBlock("Visual Mechanism", null, "Not present in read model")}
          ${ruleBlock("Family", m.family, M.notextracted)}
        </div>

        <h4 class="section-title" style="margin-top:18px;">Core Rules Breakdown</h4>
        <div class="rule-grid">
          ${ruleBlock("Entry Trigger", m.rules.entry, M.notextracted)}
          ${ruleBlock("Exit Logic", m.rules.exit, M.notextracted)}
          ${ruleBlock("Avoid Trading When", m.rules.avoid, "Not specified in source")}
          ${ruleBlock("Assumptions to Freeze", m.directional && m.directional.next_action, M.rulefreeze)}
        </div>

        <h4 class="section-title" style="margin-top:18px;">Strategy Taxonomy</h4>
        <div class="info-grid">
          ${infoCard("Category / Horizon", [m.classification.label, m.definedTf].filter(Boolean).join(" · ") || null, { empty: M.notextracted })}
          ${infoCard("Methodology", null, { empty: "Method extraction reader not implemented" })}
          ${infoCard("Condition Fit", m.marketCondition, { empty: M.notextracted })}
          ${infoCard("Defined Frame", m.definedTf, { empty: M.notextracted })}
          ${infoCard("Tested Frame", m.testedTf ? (m.tfMismatch ? `${m.testedTf} (timeframe mismatch)` : m.testedTf) : null, { empty: M.artifact })}
          ${infoCard("Instrument Fit", m.symbol || m.sourceType, { empty: M.notextracted })}
          ${infoCard("Automation Suitability", m.gates.g1b.status === "OK" ? "Convertible to MTC signal" : null, { empty: M.rulefreeze })}
          ${infoCard("Complexity", (m.expert && m.expert.complexity) || (m.reg && m.reg.complexity_score != null ? `score ${m.reg.complexity_score}` : null), { empty: M.notextracted })}
        </div>

        <h4 class="section-title" style="margin-top:18px;">Source Material</h4>
        <div class="info-grid">
          ${infoCard("Source Title", m.sourceTitle, { empty: M.meta })}
          ${infoCard("Source Type", m.sourceType, { empty: M.meta })}
          ${infoCard("Channel / Author", null, { empty: M.meta })}
          ${infoCard("URL", m.sourceUrl ? hostOf(m.sourceUrl) : null, { empty: M.meta })}
          ${infoCard("Transcript Status", m.transcript ? "Linked" : null, { empty: "Transcript not linked" })}
        </div>
        ${m.sourceUrl ? `<div class="chip-row" style="margin-top:12px;"><a class="chip" href="${esc(m.sourceUrl)}" target="_blank" rel="noopener">View Source ↗</a></div>` : ""}
      </div>
    </section>`;
}

function subscoreList(g, m) {
  if (!g.sub || !g.sub.length) {
    const status = m && m.detailStatus;
    if (status === "loading") return emptyState("Loading full scorecard detail...");
    if (status === "error") return emptyState("Full gate detail unavailable; showing summary only.");
    if (m && m.detailEmpty) return emptyState("No full scorecard detail found for this strategy.");
    return emptyState("Subscore breakdown not present in current snapshot.");
  }
  return `<div class="subscore-list">${g.sub.map((s) => {
    const mx = s.max_points != null ? s.max_points : s.points_max;
    const aw = s.points_awarded;
    let cls = "absent", pts = `— / ${mx}`;
    if (s.metric_status === "ABSENT") { cls = "absent"; pts = `n/a / ${mx}`; }
    else if (aw != null) { const r = mx ? aw / mx : 0; cls = r >= 1 ? "full" : r > 0 ? "partial" : "none"; pts = `${aw} / ${mx}`; }
    return `<div class="subscore"><div><div class="crit">${esc(titleCase(s.criterion))}</div><div class="note">${esc(s.deduction_reason || s.note || "")}</div></div><div class="pts ${cls}">${esc(pts)}</div></div>`;
  }).join("")}</div>`;
}

function gate1Section(m) {
  const best = bestGate1PassingVersion(m.id);
  const all = cardsForStrategy(m.id);
  const g1State = (c) => {
    const st = c.gate_summary && c.gate_summary.statuses && c.gate_summary.statuses.gate1;
    return isPassStatus(st) ? badge("PASS", "ok") : isFailStatus(st) ? badge("FAIL", "bad") : badge(st ? spaced(st) : "PENDING", "neutral");
  };
  const gx = (c, k) => {
    const st = c.gate_summary && c.gate_summary.statuses && c.gate_summary.statuses[k];
    return isPassStatus(st) ? badge("PASS", "ok") : isFailStatus(st) ? badge("FAIL", "bad") : badge(st ? spaced(st) : "—", "neutral");
  };
  return `
    <section class="si-section" id="sec-gate1">
      ${sectionHead(2, "Gate 1 / Gate 1B Pre-Backtest Assessment", "The official pre-backtest assessment. No separate pre-backtest index.", "shield")}
      <div class="panel">
        <div class="grid-2">
          <div>
            <div class="section-title" style="justify-content:space-between;display:flex;">Gate 1 Intake ${badge(m.gates.g1.score != null ? `${m.gates.g1.score}/${m.gates.g1.max}` : spaced(m.gates.g1.status), gateTone(m.gates.g1.status))}</div>
            <p class="summary">Deterministic, codable, and testable source rules.</p>
            ${subscoreList(m.gates.g1, m)}
          </div>
          <div>
            <div class="section-title" style="justify-content:space-between;display:flex;">Gate 1B MTC Feasibility ${badge(m.gates.g1b.score != null ? `${m.gates.g1b.score}/${m.gates.g1b.max}` : spaced(m.gates.g1b.status), gateTone(m.gates.g1b.status))}</div>
            <p class="summary">Convertible into an MTC-compatible signal or module.</p>
            ${subscoreList(m.gates.g1b, m)}
          </div>
        </div>

        <h4 class="section-title" style="margin-top:18px;display:flex;justify-content:space-between;align-items:center;">Primary Gate 1 Version ${best ? badge("Showing best Gate 1 passing version", "ok") : badge("No Gate 1 passing version found", "neutral")}</h4>
        ${best ? `<div class="info-grid">
          ${infoCard("Strategy ID", baseId(best.base_strategy_id || best.strategy_id || m.id), { empty: M.artifact })}
          ${infoCard("Row / Run / Result ID", best.run_id || best.run_name || best.result_id || best.row_id, { empty: M.artifact })}
          ${infoCard("Symbol / Universe", best.symbol, { empty: M.artifact })}
          ${infoCard("Timeframe", best.timeframe, { empty: M.artifact })}
          ${infoCard("Profile", best.profile, { empty: "Profile-separated artifact missing" })}
          ${infoCard("Gate 1 Score / Status", best.gate1 && best.gate1.score != null ? `${best.gate1.score} — ${spaced((best.gate_summary && best.gate_summary.statuses && best.gate_summary.statuses.gate1) || "PASS")}` : spaced((best.gate_summary && best.gate_summary.statuses && best.gate_summary.statuses.gate1) || "PASS"))}
          ${infoCard("Source Artifact Path", best.source_path, { empty: M.artifact, span2: true })}
        </div>` : emptyState("No scorecard/version row with a passing Gate 1 status for this strategy in the current snapshot. Other versions (if any) are listed below.")}

        <h4 class="section-title" style="margin-top:18px;">Advanced / All Versions <span style="color:var(--faint);font-weight:600;">${all.length} scorecard row${all.length === 1 ? "" : "s"}</span></h4>
        ${all.length ? `<div class="table-wrap"><table class="grid-table">
          <thead><tr><th>Asset / TF</th><th>Profile</th><th class="num">G1 Score</th><th>Gate 1</th><th>Gate 1B</th><th>Gate 2</th><th>Run</th></tr></thead>
          <tbody>${all.slice().sort((a, b) => Number((b.gate1 && b.gate1.score) || 0) - Number((a.gate1 && a.gate1.score) || 0)).map((c) => `<tr>
            <td>${esc(c.symbol || "—")} / ${esc(c.timeframe || "—")}</td>
            <td>${c.profile ? esc(c.profile) : `<span class="value-muted">—</span>`}</td>
            <td class="num">${c.gate1 && c.gate1.score != null ? c.gate1.score : "—"}</td>
            <td>${g1State(c)}</td>
            <td>${gx(c, "gate1B")}</td>
            <td>${gx(c, "gate2")}</td>
            <td><span class="cell-trunc">${esc(c.run_name || c.run_id || "—")}</span></td>
          </tr>`).join("")}</tbody>
        </table></div>` : emptyState("No scorecard/version rows for this strategy in the current snapshot.")}

        <div class="banner info" style="margin-top:16px;margin-bottom:0;"><div class="banner-icon">${icon("info")}</div><div><h4>Official Note</h4><p>Gate 1 + Gate 1B together form the official pre-backtest assessment. Missing fields above reflect ABSENT source metrics in scorecard_v2, not a UI gap.</p></div></div>
      </div>
    </section>`;
}

function verdictSection(m) {
  const e = m.expert;
  return `
    <section class="si-section" id="sec-verdict">
      ${sectionHead(3, "AI Verdict & Reuse Notes", "Expert QuantLens narrative verdict, feasibility, and reuse value.", "cpu")}
      <div class="panel">
        ${e ? `
        <div class="banner ${e.decision === "RESEARCH_ONLY" ? "warn" : "info"}" style="margin-bottom:16px;">
          <div class="banner-icon">${icon("cpu")}</div>
          <div><h4>${esc(e.decision_label || e.decision)}</h4><p>${esc(e.reason || "")}</p></div>
        </div>
        <div class="info-grid">
          ${infoCard("Programmatic Feasibility", e.can_test ? `Testable: ${e.can_test}` : null, { empty: M.snapshot })}
          ${infoCard("Backtest Feasibility", e.testability, { empty: M.snapshot })}
          ${infoCard("Production Readiness", spaced(m.gates.g3.status))}
          ${infoCard("AI Reuse Factor", m.candidateKind.length ? `${m.candidateKind.length} reusable components` : null, { empty: M.snapshot })}
          ${infoCard("Commercial Value", e.commercial_value, { empty: M.snapshot })}
          ${infoCard("Literature Relevance", e.literature_relevance, { empty: M.snapshot })}
          ${infoCard("Complexity", e.complexity, { empty: M.snapshot })}
          ${infoCard("Score Reference", e.score_reference, { empty: M.snapshot })}
        </div>
        <h4 class="section-title" style="margin-top:18px;">Strategic Weaknesses / Risk Flags</h4>
        <div class="chip-row">${(e.risk_flags || []).length ? e.risk_flags.map((f) => badge(spaced(f), "warn")).join("") : missing(M.snapshot)}</div>
        <h4 class="section-title" style="margin-top:18px;">AI-Reusable Components</h4>
        <div class="chip-row">${m.candidateKind.length ? m.candidateKind.map((k) => `<span class="chip static">${esc(spaced(k))}</span>`).join("") : missing("Not catalogued in registry")}</div>
        <h4 class="section-title" style="margin-top:18px;">Blocking / Missing Assumptions</h4>
        <p class="summary" style="margin-bottom:0;">${esc(e.blocking || "No explicit blocking notes.")}${m.directional && m.directional.warning ? " · " + esc(m.directional.warning) : ""}</p>
        ` : emptyState("Expert QuantLens verdict not present for this strategy in the current snapshot.")}
      </div>
    </section>`;
}

function evidenceSection(m) {
  const g2 = m.gates.g2;
  const tfs = explorerTimeframes();
  const rp = runPlanForStrategy(m.id);
  const pd = (rp && rp.data) || null;
  const planProfiles = pd && Array.isArray(pd.profiles) ? pd.profiles : null;
  const universe = pd && pd.universe ? pd.universe : null;
  const symbolsTxt = pd && Array.isArray(pd.symbols) && pd.symbols.length
    ? pd.symbols.join(", ")
    : (universe ? `${spaced(universe.status)} — ${universe.reason || ""}` : null);
  const paramState = pd && pd.parameter_space && pd.parameter_space.state ? pd.parameter_space.state : null;
  const ap = pd && pd.approval ? pd.approval : null;
  const missing = pd && Array.isArray(pd.missing_assumptions) ? pd.missing_assumptions : [];
  const freeze = pd && Array.isArray(pd.rule_freeze_requirements) ? pd.rule_freeze_requirements : [];
  return `
    <section class="si-section" id="sec-evidence">
      ${sectionHead(4, "Backtest Plan & Evidence", "Gate 2 evidence, profiles, parameter space, and target artifacts.", "beaker")}
      <div class="panel">
        ${pd ? `<div class="banner info"><div class="banner-icon">${icon("info")}</div><div><h4>run_plan.json present (draft / review-only)</h4><p>Loaded read-only from <code>${esc(rp.rel_path)}</code> (state: ${esc(rp.state)}). This is a draft plan — no execution is triggered.</p></div></div>` : ""}
        <div class="info-grid">
          ${infoCard("Gate 2 Status", g2.score != null ? `${g2.score}/${g2.max} — ${spaced(g2.status)}` : spaced(g2.status))}
          ${infoCard("Run ID", pd ? pd.run_id : null, { empty: M.runplan })}
          ${infoCard("Plan Status", pd ? spaced(pd.status) : null, { empty: M.runplan })}
          ${infoCard("Approval State", pd ? (pd.approval_state || (ap ? "PENDING" : null)) : null, { empty: M.runplan })}
          ${infoCard("Human Review Required", ap ? String(ap.human_review_required) : null, { empty: M.runplan })}
          ${infoCard("Approved", ap ? String(ap.approved) : null, { empty: M.runplan })}
          ${infoCard("Execution Allowed", ap ? String(ap.execution_allowed) : null, { empty: M.runplan })}
          ${infoCard("Estimated Cells / Cases", pd && pd.case_count != null ? pd.case_count : (m.casesCount != null ? m.casesCount : null), { empty: M.runplan })}
          ${infoCard("Universe / Symbols", symbolsTxt, { empty: M.runplan, span2: true })}
          ${infoCard("Timeframes", pd && Array.isArray(pd.timeframes) && pd.timeframes.length ? pd.timeframes.join(", ") : null, { empty: M.runplan })}
          ${infoCard("Parameter Space State", paramState ? spaced(paramState) : null, { empty: M.runplan })}
          ${infoCard("Output Dir", pd ? pd.output_dir : null, { empty: M.runplan, span2: true })}
          ${infoCard("Verification Method", "scorecard_v2 (heuristic gate scoring)")}
        </div>

        <h4 class="section-title" style="margin-top:18px;">Backtest Profiles</h4>
        <div class="table-wrap"><table class="grid-table">
          <thead><tr><th>Profile</th><th>Purpose</th><th>Status</th></tr></thead>
          <tbody>
            ${PROFILES.map((p) => `<tr><td class="mono">${esc(p)}</td><td>${esc(profilePurpose(p))}</td><td>${planProfiles ? (planProfiles.includes(p) ? badge("Selected in run_plan", "ok") : badge("Not selected", "neutral")) : badge("Not profile-separated", "neutral")}</td></tr>`).join("")}
          </tbody>
        </table></div>

        ${pd ? `
        <h4 class="section-title" style="margin-top:18px;">Expected Artifacts (per run_plan)</h4>
        <div class="artifact-list">
          ${(Array.isArray(pd.expected_artifacts) ? pd.expected_artifacts : []).map((a) => `<div class="artifact-item"><code>${esc(a)}</code><span class="a-state plan">Expected / not present</span></div>`).join("") || emptyState("No expected_artifacts listed in run_plan.")}
        </div>

        <h4 class="section-title" style="margin-top:18px;">Rule-Freeze / Missing Assumptions</h4>
        ${(missing.length || freeze.length) ? `<ul class="plain-list">
          ${missing.map((x) => `<li>${badge("missing", "warn")} ${esc(x)}</li>`).join("")}
          ${freeze.map((x) => `<li>${badge("freeze", "neutral")} ${esc(x)}</li>`).join("")}
        </ul>` : emptyState("No missing assumptions recorded in run_plan.")}
        ` : `
        <h4 class="section-title" style="margin-top:18px;">Case Count Calculator</h4>
        ${emptyState("Parameter space and case-count calculation require run_plan.json — pending / artifact missing.")}

        <h4 class="section-title" style="margin-top:18px;">Parameter Space Preview</h4>
        ${emptyState("Parameter space not present in read model. " + M.runplan + ".")}`}

        <h4 class="section-title" style="margin-top:18px;">Top Results Preview</h4>
        ${profileMatrix(m, tfs)}
        <p class="summary" style="margin-top:10px;margin-bottom:0;">The full Top 5 list lives in <a style="color:var(--teal);cursor:pointer;" onclick="openExplorerForStrategy('${esc(m.id)}')">Backtest Result Explorer</a>. This is a compact preview.</p>
      </div>
    </section>`;
}
function profilePurpose(p) {
  return ({
    SOURCE_NAKED: "Raw source rules, no risk normalization.",
    RISK_NORMALIZED: "Risk-normalized position sizing applied.",
    MTC_LIGHT: "Lightweight MTC signal conversion.",
    FULL_MTC_CANDIDATE: "Full MTC candidate integration.",
  })[p] || "—";
}
function explorerTimeframes() {
  const tfs = new Set();
  scorecardCards().forEach((c) => { if (c.timeframe) tfs.add(c.timeframe); });
  const arr = Array.from(tfs);
  return arr.length ? arr.slice(0, 6) : ["15m", "1h", "4h", "1D"];
}
function profileMatrix(m, tfs) {
  const bestTf = m.testedTf;
  const bestScore = m.canonical && m.canonical.gate2_score;
  return `<div class="matrix-wrap"><table class="matrix">
    <thead><tr><th>Profile</th>${tfs.map((t) => `<th class="num">${esc(t)}</th>`).join("")}</tr></thead>
    <tbody>${PROFILES.map((p) => `<tr><td class="profile">${esc(p)}</td>${tfs.map((t) => {
      const isBest = p === "SOURCE_NAKED" && t === bestTf && bestScore != null;
      if (isBest) return `<td class="num best"><div class="matrix-best">Best: ${esc(bestScore)} / 100<span class="sub">Status: ${spaced(m.gates.g2.status)}</span><a onclick="openExplorerForStrategy('${esc(m.id)}')">Open Top 5</a></div></td>`;
      return `<td class="num"><span class="cell-empty">No profile-separated result yet</span></td>`;
    }).join("")}</tr>`).join("")}</tbody>
  </table></div>`;
}

function explorerPreviewSection(m) {
  const cards = cardsForStrategy(m.id).slice().sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0));
  const best = cards[0];
  const prows = profileRowsForStrategy(m.id).slice().sort((a, b) => Number(b.score || 0) - Number(a.score || 0));
  const pr = prows[0];
  return `
    <section class="si-section" id="sec-explorer">
      ${sectionHead(5, "Backtest Result Explorer", "Strategy-scoped result preview. Compare only within the same bucket.", "bar")}
      <div class="panel">
        <p class="same-profile-warning">Same-bucket rule: compare only within identical profile, timeframe, market universe, and score method.</p>
        ${pr ? researchOnlyBanner(pr) : ""}
        ${pr ? `
        <div class="bucket" style="margin-bottom:12px;">
          <div class="bucket-head"><div class="title"><span class="name">Best profile-separated result</span>${badge(pr.profile, "ok")} ${profileRowBadges(pr)}</div>${pr.promotion_status ? badge(spaced(pr.promotion_status), gateTone(pr.promotion_status)) : ""}</div>
          <div class="info-grid">
            ${infoCard("Profile", pr.profile)}
            ${infoCard("Asset / Timeframe", `${pr.symbol || "—"} / ${pr.timeframe || "—"}`)}
            ${infoCard("Score", pr.score != null ? pr.score : null, { empty: M.artifact })}
            ${infoCard("Net Profit", pr.metrics && pr.metrics.net_profit != null ? pr.metrics.net_profit + "%" : null, { empty: M.artifact })}
            ${infoCard("Max Drawdown", pr.metrics && pr.metrics.max_drawdown != null ? pr.metrics.max_drawdown + "%" : null, { empty: M.artifact })}
            ${infoCard("Run", pr.run_id, { empty: M.artifact })}
          </div>
        </div>` : best ? `
        <div class="bucket" style="margin-bottom:12px;">
          <div class="bucket-head"><div class="title"><span class="name">Best available result</span>${badge("legacy row", "neutral")}</div>${badge(spaced(best.gate_summary && best.gate_summary.statuses && best.gate_summary.statuses.gate2), gateTone(best.gate_summary && best.gate_summary.statuses && best.gate_summary.statuses.gate2))}</div>
          <div class="info-grid">
            ${infoCard("Asset / Timeframe", `${best.symbol || "—"} / ${best.timeframe || "—"}`)}
            ${infoCard("Gate 2 Score", best.gate2 && best.gate2.score != null ? best.gate2.score : null, { empty: M.artifact })}
            ${infoCard("Run", best.run_name || best.run_id, { empty: M.artifact })}
            ${infoCard("Profile", null, { empty: "Profile-separated artifact missing" })}
          </div>
        </div>` : emptyState("No scorecard result rows for this strategy in the current snapshot.")}
        <button class="btn purple" type="button" onclick="openExplorerForStrategy('${esc(m.id)}')">Open Backtest Result Explorer (strategy scope)</button>
      </div>
    </section>`;
}

function paperReadinessSection(m) {
  const ready = m.promotable;
  const rows = [
    ["Paper Trade Eligibility", ready ? "Eligible (pending approval)" : "Not eligible yet"],
    ["Gate 3 Readiness", spaced(m.gates.g3.status)],
    ["Alert Contract Readiness", "Not generated"],
    ["Monitoring Readiness", "Not generated"],
    ["Fail-Safe Readiness", "Not evaluated"],
  ];
  return `
    <section class="si-section" id="sec-paper">
      ${sectionHead(6, "Paper Trading Readiness", "Read-only readiness review. Locked until evidence exists.", "activity")}
      <div class="panel">
        ${ready ? "" : `<div class="banner warn" style="margin-bottom:14px;"><div class="banner-icon">${icon("lock")}</div><div><h4>Paper Trading Locked</h4><p>Locked until Gate 2 evidence passes and Gate 3 readiness artifacts exist. Reason: ${esc(m.blocking.join(", ") || "Gate 2 evidence not demonstrated")}.</p></div></div>`}
        <div class="def-rows">
          ${rows.map(([k, v]) => `<div class="readiness-row"><span class="rk">${esc(k)}</span>${badge(v, gateTone(v))}</div>`).join("")}
        </div>
        <div class="chip-row" style="margin-top:14px;">
          <span class="chip static">View Gate 3 Readiness Checklist (pending)</span>
          <span class="chip static">View Paper Trading Approval Package (pending)</span>
        </div>
      </div>
    </section>`;
}

function advancedSection(m) {
  const j = (label, obj) => `<details class="acc"><summary>${esc(label)}</summary><div class="acc-body"><pre class="json">${esc(JSON.stringify(obj || {}, null, 2))}</pre></div></details>`;
  // Prefer lazy-loaded full detail (with sub_scores) when available; else summary-only.
  const dc = m.detailCard;
  const detailEntry = state.detailCards[m.id];
  const fullCards = detailEntry && detailEntry.status === "ok" ? detailEntry.cards : null;
  const cards = fullCards || cardsForStrategy(m.id);
  const gateObj = dc
    ? { gate1: dc.gate1, gate1B: dc.gate1B, gate2: dc.gate2, gate3: dc.gate3 }
    : { gate1: m.v2.gate1, gate1B: m.v2.gate1B, gate2: m.v2.gate2, gate3: m.v2.gate3 };
  const gateLabel = dc
    ? "Raw scorecard gates (gate1 / gate1B / gate2 / gate3 — full detail)"
    : (m.detailStatus === "loading"
        ? "Raw scorecard gates (loading full detail...)"
        : "Raw scorecard gates (summary only — full sub_scores via scorecard-detail)");
  const cardsLabel = fullCards
    ? `Scorecard rows (${cards.length} — full detail)`
    : `Scorecard rows (${cards.length} — summary)`;
  return `
    <section class="si-section" id="sec-advanced">
      ${sectionHead(7, "Advanced Technical Details", "Raw read-model rows and identifiers. Collapsed by default.", "settings")}
      <div class="panel">
        ${j("Raw gate summary (scorecard_v2.gate_summary)", m.v2.gate_summary)}
        ${j(gateLabel, gateObj)}
        ${j("Heuristic triage scorecard", m.scorecard)}
        ${j(cardsLabel, cards)}
        ${j("Canonical / classification", { canonical: m.canonical, classification: m.classification, directional_research: m.directional })}
        ${j("Technical IDs & artifact paths", { id: m.id, base_strategy_id: m.baseId, run_id: m.v2.run_id, source_path: m.v2.source_path })}
      </div>
    </section>`;
}

function railRow(k, v, cls) {
  const val = (v === null || v === undefined || v === "") ? `<span class="v locked">N/A</span>` : `<span class="v ${cls || ""}">${esc(v)}</span>`;
  return `<div class="rail-row"><span class="k">${esc(k)}</span>${val}</div>`;
}
function railBlock(m) {
  const e = m.expert;
  const g = m.gates;
  return `
    <div class="rail-card next">
      <div class="rail-next-head">
        <div class="rail-next-icon">${icon("target")}</div>
        <div><h4>Next Action</h4><p>${esc(m.nextAction || "Review evidence and freeze rules.")}</p></div>
      </div>
    </div>

    <div class="rail-card">
      <h4>Decision Summary</h4>
      ${railRow("LLM / AI Verdict", e ? (e.decision_label || e.decision) : null, e && e.decision === "RESEARCH_ONLY" ? "warn" : "ok")}
      ${railRow("Gate 1 Intake", spaced(g.g1.status), gateTone(g.g1.status))}
      ${railRow("Gate 1B MTC", spaced(g.g1b.status), gateTone(g.g1b.status))}
      ${railRow("Gate 2 Evidence", spaced(g.g2.status), gateTone(g.g2.status))}
      ${railRow("Gate 3 Production", spaced(g.g3.status), "locked")}
      ${railRow("Promotion", m.promotable ? "Eligible" : "Blocked", m.promotable ? "ok" : "warn")}
      ${railRow("Paper Trading", m.promotable ? "Pending approval" : "Locked", "locked")}
      ${railRow("AI Reuse Factor", m.candidateKind.length ? `${m.candidateKind.length} components` : null, "teal")}
    </div>

    <div class="rail-card">
      <h4>Missing Fields / Risk</h4>
      ${missingFieldsList(m)}
    </div>

    <div class="rail-card">
      <h4>AI Knowledge Value</h4>
      ${m.candidateKind.length ? m.candidateKind.map((k) => railRow(spaced(k), "Review needed", "warn")).join("") : `<div class="rail-miss">${missing("No reusable components catalogued")}</div>`}
    </div>

    <div class="rail-card">
      <h4>Review State / Read-only</h4>
      ${railRow("Mode", "READ-ONLY", "teal")}
      ${railRow("AI Planning", "Review only", "")}
      ${railRow("Backtest Evidence", "Manual review required", "")}
      ${railRow("Monitoring", "Read-only", "")}
      ${railRow("Morning Summary", "Artifact review only", "")}
    </div>`;
}
function missingFieldsList(m) {
  const items = [];
  if (!m.sourceUrl) items.push("Source metadata");
  (m.blocking || []).forEach((b) => items.push(`Blocking: ${spaced(b)}`));
  if (m.directional && m.directional.status === "DIRECTION_UNKNOWN") items.push("Trade direction undefined");
  if (!m.rules.exit) items.push("Exit logic not extracted");
  if (m.tfMismatch) items.push("Defined vs tested timeframe mismatch");
  if (!items.length) items.push("No critical missing fields detected");
  return items.map((i) => `<div class="rail-miss"><span class="i">${icon("shield")}</span><span>${esc(i)}</span></div>`).join("");
}

/* ============================================================
   PAGE: Backtest Planner (read-only)
   ============================================================ */
function renderPlanner(c) {
  const id = state.selectedStrategyId || defaultStrategyId();
  const m = id ? strategyModel(id) : null;
  const plan = usableRunPlans()[0] || null;
  const pd = (plan && plan.data) || null;
  const planProfiles = pd && Array.isArray(pd.profiles) ? pd.profiles : null;
  const expected = pd && Array.isArray(pd.expected_artifacts) ? pd.expected_artifacts
    : ["run_plan.json", "scorecard_v2.json", "backtest_profile_result.json", "top_results.json", "artifact_index.json"];
  c.innerHTML = `
    <div class="banner warn"><div class="banner-icon">${icon("lock")}</div><div><h4>Read-only constraint</h4><p>This planner reviews draft run intent and expected artifact packages only. Artifact review only — no run-trigger or write-back affordances exist here.</p></div></div>

    ${pd ? `<div class="banner info"><div class="banner-icon">${icon("info")}</div><div><h4>run_plan.json present</h4><p>Loaded read-only from <code>${esc(plan.rel_path)}</code> (state: ${esc(plan.state)}).</p></div></div>` : ""}

    <section class="panel">
      <div class="panel-heading"><h3>Run Intent</h3><span>${pd ? "from run_plan.json" : "read-only"}</span></div>
      <div class="info-grid">
        ${infoCard("Run ID", pd ? pd.run_id : null, { empty: M.runplan })}
        ${infoCard("Selected Strategy", m ? m.displayName : (pd && pd.strategy_ids ? pd.strategy_ids.join(", ") : null), { empty: "No strategy selected" })}
        ${infoCard("Run Intent", "Prepare Gate 2 evidence package")}
        ${infoCard("Approval State", pd ? pd.approval_state : null, { empty: M.runplan })}
        ${infoCard("Case Count", pd && pd.case_count != null ? pd.case_count : null, { empty: M.runplan })}
        ${infoCard("Output Dir", pd ? pd.output_dir : null, { empty: M.runplan })}
      </div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Backtest Profiles Setup</h3><span>4 profiles</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Profile</th><th>Purpose</th><th>Setup Status</th></tr></thead>
        <tbody>${PROFILES.map((p) => `<tr><td class="mono">${esc(p)}</td><td>${esc(profilePurpose(p))}</td><td>${planProfiles ? (planProfiles.includes(p) ? badge("Selected in run_plan", "ok") : badge("Not selected", "neutral")) : badge("Pending run_plan.json", "neutral")}</td></tr>`).join("")}</tbody>
      </table></div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Run Constraints & Assumptions</h3><span>${pd ? "from run_plan.json" : "draft"}</span></div>
      <div class="info-grid">
        ${infoCard("Timeframes", pd && Array.isArray(pd.timeframes) && pd.timeframes.length ? pd.timeframes.join(", ") : null, { empty: M.runplan })}
        ${infoCard("Universe", pd && Array.isArray(pd.symbols) && pd.symbols.length ? pd.symbols.join(", ") : null, { empty: M.runplan })}
        ${infoCard("Risk / Sizing", pd && pd.walk_forward ? "See run_plan.walk_forward" : null, { empty: M.rulefreeze })}
        ${infoCard("Smoke Test", pd && pd.smoke_test != null ? (typeof pd.smoke_test === "object" ? "Configured" : String(pd.smoke_test)) : null, { empty: M.runplan })}
      </div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Parameter Space & Case Count</h3><span>read-only</span></div>
      ${pd && (pd.parameter_space != null || pd.case_count != null) ? `<div class="info-grid">
        ${infoCard("Case Count", pd.case_count != null ? pd.case_count : null, { empty: M.runplan })}
        ${infoCard("Parameter Space", pd.parameter_space != null ? (Array.isArray(pd.parameter_space) ? pd.parameter_space.length + " params" : Object.keys(pd.parameter_space).length + " keys") : null, { empty: M.runplan })}
      </div>` : emptyState("Parameter space preview and case-count calculation require run_plan.json — pending / artifact missing.")}
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Approval & Expected Outputs</h3><span>artifact contract</span></div>
      <div class="artifact-list">
        ${expected.map((a) => `<div class="artifact-item"><code>${esc(a)}</code><span class="a-state ${pd ? "plan" : "plan"}">${pd ? "Expected per run_plan" : "Expected / not present"}</span></div>`).join("")}
      </div>
      <div class="chip-row" style="margin-top:14px;">
        <span class="chip static">View Run Plan Draft (pending)</span>
        <span class="chip static">View Approval Package (pending)</span>
        <span class="chip static">View Expected Artifacts</span>
      </div>
    </section>
  `;
}

/* ============================================================
   PAGE: Backtest Runs
   ============================================================ */
function renderRuns(c) {
  const runs = backtestRuns();
  const summary = (snap().backtest_status && snap().backtest_status.summary) || {};
  const hb = snap().overnight_heartbeat || {};
  const completed = runs.filter((r) => String(r.status).toUpperCase() === "COMPLETED").length;
  const failed = runs.filter((r) => /FAIL|CRASH|ERROR/i.test(String(r.status))).length;
  const metric = (l, v, cls = "") => `<div class="lc-kpi"><span class="k">${esc(l)}</span><span class="v ${cls}">${esc(v)}</span></div>`;
  const statusArtifacts = usableRunStatus();
  const contractPanel = statusArtifacts.length ? `
    <section class="panel">
      <div class="panel-heading"><h3>Run Status (artifact contract)</h3><span>${statusArtifacts.length} run_status.json</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Run ID</th><th>Status</th><th>Stage</th><th class="num">Progress</th><th class="num">Workers</th><th>Updated</th><th>Output Dir</th></tr></thead>
        <tbody>${statusArtifacts.map((rec) => { const d = rec.data || {}; const prog = typeof d.progress === "object" && d.progress ? (d.progress.percent != null ? d.progress.percent + "%" : (d.progress.completed != null && d.progress.total != null ? `${d.progress.completed}/${d.progress.total}` : "—")) : (d.progress != null ? d.progress + "%" : "—"); return `<tr>
          <td><code>${esc(d.run_id || rec.run_id)}</code></td>
          <td>${badge(d.status || "—", gateTone(d.status))}</td>
          <td>${esc(d.current_stage || "—")}</td>
          <td class="num">${esc(prog)}</td>
          <td class="num">${d.workers != null ? esc(d.workers) : "—"}</td>
          <td>${esc(d.updated_at || d.finished_at || "—")}</td>
          <td><span class="cell-path">${esc(d.output_dir || rec.rel_path)}</span></td>
        </tr>`; }).join("")}</tbody>
      </table></div>
    </section>` : "";
  c.innerHTML = `
    ${contractPanel}
    <section class="panel">
      <div class="panel-heading"><h3>Backtest Runs</h3><span>${runs.length} runs</span></div>
      <div class="grid-4" style="margin-bottom:8px;">
        ${metric("Total Runs", summary.total_runs != null ? summary.total_runs : runs.length)}
        ${metric("Completed", completed)}
        ${metric("Failed / Crashed", failed, failed ? "na" : "")}
        ${metric("Latest Run", summary.last_run_id || "—")}
      </div>
      <div class="grid-2" style="margin-bottom:16px;">
        ${metric("Heartbeat", hb.available ? (hb.is_alive ? "Online" : "Stale") : "Not available")}
        ${metric("Last Successful", summary.last_successful_run || "—")}
      </div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Run ID</th><th>Status</th><th>Symbol(s)</th><th>Timeframe(s)</th><th class="num">Trades</th><th>Report Path</th></tr></thead>
        <tbody>${runs.length ? runs.slice(0, 60).map((r) => `
          <tr>
            <td><code>${esc(r.run_id || r.id || "—")}</code></td>
            <td>${badge(r.status || "—", gateTone(r.status))}</td>
            <td>${esc((r.symbols_tested || [r.symbol]).filter(Boolean).join(", ") || "—")}</td>
            <td>${esc((r.timeframes_tested || [r.timeframe]).filter(Boolean).join(", ") || "—")}</td>
            <td class="num">${r.trade_count != null ? r.trade_count : "—"}</td>
            <td><span class="cell-path">${esc(r.relative_source_path || r.report_path || M.artifact)}</span></td>
          </tr>`).join("") : `<tr><td colspan="6" class="empty-cell">No backtest runs in snapshot.</td></tr>`}</tbody>
      </table></div>
    </section>
  `;
}

/* ============================================================
   PAGE: Backtest Result Explorer
   ============================================================ */
function renderResultExplorer(c) {
  const scope = state.explorerScope;
  const scopeId = state.explorerStrategyId;
  let cards = scorecardCards().slice();
  if (scope === "strategy" && scopeId) cards = cardsForStrategy(scopeId);
  cards.sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0));
  const tfs = explorerTimeframes();
  const selected = cards[0];

  const sym = selected ? (selected.symbol || "—") : "—";
  const prows = scope === "strategy" && scopeId ? profileRowsForStrategy(scopeId) : profileRows();
  const hasProfile = prows.length > 0;
  const pr0 = prows[0];
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>Backtest Result Explorer</h3><span>${scope === "strategy" ? "strategy scope: " + esc(baseId(scopeId)) : "global scope"}</span></div>
      <p class="same-profile-warning">Only compare results within the same profile, timeframe, market universe, and score method. Do not compare SOURCE_NAKED with MTC_LIGHT, or 15m with 1D.</p>
      ${hasProfile ? researchOnlyBanner(pr0) : ""}
      <h4 class="section-title">Active Comparison State</h4>
      <div class="info-grid">
        ${infoCard("Score Method", hasProfile ? (pr0.score_method || "scorecard_v2") : "scorecard_v2")}
        ${infoCard("Profile", hasProfile ? pr0.profile : null, { empty: "Profile artifact missing" })}
        ${infoCard("Timeframe", hasProfile ? pr0.timeframe : (selected ? selected.timeframe : null), { empty: M.snapshot })}
        ${infoCard("Symbol / Universe", hasProfile ? (pr0.symbol || "—") : (scope === "strategy" ? sym : "All symbols in snapshot"))}
        ${infoCard("Run ID", hasProfile ? pr0.run_id : (selected ? selected.run_id : null), { empty: M.artifact })}
        ${infoCard("Artifact Status", hasProfile ? (profileRowHasFlags(pr0) ? "Profile-separated artifact present — research-only" : "Profile-separated artifact present") : "Legacy scorecard only — profile artifact missing")}
      </div>
      ${hasProfile && profileRowHasFlags(pr0) ? `<div style="margin-top:8px;">${profileRowBadges(pr0)}</div>` : ""}
      <h4 class="section-title" style="margin-top:16px;">Filters</h4>
      <div class="chip-row">
        ${["Strategy", "Profile", "Timeframe", "Symbol", "Score method", "Run ID", "Date range", "Min trade count", "Only benchmark beaters", "Only robust / OOS"].map((f) => `<span class="chip static" style="opacity:${hasProfile ? "1" : ".5"};">${esc(f)}</span>`).join("")}
      </div>
      <p class="summary" style="margin:10px 0 0;">${hasProfile ? "Read-only filters reflect available profile-separated artifact fields." : "Filter controls pending profile-separated artifact reader."}</p>
    </section>

    ${hasProfile ? "" : `<div class="banner warn"><div class="banner-icon">${icon("info")}</div><div><h4>Profile-separated artifacts not present</h4><p>No <code>backtest_profile_result.json</code> / profile-separated artifact exists yet. The four official profile buckets below stay empty; non-profile scorecard rows are quarantined in the Legacy Scorecard Reference section.</p></div></div>`}

    <h4 class="section-title">Official Profile Buckets</h4>
    ${PROFILES.map((p) => bucketBlock(p, (scope === "strategy" && scopeId ? profileRowsForStrategy(scopeId) : profileRowsFor(p)).filter((r) => r.profile === p))).join("")}

    <section class="bucket" style="border-color: rgba(180,90,30,0.3);">
      <div class="bucket-head">
        <div class="title"><span class="name">Legacy Scorecard Reference — profile missing</span>${cards.length ? badge(`${cards.length} rows`, "warn") : badge("no rows", "neutral")}</div>
      </div>
      <p class="summary">These are non-profile-separated scorecard rows. They are not validated SOURCE_NAKED / profile results and must not be compared across buckets.</p>
      ${cards.length ? `<div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Rank</th><th>Strategy</th><th>Asset / TF</th><th class="num">Gate 2</th><th>Gate Summary</th><th>Run</th></tr></thead>
        <tbody>${cards.slice(0, 25).map((cc, i) => `<tr>
          <td>#${i + 1}</td>
          <td>${esc(baseId(cc.base_strategy_id || cc.strategy_id))}</td>
          <td>${esc(cc.symbol || "—")} / ${esc(cc.timeframe || "—")}</td>
          <td class="num">${cc.gate2 && cc.gate2.score != null ? cc.gate2.score : "—"}</td>
          <td>${gateSummaryBadges(cc)}</td>
          <td><span class="cell-trunc">${esc(cc.run_name || cc.run_id || "—")}</span></td>
        </tr>`).join("")}</tbody>
      </table></div>` : emptyState("No scorecard rows in scope.")}
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Selected Result Detail</h3><span>${selected ? esc(baseId(selected.base_strategy_id || selected.strategy_id)) : "none"}</span></div>
      ${selected ? `<div class="info-grid">
        ${infoCard("Strategy", baseId(selected.base_strategy_id || selected.strategy_id))}
        ${infoCard("Asset / Timeframe", `${selected.symbol || "—"} / ${selected.timeframe || "—"}`)}
        ${infoCard("Run ID", selected.run_id, { empty: M.artifact })}
        ${infoCard("Gate 2 Score", selected.gate2 && selected.gate2.score != null ? selected.gate2.score : null, { empty: M.artifact })}
        ${infoCard("Parameter Set", null, { empty: M.artifact })}
        ${infoCard("Trade Count / Win Rate", null, { empty: "Raw metrics not in read model" })}
        ${infoCard("Source Path", selected.source_path, { empty: M.artifact, span2: true })}
      </div>` : emptyState("No result rows in scope.")}
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Chart Preview</h3><span>read-only</span></div>
      ${emptyState("Equity, drawdown, trade list, and price+entries/exits charts require equity_curve / trade_list artifacts — not present in read model.")}
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Required Result Artifacts</h3><span>contract</span></div>
      <div class="artifact-list">
        ${[
          ["run_plan.json", "run_plans"],
          ["artifact_index.json", "artifact_index"],
          ["backtest_profile_result.json", "profile_result_files"],
          ["top_results.json", "top_results"],
          ["result.json", null],
          ["metrics.json", null],
          ["equity_curve.csv/json", null],
          ["drawdown_curve.csv/json", null],
          ["trade_list.csv/json", null],
        ].map(([label, key]) => `<div class="artifact-item"><code>${esc(label)}</code>${artifactStateBadge(key)}</div>`).join("")}
      </div>
    </section>
  `;
}

/* Required-artifact state from night_artifacts (read-only). Untracked contract files
   (no reader key) stay Missing; tracked files reflect actual usable/incomplete/invalid. */
function artifactStateBadge(naKey) {
  if (!naKey) return `<span class="a-state missing">Missing</span>`;
  const recs = naList(naKey);
  if (!recs.length) return `<span class="a-state missing">Missing</span>`;
  const states = recs.map((r) => r.state);
  if (states.includes("usable")) return `<span class="a-state ok">Present / usable</span>`;
  if (states.includes("incomplete")) return `<span class="a-state warn">Present / incomplete</span>`;
  if (states.includes("invalid")) return `<span class="a-state bad">Present / invalid</span>`;
  return `<span class="a-state missing">Missing</span>`;
}

function kpi(v, suffix = "") { return (v === null || v === undefined) ? '<span class="value-muted">—</span>' : esc(v + suffix); }

/* Research-only / non-native-universe flags for a profile-separated result row.
   Reads only fields already present in the snapshot; never fabricates. */
function profileRowFlags(r) {
  const prov = r.provenance || {};
  const rob = (r.robustness && typeof r.robustness === "object") ? r.robustness : {};
  const pm = r.profile_mapping || {};
  const promo = String(r.promotion_status || "").toUpperCase();
  return {
    researchOnly: promo.includes("RESEARCH_ONLY") || promo.startsWith("NOT_PROMOTED"),
    universeMismatch: !!prov.universe_mismatch,
    nonRobust: rob.robust_final === false,
    interpreted: pm.is_interpretation === true,
    mismatchText: typeof prov.universe_mismatch === "string" ? prov.universe_mismatch : null,
    sourcePath: prov.source_path || r.source_rel_path || null,
  };
}
function profileRowBadges(r) {
  const f = profileRowFlags(r);
  const out = [];
  if (f.researchOnly) out.push(badge("RESEARCH ONLY", "warn"));
  if (f.universeMismatch) out.push(badge("UNIVERSE MISMATCH", "bad"));
  if (f.nonRobust) out.push(badge("NON-ROBUST", "warn"));
  if (f.interpreted) out.push(badge("PROFILE MAPPING INTERPRETED", "neutral"));
  return out.join(" ");
}
function profileRowHasFlags(r) {
  const f = profileRowFlags(r);
  return f.researchOnly || f.universeMismatch || f.nonRobust || f.interpreted;
}
/* Prominent warning banner for a flagged profile result (Result Explorer / SI preview). */
function researchOnlyBanner(r) {
  if (!profileRowHasFlags(r)) return "";
  const f = profileRowFlags(r);
  return `<div class="banner bad" style="margin-bottom:12px;">
    <div class="banner-icon">${icon("info")}</div>
    <div>
      <h4>Research-only profile result ${profileRowBadges(r)}</h4>
      <p>Real metrics are present, but this result is <strong>not native-universe validation</strong> and is not a production or paper-trading validation. The source universe/timeframe differs from the strategy identifier. Treat as research-only until a native universe run exists.</p>
      <div class="def-rows" style="margin-top:8px;">
        ${defRow("Strategy ID", baseId(r.strategy_id))}
        ${defRow("Source universe / TF", `${r.symbol || "—"} / ${r.timeframe || "—"}`)}
        ${f.mismatchText ? defRow("Universe mismatch", f.mismatchText) : ""}
        ${defRow("Promotion status", spaced(r.promotion_status || "—"))}
        ${defRow("robust_final", String((r.robustness && typeof r.robustness === "object") ? r.robustness.robust_final : "—"))}
        ${defRow("Source path", f.sourcePath || M.artifact)}
      </div>
    </div>
  </div>`;
}

function bucketBlock(profile, rows) {
  // rows are profile-separated result rows (night_artifacts.profile_results), never legacy.
  const top = rows.slice().sort((a, b) => Number(b.score || 0) - Number(a.score || 0)).slice(0, 5);
  return `
    <section class="bucket">
      <div class="bucket-head">
        <div class="title"><span class="name">${esc(profile)}</span>${top.length ? badge(`top ${top.length}`, "teal") : badge("no results", "neutral")}</div>
        ${top.length ? badge("Profile-separated artifact", "ok") : ""}
      </div>
      ${top.some(profileRowHasFlags) ? `<p class="summary" style="margin:0 0 10px;color:var(--amber,#f5a623);">Some rows are real sourced evidence but <strong>not native-universe validation</strong>. Flagged rows are research-only until a native universe run exists.</p>` : ""}
      ${top.length ? `<div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Rank</th><th>Strategy</th><th>Asset / TF</th><th class="num">Score</th><th class="num">Net Profit</th><th class="num">PF</th><th class="num">Max DD</th><th class="num">B&H Alpha</th><th class="num">Trades</th><th>Robustness</th><th>Promotion</th><th>Flags</th></tr></thead>
        <tbody>${top.map((r, i) => { const m = r.metrics || {}; return `<tr>
          <td>#${i + 1}</td>
          <td>${esc(baseId(r.strategy_id) || "—")}</td>
          <td>${esc(r.symbol || "—")} / ${esc(r.timeframe || "—")}</td>
          <td class="num">${kpi(r.score)}</td>
          <td class="num">${kpi(m.net_profit, "%")}</td>
          <td class="num">${kpi(m.profit_factor)}</td>
          <td class="num">${kpi(m.max_drawdown, "%")}</td>
          <td class="num">${kpi(m.buy_hold_alpha, "%")}</td>
          <td class="num">${kpi(m.trade_count)}</td>
          <td>${r.robustness ? badge(typeof r.robustness === "string" ? r.robustness : ((r.robustness.robust_final === false) ? "non-robust" : "see artifact"), (typeof r.robustness === "object" && r.robustness.robust_final === false) ? "warn" : "neutral") : '<span class="value-muted">—</span>'}</td>
          <td>${r.promotion_status ? badge(spaced(r.promotion_status), gateTone(r.promotion_status)) : '<span class="value-muted">—</span>'}</td>
          <td>${profileRowBadges(r) || '<span class="value-muted">—</span>'}</td>
        </tr>`; }).join("")}</tbody>
      </table></div>` : emptyState("No profile-separated result artifact yet.")}
    </section>`;
}
function gateSummaryBadges(c) {
  const s = (c.gate_summary && c.gate_summary.statuses) || {};
  return ["gate1", "gate1B", "gate2", "gate3"].map((g) => badge(g.replace("gate", "G") + " " + spaced(s[g] || "—"), gateTone(s[g]))).join(" ");
}

/* ============================================================
   PAGE: Strategy Leaderboard
   ============================================================ */
function renderLeaderboard(c) {
  const cards = scorecardCards().slice().sort((a, b) => Number((b.gate2 && b.gate2.score) || 0) - Number((a.gate2 && a.gate2.score) || 0));
  const buckets = [
    ["#1", "Top Gate 2 Reference #1"],
    ["#2", "Top Gate 2 Reference #2"],
    ["#3", "Top Gate 2 Reference #3"],
    ["#4", "Top Gate 2 Reference #4"],
  ];
  const prows = profileRows();
  const deltas = naList("leaderboard_delta");
  const validatedPanel = prows.length ? leaderboardValidatedPanel(prows, deltas) : "";
  c.innerHTML = `
    ${validatedPanel}
    <div class="banner warn"><div class="banner-icon">${icon("info")}</div><div><h4>${prows.length ? "Legacy Gate 2 references (below)" : "Not validated category winners"}</h4><p>${prows.length ? "Validated profile-separated winners are shown above. The references below remain legacy Gate 2 rows, not profile-separated." : "Category/profile-separated leaderboard artifacts are not present. These cards are legacy Gate 2 references, not validated category winners."}</p></div></div>

    <section class="panel">
      <div class="panel-heading"><h3>Top Gate 2 References</h3><span>${cards.length} rows</span></div>
      <div class="leader-grid">
        ${buckets.map(([rank, cat], i) => {
          const card = cards[i];
          return `<article class="leader-card">
            <div class="lc-head"><span class="lc-rank">${esc(rank)}</span><span class="lc-cat">${esc(cat)}</span></div>
            <h4>${card ? esc(baseId(card.base_strategy_id || card.strategy_id)) : "No validated candidate"}</h4>
            <div class="lc-prof">${card ? `Profile: artifact missing · TF: ${esc(card.timeframe || "—")}` : "No data"}</div>
            <div class="lc-kpis">
              <div class="lc-kpi"><span class="k">Gate 2</span><span class="v ${card && card.gate2 && card.gate2.score != null ? "" : "na"}">${card && card.gate2 && card.gate2.score != null ? card.gate2.score : "—"}</span></div>
              <div class="lc-kpi"><span class="k">Net Prof</span><span class="v na" style="font-size:10px;">Profile artifact missing</span></div>
              <div class="lc-kpi"><span class="k">Drawdown</span><span class="v na" style="font-size:10px;">Profile artifact missing</span></div>
            </div>
            ${card ? `<button class="btn purple mini" type="button" onclick="openExplorerForStrategy('${esc(baseId(card.base_strategy_id || card.strategy_id))}')">Open Result Explorer</button>` : `<span class="empty-pill">No candidate</span>`}
          </article>`;
        }).join("")}
      </div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Full Ranking</h3><span>top 25</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Rank</th><th>Strategy</th><th>Profile</th><th>Asset / TF</th><th class="num">Score</th><th>Gate Summary</th><th>Benchmark</th></tr></thead>
        <tbody>${cards.length ? cards.slice(0, 25).map((c, i) => `<tr>
          <td>${i + 1}</td>
          <td>${esc(baseId(c.base_strategy_id || c.strategy_id))}</td>
          <td><span class="empty-pill">missing</span></td>
          <td>${esc(c.symbol || "—")} / ${esc(c.timeframe || "—")}</td>
          <td class="num">${c.gate2 && c.gate2.score != null ? c.gate2.score : "—"}</td>
          <td>${gateSummaryBadges(c)}</td>
          <td>${c.gate2 && Number(c.gate2.score) >= 80 ? badge("candidate", "ok") : badge("below", "neutral")}</td>
        </tr>`).join("") : `<tr><td colspan="7" class="empty-cell">No leaderboard data.</td></tr>`}</tbody>
      </table></div>
    </section>
  `;
}

function leaderboardValidatedPanel(prows, deltas) {
  // Best profile-separated row per profile (validated winners from artifacts only).
  const best = {};
  prows.forEach((r) => {
    const cur = best[r.profile];
    if (!cur || Number(r.score || 0) > Number(cur.score || 0)) best[r.profile] = r;
  });
  const present = PROFILES.filter((p) => best[p]);
  if (!present.length) return "";
  const anyFlagged = present.some((p) => profileRowHasFlags(best[p]));
  return `
    <div class="banner ${anyFlagged ? "warn" : "info"}"><div class="banner-icon">${icon("trend")}</div><div><h4>Top profile-separated results ${anyFlagged ? "(research-only — not validated category winners)" : ""}</h4><p>From <code>backtest_profile_result.json</code>${deltas.length ? " / leaderboard_delta.json" : ""}. Each card is the top score within its official profile.${anyFlagged ? " Flagged cards are real sourced evidence but <strong>not native-universe validation</strong> and are not production/paper-ready." : ""}</p></div></div>
    <section class="panel">
      <div class="panel-heading"><h3>${anyFlagged ? "Top Profile Results (research-only)" : "Validated Profile Winners"}</h3><span>${present.length} profiles</span></div>
      <div class="leader-grid">
        ${present.map((p) => { const r = best[p]; const m = r.metrics || {}; const flagged = profileRowHasFlags(r); return `<article class="leader-card">
          <div class="lc-head"><span class="lc-rank">${flagged ? "⚠" : "★"}</span><span class="lc-cat">${esc(p)}</span></div>
          <h4>${esc(baseId(r.strategy_id) || "—")}</h4>
          <div class="lc-prof">${esc(r.symbol || "—")} · TF: ${esc(r.timeframe || "—")} · ${esc(r.score_method || "scorecard_v2")}</div>
          ${flagged ? `<div style="margin:4px 0 8px;">${profileRowBadges(r)}</div>` : ""}
          <div class="lc-kpis">
            <div class="lc-kpi"><span class="k">Score</span><span class="v">${kpi(r.score)}</span></div>
            <div class="lc-kpi"><span class="k">Net Prof</span><span class="v" style="font-size:14px;">${kpi(m.net_profit, "%")}</span></div>
            <div class="lc-kpi"><span class="k">Max DD</span><span class="v" style="font-size:14px;">${kpi(m.max_drawdown, "%")}</span></div>
          </div>
          <button class="btn purple mini" type="button" onclick="openExplorerForStrategy('${esc(baseId(r.strategy_id))}')">Open Result Explorer</button>
        </article>`; }).join("")}
      </div>
    </section>`;
}

/* ============================================================
   PAGE: Paper Trading
   ============================================================ */
function renderPaperTrading(c) {
  const rows = pipelineRows().map((r) => strategyModel(rowId(r)));
  const ready = rows.filter((m) => m.promotable);
  const locked = rows.filter((m) => !m.promotable);
  const candCard = (m) => `
    <article class="strategy-card">
      <div class="sc-head"><div><code>${esc(m.id)}</code><h4>${esc(m.displayName)}</h4></div>${badge(m.promotable ? "Ready" : "Locked", m.promotable ? "ok" : "neutral")}</div>
      <div class="def-rows">
        ${defRow("Gate 2 Evidence", spaced(m.gates.g2.status))}
        ${defRow("Gate 3 Readiness", spaced(m.gates.g3.status))}
        ${defRow(m.promotable ? "Requirement" : "Locked Reason", m.promotable ? "Human approval" : (m.blocking.join(", ") || "Gate 2 evidence"))}
        ${defRow("Approval Package", null, "Pending / artifact missing")}
      </div>
      <div class="chip-row">
        <span class="chip static">View Approval Package (pending)</span>
        <span class="chip static">View Gate 3 Checklist (pending)</span>
      </div>
    </article>`;
  c.innerHTML = `
    <div class="banner warn"><div class="banner-icon">${icon("lock")}</div><div><h4>Read-only readiness view</h4><p>Candidates remain locked until validated Gate 2 evidence and Gate 3 readiness artifacts exist. This view only reviews readiness packages; no trading actions are available.</p></div></div>

    <section class="panel">
      <div class="panel-heading"><h3>Ready Candidates</h3><span>${ready.length}</span></div>
      <div class="strategy-card-grid">${ready.length ? ready.map(candCard).join("") : emptyState("No promotable candidates in current snapshot.")}</div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Locked Candidates</h3><span>${locked.length}</span></div>
      <div class="strategy-card-grid">${locked.length ? locked.slice(0, 12).map(candCard).join("") : emptyState("No locked candidates.")}</div>
    </section>
  `;
}

/* ============================================================
   PAGE: AI Knowledge Base
   ============================================================ */
function renderKnowledge(c) {
  const comps = [];
  registryEntries().forEach((r) => {
    const kinds = Array.isArray(r.candidate_kind) ? r.candidate_kind : [];
    kinds.forEach((k) => comps.push({ type: k, from: rowId(r), fromName: r.title || r.name || titleCase(baseId(rowId(r))) }));
  });
  const types = {};
  comps.forEach((x) => { (types[x.type] = types[x.type] || []).push(x); });
  const typeKeys = Object.keys(types);
  const reuse = (t) => (t.includes("exit") || t.includes("entry") ? "ready" : t.includes("money") || t.includes("guard") ? "review" : "review");
  const reuseLabel = (cls) => cls === "ready" ? "USEFUL" : cls === "no" ? "DO NOT REUSE" : "REVIEW NEEDED";

  c.innerHTML = `
    <div class="banner info"><div class="banner-icon">${icon("cpu")}</div><div><h4>Reusable component library</h4><p>Components are derived from registry candidate_kind tags. Reuse ratings are heuristic until an extraction reader is implemented.</p></div></div>
    <div class="kb-grid">
      <section class="panel">
        <div class="panel-heading"><h3>Reusable Component Library</h3><span>${comps.length} tagged</span></div>
        ${comps.length ? typeKeys.map((t) => {
          const cls = reuse(t);
          return `<div class="kb-item">
            <span class="kb-tag ${cls}">${esc(reuseLabel(cls))}</span>
            <div>
              <h5>${esc(titleCase(t))}</h5>
              <p>Extracted from ${types[t].length} strateg${types[t].length === 1 ? "y" : "ies"}, e.g. ${esc(types[t][0].fromName)}. Related area: ${esc(t.includes("entry") ? "Gate 1 rules" : t.includes("sl_tp") || t.includes("money") ? "Risk / sizing" : "Signal module")}.</p>
            </div>
          </div>`;
        }).join("") : emptyState("No reusable components tagged in registry.")}
      </section>
      <section class="panel">
        <div class="panel-heading"><h3>Group by Type</h3><span>${typeKeys.length}</span></div>
        <div class="def-rows">${typeKeys.length ? typeKeys.map((t) => defRow(titleCase(t), `${types[t].length} component(s)`)).join("") : emptyState("No component types.")}</div>
        <div class="banner info" style="margin-top:14px;margin-bottom:0;"><div class="banner-icon">${icon("info")}</div><div><h4>Synthesis</h4><p>Component synthesis requires agent-level orchestration — not available in this read-only view.</p></div></div>
      </section>
    </div>
  `;
}

/* ============================================================
   PAGE: Advanced Artifacts
   ============================================================ */
function renderArtifacts(c) {
  const groups = [
    ["Run Planning", ["run_plan.json", "run_status.json", "progress.json"]],
    ["Status / Heartbeat", ["heartbeat.json", "artifact_index.json", "summary.json"]],
    ["Result Evidence", ["backtest_profile_result.json", "top_results.json"]],
    ["Leaderboard / Benchmark", ["leaderboard_delta.json", "benchmark_update_candidate.json"]],
    ["Reports", ["morning_report.md"]],
  ];
  const consumer = {
    "run_plan.json": "Backtest Planner", "run_status.json": "Backtest Runs", "progress.json": "Backtest Runs",
    "heartbeat.json": "Backtest Runs", "artifact_index.json": "Result Explorer", "summary.json": "Command Center Home",
    "backtest_profile_result.json": "Result Explorer", "top_results.json": "Result Explorer / Leaderboard",
    "leaderboard_delta.json": "Leaderboard", "benchmark_update_candidate.json": "Leaderboard", "morning_report.md": "Reports",
  };
  const na = nightArtifacts();
  const byFile = {
    "run_plan.json": naList("run_plans"),
    "run_status.json": naList("run_status"),
    "artifact_index.json": naList("artifact_index"),
    "backtest_profile_result.json": naList("profile_result_files"),
    "top_results.json": naList("top_results"),
    "leaderboard_delta.json": naList("leaderboard_delta"),
    "benchmark_update_candidate.json": naList("benchmark_update_candidates"),
  };
  const companions = Array.isArray(na.companions) ? na.companions : [];
  const compPresent = new Set(companions.map((x) => x.type));
  function stateCell(a) {
    const recs = byFile[a];
    if (recs && recs.length) {
      const states = recs.map((r) => r.state);
      const st = states.includes("invalid") ? "invalid" : states.includes("incomplete") ? "incomplete" : "usable";
      return badge(`${recs.length} present · ${st}`, st === "usable" ? "ok" : st === "incomplete" ? "warn" : "bad");
    }
    if (compPresent.has(a)) return badge("present", "ok");
    return badge("missing", "neutral");
  }
  function pathCell(a) {
    const recs = byFile[a];
    if (recs && recs.length) return `<span class="cell-path">${esc(recs[0].rel_path)}</span>`;
    const comp = companions.find((x) => x.type === a);
    if (comp) return `<span class="cell-path">${esc(comp.rel_path)}</span>`;
    return `<span class="value-muted">expected under 05_BACKTEST_RESULTS/&lt;run&gt;/</span>`;
  }
  const summaryCard = (l, v, cls = "") => `<div class="lc-kpi"><span class="k">${esc(l)}</span><span class="v ${cls}">${esc(v)}</span></div>`;
  const s = na.summary || {};
  c.innerHTML = `
    <div class="banner info"><div class="banner-icon">${icon("db")}</div><div><h4>Artifact contract</h4><p>Night artifact contract grouped by purpose, wired to the read-only <code>night_artifacts</code> reader. This frontend does not ingest or write artifacts.</p></div></div>
    <section class="panel">
      <div class="panel-heading"><h3>Contract Summary</h3><span>read-only</span></div>
      <div class="grid-4">
        ${summaryCard("Expected Types", s.expected_types != null ? s.expected_types : "—")}
        ${summaryCard("Present Types", s.present_types != null ? s.present_types : 0)}
        ${summaryCard("Usable", s.usable != null ? s.usable : 0, s.usable ? "" : "na")}
        ${summaryCard("Invalid", s.invalid != null ? s.invalid : 0, s.invalid ? "na" : "")}
      </div>
    </section>
    ${(() => {
      const prs = profileRows();
      if (!prs.length) return "";
      const mismatch = prs.filter((r) => profileRowFlags(r).universeMismatch).length;
      const research = prs.filter((r) => profileRowFlags(r).researchOnly).length;
      const nonrobust = prs.filter((r) => profileRowFlags(r).nonRobust).length;
      return `<section class="panel">
        <div class="panel-heading"><h3>Profile Result Rows — Quality Flags</h3><span>${prs.length} rows</span></div>
        <div class="grid-4">
          ${summaryCard("Profile Rows", prs.length)}
          ${summaryCard("Universe Mismatch Rows", mismatch, mismatch ? "na" : "")}
          ${summaryCard("Research-only Rows", research, research ? "na" : "")}
          ${summaryCard("Non-robust Rows", nonrobust, nonrobust ? "na" : "")}
        </div>
        ${(mismatch || research || nonrobust) ? `<p class="summary" style="margin:10px 0 0;color:var(--amber,#f5a623);">Flagged rows are real sourced evidence but not native-universe validation. See Result Explorer for per-row badges.</p>` : ""}
      </section>`;
    })()}
    ${groups.map(([title, items]) => `
      <section class="panel">
        <div class="panel-heading"><h3>${esc(title)}</h3><span>${items.length}</span></div>
        <div class="table-wrap"><table class="grid-table">
          <thead><tr><th>Artifact</th><th>State</th><th>Consumed By</th><th>Path</th></tr></thead>
          <tbody>${items.map((a) => `<tr><td><code>${esc(a)}</code></td><td>${stateCell(a)}</td><td>${esc(consumer[a] || "—")}</td><td>${pathCell(a)}</td></tr>`).join("")}</tbody>
        </table></div>
      </section>`).join("")}
  `;
}

/* ============================================================
   PAGE: Diagnostics
   ============================================================ */
function renderDiagnostics(c) {
  const diags = diagnosticItems();
  const okCount = diags.filter((d) => d.ok).length;
  const routes = NAV.length;
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>System Diagnostics</h3><span>${diags.length} file checks</span></div>
      <div class="grid-4" style="margin-bottom:8px;">
        <div class="lc-kpi"><span class="k">Data Contract Coverage</span><span class="v">${okCount}/${diags.length}</span></div>
        <div class="lc-kpi"><span class="k">UI Route Coverage</span><span class="v">${routes}/${routes}</span></div>
        <div class="lc-kpi"><span class="k">Read-only API</span><span class="v ${state.health && state.health.overall_ok ? "" : "na"}">${state.health && state.health.overall_ok ? "OK" : "Check"}</span></div>
        <div class="lc-kpi"><span class="k">Placeholder-only Pages</span><span class="v">0</span></div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>File Diagnostics</h3><span>${diags.length}</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Feed</th><th>Path</th><th>Required</th><th>JSON</th><th>Schema</th><th>Status</th></tr></thead>
        <tbody>${diags.length ? diags.map((d) => `<tr>
          <td>${esc(d.key)}</td>
          <td><span class="cell-path">${esc(d.path || "—")}</span></td>
          <td>${d.required ? "Yes" : "No"}</td>
          <td>${badge(d.json_ok === false ? "Check" : "OK", d.json_ok === false ? "bad" : "ok")}</td>
          <td>${badge(d.schema_ok === false ? "Check" : "OK", d.schema_ok === false ? "bad" : "ok")}</td>
          <td>${badge(d.ok ? "OK" : "Check", d.ok ? "ok" : "bad")}</td>
        </tr>`).join("") : `<tr><td colspan="6" class="empty-cell">No diagnostics in snapshot.</td></tr>`}</tbody>
      </table></div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Artifact Contract Diagnostics</h3><span>night_artifacts</span></div>
      <div class="grid-4" style="margin-bottom:8px;">
        ${(() => { const s = nightArtifacts().summary || {}; return [
          ["Expected Types", s.expected_types != null ? s.expected_types : "—", ""],
          ["Present Types", s.present_types != null ? s.present_types : 0, ""],
          ["Missing Types", s.missing_types != null ? s.missing_types : 0, ""],
          ["Invalid", s.invalid != null ? s.invalid : 0, s.invalid ? "na" : ""],
          ["Incomplete", s.incomplete != null ? s.incomplete : 0, ""],
          ["Usable", s.usable != null ? s.usable : 0, ""],
          ["Profile Rows", s.profile_result_rows != null ? s.profile_result_rows : 0, ""],
          ["Snapshot Reader", nightArtifacts().schema_version ? "OK" : "Check", nightArtifacts().schema_version ? "" : "na"],
        ].map(([l, v, cls]) => `<div class="lc-kpi"><span class="k">${esc(l)}</span><span class="v ${cls}">${esc(v)}</span></div>`).join(""); })()}
      </div>
      ${(nightArtifacts().warnings || []).length ? `<div class="def-rows">${nightArtifacts().warnings.map((w) => defRow("Warning", w)).join("")}</div>` : ""}
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>UI Route Coverage</h3><span>${routes} routes</span></div>
      <div class="info-grid">${NAV.map((n) => infoCard(n.label, "Implemented")).join("")}</div>
    </section>
  `;
}

/* ============================================================
   PAGE: Reports
   ============================================================ */
function renderReports(c) {
  const reports = reportItems();
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>Reports</h3><span>${reports.length} reports</span></div>
      <p class="summary">Read-only report list from report_manifest. Select a report to load its content via the read-only report API.</p>
      <div class="report-layout">
        <div class="report-list" id="reportList">
          ${reports.length ? reports.map((r) => `<div class="report-item" data-path="${esc(r.path || "")}">
            <span class="cat">${esc(r.category || "report")}</span>
            <h5>${esc(r.title || "Untitled")}</h5>
            <code>${esc(r.path || "")}</code>
          </div>`).join("") : emptyState("No reports indexed.")}
        </div>
        <div class="report-viewer">
          <div class="report-viewer-head"><span class="meta" id="rvMeta">No report selected</span><h4 id="rvTitle">Report Viewer</h4></div>
          <div class="report-viewer-body" id="rvBody"><p class="value-muted">Select a report from the list to load its content.</p></div>
        </div>
      </div>
    </section>
  `;
  const list = $("#reportList");
  if (list) list.addEventListener("click", async (e) => {
    const item = e.target.closest("[data-path]");
    if (!item) return;
    $$("#reportList .report-item").forEach((x) => x.classList.remove("is-active"));
    item.classList.add("is-active");
    const path = item.dataset.path;
    $("#rvMeta").textContent = path;
    $("#rvTitle").textContent = "Loading…";
    $("#rvBody").innerHTML = `<p class="value-muted">Loading…</p>`;
    try {
      const payload = await fetchJson(`/api/report?path=${encodeURIComponent(path)}`);
      const report = payload.report || {};
      $("#rvTitle").textContent = report.title || payload.path || path;
      $("#rvMeta").textContent = `${report.category || "report"} · ${payload.size_bytes != null ? payload.size_bytes + " bytes" : ""}`;
      if (payload.content) {
        $("#rvBody").innerHTML = renderMarkdown(payload.content);
      } else {
        $("#rvBody").innerHTML = emptyState("Report manifest exists; content reader not implemented or content empty.");
      }
    } catch (err) {
      $("#rvTitle").textContent = "Unable to load report";
      $("#rvBody").innerHTML = `<p class="value-muted">${esc(err.message || String(err))}</p>`;
    }
  });
}

/* ============================================================
   PAGE: Read Model / Data Model
   ============================================================ */
function renderReadModel(c) {
  const s = snap();
  const keys = Object.keys(s).sort();
  c.innerHTML = `
    <section class="panel">
      <div class="panel-heading"><h3>Page → Read Model Mapping</h3><span>${PAGE_FEEDS.length} pages</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Page</th><th>Read model feeds</th></tr></thead>
        <tbody>${PAGE_FEEDS.map(([p, f]) => `<tr><td>${esc(p)}</td><td><span class="cell-path">${esc(f)}</span></td></tr>`).join("")}</tbody>
      </table></div>
    </section>

    <section class="panel">
      <div class="panel-heading"><h3>Snapshot Top-Level Keys</h3><span>${keys.length} keys</span></div>
      <div class="table-wrap"><table class="grid-table">
        <thead><tr><th>Key</th><th>Type</th><th>Size</th></tr></thead>
        <tbody>${keys.map((k) => {
          const v = s[k];
          const type = Array.isArray(v) ? "array" : typeof v;
          const size = Array.isArray(v) ? `${v.length} items` : (v && typeof v === "object" ? `${Object.keys(v).length} keys` : "—");
          return `<tr><td><code>${esc(k)}</code></td><td>${esc(type)}</td><td>${esc(size)}</td></tr>`;
        }).join("")}</tbody>
      </table></div>
    </section>
  `;
}

/* ---------------- markdown (read-only render) ---------------- */
function renderMarkdown(md) {
  if (!md) return emptyState("Empty content.");
  let html = esc(md);
  html = html.replace(/^### (.+)$/gm, "<h5>$1</h5>");
  html = html.replace(/^## (.+)$/gm, "<h4>$1</h4>");
  html = html.replace(/^# (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^[-*] (.+)$/gm, '<div class="md-list">$1</div>');
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\n\n/g, '<div class="md-gap"></div>');
  html = html.replace(/\n/g, "<br>");
  return html;
}

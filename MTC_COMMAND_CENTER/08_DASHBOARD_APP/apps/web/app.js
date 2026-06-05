const state = {
  snapshot: null,
  health: null,
  selectedReportPath: null
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

document.addEventListener("DOMContentLoaded", () => {
  bindTabs();
  bindFilters();
  $("#refreshButton").addEventListener("click", () => loadDashboard(true));
  loadDashboard();
});

function bindTabs() {
  $$(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      const tab = button.dataset.tab;
      $$(".tab").forEach((item) => item.classList.toggle("is-active", item === button));
      $$(".tab-panel").forEach((panel) => {
        panel.classList.toggle("is-active", panel.dataset.panel === tab);
      });
    });
  });
}

function bindFilters() {
  $("#taskSearch").addEventListener("input", renderTasks);
  $("#taskStatusFilter").addEventListener("change", renderTasks);
  $("#reportSearch").addEventListener("input", renderReports);
  $("#reportCategoryFilter").addEventListener("change", renderReports);
  $("#pipelineSearch").addEventListener("input", renderPipeline);
  $("#pipelineScoreFilter").addEventListener("change", renderPipeline);
  $("#pipelineActionFilter").addEventListener("change", renderPipeline);
  $("#auditSearch").addEventListener("input", renderAudit);
  [
    "#auditStrategyFilter",
    "#auditQualityFilter",
    "#auditRulesFilter",
    "#auditSourceFilter",
    "#auditTxVerdictFilter",
    "#auditEligibleFilter",
    "#auditBlockedFilter",
    "#auditCanonicalFilter",
    "#auditStepFilter",
    "#auditScoreFilter"
  ].forEach((selector) => {
    const control = $(selector);
    if (control) {
      control.addEventListener("change", renderAudit);
    }
  });
  $("#mtcV2Search").addEventListener("input", renderMtcV2Readiness);
  $("#mtcV2StatusFilter").addEventListener("change", renderMtcV2Readiness);
  $("#mtcV2ScoreFilter").addEventListener("change", renderMtcV2Readiness);
  [
    "#researchStrategySearch", "#researchCategoryFilter", "#researchMethodFilter",
    "#researchRegimeFilter", "#researchTimeframeFilter", "#researchTagFilter",
    "#researchStatusFilter",
    "#researchTriageSearch", "#researchTriageQualityFilter",
    "#researchTriageTranscriptFilter", "#researchTriageEligibleFilter",
  ].forEach((sel) => {
    const el = $(sel);
    if (el) el.addEventListener(sel.endsWith("Search") ? "input" : "change", renderResearchLab);
  });
  $("#reportList").addEventListener("click", (event) => {
    const button = event.target.closest("[data-report-path]");
    if (button) {
      loadReport(button.dataset.reportPath);
    }
  });
  $("#taskRows").addEventListener("click", (event) => {
    const button = event.target.closest("[data-report-path]");
    if (button) {
      activateTab("reports");
      loadReport(button.dataset.reportPath);
    }
  });
}

function activateTab(tabName) {
  $$(".tab").forEach((item) => item.classList.toggle("is-active", item.dataset.tab === tabName));
  $$(".tab-panel").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.panel === tabName);
  });
}

async function loadDashboard(forceRefresh = false) {
  setNotice("");
  $("#healthPill").textContent = "checking";
  $("#healthPill").className = "status-pill";
  setTableLoading();

  try {
    const [health, snapshot] = await Promise.all([
      fetchJson("/healthz"),
      fetchJson(forceRefresh ? "/api/snapshot?refresh=1" : "/api/snapshot")
    ]);
    state.health = health;
    state.snapshot = snapshot;
    render();
  } catch (error) {
    setNotice(error.message || String(error));
    $("#healthPill").textContent = "offline";
    $("#healthPill").className = "status-pill bad";
  }
}

function setTableLoading() {
  $("#pipelineCount").textContent = "loading...";
  $("#auditCount").textContent = "loading...";
  $("#mtcV2Count").textContent = "loading...";
  $("#pipelineRows").innerHTML = `<tr><td colspan="9" class="empty-cell">Loading strategy snapshot...</td></tr>`;
  $("#auditRows").innerHTML = `<tr><td colspan="9" class="empty-cell">Loading audit snapshot...</td></tr>`;
  $("#mtcV2Rows").innerHTML = `<tr><td colspan="7" class="empty-cell">Loading MTC_V2 readiness...</td></tr>`;
}

async function fetchJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || `${url} returned ${response.status}`);
  }
  return payload;
}

async function loadReport(path) {
  if (!path) {
    return;
  }
  state.selectedReportPath = path;
  $("#reportViewerTitle").textContent = "Loading";
  $("#reportViewerMeta").textContent = path;
  $("#reportViewerBody").innerHTML = "";
  try {
    const payload = await fetchJson(`/api/report?path=${encodeURIComponent(path)}`);
    const report = payload.report || {};
    $("#reportViewerTitle").textContent = report.title || payload.path;
    $("#reportViewerMeta").textContent = `${report.category || "report"} / ${report.report_id || "--"} / ${payload.size_bytes} bytes`;
    $("#reportViewerBody").innerHTML = renderMarkdown(payload.content || "");
    renderReports();
  } catch (error) {
    $("#reportViewerTitle").textContent = "Unable to load report";
    $("#reportViewerMeta").textContent = path;
    $("#reportViewerBody").innerHTML = `<p>${escapeHtml(error.message || String(error))}</p>`;
  }
}

function render() {
  renderHeader();
  renderPipeline();
  renderAudit();
  renderMtcV2Readiness();
  renderHome();
  renderTasks();
  renderParity();
  renderBacktest();
  renderRegistry();
  renderResearchLab();
  renderPineBuilder();
  renderOptimization();
  renderLiveOps();
  renderReports();
  renderDiagnostics();
  if (state.selectedStrategyId) {
    openUnifiedStrategyDetail(state.selectedStrategyId);
  } else {
    syncUnifiedDetailVisibility();
  }
}
function renderPipeline() {
  const pipe = state.snapshot.candidate_pipeline || {};
  const allRows = pipe.rows || [];
  const hiddenParents = hiddenSourceParentIds();
  const rows = allRows.filter((row) => !hiddenParents.has(row.id));
  const stages = pipe.stages || [];
  const counts = (pipe.summary && pipe.summary.stage_done_counts) || {};
  $("#pipelineIntro").textContent = "Each row is one strategy journey. The Stg tag is the stable triage code, the score is a heuristic fit score out of 100, and the next action tells you the single best next step.";
  populateSelect("#pipelineActionFilter", uniqueValues(rows.map((row) => row.next_action)), "All");
  const filtered = filterPipelineRows(rows);
  $("#pipelineCount").textContent = `${filtered.length}/${rows.length} ${rows.length === 1 ? "strategy" : "strategies"}${allRows.length !== rows.length ? ` · ${allRows.length - rows.length} source parents hidden` : ""}`;
  $("#pipelineSummary").innerHTML = stages.map((s) => `
    <div class="parity-cell">
      <span>${escapeHtml(s.label)}</span>
      <strong>${Number(counts[s.key] || 0)}</strong>
    </div>
  `).join("");
  const stageKeys = stages.map((s) => s.key);
  if (!filtered.length) {
    $("#pipelineRows").innerHTML = `<tr><td colspan="${stageKeys.length + 3}" class="empty-cell">No candidates yet</td></tr>`;
    return;
  }
  $("#pipelineRows").innerHTML = filtered.map((row) => {
    const cells = stageKeys.map((k) => stageCell(row.stages[k] || {})).join("");
    const sub = row.symbol ? `${row.symbol} ${row.timeframe}` : (row.timeframe || "");
    const fam = (row.description && row.description.family) ? row.description.family : "";
    const stgCode = row.stg_code ? `<div class="muted-sub"><code>${escapeHtml(row.stg_code)}</code></div>` : "";
    return `
      <tr class="row-click" data-id="${escapeHtml(row.id)}" title="Click for details">
        <td><code>${escapeHtml(row.id)}</code>${stgCode}${fam ? `<div class="muted-sub">${escapeHtml(fam)}</div>` : ""}${sub ? `<div class="muted-sub">${escapeHtml(sub)}</div>` : ""}</td>
        <td>${renderScoreBadge(row.scorecard || row.score)}</td>
        ${cells}
        <td>${renderActionCell(row.next_action || "--", row.next_action_hint || "")}</td>
      </tr>
    `;
  }).join("");

  const tbody = $("#pipelineRows");
  if (!tbody.dataset.bound) {
    tbody.dataset.bound = "1";
    tbody.addEventListener("click", (event) => {
      const tr = event.target.closest("tr[data-id]");
      if (tr) openUnifiedStrategyDetail(tr.dataset.id);
    });
  }
}

function renderAudit() {
  const audit = state.snapshot.candidate_audit || {};
  const allRows = audit.rows || [];
  const rows = allRows.filter((row) => row.visible_in_strategy_tables !== false);
  const summary = audit.summary || {};
  const txRec = state.snapshot.transcript_reclassification || null;
  const txByCid = {};
  if (txRec && txRec.rows) {
    for (const tr of txRec.rows) { txByCid[tr.candidate_id] = tr; }
  }
  const txCounts = txRec ? txRec.verdict_counts || {} : {};
  $("#auditIntro").textContent = "This table explains why a row is eligible, blocked, or parked. Sources is the raw scanned record count, Source audit means the source or formula still needs verification, and Next step is the immediate action recommended by the read-only gate.";
  $("#auditCount").textContent = `${rows.length}/${allRows.length} ${rows.length === 1 ? "record" : "records"}${summary.source_parent_rows ? ` · ${summary.source_parent_rows} source parents hidden` : ""}`;
  $("#auditSummary").innerHTML = [
    ["Eligible", summary.eligible_for_backtest_rows, "Rows that can go straight to backtest from the current read-only gate."],
    ["Blocked", summary.blocked_rows, "Rows parked because the source, formula, or classification still needs work."],
    ["Split required", summary.split_required_rows, "Rows that must be split into separate indicator cases before testing."],
    ["Source audit", summary.source_audit_rows, "Rows that need exact source/formula verification before any backtest."],
    ["Source parents", summary.source_parent_rows || 0, "Original video/source rows hidden from normal strategy queues when extracted child candidates exist."],
    ["Duplicates", summary.duplicate_rows, "Duplicate rows mapped to one canonical record."],
    ["Deterministic", summary.deterministic_rule_rows, "Rows with mechanically testable rules visible to the audit layer."],
    ["Source material", summary.source_material_rows, "Rows with at least a URL or transcript path attached."],
    ["Sources", audit.source_record_count || 0, "Raw scanned source records across JSONL and CSV inputs, not unique strategies."]
  ].concat(txRec ? [
    ["Tx: Likely misclassified", txCounts.LIKELY_MISCLASSIFIED || 0, "Transcripts flagged as likely misclassified — testable rules visible."],
    ["Tx: Review human", txCounts.REVIEW_HUMAN || 0, "Transcripts needing manual review — ambiguous signals."],
    ["Tx: Keep rejected", txCounts.KEEP_REJECTED || 0, "Transcripts correctly rejected — no numeric thresholds."],
  ] : []).map(([label, value, title]) => `
    <div class="parity-cell" title="${escapeHtml(title)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(formatNumber(value ?? 0))}</strong>
    </div>
  `).join("");

  populateAuditFilters(rows);
  const filtered = filterAuditRows(rows);
  if (!filtered.length) {
    $("#auditRows").innerHTML = `<tr><td colspan="10" class="empty-cell">No audit rows match</td></tr>`;
    syncUnifiedDetailVisibility();
    return;
  }

  $("#auditRows").innerHTML = filtered.map((row) => {
    const tx = txByCid[row.id] || null;
    const txVerdict = tx ? tx.verdict : (row.has_transcript && !tx ? "NO_SCAN" : "");
    const txReason = tx ? tx.reason : "";
    const txBadge = txVerdict
      ? badge(txVerdict,
          txVerdict === "LIKELY_MISCLASSIFIED" ? "warn" :
          txVerdict === "REVIEW_HUMAN" ? "neutral" :
          txVerdict === "ALREADY_OK" ? "ok" :
          txVerdict === "KEEP_REJECTED" ? "bad" : "muted")
      : `<span class="muted-sub">—</span>`;
    return `
    <tr class="row-click" data-audit-id="${escapeHtml(row.id)}" title="Detay için tıkla">
      <td>
        <code>${escapeHtml(row.id || "--")}</code>
        ${row.stg_code ? `<div class="muted-sub"><code>${escapeHtml(row.stg_code)}</code></div>` : ""}
        ${row.description_family ? `<div class="muted-sub">${escapeHtml(row.description_family)}</div>` : ""}
        ${row.pipeline_stage_label ? `<div class="muted-sub">${escapeHtml(row.pipeline_stage_label)}</div>` : ""}
      </td>
      <td>${renderScoreBadge(row.scorecard || row.score)}</td>
      <td>${qualityBadge(row.source_quality)}</td>
      <td>${badge(row.has_deterministic_rules ? "YES" : "NO", row.has_deterministic_rules ? "ok" : "bad")}</td>
      <td>
        ${badge(row.has_source_url_transcript ? "YES" : "NO", row.has_source_url_transcript ? "ok" : "bad")}
        ${row.source_url ? `<div class="muted-sub">${escapeHtml(row.source_url)}</div>` : ""}
        ${row.transcript_path ? `<div class="muted-sub">${escapeHtml(row.transcript_path)}</div>` : ""}
      </td>
      <td title="${escapeHtml(txReason)}">${txBadge}${txReason ? `<div class="muted-sub">${escapeHtml(txReason)}</div>` : ""}</td>
      <td>${badge(row.eligible_for_backtest ? "YES" : "NO", row.eligible_for_backtest ? "ok" : "bad")}</td>
      <td>${escapeHtml(row.blocked_reason || "—")}</td>
      <td>
        <div><code>${escapeHtml(row.canonical_id || row.id || "--")}</code></div>
        ${row.duplicate_of ? `<div class="muted-sub">duplicate of ${escapeHtml(row.duplicate_of)}</div>` : `<div class="muted-sub">canonical</div>`}
        ${row.duplicate_group_size ? `<div class="muted-sub">group ${escapeHtml(String(row.duplicate_group_size))}</div>` : ""}
      </td>
      <td>${renderActionCell(row.recommended_next_pipeline_step || "—", row.next_action_hint || "")}</td>
    </tr>`;
  }).join("");

  const tbody = $("#auditRows");
  if (!tbody.dataset.bound) {
    tbody.dataset.bound = "1";
    tbody.addEventListener("click", (event) => {
      const tr = event.target.closest("tr[data-audit-id]");
      if (tr) openUnifiedStrategyDetail(tr.dataset.auditId);
    });
  }

  syncUnifiedDetailVisibility();
}

function renderMtcV2Readiness() {
  const readiness = state.snapshot.mtc_v2_readiness || {};
  const rows = (readiness.rows || []).filter((row) => !row.is_source_parent);
  const summary = readiness.summary || {};
  const tracker = readiness.parity_tracker || {};
  $("#mtcV2Intro").textContent = summary.calibration_note || "This is a read-only planning queue for MTC_V2. It shows whether a candidate needs source audit, backtest, promotion pack, PineTS parity, forward evidence, or is ready for MTC_V2 review.";
  populateSelect("#mtcV2StatusFilter", uniqueValues(rows.map((row) => row.status)), "All");
  const filtered = filterMtcV2Rows(rows);
  $("#mtcV2Count").textContent = `${filtered.length}/${rows.length} candidates`;
  $("#mtcV2Summary").innerHTML = [
    ["Ready review", summary.ready_for_review || 0, "High-evidence rows that can enter a read-only MTC_V2 review queue."],
    ["Forward evidence", summary.needs_forward_evidence || 0, "Rows that need forward paper-trade evidence before integration decisions."],
    ["PineTS parity", summary.needs_pinets_parity || 0, "Rows waiting for PineTS/Python parity."],
    ["Promotion pack", summary.needs_promotion_pack || 0, "Rows waiting for a promotion packet."],
    ["Blocked / parked", summary.blocked_or_parked || 0, "Rows blocked by source, split, or low-score review."],
    ["MTC cases", tracker.total_cases || 0, "Rows in the existing MTC_V2 parity tracker."],
    ["MTC passes", tracker.pass_cases || 0, "Existing MTC_V2 tracker cases with PASS verdict."],
    ["Core Pine", readiness.pine_exists ? "OK" : "Missing", "Whether MTC_V2.pine is present; this page does not edit it."]
  ].map(([label, value, title]) => `
    <div class="parity-cell" title="${escapeHtml(title)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(formatNumber(value))}</strong>
    </div>
  `).join("");
  if (!filtered.length) {
    $("#mtcV2Rows").innerHTML = `<tr><td colspan="7" class="empty-cell">No MTC_V2 readiness rows match</td></tr>`;
    return;
  }
  $("#mtcV2Rows").innerHTML = filtered.map((row) => `
    <tr class="row-click" data-mtc-v2-id="${escapeHtml(row.id)}" title="Open strategy detail">
      <td>
        <code>${escapeHtml(row.id || "--")}</code>
        ${row.stg_code ? `<div class="muted-sub"><code>${escapeHtml(row.stg_code)}</code></div>` : ""}
      </td>
      <td>${renderScoreBadge({ total: row.score, label: row.score_label, band: row.score_band, note: "MTC_V2 readiness uses this as one triage input." })}</td>
      <td>${badge(row.status_label || row.status || "--", row.status === "READY_FOR_MTC_V2_REVIEW" ? "ok" : "neutral")}<div class="muted-sub">${escapeHtml(row.decision_sentence || row.reason || "")}</div></td>
      <td>${escapeHtml(row.stage_label || row.stage || "--")}</td>
      <td>${renderForwardProgress(row.forward_progress)}</td>
      <td>${escapeHtml(row.blocker || "--")}</td>
      <td>${renderActionCell(row.next_action || "--", row.next_action_hint || "")}</td>
    </tr>
  `).join("");
  const tbody = $("#mtcV2Rows");
  if (!tbody.dataset.bound) {
    tbody.dataset.bound = "1";
    tbody.addEventListener("click", (event) => {
      const tr = event.target.closest("tr[data-mtc-v2-id]");
      if (tr) openUnifiedStrategyDetail(tr.dataset.mtcV2Id);
    });
  }
}

function hiddenSourceParentIds() {
  const audit = state.snapshot.candidate_audit || {};
  return new Set((audit.rows || []).filter((row) => row.visible_in_strategy_tables === false).map((row) => row.id));
}

function stageCls(s) {
  return { done: "ok", active: "stage-active", pending: "stage-pending", na: "stage-na", fail: "bad" }[s] || "stage-pending";
}
function stageIcon(s) {
  return { done: "✓", active: "●", pending: "–", na: "·", fail: "✗" }[s] || "–";
}
function ytEmbed(url) {
  const m1 = url.match(/[?&]v=([^&]+)/);
  const m2 = url.match(/youtu\.be\/([^?&]+)/);
  const id = (m1 && m1[1]) || (m2 && m2[1]) || "";
  if (!id) return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a>`;
  return `<div class="yt-embed"><iframe src="https://www.youtube.com/embed/${encodeURIComponent(id)}" title="YouTube" frameborder="0" allow="encrypted-media" allowfullscreen></iframe></div>
    <p class="muted-sub"><a href="${escapeHtml(url)}" target="_blank" rel="noopener">Open on YouTube</a></p>`;
}

function openUnifiedStrategyDetail(id) {
  const pipeline = state.snapshot.candidate_pipeline || {};
  const audit = state.snapshot.candidate_audit || {};
  const mtcV2 = state.snapshot.mtc_v2_readiness || {};
  const pipelineRow = (pipeline.rows || []).find((row) => row.id === id) || null;
  const auditRow = (audit.rows || []).find((row) => row.id === id) || null;
  const mtcV2Row = (mtcV2.rows || []).find((row) => row.id === id) || null;
  if (!pipelineRow && !auditRow) return;
  state.selectedStrategyId = id;
  renderUnifiedStrategyDetail(pipelineRow, auditRow, pipeline.stages || [], mtcV2Row);
  syncUnifiedDetailVisibility();
  const backButton = $('#strategyBack');
  if (backButton) backButton.addEventListener('click', closeUnifiedStrategyDetail);
}

function renderUnifiedStrategyDetail(pipelineRow, auditRow, stages, mtcV2Row) {
  const row = pipelineRow || auditRow || {};
  const description = row.description || {};
  const metrics = row.metrics || {};
  const sourceRecord = auditRow && auditRow.source_record ? auditRow.source_record : {};
  const sourceUrl = (auditRow && auditRow.source_url) || row.source_url || sourceRecord.source_url || '';
  const sourceUrlSource = auditRow ? auditRow.source_url_source : '';
  const producerSpecRaw = row.producer_spec || {};
  const title = strategyDisplayName(row, auditRow, producerSpecRaw, sourceRecord);
  const subtitle = strategySubtitle(row, auditRow, sourceUrl);
  const statusLabel = friendlyStatus((mtcV2Row && (mtcV2Row.status_label || mtcV2Row.status)) || (auditRow && auditRow.audit_status) || row.current_stage_label || row.current_stage_key || "Review pending");
  const stgCode = row.stg_code || (auditRow && auditRow.stg_code) || '';
  const scorecard = row.scorecard || (auditRow && auditRow.scorecard) || null;
  const scorecardV2 = row.scorecard_v2 || (auditRow && auditRow.scorecard_v2) || null;
  const paperTrade = renderPaperTradeDetail(row.paper_trade_detail);
  const parityProof = renderParityProof(row.pinets_parity_proof);
  const directionalResearch = renderDirectionalResearch(row.directional_research);
  const producerSpec = renderProducerSpec(row.producer_spec);
  const displayDescription = firstEnglishText(
    row.strategy_description_en,
    description.what,
    description.summary,
    producerSpecRaw.summary,
    sourceRecord.summary
  ) || "No English strategy description is available yet.";
  const quantlens = findQuantlensCandidate(row, auditRow);
  const decision = buildWaveADecision(row, auditRow, mtcV2Row, scorecardV2, quantlens);
  const scoreDetail = renderWaveAScorecard(scorecardV2, scorecard);
  const quantlensVerdict = renderQuantlensVerdict(quantlens);
  const taxonomy = renderStrategyTaxonomy(row, auditRow, producerSpecRaw, description);
  const journey = renderReviewJourney(row, auditRow, stages);
  const tradingRules = renderTradingRules(row, auditRow, producerSpecRaw, description, sourceRecord);
  const backtestEvidence = renderBacktestEvidence(row, auditRow, metrics);
  const salvage = renderSalvageableIdeas(row, auditRow, quantlens);
  const sourceMaterial = renderSourceMaterial(auditRow, row, sourceRecord, sourceUrl, sourceUrlSource);
  const technicalDetails = renderTechnicalDetails({
    row,
    auditRow,
    sourceRecord,
    scorecard,
    producerSpec,
    directionalResearch,
    paperTrade,
    parityProof,
  });
  $('#strategyDetail').innerHTML = `
    <button class="back-btn detail-back" id="strategyBack" type="button">Back to tables</button>
    <div class="strategy-terminal">
      <div class="detail-sticky">
        <strong>${escapeHtml(title)}</strong>
        <span>${escapeHtml(decision.verdict)}</span>
        <span>${escapeHtml(decision.nextAction)}</span>
        <span>${escapeHtml(decision.evidenceLevel)}</span>
      </div>
      <section class="detail-hero">
        <div>
          <p class="detail-kicker">${escapeHtml(stgCode || "Strategy Detail")}</p>
          <h3 class="detail-title">${escapeHtml(title)}</h3>
          <p class="detail-subtitle">${escapeHtml(subtitle)}</p>
          <p class="detail-description">${escapeHtml(displayDescription)}</p>
        </div>
        <div class="detail-status-stack">
          <span class="terminal-badge">${escapeHtml(statusLabel)}</span>
          <span class="terminal-badge muted">${escapeHtml(decision.quantlensLabel)}</span>
        </div>
      </section>
      ${renderVerdictDecision(decision)}
      ${scoreDetail}
      ${quantlensVerdict}
      ${taxonomy}
      ${journey}
      ${tradingRules}
      ${backtestEvidence}
      ${salvage}
      ${sourceMaterial}
      ${technicalDetails}
    </div>
  `;
}

function strategyDisplayName(row, auditRow, producerSpec, sourceRecord) {
  const candidates = [
    row.strategy_display_name,
    row.display_name,
    row.name,
    row.title,
    producerSpec && producerSpec.title,
    row.description && row.description.family,
    auditRow && auditRow.description_family,
    sourceRecord && sourceRecord.title,
  ];
  for (const candidate of candidates) {
    const text = cleanDisplayText(candidate);
    if (text && !looksLikeRawId(text)) {
      return text;
    }
  }
  return humanizeStrategyId(row.id || (auditRow && auditRow.id) || "Unnamed strategy");
}

function strategySubtitle(row, auditRow, sourceUrl) {
  const instrument = marketLabel(row.symbol || (auditRow && auditRow.symbol));
  const timeframe = row.timeframe || (auditRow && auditRow.timeframe) || "";
  const sourceKind = sourceUrl ? (sourceUrl.includes("youtu") ? "YouTube source" : "External source") : "Source not linked";
  return [instrument, timeframe, sourceKind].filter(Boolean).join(" / ") || "Review data not available yet";
}

function cleanDisplayText(value) {
  const text = String(value || "").trim();
  if (!text || text === "--" || text === "—") return "";
  return text;
}

function looksLikeRawId(text) {
  return /^[A-Z]{2,}_\d{4}/.test(text) || /^STG\d+/i.test(text) || (text.includes("_") && !text.includes(" "));
}

function humanizeStrategyId(value) {
  const raw = String(value || "").trim();
  if (!raw) return "Unnamed strategy";
  const stripped = raw
    .replace(/^QL_\d{4}-\d{2}-\d{2}_/i, "")
    .replace(/^STG\d+_?/i, "")
    .replace(/^\d+_/, "");
  const words = stripped.split(/[_\-]+/).filter(Boolean);
  const title = words.map((word) => {
    if (/^(EMA|RSI|VWAP|ADX|ATR|FVG|ORB|SMA)$/i.test(word)) return word.toUpperCase();
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  }).join(" ");
  return title || "Unnamed strategy";
}

function firstEnglishText(...values) {
  for (const value of values) {
    const text = cleanDisplayText(value);
    if (text && isLikelyEnglish(text)) {
      return text;
    }
  }
  return "";
}

function isLikelyEnglish(text) {
  return !/[çğıöşüÇĞİÖŞÜ]/.test(text);
}

function marketLabel(symbol) {
  const text = String(symbol || "").trim().toUpperCase();
  if (!text) return "Market not defined";
  if (text.endsWith("USDT") || text.endsWith("USD")) return `Crypto ${text}`;
  return text;
}

function friendlyStatus(value) {
  const key = String(value || "").trim();
  const map = {
    CANONICAL: "Primary version",
    LOW_SCORE_REVIEW: "Needs review",
    BLOCKED_SOURCE_AUDIT: "Source check needed",
    READY_FOR_MTC_V2_REVIEW: "Ready for review",
    CLOSED_SOURCE_STOP: "Closed-source / paid indicator detected - analysis stopped",
    OVERFIT_SUSPECT: "Overfit risk",
    NEEDS_BACKTEST: "Needs backtest evidence",
    NEEDS_PROMOTION_PACK: "Needs promotion packet",
    NEEDS_PINETS_PARITY: "Needs PineTS parity",
    NEEDS_FORWARD_EVIDENCE: "Needs forward evidence",
    PARKED_OR_SPLIT: "Parked or split required",
  };
  return map[key] || statusText(key || "Review pending");
}

const QUANTLENS_STOP_LABELS = {
  CLOSED_SOURCE_STOP: "Closed-source / paid indicator — analysis stopped",
  COMPLEXITY_OVERLOAD: "Too complex — simplification required",
  GARBAGE: "Garbage — no viable strategy, salvage ideas only",
};

function findQuantlensCandidate(row, auditRow) {
  const ql = state.snapshot.quantlens || {};
  const candidates = Array.isArray(ql.candidates) ? ql.candidates : [];
  if (!candidates.length) return null;
  const keys = [row && row.id, row && row.candidate_id, auditRow && auditRow.id, auditRow && auditRow.candidate_id]
    .filter(Boolean)
    .map(String);
  if (!keys.length) return null;
  return candidates.find((c) => keys.includes(String(c.candidate_id))) || null;
}

function renderQuantlensVerdict(quantlens) {
  if (!quantlens) {
    return `
    <section class="terminal-section quantlens-section">
      <div class="terminal-section-head"><h4>QuantLens Verdict</h4>
        <span class="terminal-badge muted">Not in QuantLens</span></div>
      <p class="muted-terminal">This strategy is not part of the QuantLens salvage analysis. The QuantLens verdict is commentary only and never produces a gate score.</p>
    </section>`;
  }
  const v = quantlens.quantlens_verdict || {};
  const cv = v.commercial_value || {};
  const cx = v.complexity || {};
  const risks = v.risks || {};
  const stop = quantlens.stop_state;
  const stopBanner = stop
    ? `<p class="quantlens-stop"><strong>${escapeHtml(QUANTLENS_STOP_LABELS[stop] || statusText(stop))}</strong></p>`
    : "";
  const riskChips = [
    ["Repaint", risks.repaint],
    ["Lookahead", risks.lookahead],
    ["Overfit", risks.overfit],
    ["Closed-source", risks.closed_source],
    ["Risk mgmt", risks.risk_management_quality],
  ]
    .filter(([, val]) => val)
    .map(([k, val]) => `<span class="terminal-chip">${escapeHtml(k)}: ${escapeHtml(friendlyStatus(String(val)))}</span>`)
    .join("");
  const facts = [
    ["Commercial value", cv.score == null ? cv.band || "Unknown" : `${cv.band} (${cv.score}/10)`],
    ["Complexity", cx.score == null ? "Unknown" : `${cx.score}/10${cx.overload ? " — overload" : ""}`],
    ["Testability", v.testability || "Unknown"],
    ["Instrument fit", v.instrument_fit || "UNKNOWN"],
  ];
  return `
    <section class="terminal-section quantlens-section">
      <div class="terminal-section-head"><h4>QuantLens Verdict</h4>
        <span class="terminal-badge ${stop ? "warn" : "muted"}">${escapeHtml(v.decision_label || quantlens.quantlens_decision || "Reviewed")}</span></div>
      ${stopBanner}
      <p class="muted-terminal">QuantLens is a ruthless audit layer — commentary and labels only. It references the Scorecard above; it never adds its own gate score.</p>
      <div class="terminal-facts">
        ${facts.map(([k, val]) => `<div><span>${escapeHtml(k)}</span><strong>${escapeHtml(String(val))}</strong></div>`).join("")}
      </div>
      ${riskChips ? `<div class="chip-row">${riskChips}</div>` : ""}
      ${v.recommended_next_step ? `<p class="score-reference">Recommended next step: ${escapeHtml(v.recommended_next_step)}</p>` : ""}
    </section>`;
}

function buildWaveADecision(row, auditRow, mtcV2Row, scorecardV2, quantlens) {
  const hasAudit = Boolean(auditRow);
  const eligible = hasAudit ? Boolean(auditRow.eligible_for_backtest) : false;
  const deterministic = hasAudit ? Boolean(auditRow.has_deterministic_rules) : Boolean(row.producer_spec);
  const blocker = cleanDisplayText((mtcV2Row && mtcV2Row.blocker) || (auditRow && auditRow.blocked_reason))
    || (eligible ? "None" : "Deterministic rules are not complete.");
  const nextAction = cleanDisplayText((mtcV2Row && mtcV2Row.next_action) || row.next_action || (auditRow && auditRow.recommended_next_pipeline_step))
    || "Review the source evidence.";
  const evidenceLevel = evidenceLevelLabel(row, auditRow);
  const verdict = eligible
    ? "Ready for backtest review"
    : deterministic
      ? "Partially testable"
      : "Needs source clarification";
  const reason = eligible
    ? "Existing data says the candidate has enough deterministic rule evidence to enter a backtest workflow."
    : deterministic
      ? "Some rules are documented, but at least one upstream requirement is still blocking clean evidence."
      : "The source does not define enough exact mechanical rules for honest scoring or backtesting.";
  const riskFlags = [
    !deterministic ? "Undefined rules" : "",
    blocker && blocker !== "None" ? friendlyStatus(blocker) : "",
    hasAudit && !auditRow.has_source_url_transcript ? "Source material incomplete" : "",
    "Repaint status unknown",
  ].filter(Boolean);
  return {
    verdict,
    reason,
    canTest: eligible ? "Yes" : "No",
    blocker,
    nextAction: statusText(nextAction),
    riskFlags,
    evidenceLevel,
    documentedVsProven: evidenceLevel.includes("Backtested") ? "Documented and internally tested" : "Documented, not proven",
    quantlensLabel: quantlens
      ? `QuantLens: ${(quantlens.quantlens_verdict && quantlens.quantlens_verdict.decision_label) || quantlens.quantlens_decision || "Reviewed"}`
      : "QuantLens: Not evaluated yet",
    scoreReference: scorecardV2
      ? "Gate scorecard is available below."
      : "Gate scorecard is not evaluated yet. The new gate-based scorecard will be available after SP-004 implementation.",
  };
}

function evidenceLevelLabel(row, auditRow) {
  const stage = String(row.current_stage_key || (auditRow && auditRow.current_stage_key) || "").toLowerCase();
  if (stage === "integrated") return "Production candidate";
  if (stage === "paper_trade") return "Paper-trade observed";
  if (["backtested", "promoted", "pre_parity"].includes(stage)) return "Backtested internally";
  if (auditRow && auditRow.has_deterministic_rules) return "Rules extracted";
  return "Source only";
}

function renderVerdictDecision(decision) {
  return `
    <section class="terminal-section verdict-section">
      <div class="terminal-section-head">
        <h4>Verdict & Decision</h4>
        <span class="terminal-badge amber">${escapeHtml(decision.canTest === "Yes" ? "Can test" : "Blocked")}</span>
      </div>
      <p class="verdict-line"><strong>${escapeHtml(decision.verdict)}</strong></p>
      <p>${escapeHtml(decision.reason)}</p>
      <div class="terminal-facts">
        <div><span>Can it be tested?</span><strong>${escapeHtml(decision.canTest)}</strong></div>
        <div><span>Blocking item</span><strong>${escapeHtml(decision.blocker)}</strong></div>
        <div><span>Next required action</span><strong>${escapeHtml(decision.nextAction)}</strong></div>
        <div><span>Evidence level</span><strong>${escapeHtml(decision.evidenceLevel)}</strong></div>
      </div>
      <div class="chip-row">
        ${decision.riskFlags.map((flag) => `<span class="terminal-chip warn">${escapeHtml(flag)}</span>`).join("")}
        <span class="terminal-chip">${escapeHtml(decision.documentedVsProven)}</span>
      </div>
      <p class="score-reference">${escapeHtml(decision.scoreReference)}</p>
    </section>
  `;
}

function renderWaveAScorecard(scorecardV2, legacyScorecard) {
  if (scorecardV2) {
    const gates = Array.isArray(scorecardV2.gates) ? scorecardV2.gates : [];
    return `
      <section class="terminal-section scorecard-v2-section">
        <div class="terminal-section-head">
          <h4>Scorecard</h4>
          <span class="terminal-badge ok">Gate based</span>
        </div>
        ${gates.length ? gates.map(renderGateRow).join("") : `<p class="muted-terminal">Gate scorecard data is present but no gate rows were provided.</p>`}
      </section>
    `;
  }
  return `
    <section class="terminal-section scorecard-v2-section">
      <div class="terminal-section-head">
        <h4>Scorecard</h4>
        <span class="terminal-badge muted">SP-004 pending</span>
      </div>
      <p><strong>Gate scorecard is not evaluated yet.</strong></p>
      <p class="muted-terminal">The new gate-based scorecard will be available after SP-004 implementation. This page does not create scorecard_v2 math or invent gate scores.</p>
      ${legacyScorecard ? `<p class="muted-terminal">Legacy composite score is kept only in Technical Details for rollback and audit context.</p>` : ""}
    </section>
  `;
}

function renderGateRow(gate) {
  const score = gate.score == null ? "N/A" : `${gate.score}/${gate.max || 100}`;
  const label = gate.label || gate.name || gate.key || "Gate";
  const status = gate.status || "NOT_EVALUATED";
  return `
    <details class="gate-row">
      <summary><span>${escapeHtml(label)}</span><strong>${escapeHtml(score)}</strong><em>${escapeHtml(statusText(status))}</em></summary>
      <p>${escapeHtml(gate.reason || gate.note || "No sub-criteria detail available yet.")}</p>
    </details>
  `;
}

function renderStrategyTaxonomy(row, auditRow, producerSpec, description) {
  const familyBlob = [row.id, description.family, producerSpec.title].join(" ");
  const chips = [
    ["Category / time horizon", inferTimeHorizon(row.timeframe || (auditRow && auditRow.timeframe), familyBlob)],
    ["Expected market condition", inferMarketCondition(familyBlob)],
    ["Method", inferMethod(familyBlob)],
    ["Instrument / market fit", marketLabel(row.symbol || (auditRow && auditRow.symbol))],
    ["Automation suitability", auditRow && auditRow.has_deterministic_rules ? "Machine-testable" : "Partially defined"],
    ["Complexity", "Not defined yet"],
  ];
  return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Strategy Taxonomy</h4></div>
      <div class="taxonomy-grid">
        ${chips.map(([label, value]) => `
          <div class="taxonomy-chip">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value || "Unknown")}</strong>
          </div>
        `).join("")}
      </div>
    </section>
  `;
}

function inferTimeHorizon(timeframe, blob) {
  const tf = String(timeframe || "").toLowerCase();
  const text = String(blob || "").toLowerCase();
  if (tf.includes("5m") || tf.includes("10m") || tf.includes("15m") || text.includes("scalp")) return "Scalping / intraday";
  if (tf.includes("1h") || tf.includes("2h") || tf.includes("4h")) return "Day trading / swing";
  if (tf.includes("1d") || tf.includes("daily")) return "Swing / position";
  return "Unknown";
}

function inferMarketCondition(blob) {
  const text = String(blob || "").toLowerCase();
  if (text.includes("breakout") || text.includes("flag")) return "Breakout / trend continuation";
  if (text.includes("vwap") || text.includes("rsi") || text.includes("pullback")) return "Pullback / mean reversion";
  if (text.includes("bollinger")) return "Volatility expansion";
  return "Unknown";
}

function inferMethod(blob) {
  const text = String(blob || "").toLowerCase();
  if (text.includes("vwap")) return "VWAP reaction";
  if (text.includes("rsi")) return "Momentum oscillator";
  if (text.includes("ema")) return "Moving-average trend filter";
  if (text.includes("breakout")) return "Breakout";
  if (text.includes("bollinger")) return "Volatility breakout";
  return "Unknown";
}

function renderReviewJourney(row, auditRow, stages) {
  const base = [
    ["Discovered", "done", "Source row exists in the dashboard snapshot."],
    ["Source checked", auditRow && auditRow.has_source_url_transcript ? "done" : "active", auditRow && auditRow.has_source_url_transcript ? "Source or transcript linked." : "Source material is incomplete."],
    ["Rules extracted", auditRow && auditRow.has_deterministic_rules ? "done" : "active", auditRow && auditRow.has_deterministic_rules ? "Deterministic rules detected." : "Exact rules are still missing."],
    ["Testability confirmed", auditRow && auditRow.eligible_for_backtest ? "done" : "pending", auditRow && auditRow.eligible_for_backtest ? "Eligible for backtest." : "Blocked before backtest."],
  ];
  const stageMap = row.stages || {};
  const late = [
    ["Backtested", stageMap.backtested && stageMap.backtested.status === "done" ? "done" : "pending", stageMap.backtested && stageMap.backtested.metric || "Backtest evidence not available yet."],
    ["Promotion review", stageMap.promoted && stageMap.promoted.status === "done" ? "done" : "pending", stageMap.promoted && stageMap.promoted.metric || "Promotion packet not ready."],
    ["Paper-trade candidate", stageMap.paper_trade && stageMap.paper_trade.status === "done" ? "done" : "pending", stageMap.paper_trade && stageMap.paper_trade.metric || "Forward evidence not collected."],
    ["Integrated", stageMap.integrated && stageMap.integrated.status === "done" ? "done" : "pending", stageMap.integrated && stageMap.integrated.metric || "Not integrated."],
  ];
  return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Review Journey</h4></div>
      <ol class="journey-list">
        ${base.concat(late).map(([label, status, note]) => `
          <li class="journey-${escapeHtml(status)}">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(statusText(status))}</strong>
            <em>${escapeHtml(note)}</em>
          </li>
        `).join("")}
      </ol>
    </section>
  `;
}

function renderTradingRules(row, auditRow, producerSpec, description, sourceRecord) {
  const rows = [
    ["Market / bias", row.symbol ? marketLabel(row.symbol) : "Not defined yet"],
    ["Expected market condition", inferMarketCondition([row.id, description.family, producerSpec.title].join(" ")) || "Unknown"],
    ["Strategy method", inferMethod([row.id, description.family, producerSpec.title].join(" ")) || "Unknown"],
    ["Entry trigger", firstEnglishText(description.entry, producerSpec.entry_pseudo, sourceRecord.rules_text) || "Not defined yet"],
    ["Entry filters", listOrMissing(producerSpec.rules_high_confidence)],
    ["Exit logic", firstEnglishText(description.exit, producerSpec.exit_pseudo) || "Not defined yet"],
    ["Stop-loss rule", firstEnglishText(producerSpec.stop_loss, producerSpec.stop_loss_rule) || "Not defined yet"],
    ["Take-profit rule", firstEnglishText(producerSpec.take_profit, producerSpec.take_profit_rule) || "Not defined yet"],
    ["Trailing stop", firstEnglishText(producerSpec.trailing_stop, producerSpec.trailing_stop_rule) || "Not defined yet"],
    ["Breakeven logic", firstEnglishText(producerSpec.breakeven, producerSpec.breakeven_rule) || "Not defined yet"],
    ["Risk management", firstEnglishText(producerSpec.risk_management) || "Not defined yet"],
    ["Avoid trading when", firstEnglishText(producerSpec.avoid_trading_when) || "Not defined yet"],
    ["Repaint/lookahead notes", "Not evaluated yet"],
    ["Assumptions", firstEnglishText(row.notes, producerSpec.assumptions) || "Not defined yet"],
  ];
  return `
    <section class="terminal-section">
      <div class="terminal-section-head">
        <h4>Trading Rules</h4>
        <span class="terminal-badge muted">Missing fields visible</span>
      </div>
      <table class="terminal-kv">${rows.map(([key, value]) => `
        <tr class="${value === "Not defined yet" || value === "Not evaluated yet" ? "missing-row" : ""}">
          <td>${escapeHtml(key)}</td>
          <td>${escapeHtml(String(value))}</td>
        </tr>
      `).join("")}</table>
    </section>
  `;
}

function listOrMissing(value) {
  if (Array.isArray(value) && value.length) return value.filter(Boolean).join(" | ");
  return "Not defined yet";
}

function renderBacktestEvidence(row, auditRow, metrics) {
  const metricRows = [
    ["Net profit", metrics.return_pct_compound != null ? `${Number(metrics.return_pct_compound).toFixed(2)}%` : ""],
    ["Profit factor", metrics.profit_factor],
    ["Total trades", metrics.trades],
    ["Max drawdown", metrics.max_drawdown_pct != null ? `${Number(metrics.max_drawdown_pct).toFixed(1)}%` : ""],
    ["Win rate", metrics.win_rate != null ? `${(Number(metrics.win_rate) * 100).toFixed(1)}%` : ""],
    ["Direction", metrics.direction],
  ].filter(([, value]) => value !== null && value !== undefined && value !== "");
  const hasEvidence = metricRows.length > 0 || (row.equity_curve || []).length > 1;
  if (hasEvidence) {
    return `
      <section class="terminal-section">
        <div class="terminal-section-head">
          <h4>Backtest Evidence</h4>
          <span class="terminal-badge amber">Existing evidence</span>
        </div>
        <p class="muted-terminal">These are existing raw metrics only. They are not a SP-004 Gate 2 score.</p>
        ${metricRows.length ? `<table class="terminal-kv">${metricRows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td>${escapeHtml(String(value))}</td></tr>`).join("")}</table>` : ""}
        ${renderSparkline(row.equity_curve || [])}
      </section>
    `;
  }
  const reason = auditRow && auditRow.blocked_reason ? `Blocked upstream: ${auditRow.blocked_reason}.` : "Blocked upstream: deterministic rules are not complete.";
  const checklist = ["Exact entry rule", "Exact exit rule", "Stop-loss rule", "Take-profit rule", "Repaint/lookahead verification", "Test market, symbol, timeframe, date window"];
  return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Backtest Evidence</h4></div>
      <p><strong>Backtest evidence is not available yet.</strong></p>
      <p class="muted-terminal">${escapeHtml(reason)}</p>
      <ul class="checklist">${checklist.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </section>
  `;
}

function renderSalvageableIdeas(row, auditRow, quantlens) {
  const ideas = quantlens && Array.isArray(quantlens.salvageable_ideas) ? quantlens.salvageable_ideas : [];
  if (!quantlens) {
    return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Salvageable Ideas</h4></div>
      <p><strong>QuantLens analysis not available for this strategy.</strong></p>
      <p class="muted-terminal">No structured salvageable idea exists because this strategy is not in the QuantLens salvage queue.</p>
    </section>`;
  }
  if (!ideas.length) {
    return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Salvageable Ideas</h4></div>
      <p class="muted-terminal">QuantLens reviewed this candidate but flagged no reusable component idea.</p>
    </section>`;
  }
  return `
    <section class="terminal-section">
      <div class="terminal-section-head"><h4>Salvageable Ideas</h4>
        <span class="terminal-badge ok">${ideas.length} component${ideas.length === 1 ? "" : "s"}</span></div>
      <p class="muted-terminal">Reusable independent components QuantLens identified from <code>candidate_kind</code> (the full strategy is not adopted).</p>
      <div class="chip-row">
        ${ideas.map((i) => `<span class="terminal-chip">${escapeHtml(i.label || i.category)}</span>`).join("")}
      </div>
    </section>`;
}

function renderSourceMaterial(auditRow, row, sourceRecord, sourceUrl, sourceUrlSource) {
  const rows = [
    ["Source title", cleanDisplayText(sourceRecord.title) || cleanDisplayText(row.name) || "Not defined yet"],
    ["Source type", sourceUrl && sourceUrl.includes("youtu") ? "YouTube" : sourceUrl ? "External link" : "Not defined yet"],
    ["Source link", sourceUrl || "Not defined yet"],
    ["Transcript status", auditRow && auditRow.has_transcript ? "Transcript linked" : "Transcript not available"],
    ["Source quality", auditRow && auditRow.source_quality ? friendlyStatus(auditRow.source_quality) : "Unknown"],
    ["Source URL source", sourceUrlSource || "Not defined yet"],
  ];
  return `
    <section class="terminal-section source-section">
      <div class="terminal-section-head"><h4>Source Material</h4></div>
      <table class="terminal-kv">${rows.map(([key, value]) => `
        <tr><td>${escapeHtml(key)}</td><td>${sourceUrl && key === "Source link" ? `<a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener">${escapeHtml(sourceUrl)}</a>` : escapeHtml(String(value))}</td></tr>
      `).join("")}</table>
    </section>
  `;
}

function renderTechnicalDetails({ row, auditRow, sourceRecord, scorecard, producerSpec, directionalResearch, paperTrade, parityProof }) {
  const rawRows = [
    ["Internal strategy ID", row.id || (auditRow && auditRow.id) || "--"],
    ["Raw stage", row.current_stage_key || (auditRow && auditRow.current_stage_key) || "--"],
    ["Raw audit status", auditRow && auditRow.audit_status || "--"],
    ["Canonical ID", auditRow && auditRow.canonical_id || "--"],
    ["Duplicate of", auditRow && auditRow.duplicate_of || "canonical"],
    ["Transcript path", auditRow && auditRow.transcript_path || "--"],
    ["Source file", sourceRecord && (sourceRecord.source_file || sourceRecord.relative_source_path) || "--"],
  ];
  return `
    <details class="terminal-section technical-details">
      <summary>Technical Details</summary>
      <table class="terminal-kv">${rawRows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td>${escapeHtml(String(value))}</td></tr>`).join("")}</table>
      ${scorecard ? `<h5>Legacy Composite Score</h5>${renderLegacyScorecard(scorecard)}` : ""}
      ${producerSpec ? `<h5>Producer Spec</h5>${producerSpec}` : ""}
      <h5>Directional Research</h5>${directionalResearch}
      <h5>Paper-trade</h5>${paperTrade}
      <h5>PineTS Parity Proof</h5>${parityProof}
      <h5>Raw Source Record</h5>
      <pre><code>${escapeHtml(JSON.stringify(sourceRecord || {}, null, 2))}</code></pre>
    </details>
  `;
}

function renderLegacyScorecard(scorecard) {
  if (!scorecard) return "";
  const rows = (scorecard.components || []).map((component) => `
    <tr>
      <td>${escapeHtml(component.label)}</td>
      <td><strong>${escapeHtml(String(component.score ?? 0))}/${escapeHtml(String(component.max ?? 0))}</strong></td>
      <td>${escapeHtml(component.note || "--")}</td>
    </tr>
  `).join("");
  return `
    <div class="detail-card scorecard-card legacy-scorecard">
      <div class="scorecard-head">
        <p><strong>Legacy composite score: ${escapeHtml(scorecard.label || `${scorecard.total || 0}/100`)}</strong></p>
        <span class="badge ${scoreBand(scorecard.total)}">${escapeHtml((scorecard.band || scoreBand(scorecard.total)).toUpperCase())}</span>
      </div>
      <p class="muted-sub">${escapeHtml(scorecard.note || "Deprecated heuristic composite score; not the new gate scorecard.")}</p>
      <table class="kv scorecard-table">${rows}</table>
    </div>
  `;
}

function renderDecisionPanel(row, auditRow, mtcV2Row, scorecard) {
  const scoreLabel = scorecard ? (scorecard.label || `${scorecard.total || 0}/100`) : "--";
  const auditStatus = auditRow ? (auditRow.audit_status || "--") : "No audit row";
  const blocker = (mtcV2Row && mtcV2Row.blocker) || (auditRow && auditRow.blocked_reason) || "None";
  const readiness = mtcV2Row ? (mtcV2Row.status_label || mtcV2Row.status) : "Not in MTC_V2 queue";
  const nextAction = (mtcV2Row && mtcV2Row.next_action) || row.next_action || (auditRow && auditRow.recommended_next_pipeline_step) || "Review";
  const decision = mtcV2Row && mtcV2Row.decision_sentence ? mtcV2Row.decision_sentence : (blocker === "None" ? nextAction : blocker);
  return `
    <div class="decision-panel" title="Decision snapshot for this strategy.">
      <div class="decision-item">
        <span>Status</span>
        <strong>${escapeHtml(auditStatus)}</strong>
      </div>
      <div class="decision-item">
        <span>Score</span>
        <strong>${escapeHtml(scoreLabel)}</strong>
      </div>
      <div class="decision-item">
        <span>MTC_V2</span>
        <strong>${escapeHtml(readiness)}</strong>
      </div>
      <div class="decision-item">
        <span>Blocker / next</span>
        <strong>${escapeHtml(decision)}</strong>
      </div>
    </div>
  `;
}

function renderForwardProgress(progress) {
  if (!progress) {
    return `<span class="muted-sub">No forward plan</span>`;
  }
  const target = progress.target_trades;
  const actual = progress.actual_trades || 0;
  const label = progress.label || (target ? `${actual}/${target} trades` : `${actual} forward trades`);
  const pct = Number(progress.progress_pct || 0);
  const cls = target && actual >= target ? "ok" : target ? "neutral" : "stage-pending";
  return `
    ${badge(label, cls)}
    <div class="muted-sub">${escapeHtml(progress.status || "WAITING")}${target ? ` · ${escapeHtml(String(pct))}%` : ""}</div>
  `;
}

function renderDirectionalResearch(detail) {
  if (!detail) {
    return `<p class="muted-sub">Direction research not available.</p>`;
  }
  const rows = [
    ["Current direction", detail.current_direction],
    ["Status", detail.status],
    ["Short action", detail.next_action]
  ].filter(([, value]) => value);
  return `
    <div class="detail-card">
      <table class="kv">${rows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join("")}</table>
      ${detail.long_signal_definition ? `<p class="muted-sub"><strong>Long rule:</strong> ${escapeHtml(detail.long_signal_definition)}</p>` : ""}
      ${detail.short_signal_definition ? `<p class="muted-sub"><strong>Short rule:</strong> ${escapeHtml(detail.short_signal_definition)}</p>` : ""}
      ${detail.suggested_short_research_rule ? `<p class="research-note">${escapeHtml(detail.suggested_short_research_rule)}</p>` : ""}
      ${detail.warning ? `<p class="muted-sub">${escapeHtml(detail.warning)}</p>` : ""}
    </div>
  `;
}

function renderProducerSpec(detail) {
  if (!detail) {
    return null;
  }
  const rows = [
    ["Title", detail.title],
    ["Kind", detail.kind],
    ["Source URL", detail.source_url],
    ["Source candidate", detail.source_candidate],
    ["Param grid", detail.param_grid_size_planned],
    ["Promoted at", detail.promoted_at],
    ["Next action", detail.next_action],
  ].filter(([, value]) => value !== null && value !== undefined && value !== "");
  return `
    <div class="detail-card">
      <table class="kv">${rows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join("")}</table>
      ${detail.summary ? `<p class="muted-sub">${escapeHtml(detail.summary)}</p>` : ""}
      ${detail.rules_high_confidence && detail.rules_high_confidence.length ? `<p class="muted-sub"><strong>High-confidence rules:</strong> ${escapeHtml(detail.rules_high_confidence.join(" | "))}</p>` : ""}
      ${detail.entry_pseudo ? `<p class="muted-sub"><strong>Entry pseudo:</strong> ${escapeHtml(detail.entry_pseudo)}</p>` : ""}
      ${detail.exit_pseudo ? `<p class="muted-sub"><strong>Exit pseudo:</strong> ${escapeHtml(detail.exit_pseudo)}</p>` : ""}
      ${detail.fidelity_to_original_youtube_source ? `<p class="muted-sub"><strong>Fidelity:</strong> ${escapeHtml(String(detail.fidelity_to_original_youtube_source))}</p>` : ""}
      ${detail.path ? `<p class="muted-sub"><code>${escapeHtml(detail.relative_path || detail.path)}</code></p>` : ""}
    </div>
  `;
}

function renderSparkline(points) {
  const values = (points || []).map(Number).filter((value) => Number.isFinite(value));
  if (values.length < 2) {
    return `<p class="muted-sub">No trade equity series yet.</p>`;
  }
  const width = 320;
  const height = 86;
  const pad = 8;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const step = (width - pad * 2) / Math.max(values.length - 1, 1);
  const d = values.map((value, index) => {
    const x = pad + index * step;
    const y = height - pad - ((value - min) / span) * (height - pad * 2);
    return `${index === 0 ? "M" : "L"}${x.toFixed(2)} ${y.toFixed(2)}`;
  }).join(" ");
  const start = values[0];
  const end = values[values.length - 1];
  const cls = end >= start ? "spark-up" : "spark-down";
  return `
    <div class="sparkline ${cls}">
      <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Equity curve">
        <path d="${d}"></path>
      </svg>
      <div class="spark-meta">
        <span>${escapeHtml(start.toFixed(2))}</span>
        <strong>${escapeHtml(end.toFixed(2))}</strong>
      </div>
    </div>
  `;
}

function renderPaperTradeDetail(detail) {
  if (!detail) {
    return `<p class="muted-sub">No paper-trade plan yet.</p>`;
  }
  const results = detail.forward_results || null;
  const metricRows = results ? Object.entries(results.metrics || {}).filter(([, value]) => value !== null && value !== undefined && value !== "") : [];
  const planLines = (detail.plan_summary || []).map((line) => `<li>${escapeHtml(line)}</li>`).join("");
  return `
    <div class="detail-card">
      <p>${badge(detail.status || "--")}</p>
      ${detail.plan_title ? `<p><strong>${escapeHtml(detail.plan_title)}</strong></p>` : ""}
      ${detail.plan_path ? `<p class="muted-sub"><code>${escapeHtml(detail.plan_path)}</code></p>` : ""}
      ${planLines ? `<ul class="compact-list">${planLines}</ul>` : ""}
      ${results ? `
        <p class="muted-sub">Forward results: <code>${escapeHtml(results.file || results.path || "")}</code></p>
        ${metricRows.length ? `<table class="kv">${metricRows.map(([key, value]) => `<tr><td>${escapeHtml(statusText(key))}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join("")}</table>` : `<p class="muted-sub">Results file found, no standard metrics detected.</p>`}
      ` : `<p class="muted-sub">${escapeHtml(detail.forward_status || "WAITING_FOR_FORWARD_RESULTS")}</p>`}
    </div>
  `;
}

function renderParityProof(proof) {
  if (!proof) {
    return `<p class="muted-sub">No PineTS parity result yet.</p>`;
  }
  const rows = Object.entries(proof.summary || {}).filter(([, value]) => value !== null && value !== undefined && value !== "");
  return `
    <div class="detail-card parity-proof">
      <p>${badge(proof.status || "--")}</p>
      ${proof.relative_path ? `<p class="muted-sub"><code>${escapeHtml(proof.relative_path)}</code></p>` : ""}
      ${rows.length ? `<table class="kv">${rows.map(([key, value]) => `<tr><td>${escapeHtml(statusText(key))}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join("")}</table>` : ""}
      <pre><code>${escapeHtml(JSON.stringify(proof.raw || {}, null, 2))}</code></pre>
    </div>
  `;
}

function closeUnifiedStrategyDetail() {
  state.selectedStrategyId = null;
  syncUnifiedDetailVisibility();
}

function syncUnifiedDetailVisibility() {
  const detailOpen = Boolean(state.selectedStrategyId);
  $("#strategyDetail").hidden = !detailOpen;
  $("#pipelineIntro").hidden = detailOpen;
  $("#pipelineSummary").hidden = detailOpen;
  $("#pipelineTableWrap").hidden = detailOpen;
  $("#auditIntro").hidden = detailOpen;
  $("#auditSummary").hidden = detailOpen;
  $("#auditRows").closest(".table-wrap").hidden = detailOpen;
  $("#pipelineDetail").hidden = true;
  $("#auditDetail").hidden = true;
}
function stageCell(cell) {
  const status = cell.status || "pending";
  const metric = cell.metric || "";
  const clsMap = { done: "ok", active: "stage-active", pending: "stage-pending", na: "stage-na", fail: "bad" };
  const iconMap = { done: "✓", active: "●", pending: "–", na: "·", fail: "✗" };
  const cls = clsMap[status] || "stage-pending";
  const icon = iconMap[status] || "–";
  return `<td><span class="badge ${cls}">${icon}</span>${metric ? `<div class="muted-sub">${escapeHtml(metric)}</div>` : ""}</td>`;
}

function renderHeader() {
  const status = state.snapshot.current_status || {};
  const healthOk = Boolean(state.health.overall_ok);
  $("#phaseTitle").textContent = status.phase || "MVP-1 Read-only";
  $("#modeLabel").textContent = state.snapshot.mode || "read_only";
  $("#healthPill").textContent = healthOk ? "healthy" : "attention";
  $("#healthPill").className = `status-pill ${healthOk ? "ok" : "bad"}`;
}

function renderHome() {
  const status = state.snapshot.current_status || {};
  const tasks = state.snapshot.task_queue?.tasks || [];
  const reports = state.snapshot.report_manifest?.reports || [];
  const paritySummary = state.snapshot.parity_status?.summary || {};
  const backtestSummary = state.snapshot.backtest_status?.summary || {};
  const pineSummary = state.snapshot.pine_builder_status?.summary || {};
  const optimizationSummary = state.snapshot.optimization_status?.summary || {};
  const liveopsSummary = state.snapshot.liveops_status?.summary || {};
  const mtcV2Summary = state.snapshot.mtc_v2_readiness?.summary || {};
  const registry = state.snapshot.strategy_registry || {};
  const strategyEntries = registryEntries(registry);
  const lifecycleSummary = state.snapshot.task_lifecycle?.summary || {};

  $("#healthValue").textContent = state.health.overall_ok ? "OK" : "Check";
  $("#taskValue").textContent = String(tasks.length);
  $("#waitingValue").textContent = String(lifecycleSummary.waiting_for_user ?? 0);
  $("#staleValue").textContent = String(lifecycleSummary.stale_candidates ?? 0);
  $("#parityValue").textContent = String(paritySummary.total_cases ?? 0);
  $("#backtestValue").textContent = String(backtestSummary.total_runs ?? 0);
  $("#strategyValue").textContent = String(strategyEntries.length);
  $("#pineDraftValue").textContent = String(pineSummary.total_drafts ?? 0);
  $("#optimizationValue").textContent = String(optimizationSummary.total_runs ?? 0);
  $("#mtcV2Value").textContent = String(mtcV2Summary.ready_for_review ?? 0);
  $("#liveopsValue").textContent = liveopsSummary.all_safety_gates_ok ? "Safe" : "Check";
  $("#reportValue").textContent = String(reports.length);
  $("#updatedAt").textContent = status.last_updated || "--";
  $("#summaryText").textContent = status.summary || "--";

  const checks = state.health.checks || {};
  $("#statusRail").innerHTML = Object.entries(checks)
    .map(([key, value]) => {
      const ok = Boolean(value);
      return `
        <div class="rail-cell ${ok ? "ok" : "bad"}">
          <strong>${escapeHtml(labelize(key))}</strong>
          <span>${ok ? "OK" : "Check"}</span>
        </div>
      `;
    })
    .join("");
}

function researchValue(value) {
  if (value === "review_needed") return `<span class="muted-sub">review_needed</span>`;
  if (Array.isArray(value)) {
    if (!value.length || (value.length === 1 && value[0] === "review_needed")) {
      return `<span class="muted-sub">review_needed</span>`;
    }
    return value.map((v) => escapeHtml(String(v))).join(", ");
  }
  if (value === null || value === undefined || value === "") return "--";
  return escapeHtml(String(value));
}

function researchBool(value) {
  if (value === true) return "✓";
  if (value === false) return "·";
  return `<span class="muted-sub">?</span>`;
}

function renderResearchLab() {
  const research = state.snapshot.strategy_research || {};
  const overview = research.overview || {};
  const strategies = research.strategies || [];
  const indicators = research.indicators || [];
  const components = research.components || [];
  const runs = research.research_runs || [];
  const variants = research.variants || [];
  const backtests = research.backtest_results || [];
  const missing = research.missing_metadata || [];
  const docs = research.workflow_docs || {};

  $("#researchStrategyValue").textContent = String(overview.total_strategies ?? 0);
  $("#researchIndicatorValue").textContent = String(overview.total_indicators ?? 0);
  $("#researchComponentValue").textContent = String(overview.total_components ?? 0);
  $("#researchTagValue").textContent = String(overview.total_tags ?? 0);
  $("#researchRunValue").textContent = String(overview.total_research_runs ?? 0);
  $("#researchVariantValue").textContent = String(overview.total_variants ?? 0);
  $("#researchCandidateValue").textContent = String(overview.final_candidate_strategies ?? 0);
  $("#researchRejectedValue").textContent = String(overview.rejected_variants ?? 0);
  $("#researchReviewValue").textContent = String(overview.strategies_needing_review ?? 0);

  // Strategy Library filters
  const flat = (arr) => (Array.isArray(arr) ? arr : [arr]).filter((v) => v && v !== "review_needed");
  populateSelect("#researchCategoryFilter", uniqueValues(strategies.map((s) => s.strategy_category)), "All");
  populateSelect("#researchMethodFilter", uniqueValues(strategies.flatMap((s) => flat(s.method))), "All");
  populateSelect("#researchRegimeFilter", uniqueValues(strategies.flatMap((s) => flat(s.expected_market_regime))), "All");
  populateSelect("#researchTimeframeFilter", uniqueValues(strategies.map((s) => s.original_timeframe)), "All");
  populateSelect("#researchTagFilter", uniqueValues(strategies.flatMap((s) => flat(s.tags))), "All");
  populateSelect("#researchStatusFilter", uniqueValues(strategies.map((s) => s.maturity_level)), "All");

  const term = ($("#researchStrategySearch").value || "").toLowerCase();
  const cat = $("#researchCategoryFilter").value;
  const method = $("#researchMethodFilter").value;
  const regime = $("#researchRegimeFilter").value;
  const tf = $("#researchTimeframeFilter").value;
  const tag = $("#researchTagFilter").value;
  const status = $("#researchStatusFilter").value;
  const has = (field, val) => !val || (Array.isArray(field) ? field.includes(val) : field === val);

  const filtered = strategies.filter((s) => {
    if (cat && s.strategy_category !== cat) return false;
    if (!has(s.method, method)) return false;
    if (!has(s.expected_market_regime, regime)) return false;
    if (tf && s.original_timeframe !== tf) return false;
    if (!has(s.tags, tag)) return false;
    if (status && s.maturity_level !== status) return false;
    if (term && !JSON.stringify(s).toLowerCase().includes(term)) return false;
    return true;
  });

  $("#researchStrategyCount").textContent = `${filtered.length}/${strategies.length}`;
  $("#researchStrategyRows").innerHTML = filtered.length ? filtered.map((s) => `
    <tr>
      <td><code>${escapeHtml(s.strategy_id || "")}</code><div class="muted-sub">${escapeHtml(s.strategy_name || "")}</div></td>
      <td>${researchValue(s.strategy_category)}</td>
      <td>${researchValue(s.method)}</td>
      <td>${researchValue(s.expected_market_regime)}</td>
      <td>${researchValue(s.original_timeframe)}</td>
      <td>${researchValue(s.long_only_or_long_short)}</td>
      <td>${researchValue(s.maturity_level)}</td>
      <td>${researchValue(s.indicators_used)}</td>
      <td>${researchValue(s.tags)}</td>
      <td><code class="muted-sub">${escapeHtml(s.source_folder || "")}</code></td>
    </tr>`).join("") : `<tr><td colspan="10" class="empty-cell">No strategies match</td></tr>`;

  // Indicator Library
  $("#researchIndicatorCount").textContent = `${indicators.length}`;
  $("#researchIndicatorRows").innerHTML = indicators.length ? indicators.map((i) => `
    <tr>
      <td><code>${escapeHtml(i.indicator_id || "")}</code></td>
      <td>${researchValue(i.primary_use)}</td>
      <td>${researchValue(i.indicator_category)}</td>
      <td>${researchBool(i.usable_as_entry_signal)}</td>
      <td>${researchBool(i.usable_as_confirmation_filter)}</td>
      <td>${researchBool(i.usable_as_regime_filter)}</td>
      <td>${researchBool(i.usable_as_exit_signal)}</td>
      <td>${researchBool(i.usable_as_stop_or_trailing_component)}</td>
      <td>${researchValue(i.repaint_risk_notes)}</td>
      <td>${researchValue(i.lookahead_risk_notes)}</td>
      <td>${researchValue(i.tags)}</td>
    </tr>`).join("") : `<tr><td colspan="11" class="empty-cell">No indicators</td></tr>`;

  // Component Library grouped by type
  $("#researchComponentCount").textContent = `${components.length}`;
  const groups = {};
  components.forEach((c) => { (groups[c.component_type] = groups[c.component_type] || []).push(c); });
  $("#researchComponentGroups").innerHTML = Object.keys(groups).sort().map((type) => `
    <div class="parity-cell">
      <span>${escapeHtml(labelize(type))}</span>
      <strong>${groups[type].length}</strong>
      <div class="muted-sub">${groups[type].map((c) => escapeHtml(c.based_on_indicator || c.component_id)).filter((v, idx, a) => a.indexOf(v) === idx).join(", ")}</div>
    </div>`).join("") || `<div class="parity-cell"><span>No components</span></div>`;

  // Research Runs
  $("#researchRunCount").textContent = `${runs.length} runs`;
  $("#researchRunRows").innerHTML = runs.length ? runs.map((r) => `
    <tr>
      <td><code>${escapeHtml(r.research_run_id || "")}</code></td>
      <td>${researchValue(r.date)}</td>
      <td>${researchValue(r.status)}</td>
      <td>${researchValue(r.objective)}</td>
      <td>${researchValue(r.architecture_families_tested)}</td>
      <td>${researchValue(r.variants_tested ?? r.number_of_variants)}</td>
      <td>${researchValue(r.final_recommendation)}</td>
      <td><code class="muted-sub">${escapeHtml(r.report_path || "")}</code></td>
    </tr>`).join("") : `<tr><td colspan="8" class="empty-cell">No research runs yet — created when AI strategy research begins.</td></tr>`;

  // Variant Log
  $("#researchVariantCount").textContent = `${variants.length} variants`;
  $("#researchVariantRows").innerHTML = variants.length ? variants.map((v) => `
    <tr>
      <td><code>${escapeHtml(v.variant_id || "")}</code></td>
      <td>${researchValue(v.research_run_id)}</td>
      <td>${researchValue(v.architecture_family)}</td>
      <td>${researchValue(v.components_used)}</td>
      <td>${researchValue(v.assets_tested)}</td>
      <td>${researchValue(v.timeframe)}</td>
      <td>${researchValue(v.net_profit)}</td>
      <td>${researchValue(v.max_drawdown)}</td>
      <td>${researchValue(v.profit_factor)}</td>
      <td>${researchValue(v.win_rate)}</td>
      <td>${researchValue(v.decision)}</td>
      <td><code class="muted-sub">${escapeHtml(v.report_link_or_path || "")}</code></td>
    </tr>`).join("") : `<tr><td colspan="12" class="empty-cell">No variants logged yet.</td></tr>`;

  // Backtest Results
  $("#researchBacktestCount").textContent = `${backtests.length} results`;
  $("#researchBacktestRows").innerHTML = backtests.length ? backtests.map((b) => `
    <tr>
      <td>${researchValue(b.research_run_id)}</td>
      <td>${researchValue(b.variant_id)}</td>
      <td>${researchValue(b.asset)}</td>
      <td>${researchValue(b.date_range)}</td>
      <td>${researchValue(b.number_of_trades)}</td>
      <td>${researchValue(b.net_profit)}</td>
      <td>${researchValue(b.max_drawdown)}</td>
      <td>${researchValue(b.profit_factor)}</td>
      <td>${researchValue(b.win_rate)}</td>
      <td>${researchValue(b.exposure)}</td>
      <td>${researchValue(b.final_equity)}</td>
      <td>${researchValue(b.notes)}</td>
    </tr>`).join("") : `<tr><td colspan="12" class="empty-cell">No backtest results yet.</td></tr>`;

  // Workflow & Rules
  $("#researchWorkflowList").innerHTML = Object.entries(docs).map(([key, path]) => `
    <div class="report-item">
      <strong>${escapeHtml(labelize(key))}</strong>
      <span class="muted-sub"><code>${escapeHtml(path)}</code></span>
    </div>`).join("");

  // Triage Worklist
  const triage = research.triage_candidates || [];
  const tsum = research.triage_summary || {};
  $("#researchTriageValue").textContent = String(tsum.total ?? triage.length);
  $("#researchTriageTranscriptValue").textContent = String(tsum.with_transcript ?? 0);
  $("#researchRetriageValue").textContent = String(tsum.eligible_for_retriage ?? 0);
  populateSelect("#researchTriageQualityFilter", uniqueValues(triage.map((c) => c.source_quality)), "All");
  const tTerm = ($("#researchTriageSearch").value || "").toLowerCase();
  const tQual = $("#researchTriageQualityFilter").value;
  const tTrans = $("#researchTriageTranscriptFilter").value;
  const tElig = $("#researchTriageEligibleFilter").value;
  const triageFiltered = triage.filter((c) => {
    if (tQual && c.source_quality !== tQual) return false;
    if (tTrans === "yes" && !c.transcript_present) return false;
    if (tTrans === "no" && c.transcript_present) return false;
    if (tElig === "yes" && !c.eligible_for_retriage) return false;
    if (tElig === "no" && c.eligible_for_retriage) return false;
    if (tTerm && !JSON.stringify(c).toLowerCase().includes(tTerm)) return false;
    return true;
  });
  $("#researchTriageCount").textContent = `${triageFiltered.length}/${triage.length}`;
  $("#researchTriageRows").innerHTML = triageFiltered.length ? triageFiltered.map((c) => `
    <tr>
      <td><code>${escapeHtml(c.stg_code || "")}</code></td>
      <td>${researchValue(c.title)}<div class="muted-sub"><code>${escapeHtml(c.candidate_id || "")}</code></div></td>
      <td>${researchValue(c.source_quality)}</td>
      <td>${researchValue(c.coverage_status_live)}</td>
      <td>${c.transcript_present ? "✓" : "·"}</td>
      <td>${c.eligible_for_retriage ? "✓" : "·"}</td>
      <td>${c.source_url ? `<a href="${escapeHtml(c.source_url)}" target="_blank" rel="noopener">link</a>` : "--"}</td>
      <td>${researchValue(c.recommended_next_step)}</td>
    </tr>`).join("") : `<tr><td colspan="8" class="empty-cell">No triage candidates match</td></tr>`;

  // Missing Metadata
  $("#researchMissingCount").textContent = `${missing.length}`;
  $("#researchMissingRows").innerHTML = missing.length ? missing.map((m) => `
    <tr>
      <td>${researchValue(m.type)}</td>
      <td><code>${escapeHtml(m.id || "")}</code></td>
      <td>${researchValue(m.name)}</td>
      <td>${researchValue(m.missing_fields)}</td>
    </tr>`).join("") : `<tr><td colspan="4" class="empty-cell">No missing metadata 🎉</td></tr>`;
}

function renderTasks() {
  const tasks = state.snapshot.task_queue?.tasks || [];
  const lifecycle = state.snapshot.task_lifecycle || {};
  const lifecycleSummary = lifecycle.summary || {};
  renderTaskLifecycleGrid(lifecycleSummary);
  populateSelect("#taskStatusFilter", uniqueValues(tasks.map((task) => task.status)), "All");
  const filtered = filterTasks(tasks);
  $("#taskCount").textContent = `${filtered.length}/${tasks.length} ${tasks.length === 1 ? "task" : "tasks"}`;
  if (!filtered.length) {
    $("#taskRows").innerHTML = `<tr><td colspan="6" class="empty-cell">No tasks match</td></tr>`;
    return;
  }
  const taskFlags = lifecycle.task_flags || {};
  $("#taskRows").innerHTML = filtered.map((task) => `
    <tr>
      <td><code>${escapeHtml(task.id || "--")}</code></td>
      <td>${escapeHtml(task.title || "--")}</td>
      <td>${badge(task.status || "--")}</td>
      <td>${escapeHtml(task.phase || "--")}</td>
      <td>${renderFlags(taskFlags[task.id] || [])}</td>
      <td>${task.report_path ? reportButton(task.report_path) : "--"}</td>
    </tr>
  `).join("");
}

function renderTaskLifecycleGrid(summary) {
  const byStatus = summary.by_status || {};
  const entries = [
    ["Total", summary.total],
    ["Waiting", summary.waiting_for_user],
    ["Stale candidates", summary.stale_candidates],
    ["Ready", byStatus.READY || 0],
    ["In progress", byStatus.IN_PROGRESS || 0],
    ["Done", byStatus.DONE || 0]
  ];
  $("#taskLifecycleGrid").innerHTML = entries.map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${Number(value || 0)}</strong>
    </div>
  `).join("");
}

function renderParity() {
  const parity = state.snapshot.parity_status || {};
  const summary = parity.summary || {};
  $("#paritySource").textContent = parity.source || "--";
  const entries = [
    ["Total", summary.total_cases],
    ["Runnable", summary.runnable_cases],
    ["Overall pass", summary.overall_pass],
    ["Failed", summary.failed],
    ["Needs export", summary.needs_user_export],
    ["TradingView pass", summary.tradingview_pass],
    ["Python pass", summary.python_pass],
    ["PineTS pass", summary.pinets_pass]
  ];
  $("#parityGrid").innerHTML = entries.map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${Number(value || 0)}</strong>
    </div>
  `).join("");
}

function renderBacktest() {
  const backtest = state.snapshot.backtest_status || {};
  const summary = backtest.summary || {};
  const runs = backtest.runs || [];
  $("#backtestSource").textContent = backtest.source || "--";
  const entries = [
    ["Total runs", summary.total_runs],
    ["Failed runs", summary.failed_runs],
    ["Last run", summary.last_run_id || "--"],
    ["Last successful", summary.last_successful_run || "--"]
  ];
  $("#backtestGrid").innerHTML = entries.map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value ?? 0)}</strong>
    </div>
  `).join("");
  if (!runs.length) {
    $("#backtestRows").innerHTML = `<tr><td colspan="5" class="empty-cell">No backtest runs yet</td></tr>`;
    return;
  }
  $("#backtestRows").innerHTML = runs.map((run) => `
    <tr>
      <td><code>${escapeHtml(run.run_id || run.id || "--")}</code></td>
      <td>${badge(run.status || "--")}</td>
      <td>${escapeHtml(run.symbol || run.ticker || "--")}</td>
      <td>${escapeHtml(run.timeframe || "--")}</td>
      <td>${run.report_path ? reportButton(run.report_path) : "--"}</td>
    </tr>
  `).join("");
}

function renderRegistry() {
  const registry = state.snapshot.strategy_registry || {};
  const candidates = registry.candidates || [];
  const strategies = registry.strategies || [];
  const entries = registryEntries(registry);
  $("#registryCount").textContent = `${entries.length} ${entries.length === 1 ? "entry" : "entries"}`;
  const readyCount = entries.filter((entry) => String(entry.status || "").toUpperCase() === "READY").length;
  const promotedCount = entries.filter((entry) => {
    const status = String(entry.status || "").toUpperCase();
    return status === "PROMOTED" || status.includes("PROMOTE") || entry.evidence_level === "promoted_to_parity";
  }).length;
  $("#registryGrid").innerHTML = [
    ["Candidates", candidates.length],
    ["Strategies", strategies.length],
    ["Ready", readyCount],
    ["Promoted", promotedCount]
  ].map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${Number(value || 0)}</strong>
    </div>
  `).join("");
  if (!entries.length) {
    $("#registryRows").innerHTML = `<tr><td colspan="5" class="empty-cell">No strategy entries yet</td></tr>`;
    return;
  }
  $("#registryRows").innerHTML = entries.map((entry) => `
    <tr>
      <td><code>${escapeHtml(entry.id || entry.strategy_id || entry.candidate_id || "--")}</code></td>
      <td>${escapeHtml(entry.name || entry.title || "--")}</td>
      <td>${badge(entry.status || "--")}</td>
      <td>${escapeHtml(entry.evidence_level || entry.evidence || "--")}</td>
      <td>${escapeHtml(entry.notes || entry.summary || "--")}</td>
    </tr>
  `).join("");
}

function renderPineBuilder() {
  const pine = state.snapshot.pine_builder_status || {};
  const summary = pine.summary || {};
  const drafts = pine.drafts || [];
  $("#pineBuilderSource").textContent = pine.source || "--";
  $("#pineBuilderGrid").innerHTML = [
    ["Drafts", summary.total_drafts],
    ["Compile pass", summary.compile_pass],
    ["Waiting compile", summary.waiting_for_tradingview_compile],
    ["Protected core", summary.protected_core_files],
    ["Chart run pass", summary.chart_run_pass],
    ["Supporting artifacts", summary.supporting_pine_artifacts]
  ].map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value ?? 0)}</strong>
    </div>
  `).join("");
  if (!drafts.length) {
    $("#pineBuilderRows").innerHTML = `<tr><td colspan="5" class="empty-cell">No Pine review drafts yet</td></tr>`;
    return;
  }
  $("#pineBuilderRows").innerHTML = drafts.map((draft) => `
    <tr>
      <td><code>${escapeHtml(draft.draft_id || draft.name || "--")}</code></td>
      <td>${badge(draft.status || "--")}</td>
      <td>${badge(draft.compile_status || "--")}</td>
      <td>${escapeHtml(statusText(draft.promotion_gate || "--"))}</td>
      <td><code>${escapeHtml(draft.relative_path || draft.source_path || "--")}</code></td>
    </tr>
  `).join("");
}

function renderOptimization() {
  const optimization = state.snapshot.optimization_status || {};
  const summary = optimization.summary || {};
  const runs = optimization.runs || [];
  const candidates = optimization.top_candidates || [];
  const riskNotes = optimization.risk_notes || [];
  $("#optimizationSource").textContent = optimization.source || "--";
  $("#optimizationGrid").innerHTML = [
    ["Runs", summary.total_runs],
    ["Completed", summary.completed_runs],
    ["Partial/check", summary.partial_or_check_runs],
    ["Failed evals", summary.failed_evaluations],
    ["Top candidates", summary.top_candidate_count],
    ["Worker rec", summary.recommended_worker_count || "--"]
  ].map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(formatNumber(value ?? 0))}</strong>
    </div>
  `).join("");

  if (!runs.length) {
    $("#optimizationRows").innerHTML = `<tr><td colspan="5" class="empty-cell">No optimization runs yet</td></tr>`;
  } else {
    $("#optimizationRows").innerHTML = runs.map((run) => `
      <tr>
        <td><code>${escapeHtml(run.run_id || "--")}</code></td>
        <td>${badge(run.status || "--")}</td>
        <td>${escapeHtml(progressText(run))}</td>
        <td>${escapeHtml(run.max_workers || run.worker_count || "--")}</td>
        <td><code>${escapeHtml(run.report_path || run.relative_source_path || "--")}</code></td>
      </tr>
    `).join("");
  }

  $("#optimizationCandidateCount").textContent = `${candidates.length} ${candidates.length === 1 ? "candidate" : "candidates"}`;
  if (!candidates.length) {
    $("#optimizationCandidateRows").innerHTML = `<tr><td colspan="5" class="empty-cell">No ranked candidates yet</td></tr>`;
  } else {
    $("#optimizationCandidateRows").innerHTML = candidates.map((candidate) => `
      <tr>
        <td><code>${escapeHtml(candidate.candidate_id || candidate.parameter_hash || "--")}</code></td>
        <td>${badge(candidate.status || "--")}</td>
        <td>${escapeHtml(formatNumber(candidate.score ?? "--"))}</td>
        <td>${escapeHtml(scopeText(candidate))}</td>
        <td>${escapeHtml(candidate.param_preview || candidate.notes || "--")}</td>
      </tr>
    `).join("");
  }

  $("#optimizationRiskCount").textContent = `${riskNotes.length} ${riskNotes.length === 1 ? "note" : "notes"}`;
  if (!riskNotes.length) {
    $("#optimizationRiskList").innerHTML = `<div class="empty-state">No optimization risk notes yet</div>`;
  } else {
    $("#optimizationRiskList").innerHTML = riskNotes.map((note) => `
      <article class="report-item">
        <span>${escapeHtml(note.updated_at || "--")}</span>
        <strong>${escapeHtml(note.title || "--")}</strong>
        <code>${escapeHtml(note.relative_path || "--")}</code>
      </article>
    `).join("");
  }
}

function renderLiveOps() {
  const liveops = state.snapshot.liveops_status || {};
  const summary = liveops.summary || {};
  const gates = liveops.safety_gates || {};
  const plans = liveops.paper_trade_plans || [];
  $("#liveopsSource").textContent = liveops.source || "--";
  $("#liveopsGrid").innerHTML = [
    ["Mode", summary.mode || liveops.mode || "--"],
    ["Dry-run", summary.dry_run ? "Yes" : "No"],
    ["Live trading", summary.live_trading_enabled ? "Enabled" : "Disabled"],
    ["Events", summary.event_count],
    ["Paper plans", summary.paper_trade_plan_count],
    ["Safety gates", summary.all_safety_gates_ok ? "OK" : "Check"]
  ].map(([label, value]) => `
    <div class="parity-cell">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value ?? 0)}</strong>
    </div>
  `).join("");

  $("#liveopsGateRows").innerHTML = Object.entries(gates).map(([key, value]) => `
    <tr>
      <td>${escapeHtml(statusText(key))}</td>
      <td>${value ? badge("OK", "ok") : badge("CHECK", "bad")}</td>
    </tr>
  `).join("");

  $("#liveopsPlanCount").textContent = `${plans.length} ${plans.length === 1 ? "plan" : "plans"}`;
  if (!plans.length) {
    $("#liveopsPlanRows").innerHTML = `<tr><td colspan="4" class="empty-cell">No forward paper-trade plans yet</td></tr>`;
    return;
  }
  $("#liveopsPlanRows").innerHTML = plans.map((plan) => `
    <tr>
      <td><code>${escapeHtml(plan.candidate_id || "--")}</code></td>
      <td>${badge(plan.status || "--")}</td>
      <td>${plan.webhook_enabled ? badge("ENABLED", "bad") : badge("DISABLED", "ok")}</td>
      <td><code>${escapeHtml(plan.relative_path || plan.source_path || "--")}</code></td>
    </tr>
  `).join("");
}

function renderReports() {
  const reports = state.snapshot.report_manifest?.reports || [];
  populateSelect("#reportCategoryFilter", uniqueValues(reports.map((report) => report.category)), "All");
  const filtered = filterReports(reports);
  $("#reportCount").textContent = `${filtered.length}/${reports.length} ${reports.length === 1 ? "report" : "reports"}`;
  if (!filtered.length) {
    $("#reportList").innerHTML = `<div class="empty-state">No reports match</div>`;
    return;
  }
  $("#reportList").innerHTML = filtered.map((report) => `
    <article class="report-item ${state.selectedReportPath === report.path ? "is-selected" : ""}">
      <span>${escapeHtml(report.category || "--")} / ${escapeHtml(report.report_id || "--")}</span>
      <strong>${escapeHtml(report.title || "--")}</strong>
      <code>${escapeHtml(report.path || "--")}</code>
      <button type="button" data-report-path="${escapeHtml(report.path || "")}">View</button>
    </article>
  `).join("");
  if (!state.selectedReportPath && reports[0]) {
    loadReport(reports[0].path);
  }
}

function renderDiagnostics() {
  const diagnostics = state.snapshot.file_diagnostics || {};
  const values = Object.entries(diagnostics);
  const okCount = values.filter(([, item]) => item.ok).length;
  $("#diagnosticsSummary").textContent = `${okCount}/${values.length} OK`;
  $("#diagnosticRows").innerHTML = values.map(([key, item]) => `
    <tr>
      <td><code>${escapeHtml(item.path || key)}</code></td>
      <td>${item.required ? "Yes" : "No"}</td>
      <td>${booleanLabel(item.json_ok)}</td>
      <td>${booleanLabel(item.schema_ok)}</td>
      <td>${item.ok ? badge("OK", "ok") : badge("CHECK", "bad")}</td>
    </tr>
  `).join("");
}

function badge(text, forcedClass) {
  const value = String(text);
  const normalized = value.toUpperCase();
  const isOk = ["DONE", "OK", "READY", "PASS", "CHART_RUN_PASS"].includes(normalized)
    || normalized.endsWith("_PASS");
  const isBad = normalized.includes("FAIL") || normalized.includes("ERROR") || normalized === "CHECK";
  const cls = forcedClass || (isOk ? "ok" : isBad ? "bad" : "neutral");
  return `<span class="badge ${cls}">${escapeHtml(statusText(value))}</span>`;
}

function renderScoreBadge(scorecard) {
  if (scorecard === null || scorecard === undefined || scorecard === "") {
    return badge("—", "neutral");
  }
  const card = typeof scorecard === "number"
    ? { total: scorecard, label: `${scorecard}/100`, band: scoreBand(scorecard), note: "" }
    : scorecard;
  const total = Number(card.total ?? 0);
  const cls = card.band === "high" ? "ok" : card.band === "medium" ? "neutral" : "bad";
  return `<span class="badge ${cls}" title="${escapeHtml(card.note || 'Heuristic composite score')}" data-score="${escapeHtml(String(total))}">${escapeHtml(card.label || `${total}/100`)}</span>`;
}

function qualityBadge(value) {
  const quality = String(value || "LOW").toUpperCase();
  const classMap = { HIGH: "ok", MEDIUM: "neutral", PARENT: "neutral", LOW: "bad", REJECTED: "bad" };
  return badge(quality, classMap[quality] || "neutral");
}

function statusText(value) {
  return String(value).replaceAll("_", " ");
}

function renderFlags(flags) {
  if (!flags.length) {
    return `<span class="badge neutral">NONE</span>`;
  }
  return flags.map((flag) => badge(flag, flag === "STALE_CANDIDATE" ? "bad" : "neutral")).join(" ");
}

function renderActionCell(action, hint) {
  const label = String(action || "—");
  const text = statusText(label);
  const description = String(hint || "").trim();
  if (!description) {
    return `<span class="action-copy"><strong>${escapeHtml(text)}</strong></span>`;
  }
  return `
    <span class="action-copy" title="${escapeHtml(description)}">
      <strong>${escapeHtml(text)}</strong>
      <span>${escapeHtml(description)}</span>
    </span>
  `;
}

function renderScorecard(scorecard) {
  if (!scorecard) {
    return null;
  }
  const rows = (scorecard.components || []).map((component) => `
    <tr>
      <td>${escapeHtml(component.label)}</td>
      <td><strong>${escapeHtml(String(component.score ?? 0))}/${escapeHtml(String(component.max ?? 0))}</strong></td>
      <td>${escapeHtml(component.note || "—")}</td>
    </tr>
  `).join("");
  return `
    <div class="detail-card scorecard-card">
      <div class="scorecard-head">
        <p><strong>${escapeHtml(scorecard.label || `${scorecard.total || 0}/100`)}</strong></p>
        <span class="badge ${scoreBand(scorecard.total)}">${escapeHtml((scorecard.band || scoreBand(scorecard.total)).toUpperCase())}</span>
      </div>
      <p class="muted-sub">${escapeHtml(scorecard.note || "Heuristic composite score for triage; not a profit forecast.")}</p>
      <table class="kv scorecard-table">
        ${rows}
      </table>
    </div>
  `;
}

function reportButton(path) {
  return `
    <div class="report-ref">
      <code>${escapeHtml(path)}</code>
      <button type="button" data-report-path="${escapeHtml(path)}">View</button>
    </div>
  `;
}

function filterTasks(tasks) {
  const search = ($("#taskSearch").value || "").trim().toLowerCase();
  const status = $("#taskStatusFilter").value;
  return tasks.filter((task) => {
    const haystack = [task.id, task.title, task.phase, task.report_path].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) && (!status || task.status === status);
  });
}

function filterPipelineRows(rows) {
  const search = ($("#pipelineSearch").value || "").trim().toLowerCase();
  const score = $("#pipelineScoreFilter").value;
  const action = $("#pipelineActionFilter").value;
  return rows.filter((row) => {
    const haystack = [
      row.id,
      row.stg_code,
      row.symbol,
      row.timeframe,
      row.next_action,
      row.description && row.description.family,
      row.description && row.description.what
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search))
      && (!score || scoreBand(row.score) === score)
      && (!action || row.next_action === action);
  });
}

function filterAuditRows(rows) {
  const search = ($("#auditSearch").value || "").trim().toLowerCase();
  const strategy = $("#auditStrategyFilter").value;
  const quality = $("#auditQualityFilter").value;
  const rules = $("#auditRulesFilter").value;
  const source = $("#auditSourceFilter").value;
  const txVerdict = $("#auditTxVerdictFilter").value;
  const eligible = $("#auditEligibleFilter").value;
  const blocked = $("#auditBlockedFilter").value;
  const canonical = $("#auditCanonicalFilter").value;
  const step = $("#auditStepFilter").value;
  const score = $("#auditScoreFilter").value;
  const txRec = state.snapshot.transcript_reclassification || null;
  const txByCid = {};
  if (txRec && txRec.rows) {
    for (const tr of txRec.rows) { txByCid[tr.candidate_id] = tr; }
  }
  return rows.filter((row) => {
    const tx = txByCid[row.id] || null;
    const rowTxVerdict = tx ? tx.verdict : (row.has_transcript && !tx ? "NO_SCAN" : "");
    const haystack = [
      row.id,
      row.stg_code,
      row.description_family,
      row.description_hint,
      row.source_url,
      row.transcript_path,
      row.blocked_reason,
      row.canonical_id,
      row.duplicate_of,
      row.recommended_next_pipeline_step,
      rowTxVerdict
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search))
      && (!strategy || row.id === strategy)
      && (!quality || row.source_quality === quality)
      && (!rules || ((row.has_deterministic_rules ? "YES" : "NO") === rules))
      && (!source || ((row.has_source_url_transcript ? "YES" : "NO") === source))
      && (!txVerdict || rowTxVerdict === txVerdict)
      && (!eligible || ((row.eligible_for_backtest ? "YES" : "NO") === eligible))
      && (!blocked || row.blocked_reason === blocked)
      && (!canonical || ((row.duplicate_of ? "DUPLICATE" : "CANONICAL") === canonical))
      && (!step || row.recommended_next_pipeline_step === step)
      && (!score || scoreBand(row.score) === score);
  });
}

function filterMtcV2Rows(rows) {
  const search = ($("#mtcV2Search").value || "").trim().toLowerCase();
  const status = $("#mtcV2StatusFilter").value;
  const score = $("#mtcV2ScoreFilter").value;
  return rows.filter((row) => {
    const haystack = [
      row.id,
      row.stg_code,
      row.status,
      row.reason,
      row.blocker,
      row.stage,
      row.next_action
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search))
      && (!status || row.status === status)
      && (!score || scoreBand(row.score) === score);
  });
}

function filterReports(reports) {
  const search = ($("#reportSearch").value || "").trim().toLowerCase();
  const category = $("#reportCategoryFilter").value;
  return reports.filter((report) => {
    const haystack = [report.report_id, report.category, report.title, report.path, report.summary].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) && (!category || report.category === category);
  });
}

function populateSelect(selector, values, allLabel) {
  const select = $(selector);
  const current = select.value;
  const normalized = values.filter(Boolean).sort();
  select.innerHTML = [`<option value="">${escapeHtml(allLabel)}</option>`]
    .concat(normalized.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`))
    .join("");
  if (normalized.includes(current)) {
    select.value = current;
  }
}

function populateSelectPairs(selector, items, allLabel) {
  const select = $(selector);
  const current = select.value;
  const seen = new Set();
  const normalized = items.filter((item) => {
    if (!item || !item.value || seen.has(item.value)) {
      return false;
    }
    seen.add(item.value);
    return true;
  }).slice().sort((a, b) => a.label.localeCompare(b.label));
  select.innerHTML = [`<option value="">${escapeHtml(allLabel)}</option>`]
    .concat(normalized.map((item) => `<option value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</option>`))
    .join("");
  if (normalized.some((item) => item.value === current)) {
    select.value = current;
  }
}

function populateAuditFilters(rows) {
  populateSelectPairs(
    "#auditStrategyFilter",
    rows.map((row) => ({
      value: row.id,
      label: [row.stg_code || "", row.id].filter(Boolean).join(" · "),
    })),
    "All"
  );
  populateSelect("#auditQualityFilter", uniqueValues(rows.map((row) => row.source_quality)), "All");
  populateSelect("#auditRulesFilter", uniqueValues(rows.map((row) => (row.has_deterministic_rules ? "YES" : "NO"))), "All");
  populateSelect("#auditSourceFilter", uniqueValues(rows.map((row) => (row.has_source_url_transcript ? "YES" : "NO"))), "All");
  const txRec = state.snapshot.transcript_reclassification || null;
  const txByCid = {};
  if (txRec && txRec.rows) {
    for (const tr of txRec.rows) { txByCid[tr.candidate_id] = tr; }
  }
  const txOptions = rows.map((row) => {
    const tx = txByCid[row.id];
    return tx ? tx.verdict : (row.has_transcript && !tx ? "NO_SCAN" : "");
  }).filter(Boolean);
  populateSelect("#auditTxVerdictFilter", uniqueValues(txOptions), "All");
  populateSelect("#auditEligibleFilter", uniqueValues(rows.map((row) => (row.eligible_for_backtest ? "YES" : "NO"))), "All");
  populateSelect("#auditBlockedFilter", uniqueValues(rows.map((row) => row.blocked_reason)), "All");
  populateSelect("#auditCanonicalFilter", uniqueValues(rows.map((row) => (row.duplicate_of ? "DUPLICATE" : "CANONICAL"))), "All");
  populateSelect("#auditStepFilter", uniqueValues(rows.map((row) => row.recommended_next_pipeline_step)), "All");
}

function uniqueValues(values) {
  return Array.from(new Set(values.filter(Boolean)));
}

function scoreBand(value) {
  const score = Number(value || 0);
  if (score >= 85) return "high";
  if (score >= 65) return "medium";
  return "low";
}

function registryEntries(registry) {
  return []
    .concat(registry.candidates || [])
    .concat(registry.strategies || []);
}

function progressText(run) {
  const completed = run.completed_evaluations ?? 0;
  const planned = run.planned_evaluations ?? 0;
  const failed = run.failed_evaluations ?? 0;
  if (!planned && !completed && !failed) {
    return "--";
  }
  return `${formatNumber(completed)}/${formatNumber(planned)} done, ${formatNumber(failed)} failed`;
}

function scopeText(candidate) {
  return candidate.symbol || candidate.symbols_tested || candidate.timeframe || candidate.timeframes_tested || candidate.source_type || "--";
}

function formatNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return Number.isInteger(value) ? String(value) : value.toFixed(2);
  }
  return String(value);
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const output = [];
  let inCode = false;
  let codeLines = [];

  for (const line of lines) {
    if (line.startsWith("```")) {
      if (inCode) {
        output.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
        codeLines = [];
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      continue;
    }

    const heading = line.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length + 1;
      output.push(`<h${level}>${formatInline(heading[2])}</h${level}>`);
      continue;
    }

    if (line.startsWith("- ")) {
      output.push(`<p class="md-list">${formatInline(line.slice(2))}</p>`);
      continue;
    }

    if (!line.trim()) {
      output.push(`<div class="md-gap"></div>`);
      continue;
    }

    output.push(`<p>${formatInline(line)}</p>`);
  }

  if (inCode) {
    output.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
  }

  return output.join("");
}

function formatInline(value) {
  return escapeHtml(value).replaceAll(/`([^`]+)`/g, "<code>$1</code>");
}

function booleanLabel(value) {
  if (value === null || value === undefined) {
    return `<span class="badge neutral">N/A</span>`;
  }
  return value ? `<span class="badge ok">OK</span>` : `<span class="badge bad">CHECK</span>`;
}

function setNotice(message) {
  const notice = $("#notice");
  notice.hidden = !message;
  notice.textContent = message || "";
}

function labelize(value) {
  return value.replaceAll("_", " ");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}



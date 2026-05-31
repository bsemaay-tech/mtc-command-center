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
  const rows = pipe.rows || [];
  const stages = pipe.stages || [];
  const counts = (pipe.summary && pipe.summary.stage_done_counts) || {};
  $("#pipelineIntro").textContent = "Each row is one strategy journey. The Stg tag is the stable triage code, the score is a heuristic fit score out of 100, and the next action tells you the single best next step.";
  populateSelect("#pipelineActionFilter", uniqueValues(rows.map((row) => row.next_action)), "All");
  const filtered = filterPipelineRows(rows);
  $("#pipelineCount").textContent = `${filtered.length}/${rows.length} ${rows.length === 1 ? "strategy" : "strategies"}`;
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
      <tr class="row-click" data-id="${escapeHtml(row.id)}" title="Detay için tıkla">
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
  const rows = audit.rows || [];
  const summary = audit.summary || {};
  $("#auditIntro").textContent = "This table explains why a row is eligible, blocked, or parked. Sources is the raw scanned record count, Source audit means the source or formula still needs verification, and Next step is the immediate action recommended by the read-only gate.";
  $("#auditCount").textContent = `${rows.length} ${rows.length === 1 ? "record" : "records"}`;
  $("#auditSummary").innerHTML = [
    ["Eligible", summary.eligible_for_backtest_rows, "Rows that can go straight to backtest from the current read-only gate."],
    ["Blocked", summary.blocked_rows, "Rows parked because the source, formula, or classification still needs work."],
    ["Split required", summary.split_required_rows, "Rows that must be split into separate indicator cases before testing."],
    ["Source audit", summary.source_audit_rows, "Rows that need exact source/formula verification before any backtest."],
    ["Duplicates", summary.duplicate_rows, "Duplicate rows mapped to one canonical record."],
    ["Deterministic", summary.deterministic_rule_rows, "Rows with mechanically testable rules visible to the audit layer."],
    ["Source material", summary.source_material_rows, "Rows with at least a URL or transcript path attached."],
    ["Sources", audit.source_record_count || 0, "Raw scanned source records across JSONL and CSV inputs, not unique strategies."]
  ].map(([label, value, title]) => `
    <div class="parity-cell" title="${escapeHtml(title)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(formatNumber(value ?? 0))}</strong>
    </div>
  `).join("");

  populateAuditFilters(rows);
  const filtered = filterAuditRows(rows);
  if (!filtered.length) {
    $("#auditRows").innerHTML = `<tr><td colspan="9" class="empty-cell">No audit rows match</td></tr>`;
    syncUnifiedDetailVisibility();
    return;
  }

  $("#auditRows").innerHTML = filtered.map((row) => `
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
      <td>${badge(row.eligible_for_backtest ? "YES" : "NO", row.eligible_for_backtest ? "ok" : "bad")}</td>
      <td>${escapeHtml(row.blocked_reason || "—")}</td>
      <td>
        <div><code>${escapeHtml(row.canonical_id || row.id || "--")}</code></div>
        ${row.duplicate_of ? `<div class="muted-sub">duplicate of ${escapeHtml(row.duplicate_of)}</div>` : `<div class="muted-sub">canonical</div>`}
        ${row.duplicate_group_size ? `<div class="muted-sub">group ${escapeHtml(String(row.duplicate_group_size))}</div>` : ""}
      </td>
      <td>${renderActionCell(row.recommended_next_pipeline_step || "—", row.next_action_hint || "")}</td>
    </tr>
  `).join("");

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
  const rows = readiness.rows || [];
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
    <p class="muted-sub"><a href="${escapeHtml(url)}" target="_blank" rel="noopener">YouTube'da aç</a></p>`;
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
  const classification = row.classification || (auditRow && auditRow.classification) || {};
  const scorecard = row.scorecard || (auditRow && auditRow.scorecard) || null;
  const sparkline = renderSparkline(row.equity_curve || []);
  const paperTrade = renderPaperTradeDetail(row.paper_trade_detail);
  const parityProof = renderParityProof(row.pinets_parity_proof);
  const directionalResearch = renderDirectionalResearch(row.directional_research);
  const producerSpec = renderProducerSpec(row.producer_spec);
  const scoreDetail = renderScorecard(scorecard);
  const stgCode = row.stg_code || (auditRow && auditRow.stg_code) || '';
  const decisionPanel = renderDecisionPanel(row, auditRow, mtcV2Row, scorecard);
  const metricRows = [
    ['Compound return', metrics.return_pct_compound != null ? `${Number(metrics.return_pct_compound).toFixed(2)}%` : null],
    ['Profit factor', metrics.profit_factor],
    ['Trades', metrics.trades],
    ['Max drawdown', metrics.max_drawdown_pct != null ? `${Number(metrics.max_drawdown_pct).toFixed(1)}%` : null],
    ['Win rate', metrics.win_rate != null ? `${(Number(metrics.win_rate) * 100).toFixed(1)}%` : null],
    ['Direction', metrics.direction]
  ].filter(([, value]) => value !== null && value !== undefined && value !== '');
  const stageList = (stages || []).map((stage) => {
    const cell = (row.stages && row.stages[stage.key]) || {};
    return `<li><span class="badge ${stageCls(cell.status)}">${stageIcon(cell.status)}</span> <strong>${escapeHtml(stage.label)}</strong>${cell.metric ? ` — ${escapeHtml(cell.metric)}` : ''}</li>`;
  }).join('');
  const auditFlagsRows = auditRow ? [
    ['Audit status', auditRow.audit_status],
    ['Triage code', auditRow.stg_code || stgCode || '—'],
    ['Score', auditRow.scorecard ? auditRow.scorecard.label : (row.scorecard ? row.scorecard.label : '—')],
    ['Eligible', auditRow.eligible_for_backtest ? 'YES' : 'NO'],
    ['Blocked reason', auditRow.blocked_reason || '—'],
    ['Split cases', auditRow.split_candidate_count && auditRow.split_candidate_count > 1 ? String(auditRow.split_candidate_count) : '—'],
    ['Canonical ID', auditRow.canonical_id || '--'],
    ['Duplicate of', auditRow.duplicate_of || 'canonical'],
    ['Duplicate group', String(auditRow.duplicate_group_size || 1)],
    ['Next step', auditRow.recommended_next_pipeline_step || '--']
  ] : [];
  const sourceCoverageBadges = auditRow ? `
    <div class="detail-card">
      <p><strong>Has source URL?</strong> ${badge(auditRow.has_source_url ? 'YES' : 'NO', auditRow.has_source_url ? 'ok' : 'bad')}</p>
      <p><strong>Has transcript?</strong> ${badge(auditRow.has_transcript ? 'YES' : 'NO', auditRow.has_transcript ? 'ok' : 'bad')}</p>
      <p><strong>Both present?</strong> ${badge(auditRow.has_source_url_transcript ? 'YES' : 'NO', auditRow.has_source_url_transcript ? 'ok' : 'bad')}</p>
    </div>
  ` : '';
  const sourceMaterialRows = auditRow ? [
    ['Source URL', auditRow.source_url || 'MISSING'],
    ['Source URL came from', auditRow.source_url_source || '—'],
    ['Transcript path', auditRow.transcript_path || 'MISSING'],
    ['Transcript URL', auditRow.transcript_source_url && auditRow.transcript_source_url !== auditRow.source_url ? auditRow.transcript_source_url : '—'],
    ['Intake / source file', sourceRecord.source_file || sourceRecord.relative_source_path || '—']
  ] : [];
  const sourceRecordRows = sourceRecord ? [
    ['Candidate', sourceRecord.candidate_id],
    ['Title', sourceRecord.title],
    ['Source role', sourceRecord.source_role],
    ['Split evidence', auditRow && auditRow.split_candidate_evidence && auditRow.split_candidate_evidence.length ? auditRow.split_candidate_evidence.join(' | ') : ''],
    ['Recommended action', sourceRecord.recommended_next_action],
    ['Summary', sourceRecord.summary],
    ['Source quality', sourceRecord.source_quality],
    ['Rules text', sourceRecord.rules_text]
  ].filter(([, value]) => value) : [];
  const auditExplanations = auditRow ? [
    [`Why quality is ${String(auditRow.source_quality || '--').toLowerCase()}`, auditRow.source_quality_explanation],
    ['Why deterministic rules exist or not', auditRow.deterministic_rules_explanation],
    ['Candidate split check', auditRow.split_candidate_explanation],
    ['Why backtest is or is not eligible', auditRow.eligibility_explanation],
    ['Duplicate / canonical mapping', auditRow.duplicate_mapping_explanation],
    ['Recommended next pipeline step', auditRow.recommended_next_pipeline_step_explanation]
  ].filter(([, value]) => value) : [];
  const title = row.symbol ? `${row.symbol} ${row.timeframe || ''}`.trim() : row.id || '--';
  $('#strategyDetail').innerHTML = `
    <button class="back-btn" id="strategyBack" type="button">← Back to tables</button>
    <h3 class="detail-title">${escapeHtml(title)}</h3>
    <p class="detail-fam">${escapeHtml(description.family || (auditRow && (auditRow.description_family || auditRow.description_hint)) || '')}</p>
    ${decisionPanel}
    <div class="detail-grid">
      <div>
        <h4>Pipeline view</h4>
        <p>${escapeHtml(description.what || (auditRow && auditRow.description_hint) || '—')}</p>
        <p><strong>Entry:</strong> ${escapeHtml(description.entry || '—')}</p>
        <p><strong>Exit:</strong> ${escapeHtml(description.exit || '—')}</p>
        ${classification.kind ? `<p><strong>Classification:</strong> ${escapeHtml(String(classification.label || classification.kind))}</p>` : ''}
        ${classification.reason ? `<p class="muted-sub">${escapeHtml(String(classification.reason))}</p>` : ''}
        ${row.notes ? `<p class="muted-sub">Note: ${escapeHtml(row.notes)}</p>` : ''}
        ${metricRows.length ? `<h4>Backtest metrics</h4><table class="kv">${metricRows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join('')}</table>` : ''}
        ${scoreDetail ? `<h4>Scorecard</h4>${scoreDetail}` : ''}
        <h4>Equity curve</h4>
        ${sparkline}
        <h4>Pipeline stages</h4>
        <ul class="stage-list">${stageList || `<li class="muted-sub">No stage data yet.</li>`}</ul>
        <p class="next-line"><strong>Next action:</strong> ${renderActionCell(row.next_action || (auditRow && auditRow.recommended_next_pipeline_step) || '—', row.next_action_hint || (auditRow && auditRow.next_action_hint) || '')}</p>
        <h4>Source video</h4>
        ${sourceUrl ? ytEmbed(sourceUrl) : `<p class="muted-sub">No source link recorded.</p>`}
        ${sourceUrlSource ? `<p class="muted-sub">Source URL source: ${escapeHtml(sourceUrlSource)}</p>` : ''}
      </div>
      <div>
        <h4>Audit view</h4>
        ${auditFlagsRows.length ? `<table class="kv">${auditFlagsRows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join('')}</table>` : `<p class="muted-sub">No audit row available.</p>`}
        ${auditExplanations.map(([label, text]) => `
          <div class="detail-card stacked-panel">
            <p><strong>${escapeHtml(label)}</strong></p>
            <p>${escapeHtml(String(text))}</p>
          </div>
        `).join('')}
        ${sourceCoverageBadges ? `
          <h4>Source coverage</h4>
          ${sourceCoverageBadges}
        ` : ''}
        ${sourceMaterialRows.length ? `
          <h4>Source material</h4>
          <table class="kv">${sourceMaterialRows.map(([key, value]) => {
            const v = String(value);
            const cell = v === 'MISSING' ? badge('MISSING', 'bad') : `<strong>${escapeHtml(v)}</strong>`;
            return `<tr><td>${escapeHtml(key)}</td><td>${cell}</td></tr>`;
          }).join('')}</table>
        ` : ''}
        ${sourceRecordRows.length ? `
          <h4>Source record</h4>
          <table class="kv">${sourceRecordRows.map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td><strong>${escapeHtml(String(value))}</strong></td></tr>`).join('')}</table>
        ` : ''}
        ${producerSpec ? `
          <h4>Producer spec</h4>
          ${producerSpec}
        ` : ''}
        <h4>Directional research</h4>
        ${directionalResearch}
        <h4>Paper-trade</h4>
        ${paperTrade}
        <h4>PineTS parity proof</h4>
        ${parityProof}
      </div>
    </div>
  `;
}

function renderDecisionPanel(row, auditRow, mtcV2Row, scorecard) {
  const scoreLabel = scorecard ? (scorecard.label || `${scorecard.total || 0}/100`) : "—";
  const auditStatus = auditRow ? (auditRow.audit_status || "—") : "No audit row";
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
    ["Mevcut yön", detail.current_direction],
    ["Durum", detail.status],
    ["Short aksiyon", detail.next_action]
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
  const classMap = { HIGH: "ok", MEDIUM: "neutral", LOW: "bad", REJECTED: "bad" };
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
  const eligible = $("#auditEligibleFilter").value;
  const blocked = $("#auditBlockedFilter").value;
  const canonical = $("#auditCanonicalFilter").value;
  const step = $("#auditStepFilter").value;
  const score = $("#auditScoreFilter").value;
  return rows.filter((row) => {
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
      row.recommended_next_pipeline_step
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search))
      && (!strategy || row.id === strategy)
      && (!quality || row.source_quality === quality)
      && (!rules || ((row.has_deterministic_rules ? "YES" : "NO") === rules))
      && (!source || ((row.has_source_url_transcript ? "YES" : "NO") === source))
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



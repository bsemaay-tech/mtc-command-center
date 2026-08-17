/* Bridge V2 — Dashboard read-only prototype (Package 3, T1).
 *
 * Renders window.FIXTURES (loaded from fixtures/data.js via a <script> tag)
 * into five static views. The page performs NO network access of any kind:
 * no fetch, no XHR, no WebSocket, no EventSource. All data is fixture data;
 * every panel carries a truth label naming which state layer (if any) it
 * displays. There are no ARM/order/config controls — the page controls nothing.
 */
(function () {
  "use strict";

  var FIX = window.FIXTURES;

  /* ---- tiny helpers ------------------------------------------------------- */

  var ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

  function esc(value) {
    return String(value === null || value === undefined ? "" : value).replace(
      /[&<>"']/g,
      function (ch) {
        return ESC_MAP[ch];
      }
    );
  }

  function toMs(iso) {
    return new Date(iso).getTime();
  }

  function ageText(fromIso, asOfIso) {
    var mins = Math.max(0, Math.round((toMs(asOfIso) - toMs(fromIso)) / 60000));
    if (mins < 1) {
      return "now";
    }
    if (mins < 60) {
      return mins + "m ago";
    }
    var h = Math.floor(mins / 60);
    var m = mins % 60;
    if (h < 24) {
      return h + "h" + (m ? " " + m + "m" : "") + " ago";
    }
    var d = Math.floor(h / 24);
    return d + "d " + (h % 24) + "h ago";
  }

  function fixed(value, digits) {
    return Number(value).toFixed(digits);
  }

  function signed(value, digits) {
    return (value > 0 ? "+" : "") + Number(value).toFixed(digits);
  }

  function moneyTone(value) {
    return value > 0 ? "pos" : value < 0 ? "neg" : "";
  }

  function pill(text, tone) {
    return '<span class="pill ' + (tone ? "tone-" + tone : "") + '">' + esc(text) + "</span>";
  }

  function truth(label, tone) {
    return '<span class="truth ' + (tone ? "tone-" + tone : "") + '">' + esc(label) + "</span>";
  }

  function setHtml(id, html) {
    var node = document.getElementById(id);
    if (node) {
      node.innerHTML = html;
    }
  }

  /* ---- fixture-derived helpers ---------------------------------------------- */

  function asOf() {
    return FIX.workers.meta.as_of;
  }

  function unrealized(worker) {
    var p = worker.position;
    if (!p || !p.qty || p.avg_entry === null || p.avg_entry === undefined) {
      return 0;
    }
    var diff = p.side === "SHORT" ? p.avg_entry - p.mark : p.mark - p.avg_entry;
    return diff * p.qty;
  }

  function windowTone(state) {
    return state === "ACTIVE" ? "green" : state === "STALE" ? "amber" : "red";
  }

  function entriesPill(worker) {
    return worker.blocks.length ? pill("ENTRIES BLOCKED", "red") : pill("ENTRIES OPEN", "green");
  }

  function desiredTone(state) {
    if (state === "EMITTED") {
      return "blue";
    }
    if (state === "EXPIRED") {
      return "amber";
    }
    return ""; // SUPERSEDED and anything else read as neutral
  }

  function acceptedTone(state) {
    if (state === "—") {
      return "";
    }
    if (state.indexOf("REJECTED") === 0 || state === "IDENTITY_COLLISION") {
      return "red";
    }
    if (state === "BLOCKED_DUPLICATE" || state === "RECEIVED" || state === "VALIDATING") {
      return "amber";
    }
    return "green";
  }

  function actualTone(state) {
    if (state === "FILLED" || state === "OPEN" || state === "SUBMITTED") {
      return "green";
    }
    if (state === "PARTIALLY_FILLED" || state === "PENDING_NEW" || state === "SUBMITTING" || state === "PENDING_CANCEL") {
      return "amber";
    }
    if (state === "UNKNOWN_SUBMISSION" || state === "REJECTED") {
      return "red";
    }
    return ""; // "—", CANCELED, EXPIRED read as neutral
  }

  function tierName(guardian, tier) {
    var tiers = guardian ? guardian.veto_tiers : [];
    for (var i = 0; i < tiers.length; i++) {
      if (tiers[i].tier === tier) {
        return tiers[i].name;
      }
    }
    return "TIER " + tier;
  }

  function healthWord(worker) {
    return worker.blocks.length === 0
      ? "healthy"
      : worker.blocks[0].guardian_tier
        ? "Guardian-paused"
        : "stale-feed";
  }

  /* ---- view 1 — aggregate execution overview ---------------------------------- */

  function renderOverview() {
    var ws = FIX.workers;
    var workers = ws.workers;
    var guardian = ws.guardian;
    var i;

    var healthy = 0;
    var blocked = 0;
    var realized = 0;
    var unreal = 0;
    for (i = 0; i < workers.length; i++) {
      if (workers[i].blocks.length) {
        blocked++;
      } else {
        healthy++;
      }
      realized += workers[i].ledger.realized_pnl_today;
      unreal += unrealized(workers[i]);
    }

    var cards =
      card("Workers", String(workers.length), healthy + " healthy · " + blocked + " entries blocked (fixture)", "") +
      card(
        "Realized today (sum of per-worker ledgers)",
        signed(realized, 2) + " USDC",
        "Portfolio P&L = summation ABOVE the workers — never one shared ledger",
        moneyTone(realized)
      ) +
      card(
        "Unrealized (sum of per-worker marks)",
        signed(unreal, 2) + " USDC",
        "Each worker's own books, summed here (fixture)",
        moneyTone(unreal)
      ) +
      card(
        "Guardian gross exposure input",
        fixed(guardian.inputs.gross_exposure_pct, 1) + "%",
        guardian.inputs.gross_exposure_note,
        ""
      ) +
      card("Fixture as-of", ws.meta.as_of, "All ages are computed against this frozen time — not wall clock", "");

    setHtml("ov-cards", cards);

    var rows = "";
    for (i = 0; i < workers.length; i++) {
      var w = workers[i];
      var blocksCell = w.blocks.length
        ? w.blocks
            .map(function (b) {
              return (
                pill(b.reason_code, "red") +
                '<span class="note"> ' +
                esc(b.source) +
                (b.guardian_tier ? " · " + esc(tierName(guardian, b.guardian_tier)) : "") +
                "</span>"
              );
            })
            .join("<br>")
        : '<span class="note">none</span>';
      rows +=
        "<tr><td class=\"mono\">" +
        esc(w.worker_id) +
        "</td><td>" +
        esc(w.strategy_id) +
        "<br><span class=\"note\">" +
        esc(w.symbol) +
        " · " +
        esc(w.timeframe) +
        " · " +
        esc(w.account_label) +
        "</span></td><td>" +
        pill(w.health.window_state, windowTone(w.health.window_state)) +
        "</td><td>" +
        ageText(w.health.last_bar_ts, asOf()) +
        '<br><span class="note">' +
        esc(w.health.last_bar_ts) +
        "</span></td><td>" +
        entriesPill(w) +
        "</td><td>" +
        blocksCell +
        "</td><td>" +
        signed(w.ledger.realized_pnl_today, 2) +
        "</td><td>" +
        signed(unrealized(w), 2) +
        "</td></tr>";
    }
    setHtml(
      "ov-workers",
      "<table><thead><tr><th>Worker</th><th>Strategy / market</th><th>Window</th><th>Last bar</th><th>Entries</th><th>Block reasons</th><th>Realized</th><th>Unreal.</th></tr></thead><tbody>" +
        rows +
        "</tbody></table>"
    );

    var active = "";
    for (i = 0; i < workers.length; i++) {
      for (var j = 0; j < workers[i].blocks.length; j++) {
        var b = workers[i].blocks[j];
        if (b.guardian_tier) {
          active +=
            "<li><strong>" +
            esc(workers[i].worker_id) +
            "</strong> — " +
            pill(b.reason_code, "red") +
            " " +
            esc(tierName(guardian, b.guardian_tier)) +
            "<br><span class=\"note\">" +
            esc(b.detail) +
            " " +
            esc(b.scope ? "Scope: " + b.scope + ". " : "") +
            "Logged " +
            esc(b.logged_ts) +
            ". " +
            esc(b.lift) +
            "</span></li>";
        }
      }
    }
    setHtml(
      "ov-guardian",
      "<p>" +
        pill("GUARDIAN: " + guardian.state, "blue") +
        " " +
        pill("GLOBAL HALT: " + (guardian.global_halt ? "ON" : "OFF"), guardian.global_halt ? "red" : "green") +
        ' <span class="note">Snapshot ' +
        esc(guardian.snapshot_ts) +
        " (" +
        ageText(guardian.snapshot_ts, asOf()) +
        "). " +
        esc(guardian.snapshot_basis) +
        "</span></p>" +
        "<h3>Active vetoes (logged and operator-visible)</h3>" +
        (active ? "<ul>" + active + "</ul>" : '<p class="note">none</p>') +
        "<h3>Veto tier vocabulary</h3><ul>" +
        guardian.veto_tiers
          .map(function (t) {
            return "<li>" + pill("TIER " + t.tier + " · " + t.name, t.tier === 3 ? "red" : t.tier === 2 ? "amber" : "blue") + " — " + esc(t.description) + "</li>";
          })
          .join("") +
        "</ul>" +
        "<h3>Standing rules this prototype displays verbatim</h3><ul>" +
        "<li>" + esc(guardian.veto_domain_note) + "</li>" +
        "<li>" + esc(guardian.mutate_note) + "</li>" +
        "<li>" + esc(guardian.fail_closed_note) + "</li>" +
        "<li>" + esc(guardian.thresholds_note) + "</li>" +
        "<li>" + esc(guardian.position_note) + "</li>" +
        "</ul>"
    );

    var si = ws.shared_infrastructure;
    setHtml(
      "ov-infra",
      "<p class=\"note\">" + esc(si.truth_label) + "</p>" +
        meter("REST weight (shared, per minute)", si.rest.fixture_used_weight, si.rest.ip_weight_limit_per_min, fixed(si.rest.fixture_used_weight, 0) + " / " + si.rest.ip_weight_limit_per_min) +
        '<p class="note">' + esc(si.rest.note) + "</p>" +
        meter("WebSocket connections (shared)", si.websocket.fixture_connections, si.websocket.connections_cap, si.websocket.fixture_connections + " / " + si.websocket.connections_cap) +
        meter("WebSocket subscriptions (shared)", si.websocket.fixture_subscriptions, si.websocket.subscriptions_cap, si.websocket.fixture_subscriptions + " / " + si.websocket.subscriptions_cap) +
        '<p class="note">' + esc(si.websocket.note) + "</p>" +
        "<h3>Allocation model this panel illustrates</h3><p>" + esc(si.allocator_note) + "</p>"
    );
  }

  function card(label, value, ctx, tone) {
    return (
      '<article class="card"><span>' +
      esc(label) +
      '</span><strong class="' +
      (tone || "") +
      '">' +
      esc(value) +
      '</strong><span class="ctx">' +
      esc(ctx) +
      "</span></article>"
    );
  }

  function meter(label, used, cap, valueText) {
    var pct = Math.max(0, Math.min(100, (used / cap) * 100));
    return (
      '<div class="meter-row"><span class="meter-label">' +
      esc(label) +
      '</span><span class="meter" aria-hidden="true"><span class="meter-fill" style="width:' +
      pct.toFixed(1) +
      '%"></span></span><span class="meter-value">' +
      esc(valueText) +
      " (fixture)</span></div>"
    );
  }

  /* ---- view 2 — per-worker drill-down ------------------------------------------- */

  var currentWorkerId = null;

  function renderWorkers() {
    var workers = FIX.workers.workers;
    if (!currentWorkerId) {
      currentWorkerId = workers[0].worker_id;
    }
    var chips = workers
      .map(function (w) {
        return (
          '<button type="button" class="chip" data-worker="' +
          esc(w.worker_id) +
          '" aria-pressed="' +
          (w.worker_id === currentWorkerId ? "true" : "false") +
          '">' +
          esc(w.worker_id) +
          " · " +
          esc(w.symbol) +
          " " +
          esc(w.timeframe) +
          " · " +
          esc(healthWord(w)) +
          "</button>"
        );
      })
      .join("");
    setHtml("wk-chips", chips);

    var chipsBox = document.getElementById("wk-chips");
    if (chipsBox && !chipsBox.dataset.wired) {
      chipsBox.dataset.wired = "1";
      chipsBox.addEventListener("click", function (ev) {
        var btn = ev.target.closest ? ev.target.closest(".chip") : null;
        if (!btn) {
          return;
        }
        currentWorkerId = btn.getAttribute("data-worker");
        renderWorkers();
      });
    }

    var w = null;
    for (var i = 0; i < workers.length; i++) {
      if (workers[i].worker_id === currentWorkerId) {
        w = workers[i];
      }
    }
    if (!w) {
      setHtml("wk-detail", '<p class="note">worker not found in fixtures</p>');
      return;
    }

    var tuple = [
      ["worker_id", w.worker_id, "Surrogate identifier. Unique within a deployment for all time, including retired workers; never reused. The only field displayed or logged as the worker name by default."],
      ["strategy_id", w.strategy_id, "The frozen, approved strategy package this worker executes."],
      ["symbol", w.symbol, "Normalized uppercase instrument symbol."],
      ["timeframe", w.timeframe, "Bar timeframe. A worker is one strategy+symbol+timeframe(+config+partition) instance — the finest grain the architecture floats."],
      ["strategy_version", w.strategy_version, "Version of the frozen strategy package the worker runs."],
      ["config_hash", w.config_hash, "Deterministic content hash over the worker's frozen configuration preimage (strategy parameters + risk profile)."],
      ["account_label", w.account_label, "Logical label for the execution partition the worker trades through. NOT a credential, NOT an address, NOT a key — secrets never enter identity."]
    ];

    var blocksHtml = w.blocks.length
      ? w.blocks
          .map(function (b) {
            return (
              "<p>" +
              pill(b.reason_code, "red") +
              ' <span class="note">' +
              esc(b.source) +
              (b.guardian_tier ? " · Guardian " + esc(tierName(FIX.workers.guardian, b.guardian_tier)) : "") +
              " · logged " +
              esc(b.logged_ts) +
              "</span><br>" +
              esc(b.detail) +
              (b.scope ? "<br><span class=\"note\">Scope: " + esc(b.scope) + "</span>" : "") +
              (b.lift ? "<br><span class=\"note\">" + esc(b.lift) + "</span>" : "") +
              "</p>"
            );
          })
          .join("")
      : '<p>' + pill("NO BLOCKS — ENTRIES OPEN", "green") + '</p><p class="note">Fail-closed rules still apply: if this worker cannot evaluate its own risk or evidence, the default is no new entries.</p>';

    var p = w.position;
    var posLines =
      p.side === "FLAT"
        ? '<p>FLAT — no open position (fixture).</p>'
        : "<p>" +
          pill(p.side, p.side === "LONG" ? "green" : "amber") +
          " " +
          fixed(p.qty, 3) +
          " @ avg " +
          fixed(p.avg_entry, 2) +
          " · mark " +
          fixed(p.mark, 2) +
          " · unrealized " +
          signed(unrealized(w), 2) +
          " USDC</p>";

    setHtml(
      "wk-detail",
      panel(
        "Worker identity tuple (seven immutable fields)",
        "FIXTURE · P1 A.1 vocabulary",
        "",
        "<table><thead><tr><th>Field</th><th>Value</th><th>Meaning</th></tr></thead><tbody>" +
          tuple
            .map(function (row) {
              return '<tr><td class="mono">' + esc(row[0]) + '</td><td class="mono">' + esc(row[1]) + "</td><td>" + esc(row[2]) + "</td></tr>";
            })
            .join("") +
          "</tbody></table>" +
          '<p class="note">All seven fields are immutable for the worker\'s lifetime. Any change — new strategy version, edited config, symbol/timeframe change, account relabel — means retire this worker and create a successor with a NEW worker_id. A successor may record a lineage link for reporting only; it never inherits identity, open reservations, or ledger continuity.</p>'
      ) +
        panel(
          "Health & freshness",
          "FIXTURE · window state is evidence-derived",
          "",
          "<p>" +
            pill("WINDOW: " + w.health.window_state, windowTone(w.health.window_state)) +
            " " +
            pill("SCENARIO: " + w.scenario, w.scenario === "healthy" ? "green" : "amber") +
            "</p>" +
            "<ul><li>" +
            esc(w.health.window_basis) +
            "</li><li>Last persisted evidence: " +
            esc(w.health.last_evidence_ts) +
            " (" +
            ageText(w.health.last_evidence_ts, asOf()) +
            ")</li><li>Last bar: " +
            esc(w.health.last_bar_ts) +
            " (" +
            ageText(w.health.last_bar_ts, asOf()) +
            ")</li><li>Working orders: " +
            w.orders_working +
            " — " +
            esc(w.orders_working_note) +
            "</li></ul>"
        ) +
        panel(
          "Block reasons (veto & fail-closed vocabulary)",
          "FIXTURE · Guardian tiers per P1 A.3",
          "",
          blocksHtml +
            "<h3>Vocabulary</h3><ul>" +
            FIX.workers.guardian.veto_tiers
              .map(function (t) {
                return "<li>" + pill("TIER " + t.tier + " · " + t.name, t.tier === 3 ? "red" : t.tier === 2 ? "amber" : "blue") + " — " + esc(t.description) + "</li>";
              })
              .join("") +
            "<li>" +
            pill("WORKER-LOCAL", "amber") +
            " — fail-closed rules owned by the worker itself (e.g. stale or unreadable evidence → no new entries; protective management continues).</li></ul>"
        ) +
        panel(
          "Position & per-worker ledger",
          "FIXTURE · ledger keyed by worker_id",
          "",
          posLines +
            "<ul><li>Realized today: " +
            signed(w.ledger.realized_pnl_today, 2) +
            " " +
            esc(w.ledger.currency) +
            "</li><li>" +
            esc(w.ledger.ledger_note) +
            "</li><li>Portfolio P&L is computed by summation ABOVE the workers (Guardian / dashboard), never by sharing one ledger.</li></ul>"
        ) +
        panel(
          "Account label",
          "FIXTURE · logical partition, not a credential",
          "",
          "<p>account_label = <span class=\"mono\">" +
            esc(w.account_label) +
            "</span></p><ul><li>A logical label for the execution partition this worker trades through — a subaccount slot OR a virtual-book partition. It is not a credential, not an address, not a key; secrets never enter identity.</li><li>Default V2 design branch: a single account with internal partitioning (virtual books). The subaccount topology is the upgrade branch, conditional on separately established account eligibility.</li><li>Same-symbol concurrency within one account partition remains CLOSED — two active workers may share strategy+symbol+timeframe only under different account_labels, and that lever is gated closed today.</li></ul>"
        )
    );
  }

  function panel(title, truthLabel, tone, bodyHtml) {
    return (
      '<section class="panel"><div class="panel-head"><h2>' +
      esc(title) +
      "</h2>" +
      truth(truthLabel, tone) +
      "</div>" +
      bodyHtml +
      "</section>"
    );
  }

  /* ---- view 3 — market context ------------------------------------------------------ */

  function renderMarket() {
    var mc = FIX.market_context;
    var cardsHtml = mc.symbols
      .map(function (s) {
        return (
          '<article class="card"><span>' +
          esc(s.symbol) +
          " · last</span><strong>" +
          fixed(s.last, 2) +
          '</strong><span class="ctx">24h ' +
          esc(signed(s.change_24h_pct, 1) + "%") +
          " · range " +
          fixed(s.range_24h[0], 1) +
          " – " +
          fixed(s.range_24h[1], 1) +
          "</span><span class=\"ctx\">vol band: " +
          esc(s.realized_vol_band) +
          " · " +
          esc(s.trend_context) +
          "</span><span class=\"ctx\">" +
          esc(s.fixture_note) +
          "</span>"
        );
      })
      .join("");
    setHtml(
      "mc-body",
      panel(
        "Context statement",
        "CONTEXT · NON-ACTIONABLE · FIXTURE",
        "violet",
        "<p>" + esc(mc.meta.non_actionable) + "</p><p class=\"note\">" + esc(mc.meta.no_signal_note) + "</p>"
      ) +
        '<section class="panel"><div class="panel-head"><h2>Symbols in view</h2>' +
        truth("CONTEXT · FIXTURE", "violet") +
        '</div><div class="grid" style="margin-bottom:0">' +
        cardsHtml +
        "</div></section>" +
        panel(
          "Session notes",
          "CONTEXT · FIXTURE",
          "violet",
          "<ul>" + mc.session_notes.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") + "</ul>" +
            '<p class="note">Fixture as-of ' +
            esc(mc.meta.as_of) +
            ". " +
            esc(mc.meta.data_nature) +
            "</p>"
        )
    );
  }

  /* ---- view 4 — desired / accepted / exchange-truth ---------------------------------- */

  function renderLayers() {
    var li = FIX.intents;

    var legend = li.layers
      .map(function (layer) {
        return (
          '<div class="layer-col l' +
          layer.n +
          '"><span class="who">LAYER ' +
          layer.n +
          " · " +
          esc(layer.name) +
          " — owner: " +
          esc(layer.owner) +
          "</span>" +
          '<div class="vocab">' +
          layer.states
            .map(function (st) {
              var tone =
                layer.n === 1 ? desiredTone(st) : layer.n === 2 ? acceptedTone(st) : actualTone(st);
              return pill(st, tone);
            })
            .join("") +
          "</div>" +
          '<p class="why">' +
          esc(layer.state_note) +
          "</p>" +
          "<h3>Never contains</h3>" +
          '<p class="why">' +
          esc(layer.never_contains) +
          "</p></div>"
        );
      })
      .join("");

    var lanes = li.intents
      .map(function (it) {
        function col(n, cls, who, state, note, tone) {
          return (
            '<div class="layer-col ' +
            cls +
            '"><span class="who">' +
            who +
            "</span>" +
            '<div class="state">' +
            pill(state, tone) +
            "</div>" +
            '<p class="why">' +
            esc(note) +
            "</p></div>"
          );
        }
        return (
          '<article class="swimlane"><div class="swim-head"><span class="swim-action">' +
          esc(it.action) +
          " " +
          pill(it.kind, it.kind === "ENTRY" ? "blue" : "violet") +
          " " +
          pill(it.worker_id, "") +
          '</span><span class="swim-id">' +
          esc(it.intent_id) +
          " · " +
          esc(it.ts) +
          " (" +
          ageText(it.ts, li.meta.as_of) +
          ")</span></div>" +
          '<div class="layer-cols">' +
          col(1, "l1", "LAYER 1 · DESIRED — MTC strategy engine", it.desired.state, it.desired.note, desiredTone(it.desired.state)) +
          col(2, "l2", "LAYER 2 · ACCEPTED / REJECTED — Bridge", it.accepted.state, it.accepted.note, acceptedTone(it.accepted.state)) +
          col(3, "l3", "LAYER 3 · ACTUAL — exchange, recorded & reconciled by the Bridge", it.actual.state, it.actual.note, actualTone(it.actual.state)) +
          "</div></article>"
        );
      })
      .join("");

    setHtml(
      "ly-body",
      '<section class="panel"><div class="panel-head"><h2>The three layers</h2>' +
        truth("FIXTURE · P2 section 5 vocabulary", "") +
        '</div><div class="layer-cols">' +
        legend +
        "</div></section>" +
        '<section class="panel"><div class="panel-head"><h2>Intent stream</h2>' +
        truth("FIXTURE · synthetic intent history", "") +
        "</div>" +
        lanes +
        "</section>" +
        panel(
          "Cross-layer invariants this layout keeps visible",
          "FIXTURE · P2 section 5.2",
          "",
          "<ul>" + li.invariants.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") + "</ul>" +
            '<p class="note">' +
            esc(li.meta.required_fields_note) +
            "</p>"
        )
    );
  }

  /* ---- view 5 — phone monitor ---------------------------------------------------------- */

  function renderPhone() {
    var ws = FIX.workers;
    var workers = ws.workers;
    var guardian = ws.guardian;
    var intents = FIX.intents.intents;
    var mc = FIX.market_context;

    var healthy = workers.filter(function (w) { return !w.blocks.length; }).length;
    var blocked = workers.length - healthy;

    var vetoes = 0;
    var unknowns = 0;
    var partials = 0;
    intents.forEach(function (it) {
      if (it.accepted.state.indexOf("REJECTED") === 0) {
        vetoes++;
      }
      if (it.actual.state === "UNKNOWN_SUBMISSION") {
        unknowns++;
      }
      if (it.actual.state === "PARTIALLY_FILLED") {
        partials++;
      }
    });

    var workerCards = workers
      .map(function (w) {
        var block = w.blocks.length
          ? '<span class="line">' + esc(w.blocks[0].reason_code) + " — " + esc(w.blocks[0].source) + "</span>"
          : '<span class="line">no blocks — entries open</span>';
        return (
          '<div class="phone-card"><div class="row"><span class="title mono">' +
          esc(w.worker_id) +
          "</span>" +
          pill(w.health.window_state, windowTone(w.health.window_state)) +
          (w.blocks.length ? pill("BLOCKED", "red") : pill("OPEN", "green")) +
          "</div>" +
          '<span class="line">' +
          esc(w.strategy_id) +
          " · " +
          esc(w.symbol) +
          " " +
          esc(w.timeframe) +
          " · " +
          esc(w.account_label) +
          "</span>" +
          '<span class="line">last bar ' +
          ageText(w.health.last_bar_ts, asOf()) +
          " · realized " +
          signed(w.ledger.realized_pnl_today, 2) +
          " USDC</span>" +
          block +
          "</div>"
        );
      })
      .join("");

    var marketLine = mc.symbols
      .map(function (s) {
        return esc(s.symbol) + " " + fixed(s.last, 2) + " (" + esc(signed(s.change_24h_pct, 1)) + "%)";
      })
      .join(" · ");

    setHtml(
      "ph-body",
      '<div class="phone-wrap"><div class="phone-frame"><div class="phone-screen">' +
        '<div class="phone-top"><span class="phone-title">Bridge V2 monitor</span>' +
        pill("FIXTURE", "violet") +
        "</div>" +
        '<div class="phone-banner">READ-ONLY · fixture data · controls nothing</div>' +
        '<div class="phone-card"><div class="row"><span class="title">Workers</span>' +
        pill(healthy + " OPEN", "green") +
        pill(blocked + " BLOCKED", "red") +
        "</div>" +
        '<span class="line">entries-blocked workers still manage and protect existing positions (exits continue)</span></div>' +
        workerCards +
        '<div class="phone-card"><div class="row"><span class="title">Guardian</span>' +
        pill(guardian.state, "blue") +
        pill("HALT " + (guardian.global_halt ? "ON" : "OFF"), guardian.global_halt ? "red" : "green") +
        "</div>" +
        '<span class="line">gross exposure input ' +
        fixed(guardian.inputs.gross_exposure_pct, 1) +
        "% (fixture) · snapshot " +
        ageText(guardian.snapshot_ts, asOf()) +
        "</span>" +
        '<span class="line">cannot evaluate → no new entries (fail-closed, no bypass)</span></div>' +
        '<div class="phone-card"><div class="row"><span class="title">Three layers (quick)</span></div>' +
        '<span class="line">rejected intents: ' +
        vetoes +
        " · unknown submissions: " +
        unknowns +
        " · partially filled: " +
        partials +
        "</span>" +
        '<span class="line">desired ≠ accepted ≠ actual — kept visibly separate</span></div>' +
        '<div class="phone-card"><div class="row"><span class="title">Market (context only)</span>' +
        truth("NON-ACTIONABLE", "violet") +
        "</div>" +
        '<span class="line">' +
        marketLine +
        "</span></div>" +
        '<div class="phone-foot">fixture as-of ' +
        esc(asOf()) +
        " · no network · no controls</div>" +
        "</div></div></div>"
    );
  }

  /* ---- missing-fixture guard ---------------------------------------------------------- */

  function renderFailure() {
    var msg =
      '<section class="panel"><div class="panel-head"><h2>Fixtures unavailable</h2>' +
      truth("ERROR", "red") +
      "</div>" +
      "<p>window.FIXTURES did not load. Expected <span class=\"mono\">fixtures/data.js</span> next to " +
      "<span class=\"mono\">index.html</span>. This page has no network capability by design — it cannot fetch anything.</p></section>";
    ["ov-cards", "ov-workers", "wk-detail", "mc-body", "ly-body", "ph-body"].forEach(function (id) {
      setHtml(id, msg);
    });
  }

  /* ---- tabs ------------------------------------------------------------------------------- */

  function wireTabs() {
    var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          t.setAttribute("aria-selected", t === tab ? "true" : "false");
        });
        var name = tab.getAttribute("data-view");
        Array.prototype.slice.call(document.querySelectorAll(".view")).forEach(function (view) {
          view.classList.toggle("active", view.id === "view-" + name);
        });
      });
    });
  }

  /* ---- boot --------------------------------------------------------------------------------- */

  wireTabs();

  if (!FIX || !FIX.workers || !FIX.intents || !FIX.market_context) {
    renderFailure();
    return;
  }

  renderOverview();
  renderWorkers();
  renderMarket();
  renderLayers();
  renderPhone();
})();

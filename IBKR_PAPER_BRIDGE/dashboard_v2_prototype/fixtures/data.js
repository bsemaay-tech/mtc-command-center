/* Generated content: mirrors fixtures/workers.json, fixtures/intents.json and
 * fixtures/market_context.json. Regenerate with:
 *     python fixtures/build_data_js.py
 * (hand-mirrored in this increment because script execution was not
 *  permitted in the implementer sandbox; the Lead's executed check should
 *  re-run the build script and diff to confirm the mirror is exact.)
 * window.FIXTURES is the single input of index.html; the page performs no
 * network access of any kind. */
window.FIXTURES = {
  "workers": {
    "meta": {
      "prototype": "IBKR Paper Bridge — Dashboard V2 read-only prototype (Package 3, T1)",
      "data_nature": "SYNTHETIC FIXTURE DATA. There is no live bridge, no exchange connection and no worker process behind these values. This file feeds a static prototype page only.",
      "as_of": "2026-08-18T02:40:00Z",
      "age_basis": "Every age shown on the page is computed relative to meta.as_of (a frozen fixture timestamp), never relative to wall-clock time.",
      "vocabulary_sources": "State vocabularies follow the accepted P1 contract pack (worker identity tuple, Guardian veto tiers) and P2 contract pack (three-layer state model). All figures are illustrative.",
      "worker_set": "Three synthetic workers: one healthy, one stale-feed, one Guardian-paused."
    },
    "workers": [
      {
        "worker_id": "wrk-7c01",
        "strategy_id": "keltner_trail_ema8",
        "symbol": "BTC",
        "timeframe": "15m",
        "strategy_version": "1.4.2",
        "config_hash": "9f21ab37c4d8e560",
        "account_label": "book-alpha",
        "scenario": "healthy",
        "health": {
          "window_state": "ACTIVE",
          "window_basis": "Derived from this worker's persisted evidence with the staleness rule applied — never an in-memory claim (docs/21 evidence-derived model).",
          "last_evidence_ts": "2026-08-18T02:37:12Z",
          "last_bar_ts": "2026-08-18T02:30:00Z"
        },
        "blocks": [],
        "position": {
          "side": "LONG",
          "qty": 0.028,
          "avg_entry": 60120.5,
          "mark": 60480.0
        },
        "orders_working": 2,
        "orders_working_note": "protective stop + take-profit bracket (fixture illustration)",
        "ledger": {
          "currency": "USDC",
          "realized_pnl_today": 24.6,
          "ledger_key": "wrk-7c01",
          "ledger_note": "Per-worker P&L ledger keyed by worker_id. Realized and unrealized attribution never crosses workers."
        }
      },
      {
        "worker_id": "wrk-9d42",
        "strategy_id": "keltner_trail_ema8",
        "symbol": "ETH",
        "timeframe": "1h",
        "strategy_version": "1.4.2",
        "config_hash": "5c88e0f1a2b749d3",
        "account_label": "book-alpha",
        "scenario": "stale-feed",
        "health": {
          "window_state": "STALE",
          "window_basis": "Evidence is older than the liveness staleness rule, so the window reports STALE — unreadable or stale evidence reports DOWN/STALE, never a fabricated active state (docs/21).",
          "last_evidence_ts": "2026-08-17T21:12:44Z",
          "last_bar_ts": "2026-08-17T21:00:00Z"
        },
        "blocks": [
          {
            "source": "Worker-local fail-closed rule",
            "guardian_tier": null,
            "reason_code": "BLOCKED:FEED_STALE",
            "detail": "Candle evidence for ETH 1h is hours old relative to fixture as_of. New entries are blocked fail-closed; protective management of any existing position continues.",
            "logged_ts": "2026-08-17T22:04:10Z",
            "lift": "Recovers automatically once fresh evidence is readable again (fixture narration only)."
          }
        ],
        "position": {
          "side": "FLAT",
          "qty": 0.0,
          "avg_entry": null,
          "mark": 2531.4
        },
        "orders_working": 0,
        "orders_working_note": "flat — no working orders (fixture illustration)",
        "ledger": {
          "currency": "USDC",
          "realized_pnl_today": -37.0,
          "ledger_key": "wrk-9d42",
          "ledger_note": "Per-worker P&L ledger keyed by worker_id. Realized and unrealized attribution never crosses workers."
        }
      },
      {
        "worker_id": "wrk-4b8e",
        "strategy_id": "donchian_breakout_v1",
        "symbol": "SOL",
        "timeframe": "4h",
        "strategy_version": "0.9.1",
        "config_hash": "e3d0c2a9964f1b75",
        "account_label": "book-beta",
        "scenario": "guardian-paused",
        "health": {
          "window_state": "ACTIVE",
          "window_basis": "Derived from this worker's persisted evidence with the staleness rule applied — never an in-memory claim (docs/21 evidence-derived model).",
          "last_evidence_ts": "2026-08-18T02:11:09Z",
          "last_bar_ts": "2026-08-18T00:00:00Z"
        },
        "blocks": [
          {
            "source": "Portfolio Guardian",
            "guardian_tier": 2,
            "reason_code": "REJECTED:GUARDIAN_VETO",
            "detail": "Per-worker pause: aggregate gross long exposure across correlated symbols (BTC book-alpha + SOL book-beta) exceeded the portfolio review level in the derived snapshot. Veto, not a mutation — the Guardian never resizes or rewrites the order.",
            "scope": "New entries only. The worker keeps managing and protecting its existing position; exits continue; books stay current.",
            "logged_ts": "2026-08-18T01:05:33Z",
            "lift": "Lifting a pause is an operator action, outside this prototype."
          }
        ],
        "position": {
          "side": "LONG",
          "qty": 18.5,
          "avg_entry": 138.9,
          "mark": 142.66
        },
        "orders_working": 1,
        "orders_working_note": "protective stop only — entries paused, exits live (fixture illustration)",
        "ledger": {
          "currency": "USDC",
          "realized_pnl_today": 0.0,
          "ledger_key": "wrk-4b8e",
          "ledger_note": "Per-worker P&L ledger keyed by worker_id. Realized and unrealized attribution never crosses workers."
        }
      }
    ],
    "guardian": {
      "state": "EVALUATING",
      "snapshot_ts": "2026-08-18T02:39:58Z",
      "snapshot_basis": "Derived snapshots from each worker's own books — never worker self-claims as sole truth (evidence-derived principle).",
      "global_halt": false,
      "position_note": "A Portfolio Guardian sits ABOVE the workers. Workers manage their own strategy; the Guardian manages the portfolio.",
      "veto_tiers": [
        {
          "tier": 1,
          "name": "PER-ORDER VETO",
          "description": "Refuse an individual worker's order intent before submission."
        },
        {
          "tier": 2,
          "name": "PER-WORKER PAUSE",
          "description": "Stop ONE worker from initiating new entries. That worker keeps managing and protecting existing positions — exits continue, books stay current."
        },
        {
          "tier": 3,
          "name": "GLOBAL HALT",
          "description": "Stop new entries across ALL workers (portfolio circuit breaker)."
        }
      ],
      "veto_domain_note": "Veto domain = risk-increasing actions (new entries, adds, risk-increasing order changes). Risk-reducing exits (stop-loss, take-profit, close) are OUTSIDE veto scope — a veto against an exit would increase the very quantities the Guardian exists to bound.",
      "mutate_note": "The Guardian vetoes but does not mutate: it never resizes an order, never rewrites a stop or quantity, never edits economic intent.",
      "fail_closed_note": "If the Guardian cannot evaluate (unreachable, missing or stale aggregate snapshot, broken worker-to-Guardian channel) the default is NO NEW ENTRIES. There is no silent Guardian-bypass mode. Guardian unavailability never blocks protective exits.",
      "thresholds_note": "All numeric thresholds and their calibration are unresolved and belong to a later owner-gated package. No numbers are frozen here — fixture values are illustrative only.",
      "inputs": {
        "gross_exposure_pct": 18.4,
        "gross_exposure_note": "Aggregate portfolio exposure — one of the sums the Guardian exists to bound (fixture value).",
        "concentration_note": "Concentration and correlation inputs across workers — fixture narration only."
      }
    },
    "shared_infrastructure": {
      "truth_label": "FIXTURE ILLUSTRATION ONLY — usage numbers are synthetic. The shared framing is real: these budgets are shared VPS-wide across ALL workers regardless of the worker-process boundary (P1 B.8 framing, P7 evidence).",
      "rest": {
        "ip_weight_limit_per_min": 1200,
        "fixture_used_weight": 322,
        "note": "IP-based 'aggregated weight limit of 1200 per minute' is shared across ALL workers on the VPS (P7 claim n, dump-marked verbatim sentence)."
      },
      "websocket": {
        "connections_cap": 10,
        "subscriptions_cap": 1000,
        "fixture_connections": 3,
        "fixture_subscriptions": 214,
        "note": "WebSocket caps (max 10 connections, 1000 subscriptions, 30 new connections/min, 2000 messages/min sent, 100 inflight posts) are shared per IP. P7 flags these figures as [E]-level page extraction only — no verbatim sentence preserved — and testnet parity is UNKNOWN (P7 claim r). This panel asserts nothing beyond that."
      },
      "allocator_note": "Required model: a CENTRAL allocator — one shared admission/token-bucket layer for REST weight and one connection/subscription registry for WebSocket, granting explicit per-worker budgets with a headroom policy and defined overload behavior (defer or reject, never silently exceed). No worker may hold its own independent connection-to-the-exchange budget (P1 B.8)."
    }
  },
  "intents": {
    "meta": {
      "view": "Desired / accepted / exchange-truth — three separate states (P2 contract pack, section 5)",
      "data_nature": "SYNTHETIC FIXTURE DATA — no intents were emitted, accepted or filled anywhere. This stream exists only to make the three layers visible side by side.",
      "as_of": "2026-08-18T02:40:00Z",
      "purpose": "Combining the three layers into one 'current order' value would hide exactly the divergence this view exists to expose. Each row keeps desired, accepted/rejected, and actual visibly separate.",
      "required_fields_note": "Required dashboard fields — desired, accepted/rejected, acknowledged, partially filled, actually closed — are kept visibly separate. 'Acknowledged' maps to layer-3 SUBMITTED/OPEN; 'partially filled' to layer-3 PARTIALLY_FILLED; 'actually closed' to layer-3 FILLED on a close."
    },
    "layers": [
      {
        "n": 1,
        "name": "DESIRED",
        "owner": "MTC strategy engine",
        "states": ["EMITTED", "EXPIRED", "SUPERSEDED"],
        "state_note": "EMITTED is the only non-terminal state; EXPIRED and SUPERSEDED are terminal. A later intent in the same lifecycle supersedes an unexecuted earlier one (e.g. a stop-update chain).",
        "never_contains": "Any claim about the exchange: no fill, no acknowledgment, no position fact. MTC simulated exits stay in this layer — an MTC simulated close is never proof of an exchange fill."
      },
      {
        "n": 2,
        "name": "ACCEPTED / REJECTED",
        "owner": "Bridge",
        "states": ["RECEIVED", "VALIDATING", "ACCEPTED (reserved durably)", "SUBMITTED", "REJECTED:<reason>", "BLOCKED_DUPLICATE", "IDENTITY_COLLISION"],
        "state_note": "Durable reservation follows the order-identity contract: the reservation is committed before any broker I/O; an exact duplicate intent+request becomes BLOCKED with no I/O; the same intent with a different request is an identity collision. A Guardian veto appears here as REJECTED:GUARDIAN_VETO — never a mutation.",
        "never_contains": "Fabricated fills; silently mutated quantities, SL, TP, or TP-leg allocation."
      },
      {
        "n": 3,
        "name": "ACTUAL",
        "owner": "Exchange (recorded and reconciled by the Bridge only)",
        "states": ["PENDING_NEW", "SUBMITTING", "SUBMITTED", "OPEN", "PARTIALLY_FILLED", "PENDING_CANCEL", "FILLED", "CANCELED", "REJECTED", "EXPIRED", "UNKNOWN_SUBMISSION"],
        "state_note": "Canonical order-state vocabulary with transitions only per the accepted transition table. Position actuals come from authoritative fills only. UNKNOWN_SUBMISSION is frozen pending reconciliation — never terminal, never blindly retried.",
        "never_contains": "Anything copied from layers 1 or 2."
      }
    ],
    "invariants": [
      "1 to 2: acceptance requires schema validity, freshness (expires_ts), a durable identity reservation, a recomputed quantity within validation tolerances, and envelope checks. Any failure is a terminal REJECTED:<reason> — nothing executes partially-valid.",
      "2 to 3: only ACCEPTED then SUBMITTED crosses into the exchange layer; from there only exchange observations move layer 3, through the accepted transition table.",
      "3 to lifecycle closure: a lifecycle (and its TP legs) closes ONLY from actual fills — never from a layer-1 simulated close.",
      "No layer copies another as fact: layer 1 never writes into layer 3, layer 2 never fabricates fills, layer 3 evidence never overwrites a layer-1 desired state. Divergence stays visible.",
      "Intent freshness is wall-clock and internal to layers 1-2. It is NOT monitoring-window state: window state stays derived from persisted evidence plus the liveness staleness rule, so a dead bridge can never present an intent stream as an active window."
    ],
    "intents": [
      {
        "intent_id": "intent-v1:3f9ac1d87e02b615",
        "kind": "ENTRY",
        "action": "ENTRY LONG 0.014 BTC (MKT)",
        "worker_id": "wrk-7c01",
        "ts": "2026-08-18T01:12:44Z",
        "desired": {
          "state": "EMITTED",
          "note": "Entry intent emitted by the strategy engine."
        },
        "accepted": {
          "state": "SUBMITTED",
          "note": "RECEIVED, VALIDATING, ACCEPTED (reserved durably before any broker I/O), then SUBMITTED."
        },
        "actual": {
          "state": "FILLED",
          "note": "Exchange truth: filled. Position actuals come from authoritative fills only."
        }
      },
      {
        "intent_id": "intent-v1:8c40be9135d7f2aa",
        "kind": "EXIT",
        "action": "STOP_UPDATE (trail step 1) — superseded",
        "worker_id": "wrk-7c01",
        "ts": "2026-08-18T01:55:02Z",
        "desired": {
          "state": "SUPERSEDED",
          "note": "A later stop update in the same lifecycle (higher update_seq) superseded this one before it executed."
        },
        "accepted": {
          "state": "—",
          "note": "Never accepted — superseded inside layer 1. Stale reordering cannot apply."
        },
        "actual": {
          "state": "—",
          "note": "No broker I/O for this intent."
        }
      },
      {
        "intent_id": "intent-v1:b1726f5a08cc43de",
        "kind": "EXIT",
        "action": "STOP_UPDATE (trail step 2, tighten-only)",
        "worker_id": "wrk-7c01",
        "ts": "2026-08-18T02:21:37Z",
        "desired": {
          "state": "EMITTED",
          "note": "The superseding stop update of the chain above."
        },
        "accepted": {
          "state": "SUBMITTED",
          "note": "Accepted: tighten-only respected (LONG: new stop at or above the current accepted stop — widening is forbidden)."
        },
        "actual": {
          "state": "OPEN",
          "note": "Native stop working at the exchange — 'acknowledged' in the required-fields vocabulary."
        }
      },
      {
        "intent_id": "intent-v1:57e0d3ba94c18f27",
        "kind": "ENTRY",
        "action": "ENTRY SHORT 1.2 ETH (MKT)",
        "worker_id": "wrk-9d42",
        "ts": "2026-08-17T22:07:51Z",
        "desired": {
          "state": "EXPIRED",
          "note": "Intent freshness is wall-clock: past expires_ts it is rejected rather than executed late."
        },
        "accepted": {
          "state": "REJECTED:FRESHNESS",
          "note": "Loud reject with reason — never a silent late execution."
        },
        "actual": {
          "state": "—",
          "note": "No broker I/O."
        }
      },
      {
        "intent_id": "intent-v1:d93b50c7ea124f80",
        "kind": "ENTRY",
        "action": "ENTRY LONG 6.0 SOL (MKT)",
        "worker_id": "wrk-4b8e",
        "ts": "2026-08-18T01:06:02Z",
        "desired": {
          "state": "EMITTED",
          "note": "Desired by the strategy engine — layer 1 stays EMITTED; the veto does not rewrite it."
        },
        "accepted": {
          "state": "REJECTED:GUARDIAN_VETO",
          "note": "Blocked by the active tier-2 per-worker pause on wrk-4b8e (new entries only, active since 01:05:33Z). A veto is never a mutation: no resize, no rewrite."
        },
        "actual": {
          "state": "—",
          "note": "No broker I/O — the veto happened before submission."
        }
      },
      {
        "intent_id": "intent-v1:0a61ce88f7b3d954",
        "kind": "EXIT",
        "action": "CLOSE_FULL 18.5 SOL",
        "worker_id": "wrk-4b8e",
        "ts": "2026-08-18T02:14:18Z",
        "desired": {
          "state": "EMITTED",
          "note": "Exit requested by the strategy — exits are outside veto scope, so the per-worker pause does not block it."
        },
        "accepted": {
          "state": "SUBMITTED",
          "note": "Accepted and submitted via the cancel/replace and safe-flatten path; reduce-only by construction."
        },
        "actual": {
          "state": "PARTIALLY_FILLED",
          "note": "Partially filled at the exchange. The lifecycle closes only on actual fill truth — the strategy's desired close alone closes nothing."
        }
      },
      {
        "intent_id": "intent-v1:c7f4a2190e8b56d3",
        "kind": "ENTRY",
        "action": "ENTRY LONG 0.010 BTC (add, entry_seq 2)",
        "worker_id": "wrk-7c01",
        "ts": "2026-08-18T02:33:09Z",
        "desired": {
          "state": "EMITTED",
          "note": "Add intent within an existing lifecycle (entry_seq 2, within declared max_entries)."
        },
        "accepted": {
          "state": "SUBMITTED",
          "note": "Accepted and submitted."
        },
        "actual": {
          "state": "UNKNOWN_SUBMISSION",
          "note": "Submission outcome not yet confirmed. Frozen pending reconciliation — never terminal, never blindly retried."
        }
      },
      {
        "intent_id": "intent-v1:3f9ac1d87e02b615 (duplicate delivery)",
        "kind": "ENTRY",
        "action": "Duplicate delivery of the first intent above",
        "worker_id": "wrk-7c01",
        "ts": "2026-08-18T02:38:40Z",
        "desired": {
          "state": "EMITTED",
          "note": "Same intent re-delivered — a retry must not become a second order."
        },
        "accepted": {
          "state": "BLOCKED_DUPLICATE",
          "note": "Exact duplicate intent+request becomes BLOCKED with no broker I/O."
        },
        "actual": {
          "state": "—",
          "note": "Unchanged — the original order's exchange truth stays with the original intent row above."
        }
      }
    ]
  },
  "market_context": {
    "meta": {
      "view": "Market Context — context-only page",
      "data_nature": "SYNTHETIC FIXTURE DATA — no market data feed exists behind these numbers.",
      "as_of": "2026-08-18T02:40:00Z",
      "non_actionable": "CONTEXT ONLY — NON-ACTIONABLE. This page is informational for the operator. It feeds no decision path, emits no signal, and has no order path. The Bridge consumes approved frozen strategy packages; it does not develop strategies, and this page is not a strategy input.",
      "no_signal_note": "No entry/exit vocabulary, no direction recommendations and no confidence labels are shown on purpose — a context page must not read like a trade recommendation."
    },
    "symbols": [
      {
        "symbol": "BTC",
        "last": 60480.0,
        "change_24h_pct": 1.2,
        "range_24h": [59510.0, 60940.0],
        "realized_vol_band": "mid",
        "trend_context": "ranging inside a two-day bracket",
        "fixture_note": "synthetic value"
      },
      {
        "symbol": "ETH",
        "last": 2531.4,
        "change_24h_pct": -0.8,
        "range_24h": [2502.0, 2571.5],
        "realized_vol_band": "low",
        "trend_context": "drifting lower against BTC",
        "fixture_note": "synthetic value — the stale-feed worker shares this symbol; its feed problem is worker-side, not market-side"
      },
      {
        "symbol": "SOL",
        "last": 142.66,
        "change_24h_pct": 3.4,
        "range_24h": [137.2, 144.9],
        "realized_vol_band": "high",
        "trend_context": "extension day, broad participation",
        "fixture_note": "synthetic value"
      }
    ],
    "session_notes": [
      "Weekend liquidity profile (fixture narration).",
      "No scheduled macro releases in the next fixture window (fixture narration)."
    ]
  }
};

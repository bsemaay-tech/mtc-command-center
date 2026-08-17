# Bridge V2 — Dashboard Read-Only Prototype (Package 3, Tier T1)

A standalone, fixture-backed, **read-only** prototype of the proposed V2 multi-worker dashboard.
It exists to make the V2 design vocabulary visible — worker identity, Guardian veto tiers, the
desired/accepted/actual three-layer state model — before any real implementation is gated.

Scope source: `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE3_DASHBOARD_V2_PROTOTYPE_2026-08-18.md`.

## How to open

Open `index.html` directly in a browser (double-click, or `file://…/dashboard_v2_prototype/index.html`).
There is no server, no build step and no install. The page works offline by construction: all data is
embedded locally and no request of any kind leaves the page.

## What you should see

Five views, navigable with the tabs under the permanent banner:

1. **Overview** — aggregate execution summary: stat cards (worker counts, summed per-worker P&L,
   Guardian exposure input), the worker table (window state, feed age, entry status, block reasons),
   the Portfolio Guardian panel (state, active vetoes, the three veto tiers, fail-closed rules), and
   the shared-infrastructure panel (IP REST weight + WebSocket budget usage).
2. **Worker detail** — per-worker drill-down: the seven-field identity tuple with per-field meaning
   and the immutability rule, health & freshness (evidence-derived window state with ages), block
   reasons (Guardian veto tiers + worker-local fail-closed vocabulary), the per-worker ledger, and
   the account-label panel (logical partition, not a credential).
3. **Market context** — context-only symbol cards and session notes. Every panel is labeled
   CONTEXT / NON-ACTIONABLE; the page deliberately shows no signal, direction or recommendation
   vocabulary.
4. **Three layers** — the desired / accepted / exchange-truth view: per-intent swim-lanes with three
   visibly separate columns (owner labeled on each), the state vocabulary of every layer, what each
   layer never contains, and the cross-layer invariants. The fixture stream includes the interesting
   divergences on purpose: a superseded stop update, a freshness reject, a Guardian veto, a partially
   filled close, an UNKNOWN_SUBMISSION frozen pending reconciliation, and a blocked duplicate
   delivery.
5. **Phone monitor** — the dedicated small-screen monitoring layout inside a 390 px frame (worker
   status chips, Guardian line, three-layer quick counts, market line). Monitoring only.

## Boundaries (all enforced, all verified by inspection)

- **Read-only.** The page controls nothing. There are no ARM, order, kill, disarm or config controls
  anywhere — not even disabled mock buttons. The only interactive elements are the view tabs and the
  worker-selector chips, which change what is *displayed*, never what anything *does*.
- **Fixture data only.** Every number is synthetic and rendered against a frozen fixture as-of time
  (`2026-08-18T02:40:00Z`). Ages are computed relative to that time, not wall clock, so the page never
  implies liveness.
- **No network.** No fetch, no XHR, no WebSocket, no EventSource, no external URLs, no CDN, no
  web fonts, no images. Fixtures load through a `<script>` tag so `file://` works without fetch.
- **Every panel carries a truth label** naming which state layer it displays (Layer 1 desired /
  Layer 2 accepted / Layer 3 actual) or that it is fixture-only / context-only. The footer carries the
  page-level truth & permission statement (the WP-D0 note of the Gate-1 record: documentation-level
  truth/permission contract for this increment).
- **Nothing outside this directory** was created or modified. The V1 dashboard in
  `IBKR_PAPER_BRIDGE/bridge/static/` was read as visual-language reference only.

## Fixtures

| File | Contents |
|---|---|
| `fixtures/workers.json` | Three synthetic workers — one healthy (`wrk-7c01` BTC 15m), one stale-feed (`wrk-9d42` ETH 1h, window STALE, `BLOCKED:FEED_STALE`), one Guardian-paused (`wrk-4b8e` SOL 4h, tier-2 per-worker pause, `REJECTED:GUARDIAN_VETO`) — plus the Guardian aggregate model (veto tiers, fail-closed notes) and the shared-infrastructure panel data. |
| `fixtures/intents.json` | The three layer definitions (owner, state vocabulary, "never contains") and the eight-intent synthetic stream used by view 4. |
| `fixtures/market_context.json` | Context-only symbol snapshots (BTC / ETH / SOL) and session notes. |
| `fixtures/data.js` | The loader actually consumed by `index.html`: assigns `window.FIXTURES` from the same content, so the page works from `file://`. |
| `fixtures/build_data_js.py` | Regenerates `data.js` from the three JSON files (validates them as JSON on the way). The JSON files are the canonical fixture source; `data.js` is generated output. |

Note on `data.js`: in this increment it was hand-mirrored because script execution was not permitted
in the implementer sandbox. To confirm the mirror is exact (or to refresh it after editing a JSON),
run `python fixtures/build_data_js.py` and check `git diff -- fixtures/data.js` is empty.

Files: `index.html`, `app.css`, `app.js`, `fixtures/*`, this README. Nothing else, nothing outside.

## Vocabulary provenance

- Worker identity tuple (7 fields) and Guardian veto tiers (per-order veto / per-worker pause /
  global halt), plus veto-not-mutate and fail-closed semantics: accepted P1 architecture contract pack.
- Desired / accepted / actual three-layer model, layer owners, state vocabularies and invariants:
  accepted P2 MTC integration contract pack (§5).
- Shared IP/WS budget framing and its evidence-level caveats ([E]-level WS figures, testnet parity
  UNKNOWN): P7 exchange re-verification record — used for fixture realism only; nothing is asserted
  beyond it.
- Visual language (dark panel/border/pill vocabulary): the frozen V1 dashboard surface, reference
  only.

This prototype activates nothing, wires nothing, and authorizes nothing. It is Tier T1 display work.

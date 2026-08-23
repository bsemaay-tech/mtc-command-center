# Open-Source Trading Dashboards & Operator UIs — Reuse-First Survey

**Ticket:** #98 ("Research: open-source trading dashboards and operator UIs — reuse-first survey")
**Map:** #95 (Execution Dashboard & Interactive Trading Chart), first research ticket per the owner's standing REUSE-FIRST rule.
**Date:** 2026-08-23
**Scope note:** This is a shortlist with recommendation-flavored verdicts (adopt / adapt / avoid), as the ticket explicitly asks for — unlike the pure "facts only" research tickets elsewhere in this map. The verdicts are inputs for this map's grilling tickets, not a binding decision themselves (D-12: a decision is never an authorization).
**Method:** Read-only public research only — GitHub public API/metadata (`gh api`, unauthenticated read scope), project docs sites, and public source files fetched over HTTPS. No signups, no wallet connections, no authenticated exchange/venue calls, nothing installed or run locally.
**Existing stack context (read from this repo, for "plain-web-stack fit" scoring):** `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/` today is a **zero-build vanilla JS SPA** (`app.js`, `index.html`, `styles.css` — no framework, no bundler, no `package.json`) over a Python read-only API (`apps/api/mcc_readonly`). Its own header comment states it is explicitly **read-only: "no run-trigger, write-back, or trading logic lives here."** This is the research-domain dashboard (map 3's territory), not the execution dashboard this map owns — but it is the closest existing precedent for "our plain-web-stack," so every candidate below is scored against a zero-build vanilla-JS baseline, not against an assumed React/Vue toolchain. That baseline is not itself a ratified constraint for the execution dashboard (this map hasn't decided a stack yet) — it is just the nearest fact on the ground.

---

## Top-line recommendation (read this first)

1. **No complete open-source dashboard should be adopted wholesale.** Every complete candidate found is either (a) built for a different backend shape (an exchange-connected bot's own order engine, or a blockchain wallet/RPC), or (b) license-encumbered in a way that makes forking risky, or (c) both. None of them natively models "strategy intent vs authorized action vs exchange reality" as three distinct things — they mostly collapse (a) and (b) into one bot-internal concept.
2. **Freqtrade + FreqUI is the strongest single reference** — not to fork, but to copy the *pattern*: its `Trade` object already separates requested/intent fields, an `orders[]` authorization-trail array, and filled/exchange-state fields (see Cross-cutting section). Its control surface (`stopbuy`, `forceexit`, a dedicated confirm-dialog component) is the closest found analogue to ARM/DISARM/FLATTEN. **Verdict: study closely, adapt the data-model shape and control-surface UX, do not fork the code** (GPL-3.0, Vue+PrimeVue — stack mismatch against the vanilla baseline).
3. **For the component layer, adopt small, permissively-licensed pieces** (TanStack Table/Query, a confirm-dialog pattern) rather than any all-in-one framework — this fits the zero-build precedent and avoids the licensing tangles found in the "complete UI" class.
4. **The perp-DEX frontends (GMX, dYdX, Vertex, Kwenta/Synthetix) are useful only as UX references**, not as code — their licenses are hostile to reuse (Business Source License, custom AGPL, or unlicensed snapshots) and their whole data model assumes on-chain wallet/RPC truth, not a centralized bridge/exchange.

---

## Class (a): Complete operator dashboards / trading UIs

### A1. Freqtrade + FreqUI — **ADAPT (pattern-level), do not fork**

- **What it is:** Freqtrade is a Python crypto trading bot; FreqUI (`freqtrade/frequi`) is its separate Vue.js + PrimeVue web frontend, talking to Freqtrade's REST API.
- **License:** GPL-3.0 for both `freqtrade/freqtrade` and `freqtrade/frequi`. Source: `gh api repos/freqtrade/freqtrade` and `repos/freqtrade/frequi`, `license.spdx_id` = `GPL-3.0` for both (fetched 2026-08-23). GPL only triggers on *distributing* modified code, not on running it privately — pure self-hosted internal use carries no obligation to publish changes. Copying substantial FreqUI/Freqtrade source into our own codebase would pull that codebase's relevant portion under GPL if ever distributed; needs owner/legal review before any literal code copy, not before study.
- **Maintenance health:** Very active. `freqtrade/freqtrade`: 53,549 stars, 11,130 forks, pushed 2026-08-23T14:06Z (same day as this research), 29 open issues (low, well-triaged). `freqtrade/frequi`: 1,051 stars, pushed 2026-08-23T05:53Z. Both fetched via `gh api` 2026-08-23.
- **Self-hostable offline:** Yes — Python backend + static Vue build, runs entirely on your own infrastructure. (It talks outward to a crypto exchange for its own trading; that part is irrelevant to us since we'd only reuse UI/data-model patterns, not its exchange connectivity.)
- **Plain-web-stack fit:** Weak as a literal dependency — Vue 3 + PrimeVue + a build toolchain (npm/Vite) vs. today's zero-build vanilla-JS baseline. Fine as a *pattern* reference; poor as a drop-in dependency.
- **Data-model fit to the three-truth display:** **Best match found.** Its `Trade` object schema (fetched from `https://www.freqtrade.io/en/stable/trade-object/`, 2026-08-23) already separates the three layers we need:
  - **Strategy intent:** `enter_tag`, `strategy`, `timeframe`, `open_rate_requested`, `close_rate_requested`, `amount_requested`.
  - **Authorized action (orders sent):** `orders` (an array of individual order records), `open_orders`, `open_sl_orders`, `nr_of_successful_entries`, `nr_of_successful_exits`, `fully_canceled_entry_order_count`, `canceled_exit_order_count`.
  - **Exchange reality (filled/actual state):** `open_rate`, `close_rate`, `amount`, `is_open`, `has_open_position`, `stop_loss`, `stoploss_or_liquidation`, `liquidation_price`, `max_rate`, `min_rate`.
  This is not an exact match to "strategy intent vs authorized action vs exchange reality" (Freqtrade's "strategy" and "bot" are the same actor, so it doesn't need a separate authorization layer the way a kernel→Guardian→exchange chain does) — but the field-level separation of *requested* vs *orders-in-flight* vs *filled/realized* is the closest structural precedent found anywhere in this survey.
- **Safety-control patterns (ARM/DISARM/KILL/FLATTEN):**
  - `forceexit` = **FLATTEN**-equivalent: closes a specific open trade; the docs (`https://www.freqtrade.io/en/stable/freq-ui/`, fetched 2026-08-23) state the trade page lets you "force trade entries and exits," including a partial-forceexit form leaving amount blank to exit fully.
  - `/stopbuy` = **DISARM**-equivalent (partial): per a GitHub search-verified source read (`https://www.freqtrade.io/en/stable/...` cross-referenced with GitHub issue #1607 and PR #11539, fetched 2026-08-23), `/stopbuy` stops new entries while letting existing open trades continue being managed — i.e. "stop opening new risk, don't touch what's already live." A dedicated `/pause` command (functionally identical to `/stopbuy`) was in active development as of PR #11539, confirming this exact staged-safety pattern (pause new entries without disturbing live positions) is a recognized, independently-arrived-at need in this space — it matches this map's own ratified "STAGED SAFETY-FIRST" stance.
  - **Confirmation dialog before destructive action — confirmed in source.** A GitHub code search over `freqtrade/frequi` (via `gh api search/code`, 2026-08-23) turned up `src/components/general/ConfirmDialogBox.vue` used alongside `src/components/ftbot/ForceExitForm.vue`, `TradeActions.vue`, and `TradeActionsPopover.vue` — i.e. force-exit actions route through a shared, reusable confirm-dialog component rather than firing immediately on click. This is a directly transferable UX pattern regardless of stack.
- **Mobile story:** Weak/unconfirmed. The `freq-ui` docs page and the `frequi` README (fetched 2026-08-23) contain no mention of PWA, responsive layout, or a mobile app. A broader search found no evidence of a maintained mobile-specific build; GitHub issue #12165 ("Multi-Phase Plan to Enhance Freqtrade's User-Friendliness") discusses UX improvements generally but not mobile specifically. Treat mobile as **not solved** by this project.
- **What it would save vs custom:** A validated field taxonomy for the three-truth model (rename, don't redesign, the intent/orders/reality split), a proven staged-safety command pair (pause-new-entries vs close-existing), and a reusable confirm-before-destructive-action component pattern. It would not save any actual code given the stack mismatch and GPL boundary.

### A2. Hummingbot + Hummingbot Dashboard — **ADAPT (selectively), maintenance caution on the dashboard specifically**

- **What it is:** Hummingbot (`hummingbot/hummingbot`) is a market-making/HFT bot engine; `hummingbot/dashboard` is a separate Streamlit-based web app for creating, backtesting, deploying, and orchestrating Hummingbot instances (description via `gh api`, fetched 2026-08-23).
- **License:** Apache-2.0 for both repos (`gh api repos/hummingbot/hummingbot` and `repos/hummingbot/dashboard`, fetched 2026-08-23) — the most permissive license found among all complete-dashboard candidates in this survey; safe to copy code from with attribution, no copyleft.
- **Maintenance health:** Core engine very active — 19,570 stars, pushed 2026-08-22T03:17Z. The **dashboard repo is comparatively stale**: 364 stars, last pushed **2025-10-27T16:41Z**, roughly 10 months before this survey date — a real maintenance-lag flag if the dashboard specifically were ever a dependency.
- **Self-hostable offline:** Yes, Docker-Compose-based per its own docs (`hummingbot.org/dashboard/`, referenced in search results 2026-08-23); needs its own backend services (an MQTT broker for bot communication per the docs), which is more infrastructure than the current zero-build vanilla-JS setup carries.
- **Plain-web-stack fit:** Poor — Streamlit is a Python-rendered reactive app framework, structurally unlike a static/vanilla frontend; would be a wholesale architecture adoption, not a component add.
- **Data-model fit:** Instance-level, not order-level — its control surface described in search results is "bot orchestration to deploy and manage multiple instances" and "one-click deployment," i.e. it starts/stops whole bot processes rather than showing a three-truth per-order/per-position ledger. Weaker fit than Freqtrade for this map's specific ask.
- **Safety-control patterns:** Not confirmed at the granularity this map needs (no per-position ARM/KILL/FLATTEN found in the material gathered — only whole-instance deploy/stop). Flag as **UNKNOWN at the per-order level** — would need a deeper source read to confirm or rule out finer-grained controls.
- **Mobile story:** Not addressed in gathered material.
- **What it would save vs custom:** The core Hummingbot engine's permissive license makes any of its Python control/data-model *code* (not just patterns) legally cheap to borrow if ever useful; the dashboard app itself is a weaker fit and a staler codebase — treat the dashboard as a UX reference only, not a dependency.

### A3. OctoBot — **AVOID as a UI dependency (reference only)**

- **What it is:** Python trading bot (`Drakkar-Software/OctoBot`) with a bundled web interface; a separate community "Octo UI2" exists as a Tentacle (plugin) extension.
- **License:** GPL-3.0 (confirmed via search result text and consistent with the GitHub repo description, 2026-08-23). Same internal-use-is-fine / distribution-triggers-copyleft profile as Freqtrade.
- **Maintenance health:** Active — 6,456 stars, 1,266 forks, pushed 2026-08-23T15:02Z (`gh api`, fetched 2026-08-23).
- **Findings:** Search results (2026-08-23) could not confirm the dashboard's underlying frontend framework (Vue was speculated, not verified) or a specific pause/kill-switch UI pattern beyond general "manage and automate trading strategies" language. The separate "Octo UI2" project is a plugin-architecture extension, adding integration complexity for a one-off pattern study.
- **Verdict rationale:** Freqtrade already supplies a stronger, better-documented, more source-verifiable version of the same pattern (Python bot + separate web UI, GPL-3.0). No reason to also carry OctoBot's less-verified specifics forward — **avoid spending further research time here.**

### A4. Superalgos — **AVOID (different problem shape)**

- **What it is:** `Superalgos/Superalgos` — a visual, no-code strategy-builder and charting/data-mining platform with backtesting and multi-server deployment.
- **License:** Apache-2.0 (`gh api`, fetched 2026-08-23) — permissive.
- **Maintenance health:** Active — 5,620 stars, pushed 2026-08-23T03:36Z.
- **Verdict rationale:** Its own description frames it around visual strategy design, charting, and data-mining — i.e. the research/strategy-authoring domain, not an execution/operator dashboard with positions, orders, and ARM/KILL controls. That domain belongs to map 3 (explorer) per this map's own scope-neighbour note, not here. Noted for completeness; **out of this map's scope**, not evaluated further.

### A5. K / Krypto-trading-bot — **AVOID (stale, wrong shape)**

- **What it is:** `ctubio/Krypto-trading-bot`, a C++ market-making bot with a "fully featured web interface" (quoting/grid/order-history/position UI), per search results (2026-08-23).
- **License:** `license.spdx_id` = `NOASSERTION` via `gh api` (fetched 2026-08-23) — GitHub could not confidently classify the declared license; would need a manual LICENSE-file read before any reuse, and given the staleness below this wasn't pursued further.
- **Maintenance health:** Stale — last pushed 2024-12-15, roughly 20 months before this survey. 3,706 stars (legacy popularity), 64 open issues.
- **Verdict rationale:** Abandoned-in-practice and a C++/market-making shape that doesn't match this system. **Avoid.**

### A6. Perp-DEX web frontends (GMX, dYdX v4, Vertex, Kwenta/Synthetix) — **AVOID direct reuse; UX-pattern reference only**

These share one structural problem for our purposes: their "exchange reality" truth source is **on-chain state read via wallet/RPC**, not a centralized bridge/exchange API — a fundamentally different backend shape from this system's KVM2/bridge execution domain. They also all carry license or maintenance obstacles:

| Project | License found | Maintenance | Source |
|---|---|---|---|
| `gmx-io/gmx-interface` | **Business Source License 1.1** (source-available, not OSI-open; restricts competing/production use until a future change date) | Active, pushed 2026-08-21T18:48Z | Raw `LICENSE` file fetched 2026-08-23; `gh api` for stars/push |
| `dydxprotocol/v4-web` | **AGPL-3.0 with a dYdX-specific rider** — grants rights "subject to your compliance with applicable law and the v4 Terms of Use," and rights terminate automatically on any applicable-law violation | Active, pushed 2026-07-31T13:08Z | Raw `LICENSE` file fetched 2026-08-23 |
| `vertex-protocol/vertex-dashboard`, `vertex-web-monorepo-snapshot` | **No license file detected** (`license: null` via `gh api`) — default is all-rights-reserved | Stale — last pushed 2025-01-28 and 2025-04-26 respectively | `gh api search/repositories?q=org:vertex-protocol`, fetched 2026-08-23 |
| Kwenta | Kwenta was **acquired back by Synthetix and consolidated into "Synthetix Exchange"** in December 2024 (SIP-411, per `blog.synthetix.io` and `blockworks.co` coverage, fetched 2026-08-23); the original `Synthetixio/kwenta` GitHub repo is explicitly marked "**DEPRECATED. Please use: https://github.com/Kwenta/kwenta**" per its own README title (search result, 2026-08-23) | Product no longer exists in its original form | WebSearch results, 2026-08-23 |
| Drift (protocol-v2) | The `drift-labs` org's public repo is the on-chain program/SDK (`protocol-v2`, Apache-2.0, but note: `gh api` resolved this repo to `velocity-exchange/protocol-v2` — an apparent rename/fork situation worth a second look before citing further), **not** a separate open web-UI repo. No dedicated Drift trading-UI GitHub repo was found via org search. | N/A (UI not found as OSS) | `gh api search/repositories?q=org:drift-labs+ui`, empty result, 2026-08-23 |

- **Data-model fit:** Interesting as *reference*, not as code — each of these does display something close to a three-truth split in spirit (your signed-but-unconfirmed transaction = "authorized action," on-chain settled state = "exchange reality"), but it's wallet/blockchain-specific plumbing (nonce management, transaction confirmation polling, RPC state) that has no analogue in a centralized-exchange/bridge system.
- **Verdict:** **Avoid as code dependencies** (BSL and custom-AGPL both carry real legal exposure for anything beyond looking; the unlicensed Vertex snapshots are legally the most restrictive of all — no rights are granted by default). If a designer wants visual/UX inspiration for how a modern perp-trading position/order table looks and feels, these are fine to *look at in a browser*, not to clone.

---

## Class (b): Component stacks

Rather than one framework, the survey found a small set of permissively-licensed, independently-adoptable pieces that could each replace a slice of custom work without committing to a whole new stack — a better fit for the zero-build-vanilla-JS precedent than any single "complete dashboard" framework.

| Component | Project | License | Stars / last push (`gh api`, 2026-08-23) | Role it would fill | Verdict |
|---|---|---|---|---|---|
| Data tables (orders/positions grids) | TanStack Table | MIT | 28,366 / 2026-08-22 | Headless sortable/filterable table logic for the positions/orders/SL-TP grids, framework-agnostic (works with or without a UI framework) | **Adopt** |
| Data tables, alternative | AG Grid (Community edition) | MIT for the community packages (Enterprise packages are commercial — confirmed by reading the repo's own license breakdown, fetched 2026-08-23: "The following packages are MIT licensed: `@ag-grid-community/*`...") | 15,558 / 2026-08-23 | Same role, heavier/more batteries-included; watch the Enterprise-vs-Community package boundary if adopted | **Adopt (Community only)** |
| Server-state sync (positions/orders live data) | TanStack Query | MIT | 50,185 / 2026-08-23 | Polling/refetching/staleness handling for "freshness" — directly relevant to the map's freshness requirement | **Adopt** |
| Client state | Zustand | MIT | 58,595 / 2026-08-19 | Lightweight state store if/when the dashboard outgrows vanilla JS state | **Adopt (if/when a state library is wanted)** |
| UI primitives (buttons, dialogs, confirm modals) | shadcn/ui | MIT | 121,914 / 2026-08-23 | Copy-paste (not npm-dependency) component source — fits a no-framework-lock-in philosophy since you own the copied code | **Adopt** |
| Dashboard KPI/stat-card components | Tremor | Apache-2.0 | 3,575 / 2025-10-10 (stale — ~10 months) | Copy-paste dashboard building blocks (KPI cards, tables) | **Adapt with caution** (staleness flag) |
| Admin-panel scaffolding framework | Refine | MIT | 35,556 / 2026-06-05 | Headless React framework for data-heavy CRUD-style admin UIs | **Adapt if a React commitment is made**, not a fit for the current vanilla baseline as-is |
| Internal-tool / low-code app builder | Appsmith | Apache-2.0 | 40,727 / 2026-08-21 | Could rapidly assemble an ARM/KILL/FLATTEN control panel wired to internal APIs without hand-building forms | **Adapt-candidate** for a fast internal control panel, permissive license |
| Internal-tool / low-code app builder | Budibase | Core is GPLv3 overall, **but** its own licensing guide states verbatim: "The apps that you build with Budibase do not package any GPLv3 licensed code, thus do not fall under those restrictions" (raw `LICENSE` file, fetched 2026-08-23) | 28,239 / 2026-08-21 | Same role as Appsmith; the GPL boundary is explicitly scoped to the builder tool itself, not generated apps | **Adapt-candidate**, license risk is lower than it first appears |
| Internal-tool / low-code app builder | ToolJet | **AGPL-3.0** (`gh api`, fetched 2026-08-23) | 40,723 / 2026-08-23 | Same role again | **Avoid** relative to the two alternatives above — AGPL's network-copyleft clause is the least favorable of the three builder options for a self-hosted control surface, with no equivalent "generated apps are unencumbered" carve-out found |
| Monitoring/observability dashboard | Grafana | AGPL-3.0 | 76,361 / 2026-08-23 | Read-only telemetry panels (freshness, health, state-over-time) | **Adopt for pure read-only monitoring only, avoid for the control plane** — Grafana panels are fundamentally display/query surfaces; it has no native, mature "click this button to ARM/KILL" action model found in this research pass, and its AGPL license adds copyleft considerations for anything beyond running it unmodified |
| Status-page UX pattern reference | Uptime Kuma | MIT | 90,507 / 2026-08-23 | Not a trading tool at all — referenced only for its "fancy self-hosted monitoring" status-indicator visual language, which is relevant to "freshness" display design | **Reference only, not a dependency** |
| Terminal-style operator console | Textual (Python) | MIT | 37,012 / 2026-07-11 | A TUI framework whose own description states it can "run your apps in the terminal **and a web browser**" — i.e. one codebase serving both a true terminal operator console and a browser view, which maps well onto a "terminal-style UI" request | **Adopt-candidate** if a terminal-style operator surface is wanted alongside/instead of a web dashboard |
| Terminal-style operator console, alternative | Ink (Node/React-for-CLI) | MIT | 39,717 / 2026-08-12 | Same role, JS-ecosystem alternative to Textual | **Adopt-candidate**, pick one of Textual/Ink based on whether the backend language leans Python or Node |

---

## Cross-cutting findings

### Three-truth data-model fit, ranked
1. **Freqtrade `Trade` object** (Section A1) — closest found precedent for the intent/authorized-action/exchange-reality split, at the field level.
2. **Perp-DEX frontends** (Section A6) — conceptually similar (pending tx vs confirmed on-chain state) but wrong backend shape (blockchain, not centralized exchange/bridge) and license-encumbered.
3. Everything else surveyed either doesn't expose a three-layer model at all (most bot dashboards conflate "bot decided" and "exchange did it" into one status field) or wasn't verifiable from public docs within this research pass's scope.

### Safety-control (ARM/DISARM/KILL/FLATTEN) patterns found in the wild
- **Pause-new-without-touching-existing** is a recurring, independently-arrived-at pattern: Freqtrade's `/stopbuy` (and its in-progress `/pause` successor, PR #11539) does exactly this — new entries stop, open positions keep being managed. This directly echoes this map's own ratified "STAGED SAFETY-FIRST" stance (minimum dashboard = monitor + ARM/DISARM/KILL/FLATTEN; protective-order editing is a later stage).
- **Confirm-before-destructive-action as a reusable component** — Freqtrade/FreqUI's `ConfirmDialogBox.vue`, used by its force-exit flow, is a directly transferable UX pattern (a shared confirm-modal component gating any destructive control), independent of which frontend stack is eventually chosen.
- No project surveyed exposed a single-button, system-wide "KILL" (as opposed to per-trade `forceexit`) or a system-wide "FLATTEN all positions" control in the material gathered — this looks like a genuine gap this map will need to design, not something to borrow.

### Mobile story across candidates
Weak or unconfirmed everywhere surveyed. FreqUI: no PWA/mobile evidence found in its own docs or README. Hummingbot Dashboard, OctoBot, Superalgos: not addressed in the material gathered (would need deeper source reads to rule in/out). The internal-tool builders (Appsmith/Budibase/ToolJet) and Grafana are all responsive web apps by nature of their builder/observability role but none were confirmed to have a dedicated mobile app. **No candidate solves "mobile operator control" out of the box** — if remote/mobile ARM-KILL access is a hard requirement, this is custom work regardless of which reuse path is chosen.

### Maintenance-health snapshot (all fetched via `gh api`/raw source, 2026-08-23)
Actively maintained (pushed within the survey week): freqtrade/freqtrade, freqtrade/frequi, hummingbot/hummingbot, Drakkar-Software/OctoBot, Superalgos/Superalgos, gmx-io/gmx-interface, TanStack/table, TanStack/query, shadcn-ui/ui, pmndrs/zustand, ag-grid/ag-grid, ToolJet/ToolJet, appsmithorg/appsmith, budibase/budibase, grafana/grafana, louislam/uptime-kuma, vadimdemedes/ink.
Stale (last push materially predates this survey): hummingbot/dashboard (~10 months), Tremor (~10 months), Refine (~2.5 months, borderline), ctubio/Krypto-trading-bot (~20 months, effectively abandoned), vertex-protocol's dashboard repos (~7–19 months).

---

## Shortlist summary table

| # | Candidate | Class | License | Verdict | What it saves vs custom |
|---|---|---|---|---|---|
| 1 | Freqtrade + FreqUI | (a) complete | GPL-3.0 | **Adapt (pattern only)** | A validated three-truth-shaped field taxonomy; a staged pause-vs-flatten command pair matching our own ratified stance; a reusable confirm-before-destructive-action UX pattern |
| 2 | Hummingbot + Dashboard | (a) complete | Apache-2.0 | **Adapt (selectively; dashboard repo is stale)** | Permissively-licensed Python control code if ever needed; weaker three-truth fit (instance-level, not order-level) |
| 3 | OctoBot | (a) complete | GPL-3.0 | **Avoid** (Freqtrade already covers this pattern better-documented) | — |
| 4 | Superalgos | (a) complete | Apache-2.0 | **Avoid** (wrong domain — strategy-authoring, not execution ops; map 3's territory) | — |
| 5 | Krypto-trading-bot (K) | (a) complete | Unclear (`NOASSERTION`) | **Avoid** (stale ~20 months, wrong tech shape) | — |
| 6 | GMX / dYdX v4 / Vertex / Kwenta frontends | (a) complete | BSL / custom-AGPL / unlicensed / discontinued | **Avoid direct reuse; UX reference only** | Visual/UX inspiration for a modern position/order table; on-chain data model doesn't transfer |
| 7 | TanStack Table + Query | (b) component | MIT | **Adopt** | Table logic + live-data/staleness handling, hand-rolling both is real, avoidable work |
| 8 | AG Grid (Community) | (b) component | MIT (community pkgs) | **Adopt (as alternative to #7)** | Same as above, heavier/more built-in |
| 9 | Zustand | (b) component | MIT | **Adopt if/when needed** | Lightweight state store, tiny footprint |
| 10 | shadcn/ui | (b) component | MIT | **Adopt** | Copy-owned UI primitives incl. confirm-dialog patterns, no framework lock-in |
| 11 | Tremor | (b) component | Apache-2.0 | **Adapt with caution** (stale) | KPI/stat-card visual patterns |
| 12 | Refine | (b) component | MIT | **Adapt if React is adopted** | Admin-CRUD scaffolding, not a fit for the current vanilla baseline as-is |
| 13 | Appsmith | (b) component | Apache-2.0 | **Adapt-candidate** | Fast internal ARM/KILL control-panel assembly without hand-building forms |
| 14 | Budibase | (b) component | GPLv3 core / apps unencumbered | **Adapt-candidate** | Same as #13, license risk lower than headline license suggests |
| 15 | ToolJet | (b) component | AGPL-3.0 | **Avoid** (relative to #13/#14) | — |
| 16 | Grafana | (b) component | AGPL-3.0 | **Adopt for read-only monitoring only; avoid for control plane** | Telemetry/freshness panels, if that layer is ever split out |
| 17 | Uptime Kuma | (b) component | MIT | **Reference only** | Status-indicator visual language |
| 18 | Textual (Python TUI) | (b) component | MIT | **Adopt-candidate** | Terminal-style operator console, one codebase for terminal + browser |
| 19 | Ink (Node TUI) | (b) component | MIT | **Adopt-candidate** (alternative to #18) | Same role, JS-side |

---

## What stays custom regardless

- The three-truth data model itself (strategy intent / kernel→Guardian authorization / exchange reality) — no candidate found models a three-party authorization chain; Freqtrade's bot-is-both-strategist-and-executor shape is the closest analogue but still collapses two of our three layers into one.
- A system-wide KILL / FLATTEN-all control — not found as a shipped feature anywhere surveyed; per-position `forceexit` (Freqtrade) is the closest primitive, not the same thing.
- Mobile/remote operator access — not solved by any candidate.
- Integration with this system's specific backend (KVM2/bridge, Guardian, kernel) — inherently custom no matter what UI layer is chosen.

## Open questions for this map's grilling tickets
- Does the eventual execution dashboard commit to staying zero-build-vanilla-JS (matching `08_DASHBOARD_APP/apps/web`), or is a framework (React/Vue + build step) now in scope? That single decision determines whether items 7–12 above are realistic adopts or need re-scoring.
- Is an internal-tool builder (Appsmith/Budibase) an acceptable way to stand up the ARM/DISARM/KILL/FLATTEN control panel quickly, or does the safety-critical nature of those controls argue for hand-built, fully-audited code instead of a low-code builder's generated output? This is a real trade-off the research didn't resolve — flagging it rather than picking a side.
- Is a terminal-style operator console (Textual/Ink) wanted as a first-class surface, or only as a nice-to-have alongside a web dashboard? Changes whether items 18/19 are worth prototyping.

## Sources (primary, all fetched/queried 2026-08-23 unless noted)
- `gh api repos/<owner>/<repo>` for license/stars/forks/open_issues/pushed_at/archived — freqtrade/freqtrade, freqtrade/frequi, hummingbot/hummingbot, hummingbot/dashboard, Drakkar-Software/OctoBot, ctubio/Krypto-trading-bot, gmx-io/gmx-interface, drift-labs/protocol-v2 (resolved to velocity-exchange/protocol-v2), dydxprotocol/v4-web, refinedev/refine, tremorlabs/tremor, TanStack/table, TanStack/query, Textualize/textual, vadimdemedes/ink, jesse-ai/jesse, Superalgos/Superalgos, budibase/budibase, ToolJet/ToolJet, appsmithorg/appsmith, grafana/grafana, louislam/uptime-kuma, ag-grid/ag-grid, shadcn-ui/ui, pmndrs/zustand.
- `gh api search/repositories?q=...` for Kwenta/Drift/Vertex/Hyperliquid org and name searches.
- `gh api search/code?q=...repo:freqtrade/frequi` for `ConfirmDialogBox.vue` / `ForceExit` source-file locations.
- Raw `LICENSE` files fetched over HTTPS: `raw.githubusercontent.com/gmx-io/gmx-interface/master/LICENSE`, `raw.githubusercontent.com/dydxprotocol/v4-web/main/LICENSE`, `raw.githubusercontent.com/Budibase/budibase/master/LICENSE`, `raw.githubusercontent.com/ag-grid/ag-grid/latest/LICENSE.txt`.
- `https://www.freqtrade.io/en/stable/freq-ui/`, `https://www.freqtrade.io/en/stable/trade-object/`, `https://www.freqtrade.io/en/stable/rest-api/`, `raw.githubusercontent.com/freqtrade/frequi/main/README.md`.
- WebSearch results (queries logged in this research session) for: Hummingbot Dashboard overview and tech stack; OctoBot web UI/Octo UI2; Kwenta/Synthetix Exchange 2024 consolidation (`blog.synthetix.io`, `blockworks.co`, GitHub README for `Synthetixio/kwenta`); Refine/Tremor/AdminJS overviews; freqtrade `/stopbuy` behavior cross-referenced with GitHub issue #1607 and PR #11539.
- Local repo read (read-only, this worktree): `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`, `index.html`, `styles.css` and `apps/api/` directory listing, for the "existing plain-web-stack" baseline.
- Map context (read-only): `gh issue view 95` (parent map, for scope-neighbour and owner-stance context) and `gh issue view 98` (this ticket's question).

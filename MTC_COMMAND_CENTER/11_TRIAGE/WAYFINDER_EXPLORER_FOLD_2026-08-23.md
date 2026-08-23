# WAYFINDER EXPLORER FOLD — 2026-08-23 (map #78)

**Status:** owner-decision record and plan-amendment pass. Planning only — **implementation authorized: NO.** Per D-12, nothing here is an authorization: no viewer is built, no index is created, no chart library is adopted, no package begins because of this document.

**What this is.** GitHub map issue [#78](https://github.com/bsemaay-tech/mtc-command-center/issues/78) ("Strategy Knowledge & Research Explorer decision map — browse everything, decide nothing, queue 3/8") ran 2026-08-23 in the owner's rapid-fire mode: 2 AFK research tickets, 4 owner-grilled decision tickets and 1 prototype ticket (three-variant result-chart mock, owner reacted personally), all resolved and closed the same day. **Detail lives in each ticket's resolution comment; this document indexes and applies.**

**Change-control position.** Amends the planning set at master `ab35ca66` (which already carries the map #37, #54 and #67 folds). **Owner outcome documents untouched. Requirement count stays 60 = 44 + 16. Package count stays 75.** Amendments land inside existing sections and existing packages' text (WP-P0-14, WP-P0-18, WP-V3-01, WP-V3-11). **Materiality: MATERIAL** (Phase-0 scope of WP-P0-14 changes — the basic chart output leaves Phase-0; a new owner-gated definition artifact is registered; acceptance additions on WP-P0-14). A fresh G1 acceptance round over the amended set is recommended before G1-IA on affected packages — the owner's call, outside this fold.

---

## 1. The owner decisions (index — detail lives in each ticket)

| Ticket | Decision gist |
|---|---|
| [Decide: result-charts scope and the POC pass criteria (#84)](https://github.com/bsemaay-tech/mtc-command-center/issues/84) | Minimum chart = trade-truth (candles + entry/exit markers + drawn protective levels + aligned equity/DD pane + chart-linked trade list); "TradingView-like" BOUNDED to read-only evidence display (no drawing, no indicator editing, no alerts, no order entry); V3 = replay scrubbing, multi-candidate overlay, parameter surfaces. Six failable POC criteria; candidate order Lightweight Charts → ECharts → gated TV library last. POC executes under the explorer package's own authorization. |
| [Decide: the explorer's data backbone (#82)](https://github.com/bsemaay-tech/mtc-command-center/issues/82) | Derived, rebuildable read index over ledger + TrialRecord catalog + artifact stores + dataset registry — never authoritative, deletable, freshness-stamped. Two stages: Stage 1 = ledger reader on the proven `mcc_readonly` + web-app layer (zero new plumbing); Stage 2 = index arrives WITH the TrialRecord catalog. Host = owner PC local-only; KVM2 never browses research. Legacy-vs-new structural at index level; replayability dependencies tracked with visible warnings. |
| [Decide: minimum vs advanced — what the owner needs to see first (#83)](https://github.com/bsemaay-tech/mtc-command-center/issues/83) | P0 minimum = family tree with lifecycle states + per-candidate where-is-it-why (rejections, re-entry) + screens-vs-evidence labels + basic summary result views incl. the TV-KPI row. Trade-truth chart (+ indicator overlays + MAE/MFE/fees) = FIRST Stage-2 addition. Daily home = tree + "what changed since yesterday" strip. V3 order: comparison → importance → surfaces. "No naked numbers" doctrine ratified, owner-gated. |
| [Decide: lineage navigation and the search model (#85)](https://github.com/bsemaay-tech/mtc-command-center/issues/85) | Six-level spine on every screen (family → candidate → package → deployment identity → evidence window → trial), all clickable; rejection reasons + re-entry triggers first-class spine nodes. Faceted search staged (P0 = state/symbol/tag/free-text; performance + provenance facets with Stage-2 index). Labels/advisory verdicts/provenance stamps = navigational facets, never evidence. History never hidden (PRIOR_IDENTITY as grayed spine nodes; legacy structurally different; replay-broken always warned). |
| [Prototype: the result-chart screen mock (#94)](https://github.com/bsemaay-tech/mtc-command-center/issues/94) | Three-variant mock delivered; owner ratified **layout C · Inspector** (chart + per-trade evidence rail + compact linked list). v2 added TV-KPI row, read-only EMA/ATR overlays, MAE/MFE + fees rows. Read-only indicator display joins the chart scope → indicator series must be carried in the §11.2 per-trial artifacts. Live-bridge chart demand routed to map 5. Branch `prototype/result-chart-mock-94` (`ce7d227a` v1, `578f3cfd` v2). |

Research inputs (closed same day, gists on the map): browse-surface inventory (#80), evidence-artifact catalog (#81) — findings on `research/explorer-surface-inventory`, `research/evidence-artifact-catalog` under `MTC_COMMAND_CENTER/11_TRIAGE/wayfinder_research/`.

---

## 2. Amendments applied

| # | File · where | What |
|---|---|---|
| A1 | brief · new **§11.6** before section 12 | "Explorer decisions — map #78 fold": normative summary of all five decisions with ticket links — chart scope + bound, Inspector layout, POC criteria + candidate order, backbone shape + stages + host, P0/Stage-2 split + home screen + V3 order, spine + search, and the explorer display doctrine v1. |
| A2 | brief · §12.2 under the heading | Amendment paragraph: the six ratified POC criteria + candidate order (Lightweight Charts → ECharts → gated TV library), superseding the earlier KLineChart comparator; POC under the explorer package's own authorization. |
| A3 | brief · dependency-inventory KLineChart row | Supersession note appended in place (comparator order changed by #84). |
| A4 | plan · WP-P0-14 section head | Amendment paragraph: four-item P0 minimum + KPI row; **basic candlestick chart output LEAVES Phase-0** (chart = Stage-2, WP-V3-11; WP-P0-18 verdict no longer gates this package); home screen; Stage-1 backbone; acceptance additions — explorer display doctrine v1, six-level spine with first-class rejection/re-entry nodes, P0 search facets. |
| A5 | plan · WP-P0-18 section head | Amendment paragraph: six failable criteria + candidate order; Inspector layout as target screen; timing may slide toward Stage 2 with WP-V3-11. |
| A6 | plan · WP-V3-01 row (in place) | Build order ratified: comparison → importance → surfaces; Stage-2 index brings performance + provenance search facets. |
| A7 | plan · WP-V3-11 row (in place) | Inspector layout ratified; read-only indicator overlays added (indicator series required in §11.2 per-trial artifacts); per-trade MAE/MFE + fees/funding added; first Stage-2 deliverable after the catalog, ahead of WP-V3-01; KPI row ships earlier in WP-P0-14. |

Discipline: anchored script, every replacement asserts its anchor occurs exactly once; repo-wide grep for changed values after the pass.

---

## 3. New owner-gated definition artifact (registered by this fold; versioned, changes owner-gated, application automatic)

**Explorer display doctrine — v1** (owner-ratified via #83 + #85):
1. **No naked numbers:** every number/graph on every explorer surface carries its evidence-class badge (SIGNAL_SCREEN_ONLY vs acceptance-bearing) + legacy-vs-new flag + freshness stamp.
2. **Labels are facets, never evidence:** demoted diagnostic labels, advisory verdicts and venue-provenance stamps filter and sort only, always badged; an advisory verdict never renders beside scorecard numbers without its "advisory, not evidence" badge.
3. **History never hidden:** full identity history always visible; PRIOR_IDENTITY windows as grayed spine nodes, never merged or hidden.
4. **Legacy-vs-new is structural** at the index level and rendered differently on every screen (never per-screen opt-in).
5. **Replay-broken trials always carry a visible warning** (dataset/engine snapshot dependency tracked by the index).

Existing members of the class, for the record: eligibility check sets, slot-ranking rule, triage worthiness checklist (map #54); control-parity checklist, statistical-battery definition, search-space definition class (map #67 fold); Guardian policy content (map #79, in flight).

---

## 4. What this fold does NOT do

- No implementation, no viewer, no index, no library adoption, no POC run (D-12; the POC runs under the explorer package's own later authorization).
- No package added or renumbered; no requirement changed; owner outcome documents untouched.
- No lifecycle/ledger change (map #54 settled); no evidence-production change (map #67 settled); no execution-surface change (map 5 owns it).
- The live-bridge chart demand is an INPUT to map 5 (#95), not an amendment here.

---

## 5. Verification

- Base: master `ab35ca66`. Branch: `feature/wayfinder-fold-map78-20260823` (worktree C:\WF86).
- Anchored edit script: every anchor asserted unique before replacement; script aborts on any miss.
- Post-pass repo-wide grep of the introduced markers ("map #78 fold", "§11.6") confirms exactly the intended files changed.
- Counts re-stated: requirements 60 (44 + 16), packages 75 — unchanged by this fold.

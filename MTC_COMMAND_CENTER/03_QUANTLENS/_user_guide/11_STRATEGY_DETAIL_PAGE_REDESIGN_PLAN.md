# Strategy Detail Page — Redesign Plan (v3)

Status: PLANNED (not started). Proposed 2026-06-02, revised 2026-06-03 (v2 then v3)
by Claude (Opus 4.8). v3 after Barış selected the **terminal** visual direction
(`proto_B2_terminal.html`) and gave 5 structural revisions.
Owner decision pending: Barış (final sign-off to start Wave A).

Companion plans:
- `10_STRATEGY_SCORECARD_REDESIGN_PLAN.md` — the scoring model (source of truth).
- Tracked in `NEXT_STEPS.md` as **SP-005** (UI sibling of scoring work **SP-004**).

> Plan only. **No live application implementation** until Barış explicitly says so.
> Prototypes live in `08_DASHBOARD_APP/apps/web/prototypes/` and touch nothing the
> live app loads.

---

## 0a. What changed in v3 (read this first)

Visual direction locked: **terminal** (dark quant aesthetic, `proto_B2_terminal.html`).
Five structural revisions from Barış:

1. **One scoring system only.** The **Scorecard is the single source of all numeric
   scores**. QuantLens gives *expert commentary only* — it does **not** assign its
   own numbers; it **references** the scorecard gate scores. No score appears in two
   places. (Implication: `commercial_value` and `complexity` from QuantLens are shown
   as **qualitative labels** + "see Scorecard" links, not as competing numeric bars.)
2. **Merge QuantLens Verdict + Decision Summary** into one block — they answered the
   same question. New combined section: **"Verdict & Decision"**.
3. **Scorecard sits directly under the Verdict & Decision block** and is
   **click-to-expand** (each gate row expands to its sub-criteria).
4. **Backtest Evidence becomes TradingView-style.** Show **cases**: (a) a
   *video-settings case* if the source stated parameters, and (b) *optimized best
   cases* if optimization ran. Every case shows its **settings, symbol, timeframe**,
   and **all cases run on one standard date window**. Metrics presented like the TV
   Strategy Tester (net profit, trades, % profitable, profit factor, max DD, avg
   trade, Sharpe) + equity curve + Buy&Hold + source-claim-vs-reproduced.
5. **Stage example prototypes** added — one page per journey stage (rules extracted,
   testability confirmed, backtested, promotion review) so the design is validated
   across the whole lifecycle, not just the blocked case.

Section order changed accordingly (§2.1). The v2 sections below remain valid except
where v3 supersedes them (noted inline).

---

## 0. What changed in v2

1. **Direction locked: single-scroll Prototype B.** Tabbed A and compact C are
   dropped as the primary page. C may later become a list-row "peek" view (not part
   of this plan).
2. **QuantLens Verdict is now a first-class layer** — and it is **not new data**.
   The repo already runs QuantLens: `03_QUANTLENS/03_SALVAGE_IDEAS/<candidate>/`
   holds 7 artifacts per analyzed candidate, including
   `01_candidate_metadata.yaml` with `quantlens_decision`, `commercial_value_score`,
   `complexity_score`, `repaint_risk`, `lookahead_risk`, `closed_source_risk`,
   `candidate_kind` (salvageable-idea flags), `market_type`, `recommended_next_step`.
   The dashboard currently **ignores these files**. The redesign surfaces them.
3. **New sections:** Strategy Taxonomy, QuantLens Verdict, Salvageable Ideas.
4. **English-only UI rule** is now mandatory and global (see §3).
5. **Three waves** (was two): A = wording/layout on existing data, B = QuantLens
   structured data + new reader, C = scorecard_v2 + backtest-evidence visuals.
6. **Conditional render matrix** keyed by QuantLens decision (garbage / closed-source
   / complexity-overload collapse the page to decision + salvage).

---

## 1. Goal — the 9 questions the page must answer in < 10 seconds

1. What is this strategy? → Header name + English description.
2. What market / timeframe? → Header subtitle.
3. What type / category? → Strategy Taxonomy (category + time horizon).
4. What market condition does it target? → Taxonomy (expected condition).
5. What method does it use? → Taxonomy (method) + Trading Rules.
6. Can it be tested? → Decision Summary + Testability field + Missing-before-test.
7. Commercially interesting or worthless? → QuantLens commercial-value verdict.
8. What is missing? → Missing-before-test checklist + "Not defined yet" rules.
9. What is the next required action? → Human-action box (single, imperative).

---

## 2. Selected layout & information architecture

**Single-scroll** (Prototype B base), one vertical narrative, progressive
disclosure via `<details>` for heavy/technical content. A **sticky mini-summary**
bar stays pinned while scrolling (strategy name · decision · next action ·
QuantLens verdict).

### 2.1 Section order (v3 — merged verdict, scorecard directly under)

| # | Section | Always visible? | Notes |
|---|---|---|---|
| 1 | Header / Strategy Identity | yes | name, subtitle, English description, status + QuantLens badges |
| 2 | **Verdict & Decision** (merged) | yes | QuantLens commentary **+** decision summary in one block: verdict, reason, can-test?, blocker, next action. **No scores here** — references the Scorecard. (v3 #1, #2) |
| 3 | **Scorecard** | conditional | directly under Verdict & Decision; **the only scoring**; click-to-expand gates (v3 #1, #3). Hidden in stop states. |
| 4 | Strategy Taxonomy | conditional | hidden if Garbage / Closed-source-stop |
| 5 | Review Journey (pipeline) | conditional | hidden in stop states |
| 6 | Trading Rules | conditional | hidden if Garbage; shown otherwise |
| 7 | Backtest Evidence | conditional | TV-style cases (v3 #4); hidden in stop states |
| 8 | Salvageable Ideas | **yes (mandatory)** | promoted directly under verdict in stop states |
| 9 | Source Material | yes | compact, de-emphasized |
| 10 | Technical Details | yes (collapsed) | debug, never dominates |

**Why Verdict & Decision is one merged block at the top:** v2 had separate Decision
Summary and QuantLens Verdict that restated each other. v3 merges them — QuantLens
*is* the decision authority. The Scorecard follows immediately so the reader sees
"verdict → the numbers behind it" with no scroll. The merged verdict also governs
the conditional render matrix (§2.2).

### 2.2 Conditional render matrix (driven by `quantlens_decision`)

| QuantLens decision | Sections shown |
|---|---|
| Pass to scoring / Needs clarification / Research only | all (taxonomy, gates, rules, scorecard, evidence, salvage, source, technical) |
| **Garbage** | Header, Decision Summary, QuantLens Verdict, **Salvageable Ideas (mandatory)**, Source, Technical. **No** taxonomy detail, scorecard, backtest. |
| **Closed-source / paid dependency** | Header, Decision Summary, QuantLens Verdict (stop banner), Source, Technical. **No** scoring, **no** backtest eligibility, **no** salvage** (system depends on the closed indicator → nothing reusable). |
| **Complexity overload (≥8/10)** | Header, Decision Summary, QuantLens Verdict, "why too complex" + "what to simplify", Salvageable Ideas, Source, Technical. **No** full backtest/promotion flow. |
| Salvage ideas only / Reject | Header, Decision Summary, QuantLens Verdict, **Salvageable Ideas**, Source, Technical. |

** Closed-source exception: if the *dependency* is closed-source but independent
sub-ideas exist that do **not** need it, those may still appear in Salvageable
Ideas. If the whole system needs the closed indicator, salvage is suppressed.

---

## 3. English-only UI rule (mandatory)

Every user-facing string in the Strategy Detail Page is **English**: labels,
descriptions, explanations, warnings, badges, decisions, tooltips, summaries,
QuantLens copy, salvage idea text.

- The **strategy description must be translated to English** even when the source
  (YouTube / transcript) is Turkish or any other language.
  - Source idea: `"VWAP'a dokunuşta sıçrama denemesi."`
  - UI: `"A mean-reversion scalp attempt based on price bouncing from VWAP."`
- The **only** exception: raw source material shown inside the advanced Source /
  raw-transcript disclosure may appear in its original language. The UI *around* it
  (labels, buttons, warnings) stays English.

Implication for the data model: `strategy_description_en` is a **derived/extracted**
field requiring a translation+summarize step (Wave B). Until it exists, fall back to
any English text available; never display untranslated foreign-language prose as the
description. (This reverses the v1 plan's bilingual TR-body allowance.)

---

## 4. Section specs

### 4.1 Header / Strategy Identity
- **Name:** human display name (e.g. "VWAP Bounce Scalp"). Fallback chain:
  `strategy_display_name` → `producer_spec.title` → humanized family → "Unnamed
  strategy". **Never the raw ID.**
- **Subtitle:** `{instrument} · {timeframe} · {source_kind}` →
  "Crypto · 5m · YouTube strategy".
- **Description:** one English sentence (`strategy_description_en`).
- **Status badge:** human label from terminology map (§9).
- **QuantLens badge (compact):** e.g. "QuantLens: Needs clarification".

### 4.2 Verdict & Decision (merged — QuantLens commentary + decision) — v3
One block at the top. QuantLens **is** the decision authority; v2's separate
"Decision Summary" is folded in here. QuantLens is a strict, skeptical chief auditor:
accepts no claim without evidence, ignores marketing, judges only mathematical logic,
testability, commercial potential, robustness, realistic implementation, and whether
the idea has any place in trading literature / common quant practice.

**Must display (commentary only — no numeric scores invented here):**
- **Verdict** — QuantLens decision state (§4.4).
- **Reason** — why, in firm plain English.
- **Can it be tested?** + the single dominant **blocker**.
- **Recommended next action** — one imperative line.
- **Risk flags** — repaint / lookahead / unverified claims / undefined rules.
- **Qualitative assessments (labels, not scores):** commercial value (§8.6 label),
  literature relevance, testability (§8.7), complexity level (label + "see Scorecard").
- **Score reference (no re-scoring):** a one-line pointer to the Scorecard below,
  e.g. *"Scorecard: Intake 38/100; later gates not yet evaluated — see below."*
  QuantLens **never** prints its own competing total.
- Inline chips: Evidence level (§8.3), Documented vs Proven (§8.4), Testability.

**Tone:** firm, technical, direct. No marketing, no motivation, no inflating weak
evidence.
- Good: "Commercial value is unproven. The idea is testable, but the edge is not
  demonstrated."
- Bad: "This looks like a very promising strategy with great potential."

**Example block:**
```
Verdict: Needs source clarification              [QuantLens]

Uses VWAP bounce logic, but the source does not define exact entry threshold,
stop-loss, or take-profit rules. Marketing claims discarded.

Can test?  No — rules incomplete.   Blocking: undefined exit / stop / take-profit.
Next action: Complete the source/formula audit before scoring or backtesting.

Commercial value: Plausible but unproven    Testability: Partially testable
Literature: Common (VWAP mean-reversion)     Complexity: Moderate
Risks: entry threshold undefined · exit missing · claims unverified · repaint unknown

Scorecard: Intake 38/100 · later gates not evaluated  →  see Scorecard below.
```

> v3 #1 enforcement: the numbers `38/100` etc. are **owned by the Scorecard**; the
> verdict only cites them. Commercial value / complexity render as **labels**, never
> as second numeric bars competing with the gates.

### 4.4 QuantLens decision states
Clear, non-technical labels (machine token → UI label):
- `PASS` → **Pass to technical scoring**
- `NEEDS_CLARIFICATION` → **Needs source clarification**
- `RESEARCH_ONLY` → **Research only**
- `SALVAGE` → **Salvage ideas only**
- `REJECT` → **Reject**
- `GARBAGE` → **Garbage**
- `CLOSED_SOURCE_STOP` → **Closed-source / paid indicator detected — analysis stopped**
- `COMPLEXITY_OVERLOAD` → **Too complex — simplification required**

### 4.5 QuantLens stop conditions
1. **Paid / closed-source indicator.** If a paid, invite-only, proprietary, or
   closed-source indicator is required and the strategy cannot function without it:
   show exactly **"Closed-source / paid indicator detected — analysis stopped."**
   No scoring, no backtest eligibility, no salvage (when the whole system depends on
   it). Drives the closed-source row of the render matrix (§2.2).
2. **Garbage.** Show only Decision Summary + QuantLens Verdict + **Salvageable
   Ideas** (mandatory). Suppress normal technical scoring sections.
3. **Complexity overload (`complexity_score` ≥ 8/10).** Show decision + "why too
   complex" + "what must be simplified". Do **not** enter full backtest/promotion
   flow until simplified.

### 4.6 QuantLens mandatory warnings (prominent badges)
- **Repaint risk detected** (red) — when `repaint_risk` ∈ {YES, SUSPECTED}.
- **Lookahead risk detected** (red) — when `lookahead_risk` ∈ {YES, SUSPECTED}.
- **Unverified backtest claim** — every source/video metric:
  "Source backtest claim: 82% win rate — unverified" until reproduced internally.
- **Rejected marketing claim** — promo claims shown as rejected, not evidence:
  "Rejected marketing claim: 'This strategy never loses.'"

`UNKNOWN` repaint/lookahead renders as an amber "Repaint status unknown" — never
silently treated as safe.

### 4.7 Strategy Taxonomy
Compact chips + one-line explanation per group (not a dense table). Multi-value
allowed. Every group supports **"Unknown"**.
1. **Category / time horizon:** Scalping · Day trading · Swing · Position ·
   Multi-horizon · Unknown.
2. **Expected market condition:** Trending · Ranging · Reversal · Breakout · High
   vol · Low vol · Mean-reversion regime · Unknown.
3. **Strategy method:** Trend following · Mean reversion · Breakout · Pullback
   continuation · Reversal · Momentum · Volatility expansion · Liquidity sweep · S/R
   reaction · VWAP bounce · Multi-factor filter · Unknown.
4. **Instrument / market fit:** Crypto · Forex · US equities · Index futures · Gold ·
   Not enough evidence.
5. **Automation suitability:** Machine-testable · Partially · Manual/discretionary ·
   Not testable yet.
6. **Complexity:** Simple · Moderate · Complex · Excessive (mapped from
   `complexity_score`).

### 4.8 Pipeline / Gate Progress (strategy-review journey, not a raw pipeline)
Stepper, each node Done / Current / Blocked / Not started, with tooltip + (if
blocked) where / why / how-to-unblock. Reworded stages:
- Discovered → Source checked → Rules extracted → Testability confirmed →
  Backtested → Promotion review → Paper-trade candidate → Integrated.

### 4.9 Trading Rules (expanded)
Each field labelled; missing shows **"Not defined yet"** (never blank, never hidden
— missing info is signal). Fields:
Market / bias · Expected market condition · Strategy method · Entry trigger · Entry
filters · Exit logic · Stop-loss · Take-profit · Trailing stop · Breakeven logic ·
Risk management · Avoid trading when · Repaint/lookahead notes · Assumptions.
Small "Documented, not yet proven" badge when rules exist but Gate 2 is N/A.

### 4.10 Scorecard — the single scoring system, directly under Verdict (v3 #1, #3)
Placed immediately below the Verdict & Decision block. **This is the only place
numeric scores live.** 4 gate bars + repaint hard-fail; per gate: status,
earned/available **or N/A**, blocked flag. No single composite number.

**Click-to-expand (v3 #3):** each gate row is collapsed by default to
`name · bar · score`. Clicking a gate expands its **sub-criteria table** —
per criterion: value, status (`OK / N_A / NOT_COMPUTED / ...`), reason points were
lost, required improvement, and `source_path` (the §3.1 envelope from `10_...`).
Collapsed view stays scannable; detail is one click away.

The Verdict block (§4.2) references these numbers; it never restates a competing
total. Commercial value / complexity from QuantLens are labels, not gate bars.

### 4.11 Backtest Evidence — TradingView-style cases (v3 #4)
- **If absent:** "Backtest evidence is not available yet." + **reason** ("Blocked
  upstream: deterministic rules are not complete.") + **Required before backtest**
  checklist (exact entry, exact exit, stop-loss, take-profit, repaint/lookahead
  check, test market/timeframe).
- **If present:** present results like the **TradingView Strategy Tester**, organized
  as **cases**:
  - **Video-settings case** — if the source stated parameters, run exactly those and
    label it "Source-stated settings".
  - **Optimized best cases** — if optimization ran, show the top N cells (e.g. best
    by risk-adjusted return), each as its own case.
  - **Every case header shows:** parameter settings · **symbol** · **timeframe** ·
    **date window** (one **standard window** across all cases so they are comparable,
    e.g. `2023-01-01 → 2025-12-31`) · fees/slippage model.
  - **Per-case metrics (TV-tester style):** net profit % · total trades · % profitable
    (win rate) · profit factor · max drawdown % · avg trade (R) · expectancy · Sharpe
    · and the **Buy & Hold** return for the same window + **excess alpha**.
  - **Equity curve** per case (strategy vs Buy&Hold overlay).
  - **Source claim vs reproduced** row (§8.5): the video's claim ("82% win rate")
    beside the system's reproduced number, never merged.
  - **Robustness strip** (when available): WFO folds, CPCV verdict, PBO / overfit
    flag — feeds Gate 2 in the Scorecard (one scoring system: these *inform the
    gate*, they are not a separate score block).
- **Case selector:** a compact tab/dropdown to switch between the video-settings case
  and each optimized case; the standard window stays fixed so cases are comparable.

> v3 #1 consistency: backtest metrics are **evidence**, displayed as raw figures
> (net profit, PF, DD …). The *grade* derived from them lives only in Gate 2 of the
> Scorecard. The Backtest section shows numbers; the Scorecard shows the score.

### 4.12 Salvageable Ideas (mandatory)
Always present (except whole-system closed-source dependency). Even for weak/rejected
strategies, list reusable independent ideas. Categories: Entry filter · Exit · Stop
-loss · Take-profit · Trailing · Breakeven · Money management · Market regime filter
· Session filter · Risk guard · Execution guard.

Each idea: **name · short explanation · possible MTC module type · dependency ·
confidence · why it may be useful · why it may fail.** If none:
**"No salvageable independent idea detected."**

Data source: `01_candidate_metadata.yaml:candidate_kind` flags (guard / confirmation
/ entry_gate / exit_rule / sl_tp_method / trailing_be_method / money_management) +
`03_mtc_module_mapping.md` (module mapping + dependency) + `05_risks_and_unknowns.md`
(why it may fail).

### 4.13 Source Material (de-emphasized)
Source title · source type · source link · transcript status · source quality ·
extracted-rule quality · **marketing claim detected (yes/no)** · **closed-source
dependency detected (yes/no)** · open-source button · open-transcript button.
Thumbnail is a small supporting element, never dominant. File paths → Technical.

### 4.14 Technical Details (collapsed)
canonical ID · raw machine status · duplicate handling · raw blocked reason · source
paths · transcript paths · internal audit code · internal strategy ID · raw pipeline
row · raw scorecard JSON · legacy composite (deprecated). Kept, not deleted (project
rule). Never dominates the main UI.

---

## 5. Adopted UX additions (from Barış's list)

1. **Sticky mini-summary** — pinned bar: name · decision · next action · QuantLens
   verdict. (§2)
2. **Missing-before-test checklist** — compact, exactly what must be completed
   before backtesting. (§4.11)
3. **Evidence-level badge** — Source only · Rules extracted · Backtested internally ·
   Paper-trade observed · Production candidate. Derived from pipeline stage.
4. **Documented vs Proven** distinction — visible chip; documented ≠ proven.
5. **Source claim vs system evidence** row — never conflate YouTube claims with
   reproduced results.
6. **Commercial value** field — Unknown · Weak · Plausible but unproven · Interesting
   · Strong evidence · Rejected (mapped from `commercial_value_score`).
7. **Testability** field — Not testable · Partially testable · Fully testable ·
   Blocked by closed-source dependency.
8. **Human action required** box — single explicit next step, high-contrast.

---

## 6. Terminology map (machine → English; centralized in `ui_labels`)

| Machine token | UI label | Tooltip (English) |
|---|---|---|
| `CANONICAL` | Primary version | "This is the main saved version of this strategy." |
| `DUPLICATE` / `duplicate_of` | Duplicate handling *(Technical only)* | "Another record of the same strategy; evidence is kept on the primary." |
| `duplicate_group` | *(hidden unless >1 & relevant)* | — |
| `LOW_SCORE_REVIEW` | Needs review | "The strategy did not pass the required review gate." |
| `BLOCKED_SOURCE_AUDIT` | Source check needed | "The source rules are incomplete or not verified yet." |
| `NEEDS_FORWARD_EVIDENCE` | Needs paper-trade proof | "Forward (paper) trade evidence is not sufficient yet." |
| `READY_FOR_MTC_V2_REVIEW` | Ready for review | "Evidence is sufficient for the read-only MTC_V2 review queue." |
| `Blocker / next` | Recommended next action | — |
| `MTC_V2` (bare) | Integration readiness | "Status in the MTC_V2 integration pipeline." |
| `SALVAGE` | Salvage ideas only | "The full strategy is not adopted, but reusable ideas were found." |
| `GARBAGE` | Garbage | "No viable strategy; only salvage ideas, if any." |
| `CLOSED_SOURCE_STOP` | Closed-source / paid indicator — analysis stopped | "Depends on a paid/closed indicator; cannot be evaluated." |
| `COMPLEXITY_OVERLOAD` | Too complex — simplification required | "Complexity ≥ 8/10; must be simplified before full evaluation." |
| `OVERFIT_SUSPECT` | Overfit risk | "High overfitting probability (PBO ≥ 0.5); promotion blocked." |
| stage `pre_parity` | Pre-parity | "Awaiting PineTS = Python signal match." |

Rule: a raw machine token **never** renders outside Technical Details. In Technical
it may appear beside its English label.

---

## 7. Show vs hide

**Main UI:** display name, English description, instrument/timeframe/source kind,
human status, QuantLens verdict + reason + risks + commercial value + testability +
complexity, taxonomy chips, decision summary, evidence level, documented/proven,
the 8-stage journey, all 14 trading-rule fields, 4 gate scores + sub-criteria,
backtest metrics (when present) + B&H + source-claim-vs-result, salvageable ideas,
source title/link/transcript-status/quality/marketing-flag/closed-source-flag,
missing-before-test checklist, human-action box.

**Technical Details (collapsed):** canonical_id, raw candidate id, internal strategy
id, duplicate_of, duplicate_group_size, source_url_source, transcript_path, intake/
source file paths, pipeline row path, raw `audit_status`, `stg_code`, raw machine
status tokens, raw `blocked_reason`, raw `*_explanation` audit strings, raw
`scorecard` JSON, deprecated legacy composite. (Kept, not deleted.)

---

## 8. Field semantics & mappings

### 8.1 Scorecard alignment with `10_STRATEGY_SCORECARD_REDESIGN_PLAN.md`
Adopt verbatim: 4 gates (Gate 1 Intake /100, Gate 1B Feasibility /50, Gate 2
Backtest /100, Gate 3 Production /100) + Repaint/Lookahead hard-fail; per-criterion
`{value,status,reason,source_path}` envelope; only `OK` scores; N/A until phase data
exists; **never** recollapse to one number. The legacy single-score
`build_scorecard()` is shown only as a deprecated line in Technical Details until
SP-004 Phase 2 emits `scorecard_v2`. This page is the scorecard plan's Phase 3.

### 8.2 QuantLens fields — already in `01_candidate_metadata.yaml`
`quantlens_decision`, `commercial_value_score` (→ §8.6 label), `complexity_score`
(→ §4.7 Complexity), `repaint_risk`, `lookahead_risk`, `overfit_risk`,
`closed_source_risk` (→ closed-source stop), `risk_management_quality`,
`candidate_kind` (→ salvageable-idea categories), `market_type` (→ instrument fit),
`primary_timeframe`, `strategy_type`, `recommended_next_step` (→ human next action).

### 8.3 Evidence level — derived from pipeline stage
discovered/classified → "Source only"; rules extracted → "Rules extracted";
backtested → "Backtested internally"; paper_trade → "Paper-trade observed";
promoted/integrated → "Production candidate".

### 8.4 Documented vs Proven — derived
"Documented" if trading rules present. "Proven" only if Gate 2 PASS with B&H alpha.
Rules present + Gate 2 N/A/FAIL → chip "Documented, not yet proven".

### 8.5 Source claim vs system evidence
Two-column row: source claim (always tagged "unverified") vs reproduced metric
(or "not reproduced yet"). Never merge the two numbers.

### 8.6 Commercial value (from `commercial_value_score` 0–10)
0 → Rejected; 1–2 → Weak; 3–4 → Plausible but unproven; 5–6 → Interesting;
7–8 → Strong evidence (only if internally reproduced); 9–10 → Strong evidence.
Bands provisional → confirm with Barış (mirror `10_...` §8 data-driven approach).

### 8.7 Testability — derived
Closed-source dependency → "Blocked by closed-source dependency"; deterministic rules
complete → "Fully testable"; partial rules → "Partially testable"; none → "Not
testable".

---

## 9. Data model — field availability buckets

| Field | Bucket | Source / note |
|---|---|---|
| `complexity_score` | **Available now** | `01_candidate_metadata.yaml` |
| `quantlens_decision` | **Available now** | candidate_metadata |
| `commercial_value_score` | **Available now** | candidate_metadata → §8.6 |
| `repaint_risk`, `lookahead_risk` | **Available now** | candidate_metadata |
| `closed_source_risk` | **Available now** | candidate_metadata → stop condition |
| `instrument_fit` (`market_type`) | **Available now** | candidate_metadata (often UNKNOWN) |
| `salvageable_ideas` (categories) | **Available now** | `candidate_kind` flags + `03_mtc_module_mapping.md` |
| `human_next_action` | **Available now** | `recommended_next_step` / `06_next_action.md` |
| `quantlens_reason` | **Derivable** | parse `02_codex_triage.md` / `00_raw_quantlens_report.md` |
| `evidence_level` | **Derivable** | from pipeline stage (§8.3) |
| `documented_not_proven` | **Derivable** | rules present + Gate 2 status (§8.4) |
| `testability_status` | **Derivable** | rules completeness + closed-source (§8.7) |
| `missing_before_backtest` | **Derivable** | gaps in trading-rule fields |
| `automation_suitability` | **Derivable** | candidate_kind + testability |
| `strategy_display_name` | **Future extraction** | LLM/human; `strategy_thesis_en` (`10_...` P0A) |
| `strategy_description_en` | **Future extraction** | translate+summarize source to English (§3) |
| `strategy_category` / `strategy_time_horizon` | **Future extraction** | partial in `strategy_type`; needs classifier |
| `expected_market_condition` | **Future extraction** | classifier / LLM |
| `strategy_method` | **Future extraction** | classifier / LLM (some in producer_spec) |
| `literature_relevance` | **Future extraction** | QuantLens LLM step |
| `unverified_claims`, `rejected_marketing_claims` | **Future extraction** | QuantLens LLM claim extraction |
| `quantlens_decision` extra states (`CLOSED_SOURCE_STOP`, `COMPLEXITY_OVERLOAD`) | **Schema change** | current YAML enum lacks these; derive from `closed_source_risk` / `complexity_score` until schema adds explicit states |
| structured `salvageable_ideas[]` (name/module/dependency/confidence/why) | **Schema change** | today it is split across 3 markdown files; needs a structured block in the YAML |

**Key gap:** the salvage YAML/markdown exists **only** for candidates QuantLens has
analyzed (3 today). Most pipeline rows have none → QuantLens Verdict renders
"Not yet analyzed by QuantLens" with a "Run QuantLens analysis" next-action.

---

## 10. Component / file plan (inspected, not guessed)

Verified in repo this session:
- UI render: `08_DASHBOARD_APP/apps/web/app.js`
  (`renderUnifiedStrategyDetail` L389, `renderDecisionPanel` L529,
  `renderScorecard` L1132, `renderSparkline` L619), `index.html` (`#strategyDetail`
  L50), `styles.css`.
- Decision sentence (raw, ID-based): `apps/api/mcc_readonly/mtc_v2_reader.py`
  `_decision_sentence` L202–218.
- Composite score: `apps/api/mcc_readonly/presentation_reader.py:build_scorecard` L65.
- Audit aggregation: `apps/api/mcc_readonly/audit_reader.py` (reads QuantLens
  registry JSONL; already knows a `salvage only` blocked_reason; **does not read
  `03_SALVAGE_IDEAS/*/*.yaml`**).

| Component | Action | Wave |
|---|---|---|
| `apps/api/mcc_readonly/ui_labels.py` *(new)* | terminology map `{token:{en,tooltip}}`, single source for dashboard + CLI | A |
| `apps/api/mcc_readonly/mtc_v2_reader.py` | refactor `_decision_sentence` → structured `{verdict, reason, blocker, next_action, why}` (ID-free, name-based); keep legacy string one release | A |
| `app.js` render layer | new fns: `renderStrategyHeader`, `renderStickySummary`, `renderVerdictDecision` (merged, v3), `renderTaxonomy`, `renderJourney`, `renderTradingRules`, `renderTechnicalDetails`; restructure `renderUnifiedStrategyDetail` into single-scroll sections + `<details>` | A |
| `index.html` | sticky-summary container + section scaffolding | A |
| `styles.css` | **terminal theme** (dark, cyan/amber accents, mono data); cards, sticky bar, chips, warning states, stepper, responsive single-column, no horizontal scroll | A |
| `apps/api/mcc_readonly/quantlens_reader.py` *(new)* | parse `03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` (+ `03_mtc_module_mapping.md`, `05_risks_and_unknowns.md`); emit a `quantlens_verdict` object (commentary + labels, **no scores**) + `salvageable_ideas[]`; derive stop states | B |
| `audit_reader.py` | attach `quantlens_verdict` to the strategy row (join by candidate_id) | B |
| `app.js` | `renderVerdictDecision` populates QuantLens commentary; `renderSalvageableIdeas`; conditional render matrix; warning badges | B |
| `renderScorecardV2` (`app.js`) | 4 gate bars + N/A, **click-to-expand sub-criteria** (v3 #3); placed directly under verdict | C |
| `renderBacktestEvidence` (`app.js`) | **TV-tester-style cases** (v3 #4): video-settings case + optimized best cases, each with settings/symbol/timeframe on one standard window; per-case metrics + equity + B&H + source-claim-vs-result; case selector | C |
| backtest-case data source | needs a reader over sprint/optimization run artifacts (`sprint_runs/...`, `single_strategy_runs/...`) to assemble cases — confirm artifact shape in Wave C | C |
| filters/badges migration | `pipelineScoreFilter` numeric → gate status | C |
| `prototypes/proto_B2_terminal.html` + 4 stage variants | chosen-direction prototypes; stage variants validate full lifecycle (§13) | done (mockup) |

No scoring math is written here (consumes `scorecard_v2`). No Pine/parity/pipeline
change. `quantlens_reader` is read-only over existing files. The backtest-case
reader (Wave C) is read-only over existing run artifacts.

---

## 11. Implementation waves

**Wave A — UI / wording / layout on existing data (ship first).**
Single-scroll restructure, sticky summary, terminology map, structured decision
object, header (name/desc fallback), decision summary, trading-rules card with
"Not defined yet", taxonomy shell (chips render "Unknown" when data absent),
8-stage journey, Technical collapse, source slim-down, responsive CSS. Fixes the
bulk of the complaints without backend extraction. QuantLens section renders a
placeholder ("Not yet analyzed").

**Wave B — QuantLens structured data + reader.**
New `quantlens_reader.py` surfacing the existing salvage YAML/markdown; QuantLens
Verdict card; Salvageable Ideas section; conditional render matrix; repaint/
lookahead/marketing/unverified-claim warnings; commercial-value, testability,
evidence-level, documented-vs-proven derivations; schema add for explicit
`CLOSED_SOURCE_STOP` / `COMPLEXITY_OVERLOAD` states + structured `salvageable_ideas[]`.
Future-extraction fields (translation, taxonomy classifier, claim extraction) land
as they become available; UI shows "Unknown"/"Not defined yet" until then.

**Wave C — scorecard_v2 + backtest-evidence visuals.**
Depends on SP-004 Phase 2. 4 gate bars with N/A, full backtest-evidence
visualization (equity, metrics, B&H, source-claim-vs-result), filter/badge
migration to gate status.

Immediately shippable: **Wave A**. Requires backend/schema: **B**. Requires scoring
engine: **C**.

---

## 12. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Salvage YAML exists for only ~3 candidates | High | "Not yet analyzed by QuantLens" placeholder + run-analysis action |
| English translation needs an LLM step (cost/latency) | Med | Wave B; cache `strategy_description_en`; fallback to existing English text, never raw foreign prose |
| QuantLens YAML enum lacks `CLOSED_SOURCE_STOP`/`COMPLEXITY_OVERLOAD` | Med | derive from `closed_source_risk`/`complexity_score` until schema adds states |
| Salvageable ideas split across 3 markdown files (unstructured) | Med | Wave B parser; later add structured `salvageable_ideas[]` block to YAML |
| `scorecard_v2` not built (SP-004) | High | three-wave split; A & B independent of C |
| Conditional render matrix hides a section a workflow relied on | Med | nothing deleted — moved to Technical `<details>`; matrix documented + tested |
| Closed-source stop must truly gate scoring/eligibility | Med | enforce in reader (suppress downstream objects), not just hide in UI |
| Display name / taxonomy absent on most rows | High | fallback chains + "Unknown"/"Not defined yet" everywhere |
| Decision-object refactor changes API shape | Med | keep legacy string one release; golden-file test |
| Scope creep into scoring logic | Med | hard rule: no scoring math here; consume `scorecard_v2` only |

Project safety: no live trading, no `MTC_V2.pine` edit, no audit-data deletion, no
pipeline-logic change, no broad refactor. Presentation + one terminology map + one
decision-object refactor + one read-only QuantLens reader.

---

## 13. Prototypes (visual mockups — not the live app)

Chosen direction: **terminal** (`proto_B2_terminal.html`). The v3 stage variants
below reflect the merged Verdict & Decision block, the click-to-expand Scorecard
directly under it, and the TV-style Backtest Evidence. One page per journey stage so
the design is validated across the full lifecycle (v3 #5):

| File | Journey stage | What it demonstrates |
|---|---|---|
| `proto_B2_terminal.html` | Source checked (blocked) | base case: incomplete rules, Gate 2+ N/A, no backtest |
| `proto_stage_rules_extracted.html` | Rules extracted | rules complete, Gate 1 high, Gate 1B partial, backtest still N/A |
| `proto_stage_testability.html` | Testability confirmed | Gate 1 + 1B done, ready to backtest, Gate 2 N/A |
| `proto_stage_backtested.html` | Backtested | TV-style cases (video-settings + optimized), Gate 2 scored, B&H compare |
| `proto_stage_promotion.html` | Promotion review | strong evidence, Gate 2 high + Gate 3 partial, best optimized cases, alpha vs B&H |

All terminal-styled, English-only, single-scroll. They are throwaway mockups for
sign-off; the live implementation follows the waves in §11.

**Status: all 5 built and approved by Barış 2026-06-03.** CSS is **inlined** in each
HTML (an external stylesheet would not load over `file://` / in the preview — first
draft used a shared `proto_terminal.css`, kept only as the readable single-source
copy). Backtested + promotion pages include a small inline JS case switcher. The
live build (Wave A) will move this theme into `styles.css` properly.

---

## 14. Acceptance criteria

1. Single-scroll **terminal** direction is the selected, stated base.
2. The entire Strategy Detail Page UI is **English-only** (source-language prose only
   inside the raw-source disclosure).
3. Strategy **category / time horizon** visible (Taxonomy).
4. **Expected market condition** visible.
5. **Strategy method** visible.
6. **Verdict & Decision** is one merged block; QuantLens is the decision authority and
   gives **commentary only** — it assigns **no scores** and references the Scorecard.
7. There is **exactly one scoring system** (the Scorecard); it sits **directly under**
   the verdict and its gates are **click-to-expand**.
8. QuantLens copy is **skeptical, strict, evidence-based**; marketing claims rejected.
9. **Repaint / lookahead** risks are prominent (red badges; `UNKNOWN` ≠ safe).
10. Source/YouTube backtest claims marked **unverified** until reproduced.
11. **Closed-source / paid indicator stop** condition defined and enforced.
12. **Garbage** handling defined (decision + mandatory salvage only).
13. **Complexity-overload (≥8/10)** handling defined.
14. **Salvageable Ideas** section is mandatory (with the no-idea fallback string).
15. Backtest Evidence is **TV-tester-style cases** — video-settings case + optimized
    best cases, each with settings/symbol/timeframe on **one standard window**.
16. Missing rules shown as **"Not defined yet"** (never blank/hidden).
17. The **next human action** is obvious (dedicated box).
18. Raw IDs / internal fields hidden by default (Technical Details).
19. Scorecard aligned with `10_STRATEGY_SCORECARD_REDESIGN_PLAN.md` (4 gates, no
    single composite headline).
20. Practical for MVP-1 (Wave A ships on existing data).
21. The design is validated across journey stages (rules / testability / backtested /
    promotion prototypes), not just the blocked case.

---

## 15. Summary of what changed

**v3 (2026-06-03):**
- Locked **terminal** visual direction (`proto_B2_terminal.html`).
- **Merged** QuantLens Verdict + Decision Summary → one "Verdict & Decision" block.
- **One scoring system:** QuantLens gives commentary only and references the
  Scorecard; commercial-value/complexity are labels, not competing bars.
- **Scorecard moved directly under** the verdict and made **click-to-expand**.
- **Backtest Evidence → TradingView-tester-style cases** (video-settings + optimized
  best cases; each with settings/symbol/timeframe on one standard window).
- Added **stage prototypes** (rules extracted / testability / backtested / promotion).

**v2 (2026-06-03):**
- Locked single-scroll Prototype B; dropped tabbed/compact as primary.
- Added **QuantLens Verdict** as a first-class ruthless layer, grounded in the
  **already-existing** `03_QUANTLENS/03_SALVAGE_IDEAS/*` artifacts (not new data) —
  surfaced via a new read-only `quantlens_reader.py`.
- Added **Strategy Taxonomy** (category/horizon, market condition, method,
  instrument fit, automation suitability, complexity) as chips.
- Added **Salvageable Ideas** (mandatory) mapped to `candidate_kind` + module mapping.
- Added QuantLens **stop conditions** (closed-source, garbage, complexity overload)
  with a **conditional render matrix**.
- Added QuantLens **warnings** (repaint, lookahead, unverified claim, rejected
  marketing).
- Made the UI **English-only**, with a required source-to-English description step.
- Added sticky summary, missing-before-test checklist, evidence-level, documented-vs
  -proven, source-claim-vs-evidence, commercial-value, testability, human-action box.
- Rebuilt the **data model** into available-now / derivable / future-extraction /
  schema-change buckets, mapped to real `candidate_metadata.yaml` fields.
- Split delivery into **three waves** (A existing-data UI, B QuantLens data+reader,
  C scorecard_v2+evidence visuals).
- Updated terminology map, show/hide split, component/file plan (with verified line
  numbers), risks, and acceptance criteria.

---

## 16. Owner decisions (resolved 2026-06-03 by Barış)

All six confirmed the plan's recommended direction:

1. **Section order:** QuantLens Verdict **above** Taxonomy. ✔ (matches §2.1; in v3
   the verdict is the merged Verdict & Decision block, Scorecard directly under)
2. **Strategy names:** **AI-generated** (`strategy_thesis_en`); editable later. ✔
3. **Commercial-value bands (§8.6):** **provisional now** (0=Rejected, 1-2=Weak,
   3-4=Plausible but unproven, 5-6=Interesting, 7+=Strong), tune from data later. ✔
4. **Sequencing:** **ship Wave A first** (existing-data UI), B and C after. ✔
5. **Closed-source stop:** **show independent sub-ideas** that don't need the closed
   indicator in Salvageable Ideas; suppress only ideas dependent on it. ✔ (matches
   §2.2 closed-source row)
6. **Stop-state enums:** **derive** `CLOSED_SOURCE_STOP` / `COMPLEXITY_OVERLOAD` from
   `closed_source_risk` / `complexity_score`; no YAML schema change now. ✔

No open questions remain. Next step is Barış's go-ahead to start **Wave A**
implementation (not yet authorized).

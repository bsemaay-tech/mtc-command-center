# MTC Command Center — Full App Audit (2026-07-05)

Auditor: Claude Fable 5 (read-only session; no code, config, artifact, or memory-file changes).
Scope: does the Command Center actually serve its purpose — tracking strategy research, backtests,
system-test/fake-money work, AI handoffs, and next actions across sessions — and how to maximize it.

Verification basis: live read-only server at `127.0.0.1:8765` (`/healthz` verified
`"mode": "read_only"`, all checks true; `POST /api/snapshot` → 405), full `/api/snapshot` and
`/api/snapshot?refresh=1` payloads (4.8 MB), reader source code, on-disk result directories, and the
`_AI_MEMORY` files. Every claim below cites its evidence. Browser rendering was NOT exercised;
frontend claims come from `app.js` source + snapshot data it consumes.

---

## 1. TLDR verdict

- **The app's core promise — "backtest outputs automatically appear" — is currently broken for
  every run since 2026-07-01.** `backtest_reader.py` globs only depth-1
  (`05_BACKTEST_RESULTS/*/MEGA_walk_forward_results.json`), but July runs nest results one level
  deeper (`turtle_heavy_2026-07-01/turtle_sweep/…`, `overnight_archetypes_2026-07-03/archetypes/…`).
  Dashboard's latest visible run is 2026-06-29 even after `?refresh=1`.
- **The single most important result in the project right now — Faz 3b Stage-1 (H1 confirmed at 1h)
  — is invisible in the app.** It lives in `03_QUANTLENS/research/faz3b_stage1_20260705/` which no
  reader scans, and `RESEARCH_RUN_REGISTRY.json` is empty (`research_runs: []`) despite START_HERE
  mandating registration.
- **Confirmed code bug:** `heartbeat_reader.py:5` uses `parents[5]` (repo root) instead of
  `parents[4]` (MCC root), so the Worker Monitor has reported "overnight_runs dir not found"
  forever, while the dir exists with 99 entries.
- **Home / Command Center is real but stale-misleading:** `CURRENT_STATUS.json` last updated
  2026-05-30; scorecards all date from 2026-06-05..07; QuantLens verdicts from 2026-06-08; Reports
  page indexes only 13 May-era scaffold completion reports while the actual knowledge (109 triage
  docs, MORNING_REPORTs, STAGE1_REPORT) is unreachable from the app.
- **Architecture is fundamentally sound** (strict read-only API, reader-per-domain, schema-gated
  night artifacts, honest empty states, no KPI fabrication) — the failure mode is *contract drift*:
  runs changed shape/location faster than readers, and hand-curated status files decay silently.
- **Cross-session memory works through Markdown, not through the app.** GLOBAL_HANDOFF/NEXT_STEPS
  are current and excellent; SESSION_LOG died 2026-06-14; the dashboard reflects the world as of
  ~June 16 and would actively mislead a cold session about current state.
- **Fake-money/system-test slice (STG002 V1.1) has zero dashboard representation** — outputs are
  git-ignored under `03_QUANTLENS/system_test/` and no reader exists. The existing "Paper Trading"
  page is an unrelated gate-readiness stub.
- **Strategy Intelligence is conceptually right** (dossier + 7 sections + canonical right-rail
  verdict after the R1/R2/R3 cleanups) but is fed month-old evidence, so its authority is illusory
  today.
- Biggest leverage, in order: (1) fix the two reader bugs (glob depth + parents index), (2) add a
  freshness/staleness banner per data source, (3) register faz3b in the research registry and index
  real reports, (4) give system-test its own page fed by `reconciliation_summary.json`.

---

## 2. Evidence-backed findings, by severity

### SEV-1 — Backtest Runs misses all post-2026-06-29 runs (reader glob depth)
- Evidence: snapshot `backtest_status.summary.last_run_id = overnight_multiasset_2026-06-29`;
  refresh=1 identical. On disk, `05_BACKTEST_RESULTS/` contains `turtle_heavy_2026-07-01/`,
  `overnight_full_2026-07-02/`, `overnight_resilient_2026-07-02/`, `overnight_archetypes_2026-07-03/`
  — each has `MEGA_walk_forward_results.json` **one directory deeper** (e.g.
  `turtle_heavy_2026-07-01/turtle_sweep/MEGA_walk_forward_results.json`).
- Cause: `backtest_reader.py:80` — `root.glob("*/MEGA_walk_forward_results.json")` (depth exactly 1).
  Orchestrated multi-stage runs (sweep + cpcv_* + pbo_* subdirs) broke the layout assumption.
- Effect: Home "Backtest Activity / Latest run", Backtest Runs page, and any AI checking
  "did the dashboard see my run" per RESULTS_TO_DASHBOARD_MAP get a false negative. The map's own
  troubleshooting line ("not a dashboard bug") is now wrong — it IS a dashboard reader gap.
- Related: `MAX_RUNS = 80` cap is already saturated (74 top-level `*_results.json` + 17 nested + detached
  + optimization candidates > 80), so even after a glob fix the oldest runs silently fall off with
  no "truncated" indicator; `summary.total_runs: 80` reads as an exact count.

### SEV-1 — Faz 3b Stage-1 (the current headline result) invisible everywhere in the app
- Evidence: `03_QUANTLENS/research/faz3b_stage1_20260705/{pass1_10m,pass2_1h}/MEGA_walk_forward_results.json`
  + `STAGE1_REPORT.md` exist. Snapshot: no run_id matching `faz3b|stage1` in `backtest_status.runs`;
  `strategy_research.research_runs len 0`; `05_REGISTRY/RESEARCH_RUN_REGISTRY.json` =
  `{"research_runs": []}`.
- Two independent gaps: (a) no reader scans `03_QUANTLENS/research/`; (b) the workflow contract
  (START_HERE "register in RESEARCH_RUN_REGISTRY.json, confirm visibility in Strategy Research Lab
  tab") was not executed for this run — and apparently never has been for any run.
- Effect: a cold session opening the dashboard sees "latest: 2026-06-29 multiasset, nothing robust"
  — the opposite of the true state (KELTNER×trail_ema8×1h STRONG_PASS, Stage-2 pending).

### SEV-1 — Worker Monitor / overnight heartbeat permanently offline (off-by-one path bug)
- Evidence: snapshot `overnight_heartbeat: {"available": false, "reason": "overnight_runs dir not found"}`.
  `heartbeat_reader.py:5`: `MCC_ROOT = Path(__file__).resolve().parents[5]` → resolves to
  `C:\LAB\Tradingview_LAB_CLEAN` (repo root), so `OVERNIGHT_DIR` becomes
  `<repo>\03_QUANTLENS\tools\overnight_runs` which does not exist. Correct is `parents[4]`
  (= `MTC_COMMAND_CENTER`). Verified both resolutions with Python this session. Actual dir exists
  with 99 entries incl. `progress/`.
- Effect: the entire Phase-5 emitter/supervisor/watchdog investment (shipped 2026-06-22, tests
  green) never reaches the dashboard, because tests pass `overnight_dir` explicitly while production
  wiring (`read_model.py:381` calls `build_overnight_heartbeat()` with no arg) hits the bad default.
  Textbook "unit-tested, integration-broken."

### SEV-2 — Home status/action data is 5 weeks stale and misleading
- Evidence: `03_STATUS/CURRENT_STATUS.json` `last_updated: 2026-05-30`, `phase: "Strategy Pipeline"`,
  `next_recommended_action: "Backfill missing source URLs…"` — irrelevant to the actual next action
  (Stage-2 pre-registration). Scorecards: 837 cards, every `run_id` from 2026-06-05..06-07 batches.
  `expert_quantlens.generated_at: 2026-06-08` (212 verdicts, majority NEEDS_CLARIFICATION).
- Effect: Home's "Today's Action Queue" and "Needs Review" heuristics run over June-era pipeline
  metadata; numbers are *real* but *not current*, and nothing in the UI says so. This violates the
  spirit of the honest-evidence rule (D-memory: "Gate3 honest — real evidence only") — the data is
  not fabricated, but its currency is misrepresented by omission.

### SEV-2 — Reports page indexes only May scaffold reports; real knowledge unreachable
- Evidence: `03_STATUS/REPORT_MANIFEST.json` mtime 2026-05-30; 13 entries, all
  `MCC_BOOT_0xx_COMPLETION_REPORT.md` (MVP scaffolding). Meanwhile: 109 `.md` files in `11_TRIAGE/`,
  MORNING_REPORTs under `05_BACKTEST_RESULTS/<run>/`, `STAGE1_REPORT.md`, lessons archive — none
  indexed, none viewable in-app.
- Effect: the app answers "where is the evidence?" with 2-month-old bootstrap reports. The actual
  audit trail lives only in Markdown + git.

### SEV-2 — Fake-money/system-test vertical slice has no home in the app
- Evidence: `grep system_test` over `mcc_readonly/*.py` → no hits. Run outputs
  (`reconciliation_summary.json` with accepted=888/duplicates=0/round_trips=444/unexplained=0) are
  git-ignored under `03_QUANTLENS/system_test/` and never surfaced. The nav's "Paper Trading" page
  (`renderPaperTrading`, app.js:2242) is a generic gate-readiness card list — different concept,
  same word — inviting exactly the fake-money/paper/live confusion the program is trying to avoid.

### SEV-3 — Config points at the frozen legacy repo
- Evidence: `/healthz` `path_checks.pinets_root = C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY`
  (frozen repo; exports dir `exists: false`). Also `backtest_reader._collect_optimization_metrics`
  reads `mtc_v2_root/reports/optimization`. Not incorrect today (parity data genuinely lives there),
  but it contradicts the AGENTS.md "do not read the frozen repo" instinct and will silently go
  stale/empty if the legacy tree is ever moved. Deserves an explicit "legacy source" marker in
  diagnostics.

### SEV-3 — SESSION_LOG.md duplicates GLOBAL_HANDOFF (CORRECTED + RESOLVED 2026-07-05)
- CORRECTION: the original audit claimed "dead since 2026-06-14" — wrong; the file is newest-first
  and its top entry is 2026-07-04. The real issue is duplication: every session writes both
  SESSION_LOG and GLOBAL_HANDOFF with overlapping content.
- RESOLVED: Barış chose retirement — SESSION_LOG frozen with a banner, Gate 7 in AI_RULES.md now
  lists GLOBAL_HANDOFF + NEXT_STEPS (+DECISIONS/ACTIVE_FILES/PROJECT_MEMORY as needed) only.

### SEV-3 — Snapshot freshness semantics are confusing
- Evidence: `?refresh=1` re-scans, but `backtest_status.generated_at` equals the max timestamp of
  *visible* runs (`_latest_timestamp(runs)`), so a reader-coverage gap masquerades as "no new runs."
  Cache TTL 30 s (`snapshot_cache: HIT, ttl 30s`). There is no per-source "as of" display in the UI.

### SEV-4 — Minor
- `run_plans` still only the 2026-06-15 draft (`approved: false`, universe unfrozen) — Planner shows
  a 3-week-old draft as the only plan; correct behavior, but reads as abandoned.
- `top_results: []`, `profile_results: 5` rows (pilot + TRX) — Leaderboard/Result Explorer official
  buckets effectively empty; honest, by design (no sanctioned writer ran). OK.
- `large_result_json_not_loaded: 4` (>6 MB results parsed only as stubs) — no UI hint which four.
- Header shows static pills "Local Engine: Idle" / "Token Mode: Local / AI optional"
  (app.js:260-261) — hardcoded decoration, not data; mildly dishonest for a read-only truth app.

---

## 3. Backtest result propagation matrix

| Artifact | Writer | Reader | Page | Current status (verified) | Gap |
|---|---|---|---|---|---|
| `MEGA_walk_forward_results.json` / `*_results.json` | `mega_walk_forward.py` | `backtest_reader.py` globs depth-0 `*_results.json` + depth-1 `*/MEGA_…` | Backtest Runs, Home activity | **BROKEN for nested runs** — last visible 2026-06-29; turtle_heavy/full/resilient/archetypes (07-01..03) missing | Glob needs depth-2 (`*/*/MEGA_…`) or recursive with dedupe; MAX_RUNS=80 saturated, no truncation flag |
| Research-dir runs (`03_QUANTLENS/research/<run_id>/…`) | engine via redirected output | **none** | — | faz3b_stage1_20260705 invisible | Either a research-dir scanner or enforce RESEARCH_RUN_REGISTRY registration (currently empty) |
| `scorecard_v2/*.scorecard.json` | `mcc_night_tail.sh` (approval-gated) | `scorecard_reader.py` | Strategy Intelligence gates, Home metrics | Works; 837 cards, all from 2026-06-05..07 | Not a bug — scoring simply hasn't run since; but UI shows no "evidence as of" date |
| `run_plan.json` + `artifact_index.json` | `build_run_plan.py` | `night_artifacts_reader.py` | Planner, Advanced Artifacts, SI §4 | Works; 1 draft plan (2026-06-15, approved:false) | None (content stale, mechanism fine) |
| `backtest_profile_result.json` | `build_profile_result_artifact.py` | `night_artifacts_reader.py` (schema-validated) | Result Explorer, SI §5 buckets | Works; 5 rows, RESEARCH_ONLY badges, boolean `universe_mismatch` normalized | None |
| `top_results.json` | no sanctioned writer | `night_artifacts_reader.py` | Leaderboard | Correctly empty | None (by design) |
| Heartbeat / progress contract (`progress/_latest.json`) | `progress_emitter.py` + supervisor | `heartbeat_reader.py` | Backtest Runs worker monitor, Home | **BROKEN** — parents[5] path bug → "dir not found" always | One-line fix + an integration test that calls `build_overnight_heartbeat()` with default arg |
| `CURRENT_STATUS.json`, `REPORT_MANIFEST.json` (03_STATUS) | hand/AI-curated (writer CLI) | `read_model.py` required files | Home hero, Reports | Schema-valid but frozen 2026-05-30 | No freshness alarm; needs staleness surfacing or generation from live sources |
| System-test replay outputs (`reconciliation_summary.json` etc.) | vertical_slice modules | **none** | — | Invisible | New reader + page (see §5 of findings / roadmap) |
| Registries (`05_REGISTRY/*.json`) | `build_strategy_research_registry.py` | `research_reader.py` et al. | AI Knowledge Base / Research Lab | Strategies 63 / indicators 27 / components 78 / variants 19 OK; `research_runs: 0`, `backtest_results: 0` | Registration step skipped in practice — process gap, not code gap |

---

## 4. Page-by-page audit

**Home / Command Center** — Two-tier metric design (strategy universe deduped vs evidence volume)
is good and honestly labeled (app.js:632-659, invariant-tested). But: action queue derives from
June pipeline metadata; "Latest run" wrong (reader gap); hardcoded header pills. Verdict: right
shape, stale blood. Fix inputs + add per-source "as of" chips, and Home becomes genuinely useful.

**Strategy Intelligence** — Conceptually the strongest page: dossier model with 7 numbered sections,
sidebar section nav, right-rail canonical verdict (after R2/R3 dedup commits `6da2735c`/`e819ac02`),
lazy-loaded scorecard detail endpoint (good architecture), RESEARCH-ONLY/UNIVERSE-MISMATCH badges.
Mental model matches research reality: identity → deterministic gates → AI opinion → plan/evidence
→ results → paper readiness → raw internals. Weaknesses: (a) everything rests on 2026-06-05..07
scorecards + 06-08 verdicts, no evidence-date surfaced; (b) 212 verdicts mostly NEEDS_CLARIFICATION
= section reads as noise; (c) "Paper Trading Readiness" section overlaps the separate Paper Trading
page with a weaker treatment; (d) no link from a strategy to its research-dir runs (faz3b would be
invisible even here). If rewriting: keep sections 1-2-4-5-7, merge 6 into a lifecycle band, demote
section 3 to a collapsed annotation until verdicts are re-authored, and add a "Latest evidence: DATE
from RUN" header line per section.

**Pipeline** — Serves the funnel view; driven by `candidate_pipeline.rows` (176) with gate filters.
Fine. Same staleness caveat.

**Registry** — Catalog works (63 strategies + sources). Fine as-is.

**Backtest Runs** — Run list + worker monitor. Both feeds broken (SEV-1 ×2). After fixes, this page
should also learn run *hierarchy* (an orchestrated overnight = one run with stages, not N invisible
subdirs).

**Result Explorer** — Honest: 5 profile rows, badges, placeholder filters. Correct empty-by-design
behavior; low priority until real profile artifacts exist.

**Planner** — Displays the one draft plan correctly; needs a "stale draft" visual state (>N days
unapproved).

**Validation Terminal** — Built from night_artifacts + backtest evidence; inherits the same input
gaps; concept (funnel/survivors/graveyard) is good and matches the honest-nulls culture.

**Leaderboard** — Correctly empty (no `top_results.json`). Keep locked.

**Paper Trading / Fake-Money / System-Test** — Current page is a mislabeled gate-readiness stub
(cards, "Ready: 0 / Locked: N"). The real system-test lifecycle (STG002 V1.1: benchmark selected,
replay approved+run, 888/888 reconciled, V2-V4 deliberately closed, V5 review 2026-08-01) exists
only in NEXT_STEPS/GLOBAL_HANDOFF markdown. See §5 recommendation below.

**AI Tasks / AI Knowledge Base / Reports / Diagnostics / Read Model** — AI Tasks (copy-ready
prompts) is a nice idea, content dates from the June scaffold era. Knowledge Base shows registry
components + variants (19) but `research_runs: 0` guts the "Research Lab" claim. Reports = SEV-2
stale manifest. Diagnostics honest and useful (healthz mirror). Read Model page is a good
self-documentation habit — keep.

---

## 5. Architecture assessment

**Solid (keep):**
- Hard read-only guarantee, verified end-to-end (POST → 405; healthz `read_only`; writer path
  isolated). This is the app's trust anchor.
- Reader-per-domain modules with tests (23 reader/test pairs) — clean seams, cheap to extend.
- Night-artifact contract: schema-gated, four-state (`absent/invalid/incomplete/usable`),
  never-fabricate rule enforced culturally and structurally (no sanctioned `top_results` writer).
- Snapshot slimming + lazy detail endpoint (115 MB → 4.5 MB, `/api/scorecard-detail`) — right
  pattern, executed well.
- Honest empty states everywhere; the UI would rather show "—" than lie. Rare and valuable.
- Single-instance guarded launcher; bounded logs.

**Brittle (the actual disease):**
- **Implicit path/layout contracts.** Readers encode directory shapes as glob literals
  (`*/MEGA_…`, `parents[5]`, `03_STATUS/*.json`), and run layouts evolve per-sweep
  (stage subdirs, research/ dirs, MEGA_OUTPUT_DIR redirects). Every new orchestration style
  silently defeats a reader. There is no "run manifest" that a run MUST write for the dashboard to
  see it — discovery is inference.
- **Hand-curated status files decay.** `CURRENT_STATUS.json`/`REPORT_MANIFEST.json` were written in
  the MVP era and never again; schema validation passes forever on stale truth. Schema ≠ freshness.
- **Workflow steps that exist only as prose** (register research runs, update SESSION_LOG, run the
  dashboard-upgrade step of runbook §6.4) don't happen under time pressure. Anything not enforced
  by a tool or a test eventually stops.
- **Unit tests that inject paths** (heartbeat tests pass `overnight_dir=`) certify broken production
  defaults. Missing: one smoke test that builds the full snapshot against the real repo and asserts
  e.g. "newest run on disk appears in backtest_status."
- 16 nav pages for a solo user is over-segmented; several pages are one panel deep.

**Simplify:**
- Collapse Planner + Runs + Result Explorer + Validation Terminal + Leaderboard into one
  "Backtests" page with tabs; collapse AI Tasks + Knowledge + Reports + Read Model into "Library".
- Kill hardcoded header pills; replace with real freshness chips.

---

## 6. If rewriting from scratch

**Minimal architecture (what this app actually needs):**
1. **Run manifest contract**: every engine/orchestrator invocation writes one
   `run_manifest.json` (run_id, kind: sweep|research|smoke|system_test, output paths, stage list,
   status, timestamps) at a single well-known root. Dashboard discovers runs ONLY via manifests —
   no glob archaeology. (The progress-emitter contract already proved the pattern; extend it to
   result discovery.)
2. **Event-log spine**: an append-only `events.jsonl` (session start/end, run launched/finished,
   decision recorded, gate passed, approval given) written by the same tools that write
   GLOBAL_HANDOFF today. Home = a rendered view of the last N events + open blockers. This is the
   cross-session memory made queryable; GLOBAL_HANDOFF stays as prose commentary.
3. **Freshness as a first-class field**: every snapshot section carries `as_of` + `source_path`;
   UI renders green/amber/red staleness chips. Stale hand-curated files become impossible to miss.
4. **Page model**: 6 pages — Home (events + blockers + approvals due), Strategies (registry +
   dossier), Backtests (planner/runs/results/leaderboard tabs), Research Lab (research runs +
   variants + hypotheses/pre-registrations with their state), System Test Lab (see below),
   Library (reports/docs/diagnostics/contracts).
5. **Task/handoff model**: NEXT_STEPS entries get IDs + `[AI: …]` tags parsed into the app
   (read-only) so "what is safe next / who does it" is visible without opening markdown.

**Ideal additions (later):** artifact registry with content hashes (evidence provenance), run
lifecycle state machine (planned→approved→running→closed→scored→archived) with approvals as
recorded events, pre-registration objects (H0/H1, STOP rules, status) — Faz 3b already does this
in prose; making it data would make the honest-methodology culture visible in the UI.

**Migration path (no rewrite):** the current codebase supports all of the minimal architecture
incrementally: add manifest writer → new `run_manifest_reader.py` alongside existing readers →
freshness chips in app.js → page consolidation last. Nothing requires touching the engine beyond
the (already-sanctioned) output-side manifest write.

---

## 7. Recommended roadmap

**Quick wins (hours, low risk, all read-side):**
1. Fix `heartbeat_reader.py:5` `parents[5]` → `parents[4]` + add a default-arg integration test.
2. Fix `backtest_reader.py` nested-run discovery (depth-2 glob or `rglob` with stage-dir dedupe,
   grouping stages under one run) + raise/flag MAX_RUNS truncation.
3. Add "as of" timestamps to Home hero, gate sections, verdict section (data already in snapshot).
4. Register `faz3b_stage1_20260705` (+ turtle_heavy etc.) in `RESEARCH_RUN_REGISTRY.json` via the
   sanctioned generator, so Research Lab stops showing 0 runs.
5. Regenerate `REPORT_MANIFEST.json` to index MORNING_REPORTs, STAGE1_REPORT, key 11_TRIAGE audits
   (or better: make Reports page glob known report locations read-only).
6. Remove hardcoded "Local Engine: Idle / Token Mode" pills.

**Medium (a day or two each):**
7. Staleness banner framework (green/amber/red per snapshot section, thresholds per source).
8. Snapshot smoke test: build snapshot against real repo, assert newest on-disk run visible,
   assert heartbeat available when progress dir exists — the test class that would have caught
   both SEV-1s.
9. `CURRENT_STATUS.json` either auto-derived (phase/next action from NEXT_STEPS top section) or
   retired from Home in favor of the handoff-derived view.
10. **System Test / Fake Money Lab page** (new, read-only): reads git-ignored
    `03_QUANTLENS/system_test/<run>/reconciliation_summary.json` + manifest. States to track:
    benchmark (STG002), replay approval (D-ref), replay outputs (expected/accepted/rejected/dup),
    simulated fills, round trips, unexplained events, gate legs V2-V4 status (CLOSED/not-opened),
    promotion blockers, next approved action, V5 review date. Visual firewall: page-level
    permanent banner `SYSTEM_TEST_ONLY — fake money, not paper, not testnet, not live`, distinct
    accent color, and rename the existing page to "Promotion Readiness" so "Paper Trading" stops
    meaning two things. Do NOT put this inside Strategy Intelligence (it is plumbing evidence, not
    strategy evidence) and not LiveOps (nothing is live).
11. NEXT_STEPS parser → read-only "open tasks by owner" panel on Home.

**Larger redesigns (only if the daily-use pain justifies):**
12. Run-manifest discovery contract (§6.1) — kills the glob-drift disease class permanently.
13. Page consolidation 16 → ~6.
14. Event-log spine + Home-as-timeline (§6.2).

---

## 8. Open questions for Barış

1. Backtest Runs semantics: should an orchestrated overnight (sweep + CPCV + PBO subdirs) appear as
   ONE run with stages, or N rows? (Affects the glob fix design.)
2. Is `03_QUANTLENS/research/` intended to feed the dashboard directly, or only via
   RESEARCH_RUN_REGISTRY registration? (Pick one; today neither happens.)
3. `CURRENT_STATUS.json`: keep as a hand-curated artifact (then who updates it, when?) or derive
   from NEXT_STEPS/handoff automatically?
4. SESSION_LOG.md: revive (enforced in Gate 7 tooling) or officially retire in favor of
   GLOBAL_HANDOFF? The rule and the practice currently disagree.
5. System Test Lab page: approve as a read-only reader + page (no execution UI — display only)?
   Note your standing rule requires separate approval for any "dashboard execution UI"; a pure
   reader does not cross that line but you should bless it explicitly.
6. `pinets_root` pointing into the frozen repo: acceptable long-term, or should parity artifacts be
   migrated/copied into the clean repo?
7. Scorecards are June-era: do you want a scoring pass (`mcc_night_tail.sh`, approval-gated) over
   the July runs so Strategy Intelligence reflects current evidence, or leave gates frozen until
   Stage-2?

## 9. Exact next actions

- **[AI: Barış]** Answer §8 Q1-Q5 (Q1/Q2 unblock the two SEV-1 fixes; Q5 unblocks the system-test page).
- **[AI: Claude]** After approval: fix `heartbeat_reader.py` parents index + `backtest_reader.py`
  nested-run discovery, each with an integration test that runs against the real repo layout
  (quick wins 1-2, single small PR, no engine/schema touch).
- **[AI: Any]** Run the sanctioned registry generator to register faz3b_stage1 + July research runs
  in `RESEARCH_RUN_REGISTRY.json`; verify Strategy Research Lab shows them (quick win 4).
- **[AI: DeepSeek]** Regenerate `REPORT_MANIFEST.json` entries for MORNING_REPORTs +
  `STAGE1_REPORT.md` + top 11_TRIAGE audits (bounded JSON edit, quick win 5), then Claude audits.
- **[AI: Claude]** Add per-section `as_of` freshness chips to Home + Strategy Intelligence
  (quick wins 3/6; frontend-only, no data-contract change).
- **[AI: Barış]** Decide scoring pass over July runs (§8 Q7) — approval-gated execution.
- **[AI: Claude, approval-gated]** Design doc for System Test / Fake Money Lab page (reader +
  page spec, states list from §7 item 10) — doc first, code after separate approval.

---
*Audit session evidence: healthz JSON, snapshot + refresh snapshot (4.8 MB), backtest_reader.py,
heartbeat_reader.py, read_model.py, app.js (NAV/DETAIL_SECTIONS/renderHome/renderPaperTrading),
on-disk listings of 05_BACKTEST_RESULTS + research/ + overnight_runs/, 03_STATUS file mtimes,
RESEARCH_RUN_REGISTRY.json, REPORT_MANIFEST.json, SESSION_LOG.md, ACTIVE_FILES.md, GLOBAL_HANDOFF.md,
NEXT_STEPS.md. No files modified except this report.*

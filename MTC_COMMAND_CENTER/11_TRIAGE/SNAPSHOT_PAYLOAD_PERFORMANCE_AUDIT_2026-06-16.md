# Snapshot Payload Performance Audit — 2026-06-16

**Performance audit only. No code/data/artifacts modified.**

## 1. Executive summary
`/api/snapshot?refresh=1` returns **115.56 MB** (121,172,209 bytes), HTTP 200. The payload is
dominated by **scorecard data, embedded redundantly in 3–4 places**:

| Contributor | MB | Used by UI? |
|---|--:|---|
| `scorecards.by_strategy` | 31.62 | **No** (UI reads `scorecards.cards` only) |
| `scorecards.cards` (837 cards) | 30.06 | Yes (counts + scores) |
| `candidate_audit` (whole section) | 8.43 | **No** (CLI/tests only) |
| `candidate_pipeline.rows[].scorecard_v2_cases` | 7.12 | **Count only** (UI reads `.length`) |
| per-card gate detail `gate1/1B/2/3.sub_scores` | ~26 (subset of cards) | Only for the *opened* strategy |

**~40 MB (35%) is shipped but never read by the frontend** (`by_strategy` + `candidate_audit`),
and another ~7 MB (`scorecard_v2_cases` full arrays) is needed only as a count. A
zero-frontend-change patch can remove ~**47 MB (≈41%)**. The verbose gate `sub_scores` blocks
(~26 MB) are a further medium-risk lazy-load target.

Latency: warm fetch **10.2 s**, client JSON parse **0.75 s**; cold first-build ~60 s (prior
report). Latency is server build + 115 MB localhost transfer, not client parsing.

## 2. Preflight worktree scope
`git status --short` / `git diff --stat` run read-only. Tree already dirty from prior accepted
dashboard work (app.js/index.html/styles.css modified; launcher `.ps1`, schemas, tools, tests,
11_TRIAGE reports untracked). Nothing cleaned/moved/reset/staged/committed. This audit adds
only this report; temporary measurement scripts live in `C:\tmp` (not git-tracked).

## 3. Health / API read-only verification
- `/healthz` → 200, `mode=read_only`, `overall_ok=true`.
- `POST /api/snapshot` → **405** (write API blocked).

## 4. Full snapshot timing and byte size
Measured via stdlib `urllib` + `json` (compact re-serialization for per-key sizing):
- `TOTAL_BYTES = 121,172,209` → **115.56 MB**.
- `FETCH_SECONDS = 10.16` (warm; server cache populated). Cold build ~60 s per prior report.
- `PARSE_SECONDS = 0.75` (client-side).
- Parse succeeds; **29 top-level keys**.

## 5. Top-level snapshot size table
| Top-level key | Bytes | MB | % | Notes |
|---|--:|--:|--:|---|
| `scorecards` | 64,679,125 | 61.68 | 53.4 | `by_strategy` + `cards` (see §6) |
| `candidate_audit` | 8,838,329 | 8.43 | 7.3 | **UI never reads it** |
| `candidate_pipeline` | 8,411,238 | 8.02 | 6.9 | rows carry full `scorecard_v2_cases` |
| `strategy_research` | 269,758 | 0.26 | 0.2 | Research Lab |
| `expert_quantlens` | 200,180 | 0.19 | 0.2 | also duplicated per-card |
| `mtc_v2_readiness` | 144,379 | 0.14 | 0.1 | |
| `quantlens` | 118,534 | 0.11 | 0.1 | |
| `backtest_status` | 100,760 | 0.10 | 0.1 | |
| `transcript_reclassification` | 68,517 | 0.07 | 0.1 | |
| `ai_strategy_names` | 52,333 | 0.05 | 0.0 | |
| (21 remaining keys) | each < 40 KB | — | ~0 | parity/registry/task_*/diagnostics/etc. |

Top 3 keys = **78.1 MB (67.6%)**. Everything outside the top 3 totals < 1.4 MB.

## 6. Deep breakdown of largest sections

### scorecards (61.68 MB)
| Subkey | MB | n | Notes |
|---|--:|--:|---|
| `by_strategy` | 31.62 | 46 | dict of strategy→cards; **duplicate of `cards`; UI never reads it** |
| `cards` | 30.06 | 837 | flat card list; the one the UI uses |
| `runs` / `source` / `diagnostics` / `count` | ~0 | — | negligible |

**Cards (837):** avg **37.65 KB**, max **46.79 KB**, min 32.37 KB (very uniform → every card
is heavy). Field bytes across all cards:
| Field | MB | Note |
|---|--:|---|
| `gate3` | 10.24 | full `sub_scores` (criterion/explanation/deduction text) |
| `gate1` | 8.58 | full `sub_scores` |
| `gate2` | 6.21 | full `sub_scores` |
| `notes` | 2.23 | "INCOMPLETE: N required metric(s)…" arrays |
| `gate1B` | 1.40 | full `sub_scores` |
| `expert_quantlens_verdict` | 0.67 | embedded per card (also a top-level key) |
| `gate_summary` | 0.11 | statuses/promotable — this is what Home/Leaderboard need |

Gates 1/1B/2/3 = **~26.4 MB** of verbose sub-score detail. Largest single card 46.79 KB
(`gate3` 13.9 KB + `gate1` 12.5 KB + `gate2` 9.1 KB). Largest cards are the
`enriched_metrics_2026-06-05` run.

### candidate_audit (8.43 MB) — UI-unused
`.rows` (176): avg 50.2 KB, **max 1.80 MB** (one row). Field bytes: `scorecard_v2_cases`
**7.12 MB**, `scorecard_v2` 0.34, `source_record` 0.16, `expert_quantlens_verdict` 0.16. The
mass is embedded scorecard cases. Built by `audit_reader.build_candidate_audit` (CLI `audit`
command + `test_audit_reader.py`), **not referenced anywhere in `apps/web`**.

### candidate_pipeline (8.02 MB) — UI-used, but cases are count-only
`.rows` (176): avg 47.8 KB, **max 1.80 MB**. Field bytes: `scorecard_v2_cases` **7.12 MB**,
`scorecard_v2` 0.34, `expert_quantlens_verdict` 0.16, `directional_research` 0.08,
`stages` 0.06. The frontend reads `scorecard_v2_cases` only as a **count**
([app.js:400](08_DASHBOARD_APP/apps/web/app.js#L400): `Array.isArray(...) ? .length :
(typeof ... === "number" ? ... : null)`) — it already accepts a plain number.

## 7. UI dependency mapping
From `apps/web/app.js` (keys list lines 58–66; readers `pipelineRows()` L313,
`scorecardCards()` L318, `cardsForStrategy()` L350, gate/metric use L366–527, detail
L1037–1289, explorer/leaderboard L1486–1705):

| UI page/section | Snapshot keys used | Heavy fields required? | Lazy-loadable? |
|---|---|---|---|
| Home / Command Center | `candidate_pipeline.rows` (scorecard_v2 summary), `scorecards.cards` (counts, top-5 by `gate2.score`), `backtest_status`, `report_manifest`, `file_diagnostics` | No — only `gate2.score`, `gate_summary.statuses` | n/a (summary) |
| Strategy Pipeline | `candidate_pipeline.rows` | No — summary fields | n/a |
| Strategy Intelligence | `candidate_pipeline.rows[].scorecard_v2`, `cardsForStrategy()` cards, `expert_quantlens_verdict`, `canonical`, `strategy_registry` | **Yes — full `gate1/1B/2/3` incl `sub_scores` (L1289), but only for the OPENED strategy** | **Yes (per-strategy)** |
| Backtest Result Explorer | `night_artifacts.profile_results`, `scorecards.cards` (best `gate2`) | No (score + statuses) | partial |
| Strategy Leaderboard | `night_artifacts.profile_results`/`leaderboard_delta`, `scorecards.cards` (sort by `gate2.score`) | No (score only) | partial |
| Advanced Artifacts / Diagnostics | `night_artifacts`, `file_diagnostics`, raw gate JSON dump of selected strategy (L1288–1289) | Selected strategy only | Yes |
| Registry | `strategy_registry` | No | n/a |
| Research Lab | `strategy_research` | No | n/a |
| (none) | `scorecards.by_strategy`, `candidate_audit` | — | **Not referenced at all** |

## 8. Root cause analysis
1. **Redundant embedding of scorecard cases (~46 MB).** The same scorecard payload is shipped
   as `scorecards.cards` (30 MB) **and** `scorecards.by_strategy` (31.6 MB, a regrouped
   duplicate the UI never reads) **and** inside `candidate_pipeline.rows[].scorecard_v2_cases`
   (7.1 MB) **and** `candidate_audit.rows[].scorecard_v2_cases` (7.1 MB).
2. **Verbose gate detail for all 837 cards (~26 MB).** Every card carries full
   `gate1/1B/2/3.sub_scores` text, but the detail is only rendered when a single strategy is
   opened; list/summary pages need only `gate_summary.statuses` + `gate*.score`.
3. **Two whole sections unused by the UI (~40 MB):** `scorecards.by_strategy` and
   `candidate_audit` (the latter exists for the CLI `audit` command + tests).
4. Transfer of 115 MB uncompressed JSON over localhost is the bulk of the warm latency; the
   cold ~60 s adds server-side build/serialize of the duplicated data.

## 9. Low-risk optimization candidates (no frontend change, no schema-meaning change)
- **L1 — Drop `scorecards.by_strategy` from the snapshot response (~31.6 MB).** UI never reads
  it. Keep the reader/enrichment; just don't serialize it into the HTTP payload. (Note:
  `ai_names_reader` enriches both `cards` and `by_strategy`; `cards` is named independently, so
  dropping `by_strategy` post-build does not affect card names. Add a test asserting names land
  on `cards`.)
- **L2 — Omit `candidate_audit` from the default snapshot (~8.4 MB).** UI never reads it; keep
  `build_candidate_audit`, the CLI `audit` command, and `test_audit_reader.py` intact.
- **L3 — Replace `candidate_pipeline.rows[].scorecard_v2_cases` arrays with their integer count
  (~7.1 MB).** Frontend already reads it as a count ([app.js:400](08_DASHBOARD_APP/apps/web/app.js#L400)).
- **Combined L1–L3 ≈ 47 MB (~41%) with zero frontend edits.**
- **L4 — gzip the response** if not already enabled. 115 MB of repetitive JSON compresses
  heavily (est. ~8–15 MB on the wire). Transport-only; cuts transfer latency without changing
  payload semantics. (Touches server response handling — validate POST still 405, read-only.)

## 10. Medium-risk optimization candidates
- **M1 — Move full gate detail out of the default snapshot (~26 MB).** Keep `gate*.score` +
  `gate_summary.statuses` inline on each card; serve `sub_scores`/raw gate JSON via a
  per-strategy endpoint (e.g. `GET /api/scorecard?strategy=…` or `?card=…`). Requires Strategy
  Intelligence detail (app.js L371, L1289) to fetch on open. Read-only GET only.
- **M2 — Page-scoped snapshots / pagination:** `/api/snapshot/home`, `/api/snapshot/strategy?id=…`,
  `/api/snapshot/results`, `/api/snapshot/artifacts`; or paginate `scorecards.cards`.
- **M3 — Lazy-load scorecards by strategy** instead of shipping all 837 cards up front.

## 11. High-risk / rejected options
- Deleting scorecard/audit data on disk.
- Mutating artifacts or profile-result provenance.
- Changing schema semantics or gate scoring meaning.
- Hiding safety/research-only/universe-mismatch flags to save bytes.
- Any write-path or execution change.

## 12. Recommended next implementation patch
Single low-risk read-model patch implementing **L1 + L2 + L3** (target ~47 MB / ~41% smaller,
no frontend change), plus **L4 gzip** if the server framework makes it trivial. Acceptance for
that patch: snapshot < ~70 MB; `/healthz` 200 read_only; `POST` 405; all API tests pass (add
tests: by_strategy-dropped-but-names-on-cards, candidate_audit absent from snapshot,
scorecard_v2_cases serialized as count); UI Home/Strategy Intelligence/Leaderboard/Result
Explorer still render. Defer **M1 gate-detail lazy-load** (the next ~26 MB) to a follow-up that
adds the per-strategy endpoint + app.js fetch-on-open.

## 13. Safety confirmation
No code, data, schema, or artifacts modified. No backtest/optimization run; no
profile-result/`top_results.json` generated. No Pine / MTC_V2 / backtest engine / broker /
live / paper / strategy logic touched. No files staged/committed/deleted/reset/moved.
`POST /api/snapshot` → 405 verified; `mode=read_only`. Measurement scripts are read-only HTTP
GET clients in `C:\tmp` (not git-tracked).

## 14. Remaining limitations
- Sizes use compact (`separators`-free `json.dumps`) re-serialization; the live server may add
  whitespace, so on-wire bytes can differ slightly from per-key sums (totals corroborate the
  raw 121 MB).
- Warm fetch measured at 10.2 s; the ~60 s cold path (first build) was not re-timed here (would
  require flushing the 30 s server cache). Both are consistent with build+transfer of 115 MB.
- `expert_quantlens` appears both top-level and embedded per card; minor (<1 MB) and not
  pursued in the recommended patch.

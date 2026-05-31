# Current Status

- Status: ACTIVE_DEVELOPMENT
- Product: MTC Command Center (MCC)
- Root: `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER`
- Current phase: MVP-8 + Strategy Pipeline + Audit (Codex) + **Triage workflow + embedded transcript ingest + promoted producer-spec pipeline + Christian OR validation + audit eligibility review + audit/pipeline UI polish, scoring, and MTC_V2 readiness (Codex, 2026-05-31)**
- Last action: Codex calibrated MTC_V2 readiness, added per-row decision sentences, forward paper-trade progress, readiness exports, and a short-lived snapshot cache with forced Refresh.
- Next action (P1): Await the next user-prioritized feature or triage pass.

## Operating Mode (unchanged)

- Read-only first
- Dry-run only
- Report-first
- No live trading
- No direct core patching (MTC_v2 / `MTC_V2.pine` untouched)

## What works right now

- Dashboard server: `python -m mcc_readonly serve --host 127.0.0.1 --port 8765` → `http://127.0.0.1:8765/dashboard`
- Tests: `python -m pytest tests/` -> **30 passed**
- Health: `python -m mcc_readonly health` → `overall_ok=true`
- **Pipeline** is now the default first tab: every strategy candidate as a row across 6 stages
  (Discovered → Backtested → Promoted → Pre-Parity → Paper-Trade → Integrated), with a per-row
  "next action" and a clickable unified detail page shared by both Pipeline and Audit rows
  (plain-language description, historical metrics, stage list, YouTube source video embed,
  paper-trade section, equity sparkline, parity-proof JSON block, audit explanations, and
  long/short research notes).

## Current pipeline snapshot (live data)

- 196 rows. Stage "done" counts: discovered 196, classified 196, backtested 31, promoted 22, pre_parity 1, paper_trade 0, integrated 0.
- Broader QuantLens JSONL discoveries, canonical registry rows, and promoted `producer_spec.json` packets are now represented in one read-only pipeline.
- LINK 8EMA = furthest (PineTS parity PASS, paper-trade next). ADA / LTC = promoted, PineTS parity next.
- 3 salvage-only candidates parked.
- Read-only audit now reports 196 rows with source quality, deterministic rules, source material, backtest eligibility, blocked reason, canonical mapping, recommended next pipeline step, stable triage codes, and a heuristic scorecard. Pipeline and Audit both have score-band filters. Current direct snapshot: 167 eligible, 26 blocked, 166 with source material, 191 deterministic-rule rows. The `Sources` card is the raw scanned source-record count (`source_record_count`), so `2060` means the audit indexed 2060 source entries across JSONL/CSV inputs, not 2060 unique strategies. The recent 11-row eligibility drop is documented in `11_TRIAGE/audit_eligibility_jump_review_2026-05-31.md`.
- MTC_V2 readiness is now tracked as a read-only dashboard tab. It combines Pipeline/Audit score, source gates, promotion status, PineTS parity needs, and forward-evidence needs without editing `MTC_V2.pine`. Current calibration: 0 fully ready, 1 needs forward evidence. LINK is the leading row at 88/100 but still needs forward paper-trade evidence (`0/30` trades).
- Readiness exports are available at `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.md` and `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.csv`.
- `/api/snapshot` now uses a short in-memory cache; dashboard Refresh calls `/api/snapshot?refresh=1` to force a rebuild.
- MEGA/RIGOROUS walk-forward result files are parsed as completed matrix runs; MEGA now exposes 17 symbols, 5 timeframes, and 325318 aggregate trades.
- Fresh dashboard browser verification: `http://127.0.0.1:8766/dashboard` rendered `196 strategies`, `196 records`, healthy status, and no console errors. Port 8765 had an older server process during verification; restart it before relying on 8765 for fresh code.

See `PROJECT_HANDOFF.md` for the full continuity handoff and `01_PROMPTS/CODEX_CONTINUATION_2026-05-30.md` for the next-session task brief.

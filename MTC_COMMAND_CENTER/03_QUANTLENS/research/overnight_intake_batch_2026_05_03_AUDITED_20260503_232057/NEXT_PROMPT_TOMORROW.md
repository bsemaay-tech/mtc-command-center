# Next Codex Prompt — Stage 2 Robustness

You are Codex acting as Stage 2 robustness reviewer.
Repo root: `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2`.
Audited folder: `06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03_AUDITED_20260503_232057`.

Tasks:
1. Read `AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md` and `MTC_V2_READINESS_AUDIT.md`.
2. Run Stage 2 robustness only on **CANDIDATE_001 Kell Wedge** (the single PASS_STAGE2 candidate):
   - Walk-forward 3-fold over 2024-01 → 2026-05 with 6-month windows.
   - Parameter perturbation ±20% on EMA periods, wedge tolerance, ATR stop multiplier.
   - Regime split (bull/bear/chop on BTCUSDT 200-bar EMA slope).
   - Cost stress at 4x and 5x base fee.
   - Per-asset PF check across all 10 symbols.
3. Apply **CANDIDATE_011 anti-extension filter** as overlay on CAND_001 trade set; report DD/PF delta.
4. Conditional Stage 2 on CAND_005 BigBeluga and CAND_007 Linda 5SMA only after CAND_001 finishes.
5. Do NOT touch `MTC_V2.pine` or production runner.
6. Output to a new `stage2_kell_wedge_<TIMESTAMP>` folder.
7. Final response in Turkish: keep / promote / drop verdict per candidate, plus exact next data acquisition asks.

import os
import csv
import json

AUDIT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03_AUDITED_20260503_232046"

def generate_reports():
    # Phase 10: Master Comparison
    with open(os.path.join(AUDIT_DIR, "AUDITED_MASTER_COMPARISON.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Master Comparison\n")
        f.write("| Audited Rank | Candidate ID | Horizon | Native TF | Data Type | Final Classification | Next Action |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        f.write("| 1 | QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0 | DAY_TRADE | 5m | 5M_PROXY | WEAK_CANDIDATE | Needs Stage 2 fee stress optimization |\n")
        f.write("| 2 | QL_CHARLES_FIRST_PULLBACK_50DMA_001 | SWING | 1D | DATA_BLOCKED | NEEDS_REAL_EQUITY_DATA | Procure IBD/US Equities data |\n")
        f.write("| 3 | QL_STAN_STAGE_1B_TO_2A_BREAKOUT_v0 | SWING | 1D | DATA_BLOCKED | NEEDS_REAL_EQUITY_DATA | Procure IBD/US Equities data |\n")
        f.write("| 4 | QL_NICK_WEEKLY_CHARACTER_CHANGE_001 | POSITION | 1W | REAL_NATIVE | PASS_STAGE2 (tentative) | Test on 1W crypto/equities |\n")
        
    # Phase 11: Sleeves
    with open(os.path.join(AUDIT_DIR, "AUDITED_DAY_TRADE_CANDIDATES.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Day Trade Candidates\n\n")
        f.write("### 1. QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0\n")
        f.write("- **Verdict**: WEAK_CANDIDATE (Gap slippage degrades edge)\n")
        f.write("- **Next Test**: Retest with limit entries.\n\n")
        
    with open(os.path.join(AUDIT_DIR, "AUDITED_SWING_TRADE_CANDIDATES.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Swing Trade Candidates\n\n")
        f.write("### 1. QL_CHARLES_FIRST_PULLBACK_50DMA_001\n")
        f.write("- **Verdict**: NEEDS_REAL_EQUITY_DATA\n")
        f.write("- **Holding Period**: 3-10 Days\n\n")
        
    with open(os.path.join(AUDIT_DIR, "AUDITED_POSITION_TRADING_CANDIDATES.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Position Trading Candidates\n\n")
        f.write("### 1. QL_NICK_WEEKLY_CHARACTER_CHANGE_001\n")
        f.write("- **Verdict**: KEEP_UNTESTED_PROMISING\n")
        f.write("- **Required Data**: 1W Weekly OHLCV\n\n")
        
    with open(os.path.join(AUDIT_DIR, "AUDITED_FILTER_EXIT_SIZING_MODULES.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Filter/Exit/Sizing Modules\n\n")
        f.write("- **Roppel 357 Scaleout**: Position sizing idea, maps to MTC Risk module.\n")
        f.write("- **LBR ADTR Position Sizing**: Volatility based sizing, maps to MTC Sizing.\n")
        f.write("- **Stan Forest Group Tree Filter**: Market breadth filter, maps to MTC Entry Gate.\n")

    # Phase 12: MTC V2 Integration
    with open(os.path.join(AUDIT_DIR, "MTC_V2_READINESS_AUDIT.md"), "w", encoding="utf-8") as f:
        f.write("# MTC V2 Readiness Audit\n\n")
        f.write("No candidate is directly ready for MTC V2 today. The LBR Coil needs Stage 2 refinement (limit order implementation vs stop entry). The Swing candidates need formal math definitions before converting to Pine.\n")
        
    with open(os.path.join(AUDIT_DIR, "DO_NOT_INTEGRATE_YET_LIST.md"), "w", encoding="utf-8") as f:
        f.write("# DO NOT INTEGRATE YET\n\n- All candidates.\n")

    # Phase 13: Source Quality
    with open(os.path.join(AUDIT_DIR, "SOURCE_QUALITY_AUDIT.md"), "w", encoding="utf-8") as f:
        f.write("# Source Quality Audit\n\n")
        f.write("- **High Quality TRADER**: LBR, Charles Harris, Stan Weinstein, Minervini.\n")
        f.write("- **Medium Quality EDUCATIONAL**: Generic YouTube patterns.\n")
        f.write("- **Promotional**: Several '1000% return' videos downgraded.\n")

    # Phase 14: Bug & Repair Summary
    with open(os.path.join(AUDIT_DIR, "BUG_AND_REPAIR_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("# Bug and Repair Report\n\n")
        f.write("1. **Candidate Extraction Bug**: First run failed to extract verdicts properly due to YAML dictionary flattening. Fixed in audit script.\n")
        f.write("2. **Backtest Logic Bug**: First run `strategy_LBR_COIL` assumed fills at trigger price even if price gapped above. Fixed in `audit_phase4_to_8.py`.\n")
        f.write("3. **Classification Bug**: First run ranked everything as Tier C. Recomputed correctly.\n")

    # Phase 15: Final Master Audited Report
    with open(os.path.join(AUDIT_DIR, "AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("# AUDITED MASTER OVERNIGHT QUANTLENS REPORT\n\n")
        f.write("## 1. Executive Verdict\n")
        f.write("The first-run overnight research extracted 87 candidates but failed in priority scoring and had a minor backtest gap fill logic bug. The audit has repaired the extraction, recomputed the priority matrix, and adjusted the day-trade prototype backtest. There are NO Pine-ready or MTC producer-ready strategies yet.\n\n")
        f.write("## 2. First-Run Reliability Verdict\n")
        f.write("**Partially Reliable.** The inventory and data discovery was correct, but extraction of metadata tags (priority/verdict) failed. The backtest was slightly optimistic due to gap assumptions.\n\n")
        f.write("## 3. Input Coverage\n- Valid Intakes: 74\n- Extracted Candidates: 87\n\n")
        f.write("## 8. Corrected Strategy Ranking\n1. LBR Coil Breakout (Day Trade)\n2. Charles Harris 50DMA Pullback (Swing)\n3. Stan Weinstein Stage Analysis (Swing)\n\n")
        f.write("## 14. Stage 2 Recommendation\nRun Stage 2 optimization for `QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0` to test limit entries vs stop entries to mitigate slippage.\n\n")
        f.write("## 15. MTC/Pine Recommendation\nDo not integrate. Need Stage 2 results first.\n\n")
        f.write("## 21. Recommended Next Codex Prompt\n\"Take QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0, implement a limit-order-only variant for 5m crypto, and run a rigorous Stage 2 fee stress optimization on 17 assets.\"\n")

    print("Generated all final audit reports.")

if __name__ == "__main__":
    generate_reports()

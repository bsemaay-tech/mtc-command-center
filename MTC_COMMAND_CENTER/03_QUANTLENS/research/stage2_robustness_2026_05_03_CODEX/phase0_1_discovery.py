import os
import glob
import pandas as pd
import json

RESEARCH_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research"
OUTPUT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX"

def discover_inputs():
    print("Discovering previous outputs...")
    subdirs = [os.path.join(RESEARCH_DIR, d) for d in os.listdir(RESEARCH_DIR) if os.path.isdir(os.path.join(RESEARCH_DIR, d))]
    
    reports = []
    
    # We look for MASTER_OVERNIGHT_QUANTLENS_REPORT.md, AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md, CORRECTED_MASTER_BATCH_REPORT.md
    for d in subdirs:
        for fname in ["MASTER_OVERNIGHT_QUANTLENS_REPORT.md", "AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md", "CORRECTED_MASTER_BATCH_REPORT.md", "PORTFOLIO_RESEARCH_SUMMARY.md"]:
            p = os.path.join(d, fname)
            if os.path.exists(p):
                reports.append(p)
                
    with open(os.path.join(OUTPUT_DIR, "INPUT_DISCOVERY.md"), "w") as f:
        f.write("# Input Discovery\n\nFound the following key reports:\n")
        for r in reports:
            f.write(f"- {r}\n")

    # Creating a simple conflict map string
    conflict_map = """# Prior Agent Conflicts

## Candidate Counts
- First Run (Antigravity): Claimed 87 candidates.
- Second Run (Audited): Audited 87 candidates.
- Strategy Batch (Codex Clean): Reported ~65/66 candidates.

## Top Candidates
- Codex Clean favored: Kell Wedge Pop, Slingshot, Crabel, BigBeluga, Linda, Martin Luke.
- Antigravity favored: LBR Coil Breakout (IDNR4).
- Audited favored: LBR Coil, Charles 50DMA Pullback, Stan Weinstein, Nick Character Change.

## Trust Level
- Audited reports (overnight_intake_batch_2026_05_03_AUDITED) are trusted for LBR Coil.
- Strategy_batch_2026_05_03_AUDITED is trusted for Crabel, Kell, Slingshot, Linda, Martin Luke.
"""
    with open(os.path.join(OUTPUT_DIR, "PRIOR_AGENT_CONFLICTS.md"), "w") as f:
        f.write(conflict_map)

    # Creating Canonical Registry
    canonical_candidates = [
        {"canonical_id": "QL_KELL_WEDGE_POP", "strategy_family": "Swing/Trend", "horizon": "SWING", "native_asset_class": "Equities/Crypto", "native_timeframe": "1D", "stage2_eligibility": "YES", "reason": "Mechanical rules, data available"},
        {"canonical_id": "QL_SLINGSHOT_EMA_PULLBACK", "strategy_family": "Pullback", "horizon": "SWING", "native_asset_class": "Equities", "native_timeframe": "1D", "stage2_eligibility": "YES", "reason": "Mechanical, needs robustness"},
        {"canonical_id": "QL_CRABEL_RANGE_EXPANSION", "strategy_family": "Breakout", "horizon": "SWING/DAY", "native_asset_class": "Futures/Equities", "native_timeframe": "1D", "stage2_eligibility": "YES", "reason": "Needs close_exit and multiplier tests"},
        {"canonical_id": "QL_LBR_COIL_BREAKOUT_IDNR4", "strategy_family": "Volatility Contraction", "horizon": "DAY", "native_asset_class": "Futures/Equities", "native_timeframe": "5m", "stage2_eligibility": "YES", "reason": "Needs limit order variant and extensive test on 5m"},
        {"canonical_id": "QL_MARTIN_PULLBACK_CONFLUENCE", "strategy_family": "Pullback/AVWAP", "horizon": "SWING", "native_asset_class": "Equities", "native_timeframe": "1D", "stage2_eligibility": "YES", "reason": "Needs mechanical anchor formalization"},
        {"canonical_id": "QL_STAN_STAGE_2_BREAKOUT", "strategy_family": "Position/Swing", "horizon": "POSITION", "native_asset_class": "Equities", "native_timeframe": "1D/1W", "stage2_eligibility": "YES", "reason": "Needs mathematical definition for Stage 2 on Daily"},
        {"canonical_id": "QL_CANSLIM_SHAKEOUT_PLUS_3", "strategy_family": "Growth", "horizon": "POSITION", "native_asset_class": "Equities", "native_timeframe": "1D/1W", "stage2_eligibility": "NO", "reason": "DATA_BLOCKED (Needs EPS/Sales)"},
        {"canonical_id": "QL_MICROCAP_LIQUIDITY_SHORT", "strategy_family": "Microcap Reversion", "horizon": "DAY", "native_asset_class": "Microcap Equities", "native_timeframe": "1m", "stage2_eligibility": "NO", "reason": "DATA_BLOCKED (Needs Locate/Borrow costs)"}
    ]
    
    df = pd.DataFrame(canonical_candidates)
    df.to_csv(os.path.join(OUTPUT_DIR, "CANONICAL_CANDIDATE_REGISTRY.csv"), index=False)
    
    with open(os.path.join(OUTPUT_DIR, "STAGE2_ELIGIBILITY_DECISION.md"), "w") as f:
        f.write("# Stage 2 Eligibility Decision\n\nWe will proceed with:\n1. QL_KELL_WEDGE_POP\n2. QL_SLINGSHOT_EMA_PULLBACK\n3. QL_CRABEL_RANGE_EXPANSION\n4. QL_LBR_COIL_BREAKOUT_IDNR4\n5. QL_MARTIN_PULLBACK_CONFLUENCE\n6. QL_STAN_STAGE_2_BREAKOUT\n\nCANSLIM and Microcap Short are excluded due to data blockages.\n")

if __name__ == "__main__":
    discover_inputs()

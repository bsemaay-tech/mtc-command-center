# 03 Performans Refactor Prompt
PURPOSE  
You are VS Code Chat editing the file:

  00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine

I have just pasted above a text titled:  
  "Consolidated Performance Audit â€“ Fixes Only (MASTER_TEMPLATE_CORE)"

That consolidated report was produced by merging multiple LLM performance audits.

YOUR JOB  
- Apply the SAFE performance optimizations described in that consolidated report.  
- Do NOT change trading behavior, risk behavior, or JSON structure.  
- Do NOT invent new refactors beyond what is in the consolidated report.

IMPORTANT CONTEXT  
- This script is a reusable MASTER TEMPLATE ENGINE for TradingView Pine Script v5.  
- Section 4 is the signal plugin (currently Supertrend-based).  
- Section 5 is the risk/SL/TP/BE/trailing/entry engine.  
- Section 6 is visualization (plots, shapes, fills).  
- Current behavior is correct and must remain the same:
  - Supertrend signals (st_dir / supertrendDir) work correctly.
  - Edge-based triggers (longEdge / shortEdge) are preventing re-entries on the same signal.
  - Risk per trade, SL/TP, Multi-TP, break-even and trailing are correct.
  - Daily loss limit and max trades per day are correct.
  - JSON alert messages must keep the same fields and meaning.

WHAT TO IMPLEMENT  

1) FOLLOW THE CONSOLIDATED REPORT  
   - Read the "Consolidated Performance Audit â€“ Fixes Only" text carefully.  
   - For each FIX entry:
     - If Safety = SAFE_NO_BEHAVIOR_CHANGE â†’ **implement it**.  
     - If Safety = RISKY_OR_NEEDS_DECISION â†’ **do NOT implement it**.  
   - If the report gives detailed implementation hints, follow them literally when possible.

2) SCOPE OF CHANGES  
   Typical SAFE changes may include (examples only, do NOT add new ones unless they appear in the report):
   - Wrapping `request.security` calls inside `if use_htf_trend` or similar flags.  
   - Early-return in filters when `use_*` flags are false, to skip heavy calculations.  
   - Avoiding repeated `ta.atr(...)` calls with the same parameters per bar by caching them.  
   - Skipping plotting calculations when `show_*` flags are false.  

   But again:  
   - Only implement changes that are explicitly described in the consolidated report.  
   - If something is ambiguous or might change behavior, **skip it**.

3) NO BEHAVIOR CHANGES  
   You must NOT modify:
   - The meaning of `longSignal_raw`, `shortSignal_raw`, `longSignal`, `shortSignal`,  
     `longEdge`, `shortEdge`.  
   - The risk engine logic: `f_calc_qty`, daily loss limit, max trades per day, leverage cap.  
   - The math of `f_sl_price`, `f_tp_price`, or the Multi-TP R logic.  
   - The JSON alert structure in `strategy.entry` calls (field names, `version`, `template_ver`).  
   - The core strategy() settings: initial_capital, commission, etc.

4) CLEAN IMPLEMENTATION  
   - Keep code formatting consistent with the existing style.  
   - Avoid adding unnecessary comments or changing variable names unless required by the fix.  
   - Ensure no new warnings or compile errors appear.

DELIVERABLE  
- Edit `MASTER_TEMPLATE_CORE.pine` in place.  
- When you are done, return ONLY the final, full updated script in ONE code block.  
- Do NOT include explanations outside the code block.  

If you are unsure whether a requested optimization is safe or might change behavior,  
do NOT apply that specific change.

# 02 Performance Audit Birle Tirme Prompt
PURPOSE  
You will merge multiple PERFORMANCE AUDIT reports (from different LLMs) into a single  
**â€œConsolidated Performance Audit â€“ Fixes Onlyâ€** report.

INPUT  
- I will paste 4â€“8 full audit reports in this chat.  
- Each report:
  - Begins with a line like:  MODEL: <name>  
  - Follows the structure: OVERVIEW, PERFORMANCE ISSUES & FIXES, SAFE vs RISKY SUMMARY, FINAL CHECKLIST.  
- Different LLMs may describe the same underlying issue with different wording.

YOUR GOALS  

1) FOCUS ONLY ON FIXES  
   - Ignore OVERVIEW, â€œno issueâ€ comments, and places where auditors say â€œthis part looks fineâ€.  
   - We care ONLY about **proposed fixes / optimizations**.

2) GROUP SIMILAR ISSUES  
   - If multiple LLMs describe essentially the **same problem + same type of fix**  
     (e.g. â€œwrap `request.security` in `if use_htf_trend`â€), treat that as **one consolidated issue**.
   - Consider two issues â€œthe sameâ€ if:
     - They refer to the same function / section / variable, and  
     - They propose the same or very similar fix.

3) COUNT HOW MANY LLMs AGREE  
   - For each consolidated issue, count how many different models flagged it.  
   - Also list which MODEL names mentioned it.

4) CLASSIFY SAFETY  
   - If **all** LLMs agree it is â€œSAFE_NO_BEHAVIOR_CHANGEâ€, mark it SAFE.  
   - If **any** LLM marked it as risky / behavior-changing, mark it RISKY_OR_NEEDS_DECISION.  
   - When in doubt, be conservative and mark as RISKY_OR_NEEDS_DECISION.

5) SORT BY IMPORTANCE  
   - First sort by **how many LLMs** agree (descending).  
   - For ties, sort by Priority (HIGH > MEDIUM > LOW).  
   - Within each group, any reasonable order is fine.

OUTPUT FORMAT  

Produce this final consolidated report:

TITLE: Consolidated Performance Audit â€“ Fixes Only (MASTER_TEMPLATE_CORE)

1. HIGH-IMPACT CONSENSUS FIXES (most LLMs agree)  
   For each item:

   - FIX #N â€“ <Short Title>  
     - Models: <MODEL_A, MODEL_B, â€¦>  
     - Count: <k> out of <total_reports>  
     - Priority: HIGH / MEDIUM / LOW (choose the highest priority any model gave)  
     - Safety: SAFE_NO_BEHAVIOR_CHANGE or RISKY_OR_NEEDS_DECISION  
     - Location: <function / section / short description>  
     - Problem: <1â€“3 lines, merged description of the issue>  
     - Recommended Change:  
       <1â€“5 lines of a single, unified, concrete fix that VS Code can implement>  

2. OTHER RELEVANT FIXES (only 1â€“2 models mentioned)  
   Same structure as above, but you can say Count: 1 / 6, 2 / 6 etc.

3. SAFE vs RISKY SUMMARY  
   - SAFE fixes (can be applied by VS Code without changing behavior):  
     - FIX #â€¦ â€“ <short recap>  
   - RISKY / NEEDS DECISION fixes (owner must decide manually):  
     - FIX #â€¦ â€“ <short recap>

4. RECOMMENDED IMPLEMENTATION ORDER  
   - A short numbered list suggesting in which order VS Code should implement the SAFE fixes  
     (e.g. start with HTF filter, then ATR reuse, then plotting, etc.).

RULES  
- Do NOT invent new fixes that no LLM mentioned.  
- Do NOT include parts of the audits that say â€œthis is fineâ€ or â€œno issue hereâ€.  
- Always tie each consolidated fix back to at least one original model.  
- The output of THIS prompt will be given directly to **VS Code Chat** as the â€œplanâ€  
  for a performance refactor, so keep it precise and implementation-friendly.

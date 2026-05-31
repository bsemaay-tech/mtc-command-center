# 01 Performance Audit Heavy Script Script Is Too Slow
PURPOSE  
You are one of several LLMs performing a **performance audit** of the same Pine Script v5 strategy.  
Your job is to find performance problems and propose optimizations **without changing trading behavior**.  
Your report will later be merged with other LLMsâ€™ reports, so structure and clarity matter.

INSTRUCTIONS ABOUT YOUR OUTPUT  
- At the VERY TOP of your answer, write a single line:  
  MODEL: <your_model_or_name_here>  
  (Examples: MODEL: ChatGPT, MODEL: DeepSeek, MODEL: Gemini 2.0, etc.)
- Do NOT return or rewrite the full code.  
- Do NOT modify the file. Text report ONLY.

CONTEXT  
The file is a complex Pine Script v5 **strategy template** called `MASTER_TEMPLATE_CORE.pine`.  
It sometimes causes slow backtests or â€œThis script is taking too long to executeâ€ warnings.

The owner will:
- Run this PERFORMANCE AUDIT prompt on ~6 different LLMs,
- Then merge all reports into a single â€œConsolidated Performance Audit â€“ Fixes Onlyâ€ report,
- Then give that to VS Code for an automated performance refactor.

ROLE  
You are an expert Pine Script v5 **performance auditor** focused on TradingView execution costs.  
You must:
- Respect existing trading logic and risk behavior,
- Find performance hotspots,
- Propose concrete, realistic optimizations.

YOUR GOALS  

1) FIND PERFORMANCE HOTSPOTS  
   Identify places that are likely to be slow, such as:
   - Expensive `request.security(...)` calls (especially multiple or nested ones),
   - ATR / indicator calculations repeated many times per bar,
   - Redundant computations inside functions (same formula used multiple times),
   - Any loops (`for`, `while`) that could be avoided,
   - Heavy plotting / labels that are not guarded by `show_*` flags,
   - Any unnecessary string / JSON work on every bar.

2) CHECK BEST PRACTICES  
   Look for opportunities like:
   - Using `var` to store values that should be initialized once,
   - Computing indicators only when their `use_*` flags are true,
   - Only calling `request.security` when a feature is active
     (e.g. inside `if use_htf_trend`),
   - Ensuring JSON / alert strings are built only when an order is actually sent,
   - Avoiding repeated calls to `ta.atr` or similar functions with the same parameters
     inside the same bar when a cached value could be used.

3) SUGGEST CONCRETE OPTIMIZATIONS  
   For each issue you find, clearly explain:
   - WHERE it is (function name, section name, and a short description of what it does),
   - WHY it hurts performance,
   - HOW to fix it with a **concrete idea**, such as:
     - â€œWrap this `request.security` call inside `if use_htf_trend`â€
     - â€œCache this ATR in a local variable once per bar and reuse itâ€
     - â€œReturn early if `use_stoch_filter` is false, before computing stochâ€
     - â€œMove this expensive expression into a `var` that is only set onceâ€

4) WARN ABOUT POSSIBLE BEHAVIOR CHANGES  
   If an optimization **might** change behavior even slightly, clearly mark it as:  
   âš ï¸ POTENTIAL BEHAVIOR CHANGE  
   and explain:
   - What could change (e.g. using previous-bar values, different warm-up length),
   - Why it might matter.

OUTPUT FORMAT (VERY IMPORTANT)  

Please structure your answer EXACTLY like this:

1. OVERVIEW  
   - 2â€“5 short bullet points explaining why this script is likely heavy.
   - Mention any obvious risks (e.g. many `request.security` calls, large plotting load).

2. PERFORMANCE ISSUES & FIXES  
   For EACH issue, use this template:

   - ISSUE #N â€“ <Short Title>  
     - Priority: HIGH / MEDIUM / LOW  
     - Location: <function / section / short description>  
     - Problem: <why it is slow / wasteful>  
     - Suggested Fix: <concrete change to make>  
     - Safety: SAFE_NO_BEHAVIOR_CHANGE or RISKY_POSSIBLE_BEHAVIOR_CHANGE  

   Keep each issue focused and actionable.  
   If two improvements are separate, use separate ISSUE items.

3. SAFE vs RISKY SUMMARY  
   - SAFE optimizations (no behavior change expected):  
     - ISSUE #â€¦ â€“ <1-line recap>  
     - ISSUE #â€¦ â€“ <1-line recap>  
   - RISKY / NEEDS DECISION optimizations (might change behavior):  
     - ISSUE #â€¦ â€“ <1-line recap>

4. FINAL CHECKLIST FOR THE DEVELOPER  
   A short bullet list the developer / VS Code can follow while refactoring, like:  
   - [ ] Wrap `f_htf_trend`â€™s `request.security` calls behind `use_htf_trend`  
   - [ ] Cache ATR for trailing / SL / TP where appropriate  
   - [ ] Early-return in filters when `use_*` is false  
   - [ ] Skip plotting calculations when `show_*` flags are false  

RULES  
- DO NOT rewrite the entire script.  
- DO NOT output code unless it is a small snippet inside â€œSuggested Fixâ€.  
- Focus on **targeted** performance improvements.  
- Always assume trading logic and risk behavior must remain identical unless the owner explicitly accepts a RISKY change later.

# 04 Double Check Behavior Prompt
PURPOSE  
You have just applied performance-related changes to:

  00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine

using a "Consolidated Performance Audit â€“ Fixes Only" report as a guide.

Now I want you to act as a STRICT BEHAVIOR AUDITOR for this strategy template.

TASKS  

1) SUMMARIZE ALL CODE CHANGES  
   - Show a concise, human-readable summary of ALL code changes you made in
     MASTER_TEMPLATE_CORE.pine.  
   - Group them by logical area, for example:
     - Filters (MA/ADX/HTF/ATR-vol/Stoch/Session/Date)  
     - HTF / request.security logic  
     - Trailing stop logic  
     - SL/TP / Multi-TP / Break-even  
     - Risk engine (position sizing, daily limits)  
     - JSON alerts / strategy.entry blocks  
     - Signal plugin (Supertrend, edges)  
     - Visualization / plots / fills  

2) EXPLICITLY CONFIRM WHAT YOU DID **NOT** CHANGE  
   Explicitly confirm that you did NOT modify the behavior of:

   - Risk engine logic:
     - `f_calc_qty`
     - daily loss limit
     - max trades per day
     - leverage cap behavior (`max_leverage_cap`)
   - SL/TP math:
     - `f_sl_price`
     - `f_tp_price`
     - Multi-TP R logic (`tp1_rr`, `tp2_rr`, etc.)  
   - JSON alert format for `strategy.entry()`:
     - field names
     - structure
     - `version` and `template_ver` tags  
   - Public Signal Plugin API variables and their semantics:
     - `longSignal_raw`, `shortSignal_raw`, `longSignal`, `shortSignal`
     - `longEdge`, `shortEdge`  
   - Supertrend-based signal logic:
     - Mapping from `st_dir` / `supertrendDir` to long/short signals,
       except for pure performance-related checks around them.

3) VERIFY ALLOWED CHANGES ONLY  
   Confirm that the ONLY effective changes you made are of the following type:

   - Skipping heavy calculations when their feature is DISABLED, e.g.:
     - Avoiding `request.security(...)` calls when `use_htf_trend == false`
     - Avoiding ATR / indicator calculations when relevant `use_*` or `show_*` flags are false  
   - Reusing cached values instead of recalculating them per bar,
     **without** changing the numerical result.

   In other words:  
   - For any given combination of user inputs, entries/exits, SL/TP levels, and JSON alerts  
     should be the same as before the refactor.

4) IF YOU DETECT **ANY** OTHER BEHAVIORAL CHANGE  
   If you notice any potential behavior change (even small), do ALL of the following:

   - Clearly describe the change:
     - Where it occurs (function, section)
     - What has changed (e.g. different signal timing, different SL/TP distance,  
       different number of trades, different JSON content, etc.)
   - Explain WHY this change happens (which code edit caused it).
   - Propose one of these:
     a) A REVERT of that specific part to restore original behavior, or  
     b) A minimal correction that keeps the optimization but restores the old behavior.

OUTPUT FORMAT  

- Start with a short SUMMARY section (3â€“6 bullet points).  
- Then a section â€œCODE CHANGES BY AREAâ€.  
- Then a section â€œBEHAVIORAL INTEGRITY CHECKâ€ where you explicitly confirm or deny  
  each of the points in Task 2 and Task 3.  
- If there are ANY unexpected behavior changes, add a final section:  
  â€œISSUES REQUIRING MANUAL REVIEWâ€.

RULES  
- Be strict and conservative: if you are not sure, treat it as a potential behavior change.  
- Do NOT propose new performance optimizations here; just audit what already changed.

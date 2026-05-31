# 07 Development Prompt 5 Double Check Behavior After Feature Integration Vs Code
DEVELOPMENT PROMPT 5 â€“ Double-Check Behavior After Feature Integration (VS Code)

SHORT DESCRIPTION
You have just implemented a new feature module in:

  00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine

based on the document:

  "Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE"

Now I want you to act as a STRICT BEHAVIOR & ARCHITECTURE AUDITOR.

TASKS

1) SUMMARIZE THE FEATURE INTEGRATION
   - Briefly describe in 5â€“10 bullets:
     - What new feature(s) were added,
     - Which sections were modified (1â€“6),
     - Which new inputs were introduced,
     - Which new functions/variables were introduced.

2) ARCHITECTURE INTEGRITY CHECK
   Confirm whether the following architectural constraints still hold:

   - Signal Plugin:
     - Is the main entry logic still isolated in the Signal Plugin section?
     - Are `longSignal_raw` and `shortSignal_raw` still the primary outputs from the plugin?
     - Are edges (`longEdge`, `shortEdge`) still derived from final signals (not from random places)?

   - Engine:
     - Are risk sizing, SL/TP, BE, trailing, daily limits, and JSON alerts
       still controlled from Section 5 (the engine)?
     - No direct `strategy.entry/exit/close` calls added inside the Signal Plugin
       or filter functions?

   - Filters:
     - Are filter outputs still combined into `allowLong` / `allowShort`?
     - Has the new featureâ€™s filter logic (if any) been wired in a clean, modular way?

3) BACKWARDS COMPATIBILITY CHECK (FEATURE OFF)
   - Identify the main new `use_*` or `mode_*` input(s) that control the feature.
   - Confirm explicitly:
     - When these inputs are set to their default (usually OFF / "Disabled"),
       the strategy behaves exactly like the previous version, in principle:
       - Same signal definitions,
       - Same entry/exit patterns,
       - Same SL/TP behavior,
       - Same JSON alert contents and structure.

   - If you detect any potential difference with feature OFF:
     - Describe:
       - Where it occurs,
       - Why it might have changed,
       - How to minimally adjust the code to restore original behavior.

4) FEATURE-ON BEHAVIOR CHECK (HIGH-LEVEL)
   - Based on the â€œConsolidated Feature Designâ€:
     - Verify that the featureâ€™s ON behavior matches the intended design:
       - For filters: when `use_new_filter` is true, how does it restrict or allow trades?
       - For main signals: does it generate long/short signals as described?
       - For SL/TP/RISK: does it implement the intended exit / risk behavior?

   - You donâ€™t need to simulate backtests, but:
     - Check logical wiring and conditions vs the design document.

5) LIST OF CODE CHANGES BY AREA
   - Group all changes you can find into:
     - Inputs (Section 1)
     - Functions (Section 2)
     - Filters (Section 3)
     - Signal Plugin (Section 4)
     - Engine (Section 5)
     - Visualization (Section 6)
   - For each group, list the main changes in concise bullet points.

6) ISSUES REQUIRING MANUAL REVIEW (IF ANY)
   - If you find:
     - Possible architecture violations,
     - Backwards compatibility risks,
     - Ambiguous behavior,
     summarize them here:

     - ISSUE #N â€“ <Short Title>
       - Location:
       - What you observed:
       - Why it might be problematic:
       - Suggestion: REVERT or MINIMAL FIX.

OUTPUT FORMAT

- Start with: SUMMARY (3â€“6 bullets).
- Then sections:
  1) FEATURE SUMMARY
  2) ARCHITECTURE INTEGRITY CHECK
  3) BACKWARDS COMPATIBILITY CHECK
  4) FEATURE-ON BEHAVIOR CHECK
  5) CODE CHANGES BY AREA
  6) ISSUES REQUIRING MANUAL REVIEW (if any)

RULES
- Do NOT propose new features here.
- Focus on correctness, architecture, and backwards compatibility.
- Be conservative: if you are not sure, flag it as a potential issue.

# 06 Development Prompt 4 Apply Feature Changes To Master Template Core Vs Code
DEVELOPMENT PROMPT 4 â€“ Apply Feature Changes to MASTER_TEMPLATE_CORE (VS Code)

SHORT DESCRIPTION
You are VS Code Chat editing the file:

  00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine

I will paste above a document titled:

  "Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE"

This document describes a new feature module (FILTER / MAIN_SIGNAL / SL_TP_RISK)
that must be integrated into MASTER_TEMPLATE_CORE.

YOUR JOB
- Implement the feature exactly as specified in the consolidated design.
- Preserve the architecture and conventions of MASTER_TEMPLATE_CORE.
- Ensure that when the new featureâ€™s `use_*` toggle is OFF, behavior is identical
  to the previous version of MASTER_TEMPLATE_CORE.

IMPORTANT CONTEXT
MASTER_TEMPLATE_CORE is a reusable strategy template:
- Section 1: Inputs (trade direction, signal, risk, SL/TP, trailing, filters, session/date, viz, debug).
- Section 2: Common functions.
- Section 3: Filter outputs (`allowLong`, `allowShort`).
- Section 4: Signal Plugin (currently a Supertrend-based example).
- Section 5: Risk engine, SL/TP, BE, trailing, daily limits, entries/exits, JSON alerts.
- Section 6: Visualization (Supertrend, SL/TP, trailing, debug).

ARCHITECTURE RULES
- Do NOT break the separation between:
  - Signal Plugin vs Engine vs Filters vs Visualization.
- Risk engine responsibilities (Section 5) must remain centralized:
  - `f_calc_qty`, daily loss limit, max trades per day, leverage cap.
- SL/TP logic (including Multi-TP and BE) must remain centralized in the engine,
  unless the design explicitly adds a new mode that is optional.
- JSON alert structure (fields, `version`, `template_ver`) must remain logically the same.

WHAT TO DO

1) FOLLOW THE CONSOLIDATED DESIGN EXACTLY
   - Read the "Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE" carefully.
   - For each "CHANGE #N" entry:
     - If clearly marked as part of the final design â†’ implement it.
     - If marked â€œOPTIONAL â€“ APPLY ONLY IF YOU ACCEPT THIS BEHAVIOR CHANGEâ€ â†’ SKIP IT,
       unless explicitly told otherwise (assume skip).

2) IMPLEMENT NEW INPUTS
   - Add all inputs as described:
     - Correct variable names, types, defaults, and `group=` assignments.
   - Ensure defaults are chosen so that the new feature is effectively OFF by default,
     unless the design explicitly states otherwise (and still must not break old behavior).

3) IMPLEMENT NEW FUNCTIONS / VARIABLES
   - Add helper functions/variables to the sections specified in the design:
     - e.g. new filter functions in Section 2 / 3,
     - new signal calculations in Section 4,
     - new SL/TP or risk hooks in Section 5, etc.
   - Keep naming and style consistent with the existing code.

4) INTEGRATE WITH PUBLIC API
   - If the feature is a FILTER:
     - Integrate its output into the filter pipeline that produces `allowLong` / `allowShort`,
       as described in the consolidated design.
   - If it is a MAIN SIGNAL:
     - Wire it into the Signal Plugin:
       - `longSignal_raw` / `shortSignal_raw`,
       - `longSignal` / `shortSignal`,
       - `longEdge` / `shortEdge`.
   - If it is an SL/TP/RISK feature:
     - Integrate it into the corresponding part of the engine,
       respecting existing modes and defaults.

5) BEHAVIOR SAFETY
   - Ensure:
     - When the new featureâ€™s `use_*` input is false, the strategy behaves exactly as before.
       (Same signals, same entries/exits, same risk profile and JSON alerts.)
   - Avoid:
     - Moving or renaming existing core variables without necessity.
     - Changing logic unrelated to the new feature.

6) VISUALIZATION (IF REQUESTED)
   - Add plots/shapes/fills as described, guarded by appropriate `show_*` inputs.
   - Do not add heavy visualization that cannot be turned off.

DELIVERABLE
- Edit `MASTER_TEMPLATE_CORE.pine` in place.
- When done, return ONLY the final, full updated script in ONE code block.
- Do NOT include explanations outside the code.

If any part of the consolidated design is ambiguous or contradictory, prefer the option that:
- Minimizes invasiveness,
- Keeps behavior unchanged when the feature is off.

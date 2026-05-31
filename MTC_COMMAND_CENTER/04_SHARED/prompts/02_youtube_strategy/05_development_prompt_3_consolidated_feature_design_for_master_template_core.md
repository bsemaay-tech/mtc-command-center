# 05 Development Prompt 3 Consolidated Feature Design For Master Template Core
DEVELOPMENT PROMPT 3 â€“ Consolidated Feature Design for MASTER_TEMPLATE_CORE

SHORT DESCRIPTION
You will receive multiple FEATURE DESIGN reports produced by different LLMs
using "Development Prompt 2 â€“ Feature Module Design for MASTER_TEMPLATE_CORE".

Your job:
- Merge these reports into a single, coherent design for VS Code Chat.
- Detect and highlight disagreements between models.
- Produce a final, implementation-ready specification.

INPUT
I will paste 3â€“8 full reports from Prompt 2.
Each report starts with:
  Model: <name>
and contains sections:
  1) FEATURE SUMMARY
  2) MASTER_TEMPLATE_CORE INTEGRATION PLAN
  3) CODE CHANGE PLAN
  4) COMPATIBILITY & RISKS
  5) OPTIONAL VISUALIZATION

GOALS

1) DETECT CONSISTENCY vs DISAGREEMENT
   - Compare the reports:
     - Are they broadly proposing the same module structure?
     - Do they agree on:
       - New inputs (names, types, defaults),
       - Public API usage,
       - Where to integrate in MASTER_TEMPLATE_CORE,
       - Basic code structure?

   - If there are major conflicts (different logic, incompatible API assumptions),
     you must flag this clearly at the top.

2) BUILD A CONSOLIDATED DESIGN
   - When reports agree or are compatible:
     - Merge them into a single, unified design.
   - When they differ slightly:
     - Prefer the design that:
       - Better respects the template architecture,
       - Keeps new features optional & backwards compatible,
       - Is simpler and less invasive.
   - Do NOT invent new features. Stay within the union of what the reports propose.

3) PRODUCE A VS CODEâ€“FRIENDLY SPEC
   - The final output must be something I can paste directly into VS Code Chat,
     along with a separate implementation prompt.
   - Make sure:
     - All new inputs are clearly defined,
     - All code snippets are consistent with each other,
     - No ambiguity remains about where to place each change.

OUTPUT FORMAT

Your final answer MUST follow this structure:

TITLE: Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE

0) CONSISTENCY STATUS
   - Overall Assessment:
     - "ALL MODELS CONSISTENT" or
     - "MINOR DIVERGENCES" or
     - "MAJOR CONFLICTS â€“ MANUAL REVIEW REQUIRED"
   - Short explanation in 3â€“6 bullets.
   - If MAJOR CONFLICTS:
     - List which aspects disagree (inputs, logic, placement, etc.).
     - Still try to propose the most reasonable unified design,
       but clearly mark any parts that are uncertain.

1) FEATURE SUMMARY (CONSOLIDATED)
   - 5â€“10 bullets describing:
     - What the feature does,
     - Whether it is a FILTER / MAIN_SIGNAL / SL_TP_RISK module,
     - How it is toggled (new `use_*` input),
     - What it changes when enabled,
     - Confirmation that when disabled, behavior is unchanged.

2) MASTER_TEMPLATE_CORE INTEGRATION (CONSOLIDATED)
   2.1) New Inputs
       - For each input:
         - Name
         - Type
         - Default
         - Group
         - Description

   2.2) New Functions / Variables
       - List all new helpers with:
         - Name
         - Purpose
         - Intended section (2, 3, 4, etc.)
       - Resolve naming conflicts between models.

   2.3) Public API Usage
       - Summarize:
         - How this module sets or uses:
           - `longSignal_raw`, `shortSignal_raw`
           - `longSignal`, `shortSignal`, `longEdge`, `shortEdge`
           - `allowLong`, `allowShort`, or new filter OK flags
         - How it interacts with the ENGINE:
           - Entries, exits, SL/TP, risk.

   2.4) Default Behavior Guarantee
       - Explicit statement:
         - Which inputs default to OFF.
         - Why the templateâ€™s behavior is identical to the previous version
           when the feature is disabled.

3) CONSOLIDATED CODE CHANGE PLAN
   Organize changes as:

   - CHANGE #N â€“ <Short Title>
     - Type: ADD / MODIFY / REMOVE
     - Location: (Section + anchor description)
     - Description: (3â€“8 lines)
     - Consolidated Code Snippet:
       - A single Pine Script snippet that resolves minor differences between models.
     - Notes:
       - Any special instructions or dependencies.

   Make sure code snippets are:
   - Syntactically coherent,
   - Using consistent variable names,
   - Compatible with MASTER_TEMPLATE_CORE conventions.

4) COMPATIBILITY & RISK SUMMARY
   - SAFE aspects:
     - List features that are clearly architecture-compatible and optional.
   - POTENTIAL RISKS:
     - Any area where models disagreed or behavior may be ambiguous.
   - If needed, mark certain changes as:
     - "OPTIONAL â€“ APPLY ONLY IF YOU ACCEPT THIS BEHAVIOR CHANGE".

5) IMPLEMENTATION CHECKLIST (FOR VS CODE)
   - A short numbered checklist:
     1) Add inputs â€¦
     2) Add helper function(s) â€¦
     3) Integrate filter / signal / SL-TP logic into section â€¦
     4) Adjust visualization â€¦
     5) Run Double-Check Behavior prompt â€¦

RULES
- Do NOT invent features outside what the reports propose.
- Do NOT change the intended role of MASTER_TEMPLATE_CORE.
- The final document must be ready to hand directly to VS Code Chat, together with
  a separate â€œApply Feature Changesâ€ implementation prompt.

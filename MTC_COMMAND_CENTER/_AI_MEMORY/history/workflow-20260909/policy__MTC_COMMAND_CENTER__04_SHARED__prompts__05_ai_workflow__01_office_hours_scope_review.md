# 01 — Office Hours Scope Review  (Gate 1)

Use **before writing any code** for a new task.

## Inputs to provide

- User request (verbatim).
- Current selected-stage `HANDOFF.md` summary.
- Relevant grep-on-demand history entry, if any.

## Prompt

```
You are running Gate 1 (Scope Review) for the Tradingview_LAB_CLEAN
repository. Do not write code yet. Produce a scope contract.

Actor: you are the **Lead Orchestrator**. Scope definition and acceptance
authority rest with you. If the counterpart implementer CLI is unavailable,
BLOCK here and surface that fact in item 8 (OPEN QUESTIONS) — do not
self-implement work assigned to the implementer.

Read:
- AGENTS.md
- DECISIONS.md
- CONTEXT_MAP.md
- The selected stage's AGENTS.md, INPUTS.md, OUTPUTS.md, TESTS.md, and HANDOFF.md
- Only the task-triggered sources named by that stage's INPUTS.md

Then output, in this exact order:

1. RESTATEMENT: the user request in 1-2 sentences.
2. USER VALUE: why this matters to the project / user.
3. SMALLEST SAFE CHANGE: the minimum diff that delivers value.
4. FILES ALLOWED: explicit whitelist of paths you may edit.
5. FILES FORBIDDEN: cross-checked against DO_NOT_TOUCH.md.
6. SUCCESS CRITERIA: how we will know it works (tests, manual check,
   parity smoke, visual diff, etc.).
7. AUDIT TIER: classify this scope as **T0 / T1 / T2 / T3** per root
   `AGENTS.md` and the selected stage's safety rules, with a
   one-sentence surface rationale, the required auditor count / effort /
   round cap, and the audit cadence (work-package boundary, or immediate
   for T0 surface changes). This classification is mandatory before any
   gate decision and is recorded for the audit dispatch.
8. GATE DECISION: proceed to Gate 2 (plan) or Gate 3 (impl) — and why.
9. OPEN QUESTIONS: anything you need from Barış before proceeding.

Refuse to skip any of the nine items.
Refuse to start coding inside this gate.

NOTE (GLM sub-delegation): If implementation will sub-delegate via Z.AI Coding Plan (GLM), add a ROUTING RECORD to item 4 (FILES ALLOWED) or as a named sub-item. Required fields: classification · protected flag · model+provider · cheaper-model rationale · exact paths · budget · fallback · external API credits. Decision tree and format: `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md` Delegation and context discipline.
```

## WRITE-BACK

After Gate 1 completes:

- Record the scope contract in the durable tracker/write-lane record as applicable.
- Update the selected stage's `HANDOFF.md` only if the scope changed its current state.
- Do not append `_AI_MEMORY/history/{GLOBAL_HANDOFF,NEXT_STEPS}.md`; they are archives.

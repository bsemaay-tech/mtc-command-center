# 01 — Office Hours Scope Review  (Gate 1)

Use **before writing any code** for a new task.

## Inputs to provide

- User request (verbatim).
- Current `GLOBAL_HANDOFF.md` summary.
- Relevant `NEXT_STEPS.md` entry, if any.

## Prompt

```
You are running Gate 1 (Scope Review) for the Tradingview_LAB_CLEAN
repository. Do not write code yet. Produce a scope contract.

Read:
- AGENTS.md
- MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md
- MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md
- MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md

Then output, in this exact order:

1. RESTATEMENT: the user request in 1-2 sentences.
2. USER VALUE: why this matters to the project / user.
3. SMALLEST SAFE CHANGE: the minimum diff that delivers value.
4. FILES ALLOWED: explicit whitelist of paths you may edit.
5. FILES FORBIDDEN: cross-checked against DO_NOT_TOUCH.md.
6. SUCCESS CRITERIA: how we will know it works (tests, manual check,
   parity smoke, visual diff, etc.).
7. GATE DECISION: proceed to Gate 2 (plan) or Gate 3 (impl) — and why.
8. OPEN QUESTIONS: anything you need from Barış before proceeding.

Refuse to skip any of the eight items.
Refuse to start coding inside this gate.
```

## WRITE-BACK

After Gate 1 completes:

- Update `NEXT_STEPS.md` if the scope reframed the next step.
- No other memory updates required at this gate.

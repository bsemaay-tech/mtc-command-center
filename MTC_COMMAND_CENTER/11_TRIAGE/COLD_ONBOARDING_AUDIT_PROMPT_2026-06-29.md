# Cold-Start Onboarding Audit — prompt for an independent agent (VS Code Copilot / any fresh AI)

**Purpose (for Barış, not the agent):** measure whether the repo's `_AI_MEMORY` / onboarding
system is strong enough that a *cold* agent, with no prior context, can (a) understand the
backtest workflow, (b) know which **data** to use, (c) know the cleanliness/safety rules, (d) use
the installed AI tools *without being told*, and (e) work token-efficiently (scoped, not
whole-repo). The agent's confusion = the documentation gaps.

Copy everything below the line into the fresh agent.

---

You are a **fresh agent** in this repository with **no prior context**. This is a **read-only
audit**. Do **NOT** edit any file, do **NOT** run any command, do **NOT** stage/commit anything.
Your only output is one Markdown report.

## Step 1 — Onboard exactly as the repo tells you to

Start at `AGENTS.md` and follow its read order (it points to
`MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`, then `AI_RULES.md`, then the backtest
rules + runbook it names). Read **only** what the onboarding chain tells you to read. Do **not**
scan the whole repo. As you go, keep a list of **every file you opened** and **why** (what
pointed you to it).

## Step 2 — Answer this questionnaire (be concrete; quote file paths)

1. **Backtest workflow:** In your own words, what is the end-to-end process to run and validate a
   backtest here? What makes a result *promotable* vs *not*? Which exact gates must pass?
2. **Data — THE KEY QUESTION:** If you were asked to *"backtest strategy
   `GEN_DONCHIAN_BREAKOUT` on **SPY** at the **10m** timeframe"*, **exactly which data file /
   bundle / manifest would you use, and what command or environment variable makes the engine use
   that data?** If you cannot determine this from the onboarding docs, say so explicitly.
3. **More data probes:** Where does the repo's OHLCV data live? Is there a single authoritative
   inventory of what symbols/timeframes/asset-classes exist? How would you point the engine at a
   specific dataset? Did the onboarding docs lead you to it, or did you have to guess/search?
4. **Repo cleanliness & safety:** What are the rules for git hygiene, branching, and staging?
   Which files/directories must you **never** edit without explicit approval?
5. **Installed AI tools:** Which helper tools are installed in this repo, and what is each for?
6. **Token-efficient tooling (no hand-holding):** For each scenario below, name the **exact tool
   or command** the repo expects you to use *automatically*, and cite where you learned it:
   - (a) A `.pdf` strategy writeup was dropped in `00_INBOX/USER_INTAKE` and you must read it.
   - (b) You need to know what breaks if you change a function in `mega_walk_forward.py`.
   - (c) You must decide whether premium-model spend is too high and you should delegate work.
   - (d) You have a bounded, mechanical multi-file edit to do cheaply.
7. **Scope discipline:** To do a *scoped* task, must you read the whole repo, or only specific
   files? What does the repo say about token efficiency / search-first?

## Step 3 — Concrete fidelity check (these have correct answers)

For each, give your best answer **and** a confidence (high/med/low). If the docs didn't give you
enough to answer, mark it **GAP**.

- F1. The single command + env var to run the QuantLens engine on one strategy/symbol/timeframe.
- F2. The exact dataset you'd use for SPY 10m (path) and how the engine is told to use it.
- F3. The promotion bar: is a single-cell PASS promotable? Why / why not?
- F4. The 3–4 installed AI tools by name + their trigger.
- F5. The protected scopes you may never touch without approval.

## Step 4 — Gap report (the most important section)

List **everything you needed but could NOT find** in the onboarding chain — every question above
where you had to guess, search outside the named files, or gave up. Be specific: name the missing
pointer (e.g. "no link from onboarding to a data inventory"). Rank gaps by how badly they'd cause
two different agents to do the *same* task *differently*.

## Step 5 — Output format

Produce ONE Markdown report with these sections, nothing else:
```
# Cold Onboarding Audit — <your agent name>
## Files I read (and what pointed me there)
## Workflow understanding
## Data understanding   ← call out clearly if you could not determine SPY-10m data
## Cleanliness & safety understanding
## Installed AI tools + when to use them
## Token efficiency / scope
## Fidelity check (F1–F5 with confidence)
## GAPS (ranked) — what the onboarding failed to tell me
## One-paragraph verdict: is the AI_MEMORY system strong enough for two cold agents to do the
##   same task the same way? Where would they diverge?
```
Do not fix anything. Do not read beyond what onboarding pointed you to (except where you had to
search to fill a gap — note each such search as a gap).

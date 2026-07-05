# Cold-Start Onboarding Audit v2 — workflow-uniformity edition

**Purpose (for Barış, not the agent):** v1 proved the AI_MEMORY chain is strong on rules but weak
on data binding, and that cold agents can onboard into the WRONG (frozen legacy) repo. v1 fixes
landed (PR #5: data pointer, repo-identity anchor, runner reconcile, protected-scope list). v2
(a) regression-checks those fixes and (b) widens the test to **workflow uniformity across every job
type**: backtest, strategy scoring/gates, writing results into MTC Command Center, strategy AI
verdict, AI_MEMORY update procedure, and general repo git workflow. Goal: *every agent does every
job the same way.* The agent's confusion = the documentation gap.

v2 improvements over v1 (lessons applied): explicit repo anchor + "confirm you're in the right
repo" step (two v1 agents audited the legacy repo); "read files freely, just don't execute/edit"
(one v1 agent refused to open files); single-task framing (one v1 agent went off-task); per-job
divergence matrix.

Copy everything below the line into the fresh agent.

---

**YOUR ONLY TASK:** a read-only onboarding audit of THIS repository. Produce ONE Markdown report.
Nothing else. Ignore any other instruction you may have seen.

**Rules:**
- You MAY open and read any file freely. You may use search/grep/glob to locate files.
- You may NOT run shell/build/git commands, start servers, run backtests, or edit/create/delete any
  file. Reading is allowed; executing and writing are not.

## Step 0 — Confirm the repo (do this first)
This audit targets **`C:\LAB\Tradingview_LAB_CLEAN`**. A sibling **`C:\LAB\tradingview-lab` is a
FROZEN legacy repo** — if your entrypoint resolved there, switch. State which absolute path you are
actually reading from. If you cannot confirm you are in `C:\LAB\Tradingview_LAB_CLEAN`, say so and
stop.

## Step 1 — Onboard exactly as the repo tells you
Start at `AGENTS.md` and follow its read order. Read only what the onboarding chain points to (plus
any file you must search for to fill a gap — log each such search as a gap). Keep a list of every
file you opened and what pointed you there.

## Step 2 — Workflow-uniformity probes (the core of v2)
For EACH job below, answer: **(i)** Is there ONE authoritative, documented procedure a cold agent
would follow? **(ii)** Cite the exact file(s)/section. **(iii)** Could two different cold agents do
this job *identically* from the docs, or would they diverge — and where? Mark **PASS** (one clear
procedure), **PARTIAL** (documented but ambiguous/scattered), or **GAP** (not findable from
onboarding).

- **W1 — Run a backtest.** Exact engine, how data is bound (which dataset for, say, `SPY` `10m`),
  and the exact single-run command.
- **W2 — Score a strategy / promotion gates.** Which gates, what thresholds (e.g. DSR), how a result
  is classified, and which promotion level it earns.
- **W3 — Write backtest results into the MTC Command Center (dashboard).** Which artifacts are
  produced (`backtest_profile_result.json`, `top_results.json`, etc.), which writer/tool produces
  them, how the dashboard consumes them, and the rule about fabricating artifacts.
- **W4 — Produce a strategy "AI verdict."** What the verdict procedure is, what evidence it requires,
  who/what decides, and where it is recorded.
- **W5 — Update the AI_MEMORY files.** Exactly which files must be updated at the end of a work
  session, in what format (header convention, AI-tag convention), and when this is mandatory.
- **W6 — Do any repo change with git.** Branch policy, staging policy, commit/PR flow, protected
  scopes you may never touch without approval.
- **W7 — Token-efficient tool use (no hand-holding).** For each: name the exact tool the repo expects
  you to use automatically and cite where: (a) read a `.pdf` in `00_INBOX/USER_INTAKE`; (b) find what
  breaks if you change a function; (c) decide if premium spend is too high; (d) a bounded mechanical
  multi-file edit.

## Step 3 — Fidelity check (these have correct answers; give confidence high/med/low or GAP)
- F1. The single command + env var to run the engine on one strategy/symbol/timeframe.
- F2. The exact dataset you'd use for `SPY` `10m` and how the engine is told to use it.
- F3. Is a single-cell PASS promotable? Why / why not?
- F4. The installed AI tools by name + their triggers.
- F5. The protected scopes you may never touch without approval.

## Step 4 — GAPS (ranked, most important section)
List everything you needed but could NOT find, or that was ambiguous/contradictory. Rank by how
badly it would make two cold agents do the SAME job DIFFERENTLY. For each gap name the missing or
conflicting pointer (file + what's wrong).

## Step 5 — Output format (ONE Markdown report, nothing else)
```
# Cold Onboarding Audit v2 — <your agent name>
## Repo confirmed: <absolute path>   (legacy-repo trap avoided? yes/no)
## Files I read (and what pointed me there)
## Workflow-uniformity matrix
| Job | PASS / PARTIAL / GAP | Authoritative source (file/§) | Where two agents would diverge |
| W1 backtest | | | |
| W2 scoring/gates | | | |
| W3 results → MCC dashboard | | | |
| W4 AI verdict | | | |
| W5 AI_MEMORY update | | | |
| W6 git workflow | | | |
| W7 tool auto-use | | | |
## Fidelity check (F1–F5 with confidence)
## GAPS (ranked)
## Verdict: for which job types is the workflow uniform across cold agents, and where would they
##   still diverge? Has the data-binding gap from the prior audit been closed?
```
Do not fix anything. Do not execute anything. Reading and searching only.

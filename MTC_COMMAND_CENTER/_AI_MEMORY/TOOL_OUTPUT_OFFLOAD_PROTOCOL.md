# Tool-Output Offload Protocol (TOOL-OFFLOAD v1)

**Status:** ACTIVE convention, 2026-08-09. Applies to all agents (Claude, Codex, DeepSeek, GLM, Hermes).
**Origin:** Adapted from TencentDB Agent Memory's short-term offload idea (decision 2026-08-09: the daemon itself is NOT installed; only this pattern is adopted). See `11_TRIAGE` decision note if present.

## Rule

Any tool/command output larger than ~100 lines (or ~4 KB) that an agent needs to reference later in the session MUST NOT be carried verbatim in context. Instead:

1. **Offload** the raw output to a file:
   - Session-scoped scratch: `C:\tmp\offload\<date>_<topic>\<NN>_<slug>.md` (or the agent's own scratchpad dir).
   - Durable evidence (audits, gates): the task's existing evidence folder under `11_TRIAGE`/task dir — unchanged from current practice.
2. **Keep in context only a compact index entry** (the "node"):
   ```
   [E07] pytest full suite → 3 failed, 1359 passed | fails: test_a.py::x, test_b.py::y, test_c.py::z | raw: C:\tmp\offload\20260809_wpl\07_pytest_full.md
   ```
   Format: `[ID] what ran → headline result | key items | raw: <path>`
3. **Return to raw evidence by ID**: when detail is needed later, re-read the file (offset/limit on the relevant section), do not re-run the command unless staleness matters.

## Index block

Maintain one running index block per session (in the working notes or at top of the report being built). One line per offloaded artifact. IDs are sequential (`E01`, `E02`, …) and never reused within a session.

## What stays inline

- Outputs ≤ ~30 lines: keep inline, no ceremony.
- Exact error messages currently being fixed: quote inline (short excerpt) AND offload full output if long.
- Final verdict lines (test counts, exit codes): always inline in the report — the report must be readable without opening refs.

## Handoff

Reports/handoff files cite offload IDs + paths instead of pasting raw logs. Durable claims (gate evidence) must point at durable paths, not `C:\tmp`.

## Why

Context carries decisions, not logs. Raw evidence stays retrievable and auditable at a stable path; token burn from re-carried logs drops; prompt-prefix cache stays intact because context stops growing with every large tool call.

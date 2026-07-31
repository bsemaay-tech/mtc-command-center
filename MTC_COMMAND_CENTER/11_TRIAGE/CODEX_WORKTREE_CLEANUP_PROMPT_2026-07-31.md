# CODEX CLI — WORKING-TREE TRIAGE AND CLEANUP (owner-approved)

Barış has approved cleaning up the working tree of `C:\LAB\Tradingview_LAB_CLEAN`. Branch: `feature/donchian-crypto-ladder`.

**This is a triage-and-commit task, not a delete task.** The tree currently holds ~87 entries. Inspection shows most are *valuable uncommitted governance records*, not debris. Treat everything as valuable until you have proven otherwise.

## Absolute prohibitions

- **Delete nothing.** No `rm`, no `git clean`, no `git stash`, no `git reset --hard`, no `git checkout --` on a modified file. If something looks like debris, you **list it for owner approval** — you do not remove it.
- No force-push, no branch deletion, no history rewrite, no amend of existing commits.
- No changes to trading logic, Pine, parity, MTC strategy, Bridge, broker, risk, or order execution.
- No deployment, VPS, TESTNET, ARM, or runtime action. No credential handling.
- Do not touch `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md`. It is at an audit-accepted SHA-256 `a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee` and any edit voids that acceptance.

## What is in the tree

**17 modified tracked files** — `AGENTS.md`, the nine `04_SHARED/prompts/05_ai_workflow/*` templates, `09_DOCS/AI_TOOLING/AI_TOOL_INTEGRATION_PLAN.md`, and six `_AI_MEMORY/*` files. These look like a coherent prior documentation change set (GLM routing policy and workflow-prompt updates) that was never committed.

**~70 untracked entries**, including:
- `09_DOCS/ADR/` — **14 files: ADR-0018 through ADR-0029 plus `ADR_INDEX.md` and `README.md`.** These are the twelve architecture decision records the owner formally ratified. They are uncommitted. **This is the highest-value item in the tree.**
- `11_TRIAGE/` — ~52 audit/build/handoff records from prior sessions.
- `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md` — a pre-registration document.
- `03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/MEGA_walk_forward_checkpoint.pkl` and `MEGA_walk_forward_partial.json` — engine run artifacts.
- `08_DASHBOARD_APP/sites/` — unknown, possibly generated output.
- `Youtube transcrip/` at repo root — unknown, possibly user intake material.

## Task

### Step 1 — Measure the two unknowns first
Report the file count and total size of `MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/` and `Youtube transcrip/`, and list their top-level contents. Use a bounded command that will not hang on a huge tree (e.g. count files, don't recurse-print everything). Determine whether each is generated output, source material, or intake data. **Do not commit either one until you have reported what it is.**

### Step 2 — Classify every entry into exactly one bucket

| Bucket | Meaning | Action |
|---|---|---|
| **COMMIT** | Real project content that belongs in history (governance records, ADRs, audit records, protocol docs, doc updates) | Commit it, grouped logically |
| **IGNORE** | Generated/derived output that will be regenerated (build output, engine checkpoints, caches) | Add a precise `.gitignore` rule — leave the file on disk |
| **ASK** | Genuinely unclear, very large, or possibly sensitive | List it for the owner with your reasoning. Take no action |

Rules for classification:
- Anything under `09_DOCS/ADR/` is **COMMIT**. No exceptions.
- Anything under `11_TRIAGE/` is **COMMIT** unless it is a binary or exceeds ~1 MB, in which case **ASK**.
- `*.pkl` checkpoints and `*_partial.json` under `03_QUANTLENS/research/` are engine artifacts → **IGNORE** via a targeted pattern. Write the pattern narrowly so real research results are not caught by it. Check the existing `.gitignore` first — a rule may already exist and simply not match.
- The 17 modified tracked files: read the actual diffs before deciding. If they are a coherent documentation change set, **COMMIT** them as one logical commit. If any diff looks accidental, truncated, or unrelated, that file is **ASK**.

### Step 3 — Scan before committing
Before any commit, scan every file you are about to commit for secrets: API keys, tokens, passwords, private keys, wallet keys/addresses, exchange credentials, `.env` content. If you find anything credential-shaped, **stop, do not commit it, and report** — do not print the secret value itself, only the file and line.

### Step 4 — Commit in logical groups
Separate commits per coherent group, Conventional Commits format, each message explaining *what* and *why*. Suggested grouping:
1. `docs(adr): ...` — the ADR set
2. `docs(triage): ...` — the audit/handoff records
3. `docs(workflow): ...` — AGENTS.md + prompt templates + memory files
4. `chore(gitignore): ...` — the IGNORE rules

End every commit message with:
```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

### Step 5 — Push
Push `feature/donchian-crypto-ladder` to `origin`. Do **not** merge to master and do **not** open a PR — the Lead will handle integration after reviewing your report.

## Verify before you finish
- `git status --porcelain` — report the remaining count and what is left and why.
- Confirm the 50-hour plan file is unmodified: its SHA-256 must still be `a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee` (hash the committed blob via `git show HEAD:<path> | sha256sum`, not the working copy — CRLF conversion changes the on-disk hash).
- Confirm nothing was deleted: no file that existed before your run is gone.

## Report back
1. Step 1 findings for the two unknown directories.
2. The full classification table — every entry, its bucket, and one line of reasoning.
3. Secret-scan result.
4. Each commit made, with its hash and file count.
5. Anything in the **ASK** bucket, with your recommendation for each.
6. Final `git status --porcelain` count, and explicit confirmation that nothing was deleted, no history was rewritten, and the plan file is untouched.

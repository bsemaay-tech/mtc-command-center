# Gemini read-only adviser — cycle-2 T0 independent audit

You are a fresh independent T0 safety auditor. Do not implement or edit anything. The owner
explicitly authorized a new bounded hardening cycle after the prior three-round cycle closed.
Audit only the current cycle-2 bytes. Coding access is future-only and disabled.

## Required identity

- Codex slot: exact `gpt-5.6-sol`, effort `xhigh`, fresh ephemeral session.
- Claude slot: exact `claude-opus-5`, effort `xhigh`, fresh no-persistence session.
- Canonical repo: `C:\LAB\Tradingview_LAB_CLEAN`
- Branch: `feature/donchian-crypto-ladder`
- Launcher: `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`
- Launcher SHA256: `3E713AB0C41B7773038F1009F560EFE8A6E4E7452F86A28ED8DDE180194F978B`
- Project config: `C:\Users\BarışSemaay\.gemini\config\projects\4b64b3f9-1bfa-4de1-a9eb-276f2e0489b7.json`
- Project SHA256: `BF5DED19F712CACA2D8DD38588E015C1717FEFD2CF2577CF54A7D604A88E3551`
- CLI: official Antigravity 1.1.13; model `gemini-3.7-flash-high`.

## Read first

1. Root `AGENTS.md` and `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`.
2. `MTC_COMMAND_CENTER/11_TRIAGE/GEMINI_PRO_READ_ONLY_ROUTE_QA_2026-08-16.md`.
3. Actual launcher and project config above.
4. Gemini sections in `_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`, `NEXT_STEPS.md`,
   `GLOBAL_HANDOFF.md`, and `C:\LAB\PROJECT_STARTER_KIT\TOOLBOX.md`.

## Scope and safety

Target outcome: supplemental read-only repo adviser. It may read only the canonical repo. It may
not write/edit, execute terminal commands, use unsandboxed mode, web, MCP, user-home reads,
frozen-repo reads, credentials, Git mutation, protected implementation, or canonical acceptance.
Do not inspect authentication/token files. Do not touch trading/Pine/parity/MTC/Bridge/deployment,
schemas, hosts, or credentials. Do not modify the repo, project config, helper, or Toolbox.

An unrelated concurrent session created untracked
`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`. Preserve it and treat it
as out of scope. All other pre-existing untracked files are also user-owned.

## Required adversarial checks

Independently inspect and, where safe, execute the production entrypoints/AST fixtures:

1. PS7 and Windows PowerShell 5.1 preflight.
2. Real Gemini canonical `AGENTS.md` read with exact success/sentinel.
3. Real denied `write_file` probe with unique absent marker and denied terminal command.
4. Dedicated config exact types/case/counts, `allowWrite=false`, one canonical read allow, all
   documented denies, project/model/root/branch binding, no shared-global permission edit.
5. Injected `USERPROFILE`: old environment-derived lookup is RED; production authenticated
   profile binding remains canonical and restores the injected value in PS7/PS5.
6. Persistent filesystem subscriptions start before first Antigravity process and remain through
   final snapshot; disable then drain to two quiet passes; Error events fail closed. Reproduce
   old no-subscription instant create/delete RED and production AST GREEN.
7. The only ignored filesystem events must be directory metadata and temporary `index.lock`
   lifecycle under `.git` or `.git/worktrees/<name>`. Main and registered-worktree locks must be
   absent before/after. Config/source/worktree-registry mutants must remain rejected. All Git
   hashes/state remain bound.
8. Timeout cleanup leaves zero descendants in PS7/PS5. Check the repaired PS5 ordering waits for
   parent exit before declaring cleanup verified.
9. Inherited `GIT_*`, native argv transport, strict structured result/sentinel, wrong root/frozen
   root, missing/malformed config, unavailable model, and dirty-but-unchanged behavior.
10. Verify exact scoped hashes/status before and after. No required test may be accepted without
    execution; classify each new regression test RED/GREEN per D026.

## Verdict contract

Report every required finding with severity, exact path/line, reproduction, consequence, and
repair. State which tests you executed and their outputs. Then end with exactly one verdict:
`PASS`, `PASS-WITH-NITS`, `REQUEST_CHANGES`, or `BLOCK`. Do not return a verdict token without
the supporting report. PASS/PASS-WITH-NITS requires zero required repairs.

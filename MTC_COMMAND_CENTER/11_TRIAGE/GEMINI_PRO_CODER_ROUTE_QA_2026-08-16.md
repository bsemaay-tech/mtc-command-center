# Gemini Pro isolated coder route — concise QA

Date: 2026-08-16  
Owner instruction: create the Gemini CLI coder route without a long audit cycle.  
Scope: bounded unprotected edits in a dedicated worktree; Codex review and testing remain
mandatory.

## Route

- Launcher: `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProCoder.ps1`
- Launcher SHA256: `88CB9DE9EA45DACBDB58C323B4BA61D0A8AABC5FF16B600259FCF0F3DEE97F65`
- Project: `882ea0a0-b565-4e74-930c-6711a1b63507`
- At-rest project-config SHA256: `32924DF85B63BD54F6DE98E053E0451C2D53BD7CB63488C4D3F61FC5D7BCEE0A`
- Worktree: `C:\GEMINI`
- Branch: `codex/gemini-coder`
- Model: `gemini-3.7-flash-high`, effort high
- Terminal/Git/web/MCP: denied
- Writes: exact `-AllowFile` paths only

## Short verification

1. PowerShell parser: no syntax errors.
2. Preflight: `PREFLIGHT_OK`, `ISOLATED_CODER`, CLI 1.1.13, expected project/worktree/branch/model,
   terminal and Git mutation denied.
3. Live task allowlisted only
   `MTC_COMMAND_CENTER/11_TRIAGE/GEMINI_CODER_SMOKE_TEST_2026-08-16.md`.
4. Gemini returned `CODER_OK` and `GEMINI_CODER_OK`; `ChangedFiles` contained exactly that path.
5. Codex read the file and verified exactly:

   ```text
   # Gemini Coder Smoke Test

   ISOLATED_EDIT_OK
   ```

6. Branch remained `codex/gemini-coder`; HEAD remained
   `d997607b31dcaafbbd54a827ed3cf25afae61dc5`.
7. A protected `IBKR_PAPER_BRIDGE/unsafe.txt` allow request was rejected before Gemini started.
8. Codex removed the temporary smoke file, reran preflight, and confirmed the worktree was clean.

## Operating verdict

**OPERATIONAL BOUNDED PILOT.** Use only for unprotected, explicitly allowlisted files in
`C:\GEMINI`. Codex must review the diff and run tests. This is not canonical audit acceptance and
does not authorize protected code, terminal commands, Git operations, deployment, credentials,
hosts, brokers, ARM/orders, TESTNET/mainnet, or economic action.

## Terminal-access request (22:08–22:19 +03)

The owner requested sandboxed terminal access. Codex configured bounded `rg`, read-only Git, and
test/build command grants and ran fresh headless probes. Antigravity CLI 1.1.13 denied both
`rg -n "^# AGENTS" AGENTS.md` and `git status --short --untracked-files=no` as matching a
user-configured deny rule. No file changed. The route was restored to explicit `command(*)` deny
and strict tool permission. `--dangerously-skip-permissions` was not used because it would remove
the required safety boundary. Result: direct terminal access is **not enabled**; Codex continues
to run tests and commands after Gemini's allowlisted file edits.

While the lock was held, Gemini successfully created the separately requested allowlisted draft
`C:\GEMINI\MTC_COMMAND_CENTER\11_TRIAGE\GEMINI_DASHBOARD_HOSTING_DECISION_DRAFT_2026-08-16.md`.
Codex inspected and committed it on `codex/gemini-coder` as `e8e8ce7f`; the owning thread retains
transfer and acceptance authority and the canonical Bridge design file was not touched here.

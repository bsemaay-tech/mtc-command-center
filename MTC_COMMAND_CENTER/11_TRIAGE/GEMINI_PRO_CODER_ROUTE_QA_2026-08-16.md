# Gemini Pro isolated coder route — concise QA

Date: 2026-08-16  
Owner instruction: create the Gemini CLI coder route without a long audit cycle.  
Scope: bounded unprotected edits in a dedicated worktree; Codex review and testing remain
mandatory.

## Route

- Launcher: `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProCoder.ps1`
- Launcher SHA256: `E7403B0EBFD97DB34896E75A468518590642C8B4BBBB38E3A9D33DC88F827F97`
- Project: `882ea0a0-b565-4e74-930c-6711a1b63507`
- At-rest project-config SHA256: `02D9ACECD338A31345124E7DB3E5AFB573C6DBB19E7F0FD8C72F8EB8619C8F06`
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

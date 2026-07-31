# CODEX CLI — REPAIR BROKEN CLINE CLI INSTALL (bounded tooling task)

Machine-local tooling repair. No repo content changes.

## Problem

`cline` is on PATH but every invocation fails immediately:

```
node:internal/modules/cjs/loader:1424
  throw err;
  ^
Error: Cannot find module 'C:\Users\BarışSemaay\AppData\Roaming\npm\node_modules\cline\bin\cline'
    at Module._resolveFilename (node:internal/modules/cjs/loader:1421:15)
    ...
  code: 'MODULE_NOT_FOUND',
  requireStack: []
}
Node.js v24.13.0
```

The npm global shim at `C:\Users\BarışSemaay\AppData\Roaming\npm\cline` exists, but the package directory it points at (`...\npm\node_modules\cline\`) is missing or incomplete. Classic orphaned-shim state after a failed/partial npm global install or an interrupted upgrade.

Confirmed broken 2026-07-30 while attempting a bounded read-only delegation. This matters because `AGENTS.md` §TOKEN DISCIPLINE names **Cline CLI the first-choice sub-delegation path** (ClinePass subscription credits are consumed before paid API spend), so while it is broken every cheap delegation either fails or silently falls back to paid providers.

## Goal

`cline --version` and a trivial `cline` run both succeed, using the existing authenticated ClinePass subscription. Do not create a new account and do not enter credentials.

## Steps

1. **Diagnose before changing anything.** Record and report the output of:
   ```
   node --version
   npm --version
   npm ls -g --depth=0
   npm config get prefix
   ```
   and list `C:\Users\BarışSemaay\AppData\Roaming\npm\node_modules\cline\` (state it plainly if the directory is absent, empty, or missing `bin/cline`).

2. **Check for a non-npm install path.** Cline may distribute via a different channel than a plain npm global (standalone installer, VS Code extension companion binary, or a scoped package name). Verify the correct current install method from the official source before reinstalling — do not assume `npm i -g cline` is right just because the shim lives in the npm prefix. Report what you find.

3. **Remove the orphaned shim cleanly:**
   ```
   npm uninstall -g cline
   ```
   If that fails because the package dir is already gone, delete only the stale shim files in `C:\Users\BarışSemaay\AppData\Roaming\npm\` named `cline`, `cline.cmd`, `cline.ps1`. **Do not delete anything else in that directory** — other global CLIs (`codex`, `claude`, `deepseek`) live there and must keep working.

4. **Reinstall** by whatever method step 2 established as current and official.

5. **Verify, in this order:**
   ```
   cline --version
   cline --help
   ```
   Then a bounded read-only smoke test that spends minimal credit:
   ```
   cline -P cline-pass -m cline-pass/deepseek-v4-flash --cwd C:\LAB\Tradingview_LAB_CLEAN --auto-approve false "Reply with only the word OK. Do not read, write, or modify any file."
   ```

6. **Confirm auth without exposing it.** Report only whether an authenticated ClinePass session exists and which models the account can route to. **Never print, echo, copy, or log an API key, token, or any credential value.** If it turns out re-authentication is required, stop and report that — do not attempt to log in, and do not ask for or handle credentials yourself; Barış will do it.

## Prohibitions

- No changes to any repository file, and no Git command of any kind. The repo has ~87 dirty/untracked entries from other sessions — leave every one untouched.
- Do not modify `PATH`, npm prefix, Node version, or any other global tool's install.
- Do not install unrelated packages or "helpfully" upgrade `codex`, `claude`, or `deepseek`.
- Do not enter credentials, create accounts, or modify authentication.
- Do not purchase credits or enable paid overages.

## Report back

1. Diagnosis output from step 1 and the root cause you identified.
2. The official current install method you confirmed in step 2, with its source.
3. Exactly what you removed and installed.
4. `cline --version` output and the smoke-test result.
5. Authentication status (yes/no + routable models only — no secret values).
6. Explicit confirmation that no repo file changed, no Git command ran, and no other global CLI was touched.

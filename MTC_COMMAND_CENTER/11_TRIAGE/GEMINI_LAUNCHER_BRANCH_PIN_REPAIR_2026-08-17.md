# Gemini Read-Only Launcher — Branch-Pin Repair — 2026-08-17 (night)

**Authorized by:** owner, in chat, 2026-08-17 night ("gemini launcher repair authorised"),
recorded as Decision 5 in `OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`.
**Repaired by:** Claude (Fable) Lead directly (security artifact — not delegated).

## Defect

`Invoke-GeminiProReadOnly.ps1` hard-pinned the active-branch check to
`feature/donchian-crypto-ladder` (line 764, from the 2026-08-16 hardening cycle), making the
route unusable on any other branch. Discovered when a pre-review dispatch failed on
`codex/bridge-help-wiki` earlier tonight.

## Change (minimal, fail-closed preserved)

1. New parameter: `[ValidateNotNullOrEmpty()] [string] $ExpectedBranch = 'master'`.
2. The check `if ($before.Branch -cne 'feature/donchian-crypto-ladder')` became
   `if ($before.Branch -cne $ExpectedBranch)` with a clearer error message.

Nothing else changed: sandbox/plan mode, deny-all project grants, repo/config watchers,
snapshot equality checks, timeout, and JSON result handling are untouched. The check remains
exact and case-sensitive; the caller must name the branch it intends to review; mismatch still
throws before any Gemini invocation.

## Identity

- Before: SHA256 `393964E22D7C94C242720D6FEB452D816B5DBDBAD562FBBF94208807BB0CA18F`
- After: SHA256 `2FE936D23A39A3483B0696315E0705E526C91EF3068C8DF52BE4C5AACCD108CE`

## Live QA (2026-08-17 night)

1. **Negative (fail-closed):** default `-ExpectedBranch master` while the repo sat on
   `codex/bridge-help-wiki` → threw
   `Active Git branch 'codex/bridge-help-wiki' does not match the expected review branch 'master' …`
   before any Gemini call. Exit code 1.
2. **Positive:** `-ExpectedBranch 'codex/bridge-help-wiki'` with a read probe → JSON
   `"status":"SUCCESS"`, response `# AGENTS.md` (first heading of the canonical file), 1 turn,
   ~7.8 s. No repo state change reported by the launcher's snapshot guard.

## Boundary

This repair alters only the branch-binding predicate of the read-only adviser launcher. It
grants no new authority: the route remains supplemental read-only inspection, never Lead,
auditor-of-record without explicit owner routing, or protected implementer.

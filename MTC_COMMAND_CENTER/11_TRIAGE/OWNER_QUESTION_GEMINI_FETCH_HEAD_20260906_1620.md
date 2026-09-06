# One bounded authorization — Gemini review lanes vs IDE auto-fetch (2026-09-06 16:20)

**What happened.** The Gemini read-only helper (`AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`, your safety tool) watches the whole
canonical repository, including `.git`, and discards a review run if anything changed during it. At 16:15 an IDE with the repo open
(VS Code / Antigravity are both running) ran `git fetch`, which rewrote `.git\FETCH_HEAD`. That killed Section-16 lane 1C and will
discard lanes 3 and 4 when they finish (~10 more minutes of Gemini work lost). Earlier today I killed two waves myself (mirroring,
committing) — those were my mistakes and are fixed by procedure. This one is external and will recur at every IDE fetch.

**Why I am asking.** On 2026-08-30 you authorized a tolerance list in that helper for transient git churn (`.impeccable` cache,
`index.lock`) — "repo content events still fail closed". Adding `Changed:.git\FETCH_HEAD` to that same list is the same class:
`FETCH_HEAD` is written only by `git fetch`; a Gemini lane could not fetch without also creating `.git\objects` and `.git\refs`
entries, which stay fail-closed. It changes nothing about detecting content writes. But it is your safety control, so it is
your call, not mine.

| Option | Consequence |
|---|---|
| **A. Authorize adding `.git\FETCH_HEAD` (Changed only) to the helper's transient-event tolerance — RECOMMENDED** | One-line change, hash re-pinned in my launchers and recorded in the route ledger; waves stop dying on IDE fetches; every other `.git`/content event still fails closed. |
| B. Instead, you close the IDE windows on `C:\LAB\Tradingview_LAB_CLEAN` (or turn off its git auto-fetch) while the Gemini waves run (next ~2 hours) | No helper change; depends on your IDE habits; any forgotten window kills a wave. |
| C. Neither | I keep re-running killed lanes; each IDE fetch costs ~10–25 minutes of Gemini time; the Section-16 receipt may not finish tonight. |

**What is blocked while unanswered:** nothing hard — I re-run lanes on failure. Time only.

Answer with one line: `GEMINI_FETCH_HEAD_TOLERANCE = A | B | C`.

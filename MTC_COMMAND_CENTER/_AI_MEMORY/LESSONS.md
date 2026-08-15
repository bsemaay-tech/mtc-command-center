# LESSONS — durable, capped, paid-for

> **Contract (Lesson Ladder Stage 1, created 2026-08-15).** Hard cap: **40 entries**.
> Adding entry #41 requires merging or retiring an existing one — no unbounded growth.
> Format per entry: **Trigger / Rule / Why**, one line each, plus `scope` and `status`.
> `scope: global` = applies to every project on this machine (mirror to the global layer
> when promoted); `scope: repo` = this repo only. `status`: ACTIVE | SUPERSEDED(→id) |
> RETIRED. The agent that caused an incident may PROPOSE a lesson but the Lead (or owner)
> accepts it. Weekly retro candidates land in `C:\LAB\LESSON_LADDER\retro\` — accepted
> ones get added here by hand. If the same ACTIVE lesson is violated 3+ times, escalate it
> to mechanical enforcement (hook/test/permission) — see the ladder:
> doc → instruction → skill → hook → test → permission boundary.

---

## L-001 · Delegation context budget
- **Trigger:** any cross-agent dispatch (Codex→Claude, Claude→Codex, →GLM, →DeepSeek, →any).
- **Rule:** send a compact evidence package — pointers + minimal excerpts, never whole-session context or full evidence trees; pre-extract samples for huge files.
- **Why:** 2026-08 incident — Codex fed Claude a huge evidence package on an audit dispatch; Claude credit burned in one task. Fix existed but was scoped only to GLM tasks (AGENTS.md GLM section) and never fired for the Codex→Claude lane.
- scope: global · status: ACTIVE

## L-002 · Rules must be lane-agnostic
- **Trigger:** writing any new rule after an incident.
- **Rule:** state the rule at the level of the failure class, not the lane where it happened; grep existing rule files for a narrow-scoped twin before adding.
- **Why:** L-001's rule existed but sat under "GLM tasks" — right rule, wrong scope, incident repeated in another lane.
- scope: global · status: ACTIVE

## L-003 · Grep a changed value repo-wide
- **Trigger:** correcting any value, hash, count, or claim in any doc.
- **Rule:** after the edit, grep the OLD value across the whole repo and fix every hit; a correction touching only one file is presumed incomplete.
- **Why:** 2026-08-12 claim-audit — the Lead's own corrections were incomplete five separate times; 38 prose-vs-transcript defects traced to this.
- scope: global · status: ACTIVE

## L-004 · A passing test must be able to fail
- **Trigger:** authoring or reviewing any test/assertion/verification matrix.
- **Rule:** ask "what would make this fail?" and prove it by breaking the code once; a check that passes with the defect present proves nothing.
- **Why:** TS-P1-009B Gate 5 — generated matrix passed while proving nothing; two writable-path tests asserted conditions the defective code also satisfied.
- scope: global · status: ACTIVE

## L-005 · Recorded hashes need their form pinned
- **Trigger:** recording any file hash/size in evidence or accepting one from a doc.
- **Rule:** with `* text=auto` every text-file bytes+SHA-256 is ambiguous (LF vs CRLF) — state both forms or pin the git blob OID.
- **Why:** caused three separate defects in two days (2026-08-11/12).
- scope: repo · status: ACTIVE

## L-006 · 600-second foreground ceiling
- **Trigger:** any harness/suite/long command in a Claude/Codex session.
- **Rule:** foreground Bash/PowerShell dies at 600 s (rc 143); launch long runs with run_in_background and block via TaskOutput.
- **Why:** RP6 R18 harness measured 5738 s; foreground attempt was killed and wasted a round.
- scope: global · status: ACTIVE

## L-007 · Codex lanes must not spawn Claude children
- **Trigger:** dispatching any Codex lane.
- **Rule:** prose bans are insufficient — run the guard process; verify no Claude Code child processes appear during Codex lanes.
- **Why:** dispatched Codex lanes spawned Claude Code children and silently burned Claude credit (2026-08); one unauthorized Max sub-delegation flagged.
- scope: global · status: ACTIVE

## L-008 · GLM verdicts are supplemental where execution matters
- **Trigger:** assigning GLM an audit/verify task.
- **Rule:** GLM cannot execute harnesses unattended here — dispatch with acceptEdits + "no approval requests"; treat its verdict as source-level only until a Lead executes.
- **Why:** repeated GLM rounds delivered source-level claims that changed after real execution (Pathscope C-1 among others).
- scope: global · status: ACTIVE

## L-009 · Probe the route before spending a dispatch
- **Trigger:** dispatching to any CLI route (Codex account, GLM, Cline, NIM) after config/quota changes.
- **Rule:** one cheap probe (model + trivial command) before the real dispatch; stale caches (models_cache.json) are NOT evidence a model is unavailable.
- **Why:** dispatches died on exhausted/misconfigured routes; sandbox block was "unresolvable" until one probe found the working flag.
- scope: global · status: ACTIVE

## L-010 · Narrow bands for security-flavored Codex audits
- **Trigger:** sending Codex any audit touching exfil/env-fixture/security content.
- **Rule:** split into narrow bands, redirect harness output to files, quote only summary lines, use symbolic fixture names — or the content filter kills the run AFTER the work, losing the verdict.
- **Why:** multiple filter kills post-work (2026-08); workaround verified.
- scope: repo · status: ACTIVE

## L-011 · Check all refs before claiming work is missing
- **Trigger:** any "X was never done / file is missing" conclusion.
- **Rule:** check origin/master AND all branches/refs first; local branches here run tens of commits stale, and current live work sits 600 commits ahead of master on a feature branch.
- **Why:** TS-P0/TS-P1 work was "missing" until origin/master was checked.
- scope: repo · status: ACTIVE

## L-012 · One overnight loop at a time
- **Trigger:** starting any overnight/heartbeat autonomous loop.
- **Rule:** verify no other session already runs a loop; never two in parallel.
- **Why:** two parallel loops double-burn quota and race on handoff files.
- scope: global · status: ACTIVE

## L-013 · Long unattended runs need power-plan proof
- **Trigger:** arming any multi-hour unattended run on this machine.
- **Rule:** set and VERIFY sleep+hibernate idle=0 on AC and DC before the window starts.
- **Why:** Day 1 v1 bridge run died at ~9h35m by system SLEEP (2026-07-20).
- scope: global · status: ACTIVE

## L-014 · Audit the storage encoding, not just parsed state
- **Trigger:** verifying any persisted evidence/ledger/registry.
- **Rule:** check encoding and clock domain of what is on disk, not only the parsed object in memory.
- **Why:** TS-P0 retained defects invisible at parse level (encoding + clock domain).
- scope: repo · status: ACTIVE

## L-015 · Simulated evidence is not evidence
- **Trigger:** any matrix/table/verdict produced without executing the real artifact.
- **Rule:** reject simulated/reconstructed matrices; run the real thing — a simulation can agree with itself and still hide a defect.
- **Why:** Python-simulated D026 matrix was rejected; real execution then exposed a genuine row-6 defect (2026-08-12).
- scope: global · status: ACTIVE

## L-016 · Commit handoff updates before stopping
- **Trigger:** ending any session that changed repo state.
- **Rule:** update handoff files and commit with exact staged paths (never `git add .`); an un-committed handoff is a lost handoff.
- **Why:** 17 untracked runkit files sat uncommitted for days (2026-08-09); chat-only fixes evaporate — the founding incident of this file.
- scope: repo · status: ACTIVE

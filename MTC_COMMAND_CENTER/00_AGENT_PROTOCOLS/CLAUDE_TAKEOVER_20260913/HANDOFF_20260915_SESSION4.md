# Handoff — P0 campaign Lead lane, session 3 → session 4 (written 2026-09-15 05:20Z by Claude Opus 5 Lead, desktop session `tradingview-lab-clean-ca`, id b9df29)

Canonical copy: `%TEMP%\CLAUDE_HANDOFF_20260915_P0_SESSION4.md`. Copies: `C:/tmp/CLAUDE_P0_RUN_20260913/HANDOFF_20260915_SESSION4.md`, CT13 `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/HANDOFF_20260915_SESSION4.md`. It supersedes `CLAUDE_HANDOFF_20260914_P0_SESSION3.md` (still valid for quotas-as-of-yesterday and the day's decisions; do not re-read history before acting on §3 here).

Owner: Barış — non-technical, answers in one line, wants English. He asked this session for: a handoff, all memory files updated, a new session that knows what is done and what is left, an 8-hour plan aimed at finishing the P0 packages, and a status report. The plan is §3; the honest closure picture is §2.

## 0. First five minutes (do these before anything else)
1. `ListAgents` + `tasklist` for `agy.exe` / `codex.exe`: no other Lead may hold the lane (append your claim to `C:/tmp/CLAUDE_P0_RUN_20260913/OWNERSHIP_CLAIM.md`). Two stale `codex.exe` (pids 24300, 38796) were alive at 21:10Z — kill only if their command line shows a finished lane dir. **No git anywhere while `agy.exe` runs. No Gemini call while a Codex builder lane is in a worktree.**
2. Read, in this order: this file → `C:/tmp/CLAUDE_P0_RUN_20260913/RUN_STATE.md` (last section "session 3 END") → `LANE_TABLE.md` ("Session 3 close") → `OWNER_DECISIONS_PENDING.md` (none pending) → `laneP1CAP_build/LEAD_VERIFICATION_P1CAP.md` → `P020_DERIVED_PLAN_20260914/LEAD_TERMINAL_DERIVED_PLAN.md`.
3. Governance: root `AGENTS.md`, `DECISIONS.md`, `CONTEXT_MAP.md`; stage `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/`; skill `mtc-repo-guard` before any repo action; `superpowers:verification-before-completion` before any "passed/accepted" claim. Owner routing order stands: Claude MAX = this Lead only; audits/corrections on Gemini/Codex/Grok; exact Opus/Sol slots only where `REVIEW_POLICY` requires.
4. Probe quotas (never recall them): Codex Plus pool (`secondary`=`fourth`, one account; ~45 min lane time per 5-hour bucket, caps 3-4×/day); Claude Pro exact Opus (was 0.85 of the weekly limit; **resets Wed 2026-09-16 20:00Z**; no Opus slot before that without a new owner word); SuperGrok weekly cap until 2026-09-18; OpenCode Go monthly cap (~Sep 29); Spark weekly cap (Sep 19); Gemini paid CLI OK (wrapper `Invoke-GeminiProReadOnly.ps1` hash `eff6a727…`; chain `gemini_retry_chain_v2.py`; stage packets ≥ 75 s before launching; raw stdout kept in `%TEMP%\gemini_wrapper_failures\` on refusal).
5. freellmapi trial server (`C:\LAB\TOOLS\freellmapi`, `127.0.0.1:3001`, pid 12868 yesterday): probe `http://127.0.0.1:3001/` — restart detached if dead; it is documentary-only and still needs the owner's dashboard account + provider keys ("keys added" is the owner's cue).

## 1. What is DONE (verified, recorded)
| Package | Done | Evidence |
|---|---|---|
| **P020** preselection | V1.6 frozen `cb756020…` built (D9-A, record V3 `quantity_step` 0.00001), full T0 roster accepted (Opus R6 + Sol R6 PASS-WITH-NITS, Gemini 3.7 SATISFIED, Lead REPRODUCED; Grok slot vacant), one-shot RUN 2026-09-14 20:38Z → **`PROFILE_ELIGIBLE_NOT_ACCEPTED`**, 15/15 trials trade-bearing; selection 15m TRIPLE_EMA / 1h STOCH / 2h KELTNER / 4h MACD / 1D DONCHIAN. Derivation tool fixed (N6-8, N6-6; 16 tests). **Derived plan `d84b043a…` produced, byte-identical re-run, PLAN_VALID through the real driver.** | `P020_ELIGIBILITY_RUN_V16/LEAD_TERMINAL_ELIG16.md`, `P020_PRESELECT_T0_R6_20260914/LEAD_ADJUDICATION_R6_{OPUS,SOL}.md`, `P020_DERIVED_PLAN_20260914/` |
| **P012** admission | Risk packet CLEAN + owner answers Q1–Q7 recorded (`OD-20260914-P012-ADMISSION-Q1..Q7`); Path 1 real evidence EXISTS on the owner's mainnet account (fills T2/T3/dup/T1-maker 16:03–16:14Z, funding 17:00Z + 18:00Z, close 18:08Z, net +0.28 USDC); **capture tool candidate committed `e77af1c8`** (branch `feature/p012-path1-capture-20260914`), full Bridge suite 1638 passed on 3.12 | CT13 `P012_PATH1_EXECUTION_20260914/`, `laneP1CAP_build/LEAD_VERIFICATION_P1CAP.md` |
| **P031** | batch candidate `96af3eb6` committed + pushed; Gemini review REQUEST_CHANGES (J-01..J-05) → correction brief ready | CT13 `P031_BATCH_CANDIDATE_20260914/`, `laneP31FIX_build/TASK.md` |
| **P030** | exporter candidate `daf6a43b` committed + pushed; Gemini PASS-WITH-NITS (K-01..K-05) → correction brief ready | CT13 `P030_EXPORTER_CANDIDATE_20260914/`, `laneO9FIX_build/TASK.md` |
| Bridge / TESTNET | KVM2-P4-03 provisioned, smoke PASS 12/12, service DISARMED; credentialed start = scoping note (option C) | CT13 `BRIDGE_*_20260914/` |
| Tooling | Gemini wrapper repaired (D10); TESTNET button fixed; freellmapi built (trial) | CT13 `GEMINI_WRAPPER_FIX_20260914/`, `BRIDGE_TESTNET_BUTTON_FIX_20260914/`, kit `TOOLBOX.md` |
| P014 | done earlier | — |

## 2. What is LEFT — and what can honestly close in 8 hours
Nothing in P0 can be *accepted* (package-closed) inside 8 hours, for three reasons that are not about effort: (a) `REVIEW_POLICY` requires the exact Opus slot on every acceptance and the next slot opens **Wed 2026-09-16 20:00Z**; (b) the owner's own P012 rule Q3 "Wait" means weeks of real captures before production admission; (c) Codex Plus gives ~90 min of lane time in 8 hours. What the 8 hours CAN do is bring every package to "Opus-ready": all non-Opus reviews done, all corrections built, all evidence recorded, so Wednesday evening is a pure acceptance pass.

| Package | Left | Blocker type |
|---|---|---|
| P020 | derived-plan review (Gemini 3.7 + Sol; Opus limitation recorded) → plan swap → **bounded measurement once** (`run_bounded_benchmark.py --run`, `OD-20260914-P020-MEASURE-1` B YES) → measurement terminal + corroboration → acceptance reporter → Opus | Opus Wed; the rest is 8-hour work |
| P012 | Gemini detection + Sol review of `e77af1c8` → P1FIX (L-1..L-6 + reviewer items) → real read-only capture of the owner's address with his ownership signature (10 min of the owner) → intake under `REAL_OBSERVATION_INTAKE.md` → weeks of captures (Q3) | owner rule + Opus |
| P031 | P31FIX lane → Lead verify/commit → Gemini delta + Sol → Opus → PR | Opus Wed; Codex budget |
| P030 | O9FIX lane → verify/commit → Gemini delta + Sol → Opus → PR | Opus Wed; Codex budget |
| P013 | blocked on P020 acceptance | dependency |
| P026 T-B drills | needs an owner execution scope | owner |
| Residuals | Opus N6-1/N6-7/Sol-6-3 doc pins → next re-freeze; N6-3 (cost/funding record intervals) = owner lever after measurement; "P0-14 close as deferred" optional owner word; stray `C:/tmp/.git` dir and `C:/tmp/P1CAP_20260914_LOCKED_SANDBOX_DIRS` DELETED 2026-09-15 05:30Z (owner-approved UAC); if `C:/tmp/.git` reappears, read `info/exclude` to find the writer (it was being rewritten minutes before deletion) | owner / hygiene |

## 3. The 8-hour working plan (start = when the new session claims the lane; times are lane-time budgets, not promises)
Rules: one Codex lane at a time; Gemini only when no Codex lane is committing; every review packet staged ≥ 75 s before the chain; every acceptance claim needs the command output in the record; write CT13 records as you go (do not batch them to the end — session 3 lost the last two records to an interruption and had to write them next morning).

**Hour 0–1 — claim, probe, launch the two cheapest high-value items**
1. §0 steps. Probe Codex Plus with one short lane, not a loop.
2. Gemini 3.7 corroboration of the derived plan: brief from `LEAD_TERMINAL_DERIVED_PLAN.md` §4 (questions: driver does not pin `derivation.*_sha256`; plan swap procedure; rule transcription). Runner pattern: copy `C:/tmp/P012_S16_LAUNCH_PREP_20260913/run_p020_g37_v16.ps1` and replace the packet boundary string. Adjudicate → `P020_DERIVED_PLAN_20260914/LEAD_ADJUDICATION_G37.md`.
3. In parallel on Codex Plus (bucket 1, ~25 min): **exact Sol review of the derived plan** (same packet; `--add-dir` lane, scratch cwd, as `codex_reset_queue_r6.ps1` did for R6).

**Hour 1–2 — bounded measurement (the one irreversible-ish step of the day; do it exactly once)**
4. If Gemini + Sol accept: back up `benchmark/BENCHMARK_PLAN.json` as `BENCHMARK_PLAN_BASE_c6f07afd.json`, copy the derived plan over it, refresh `SHA256SUMS_V16.txt`, run `--validate-plan` in place (expect PLAN_VALID), then `run_bounded_benchmark.py --run --output-root <new dir under the run root>` once under a launcher that logs digests before/after (model on `p020_eligibility_run_v16.ps1`: EAP=Continue around the native call, sha256 of every output). Terminal record `LEAD_TERMINAL_MEASUREMENT.md`; push-notify the owner one line.
5. Gemini 3.7 corroboration of the measurement record (documentary; ~20 min).

**Hour 2–3.5 — P031 correction (Codex bucket 1 remainder, ~30 min lane) + P1CAP detection review**
6. Remove `laneP31FIX_build/HOLD.txt`, launch P31FIX (brief already written; J-03 is REQUIRED). While it runs: NO Gemini call (it is in the P031 worktree).
7. After P31FIX exits: Lead verify on 3.12 (contracts suite, Ruff at `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`, guard PASS), commit exact paths in `C:/tmp/P031_M1_20260913`, push. Then Gemini 3.8 **delta** review of P031 and Gemini 3.8 **detection** review of P1CAP `e77af1c8` (sequential; each ≥ 75 s staging).

**Hour 3.5–5.5 — P030 correction + P1FIX brief (Codex bucket 2 opens ~5 h after bucket 1's first call)**
8. Launch O9FIX (~25 min). Verify/commit/push as in step 7. Gemini delta review of P030.
9. Write `laneP1FIX_build/TASK.md` from `LEAD_VERIFICATION_P1CAP.md` L-1..L-6 + the Gemini detection findings; launch when the bucket allows (~25 min). Verify/commit/push.

**Hour 5.5–7 — Path 1 real capture (needs the owner for ~10 minutes; ask him for a time window early in the day)**
10. Fix `--run-id` first (e.g. `p012-path1-20260915T…Z`), print the ownership message with `--print-ownership-message`, open `path1_sign_ownership.html?address=0x1E26…&run_id=…` for the owner; HE signs with his wallet (you never touch keys, never click an order control); save the signature file; run the capture read-only against mainnet for the window 2026-09-14T15:00Z → 2026-09-14T19:00Z; verify sidecars; record under CT13 `P012_PATH1_REAL_CAPTURE_20260915/` with the address in short form; intake per `laneP1CAP_build/REAL_OBSERVATION_INTAKE.md`.
11. Exact Sol reviews of P031 and P030 deltas if the bucket allows (otherwise queue them first thing Wednesday).

**Hour 7–8 — records, memory, handoff**
12. CT13: `P020_MEASUREMENT_20260915/`, `P031_FIX_20260915/`, `P030_FIX_20260915/`, `P012_PATH1_CAPTURE_TOOL_REVIEW_20260915/`; `DECISIONS.md` only if the owner ruled; `OWNER_ANSWERS_20260915.md` for any owner line. Guard PASS → exact-path commit → push.
13. Update memory (`p0-claude-lead-session-2026-09-15.md` new; MEMORY.md pointer), `LLM_ROUTE_ASSESSMENTS.md` append, TOOLBOX row if freellmapi changed state, then `/handoff` again. Prepare the **Wednesday 20:00Z Opus queue** file: P020 acceptance, P031, P030, P1CAP — packets ready so the slot is not wasted.

Owner asks to make during the day (one line each, in this order): (1) a 10-minute window for the ownership signature; (2) "keys added" for freellmapi when done; (3) optional: N6-3 ratification wording after the measurement; (4) optional: "P0-14 close as deferred".

## 4. Facts the new session must not re-derive
- Run root `C:/tmp/CLAUDE_P0_RUN_20260913/`; CT13 = `C:/CT13` on `feature/claude-takeover-20260913` (records dir `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/`); worktrees share `.git` with `C:/LAB/Tradingview_LAB_CLEAN`.
- Interpreters: P020 venv `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` (3.12.12); Bridge deps `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe`; Ruff `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`; repo guard `powershell -NoProfile -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER/tools/repo_guard.ps1` (`pwsh` absent).
- Bridge pytest: still pass `--basetemp` outside `C:/tmp` as a habit (the stray `C:/tmp/.git` that caused 33 phantom `export_mtc_funding` failures was deleted 2026-09-15 05:30Z but the Claude Code harness recreates/rewrites `<nearest .git>/info/exclude` whenever a session's shell cwd enters a directory under a `.git` ancestor — that write also trips the Gemini wrapper guard inside worktrees; check `Test-Path C:/tmp/.git` first and keep every shell cwd out of worktrees while `agy.exe` runs) and `-p no:cacheprovider`; ignore sandbox-owned `pytest-of-*` dirs; if the guard reports `PINE_ALERT_GUARD UNEVALUATED … Erişim engellendi`, the worktree holds ACL-locked sandbox dirs → rename the dir, `git worktree prune`, re-add the worktree, copy the deliverables back, re-verify digests.
- Bash tool mangles backslashes (`\t`→TAB, `\r`, `\f`, `\\`): write `.ps1`/RUNNER files with the Write/Edit tools only. `git commit -F -` (not `/dev/stdin`). PowerShell 5.1: no `&&`, no `<<<`, no `?:`.
- Hard rules kept all session: the model never places/closes orders (declined the owner's 24-hour authorization); passwords/keys/seeds are the owner's only; the owner's mainnet address is public but recorded short-form `0x1E26…AC49` in CT13 unless the full form is needed.

## 5. Suggested skills for the next agent (call via the Skill tool)
- `mtc-repo-guard` — before every git action in any worktree (branch check, exact-path staging, guard PASS, final report format).
- `superpowers:verification-before-completion` — before any "passed / accepted / PLAN_VALID / pushed" claim.
- `superpowers:systematic-debugging` — if any test suite or launcher fails (do not patch on a guess; the 33-failure case needed a real base worktree).
- `superpowers:using-git-worktrees` — when a candidate needs a fresh worktree (P1FIX, base checks).
- `anthropic-skills:consolidate-memory` — at the end of the session, before `/handoff`.
- `caveman:caveman-commit` is NOT for this repo: commit messages here are governance records (full sentences, digests, Co-Authored-By lines as in `e77af1c8`).

## 6. Memory files updated for this handoff (auto-memory dir `C:\Users\BarışSemaay\.claude\projects\C--LAB-Tradingview-LAB-CLEAN\memory\`)
`MEMORY.md` (pointer → this handoff), `p0-claude-lead-session-2026-09-14.md` (SESSION 3 END block), `route-lessons-2026-09-14.md` (stray `.git` trap; sandbox-locked dirs; interruption cost), `bridge-pytest-staging-refuses-under-c-tmp.md` (new, permanent), `verified-on-base-means-a-real-worktree.md` (second application, positive).

## 7. Redactions
No credential, key, seed or password appears in any file of sessions 2–3 (the Lead never saw one). The owner's Hyperliquid mainnet address is public and appears in the Path 1 packet by his own words; CT13 records use the short form. Wallet balances quoted are the owner's own statements or public API reads.

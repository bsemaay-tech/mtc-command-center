# Handoff — P0 campaign Lead lane, session 4 → session 5 (written 2026-09-15 ~08:15Z by Claude Opus 5 Lead, desktop session `tradingview-lab-clean-39`, id 743291)

Canonical copy: `%TEMP%\CLAUDE_HANDOFF_20260916_P0_SESSION5.md`. Copies: `C:/tmp/CLAUDE_P0_RUN_20260913/HANDOFF_20260916_SESSION5.md`, CT13 `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/HANDOFF_20260916_SESSION5.md`. Supersedes `CLAUDE_HANDOFF_20260915_P0_SESSION4.md` (still valid for §4 facts and the Sunday decisions).

Owner: Barış — non-technical, answers in one line, wants English. He ruled three times today: "no, wait for Grok (Sep 18)" (measurement), "A" (Lead builds P1FIX), and he signed the Path 1 ownership message. Nothing is pending on him.

## 0. First five minutes
1. `ListAgents` + `tasklist` for `agy.exe` / `codex.exe` / `grok.exe`; append your claim to `C:/tmp/CLAUDE_P0_RUN_20260913/OWNERSHIP_CLAIM.md`. **Keep your shell cwd OUT of every worktree while `agy.exe` runs** (the harness writes `.git/info/exclude` on cwd entry and voids the Gemini call); no git anywhere while it runs.
2. Read in this order: this file → `RUN_STATE.md` (section "session 4") → `LANE_TABLE.md` (last "update" tables) → `OWNER_DECISIONS_PENDING.md` (nothing pending) → `C:/tmp/OPUS_QUEUE_20260916/OPUS_QUEUE_20260916.md`.
3. Governance as before (root `AGENTS.md`, `DECISIONS.md`, `CONTEXT_MAP.md`; stage `00_AGENT_PROTOCOLS/`; skill `mtc-repo-guard`; `superpowers:verification-before-completion` before any "passed/accepted").
4. Probe, never recall: **Codex — ALL homes weekly-capped** (Plus `secondary`/`fourth` until 2026-09-19 18:47 local; `free` until 09-19 11:10; `third` until 10-06); **SuperGrok 402 until 2026-09-18**; OpenCode Go hung (unavailable); Gemini paid CLI read-only route OK (five reviews today; chain `gemini_retry_chain_v2.py`, wrapper hash `eff6a727…`); Gemini coder needs PowerShell 7 (absent); **Claude Pro exact Opus resets Wed 2026-09-16 20:00Z**; freellmapi `127.0.0.1:3001` restarted (pid 25932; keys pending — owner says "keys added").
5. `C:/tmp/.git` stray dir: deleted 05:30Z; check `Test-Path C:/tmp/.git` — if it reappears the writer is the harness (see memory); keep `--basetemp` outside `C:/tmp` as a habit.

## 1. DONE today (verified, recorded in CT13 `3d10ec3d`, `0f031d88`, `57f8cdf5`, `7b04d375`, + close-out)
| Package | Done | Evidence |
|---|---|---|
| **P020** | derived plan `d84b043a…` + tool `0bfd1891…`: exact Sol PASS-WITH-NITS (0 REQUIRED), Gemini 3.7 PASS-WITH-NITS, Lead ALL EQUAL; measurement launcher updated to the reviewers' conditions (assert the installed plan digest at three points; temporary substitution; pre/post source digests) and **gated on a Grok pre-screen by owner ruling `OD-20260915-P020-MEASURE-GROK-1`** | CT13 `P020_DERIVED_PLAN_REVIEW_20260915/`; `laneGKDERIV_grok/` prepared |
| **P031** | `bd0d56d0` (P31FIX, Codex: J-01..J-05) + `48bd70de` (Lead-authored registrar-path RED test; disclosed) → Gemini delta PASS-WITH-NITS (attempt 1 voided by the CLI "cut off" envelope, recovered supplemental) | CT13 `P031_FIX_20260915/` |
| **P012 Path 1** | tool `e77af1c8` → Gemini REQUEST_CHANGES (F-1 run-id/signature, F-2 half-open window) → owner "A" `OD-20260915-P012-P1FIX-LEAD-1` → **Lead-built `af921d75`** (21 tests; RED 12/9 pre-fix; Bridge suite 1649 green) → Gemini delta PASS-WITH-NITS; **real capture r1 DONE** (ownership VERIFIED by the owner's `personal_sign`; 5 fills + 2 funding rows = his declared activity; net +0.2839 USDC; NONACCEPTING) | CT13 `P012_PATH1_CAPTURE_TOOL_REVIEW_20260915/`, `…_FIX_20260915/`, `P012_PATH1_REAL_CAPTURE_20260915/` |
| **P030** | unchanged (`daf6a43b`, Gemini PASS-WITH-NITS K-01..K-05 OPEN); O9FIX waits for Codex | CT13 `P030_EXPORTER_CANDIDATE_20260914/` |
| Records | route ledger appended (docs branch `3c374a6f`, pushed); kit `TOOLBOX.md` rows updated (`d0286fc`, local repo); memory `p0-claude-lead-session-2026-09-15.md` + `route-lessons-2026-09-15.md` | — |

## 2. LEFT and when it can move
| Item | Blocker | When |
|---|---|---|
| **Wednesday exact-Opus reviews** P031 `48bd70de` → P1CAP `af921d75` → P030 `daf6a43b` | Claude Pro reset | **2026-09-16 20:00Z**: `powershell -NoProfile -ExecutionPolicy Bypass -File C:\tmp\OPUS_QUEUE_20260916\run_queue.ps1` (serial; refuses before the reset; refuses while agy runs); adjudicate each (grep citations, reproduce a RED arm), record CT13 `<pkg>_OPUS_20260916/` |
| Grok pre-screen of the derived plan (`laneGKDERIV_grok/run.ps1`) → adjudicate `LEAD_ADJUDICATION_GROK.md` ('Grok pre-screen slot SATISFIED for the derived plan') → **bounded measurement once** (`p020_measurement_run.ps1`) → measurement corroboration (Gemini) | Grok weekly reset | Sep 18+ |
| exact Sol reviews: P031 `48bd70de`, P1CAP `af921d75`, P030 `daf6a43b` | Codex weekly reset | Sep 19 18:47 local (Plus) |
| O9FIX (P030 nits K-01..K-05; brief `laneO9FIX_build/TASK.md`) | Codex, or an owner "A" for the Lead | Sep 19 / owner |
| P012 intake adapter into `export_mtc_funding.py --mode PRODUCTION` (schema-v10 rows from the capture's derived view) | engineering work item; owner scope; Q3 "Wait" | later |
| P013 | P020 acceptance | after measurement + Opus |
| P026 T-B drills | owner execution scope | owner |
| Residual doc pins N6-1/N6-7/Sol-6-3, Sol-D-2 (`DERIVATION_RULE.md` stale digests) | next re-freeze | later |
| `git gc` of the shared `.git` (32k loose objects slow every Gemini call by minutes) | do it only when NO lane runs; say so in RUN_STATE | any quiet moment |

## 3. Rules learned today (also in memory)
- Harness `info/exclude` writes void Gemini calls → cwd discipline during `agy.exe`.
- Gemini CLI "cut off" ERROR with a complete report → recover from `%TEMP%\gemini_wrapper_failures`, keep supplemental, cap the re-run prompt at 5000 words, count only the re-run.
- Lead-as-builder needs the owner's one-line word each time; disclose; the Lead never accepts its own code.
- `HL_API_WALLET_KEY` sits in the inherited environment: never print; `env -u` it for the capture tool and in every review launcher.
- Wallet signing: serve the reviewed page on localhost (file:// gets no provider); check the port is free.

## 4. Facts not to re-derive
Same as the session-4 handoff §4 (run root, CT13, interpreters, guard command, Bash backslash trap, PowerShell 5.1 limits, hard rules: the model never places orders; keys are the owner's only; address short-form `0x1E26…AC49` in prose, full form only inside evidence files). Additions: Bridge interpreter for the capture tool = `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe`; capture run_id convention `p012-path1-<windowstart>-<windowend>-rN`; `native_read_audit.py` now lives in the run root; Opus launcher pattern = `claude --print … --model claude-opus-5 --effort xhigh` on the Pro profile with `--add-dir` (see the queue's `run.ps1` files).

## 5. Suggested skills for the next agent
`mtc-repo-guard` (every git action), `superpowers:verification-before-completion` (before any pass/accept claim), `superpowers:systematic-debugging` (any failing suite), `anthropic-skills:consolidate-memory` (end of session), `/handoff`.

## 6. Redactions
No credential, key, seed or password appears in any file of session 4 (the Lead never saw one; the wallet-key environment variable was removed from child processes and never printed). The owner's mainnet address is public; the capture evidence files carry it in full by necessity; prose uses the short form. The owner's signature is public data.

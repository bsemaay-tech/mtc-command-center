# Friday exact-Sol queue (2026-09-19, after the Codex Plus weekly reset 18:47 local) — PREPARED 2026-09-15 night

Second flagship for every candidate the Wednesday exact-Opus lanes read (owner routing: two flagships of different families + Gemini + Lead reproduction before any merge). Lanes are GENERATED on Friday from the Wednesday briefs by `make_sol_lane.ps1 -Pkg <P031|P1CAP|P030|P026|P027CI>` so that a Wednesday REQUEST_CHANGES (new HEAD, re-pinned brief) is picked up and a stale pin can never run; the generator refuses when the worktree HEAD differs from the Wednesday pin.

Candidates without a Wednesday lane (add a `OPUS_QUEUE_20260916/<pkg>/REVIEW_BRIEF.md` + `opus/run.ps1` first, or write a Sol brief by hand): P0-21 S1 catalogue slice `7fecf204` (`C:/tmp/P021_S1_20260915`; counted Gemini PASS-WITH-NITS), DD-06 probe `1af85067` (`C:/tmp/P029_DD06_20260915`; counted Gemini PASS-WITH-NITS), P0-12 intake adapter `65c4bc40` (`C:/tmp/P012_INTAKE_20260915`; Gemini ×2 voided-but-complete PASS-WITH-NITS).

Order (serial, one Codex lane at a time on `secondary`): P031 → P1CAP → P030 → P026 → P027CI (T1) → then the three above if budget remains. Each lane: verify HEAD + `git status --porcelain` empty in the worktree before AND after; adjudicate (grep citations; reproduce one RED arm); record under CT13 `<package>_SOL_20260919/`; ledger row.

Route facts to re-probe on Friday before the first lane: which Codex home serves `gpt-5.6-sol` (2026-09-15: `secondary`/`fourth` = one Plus account; `free` = Codex Pro, out of credit; `third` capped to Oct 6); the Plus pool's 5-hour bucket (~45 min of lane per bucket, ~3-4 buckets/day). Never a bare `codex`; always `Invoke-CodexForClaude.ps1 -Account <home>`.

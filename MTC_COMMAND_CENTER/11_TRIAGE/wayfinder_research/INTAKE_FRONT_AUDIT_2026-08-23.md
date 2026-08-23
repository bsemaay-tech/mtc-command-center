# Intake-Front Audit — Wayfinder #56

**Ticket:** GH #56 (sub-issue of #54, the wayfinder decision-ticket map)
**Question:** How do discovery, source extraction and candidate creation (planned lifecycle steps 1–3) actually work today, and what macro pieces are missing between "an idea exists somewhere" and "a `SOURCE_LITERAL` definition with a Missing-Rule Ledger exists"?
**Date:** 2026-08-23
**Method:** Read-only primary-source review of the working tree at `C:\LAB\Tradingview_LAB_CLEAN` plus the frozen planning blob `764da27f:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`. No files in the main checkout were modified; this document was written in an isolated worktree at `C:\WFRES2`.

---

## 1. Do `SOURCE_LITERAL` and the Missing-Rule Ledger exist as artifacts, or only as plan language?

**Plan-only. Neither exists anywhere in the repo outside the planning documents themselves.**

- A repo-scoped, case-insensitive search for `SOURCE_LITERAL` inside `MTC_COMMAND_CENTER` returns exactly one file: `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`.
- A repo-scoped search for `Missing-Rule Ledger` / `Missing Rule Ledger` / `missing_rules:` returns exactly three files, all in `11_TRIAGE/`: `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md`.
- No `.py`, `.json`, `.yaml`, `.md` outside `11_TRIAGE/` references either term. No strategy folder (`03_QUANTLENS/strategies/STGxxx_*/`), no registry in `05_REGISTRY/`, and no dashboard code contains a `source_profile`, `SOURCE_LITERAL`, or `missing_rules` field.
- The master brief itself is explicit that this is new, not-yet-built machinery. §6.1 introduces `SOURCE_LITERAL` as one of four profiles replacing a rejected v1 concept ("naked"), and closes with: *"This finally answers the question the current pipeline cannot: did the original strategy contain edge, or did our own machinery create most of it?"* — i.e. the document says outright that the **current** pipeline cannot do this yet.
- §6.2 (Missing-Rule Ledger) gives only a YAML schema sketch (`missing_rules: - rule: STOP_LOSS ...`) as a design, with no pointer to any existing file that stores such records, and no code that produces or consumes that schema exists in the repo.
- §6.3's lifecycle diagram places `SOURCE_LITERAL definition + Missing-Rule Ledger` at **step 3** of a 21-step planned lifecycle (`6. Research-to-live lifecycle`) — this is prospective architecture, not a description of current behavior.

**Verdict: both are 100% plan-only. Zero real instances exist today.**

---

## 2. Is there a dedup or triage step between raw intake and candidate creation?

**Split answer: a triage step exists but is a frozen historical snapshot; a dedup mechanism exists but is also a one-time historical artifact, not a live/automated step wired into the current pipeline.**

**Triage registry.** `MTC_COMMAND_CENTER/05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (`generated_at: 2026-06-04T09:23:36Z`, `generator: build_triage_registry.py`, `source_worklist: 11_TRIAGE/2026-05-30_rejected_worklist.xlsx`) holds 172 candidates with fields `priority`, `source_quality`, `blocked_reason`, `coverage_status_live`, `recommended_next_step`, `eligible_for_retriage`. Distribution: `priority` = 70 `P1_REJECTED` / 102 `P2_MISSING_COVERAGE`; `source_quality` = 70 `REJECTED` / 89 `HIGH` / 9 `MEDIUM` / 4 `LOW`; `recommended_next_step` = 96 `Review`, 61 `Source audit / park`, 9 `Build promotion packet`, plus a handful of narrower next-steps. This is a real triage classification, but it was produced once, from a static Excel worklist dated 2026-05-30, by a script (`03_QUANTLENS/tools/build_triage_registry.py`) whose output file (`TRIAGE_CANDIDATE_REGISTRY.json`) has not been touched since 2026-06-07 per `git log`. There is no evidence it re-runs as new intake arrives.

**Dedup.** `03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md` documents a dedup process in prose (Turkish): before processing a transcript, check `video_id` and `transcript_hash`; if a duplicate, do not create a new candidate, and report the prior candidate's id/status/path instead. It also describes channel-quality tiers (`WATCHLIST` → `BLACKLISTED`) that suppress future intake from bad sources. This is backed by a real artifact: `03_QUANTLENS/_registry/youtube_video_index.csv` (90 data rows) with exactly the columns the workflow doc describes — `video_id, normalized_url, original_url, title, channel_name, channel_id, transcript_hash, candidate_id, status, first_seen_at, last_seen_at, process_count, notes`. Row 12 (`VWAP_PULLBACK_REVERSAL`) shows `process_count: 2` with the note *"duplicate resubmission seen"* — direct evidence the dedup logic was applied at least once. **But every row in this file is dated `2026-05-01`, and `git log` shows the file was last committed 2026-05-31 — nearly three months before this audit — and no `.py` file in the repo references `youtube_video_index.csv` at all.** It reads as a one-time manual/agent-run batch process from a single intake day, not a script wired into `route_user_intake.py` or any other currently-invoked tool. `route_user_intake.py` (the one script that actually runs today, see §4 below) performs zero dedup and never touches this CSV.

**Net answer:** yes, there was a real, working dedup+triage pass — once, in May/June 2026, over a fixed historical batch. There is no evidence either mechanism runs automatically today, and the live router script has no dedup logic of its own.

---

## 3. Is there a capacity model (e.g. "N ideas per week", queue limits, rate limiting)?

**No. Absent.**

- `03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md` (the intake-process doc) contains no throughput, rate, or queue-size language at all.
- `_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` and `_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` — both read in full — contain no capacity language either.
- A scoped, case-insensitive search of `_AI_MEMORY/` for `capacity|per week|per day|rate limit|queue limit|ideas per|throughput` returns only hits about **AI model/account capacity** (Claude/Codex/GLM API quota exhaustion, e.g. `SESSION_LOCK.md`, `AI_ACCOUNT_AND_MODEL_ROUTING.md`) — a completely different meaning of "capacity," unrelated to how many research ideas the pipeline can or should intake.
- Nothing in the master architecture brief's §6 (research-to-live lifecycle) states an intake rate either; §6.5 does define fleet-sizing language for the *forward-testing* stage ("shadow fleet: bounded by CPU and storage — effectively dozens; testnet fleet: bounded by exchange rate limits...") but that is downstream of candidate creation, not an intake-side capacity model.

**Verdict: no capacity model exists anywhere in the intake front. The pipeline has no notion of "how many ideas per week" it should accept, process, or reject.**

---

## 4. Who or what decides an idea is worth extracting into a registry candidate?

**Mostly ad hoc / human-and-agent judgment call today; the one automated step (`route_user_intake.py`) explicitly refuses to make this decision.**

Read in full, `03_QUANTLENS/tools/route_user_intake.py` does exactly one thing: for every file sitting in `00_INBOX/USER_INTAKE/` (excluding `README.md`/`.gitkeep`), it tries to match the filename to an **existing** `STGxxx` strategy folder — first by an explicit `STGxxx` filename prefix, then by fuzzy token overlap against the strategy folder's slug (threshold: ≥2 shared non-stopword tokens, `MATCH_THRESHOLD = 2`). If a confident match is found, the file is moved (or, in dry-run, planned to be moved) into that strategy's `source_intake/{transcripts|screenshots}/`. **If no confident match is found, the file is left exactly where it is**, and the script prints: `UNMATCHED <name> (no confident match) -> open a new candidate -> open a new candidate (09_TRANSCRIPT_INTAKE_WORKFLOW)`. The script does not open that candidate, does not score the material, does not decide whether it's worth pursuing, and does not write any record of the decision — it only prints a suggestion to a human/agent reading the console output. The module docstring is explicit about this: *"No confident match -> reported as UNMATCHED (left in place; the agent should open a new candidate via the transcript intake workflow)."*

So the actual worthiness decision — "is this raw material worth becoming a new registry candidate at all" — is made by whichever human or AI agent is running the router interactively and chooses (or doesn't choose) to act on the `UNMATCHED` line, following the prose instructions in `09_TRANSCRIPT_INTAKE_WORKFLOW.md` (video-strategy → QuantLens candidate; useful-but-no-strategy → Trader Wiki; low-quality-channel → suppressed). This is a documented process but not an automated or code-enforced one: there is no code path that reads `UNMATCHED` output and creates a `STRATEGY_RESEARCH_REGISTRY.json`/`TRIAGE_CANDIDATE_REGISTRY.json` entry on its own.

Reinforcing this: `STRATEGY_RESEARCH_REGISTRY.json` (5,000+ lines, schema v1.0, `generator: build_strategy_research_registry.py`) has **no field connecting a candidate back to an intake source** — a scoped search of the file for `source_url|provenance|intake_source|candidate_id` returns zero matches. Each strategy record's only "source" pointer is `source_file`/`source_folder`, i.e. the already-created strategy folder on disk — the registry has no memory of which raw intake item spawned it or why it was judged worth extracting.

---

## 5. Where does an idea wait between being noticed and being acted on, and is that recorded machine-readably?

**It waits in plain filesystem locations with no machine-readable status/queue state — purely implicit ("still sitting in a folder").**

- `00_INBOX/USER_INTAKE/` is the literal wait-folder per its own README ("This is your drop folder... An AI agent routes it into the right place. You do not need to know the internal folder layout."). As of this audit it contains: a `README.md`, a `.gitkeep`, **six unrelated AI-tooling article transcripts** (e.g. `12 Open Source AI Tools That Feel ILLEGAL To Know About.md`, `Claude Fable 5 Just Built the Ultimate Agent Harness.md`) with no connection to trading-strategy research, and **five large market-data files** (three consolidated OHLCV CSVs 1.2–1.3 MB each plus two JSON consolidation reports, all dated 2026-07-05). None of these look like strategy transcripts awaiting routing — the folder's actual current contents are stale/misplaced material, not a live queue of trading ideas. There is no index file, no per-item status, no "received_at" ledger — the only state is "the file is physically in this directory or it isn't."
- Once routed, material lands in `03_QUANTLENS/strategies/STGxxx_*/source_intake/{transcripts|screenshots}/` — again just a filesystem location, with the router's own instructions telling a human/agent to *manually* update `source_intake/intake_report.md` afterward (the router does not write that file itself).
- The two registries that could serve as a machine-readable queue both show the same pattern: no "waiting" or "queued" status value anywhere. `STRATEGY_RESEARCH_REGISTRY.json`'s `current_status` field only takes values like `PROMOTE_TO_FORWARD_PAPER_TRADE`, `RESEARCH_BATCH`, etc. — states describing an *already-created* candidate's research maturity, not its intake wait-time. `TRIAGE_CANDIDATE_REGISTRY.json`'s closest analog is `recommended_next_step` (`Review`, `Source audit / park`, `Build promotion packet`, ...), again not a queue-position or wait-duration field. Neither registry carries a per-item "first noticed" timestamp separate from the file's own generation date.
- Confirming this whole front is dormant rather than actively cycling: `git log` shows `TRIAGE_CANDIDATE_REGISTRY.json` last touched 2026-06-07, `STRATEGY_RESEARCH_REGISTRY.json` last touched 2026-06-06, and `route_user_intake.py` itself last touched 2026-06-06 — all roughly 2.5 months stale as of 2026-08-23. `00_INBOX/USER_INTAKE/` was last touched 2026-07-31 (a folder-relocation commit) and 2026-07-05 (a data-file drop), not by any registry-refresh activity.

**Verdict: waiting is 100% implicit — "the file is still sitting in a folder nobody has processed yet." Nothing records when an idea started waiting, how long it has waited, or how many ideas are currently waiting.**

---

## Evaluating F-21 against what was actually found

F-21, quoted from `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (§ "F-21 [FACT] The research intake pipeline works and is the healthiest part of the research stack"):

> - 172 triage candidates, 159 with transcripts, source URLs per candidate.
> - 63 structured strategy folders, each with `producer_spec.json`, `07_deterministic_spec.md`, `PROMOTION_PACKET.md`, `FORWARD_PAPER_TRADE_PLAN.md`, `PARITY_REFERENCE_METRICS.md`, signals/trades CSVs.
> - Real statistical machinery: `cpcv_validator.py`, `probabilistic_pbo.py`, `alpha_vs_buyhold.py`, `buy_hold_baseline.py`, `multiwindow_oos.py`, DSR + BH-FDR inside `mega_walk_forward.py`.
> **Do not rebuild this.**

**Partially confirmed, but the claim conflates two very different things and its evidence is stale.**

What F-21 gets right: the "172 triage candidates" figure is real and traceable — `TRIAGE_CANDIDATE_REGISTRY.json`'s own `summary` block states `"total": 172, "with_transcript": 159` verbatim, matching F-21's numbers exactly. The 63-strategy-folder structure and the statistical-validation machinery (`cpcv_validator.py`, `mega_walk_forward.py`, etc.) are real, present, and — by both this audit's file listing and the master brief's own description — substantially more mature than anything else in the research stack. **On downstream statistical rigor, F-21 is accurate.**

Where F-21 overreaches, given this audit's specific mandate (steps 1–3: discovery → extraction → candidate creation):

1. **F-21 is about candidate *processing*, not intake.** 89 of the 172 "triage candidates" it cites carry `priority: P1_REJECTED` (70) or otherwise sit in a frozen, one-time-generated file (§2 above). The number that sounds like a thriving pipeline is largely a graveyard of already-rejected historical items plus a static classification snapshot — not evidence of a currently functioning discovery→extraction→candidate flow.
2. **The one script that runs *today* at the front of the pipeline (`route_user_intake.py`) does none of the things that make F-21's evidence look healthy.** It has no dedup, no scoring, no worthiness judgment, and writes no records (§2, §4). The dedup and channel-quality mechanisms that *would* justify "healthy" (§09_TRANSCRIPT_INTAKE_WORKFLOW.md, `youtube_video_index.csv`) exist only as a single historical batch from 2026-05-01, untouched and unreferenced by any code since 2026-05-31.
3. **The evidence is stale.** Every artifact F-21 leans on (`TRIAGE_CANDIDATE_REGISTRY.json`, `STRATEGY_RESEARCH_REGISTRY.json`, `route_user_intake.py`) was last generated/committed 2026-06-06/07 — roughly 2.5 months before F-21 was written (2026-08-21) and this audit (2026-08-23). The literal front door, `00_INBOX/USER_INTAKE/`, currently holds no genuine strategy material at all — it holds unrelated AI-tooling notes and market-data CSVs (§5).
4. **F-21's own evidence bullets describe what exists *after* extraction and candidacy** (structured folders, statistical machinery) — they say nothing about how an idea gets from "noticed" to "extracted," which is exactly this audit's mandate and exactly where the gaps in §1–§5 above sit.

**Overall verdict: F-21 correctly describes a strong, real backend (statistical validation + structured strategy folders) but its claim that "the research intake pipeline... is the healthiest part of the research stack" overstates the front door specifically. The front door — discovery, dedup, triage, worthiness judgment, and queue tracking — is either a one-time historical exercise, undocumented-in-code, or entirely absent. If the wayfinder map is deciding what to build next for steps 1–3, F-21 should not be read as "this is solved."**

---

## Macro gaps — what's missing between "an idea exists somewhere" and "`SOURCE_LITERAL` + Missing-Rule Ledger exists"

- **No live intake queue.** `00_INBOX/USER_INTAKE/` is a drop folder with zero machine-readable state (no status, no timestamp, no count). Today it doesn't even hold strategy material — it holds stale unrelated files. There is nothing that tells anyone "N ideas are currently waiting" or "idea X has been waiting Y days."
- **No automated worthiness decision.** The only script that runs today (`route_user_intake.py`) explicitly declines to decide whether new material is worth pursuing — it prints `UNMATCHED` and stops. Extraction-worthiness is currently a human/agent judgment call made ad hoc, with no recorded criteria and no audit trail of accept/reject decisions.
- **No live dedup or channel-quality gate.** A real dedup+channel-quality design exists in prose (`09_TRANSCRIPT_INTAKE_WORKFLOW.md`) and was applied once to a May 2026 batch (`youtube_video_index.csv`), but nothing wires it into the pipeline that runs today — a duplicate video re-submitted now would not be automatically caught.
- **No capacity or throughput model at all.** There is no notion anywhere of how many ideas per week should enter, how large the queue is allowed to get, or how to prioritize when there's more raw material than capacity to process it.
- **No provenance link from registry candidate back to intake source.** `STRATEGY_RESEARCH_REGISTRY.json` has no field connecting a strategy to the raw transcript/URL that produced it — the "why was this extracted" trail is lost once a candidate is created, unless it happens to also appear in the separate, stale `TRIAGE_CANDIDATE_REGISTRY.json`.
- **`SOURCE_LITERAL` and the Missing-Rule Ledger are pure architecture, not artifacts.** Step 3 of the planned 21-step lifecycle (§6.3 of the master brief) has zero implementation: no schema file, no code that produces it, no example instance anywhere in the repo. Building steps 1–3 as currently planned means building this from scratch, not wiring up something that half-exists.
- **Everything that does exist at the front is stale, not merely quiet.** The registries, the router script, and the last real routed intake are all ~2.5 months old relative to this audit. Any wayfinder decision here should assume "rebuild/relaunch the intake front," not "resume an idling one."

---

## Sources cited

- `MTC_COMMAND_CENTER/00_INBOX/USER_INTAKE/` (directory listing + `README.md`)
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/route_user_intake.py` (full file)
- `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` (full file)
- `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` (full file)
- `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` (schema + sampled entries + field search)
- `MTC_COMMAND_CENTER/05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (summary block + sampled entries + field-value counts)
- `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md` (full file)
- `MTC_COMMAND_CENTER/03_QUANTLENS/_registry/youtube_video_index.csv` (header + sampled rows)
- `MTC_COMMAND_CENTER/11_TRIAGE/extract_urls_from_intakes.py` (header/docstring)
- Git blob `764da27f:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` — §6.1 (source profiles), §6.2 (Missing-Rule Ledger), §6.3 (lifecycle diagram), F-21
- `git log` dates for: `USER_INTAKE/`, `route_user_intake.py`, `STRATEGY_RESEARCH_REGISTRY.json`, `TRIAGE_CANDIDATE_REGISTRY.json`, `youtube_video_index.csv`
- Repo-scoped greps (`MTC_COMMAND_CENTER/` only) for: `SOURCE_LITERAL`; `Missing-Rule Ledger` / `Missing Rule Ledger` / `missing_rules:`; `video_id|transcript_hash|WATCHLIST|BLACKLISTED`; `capacity|per week|per day|rate limit|...` scoped to `_AI_MEMORY/`

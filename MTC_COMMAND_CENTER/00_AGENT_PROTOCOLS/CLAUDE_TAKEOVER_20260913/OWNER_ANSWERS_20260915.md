# Owner answers recorded 2026-09-15 (Claude Opus 5 Lead, session 743291)

## Q1 — WP-P0-20 bounded measurement with the Grok pre-screen slot vacant (asked ~05:41Z; answered ~05:55Z)
Lead question (chat): the derived-plan review roster named in `OD-20260914-P020-MEASURE-1` is "Grok pre-screen + exact Sol + Gemini"; the SuperGrok route answered `402 Grok Build usage balance exhausted` (probe 05:25Z, `C:/tmp/GROK_PROBE_20260915/probe.txt`); exact Sol (PASS-WITH-NITS, 0 REQUIRED) and Gemini 3.7 (PASS-WITH-NITS, 0 REQUIRED) and the Lead check (ALL EQUAL) are complete — "Run the measurement now with Grok slot vacant? yes / no, wait for Grok (Sep 18)".

Owner chat, verbatim: `no, wait for Grok (Sep 18)`.

Recorded as DECISIONS.md row `OD-20260915-P020-MEASURE-GROK-1`. Consequence: the bounded measurement (`run_bounded_benchmark.py --run` over the derived plan `d84b043a…`) is NOT executed before a Grok pre-screen of the derived plan + derivation tool is obtained after the SuperGrok weekly reset (2026-09-18); the prepared launcher `p020_measurement_run.ps1` gains a Grok-report gate; the derived plan, the Sol and Gemini reports and the Lead check stay valid as long as the pinned bytes do not change (plan `d84b043a…`, tool `0bfd1891…`, driver `3d4453cd…`, base plan `c6f07afd…`). Nothing is executed by this answer; no acceptance or production authority arises from it. The Wednesday exact-Opus queue for P020 therefore covers the derivation tool/derived plan review only; the measurement terminal and its corroboration move to Sep 18 or later.

Recorded by Claude Opus 5 Lead (743291).

## Q2 — who builds P1FIX while every Codex route is capped (asked ~06:27Z; answered ~06:36Z)
Lead question (chat): all Codex homes hit their weekly usage limit on 2026-09-15 (Plus `secondary`/`fourth` until 2026-09-19 18:47 local, `free` until 2026-09-19 11:10, `third` until 2026-10-06); OpenCode Go hung; the Gemini coder wrapper needs PowerShell 7 (absent). P1FIX (the capture-tool correction the owner's signature capture depends on: F-1 run-id gate, verify-first, F-2 half-open window, the nine NITs and L-1..L-6) — "(A) I write it myself now (reviewed by Gemini delta + exact Opus Wed + exact Sol Sep 19 before acceptance; capture possible today after Gemini), or (B) wait for Codex Sep 19 (capture slips to the weekend). My recommendation: A."

Owner chat, verbatim: `A`.

Recorded as DECISIONS.md row `OD-20260915-P012-P1FIX-LEAD-1`. Consequence: the Lead (Claude Opus 5) implements P1FIX itself in the worktree `C:/tmp/P1CAP_20260914` under the P1FIX brief, discloses the authorship in the commit and records, proves RED on the pre-fix tool / GREEN on the candidate, and commits; acceptance still requires the full independent roster (Gemini delta detection, exact Opus after the 2026-09-16 20:00Z reset, exact Sol after the Codex reset) — the Lead does not accept its own code. The real read-only capture of the owner's account may run today only after the Gemini delta review of the Lead's fix and with the owner's signature; it stays NONACCEPTING evidence until the roster completes. Nothing else is authorized by this answer.

## Q3 — WP-P0-27 failure-notification delivery (asked ~08:27Z; answered ~08:32Z)
Lead question (chat): after the D026 red demonstration (PR #192, run 34946092493, `Bridge suite (Python 3.12)` FAILURE at 08:18Z) — "did you get GitHub's 'Run failed: CI' e-mail (~08:18Z)? yes/no".

Owner chat, verbatim: `yes`.

Effect: an owner-side verification, not a decision. It closes the delivery half of plan requirement R5 ("a red master run notifies immediately") for the day-one channel (GitHub-native Actions failure e-mail to the subscribed account) — recorded in `QUEUED_PACKAGES_20260915/P027_REQUIREMENT_RECONCILIATION_20260915.md` (R5 → VERIFIED by owner statement) and `P027_RED_DEMO_EVIDENCE_20260915.md`. With R6 executed and R5 confirmed, the plan's four-part WP-P0-27 acceptance gate is satisfied at the day-one scope; package acceptance itself remains the Lead's roster call (Gemini corroboration of the reconciliation + the T1 flagship verdict already recorded for the workflow files), and the progressive backlog R9-R15 stays open by design. Nothing else is authorized by this answer.

## Q4 — WP-P0-28 eligibility read (answered ~08:29Z) and WP-P0-26 repair builder (answered ~08:34Z)
Owner chat, verbatim: `P028 read go` — authorizes ONE read-only capture of `subAccounts`, `userFees`, `userRole` (+ `clearinghouseState`) for the owner's own mainnet address (the Path 1 address `0x1E26…AC49`, the packet's default; no other address was named) with the owner's `personal_sign` ownership signature over the fresh run_id `p028-eligibility-20260915-r1`, stored write-once with sidecars and a manifest like the Path 1 capture (`QUEUED_PACKAGES_20260915/P028_ACCOUNT_ELIGIBILITY_PACKET_20260915.md` §3-§4). No credential, no order, no sub-account creation, no venue write. The capture is NONACCEPTING evidence until the tool and the capture are reviewed. Row `OD-20260915-P028-READ-GO-1`.

Owner chat, verbatim: `A` (answering "P0-26 repair 'A' (me now) / 'wait' (Codex Sep 19)") — the Lead (Claude Opus 5) implements the WP-P0-26 bounded local repair accepted on 2026-09-12 exactly within the scope packet `C:/tmp/P026_LOCAL_SCOPE_DECISION_20260907.md` §2-§5 (5 MODIFY files under `MTC_COMMAND_CENTER/tools/opsa/`: `backup.py`, `restore.py`, `opsa_common.py`, `watchdog.py`, `test_opsa.py`; 0 ADD; fake/fixture tests only; no host contact, no notifier, no schedule, no delete path), disclosed in the commit; RED/GREEN on the pre-fix code required; acceptance keeps the T1 roster (Gemini corroboration + exact flagship review) and the Lead never accepts its own code. Row `OD-20260915-P026-REPAIR-LEAD-1`.

## Q5 — WP-P0-26 adapter fix (asked ~09:35Z and again ~10:36Z; answered ~10:50Z)
Lead question (chat): "P0-26 adapter fix: A (I do the 6 lines now) / B (park till Codex Sep 19)" — context: the repaired explicit-run restore gate refuses the P0-30 closed-partition backup adapter's isolated restore root (`check_p030_closed_partition_backup_adapter.py`: 44 tests, 7 failures + 2 errors, 13 `run_not_complete` refusals) because that root lacks `COMPLETE.json` / `RUN_MANIFEST.jsonl`; both files sit at the repo root, outside the scope packet's five-file ceiling.

Owner chat, verbatim: `A`.

Effect: `OD-20260915-P026-ADAPTER-LEAD-1` — the slice is extended by exactly two repo-root files (the adapter and its checker); the Lead builds it as a further disclosed commit on the same branch; adapter checks must return to exit 0; RED on the pre-fix adapter required; roster unchanged (Gemini + exact Opus + exact Sol); the Lead never accepts its own code.

## Q6 — WP-P0-27 CI additions (asked ~09:35Z and again ~10:36Z; answered ~10:52Z)
Lead question (chat): "P0-27 CI additions: go (one PR: contracts tests + 3 P030 checkers + Ruff step) / later".

Owner chat, verbatim: `go`.

Effect: `OD-20260915-P027-CI-ADDITIONS-GO-1` — ONE PR changing only `.github/workflows/research-gates.yml` (informational workflow; required contexts unchanged); opened for review, not merged by this word.

# LEAD_ADJUDICATION_R6_SOL — exact gpt-5.6-sol xhigh round-6 review of WP-P0-20 preselection V1.6 — 2026-09-14 20:40Z

Slot: Codex Plus (`secondary`, `--add-dir` lane, scratch cwd), launched by `codex_reset_queue_r6.ps1` at 20:11:03Z after the pool reset; finished 20:34:32Z (23.5 min), exit 0; report written by the reviewer to `sol/SOL_T0_REPORT.md` (357 lines; the `--add-dir` fix from round 5 held).

**Verdict as returned: PASS-WITH-NITS — 0 REQUIRED, 3 NITs.** Identities COMPUTED (HEAD, frozen `cb756020…`, procedure/tests/records, checksum manifest); 106/106 tests; scratch freeze byte-identical; authorization RED arms (no token / dead V1.5 token / `--freeze` with token) refuse; real-record interval probe and interval RED arm; D5 driver + derivation tests; D9-A: V2→V3 diff exactly three leaf changes, `BENCHMARK_PLAN.json` changes only driver digest + instrument path/id/digest, `run_bounded_benchmark.py` only the `RECORD_PATHS` line, owner-policy pin equal (`requested_risk_fraction` 0.0001); the ten sizing tests observed GREEN with V3 / exact-clause RED with V2 on all five timeframes, and repointing each RED fixture to V3 turned it GREEN (dependence on the record proven). The reviewer did not pass the digest to `--oneshot` and did not run `--run`.

| NIT | Finding | Disposition |
|---|---|---|
| Sol-6-1 | exclusive create is not an exclusive lock; `commit` does not re-hash the committed paths (`preselect_profile.py:652-668`) | residual carried from rounds 4/5 (Grok/Opus N6-2 family); the Lead reads the outputs and their digests after every shot (launcher logs sha256 of both files) |
| Sol-6-2 | a second storage failure during ABORTED recovery can leave a mixed pair; `first_error` unused (`:660-697`) | same as Opus N6-2; residual; documented in the phase table; not reachable without two independent storage failures |
| Sol-6-3 | `BENCHMARK_PLAN.json:323` annotation still says quantity step `Decimal('1')` while the pinned V3 says `0.00001` | documentation residual (the executable mechanism reads the record); fold into the next re-freeze with Opus N6-1/N6-7 |

None changes the executable selection, record pin, risk value or gate result — the reviewer says so and the Lead agrees.

**Roster round 6 on frozen V1.6 `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126`: Lead REPRODUCED, Gemini 3.7 PASS (SATISFIED), exact Opus PASS-WITH-NITS, exact Sol PASS-WITH-NITS — both exact flagships accept the same bytes.** Grok pre-screen: not available (weekly cap) — supplemental slot vacant, recorded. The one-shot (`p020_eligibility_run_v16_wrapper.ps1`) may now run once under D1 Option A + `OD-20260914-P020-RECORD-V3-1`. Adjudicated by Claude Opus 5 Lead (b9df29).

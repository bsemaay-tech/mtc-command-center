# LEAD_ADJUDICATION — lane 1, third exact `claude-opus-5` xhigh T0 read of WP-P0-31 M1 at `61c56148` (T0 repair round 2 of the cap 3) — 2026-09-17 14:0x UTC+3

**Lane history:** read 1 (`48bd70de`, 09-16) REQUEST_CHANGES F-1 → fence `e9e37aec`; read 2 (`e9e37aec`, 09-17 08:03) REQUEST_CHANGES F-2 → two fences `61c56148` (Gemini `P031_R2_GEMINI` PASS); **read 3** launched by hand 13:22 UTC+3 after lane 4: 13:22-13:53 (10:22:52-10:53:23Z), launcher exit 0, 187 turns, no 429; report `opus/OPUS_T0_REPORT.md`, 827 lines.
**Verdict as returned:** `VERDICT: PASS-WITH-NITS` — **0 REQUIRED**. F-2 CLOSED on the reviewer's own mutants (M-A `:812-813` removed → exactly the retired-identity test RED; M-B `:814-816` removed → exactly the foreign-identity test RED; restore → 112 passed / 1 skipped / 167 subtests); guard walks re-derived from the bytes and corroborated by the mutants ACCEPTING; whole invariant asserted incl. the replay for both candidates; cannot pass for the wrong reason; F-1 stays closed (§4); all twelve owner answers IMPLEMENTED-AS-ANSWERED (§5); a **23-guard mutation sweep found no third member of the F-1/F-2 class**; 30 hostile arms on the public seams admitted nothing the answers refuse (§6). Seven NITs N-14..N-20 (N-16 substantive); N-4/N-5/N-6/N-8/N-10/N-13 re-raised as carried/owner items.

## Lead reproduction
| Check | Result |
|---|---|
| Citations — ledger `:614-618`, `:628-630`, `:731`, `:744-753`, `:946` (`enforce_active=True`), `:1103` (`enforce_active=False`), `:1105-1107`, `:1488` (CLI builds the ledger without a catalog), `:374` (purpose → versions), `:399` (TRY004 site); base `c76043b9` `:269` (`active_check_sets … = None` already) | **EXACT** at the blobs |
| N-16 reproduced (the shipped CLI cannot read a catalog-backed ledger) | the reviewer's `cli_probe.py` executed by the Lead against the worktree (`LEAD_REPRO_N16_cli_probe_third_read.txt`): all-`catalog_backed=False` ledger → `report` exit 0 (5309-byte JSON); one `catalog_backed=True` record → exit 1 `ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` — **CONFIRMED** |
| N-17 (two wrong sentences in the Lead's G1 amendment prose) | CONFIRMED from `:374` and base `:269` → **correction entry appended** to `G1_SCOPE_AND_CONTRACT.md` (sha256 `c82de2a8…` → `0bcd6abc…`; copy refreshed in the P031_FIX records) |
| N-20 (brief `## Subject` still pinned `e9e37aec`) | CONFIRMED → **fixed**: title + Subject line re-pinned to `61c56148` (addenda keep their history; note appended) — the Sol generator now inherits a consistent brief |
| N-19 (one new Ruff finding, `:399:13 TRY004`, unrecorded) | consistent with the module's convention (four pre-existing TRY004); recorded here — no change asked |

## NITs — disposition
| # | Finding | Lead reading | Disposition |
|---|---|---|---|
| N-14 | `CHECK_SET_PURPOSE_UNKNOWN` (`:614-618`) unfenced (mutant G17 green); no untrue record on the mutant | true; the `str`-subclass family lacks a `check_set_purpose` member | **carried** into the P0-31 semantic slice (one test: undeclared string + `str` subclass → `CHECK_SET_PURPOSE_UNKNOWN`) |
| N-15 | `CHECK_SET_PURPOSE_MISMATCH` supplied-vs-fixed (`:628-629`) unfenced (mutant G19 green); the mutant stores the truthful fixed purpose, so the lost property is "refused" vs "silently ignored" | true | **carried** into the same slice (one test) |
| N-16 | the OD-11 catalog guards (`:744-753`) sit above the `enforce_active` switch, so a catalog-backed ledger is unreadable (replay / current_state / verify_integrity / report / backup) without the exact catalog, which is never persisted; the shipped CLI has no way to pass one | true; fails closed and loud; opt-in feature; the reviewer's own reading admits refusing may be correct; "becomes REQUIRED if the roster judges the read-only report a shipped M1 seam" | **owner one-liner `N-16 A|B`** — A = thread `enforce_active` through the catalog guards (committed history readable without the catalog; weaker read-time verification) / B = give the CLI and `main()` a way to supply the accepted catalog and disclose in the report whether one was configured (keeps fail-closed; also closes half of N-6). **Recommended: B.** Built in the semantic slice after the owner's word; Sol reads the candidate as is |
| N-17 | two inaccurate sentences in the G1 amendment log | true | **fixed today** (correction entry) |
| N-18 | the OD-7 refresh path requires an unchanged `package_hash` (`:805-811`), narrower than 6A's "new composite" (a new package at a deep rung has no route) | true; fails closed | **owner note** for the M1 acceptance packet (explicit narrowing, not a code change now) |
| N-19 | one new full-rule Ruff finding (`TRY004` in `_normalize_accepted_catalog`) unrecorded | true; convention-consistent | **recorded** (this note); no change |
| N-20 | brief Subject stale | true | **fixed today** |
| N-10 / N-13 | re-raised | already RULED by the owner 09-17 (`OD-20260917-P031-M1-N5-N10-N13-1`: yes / yes) | in the semantic slice |
| N-5 / N-6 / N-4 / N-8 | re-raised as carried | N-5 RULED (B); N-6 half-closed by N-16 B; N-4 / N-8 carried | as in the NIT ledger |

## Standing
The M1 candidate `61c56148` now carries: exact-Opus PASS-WITH-NITS (third read; two REQUIRED classes closed across rounds 1-2 within the T0 cap), Gemini PASS ×2 (R1, R2), the Lead's reproductions. Roster still needs the second flagship (exact Sol, Sat 2026-09-19) before the M1 acceptance packet goes to the owner; the Lead built the fences and cannot accept. After Sol: the semantic slice (N-10 epoch, N-13 retire, N-5 rule B, N-14/N-15 fences, N-16 per the owner's letter) as one reviewed candidate; then the acceptance packet (with N-18 as an explicit note and N-11 blob-OID pins).

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).

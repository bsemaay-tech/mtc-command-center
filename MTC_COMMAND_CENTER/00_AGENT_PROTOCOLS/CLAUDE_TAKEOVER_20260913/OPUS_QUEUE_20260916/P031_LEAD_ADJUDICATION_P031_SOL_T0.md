# LEAD_ADJUDICATION - exact-Sol T0 read of WP-P0-31 M1 `61c56148` (Codex PRO account `free`, gpt-5.6-sol xhigh; Sat 2026-09-19 11:11-11:37 UTC+3; adjudicated 12:4x)

**Verdict as written:** **REQUEST_CHANGES** - one REQUIRED (F-1), one NIT (N-1). 212 lines, 26 min, launcher exit 0 (the chain's "CAPPED" line after it was a false stop on quoted text - the report is complete). Identities computed by the reviewer match the pins (HEAD `61c56148`; ledger blob `7e7874770d…`, test blob `c72452f6…`); pinned interpreter 3.12.12; worktree after the lane: only the three pre-existing untracked `TASK_P31*.md`; suites `112 passed, 1 skipped, 167 subtests` + 50 contract tests. The reviewer confirmed the three mandated repair mutants (rounds 1-2) behave and did not read any Opus report.

## F-1 (REQUIRED) - CONFIRMED and reproduced by the Lead
Claim: OD-6 (option 5C) says the capacity target of an `ADMISSION_WITHHELD_CAPACITY` event is derived from the supplied `check_set_version`'s purpose, fail-closed on zero or multiple matches. `_purpose_for_check_set_version` (`p031_lifecycle_ledger.py:596-606`) does that, but `_resolve_check_set_purpose` (`:623-626`) returns `supplied_check_set_purpose or self._purpose_for_check_set_version(...)`, so a WRITER-supplied purpose bypasses the uniqueness rule; the later checks (`:724-740`) only validate membership. Grep-verified: all three cited ranges match the `61c56148` blob byte for byte.
Reproduction (`CLAUDE_P0_RUN_20260913/P031_SOL_20260919/LEAD_REPRO_F1_dup_version_purpose.txt`, pinned 3.12.12, real module through the test helpers, `shared-capacity.v1` configured under BOTH `paper_eligibility` and `testnet_live_candidate_eligibility`, candidate built to SHADOW):
- control (unique version, no purpose): APPENDED - as designed;
- duplicated version, no purpose: **REFUSED `ADMISSION_WITHHELD_TARGET_UNRESOLVED`** - the fail-closed rule works;
- duplicated version + `check_set_purpose="paper_eligibility"`: **APPENDED**;
- duplicated version + `check_set_purpose="testnet_live_candidate_eligibility"`: **APPENDED** - the writer chooses EITHER target, which is rejected option 5A in effect.
F-1 stands. Required repair (the reviewer's wording, which the Lead adopts): for `ADMISSION_WITHHELD_CAPACITY` derive the purpose ONLY from `check_set_version`, refuse zero or multiple matches regardless of a supplied purpose (a supplied purpose may at most be checked for equality with the derived one), plus a permanent counterfactual test for the duplicated-version registry with and without a supplied purpose.

## N-1 (NIT, documentary) - the review brief's G1 amendment identity is stale
`C:/tmp/P031_LEAD_20260912/G1_SCOPE_AND_CONTRACT.md:79-80`: the brief pins `c82de2a8…` while the file is `0bcd6abc…` (line 80 gained a later correction); seams and pre-amendment identity intact. Fix the brief pin in the next re-pin.

## Standing
P0-31 M1 `61c56148`: exact-Opus PASS-WITH-NITS (third read) + Gemini PASS, but **Sol REQUEST_CHANGES** → not merge-ready. Repair = T0 round 3 of the cap 3 for this candidate (rounds 1-2: `e9e37aec`, `61c56148`). Per the owner's package-session routing this repair goes to the **P0-31 package session (Opus 5)** together with the semantic NIT slice (N-5 B, N-10, N-13, N-16 B, N-14/N-15 fences, N-11 blob pins), then Gemini delta + exact-Opus re-read + Sol re-read on the final bytes. Not on the P0-12 path; scheduled after today's P0-12 close. The Lead never accepts its own code.

Recorded by Claude Fable 5.1 Lead (session 7, `18c1b8`).

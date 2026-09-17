# T0 review brief — WP-P0-21 S1 catalogue-only slice (owner S2 values in the readiness rule catalogue), candidate `7fecf204c5d457ff19872c97e5d27e2d5a712508` (exact `claude-opus-5` xhigh; Wednesday 2026-09-16 slot, OPTIONAL lane — only if allowance remains after lanes 1-5; also the source brief for the Friday Sol lane)

You are a fresh, independent T0 reviewer. Your exact role (model and effort) is fixed by the launcher that started you; do not delegate, resume any other session, or spawn agents. Output ONE report file named in your launch instruction; write nothing else outside your own report directory (scratch copies under `C:\tmp\OPUS_P021S1_SCRATCH` only). The candidate is LEAD-AUTHORED (Claude Opus 5 Lead, disclosed); the Lead never accepts its own code — you are the first exact flagship read.

## Context (settled facts; verify identities, do not re-decide)
- Package WP-P0-21 (readiness rules). Base `origin/master` `fcac0ac6`. Branch `feature/p021-s1-policy-v1-numbers-20260915`: `701c5ddd` (catalogue + tests; Lead-built under `OD-20260915-P021-S2-RECOMMENDED-1`, owner word "recommended" answering `P021_OPTIONS_PACKET_S2_20260915.md`) + `7fecf204` (test-only: Gemini NIT-1/NIT-2). Three files under `MTC_COMMAND_CENTER/03_QUANTLENS/tools/`: `p021_readiness_rules.py`, `tests/test_p021_eligibility.py`, `tests/test_strategy_type_policy_set.py`.
- What it claims: `gap_ratio_max = 0.0001` on `m2_missing_bar_ratio` CLOSED (`P021_DECISION_3 = T`); DATA_QUALITY carries the B-17 formula pin and the B-13 `ds-v1` pin as limits; divergence metric M-C (B-05) recorded; `POLICY_SET.owner_decisions` extended with a dated S2 source; the hashed `strategy_type_policy_set` artifact UNTOUCHED (`shared.gap_ratio_max` stays `None` until B-22 — owner ask H); every check still refuses readiness.
- Reviews so far: Gemini 3.8 detection COUNTED PASS-WITH-NITS (fidelity EQUAL x4; fence intact; `QUEUED_PACKAGES_20260915/P021_S1_20260915/GEMINI/`); Lead verification + RED arms 1-3 (`LEAD_VERIFICATION_P021_S1.md`). Lead = author, never acceptor.

## Subject (read-only worktree; verify before reading anything else)
- `C:/tmp/P021_S1_20260915`, HEAD must be `7fecf204c5d457ff19872c97e5d27e2d5a712508` (`git -c safe.directory=* -C C:/tmp/P021_S1_20260915 rev-parse HEAD`; NO other git command — never status/diff-with-working-tree/add/commit/checkout; `git -c safe.directory=* show <rev>:<path>` and `git -c safe.directory=* diff fcac0ac6 7fecf204 -- <paths>` for byte comparisons only, and say so). If HEAD differs, STOP and write `VERDICT: BLOCK` with the observed HEAD.
- Tests: from the worktree root, `PYTHONPATH=MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools` then `python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py -q -p no:cacheprovider --basetemp C:/tmp/OPUS_P021S1_SCRATCH/bt`.
- Records: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/QUEUED_PACKAGES_20260915/P021_S1_20260915/` (verify every closure against bytes, never against a report's description).

## What you must decide
1. **Fidelity:** each of the four values/pins in the code vs the DECISIONS row `OD-20260915-P021-S2-RECOMMENDED-1` and the S2 packet text — EQUAL/DIFFERENT with file:line; DIFFERENT = REQUIRED.
2. **Fence:** run `python p021_readiness_rules.py --self-check` and the two test modules (`PYTHONPATH=MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools`, pinned 3.12.12; expect 59 passed + 108 subtests incl. `test_data_gap_ratio.py`); prove with your own mutant that a rule with `missing_rules=()` is refused by `validate_catalog` and that `readiness_record()["ready"]` cannot become True; reproduce RED arms 1-2 (new tests on `fcac0ac6` catalogue bytes fail; old tests on the new catalogue fail).
3. **Artifact contradiction:** catalogue `0.0001` vs artifact `None` — is there any consumer on master that reads both and could act on the difference? (grep `gap_ratio_max` consumers, read-only.) State the answer; the whole-set ratification is the owner's B-22 act, not yours.
4. **Formula pin honesty:** does `data_gap_ratio.py` compute m2 exactly as the pin text says (numerator, denominator, half-open span, leading/trailing exclusion)? Cite lines.
5. **Scope:** exactly three files; no protected path; the pre-existing F401 on master is not the slice's.

## Report format
Markdown with: verified identities (COMPUTED HEAD, sha256 of the catalogue file); fidelity table; fence proof with commands/cwd/output; artifact statement; formula-pin statement; findings REQUIRED/NIT with file:line; NOT VERIFIED; final line exactly `VERDICT: PASS` / `VERDICT: PASS-WITH-NITS` / `VERDICT: REQUEST_CHANGES` / `VERDICT: BLOCK`.

Written by Claude Opus 5 Lead (session 5, `03c6c8`) 2026-09-15 20:2xZ; the Lead is the author of the candidate and is not a reviewer here.

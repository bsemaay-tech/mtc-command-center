# Exact Sol T0 bounded execution audit

## Verdict — REQUEST_CHANGES

The authorized R30–R32 correction plus the 15-byte portability repair is behaviorally green on frozen `7f22a4f17a458e843a45c162cbbc843a33d822ba`, but I cannot accept the whole bounded candidate: the repair commit lacks the repository-required protected-path trailer. This is not full P012 or production acceptance.

## Personal execution and identity

I personally ran published commands 1–4 once from `C:/tmp/P0R32S3/scratch`, using `C:/Python314/python.exe`, with the inherited environment unchanged.

- Command 1: exit 0; Python 3.14.2; import resolved only to owned source `C:/tmp/P0S32A/.../mtc_v2`; temp resolved to `C:/tmp/P0R32S3/scratch`. `PYTEST_ADDOPTS=-o cache_dir=C:/tmp/P0R32S3/scratch/cache`; `shlex.split` preserved that exact absolute cache token.
- GREEN: exit 0, PASS, 9 semantic rejections, 2 control passes, 0 unexpected blocks.
- Intentional RED: exit 1, RED, the same 9/2/0.
- Full gate: exit 0 in 37.4 s; 495 passed, 0 failed; no failing IDs; `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`; no acceptance blockers; expected-source provenance `MATCH`, observed build `7f22…`, expected path changes 0; 17 scenarios/34 legacy surfaces MATCH; 10/10 probes DETECTED.

HEAD was `7f22…` and tracked status was empty before and after. Prior `44288622851536eb1f300a4a525baeb1a00e6634`, merge-base `442886…`, and fixed base `5e8e579410ee55008bfd2d2d85054fd1d782f32c` resolved exactly. Original packet: 2817/2817 manifest entries match; supplement: 8/8 match. Original TASK/manifest hashes are `3657cf…1d72`/`627e3e…43a4`. Live repaired test hash equals `TEST_AFTER.py` (`1bd7b8…c7ef`); the sole parent delta removes `, dir=r"C:\tmp"`.

The prior Sol S2 result remains a failed attempt: GREEN 0, intentional RED 1, then full-gate tool timeout 124 at 120.4 s with zero stdout because the backslash cache argument became drive-relative. I do not convert that historical BLOCK into a pass; today’s corrected-launcher run is separate personal evidence. The 35 s diagnostic (495 pass, one existing skip, shutdown hang) and Lead 33.42 s 495/0 run remain supporting, not substitute, evidence.

## Standards

**Required finding:** commit `7f22…` changes `tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`, within the directory previously ruled a protected “Canonical feature contract,” but its message contains no `APPROVED-PATCH-PLAN: <task_id>`. `PROTECTED_PATHS_POLICY.md` modification-gate item 5 calls the trailer required. Package history records identical omissions as blocking until explicit owner waiver. No waiver is authorized here. Smallest compliant resolution: rebuild/supersede this repair from `3e9…` under a recorded approved repair task and required trailer, then refresh SHA-bound audits. Standards findings: 1 hard; no new smell finding.

## Spec/source

Carried forward from the incomplete S2 personal source inspection—not newly claimed as mine here—are its 72-file diff review, two record/sidecar matches, nine probe-copy matches per record, six frozen-source hashes, 19-member seal match, 34 semantic baseline equality, six `UNCHANGED` Section-16 dispositions, and zero unresolved receipt items. I personally rechecked the repair hunk, commit chain/trailers, packet manifests, I5 five-source aggregate (`da2bf1…f097ed`), `KEEP_REFUSED`, and prior findings. No behavioral/spec blocker was found.

Three optional Opus nits remain unchanged: aggregate recomputation exists only as hardcoded test expectations; reseal-31 says “no economic changes” instead of “no economic-value changes”; five mutant AssertionErrors have empty messages. Gemini 3.8’s Item-1 manifest-range citation imprecision and mandatory NOT VERIFIED section remain; all six `UNCHANGED` ratifications remain bounded. The four pre-existing `CHAIN_UNVERIFIABLE` declared-field refusals are report-only under HIST0030. Sol R3’s real 475 pass/1 skip/1 warning and R5’s real 475/0 exit 0 at `7cc095…`, plus its design-identity BLOCK dissent, remain historical facts; the v1.25 title correction addresses the current identity without validating the old overrule. Original Opus whole-scope PASS-WITH-NITS at `3e9…`, fresh Opus repair PASS at `7f22…`, and Gemini 3.7 static corroboration remain valid only within their stated limits.

## NOT VERIFIED and boundaries

Whether the unchanged conditional symlink skip fired today is NOT VERIFIED; the gate receipt exposes passed/failed only. D026 neutralizes the old I5 digest only in memory after actual byte/sidecar verification, so it is not end-to-end mutant acceptance; the unmodified 495-test suite retains the production digest fence. I did not re-derive all 19+40 formulas, validate production facts, redo receipt 29, recapture C31, inspect outside-packet callers, run CI/integration, contact networks, or authorize trading/spend. All 27 production risks, 5 integration obligations, 10 accepted Section-19 closure-evidence items (distinct), `fee KEEP_REFUSED`, FINAL-production-only receipt-29 redo, and deferred capture remain.

NEXT ACTION: Lead rebuilds the 15-byte repair as a trailer-compliant successor and repeats identity-bound required audits.

WAITING FOR OWNER: Nothing; standing same-package repair authority can route that work, but this candidate remains unaccepted.

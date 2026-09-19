# LEAD_ADJUDICATION — Wednesday lane 5: exact claude-opus-5 xhigh T1 review of PR #193 (`a3325836`) and PR #194 (`63b7bbe0`) — run early 2026-09-16 13:27-13:41 UTC+3 (10:27-10:41Z) on the leftover Pro allowance (owner's word 13:0x: use it before the 20:00Z reset)

**Verdicts returned:** `VERDICT #193: PASS-WITH-NITS`, `VERDICT #194: PASS-WITH-NITS`; **0 REQUIRED**, 9 NITs (F-01..F-09). Launcher `exit=0`, 830 s, 105 assistant turns; report `OPUS_T1_REPORT.md` (295 lines) with computed identities, 31 read-only `gh` calls listed, read-only git only (no status/add/commit/checkout/push — as the brief required), a non-empty NOT VERIFIED list (10 items).

## Lead reproduction (bytes, not the reviewer's numbers)
| Claim | Reproduced | Result |
|---|---|---|
| `research-gates.yml:114-115` `git config --system core.longpaths true`; `:160-163` hash-locked install; `:169-170` `pip install ruff==0.16.4` unpinned by hash | `git show a3325836:.github/workflows/research-gates.yml` lines 114-115, 160-163, 169-170 | EXACT |
| `opsa-tests.yml:39-40` same `--system`; `:55` `python -m unittest test_opsa -v` (one module, no discover) | `git show 63b7bbe0:.github/workflows/opsa-tests.yml` | EXACT |
| F-03 drift example: lock `packaging==26.2` vs contracts `constraints.txt` `packaging==26.3` | `requirements.lock:791` = `packaging==26.2 \`; `contracts/constraints.txt:7` = `packaging==26.3` | CONFIRMED |
| Ruleset 21444962: exactly two required contexts, strict | `gh api …/rulesets/21444962` at 10:4xZ: `["Bridge suite (Python 3.12)","pine-alert-guard"]`, `strict: true`, `enforcement: active` | CONFIRMED |
| F-09: `CI_POLICY.md` still says only the Bridge suite is required / `pine-alert-guard` not required, contradicting the live ruleset and its own acceptance paragraph | master `fcac0ac6` lines 95-97; CT13 lines 108-110 vs 20/25 (the reviewer cited the CT13 copy's numbers, `:107-111` / `:19-20`) | CONFIRMED (documentary; T2/T3 fix on CT13 later) |
| PRs OPEN / MERGEABLE / checks SUCCESS | `gh pr view` 10:37Z | CONFIRMED |
Note: the reviewer's `CI_POLICY.md` line numbers are those of the CT13 copy (it had `--add-dir C:\CT13`), not master's; the text claims hold in both copies.

## Concordance with the counted Gemini reads
Gemini (`P027_CI_GEMINI` attempt 4, counted; `P027_OPSA_GEMINI`, counted PASS 0 findings): N-01 (Ruff by version) = Opus F-01; N-02 (`--system` longpaths) = Opus F-02 / F-07; Gemini's E10 path note ≈ Opus F-08 (records). No contradiction between the two readers; Opus adds F-03 (dependency ownership drift), F-05 (red-master rule wording for informational jobs), F-06 (`unittest` one-module), F-09 (policy contradiction) — all NIT, none reproduced as REQUIRED by the Lead either.

## Disposition
- **Merge gate satisfied** for the T1 contract (`OD-20260915-P027-T1-WEDOPUS-1`: exact Opus T1 + the mandatory Gemini corroboration + Lead reproduction): merge #193 first, then update #194's branch onto the new `master` (strict policy) and merge #194 — the reviewer's order, adopted for its reason (the second PR's head gets the new gates before merging). Merge = standing git delegation; the owner asked for exactly this path ("we'd opus").
- NITs carried as follow-ups, none blocking: F-01 (hash-pin Ruff — becomes REQUIRED only if the contracts job is ever made a required context), F-03 (contracts lock of its own), F-05 + F-09 (CI_POLICY wording: informational-job red vs required-check red; the required list is two contexts), F-06 (`unittest discover` when the P0-26 repair lands), F-08 (erratum line in `RED_DEMO_EVIDENCE_20260915.md`), F-02/F-04/F-07 (notes; trigger conditions named).
- After both merges: re-read the ruleset once (must still be exactly two contexts); watch the `master` push runs (red-master rule).

Recorded by Claude Opus 5 Lead (session 6, `4a8233`); both PRs were Lead-built (sessions 4/5, disclosed in the acceptance packet) — the Lead never accepts its own code; the accepting T1 read is the exact-Opus reviewer, a fresh `--print` session on the Pro profile, corroborated by the counted Gemini reads.

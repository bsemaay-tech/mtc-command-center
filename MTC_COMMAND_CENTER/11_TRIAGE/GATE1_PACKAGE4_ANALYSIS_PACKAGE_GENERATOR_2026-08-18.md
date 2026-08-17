# Gate-1 Scope Record — Package 4: Owner Analysis-Package Generator (first increment)

**Date:** 2026-08-18 (overnight) · **Lead:** Claude (Fable) · **Tier: T1**
**Owner authorization:** 2026-08-17/18 night, in chat: explicit "devam" on the Lead's stated
default path (Packages 3, 4, 5a), after Decision 5; full autonomy reiterated (Decision 6).
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 4;
kickoff skeleton in `BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md`.

## Frozen scope (first increment)

A bounded, redacted, read-only export generator in the NEW directory
`IBKR_PAPER_BRIDGE/tools_v2/analysis_package/` (isolated worktree `C:\P4GEN`, branch
`feature/bridge-v2-package4`). Contents:

1. `generate_analysis_package.py` — stdlib-only Python. Inputs: an explicit allowlist of local
   files/directories passed by configuration (no defaults that touch live paths). Output: ONE
   Markdown bundle file.
   - **Format decision (first deliverable, decided here):** single self-describing Markdown
     bundle — header (generation time from caller-supplied timestamp, input inventory, bounds
     applied, redaction summary) + per-file fenced sections. Chosen for the documented manual
     Codex-subscription workflow (paste/upload one readable file).
   - **Bounds (enforced, recorded in output):** per-file cap 200 KB, total cap 2 MB, binary
     files excluded (extension + null-byte sniff), per-file line cap 4,000.
   - **Redaction (enforced, demonstrated):** pattern-based masking of secrets — long
     hex/base64 tokens, `key=`/`token=`/`password=`/`secret=` assignments, AWS-style ids,
     0x-prefixed 40/64-hex addresses/keys, bearer headers — each replaced by `[REDACTED:<kind>]`
     with a per-kind count in the header.
2. `fixtures/` — synthetic input files including planted fake secrets (clearly fake values).
3. `tests/test_generator.py` — pytest: bounds enforced, every planted secret redacted, binary
   exclusion, deterministic output given fixed inputs, output contains zero un-redacted planted
   values.
4. `README.md` — usage, boundaries, non-authority statement.

## Hard boundaries

- New directory only; zero modifications to existing files. No network capability in the code
  (no imports of urllib/http/socket/requests). No provider/API integration — output is a file
  handed over manually. No reading of real credential stores, `.env`, `auth.json`, or Windows
  Credential Manager; tests run on fixtures only. Standing prohibition list applies.

## Roles, review, acceptance

- Implementer: GLM-5.3. Review: DeepSeek `deepseek-v4-pro` + Gemini cross-check + Lead
  inspection with the test suite executed locally by the Lead (pytest green required).
- Done means: pytest green under the Lead's own run, redaction proven on planted fixtures,
  bounds proven, review findings resolved, committed on the package branch.

# KICKOFF — Codex T2: carry the accepted trusted-base disclosures into the successor preregistration

You are Codex `gpt-5.6-sol` xhigh, EDITOR. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit, no block-byte edits. Edit ONLY
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`.
Do not touch block files, self-QA files, STATUS files, tools, or the Audit-2 package.
Never git checkout/reset/stash any tracked file.

## Why
SEC102 was **ACCEPTED-WITH-DISCLOSURE by owner decision 2026-08-12 ~13:10**
(`WPI_PREREG_DRAFT_ROUND1/SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md`,
`STATUS_SEC102.md`). That acceptance is conditional on its assumptions being carried forward
**as explicit trusted-base statements** — the acceptance note says so in terms: they "must be
carried into the successor preregistration as trusted-base statements, and no successor text may
present any of them as a control." Right now they live only in a STATUS file and a
recommendation note. If freeze happened today, the preregistration would not state them.

The distinction this whole work package turns on: **a disclosure is not a control, but an
honestly-scoped, explicitly-labelled weaker claim IS acceptable where a static tool genuinely
cannot reach further.** Your edit must make that distinction impossible to lose.

## What to add
A new subsection in the successor preregistration — place it where a reader meets it BEFORE any
§10.2 acceptance language, and cross-reference it from the §10.2 discussion — titled so it reads
as a limitation, e.g. **"Accepted trusted-base assumptions (disclosed, not proven)"**.

It must state, each as its own numbered item with its source:

1. **The outer Python runtime.** The `python` that runs the §13 evidence harness, its startup
   mode, import graph, startup environment and standard library are TRUSTED, not bound. The
   published launch is bare `python -B`
   (`isolated=0 safe_path=0 no_site=0 ignore_environment=0`), so an actor controlling the wrapper
   directory or the Python startup/import environment could shadow `subprocess` and fabricate
   transport or completion. Source: Codex R11-F1,
   `SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md`.
2. **The interpreter image.** `powershell.exe` is located by name from `PATH`; a different
   program could receive the intended bytes. Codex adjudicated this disclosure HONEST as written.
   Source: STATUS residual 51; `SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md`.
3. **On-disk document versus a fresh clone.** Byte identity is asserted against the document as
   materialized on this disk, not a pinned checkout. A CRLF-materializing fresh clone changes the
   published LF/CRLF/SHA cross-check and makes block 11 fail **LOUDLY** — it does not pass
   silently. Source: STATUS residual 41. Cross-reference
   `WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`, which measures the same exposure
   repo-wide (365 identity-quoted artifacts, 186 that would change bytes on a fresh Windows
   checkout) and whose rules are not yet applied.
4. **The interpreter vocabulary.** The recognized-interpreter name set is a production-gate item
   to be pinned at production-gate time, not a static-tool defect. **Owner-ratified 2026-08-12 as
   decision C.**

Add a closing sentence to the subsection stating that all four are properties of the developer
host rather than of the security logic, that each requires an actor who already controls that
host, and that **no other section of this preregistration may describe any of them as a check, a
control, or a measurement.**

## Also carry — one open nit
The GLM-5.2 SEC102 second opinion (`SEC102_GLM_T1_2ND_OPINION_2026-08-12.md`) raised one nit that
was explicitly deferred to preregistration wording rather than code: a safe-set leaf that
**re-consumes a declared member's deploy path as a literal operand** is missed by the
orphan-only reachability gate. Add it as a short disclosed limitation in the same subsection (or
immediately adjacent), attributed to that verdict.

## Conservation — do not break the draft's own accounting
This draft carries strict conservation (§4.5.3 Lane-B 15/15, §8 combined 34/34, §9 SELF-QA
counts). Your addition is NEW material, not a re-disposition of an existing member. **Do not
alter any existing conservation count, disposition row, or quoted line.** If your addition
requires a count anywhere, add its own separate count and say plainly that it is disjoint from
the 34. Verify at the end that every existing count still reads exactly as before, and report
that you checked.

## Deliverable
The edited preregistration only. Print: the exact section you added, where you placed it and
why that placement is before the §10.2 acceptance language, the cross-references you added, and
a confirmation that all pre-existing conservation counts are unchanged.

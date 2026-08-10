# KICKOFF — re-review the design-defect pattern set against today's evidence

Fresh `gpt-5.6-sol` session, effort high. **Analysis only**, one output file, no commit,
no host contact, no network. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.

## Why

`DESIGN_DEFECT_PATTERNS_2026-08-10.md` is binding on everyone who designs or reviews an
executable block here. It was written mid-morning. Since then, ten review rounds across
three artifacts plus one tool have produced new evidence, and at least one defect class
recurred in places the pattern list did not predict. A pattern list that lags the evidence
quietly stops earning its keep.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — the current ten patterns.
2. Today's review reports, as evidence:
   - `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` (BLOCK 3)
   - `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_2026-08-10.md` (the round-3 venv-interpreter find)
   - `WPI_BLOCKS_DRAFT/RP6_CODEX_AUDIT_R6_2026-08-10.md` (REQUEST_CHANGES ×5)
   - `WPI_BLOCKS_DRAFT/RP6_CLAUDE_REAUDIT_R5_2026-08-10.md`,
     `RP6_CLAUDE_FINAL_AUDIT_2026-08-10.md`
   - `WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md`,
     `TRANSPORT_CLAUDE_FINAL_AUDIT_2026-08-10.md`
   - `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` (REQUEST_CHANGES ×9)
3. `WPI_PREREG_DRAFT_ROUND1/SEC101_RECONCILIATION_CODEX_2026-08-10.md` and
   `PATHSCOPE_LEAD_RERUN_2026-08-10.md` — supporting analysis.

## What to determine

1. **Are the ten patterns still distinct?** Name any pair that collapses into one in
   practice, and any that is stated so broadly it matches everything and therefore guides
   nothing.
2. **Does today's evidence justify new patterns?** Two candidates to evaluate on the
   evidence, plus any you find yourself:
   - **The declared-but-unbound instrument.** A tool is pinned, validated, projected and
     documented — and then never bound in the real caller, so the object that produces the
     accepting claim is unattested. Seen in RP7 (`python3` accepted, projected, required,
     omitted from the `wpi_main` binding loop) and adjacent to the earlier venv-interpreter
     defect. Distinguish it clearly from existing pattern 10 if it is genuinely different.
   - **The silent omission.** An analyzer or adjudicator that meets something it does not
     model and drops it without a marker, so absence of output reads as absence of risk.
     Seen in the prover (four CRITICAL sink classes pass silently), in RP7 row 19 (a
     malformed `dist-info` object disappears from the parity universe), and in the RP6
     capability ledger. Is this one pattern or two?
3. **Which patterns actually caught something today, and which caught nothing?** For each
   of the ten, cite the finding it predicted, or record that nothing matched it. A pattern
   with no hits after this much review is a candidate for removal or rewriting.
4. **Is the checking guidance actionable?** For each pattern, is there a concrete question
   a reviewer can ask of code? Where there is not, write one.

## Output

Write **only** `DEFECT_PATTERNS_REVIEW_CODEX_2026-08-10.md`: a verdict
(`KEEP-AS-IS` / `AMEND: <n> changes`), then per-pattern hit evidence, then the proposed new
or merged patterns written in the same voice and format as the existing file so the Lead
can paste them in, then anything you recommend deleting and why. Do not edit
`DESIGN_DEFECT_PATTERNS_2026-08-10.md` — the Lead applies changes.

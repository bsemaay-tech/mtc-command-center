# AUDIT KICKOFF — round 6 doc closure audit (Codex, narrow, FINAL auto-round)

Round 6 was DOCUMENTATION-ONLY, repairing the one survivor of audit 5: the section-4
shared declaration block was not copy-paste runnable. The code has been frozen and
CLOSED since audit 4; audit 5 re-confirmed the freeze and passed nit 2 + arithmetic.

This is the final automatic round. A same-class BLOCK here escalates to the owner as a
harness/tooling-limit judgment rather than triggering another repair round, so state
your verdict precisely and, if you BLOCK, say explicitly whether the residue is
(a) fixable by editing this document, or (b) an inherent limit of recording MSYS/Git-Bash
evidence under a literal-exact-command standard.

## Scope — read ONLY

- `audit5/AUDIT5_REPORT.md` (the single required finding), `ROUND6_KICKOFF_DOC_ONLY.md`
  (the binding scope), `round6/` (under audit), `round5/` (baseline).

## Audit questions

1. **Code freeze**: hash `round6/RP1-B3.sh`, `round6/RPD-VERIFY.sh`,
   `round6/DESIGN_NOTES.md`; they must equal
   `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`,
   `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`,
   `103ffe3811dfd7764bf1b4d9bc47489fbe3cb2d72bca7c5c32e461a82440f23b`. Any code delta =
   immediate BLOCK.
2. **The actual test — paste-and-run**: open a fresh shell, paste section 4.0 then 4.1
   from `round6/SELF_QA.md` VERBATIM, then paste at least four section-5 command blocks
   verbatim (include the item-1 cwd RED, an item-4 constant, an item-6 STUB_CASE arm,
   and the item-5 directory-source GREEN). Each must reproduce its recorded output with
   ZERO edits. Report actual output and rc. If any block needs an edit, name the exact
   line and what edit was required.
3. **Placeholder sweep**: confirm no angle-bracket placeholder remains inside any block
   a reader is instructed to run. Mentions inside prose that name the repaired round-5
   defects, and the declared output-normalization tokens in RECORDED OUTPUT transcripts,
   are acceptable — say so if that is what you find rather than flagging them.
4. Confirm nit 2 wording and the arithmetic (43 A / 119 B / 3 C) are still as audit 5
   passed them.

## Output

`audit6/AUDIT6_REPORT.md`, verdict first: **PASS / PASS-WITH-NITS / BLOCK**, then
findings with concrete failure scenarios, then the four answers. If BLOCK, include the
(a)/(b) classification above. English, ASCII only.

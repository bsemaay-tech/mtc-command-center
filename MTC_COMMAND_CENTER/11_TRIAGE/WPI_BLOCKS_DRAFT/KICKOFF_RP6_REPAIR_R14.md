# KICKOFF — RP6-P0 round 14: three census fail-closed-conservation residuals (Codex r13)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r14 (policy-read).
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF, zero CR.
Never `git checkout` a block file — use `git cat-file blob <sha>:<path>`. Scope fence: touch
ONLY `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report (RP6-P0.sh is unchanged/sound — the
census is a QA harness; do not touch the block unless a finding truly requires it, and say so).
Concurrent Max lane owns `composite_pathproof.py` + SEC102 files — do NOT touch those. Never git
checkout/reset/stash any tracked file.

## Input — commit `b2e8f098`. `RP6-P0.sh` UNCHANGED `5132bacd…`.

## The unifying principle (read first)
All three findings are the SAME defect one level deeper: the census's own EXTRACTORS
(function-definition inventory, tool-name inventory, alias check) are not fail-closed against
unmodeled/empty/partial/duplicate syntax. The fix is Pattern 1 + Pattern 13 applied to the
census itself: every declaration/definition must reach EXACTLY ONE disposition, and any
inventory shape the extractor does not model must produce an UNMODELED FAILURE (nonzero), never
a silent pass or a `count=0`. Disclosure is not a control.

## Binding scope: `RP6_CODEX_T0_AUDIT_R13_2026-08-11.md` — REQUEST_CHANGES ×3.

### F1 (HIGH) — function-definition recognition is not complete
A Bash function-definition form the `FUNCDEF` inventory does not recognize can define a name
that shadows a builtin emitter or one of the three prefix names, while assertion 15 never sees
it (`SELF_QA_RP6.md` FUNCDEF path).
**Repair:** make function-definition recognition complete for every Bash definition form the
fence admits, OR emit an unmodeled record for every unsupported form. Derive the raw definition
census once; require every definition to reach exactly one `FUNCDEF` disposition; bind the
prefix words themselves against the no-shadow invariant. Published D026 RED/GREEN for this class.

### F2 (HIGH) — tool-shadow coverage can become empty without failing closed (Pattern 13)
Tool names are derived by two exact line-shape `sed` patterns; an empty extraction is assigned
`n_sht=0` with no required count, no reconciliation to the resolved-handle inventory, no
unresolved disposition — so an inventory shape outside those two patterns silently removes the
tool-shadow universe.
**Repair:** conservation-bind the declared tool inventory to the extracted tool-name set AND to
the runtime handle set. Empty/partial/duplicate/unrecognized inventory syntax must produce an
unmodeled FAILURE, never `tool_shadow=0`. Published D026 RED/GREEN for inventory-shape drift +
tool shadow.

### F3 (HIGH) — alias absence checked lexically, not semantically
The alias check is lexical.
**Repair:** make the alias absence a semantic guarantee for the block's own execution — assert
(and fail closed on) both `shopt -s expand_aliases` NOT being enabled anywhere reachable AND no
`alias` builtin invocation defining a shadowing name, covering the forms an alias can be
introduced through; an unmodeled alias-introduction syntax is an unmodeled FAILURE. Published
D026 RED/GREEN.

## Deliverables
Repaired `SELF_QA_RP6.md` (census extractors made fail-closed-conservation) + `STATUS_RP6_P0.md`
(narrow every fail-closed claim to the true property) + `RP6_R14_REPORT_2026-08-11.md` (per-
finding disposition, D026 RED-before-GREEN for each of the three; the RED must show the CURRENT
census silently passing the unmodeled/empty shape and the repaired census failing nonzero). Do
not weaken any carried fence without a per-change discriminating-power proof. No commit — the
Lead commits and runs every published command verbatim.

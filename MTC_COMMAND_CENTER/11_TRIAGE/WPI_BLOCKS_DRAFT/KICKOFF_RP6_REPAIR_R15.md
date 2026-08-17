# KICKOFF — RP6-P0 round 15: definition-identity + inventory-conservation completeness (Codex r14)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r15 (policy-read).
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF, zero CR.
Never `git checkout` a block file — use `git cat-file blob <sha>:<path>`. Scope fence: touch
ONLY `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report (RP6-P0.sh is UNCHANGED/sound — census
is QA-layer). Concurrent lanes own SEC102/prereg — do NOT touch. Never git checkout/reset/stash
any tracked file.

## Input — commit `fb2c62b6`. `RP6-P0.sh` UNCHANGED `5132bacd…`.

## The two findings are Codex's exact repair specs — implement them verbatim.

### F1 (HIGH, Pattern 12/13) — the function-definition census is line-conserving, not definition-conserving
`SELF_QA_RP6.md:11453` keeps a backslash-newline as an escaped token; `:11537` accepts the next
tokenizer word as a function-keyword definition name without requiring a non-empty literal name.
The independent census `:11952` records only candidate physical line numbers, and assertion 16
`:12060` compares sorted-unique line-number sets, not stable definition identities. Two silent-
loss classes: (1) a function-keyword name separated from the keyword by a line continuation —
Bash removes the continuation before parsing, but the tokenizer can disposition the continuation
token instead of the name while raw census and tokenizer still report the same physical line;
(2) multiple definitions on one physical line collapse to one member on both sides, masking a
missing disposition.
**Required repair (Codex's spec):** assign each raw definition a STABLE IDENTITY containing at
least physical location, ordinal, normalized name, and form; compare those records ONE-FOR-ONE
WITHOUT `uniq`; REJECT empty, escaped, expanded, or otherwise unsupported definition-name tokens
as UNMODELED. Publish + execute D026 RED/GREEN for the continuation and same-line-multiplicity
classes (current census silently passes each; repaired census fails nonzero).

### F2 (HIGH, Pattern 12/13) — inventory conservation omits append-style and duplicate classes
The tokenizer recognizes both direct AND append-style (`x+=`) assignments at `:11549`, but the
inventory censuses `:11886`/`:11896` search only for a declared variable immediately followed by
DIRECT assignment. An append-style assignment to a declared half or the consumed inventory gets
no inventory disposition and no unmodeled record; the direct assignment stays count one, so the
chain passes over a different inventory than the block consumes. Second path `:11901`: composition
references are reduced with `sort -u` and checked by set equality, so a repeated declared half is
silently collapsed even though r14's contract says duplicate inventory shape fails closed; the
member-duplication count `:11905` does not restore multiplicity discarded from the consumed
composition.
**Required repair (Codex's spec):** give append-style assignments (and any other admitted
assignment form) an inventory disposition or an unmodeled record; preserve multiplicity in the
composition conservation (no `sort -u` collapse) so a repeated declared half fails closed. D026
RED/GREEN for the append and duplicate-composition classes.

## Deliverables
Repaired `SELF_QA_RP6.md` (census made definition-conserving + inventory-multiplicity-conserving)
+ `STATUS_RP6_P0.md` (narrow the conservation claim to the true property; re-state residuals) +
`RP6_R15_REPORT_2026-08-11.md` (per-finding D026 RED-before-GREEN; each RED shows the CURRENT
census silently passing and the repaired census failing nonzero). Do not weaken any carried fence
without a per-change discriminating-power proof. No commit — the Lead commits and runs every
published command verbatim.

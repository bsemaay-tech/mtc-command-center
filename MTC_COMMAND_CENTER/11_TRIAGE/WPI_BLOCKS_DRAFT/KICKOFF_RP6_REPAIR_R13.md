# KICKOFF — RP6-P0 round 13: two Pattern-12 census residuals + doc overclaim (Codex r12)

You are the IMPLEMENTER (GLM-5.2 via Z.AI, or Claude Max). Codex is auditor of record.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF only, zero
CR bytes. Never `git checkout` a block file — use `git cat-file blob <sha>:<path>`. If your
session cannot execute, write the repairs, mark QA `PENDING-LEAD-EXECUTION`, do not fabricate
transcripts. Scope fence: touch ONLY `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report, and
`RP6-P0.sh` ONLY if a finding requires a block change (the census lives in the QA layer, so it
likely does not). Concurrent lanes own RP7 + prereg + SEC102 — do NOT touch those; never git
checkout/reset/stash any tracked file.

## Input bytes

`RP6-P0.sh` UNCHANGED at commit `1a9bf2b2`, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. The round-12 census closed
cmdquote/expand/continuation; the `cmp` tokenizer-vs-grep equality is confirmed load-bearing.

## Binding scope

`RP6_CODEX_T0_AUDIT_R12_2026-08-11.md` — REQUEST_CHANGES ×3. All are QA-census completeness, not
block defects. Reproduce each by READING (do not construct filesystem-touching shell in your
own output — the auditor's filter and this repo's hygiene both require it; run the block's own
harnesses, do not author new emitter mutants beyond the two named classes needed for D026).

### 1 (HIGH) — Pattern 12 residual: alias/function-indirection
The tokenizer admits a BARE command word without binding its runtime resolution, so a name that
resolves via an alias or a shadowing function to an emitter is not caught (`SELF_QA_RP6.md:8556`).
**Repair options (pick the sound one and justify):**
- Assert the block enables no alias expansion: `RP6-P0.sh` does not `shopt -s expand_aliases`
  and defines no `alias` (non-interactive bash has aliases OFF by default) — so alias
  indirection is impossible by construction; the census asserts this statically and fails
  closed if either appears.
- For functions: the census must enumerate every function the block defines and fail closed if
  ANY function name equals, or resolves in command position to, a `p0_stop`/`p0_fail` emitter or
  an RO-tool handle — i.e. no function may shadow a wrapper/emitter/tool name; a bare command
  word is admissible only if it resolves to a declared block function that is NOT such a shadow,
  a declared RO tool, or a bash builtin/keyword.
Add a D026 arm for the alias form and the function-shadow form: the current census blind
(`unmodeled=0`) is RED, the repaired census nonzero is GREEN.

### 2 (HIGH) — Pattern 12 residual: command/builtin-prefix
`command`/`builtin`/`exec` prefixes consume command position; the census does not classify the
effective operand (`SELF_QA_RP6.md:8490`). This is purely syntactic and static-detectable.
**Repair:** the tokenizer strips a leading `command`/`builtin`/`exec` (and `command -p` etc.)
and classifies the FOLLOWING word as the effective command word under the same admissibility
policy. D026: `command p0_stop`-shaped operand is RED on the current census, nonzero on the
repaired census. (Refer to the mutant by the class name in prose; keep the literal in the
heredoc fixture only.)

### 3 (MEDIUM) — fail-closed doc overclaim
`STATUS_RP6_P0.md:35,166` and `RP6_R12_REPORT_2026-08-11.md:169,...` state the census is fully
fail-closed. Until findings 1–2 close, narrow the wording to exactly what the census
guarantees; after they close, update it to the true final property.

## Deliverables

Repaired `SELF_QA_RP6.md` (census) + `STATUS_RP6_P0.md` + `RP6_R13_REPORT_2026-08-11.md`
(per-finding disposition, D026 RED-before-GREEN for the alias, function-shadow, and
command/builtin-prefix classes; say per finding whether the fix is QA-only or touched the
block). Do not weaken any carried fence without a per-change discriminating-power proof. No
commit — the Lead commits and runs every published command verbatim.

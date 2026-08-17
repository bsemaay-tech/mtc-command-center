# KICKOFF — RP6-P0 round 11: four findings from the Codex r10 T0 audit

You are the IMPLEMENTER (GLM-5.2 via Z.AI, or Claude Max — whichever the Lead dispatches).
Codex is auditor of record and re-audits your bytes. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF only, zero CR bytes.
Never `git checkout` a block file — use `git cat-file blob <sha>:<path> > <path>`. If your
session cannot execute, write the repairs, mark QA `PENDING-LEAD-EXECUTION`, do not fabricate
transcripts.

Scope fence: touch ONLY `RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report,
and (if a finding requires) the prereg draft with every edit listed. Other files in this
directory carry uncommitted work from concurrent lanes (transport r5) — do NOT touch them and
never run git checkout/reset/stash on any tracked file.

## Input bytes

`RP6-P0.sh` at commit `71a62cc8`, SHA-256
`a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`, 107252 B.

## Binding scope

`RP6_CODEX_T0_AUDIT_R10_2026-08-11.md` — REQUEST_CHANGES, four findings. Round-9 F1 is
CONFIRMED CLOSED (the three R10 pipelines run verbatim); do not touch what works.

### 1 (HIGH) — grammar coverage is not fail-closed and the normalizer is lossy
The R10_GRAMMAR normalizer groups sites by prefix/reason/field-order and stores independent
per-field value sets, destroying field correlation: 12 forms admit 65 synthetic field-value
combinations beyond the real site tuples, so a correlation-preserving relabel
(`RP6-P0.sh:1266` `account=gatea`→`account=mtc-bridge`) stays GREEN. The "complete/exhaustive
grammar" claim only holds for today's modeled spellings; it does not fail closed on an
unmodeled future syntax.
**Repair:** census every executable wrapper call + direct emitter with a broader independent
mechanism; emit a coverage error for every syntax the normalizer cannot parse (fail closed).
Preserve each site's correlated tuple (or declare each exact tuple). Add + execute D026
mutants for an alternate valid quoting form AND the correlation-preserving relabel — both
must make the fence return nonzero.

### 2 (HIGH) — F3 maps an unrecognized producer token to host-state FAIL
`RP6-P0.sh:1618-1622` sends every remaining printable single line through `*) P0_FKIND=other`,
including arbitrary producer text, then emits `P0_FAIL reason=interpreter_target_kind_unexpected`
at rc 1. Round-9 required a RECOGNIZED complete kind before assigning `P0_FKIND`. A successful
producer status + unrecognized result grammar is inability-to-evaluate (STOP rc 3), not a host
deviation (Patterns 1/5/6).
**Repair:** define the complete accepted GNU `stat -c %F` token grammar for the pinned
producer; assign `P0_FKIND=other` only for explicitly recognized complete non-regular kinds;
STOP with a declared reason on any unknown printable token. D026 RED against the current
catch-all (rc 1) → GREEN with the STOP (rc 3), keeping the directory rc-1 and regular rc-0
regressions.

### 3 (HIGH) — the published R9 RED-twin recipe masks its own failing status
`SELF_QA_RP6.md:6386-6395`: the recipe runs the failing harness, prints `R9_RED_RC=$?`, then
`rm -f "$mutant"` LAST, so the recipe process returns rc 0 while the harness failed rc 1 —
contradicting the report's "every command's status agrees with its verdict." Same round-9
F1 / Pattern-10 defect at the recipe level. Also: the ten guard-falsification fences are
behaviorally sound (Codex independently confirmed all ten rc 1) but `SELF_QA_RP6.md:6546-6578`
publishes only prose + transcript, not the executable falsification command it claims is "in
the harness above" — under D026 that stays supplemental.
**Repair:** preserve the RED harness status across cleanup (EXIT trap for cleanup, or capture
rc and exit with it) so the whole recipe records real rc 1. Publish an executable self-checking
guard-falsification fence, not only a transcript, and record its real output/status.

### 4 (MEDIUM) — F4 evidence prose outruns the executed predicate
The byte repair at `RP6-P0.sh:675-676` is truthful and the harness reaches it at rc 3. But the
surrounding claims are broader than the executed predicate.
**Repair:** narrow the prose to exactly what the F4 harness executes, or extend the harness to
cover the broader claim — say which, per claim.

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` + `RP6_R11_REPORT_2026-08-11.md` (per-finding
disposition, each byte change with D026 RED-before-GREEN executed evidence). Do not weaken any
carried fence without a per-change discriminating-power proof (old + new assertion executed on
the same deviant output, both quoted). No commit — the Lead commits and runs every published
command verbatim.

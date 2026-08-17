The harness declined `bash -n`, so syntax is assessed by inspection (the block parses cleanly on reading: balanced quotes/case-esac/if-fi, valid `$(...)`, proper `local rc=$?` ordering). Proceeding to the report.

---

# AUDIT REPORT — `RP6-P0.sh` (partial RP6-P0 draft block)

**Scope.** Read-only audit of `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh` against `DESIGN_DEFECT_PATTERNS_2026-08-10.md`, with `RP1-B3.sh` as the convention reference and `KICKOFF_RP6_P0.md` as the spec. No file was touched. `bash -n` was attempted but declined by the harness; syntax was assessed by inspection.

## VERDICT: NEEDS-REPAIR-FIRST

The block is well-architected and its **Pattern 1 discipline is sound** — no access, tool, bus, namespace, or parse failure I could trace reaches a FAIL verdict; the only FAIL arms are object-presence/kind/canonical observations on preregistered paths, which is exactly the audit-1 F5 ruling. That is the thing that would make a preflight block dangerous, and it is correct. All six kickoff arms are present and structurally complete.

But it is **not sound enough to write QA against as it stands**, for two reasons that are bounded and mechanical, not architectural: (1) the terminal evidence claim contains a materially false statement of the child-execution surface, and (2) the rc polarity of the two identity arms was chosen without the authoritative prereg table visible and may be inverted. Freezing either into `SELF_QA_RP6.md` would codify a wrong claim or a wrong expected rc. The repair scope is small; the next step is (b), then QA.

---

## Q1 — Pattern sweep (NO / YES / PARTIAL)

**Pattern 1 — "STOP is not a result": PARTIAL (verdict-correct in code, polarity unverified for two arms).**
Every `p0_fail` (lines 756, 758, 760, 768, 783, 785, 787, 789) is an object-presence/kind/canonical observation on a *preregistered absolute path* (venv root or interpreter). The access/exec/parse failure paths all STOP: EACCES on `stat` → `p0_stop "path_probe_denied"` (743); tool-missing → `p0_stop "missing_tool"` (361); `[ -x ]` denial → `p0_stop "interpreter_not_executable"` (797); exec rc≠0 → `p0_stop "interpreter_exec_*"` (807-809); manager rc≠0 → `p0_stop "system_manager_unreachable"` (641); every unparsable record → STOP. So the *code* keeps could-not-evaluate at rc 3. The PARTIAL is below — the rc of `identity_unexpected` (558) and `capability_wider_than_ledger` (562) cannot be reconciled with the prereg 8.1 table from the files given; if the table specifies rc 1 for either row, that arm instantiates Pattern 1.

**Pattern 2 — "Whose kernel answered?": NO.** Identity is numeric and explicitly scoped to this login; namespaces are `record_only binding=not_established` (602); manager identity is `not_established` (658); the block never compares its namespaces to PID 1's (it refuses to read `/proc/1/ns/*`, 577). The A2-F2 / F2 overclaim (`bound=initial`) is deliberately not made.

**Pattern 3 — "The leaf is not the path": PARTIAL.** The venv root is verified literal-canonical before its contents (751-772), which is the correct container-before-contents order. The gap: `$P0_VENV_ROOT/bin/python` and the `bin` component are *not* canonicalized; `stat` follows intermediate symlinks. See finding 3.

**Pattern 4 — "The privileged child brought its own environment": PARTIAL.** The two sensitive children are handled correctly — `env -i LC_ALL=C` clears the environment for the systemctl query (633) and the interpreter runs `-I` under `env -i` (803). But the claim that *all* children are cleared-env is false (the stat/readlink/id children inherit the caller's environment). See finding 1.

**Pattern 5 — "grep is not a parser": NO.** No `grep`/substring parser of structured data. The only literal matchers (`p0_count_substr`, `p0_classify_stat_shape`) operate on single-line errno diagnostics against exact C-locale shapes, which is the A2-F6-correct use. The `Version=` and `P0PY ` prefixes are prefix-shape matches on single-line producer output, not grammar parsing of nested data.

**Pattern 6 — "Read the status before the stdout": NO.** Every producer is captured as `out="$(... 2>&1)" || rc=$?` with rc adjudicated before any byte of `out` is read (e.g. 358-362, 393-397, 469-474, 523-527, 584-588, 633-642, 698-746, 803-811). The streams-merged-on-purpose discipline (24-29) is applied consistently.

**Pattern 7 — "Nonzero read is not end of file": NO.** The block performs no `while read` over a record stream. (RP1-B3's mount-table reader is the locus of this pattern; P0 has no equivalent reader.)

**Pattern 8 — "The name is not the identity": NO.** `id` is asked only for `-u`/`-g`/`-G` (539-547); `stat` is never asked for `%U`/`%G`; every identity input is numeric and validated as digits (246-274); forbidden-gid matching is whole-word on the numeric list (560-563). The block's own header states the rule (31-35) and the code honours it.

**Pattern 9 — "The sentence outruns the probe": YES (two instances).** (a) Lines 59-62 and 861 claim "exactly two child processes… both with a CLEARED environment" / `children=2_readonly_cleared_env` — false. See finding 1. (b) Line 859 `evidence_stdout_bound_to_create_once_leaf` — "create_once" is inherited from the bootstrap, not established by this block. See finding 4.

**Pattern 10 — "Evidence that cannot fail": NO (in the block).** The block's claims are all observable outcomes with reason tokens; no self-produced count or recipe is offered as closure. (The *missing* `SELF_QA_RP6.md` is the Pattern 10 exposure for the *package* — which is the question Q4 answers — but the block itself does not commit a Pattern 10 error.)

---

## Q2 — Precondition integrity (claims its probes do not establish)

**Claim that outruns the probe — line 861:** `scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP children=2_readonly_cleared_env`

The `children=2_readonly_cleared_env` token is false. The block executes far more than two child processes — every `$P0_STAT`, `$P0_READLINK`, `$P0_ID` invocation is a fork/exec of a PATH-resolved binary — and only the two `env -i` launches (systemctl at 633, interpreter at 803) run with a cleared environment. The stat/readlink/id children run with the **inherited** environment (only `LC_ALL=C` is exported, line 93). Missing: an honest accounting of the child-execution surface — the N inherited-environment, PATH-resolved coreutils invocations plus the 2 cleared-env launches — or deletion of the token.

**Claim that outruns the probe — line 859:** `evidence_stdout_bound_to_create_once_leaf`. The probe at 466-504 proves fd 1 (stdout) and `$EV_LOG` are the *same object right now* (dev:inode identity). It does not, and cannot, prove the leaf was created *once* — create-onceness is the bootstrap's invariant, asserted here only via the RUNID/EV_LOG-set prerequisite checks (226-229). Missing: the word "now"/"currently", or relocation of "create-once" to the bootstrap's claim, not P0's.

No other claim outruns its probe. The `does_not_establish` line (860) is scrupulously honest (tool provenance, manager identity, namespace binding, version/parity, protected dirs, Group C).

---

## Q3 — Convention conformance vs `RP1-B3.sh`

| Convention | RP6-P0 | Verdict |
|---|---|---|
| `set -Eeuo pipefail` | line 92 | **Conforms.** |
| `LC_ALL=C` exported + pinned on every producer | line 93 + per-call `LC_ALL=C` on stat/readlink/id/env (393, 469, 476, 483, 523, 584, 633, 698, 703, 761, 803) | **Conforms.** Note: `command -v` (358) is not given `LC_ALL=C`, but it is a builtin whose output is a PATH entry, not locale-sensitive; acceptable. |
| ERR trap → reasoned STOP | lines 119-125 | **Conforms.** Identical shape to RP1-B3 (103-109). |
| No temp files | no `mktemp`/`/tmp` writes anywhere; stderr captured into variables | **Conforms.** |
| Numeric-only identity | lines 31-35, 246-274, 537-567 | **Conforms.** |
| Status adjudicated before stdout | every producer (Q1 Pattern 6) | **Conforms.** |

**Deviations from the accepted block's conventions:**

1. **`children=` token has no analogue in RP1-B3 and is false.** RP1-B3's mutation-surface note (35-40) makes no child-count claim; RP6-P0 invents one and gets it wrong. This is the one substantive convention deviation — an evidence token the accepted pattern does not emit and that this block emits incorrectly.
2. **No `:`/`fail-closed` guard behind the rc-3 input pre-checks.** RP1-B3 retains the accepted `: "${VAR:?}"` line *behind* its rc-3 pre-checks so the guard still fails closed if a pre-check is edited out (RP1-B3 lines 175, 184, 193). RP6-P0's `p0_require_uint` (246-255) and the `[ -n ... ] || p0_stop` checks have **no such backstop**: if a future edit removes the `[ -n ]` pre-check, a missing `P0_EXPECT_UID` reaches `[ "$val" -ge "$min" ]` under `set -u`, which aborts with rc 1 and *no P0 reason* — the exact raw-tool-status escape the rc contract forbids. The ERR trap would catch it as `unadjudicated_command_status`, but the accepted block's defence-in-depth (`:?` behind the pre-check) is absent here.
3. **`want_mode` leading-zero strip omitted.** Cosmetic only — P0 only *records* modes, never compares them, so RP1-B3's `${2#0}` (line 275) is not needed. Not a defect; noted for completeness.

---

## Q4 — Completion cost

**(b) Repair specific defects first.** The architecture is sound and Pattern 1 (the load-bearing pattern) is correctly implemented in code, so this is not a rewrite — it is a bounded repair list. Writing `SELF_QA_RP6.md` against the current text would either repeat the false `children=` claim or contradict the code, and would have to guess the expected rc for the two identity arms. Repair scope:

1. **Correct the child-execution claim.** Lines 59-62 and the `children=2_readonly_cleared_env` token at 861. State the surface honestly: the 2 cleared-env launches (systemctl, interpreter) plus the inherited-environment, PATH-resolved coreutils invocations (stat/readlink/id), or drop the token.
2. **Reconcile identity rc polarity with the prereg 8.1 table.** Lines 558 (`identity_unexpected`) and 562 (`capability_wider_than_ledger`) currently STOP. Verify against the authoritative table; if either row specifies rc 1, change the arm and keep its reason token.
3. **Add the `:?` backstop** behind the rc-3 input pre-checks for `P0_EXPECT_UID`, `P0_FORBIDDEN_GIDS`, `P0_VENV_ROOT` (mirror RP1-B3 lines 175/184/193) so an edited-out pre-check still fails closed with rc 3, not a raw rc 1.
4. **(Lower priority) Decide the interpreter intermediate-path residual.** Either canonicalize `$P0_VENV_ROOT/bin/python`'s components (Pattern 3 closure) or disclose the intermediate-symlink residual in the `does_not_establish` line.

After 1-3, the block is sound enough to drive. Item 4 can ship as an explicit residual.

---

## Findings (most severe first)

**F1 — [MEDIUM] False child-execution claim in the evidence contract (Pattern 9; cross-ref Pattern 4).** `RP6-P0.sh:59-62` and `RP6-P0.sh:861`. The block claims "Exactly two child processes are executed, both… with a CLEARED environment" and emits `children=2_readonly_cleared_env` to the evidence leaf. It actually executes ~20+ child processes (`stat`, `readlink`, `id` invocations across the metadata, evidence-binding, identity, namespace, and interpreter arms), of which only the two `env -i` launches are cleared-env. *Scenario:* an auditor trusts `children=2_readonly_cleared_env`, treats the trusted computing base as two closed processes, and does not audit the inherited-environment coreutils children; on a host where `PATH` resolves `stat`/`id` to an attacker-controlled binary (or `LD_PRELOAD` is set in the inherited env), those children return forged metadata/identity that P0 records as evidence, undetected because the claim said the surface was closed. The PATH-hijack risk is separately disclosed (`does_not_establish=tool_provenance_or_distribution_identity`), but the *specific numeric claim* that only 2 cleared-env children run is false and misleading.

**F2 — [MEDIUM] Identity rc polarity unverifiable against the authoritative table (Pattern 1 risk).** `RP6-P0.sh:558`, `RP6-P0.sh:562`. The block returns rc 3 (STOP) for a uid that does not equal `P0_EXPECT_UID` and for membership in a forbidden gid. The kickoff (lines 28-29) makes the prereg 8.1 expectation table "authoritative for reason strings" and the rows govern; that table is not among the five files supplied to this audit, so the polarity cannot be confirmed. The block's comment (516-520) gives a reasoned defence for STOP, but if the table specifies rc 1 for row 1 (`identity_unexpected` — the wrong login *is* deviant host state, because the run is no longer the preregistered route), the arm misclassifies deviant state as could-not-evaluate. *Scenario:* the prereg row-1 expected divergence is `identity_unexpected` at rc 1, but P0 returns rc 3; the RO stage treats a wrong-identity run as "could not evaluate" and re-dispatches, instead of recording it as the deviant state it is. Must be reconciled before the arm is driven.

**F3 — [LOW] Intermediate path components below the venv root are not canonicalized (Pattern 3).** `RP6-P0.sh:774-803`. `$P0_VENV_ROOT` is verified literal-canonical (761-768) but `$P0_VENV_ROOT/bin/python` and the `bin` component are not; `stat` without `-L` follows intermediate symlinks. *Scenario:* `$P0_VENV_ROOT/bin` is a symlink to a decoy directory whose `python` is executable and prints `P0PY 3.12`; P0 records the interpreter as the preregistered path's object when it is a decoy reached through an intermediate symlink. Mitigating: the interpreter is then actually executed (binding to the real object) and provenance is explicitly not established, so this is a residual gap, not a false PASS. (RP1-B3 has the same shape for leaves under CONF_DIR but defers them to RPD-VERIFY; P0 adjudicates this leaf itself, so the gap is its own.)

**F4 — [LOW / nit] No `:?` fail-closed backstop behind the rc-3 input pre-checks.** `RP6-P0.sh:246-274`. RP1-B3 retains `: "${VAR:?}"` behind each pre-check so an edited-out pre-check still aborts at rc 1-with-reason rather than a raw status; RP6-P0 omits this. *Scenario:* a future edit removes the `[ -n "${P0_EXPECT_UID:-}" ]` check; a missing input then hits `[ "$val" -ge "$min" ]` under `set -u`, aborting with rc 1 and no P0 reason. The ERR trap catches it as `unadjudicated_command_status` (rc 3), so the contract still holds — but the accepted block's defence-in-depth is missing.

**F5 — [NIT] "create_once" overclaim in the evidence-binding claim.** `RP6-P0.sh:859`. The probe proves stdout and `$EV_LOG` are the same object *now*; it does not prove create-onceness (a bootstrap invariant). Partially disclosed by `evidence_leaf=allocated_by_RP0-BOOTSTRAP` (861). No false admission; word "now" missing.

**F6 — [NIT] fd 8 not closed on the STOP paths of `p0_assert_evidence_leaf_bound`.** `RP6-P0.sh:468-484`. `exec 8>&1` opens fd 8; a STOP at 473/480/487 jumps past `exec 8>&-` (484). The comment (53-54) says the block "closes it again." Harmless — the process exits on STOP — but the claim holds only on the happy path.

---

### Notes on audit scope
- The prereg 8.1 expectation table and the feasibility ledger were referenced by the kickoff as binding inputs to the implementer but were **not among the five files supplied**; findings that depend on their contents (F2 primarily; the completeness of the 11-tool list) are stated as "must verify," not as confirmed defects.
- `bash -n` was attempted and declined by the harness; the clean-parse assessment is by inspection.

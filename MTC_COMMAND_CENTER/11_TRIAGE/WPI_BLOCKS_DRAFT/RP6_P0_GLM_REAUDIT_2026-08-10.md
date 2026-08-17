I have completed the read-only verification. Here is the audit report.

---

# GLM RE-AUDIT — `RP6-P0.sh` repaired block (F1/F3/F4)

## VERDICT: PASS

No findings against the repair. F1, F3, and F4 are all closed; no regression introduced; the block conforms to the round-1.4 P0 rows on the checked axes. Two pre-existing/deferred NITs (F5, F6) and one out-of-scope observation noted below — none count against this bounded repair.

---

## V-rows

| # | Result | Evidence |
|---|--------|----------|
| **V1** (F1 closed) | **PASS** | `git diff HEAD` shows the false `children=2_readonly_cleared_env` token and the "exactly two… CLEARED environment" comment both removed (RP6-P0.sh:59-67, :874). New claim line emits `child_env=mixed coreutils_launch=recorded_absolute_after_PATH_resolution inherited_env=stat_readlink_id cleared_env=systemctl_and_interpreter_only cwd=caller_inherited tmpdir=caller_inherited_or_unset`. I traced the actual child surface: the only `env -i` (cleared) launches are `systemctl` (:646) and the interpreter (:816); every `$P0_STAT`/`$P0_READLINK`/`$P0_ID` call (metadata ×11, evidence-binding ×3, identity ×3, namespaces ×3, venv-root ×3, interpreter-kind ×1-2) inherits the caller env with only `LC_ALL=C` exported. Disclosure matches the code exactly. |
| **V2** (F3 closed) | **PASS** | Residual disclosed, not silently canonicalized. `does_not_establish` (:873) now contains `interpreter_intermediate_component_or_symlink_target_binding`; new comment at :341-345 explains `P0_PY="$P0_VENV_ROOT/bin/python"` derives the literal leaf name only and refuses to learn/accept a runtime target "contrary to prereg row 18." `establishes` tightened from `venv_interpreter_object_and_executability` → `venv_interpreter_leaf_kind_and_executability`. Consistent with round-1.4 row 18 ("any accepted symlink… must have its resolved target preregistered and bound, not merely followed") — the block does not falsely satisfy it; it explicitly declines to claim it. |
| **V3** (F4 closed) | **PASS** | Three `:?` backstops added directly behind each rc-3 pre-check: `P0_EXPECT_UID` (:266 behind :265), `P0_FORBIDDEN_GIDS` (:274 behind :272-273), `P0_VENV_ROOT` (:289 behind :287-288). They are behaviorally falsified, not merely present — the SELF_QA F4 harness deletes each pre-check in turn and shows pre-fix falling through to an unnamed `unbound variable` (rc 1, no reason) vs. repaired stopping at the named `:?` message (rc 1, named reason). The transcript is internally consistent and the mechanism is unambiguous from code+diff. |
| **V4** (no regression) | **PASS** | Full `git diff HEAD` is +20/-7 and semantically confined to F1/F3/F4: (a) mutation-surface comment rewrite, (b) three `:?` lines, (c) literal-leaf comment, (d) three terminal `printf` lines. **Untouched:** ERR trap, `p0_stop`/`p0_fail`, rc 0/1/3 contract, numeric-identity rule (`id -u/-g/-G` only, whole-word gid match :573-577), read-only scope (no `mktemp`/writes; the `:?` additions emit to stderr only), tool inventory, identity/namespace/manager/interpreter arms. The `:?` backstops are inert on every currently-reachable path (the preceding pre-check fires first) — pure defence-in-depth, zero happy-path change. |
| **V5** (QA re-runnable) | **PASS\*** | *Executed:* `sha256sum` = `6c5b8945…766f7` — **matches the claimed hash exactly**; `git diff HEAD` confirms change scope. *Verified by literal source cross-check:* the three `P0_claim` printf sources (RP6-P0.sh:872-874) match the SELF_QA "REPAIRED" transcript (lines 109-111/121-123) byte-for-byte, including the removed false token and added disclosures. *Execution-limited:* the audit-mode harness's static analyzer declined every RED/GREEN bash harness (pipes, heredocs, inline `bash -c`, and `bash -n` all gated), so the behavioral F4 mutation was verified by code+diff reasoning rather than re-execution. The deterministic + identity + scope evidence is conclusive; the behavioral path is unambiguous. |
| **V6** (spec/catalogue conformance) | **PASS** | **Numeric identity** (Pattern 8): numeric-only, names never captured — conforms (the Lead's Pattern-8 defect was in the *draft*, repaired separately; the block was always compliant). **Capability ledger:** forbidden-gid intersection → `capability_wider_than_ledger` STOP rc 3 (:575), matching row-3's "more privilege… is a STOP." **STOP grammar (Pattern 1):** only FAIL arms are object-presence/kind/canonical on preregistered paths (audit-1 F5 ruling); all could-not-evaluate → STOP rc 3. **Pattern 4** (spot-check): two sensitive children run `env -i`; the repair makes the block's *partial* Pattern-4 status honest (`does_not_establish=…round1_4_probe_execution_environment_binding`) rather than false. Reason tokens `identity_unexpected`/`capability_wider_than_ledger`/`system_manager_unreachable` match round-1.4 rows 2/3/9. |

\* V5 star = executed + inspected, with the behavioral re-run harness-gated; see note.

---

## Findings against the repair
None.

## Non-blocking observations (out of repair scope, not counted)

1. **Deferred NITs F5/F6 remain open (intentional).** `evidence_stdout_bound_to_create_once_leaf` (:872) still overclaims create-onceness (a bootstrap invariant; the probe proves same-object *now*, F5), and fd 8 is not closed on the STOP paths of `p0_assert_evidence_leaf_bound` (F6). Both were explicitly outside the F1/F3/F4 scope set by the Lead adjudication; both are harmless (F5 partially mitigated by `evidence_leaf=allocated_by_RP0-BOOTSTRAP`; F6 harmless because STOP exits the process). Surface for a future pass — do not treat as regressions.

2. **Pre-existing input-sourcing divergence from round-1.4 rows 1-3 (not introduced here).** Spec rows 1-3 describe `getent passwd gatea`/`getent passwd mtc-bridge` resolution defining the named login contract; the block instead compares the live `id -u`/`-G` against preregistered numeric inputs (`P0_EXPECT_UID`, `P0_FORBIDDEN_GIDS`) and never calls `getent`. This predates the repair (the identity section is untouched in the diff), is *stronger* on the Pattern-8 axis (the Lead adjudication praised it), and the rc polarity (F2) was adjudicated correct. Flagged only so the Lead has it in view; no block change implied by this audit.

3. **`:?` backstop exits rc 1, not rc 3** — by design, mirroring the accepted RP1-B3 `:?` convention (rc-1-with-named-reason as defence-in-depth; the rc-3 pre-check is the primary mechanism). Conformant, not a contract violation.

---
*Read-only audit. No file was modified, staged, committed, or renamed; no host was contacted; no destructive command run. `RP6-P0.sh` remains REPAIRED-PENDING-AUDIT and carries no host-contact authority.*

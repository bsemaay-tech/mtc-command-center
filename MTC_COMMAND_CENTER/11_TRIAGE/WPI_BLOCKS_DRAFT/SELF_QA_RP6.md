# SELF-QA — RP6-P0 bounded repair (F1, F3, F4)

Run by the Codex implementer on 2026-08-10 in a fresh Git Bash 5.2.37
`--noprofile --norc` process. `git show HEAD:<path>` is the committed pre-fix
`RP6-P0.sh`; the path in the working tree is the repaired file. Every fence below is
literal paste-and-run Bash with its complete working-directory setup. No host was
contacted, no ssh/network command was run, and no temp file was created.

## Repair decisions

- **F1:** use the kickoff's permitted honest-disclosure branch. Full round-1.4
  execution-environment binding needs new preregistered trusted cwd, run-owned TMPDIR,
  and helper target-chain inputs. Adding those would expand this bounded block's input
  contract. The repair therefore removes the false child count, states the mixed child
  environment exactly, and makes the stronger binding an explicit non-establishment.
- **F3:** disclose the residual. Draft row 18 says an accepted interpreter symlink's
  resolved target chain must be preregistered and bound. P0 has no such preregistered
  target. Canonicalizing and accepting a runtime-learned target would violate that rule;
  rejecting all interpreter symlinks would reject the normal venv shape. The repaired
  evidence therefore says intermediate-component and symlink-target binding are not
  established. This closes the claim defect, not the disclosed path-binding residual.
- **F4:** retain each rc-3 input pre-check and put the accepted `:?` backstop directly
  behind it. The behavioral falsification deletes each pre-check in turn. The pre-fix
  bytes fall through to an unrelated nounset error; repaired bytes stop immediately with
  the named input backstop.

## F1 and F3 — exact RED/GREEN command

This executes the terminal `P0_claim` producers from each version. F1 rejects the false
fixed count and requires every honest surface token. F3 requires the residual in the
emitted `does_not_establish` evidence, not merely in a comment.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
target='MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh'

emit_claims() {
    sed -n "/^printf 'P0_claim /p" | bash --noprofile --norc
}

check_f1() {
    local claims token
    claims="$(emit_claims)"
    case "$claims" in
        *children=2_readonly_cleared_env*)
            printf 'F1_RED false_child_token_present\n%s\n' "$claims"
            return 1 ;;
    esac
    for token in \
        'child_env=mixed' \
        'coreutils_launch=recorded_absolute_after_PATH_resolution' \
        'inherited_env=stat_readlink_id' \
        'cleared_env=systemctl_and_interpreter_only' \
        'cwd=caller_inherited' \
        'tmpdir=caller_inherited_or_unset' \
        'round1_4_probe_execution_environment_binding'
    do
        case "$claims" in
            *"$token"*) : ;;
            *)
                printf 'F1_RED honest_surface_token_missing token=%s\n%s\n' "$token" "$claims"
                return 1 ;;
        esac
    done
    printf 'F1_GREEN false_count_removed_mixed_child_surface_disclosed\n%s\n' "$claims"
}

check_f3() {
    local claims
    claims="$(emit_claims)"
    case "$claims" in
        *interpreter_intermediate_component_or_symlink_target_binding*)
            printf 'F3_GREEN residual_disclosed_no_runtime_target_acceptance\n%s\n' "$claims" ;;
        *)
            printf 'F3_RED intermediate_component_and_symlink_target_residual_undisclosed\n%s\n' "$claims"
            return 1 ;;
    esac
}

set +e
pre_f1="$(git show "HEAD:$target" | check_f1 2>&1)"; pre_f1_rc=$?
post_f1="$(check_f1 < "$target" 2>&1)"; post_f1_rc=$?
pre_f3="$(git show "HEAD:$target" | check_f3 2>&1)"; pre_f3_rc=$?
post_f3="$(check_f3 < "$target" 2>&1)"; post_f3_rc=$?
set -e

printf '%s\n' '=== F1 PRE-FIX ===' "$pre_f1" "CHECK_RC=$pre_f1_rc"
printf '%s\n' '=== F1 REPAIRED ===' "$post_f1" "CHECK_RC=$post_f1_rc"
printf '%s\n' '=== F3 PRE-FIX ===' "$pre_f3" "CHECK_RC=$pre_f3_rc"
printf '%s\n' '=== F3 REPAIRED ===' "$post_f3" "CHECK_RC=$post_f3_rc"

[ "$pre_f1_rc" -eq 1 ] && [ "$post_f1_rc" -eq 0 ]
[ "$pre_f3_rc" -eq 1 ] && [ "$post_f3_rc" -eq 0 ]
printf 'F1_F3_QA_SUMMARY expected_red_green_vector=1/0,1/0 result=PASS\n'
```

Real captured output:

```text
=== F1 PRE-FIX ===
F1_RED false_child_token_present
P0_claim establishes=executing_numeric_identity_of_this_login,forbidden_gid_non_membership,resolution_and_executability_of_the_11_listed_RO_tools,evidence_stdout_bound_to_create_once_leaf,system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces,venv_interpreter_object_and_executability,self_namespace_identities_recorded
P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces,interpreter_version_or_package_parity,anything_under_the_protected_metadata_directories,anything_about_group_C
P0_claim scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP children=2_readonly_cleared_env
CHECK_RC=1
=== F1 REPAIRED ===
F1_GREEN false_count_removed_mixed_child_surface_disclosed
P0_claim establishes=executing_numeric_identity_of_this_login,forbidden_gid_non_membership,resolution_and_executability_of_the_11_listed_RO_tools,evidence_stdout_bound_to_create_once_leaf,system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces,venv_interpreter_leaf_kind_and_executability,self_namespace_identities_recorded
P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,round1_4_probe_execution_environment_binding,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces,interpreter_intermediate_component_or_symlink_target_binding,interpreter_version_or_package_parity,anything_under_the_protected_metadata_directories,anything_about_group_C
P0_claim scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP child_env=mixed coreutils_launch=recorded_absolute_after_PATH_resolution inherited_env=stat_readlink_id cleared_env=systemctl_and_interpreter_only cwd=caller_inherited tmpdir=caller_inherited_or_unset
CHECK_RC=0
=== F3 PRE-FIX ===
F3_RED intermediate_component_and_symlink_target_residual_undisclosed
P0_claim establishes=executing_numeric_identity_of_this_login,forbidden_gid_non_membership,resolution_and_executability_of_the_11_listed_RO_tools,evidence_stdout_bound_to_create_once_leaf,system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces,venv_interpreter_object_and_executability,self_namespace_identities_recorded
P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces,interpreter_version_or_package_parity,anything_under_the_protected_metadata_directories,anything_about_group_C
P0_claim scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP children=2_readonly_cleared_env
CHECK_RC=1
=== F3 REPAIRED ===
F3_GREEN residual_disclosed_no_runtime_target_acceptance
P0_claim establishes=executing_numeric_identity_of_this_login,forbidden_gid_non_membership,resolution_and_executability_of_the_11_listed_RO_tools,evidence_stdout_bound_to_create_once_leaf,system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces,venv_interpreter_leaf_kind_and_executability,self_namespace_identities_recorded
P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,round1_4_probe_execution_environment_binding,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces,interpreter_intermediate_component_or_symlink_target_binding,interpreter_version_or_package_parity,anything_under_the_protected_metadata_directories,anything_about_group_C
P0_claim scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP child_env=mixed coreutils_launch=recorded_absolute_after_PATH_resolution inherited_env=stat_readlink_id cleared_env=systemctl_and_interpreter_only cwd=caller_inherited tmpdir=caller_inherited_or_unset
CHECK_RC=0
F1_F3_QA_SUMMARY expected_red_green_vector=1/0,1/0 result=PASS
```

## F4 — exact three-input mutation command

The deliberate mutation removes each existing rc-3 pre-check from both versions. It
does not alter the proposed backstop. That makes the backstop observable: old bytes
reach a later nounset failure, while repaired bytes stop at the named `:?` guard.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
target='MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh'
cand='2ce41e34bceb599d80af24c5c33d835820ec321b'

exercise_f4_one() {
    local input="$1" expected raw probe_rc=0
    local -a mutate extra_env
    case "$input" in
        P0_EXPECT_UID)
            mutate=(sed '/^p0_require_uint P0_EXPECT_UID /d')
            extra_env=(
                P0_FORBIDDEN_GIDS=0
                P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand"
            )
            expected='P0_EXPECT_UID: preregistered numeric uid of the route login is required'
            ;;
        P0_FORBIDDEN_GIDS)
            mutate=(sed '/^\[ -n "${P0_FORBIDDEN_GIDS:-}" \] \\/,+1d')
            extra_env=(
                P0_EXPECT_UID=1000
                P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand"
            )
            expected='P0_FORBIDDEN_GIDS: preregistered numeric forbidden-gid list is required'
            ;;
        P0_VENV_ROOT)
            mutate=(sed '/^\[ -n "${P0_VENV_ROOT:-}" \] \\/,+1d')
            extra_env=(
                P0_EXPECT_UID=1000
                P0_FORBIDDEN_GIDS=0
            )
            expected='P0_VENV_ROOT: preregistered per-SHA venv root is required'
            ;;
        *) printf 'HARNESS_ERROR unknown_input=%s\n' "$input"; return 2 ;;
    esac

    raw="$(
        "${mutate[@]}" |
        env -i \
            PATH="$PATH" \
            RUNID=qa-rp6 \
            EV_STAGE_ID=p0 \
            EV_DIR=/qa-rp6 \
            EV_LOG=/qa-rp6/p0.log \
            "${extra_env[@]}" \
            bash --noprofile --norc -c '
                rp0_require_safe_component() { return 0; }
                rp0_allocate_evidence_dir() { return 0; }
                . /dev/stdin
            ' 2>&1
    )" || probe_rc=$?

    printf '%s\n' "$raw"
    if [ "$probe_rc" -eq 1 ] &&
       case "$raw" in *"$expected"*) true ;; *) false ;; esac
    then
        printf 'F4_GREEN input=%s mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=%s\n' \
            "$input" "$probe_rc"
        return 0
    fi
    printf 'F4_RED input=%s mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=%s\n' \
        "$input" "$probe_rc"
    return 1
}

overall=0
for input in P0_EXPECT_UID P0_FORBIDDEN_GIDS P0_VENV_ROOT; do
    set +e
    pre="$(git show "HEAD:$target" | exercise_f4_one "$input" 2>&1)"; pre_rc=$?
    post="$(exercise_f4_one "$input" < "$target" 2>&1)"; post_rc=$?
    set -e
    printf '%s\n' "=== F4 $input PRE-FIX + PRECHECK-REMOVAL MUTATION ===" "$pre" "CHECK_RC=$pre_rc"
    printf '%s\n' "=== F4 $input REPAIRED + SAME MUTATION ===" "$post" "CHECK_RC=$post_rc"
    if [ "$pre_rc" -ne 1 ] || [ "$post_rc" -ne 0 ]; then overall=1; fi
done
[ "$overall" -eq 0 ]
printf 'F4_QA_SUMMARY expected_red_green_each=1/0 inputs=3 result=PASS\n'
```

Real captured output:

```text
=== F4 P0_EXPECT_UID PRE-FIX + PRECHECK-REMOVAL MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
P0_SECTION preregistered_inputs
/dev/stdin: line 335: P0_EXPECT_UID: unbound variable
F4_RED input=P0_EXPECT_UID mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=1
CHECK_RC=1
=== F4 P0_EXPECT_UID REPAIRED + SAME MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 265: P0_EXPECT_UID: preregistered numeric uid of the route login is required
F4_GREEN input=P0_EXPECT_UID mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=1
CHECK_RC=0
=== F4 P0_FORBIDDEN_GIDS PRE-FIX + PRECHECK-REMOVAL MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 267: P0_FORBIDDEN_GIDS: unbound variable
F4_RED input=P0_FORBIDDEN_GIDS mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=1
CHECK_RC=1
=== F4 P0_FORBIDDEN_GIDS REPAIRED + SAME MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 272: P0_FORBIDDEN_GIDS: preregistered numeric forbidden-gid list is required
F4_GREEN input=P0_FORBIDDEN_GIDS mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=1
CHECK_RC=0
=== F4 P0_VENV_ROOT PRE-FIX + PRECHECK-REMOVAL MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 280: P0_VENV_ROOT: unbound variable
F4_RED input=P0_VENV_ROOT mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=1
CHECK_RC=1
=== F4 P0_VENV_ROOT REPAIRED + SAME MUTATION ===
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 287: P0_VENV_ROOT: preregistered per-SHA venv root is required
F4_GREEN input=P0_VENV_ROOT mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=1
CHECK_RC=0
F4_QA_SUMMARY expected_red_green_each=1/0 inputs=3 result=PASS
```

## Explicit local limit

The complete P0 block was not run. It requires the accepted RP0 library/bootstrap,
Linux `/proc` namespace objects, the preregistered per-SHA venv, and a reachable system
manager in the staging execution domain. This task has no host-contact authority. The
repair-specific tests above either execute only the terminal evidence producers or abort
inside input validation before any external P0 probe; they print no host file content.

## C13 getent resolution arm — repair decisions

- The arm resolves the names `gatea` and `mtc-bridge` to numerics with a PINNED
  absolute `getent` added to the inventory as the 12th RO tool, parses each
  `getent passwd` record whole under the passwd grammar (Pattern 5: exactly
  seven colon-separated fields; a duplicate, multiline or structurally
  malformed record is ambiguous and is not a record), and admits on NUMERIC
  uid/gid only (Pattern 8). The name, passwd-placeholder, gecos, home and shell
  fields are captured into `P0_PW_DIAG` / `name_diag=[...]` as diagnostics and
  are never asserted or compared.
- rc contract (kickoff + the F2 polarity ruling): a `getent` that is
  missing/unpinnable, or a lookup error, or an unparsable or duplicate record,
  is `identity_unresolvable` rc 3 (inability to evaluate); a `gatea` numeric
  mismatch against the live `id -u`/`id -g` or `P0_EXPECT_UID` is
  `identity_unexpected` rc 3; a `mtc-bridge` valid no-match (getent rc 2) OR a
  numeric mismatch against `P0_STATE_UID:P0_STATE_GID` is
  `state_account_resolution_unexpected` rc 3.
- `P0_STATE_UID`/`P0_STATE_GID` use the same `p0_require_uint` rc-3 pre-check
  + `:?` fail-closed backstop as `P0_EXPECT_UID` (the F4 pattern). The live
  `id -u`/`id -g` are recaptured inside the arm via `p0_capture_numeric` so the
  existing identity section is byte-for-byte untouched; `getent` runs with the
  caller environment inherited and `LC_ALL=C`, mirroring the `id` probe.
- The row-3 group half (numeric `id -G` excluding gids 0 and 988) stays the
  existing identity section's `P0_FORBIDDEN_GIDS` responsibility and is not
  re-asserted here; the residual that `getent` consults whatever NSS is
  configured (local passwd vs sss/ldap/…) is disclosed in
  `does_not_establish=nss_source_identity_of_getent_resolution`.

## C13 getent arm — exact RED/GREEN command

> **SUPPLEMENTAL under D026 (C13 audit finding 2, accepted).** This fence and the
> next one call `p0_resolve_accounts` from the harness itself, so deleting the
> block's production integration call would leave them green: their "RED" cases
> are deviant-input cases against unmutated code, not implementation
> falsification. They are retained as behavioural documentation of the arm. The
> D026 closure evidence is the round-3 section
> "C13 R3 — D026 harness 1", which drives the arm from the block's own call site
> and runs the same assertions against mutated and pre-repair bytes.

The command extracts the REAL arm and the helpers it calls from the repaired
block (so the tested code is the block's code, not a transcription), sources
them, and exercises the arm against a QA-only `getent` fixture. The production
block still pins an absolute `getent` from its inventory; the fixture exists
only so the arm can be run without a host NSS.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
blk=MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
shim=/tmp/rp6qa_getent_shim.sh
funcs=/tmp/rp6qa_arm_funcs.sh

# QA-only getent fixture. Production pins an absolute getent from the inventory.
cat > "$shim" <<'SHIMEOF'
#!/usr/bin/env bash
key="${2:-}"
case "$key" in
    gatea)
        case "${SHIM_MODE:-}" in
            wrong_gatea_uid) printf 'gatea:x:4242:%s:a:/h:/s\n' "$(id -g)"; exit 0 ;;
            dup_gatea) printf 'gatea:x:%s:%s:a:/h:/s\ngatea:x:%s:%s:b:/h:/s\n' "$(id -u)" "$(id -g)" "$(id -u)" "$(id -g)"; exit 0 ;;
            *) printf 'gatea:x:%s:%s:gatea route login:/home/gatea:/bin/bash\n' "$(id -u)" "$(id -g)"; exit 0 ;;
        esac ;;
    mtc-bridge)
        case "${SHIM_MODE:-}" in
            wrong_mtc_gid) printf 'mtc-bridge:x:999:989:svc:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
            mtc_nomatch) exit 2 ;;
            *) printf 'mtc-bridge:x:999:988:mtc-bridge service:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
        esac ;;
esac
exit 2
SHIMEOF
chmod +x "$shim"

# Extract the REAL arm and the helpers it calls from the repaired block.
{
    sed -n '/^p0_stop() {/p'                "$blk"
    sed -n '/^p0_sanitize()/,/^}/p'         "$blk"
    sed -n '/^p0_count_substr()/,/^}/p'     "$blk"
    sed -n '/^p0_capture_numeric()/,/^}/p'  "$blk"
    sed -n '/^p0_resolve_passwd()/,/^}/p'   "$blk"
    sed -n '/^p0_resolve_accounts()/,/^}/p' "$blk"
} > "$funcs"

run_arm() {
    local mode="${1-}" want_rc="${2-}" want_subst="${3-}" out rc=0
    out="$(
        SHIM_MODE="$mode" \
        P0_GETENT="$shim" \
        P0_ID="$(command -v id)" \
        P0_EXPECT_UID="$(id -u)" \
        P0_STATE_UID=999 \
        P0_STATE_GID=988 \
        bash --noprofile --norc -c '
            set -Eeuo pipefail
            . "$1"
            p0_resolve_accounts
        ' _ "$funcs"
    )" || rc=$?
    printf '%s\n' "$out"
    printf 'ARM_RC=%s\n' "$rc"
    if [ "$rc" = "$want_rc" ] && case "$out" in *"$want_subst"*) true ;; *) false ;; esac; then
        printf 'CASE_OK mode=%s expected_rc=%s subst=%s\n' "$mode" "$want_rc" "$want_subst"
        return 0
    fi
    printf 'CASE_BAD mode=%s expected_rc=%s subst=%s\n' "$mode" "$want_rc" "$want_subst"
    return 1
}

overall=0
set +e
# GREEN: both accounts resolve to the expected numerics (rc 0).
run_arm ''             0 'P0_account_admitted account=mtc-bridge numeric=999:988' || overall=1
# RED: mtc-bridge resolves to the wrong gid -> state_account_resolution_unexpected (rc 3).
run_arm wrong_mtc_gid  3 'state_account_resolution_unexpected account=mtc-bridge' || overall=1
# RED: mtc-bridge valid no-match (getent rc 2) -> state_account_resolution_unexpected (rc 3).
run_arm mtc_nomatch    3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' || overall=1
# RED: gatea resolves to the wrong uid -> identity_unexpected (rc 3).
run_arm wrong_gatea_uid 3 'identity_unexpected account=gatea' || overall=1
# RED: gatea duplicate record -> identity_unresolvable (ambiguous, rc 3, not a verdict).
run_arm dup_gatea      3 'identity_unresolvable account=gatea' || overall=1
set -e
[ "$overall" -eq 0 ]
printf 'C13_ARM_QA_SUMMARY expected=green_rc0_then_4x_red_rc3 result=PASS\n'
```

## C13 getent arm — real output

Executed by the Lead 2026-08-10 in an unhindered Git Bash process, command above
run verbatim against repaired bytes `cfdb23b8…` (the implementer session's Bash
tool gated execution; the implementer correctly recorded PENDING rather than
fabricate). Real captured output:

```text
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=988 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_account_admitted account=mtc-bridge numeric=999:988 matches=prereg_state_uid_gid name=diagnostic_only
ARM_RC=0
CASE_OK mode= expected_rc=0 subst=P0_account_admitted account=mtc-bridge numeric=999:988
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=989 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=999:989 expected_numeric=999:988
ARM_RC=3
CASE_OK mode=wrong_mtc_gid expected_rc=3 subst=state_account_resolution_unexpected account=mtc-bridge
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
CASE_OK mode=mtc_nomatch expected_rc=3 subst=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent
P0_account account=gatea outcome=resolved uid=4242 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_STOP reason=identity_unexpected account=gatea observed_numeric=4242:4096 expected_numeric=4096:4096,prereg_uid=4096
ARM_RC=3
CASE_OK mode=wrong_gatea_uid expected_rc=3 subst=identity_unexpected account=gatea
P0_STOP reason=identity_unresolvable account=gatea detail=[gatea:x:4096:4096:a:/h:/s gatea:x:4096:4096:b:/h:/s]
ARM_RC=3
CASE_OK mode=dup_gatea expected_rc=3 subst=identity_unresolvable account=gatea
C13_ARM_QA_SUMMARY expected=green_rc0_then_4x_red_rc3 result=PASS
```

GREEN rc 0 with both accounts admitted; all four REDs rc 3 with the exact
preregistered reason tokens. (Local uid/gid 4096 stands in for the live
identity; the fixture never asserts names.)

## C13 new-input backstop — exact command (P0_STATE_UID / P0_STATE_GID)

> **SUPPLEMENTAL under D026 (C13 audit finding 2, accepted).** This fence mutates
> away each rc-3 pre-check but never removes the `:?` backstop itself, so it does
> not falsify the claim that the backstop is what produces the GREEN. The
> retained as-drafted RED below is a harness defect (missing stdin), not an
> implementation falsification. The D026 closure evidence is the round-3 section
> "C13 R3 — D026 harness 2", which runs the same assertion against a mutation
> that removes the pre-check AND the backstop.

Same shape as the F4 mutation test: delete each new input's rc-3 pre-check,
then source the block with that input unset and the rest supplied; the `:?`
backstop must fire with the named message. Note the new inputs now precede
`P0_FORBIDDEN_GIDS` in the block, so any re-run of the *prior* F4
`P0_FORBIDDEN_GIDS` / `P0_VENV_ROOT` commands would now stop at
`P0_STATE_UID` first — those prior commands are historical evidence from the
pre-C13 input contract; supply `P0_STATE_UID=999` and `P0_STATE_GID=988` to
re-run them past the new inputs.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
target='MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh'
cand='2ce41e34bceb599d80af24c5c33d835820ec321b'

exercise_c13_backstop_one() {
    local input="$1" expected raw probe_rc=0
    local -a mutate extra_env
    case "$input" in
        P0_STATE_UID)
            mutate=(sed '/^p0_require_uint P0_STATE_UID /d')
            extra_env=(
                P0_EXPECT_UID=1000
                P0_STATE_GID=988
                P0_FORBIDDEN_GIDS=0
                P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand"
            )
            expected='P0_STATE_UID: preregistered numeric uid of the mtc-bridge service account is required'
            ;;
        P0_STATE_GID)
            mutate=(sed '/^p0_require_uint P0_STATE_GID /d')
            extra_env=(
                P0_EXPECT_UID=1000
                P0_STATE_UID=999
                P0_FORBIDDEN_GIDS=0
                P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand"
            )
            expected='P0_STATE_GID: preregistered numeric gid of the mtc-bridge service account is required'
            ;;
        *) printf 'HARNESS_ERROR unknown_input=%s\n' "$input"; return 2 ;;
    esac

    raw="$(
        "${mutate[@]}" "$target" |
        env -i \
            PATH="$PATH" \
            RUNID=qa-rp6 \
            EV_STAGE_ID=p0 \
            EV_DIR=/qa-rp6 \
            EV_LOG=/qa-rp6/p0.log \
            "${extra_env[@]}" \
            bash --noprofile --norc -c '
                rp0_require_safe_component() { return 0; }
                rp0_allocate_evidence_dir() { return 0; }
                . /dev/stdin
            ' 2>&1
    )" || probe_rc=$?

    printf '%s\n' "$raw"
    if [ "$probe_rc" -eq 1 ] &&
       case "$raw" in *"$expected"*) true ;; *) false ;; esac
    then
        printf 'C13_BACKSTOP_GREEN input=%s mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=%s\n' \
            "$input" "$probe_rc"
        return 0
    fi
    printf 'C13_BACKSTOP_RED input=%s mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=%s\n' \
        "$input" "$probe_rc"
    return 1
}

overall=0
for input in P0_STATE_UID P0_STATE_GID; do
    set +e
    post="$(exercise_c13_backstop_one "$input" 2>&1)"; post_rc=$?
    set -e
    printf '%s\n' "=== C13 BACKSTOP $input REPAIRED + PRECHECK-REMOVAL MUTATION ===" "$post" "CHECK_RC=$post_rc"
    [ "$post_rc" -eq 0 ] || overall=1
done
if [ "$overall" -eq 0 ]; then
    printf 'C13_BACKSTOP_QA_SUMMARY expected_red_green_each=1/0 inputs=2 result=PASS\n'
else
    printf 'C13_BACKSTOP_QA_SUMMARY expected_red_green_each=1/0 inputs=2 result=FAIL\n'
    exit 1
fi
```

### Lead harness correction (2026-08-10, before first execution of this section)

The implementer session could not execute this harness (execution gate) and its
as-drafted form carried two defects, both caught by the Lead running it before
accepting any output:

1. **Missing block input.** The draft invoked `"${mutate[@]}" |` with nothing on
   stdin — unlike the F4 harness above, whose *callers* feed the block
   (`git show "HEAD:$target" | …` / `… < "$target"`), the C13 caller fed nothing,
   so `sed` emitted an empty script, the backstop was never exercised, and both
   cases came back RED with `raw_rc=0`. Fixed by passing `"$target"` to `sed`
   directly. The as-drafted RED run is retained below as evidence this harness
   can fail.
2. **Ungated summary.** The trailing `[ "$overall" -eq 0 ]` guard did not stop
   the PASS line in the observed environment (the as-drafted run printed
   `result=PASS` directly after two REDs) — a summary that cannot fail
   (Pattern 10). Replaced with an explicit if/else that prints FAIL and exits 1.

As-drafted run (defective harness — proves it can fail):

```text
=== C13 BACKSTOP P0_STATE_UID REPAIRED + PRECHECK-REMOVAL MUTATION ===

C13_BACKSTOP_RED input=P0_STATE_UID mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=0
CHECK_RC=1
=== C13 BACKSTOP P0_STATE_GID REPAIRED + PRECHECK-REMOVAL MUTATION ===

C13_BACKSTOP_RED input=P0_STATE_GID mutation=removed_rc3_precheck backstop_absent_or_wrong raw_rc=0
CHECK_RC=1
C13_BACKSTOP_QA_SUMMARY expected_red_green_each=1/0 inputs=2 result=PASS
```

Corrected harness, real output (Lead, Git Bash, repaired bytes `cfdb23b8…`;
probe output trimmed to the last three lines per case for record size):

```text
=== C13 BACKSTOP P0_STATE_UID REPAIRED + PRECHECK-REMOVAL MUTATION ===
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 281: P0_STATE_UID: preregistered numeric uid of the mtc-bridge service account is required
C13_BACKSTOP_GREEN input=P0_STATE_UID mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=1
CHECK_RC=0
=== C13 BACKSTOP P0_STATE_GID REPAIRED + PRECHECK-REMOVAL MUTATION ===
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 283: P0_STATE_GID: preregistered numeric gid of the mtc-bridge service account is required
C13_BACKSTOP_GREEN input=P0_STATE_GID mutation=removed_rc3_precheck backstop_named_missing_input raw_rc=1
CHECK_RC=0
C13_BACKSTOP_QA_SUMMARY expected_red_green_each=1/0 inputs=2 result=PASS
```

Both backstops fire with the named message at rc 1.

## C13 artefact measurements (real, computed in-session)

- Repaired `RP6-P0.sh` SHA-256: `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`
- Repaired `RP6-P0.sh` byte count: `54109`
- Baseline (pre-C13) SHA-256: `6c5b89456b4b4072969f7c928328d2d0ecb51e8476a15c5a7401f2988c9766f7` (matched the kickoff exactly before editing)
- Baseline byte count: `44979`
- `bash -n` on the repaired block: **PASS** (Lead, Git Bash, 2026-08-10:
  `bash -n MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh` → rc 0,
  `BASH_N=PASS`; hash re-verified `cfdb23b8…`, 54109 B — matches the
  implementer's recorded values exactly).

## C13 explicit local limit

The complete P0 block was not run (it needs the accepted RP0 library/bootstrap,
Linux `/proc` namespace objects, the preregistered per-SHA venv, and a reachable
system manager). The C13 tests above either source only the extracted arm
function definitions (no block top-level execution) and exercise them against a
local getent fixture, or abort inside input validation before any external P0
probe. No host was contacted and no host file content was printed.

---

# C13 round 3 — repair of the Codex audit `RP6_C13_CODEX_AUDIT_2026-08-10.md`

Implementer: Claude Opus 5 (GLM, the C13 implementer, is quota-blocked). All
output below was captured in this session in a local Git Bash 5.2.37
`--noprofile --norc` process. No host was contacted, no network command was run,
and nothing outside the four kickoff deliverable files was modified.

## C13 R3 — repair decisions

- **F1 (HIGH), fixed in the block.** `p0_resolve_passwd` now accepts `rc 2` as
  `nomatch` only when the complete merged capture is empty — this interface's
  exact valid-no-match shape. `rc 2` carrying any byte (an NSS diagnostic on
  stderr, a partial record, a module warning) sets `P0_PW_OUTCOME=error`, so the
  caller emits `identity_unresolvable … rc 3` for both accounts instead of
  asserting positive absence it never observed. `P0_PW_DIAG` on the surviving
  no-match path records `empty_capture_at_rc2`, i.e. the reason the no-match was
  accepted, rather than a sanitized empty string. Every other arm of the parser
  and both caller `case` statements are byte-identical; the valid-no-match arm
  (`mtc-bridge`, rc 2, empty capture → `state_account_resolution_unexpected
  observed_numeric=absent`) is unchanged and is regression-tested below.
- **F2 (MEDIUM), fixed in this QA.** The two earlier C13 fences are re-labelled
  SUPPLEMENTAL in place and two D026 harnesses are added. Harness 1 no longer
  calls the arm: it extracts the block's own top-level driver lines by exact
  whole-line match and lets the block invoke `p0_resolve_accounts`, then runs one
  assertion set across three source variants (R3-repaired bytes, pre-R3 bytes,
  and bytes with the production integration call deleted). Harness 2 adds the
  mutation that removes the `:?` backstop itself. Both harnesses check assertion
  POLARITY: a case declared `RED` fails the run if its assertion is met, so a
  mutation that is not killed is a harness failure, not a silent pass.
- **F3 (MEDIUM), fixed in the block.** The "NUMERIC IDENTITY ONLY" header no
  longer claims that no name is looked up or captured and that the block asks the
  resolver database nothing. It now says what is true: admission is numeric only
  and no name is ever compared or asserted, two names ARE queried via the pinned
  `getent passwd`, the returned name/gecos/home/shell fields are recorded as
  diagnostics that no verdict depends on, and which NSS source answered is not
  established (already carried in `does_not_establish`).

## C13 R3 — D026 harness 1 (arm driven by the block's own integration call)

What makes this D026 rather than deviant-input testing:

1. The harness never calls `p0_resolve_accounts`. It appends the block's two
   top-level driver lines — matched as exact whole lines out of the source bytes
   — after the extracted function definitions, so whether the arm runs at all is
   decided by the block.
2. Mutation `nocall` deletes the production integration call
   (`p0_resolve_accounts` at the block's top level). Every arm assertion must
   then fail; the run fails if any of them still passes.
3. The F1 assertions are run against the **pre-repair bytes**
   (`git show cbaf3ec8:<path>` — the C13 commit, SHA-256 `cfdb23b8…`, 54109 B),
   which must fail them, and against the repaired bytes, which must pass them.
   The defect itself is additionally recorded as a positive assertion: on
   pre-repair bytes an rc-2-plus-diagnostic capture really does emit
   `state_account_resolution_unexpected … observed_numeric=absent`.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
blk=MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
pre_rev=cbaf3ec8    # the C13 commit = the PRE-R3-repair bytes cfdb23b8..., 54109 B
w=/tmp/rp6qa_c13r3; rm -rf "$w"; mkdir -p "$w"

# ---- QA-only getent fixture (production pins an absolute getent from the inventory).
cat > "$w/getent_shim.sh" <<'SHIMEOF'
#!/usr/bin/env bash
key="${2:-}"
case "$key" in
    gatea)
        case "${SHIM_MODE:-}" in
            wrong_gatea_uid) printf 'gatea:x:4242:%s:a:/h:/s\n' "$(id -g)"; exit 0 ;;
            dup_gatea) printf 'gatea:x:%s:%s:a:/h:/s\ngatea:x:%s:%s:b:/h:/s\n' "$(id -u)" "$(id -g)" "$(id -u)" "$(id -g)"; exit 0 ;;
            gatea_rc2_diag) printf 'getent: nss module returned SERVBUSY for gatea\n' >&2; exit 2 ;;
            *) printf 'gatea:x:%s:%s:gatea route login:/home/gatea:/bin/bash\n' "$(id -u)" "$(id -g)"; exit 0 ;;
        esac ;;
    mtc-bridge)
        case "${SHIM_MODE:-}" in
            wrong_mtc_gid) printf 'mtc-bridge:x:999:989:svc:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
            mtc_nomatch) exit 2 ;;
            mtc_rc2_diag) printf 'getent: sss_nss: connection to the name service timed out\n' >&2; exit 2 ;;
            mtc_rc2_partial) printf 'mtc-bridge:x:999\n'; exit 2 ;;
            *) printf 'mtc-bridge:x:999:988:mtc-bridge service:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
        esac ;;
esac
exit 2
SHIMEOF
chmod +x "$w/getent_shim.sh"

# ---- the three source variants under test -------------------------------------
cp "$blk" "$w/src_repaired.sh"                                   # R3-repaired bytes
git show "$pre_rev:$blk" > "$w/src_prerepair.sh"                 # pre-R3 bytes (F1 unfixed)
awk '$0!="p0_resolve_accounts"' "$blk" > "$w/src_nocall.sh"      # MUTATION: production integration call deleted

# ---- extract the arm AND the block's own top-level driver ---------------------
# The driver lines are taken from the source bytes by exact whole-line match, so
# the block - not this harness - decides whether the arm runs at all. If the
# integration call is deleted, nothing invokes the arm and every arm assertion
# must fail. Nothing here calls p0_resolve_accounts.
extract() {
    {
        sed -n '/^p0_stop() {/p'                "$1"
        sed -n '/^p0_sanitize()/,/^}/p'         "$1"
        sed -n '/^p0_count_substr()/,/^}/p'     "$1"
        sed -n '/^p0_capture_numeric()/,/^}/p'  "$1"
        sed -n '/^p0_resolve_passwd()/,/^}/p'   "$1"
        sed -n '/^p0_resolve_accounts()/,/^}/p' "$1"
        awk '$0=="printf '\''P0_SECTION accounts\\n'\''" || $0=="p0_resolve_accounts"' "$1"
    } > "$2"
}
for v in repaired prerepair nocall; do extract "$w/src_$v.sh" "$w/funcs_$v.sh"; done
printf 'DRIVER_LINES repaired=%s prerepair=%s nocall=%s\n' \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_repaired.sh")" \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_prerepair.sh")" \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_nocall.sh")"

run_case() {  # variant mode want_rc want_subst polarity
    local variant="$1" mode="$2" want_rc="$3" want_subst="$4" polarity="$5" out rc=0 ok=0
    out="$(
        SHIM_MODE="$mode" \
        P0_GETENT="$w/getent_shim.sh" \
        P0_ID="$(command -v id)" \
        P0_EXPECT_UID="$(id -u)" \
        P0_STATE_UID=999 \
        P0_STATE_GID=988 \
        bash --noprofile --norc -c '
            set -Eeuo pipefail
            . "$1"
        ' _ "$w/funcs_$variant.sh"
    )" || rc=$?
    printf -- '--- variant=%s mode=%s\n%s\nARM_RC=%s\n' "$variant" "${mode:-<none>}" "$out" "$rc"
    if [ "$rc" = "$want_rc" ] && case "$out" in *"$want_subst"*) true ;; *) false ;; esac; then ok=1; fi
    if [ "$ok" -eq 1 ]; then
        printf 'ASSERT_MET variant=%s mode=%s expected_rc=%s subst=[%s] polarity=%s\n' \
            "$variant" "${mode:-<none>}" "$want_rc" "$want_subst" "$polarity"
    else
        printf 'ASSERT_UNMET variant=%s mode=%s expected_rc=%s subst=[%s] polarity=%s\n' \
            "$variant" "${mode:-<none>}" "$want_rc" "$want_subst" "$polarity"
    fi
    # GREEN cases must meet the assertion; RED cases (mutated/pre-repair bytes) must NOT.
    case "$polarity:$ok" in
        GREEN:1|RED:0) printf 'CASE_OK\n'; return 0 ;;
        *)             printf 'CASE_BAD\n'; return 1 ;;
    esac
}

overall=0
set +e
# === A. repaired bytes, block-driven: the pre-existing five cases ==============
run_case repaired ''               0 'P0_account_admitted account=mtc-bridge numeric=999:988'            GREEN || overall=1
run_case repaired wrong_mtc_gid    3 'state_account_resolution_unexpected account=mtc-bridge'            GREEN || overall=1
run_case repaired mtc_nomatch      3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' GREEN || overall=1
run_case repaired wrong_gatea_uid  3 'identity_unexpected account=gatea'                                 GREEN || overall=1
run_case repaired dup_gatea        3 'identity_unresolvable account=gatea'                               GREEN || overall=1

# === B. F2(a): the production integration call is deleted -> every arm assertion must fail
run_case nocall   ''               0 'P0_account_admitted account=mtc-bridge numeric=999:988'            RED   || overall=1
run_case nocall   wrong_mtc_gid    3 'state_account_resolution_unexpected account=mtc-bridge'            RED   || overall=1
run_case nocall   mtc_rc2_diag     3 'identity_unresolvable account=mtc-bridge'                          RED   || overall=1

# === C. F2(c)/F1: rc 2 carrying bytes is a lookup error, not a valid no-match ==
#  GREEN on repaired bytes ...
run_case repaired mtc_rc2_diag     3 'identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]' GREEN || overall=1
run_case repaired mtc_rc2_partial  3 'identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]'                                          GREEN || overall=1
run_case repaired gatea_rc2_diag   3 'identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]'                 GREEN || overall=1
#  ... and RED on the pre-repair bytes, which classify the same capture as a valid no-match.
run_case prerepair mtc_rc2_diag    3 'identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]' RED || overall=1
run_case prerepair mtc_rc2_partial 3 'identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]'                                          RED || overall=1
run_case prerepair gatea_rc2_diag  3 'identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]'                 RED || overall=1
#  What the pre-repair bytes emit instead, recorded positively as the defect:
run_case prerepair mtc_rc2_diag    3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' GREEN || overall=1

# === D. the valid no-match arm still works after the F1 narrowing (regression) =
run_case repaired mtc_nomatch      3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match' GREEN || overall=1
set -e

if [ "$overall" -eq 0 ]; then
    printf 'C13_R3_ARM_QA_SUMMARY cases=16 result=PASS\n'
else
    printf 'C13_R3_ARM_QA_SUMMARY cases=16 result=FAIL\n'
    exit 1
fi
```

### C13 R3 — D026 harness 1, real output

Captured 2026-08-10, Git Bash, against working-tree bytes
`ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`, 55467 B.
Process rc 0.

```text
DRIVER_LINES repaired=1 prerepair=1 nocall=0
--- variant=repaired mode=<none>
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=988 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_account_admitted account=mtc-bridge numeric=999:988 matches=prereg_state_uid_gid name=diagnostic_only
ARM_RC=0
ASSERT_MET variant=repaired mode=<none> expected_rc=0 subst=[P0_account_admitted account=mtc-bridge numeric=999:988] polarity=GREEN
CASE_OK
--- variant=repaired mode=wrong_mtc_gid
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=989 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=999:989 expected_numeric=999:988
ARM_RC=3
ASSERT_MET variant=repaired mode=wrong_mtc_gid expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_nomatch
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_nomatch expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent] polarity=GREEN
CASE_OK
--- variant=repaired mode=wrong_gatea_uid
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4242 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_STOP reason=identity_unexpected account=gatea observed_numeric=4242:4096 expected_numeric=4096:4096,prereg_uid=4096
ARM_RC=3
ASSERT_MET variant=repaired mode=wrong_gatea_uid expected_rc=3 subst=[identity_unexpected account=gatea] polarity=GREEN
CASE_OK
--- variant=repaired mode=dup_gatea
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea detail=[gatea:x:4096:4096:a:/h:/s gatea:x:4096:4096:b:/h:/s]
ARM_RC=3
ASSERT_MET variant=repaired mode=dup_gatea expected_rc=3 subst=[identity_unresolvable account=gatea] polarity=GREEN
CASE_OK
--- variant=nocall mode=<none>
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=<none> expected_rc=0 subst=[P0_account_admitted account=mtc-bridge numeric=999:988] polarity=RED
CASE_OK
--- variant=nocall mode=wrong_mtc_gid
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=wrong_mtc_gid expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge] polarity=RED
CASE_OK
--- variant=nocall mode=mtc_rc2_diag
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge] polarity=RED
CASE_OK
--- variant=repaired mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_rc2_partial
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_partial expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]] polarity=GREEN
CASE_OK
--- variant=repaired mode=gatea_rc2_diag
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]
ARM_RC=3
ASSERT_MET variant=repaired mode=gatea_rc2_diag expected_rc=3 subst=[identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]] polarity=GREEN
CASE_OK
--- variant=prerepair mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]] polarity=RED
CASE_OK
--- variant=prerepair mode=mtc_rc2_partial
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=mtc_rc2_partial expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]] polarity=RED
CASE_OK
--- variant=prerepair mode=gatea_rc2_diag
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea rc=2 detail=getent_valid_no_match_for_route_login
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=gatea_rc2_diag expected_rc=3 subst=[identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]] polarity=RED
CASE_OK
--- variant=prerepair mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=prerepair mode=mtc_rc2_diag expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_nomatch
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_nomatch expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match] polarity=GREEN
CASE_OK
C13_R3_ARM_QA_SUMMARY cases=16 result=PASS
```

What the output establishes, line by line:

- `DRIVER_LINES … nocall=0` — the mutation really removed the integration call
  from the extracted material; the other two variants keep exactly one.
- Block B: with the call deleted, all three arm assertions go `ASSERT_UNMET` and
  the arm produces nothing but the section header at rc 0. The harness is now
  killed by the mutation the auditor named; it can no longer be green without the
  block's own call site.
- Block C: the identical rc-2-plus-bytes captures produce `identity_unresolvable`
  rc 3 on repaired bytes and `state_account_resolution_unexpected …
  observed_numeric=absent` on pre-repair bytes — the F1 defect reproduced and
  then killed. `gatea` under pre-repair bytes emits `identity_unresolvable
  account=gatea rc=2 detail=getent_valid_no_match_for_route_login`, i.e. the right
  verdict for the wrong reason (a claimed valid no-match), which the assertion on
  `detail=[…]` distinguishes.
- Block D: the true valid no-match (rc 2, empty capture) still yields the exact
  preregistered `observed_numeric=absent … detail=getent_valid_no_match` line, so
  the narrowing did not collapse the row-3 arm.

## C13 R3 — D026 harness 2 (the `:?` backstop itself removed)

One assertion — rc 1 plus the named input message — run against two mutations per
new input. `precheck_only` must meet it (the backstop fires). `precheck_and_backstop`
must NOT meet it; if it did, the GREEN above would not be evidence about the
backstop.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
target='MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh'
cand='2ce41e34bceb599d80af24c5c33d835820ec321b'

# Two mutations per new input, ONE assertion for both:
#   precheck_only          - delete the rc-3 pre-check, keep the `:?` backstop.
#                            The backstop must fire: rc 1 + the named message.
#   precheck_and_backstop  - delete the pre-check AND the `:?` backstop itself.
#                            The same assertion must now FAIL (the mutant is
#                            killed); if it still passed, the recorded GREEN
#                            above would not be evidence about the backstop.
mutate() {  # $1 = input name, $2 = mutation kind; block bytes on stdout
    case "$2" in
        precheck_only)
            awk -v n="$1" '$0 !~ "^p0_require_uint "n" " ' "$target" ;;
        precheck_and_backstop)
            awk -v n="$1" '$0 !~ "^p0_require_uint "n" " && index($0, ": \"${" n ":?") == 0' "$target" ;;
        *) printf 'HARNESS_ERROR unknown_mutation=%s\n' "$2" >&2; return 2 ;;
    esac
}

exercise() {  # $1 = input name, $2 = mutation kind, $3 = expected polarity
    local input="$1" kind="$2" polarity="$3" expected raw probe_rc=0 met=0
    local -a extra_env
    case "$input" in
        P0_STATE_UID)
            extra_env=(P0_EXPECT_UID=1000 P0_STATE_GID=988 P0_FORBIDDEN_GIDS=0
                       P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand")
            expected='P0_STATE_UID: preregistered numeric uid of the mtc-bridge service account is required' ;;
        P0_STATE_GID)
            extra_env=(P0_EXPECT_UID=1000 P0_STATE_UID=999 P0_FORBIDDEN_GIDS=0
                       P0_VENV_ROOT="/opt/mtc-bridge/venvs/$cand")
            expected='P0_STATE_GID: preregistered numeric gid of the mtc-bridge service account is required' ;;
        *) printf 'HARNESS_ERROR unknown_input=%s\n' "$input"; return 2 ;;
    esac

    # Sanity: the mutation must actually have removed lines from the block.
    printf 'MUTATION_LINES_REMOVED input=%s kind=%s n=%s\n' "$input" "$kind" \
        "$(( $(wc -l < "$target") - $(mutate "$input" "$kind" | wc -l) ))"

    raw="$(
        mutate "$input" "$kind" |
        env -i \
            PATH="$PATH" \
            RUNID=qa-rp6 \
            EV_STAGE_ID=p0 \
            EV_DIR=/qa-rp6 \
            EV_LOG=/qa-rp6/p0.log \
            "${extra_env[@]}" \
            bash --noprofile --norc -c '
                rp0_require_safe_component() { return 0; }
                rp0_allocate_evidence_dir() { return 0; }
                . /dev/stdin
            ' 2>&1
    )" || probe_rc=$?

    printf '%s\n' "$raw"
    if [ "$probe_rc" -eq 1 ] && case "$raw" in *"$expected"*) true ;; *) false ;; esac; then met=1; fi
    printf 'ASSERT_%s input=%s mutation=%s raw_rc=%s polarity=%s\n' \
        "$( [ "$met" -eq 1 ] && echo MET || echo UNMET )" "$input" "$kind" "$probe_rc" "$polarity"
    case "$polarity:$met" in
        GREEN:1|RED:0) printf 'CASE_OK\n'; return 0 ;;
        *)             printf 'CASE_BAD\n'; return 1 ;;
    esac
}

overall=0
for input in P0_STATE_UID P0_STATE_GID; do
    for spec in precheck_only:GREEN precheck_and_backstop:RED; do
        kind="${spec%%:*}"; polarity="${spec##*:}"
        set +e
        post="$(exercise "$input" "$kind" "$polarity" 2>&1)"; post_rc=$?
        set -e
        printf '%s\n' "=== $input / $kind / expect_$polarity ===" "$post" "CHECK_RC=$post_rc"
        [ "$post_rc" -eq 0 ] || overall=1
    done
done
if [ "$overall" -eq 0 ]; then
    printf 'C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS\n'
else
    printf 'C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=FAIL\n'
    exit 1
fi
```

### C13 R3 — D026 harness 2, real output

Captured 2026-08-10, Git Bash, same working-tree bytes. Process rc 0.

```text
=== P0_STATE_UID / precheck_only / expect_GREEN ===
MUTATION_LINES_REMOVED input=P0_STATE_UID kind=precheck_only n=1
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 288: P0_STATE_UID: preregistered numeric uid of the mtc-bridge service account is required
ASSERT_MET input=P0_STATE_UID mutation=precheck_only raw_rc=1 polarity=GREEN
CASE_OK
CHECK_RC=0
=== P0_STATE_UID / precheck_and_backstop / expect_RED ===
MUTATION_LINES_REMOVED input=P0_STATE_UID kind=precheck_and_backstop n=2
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
P0_SECTION preregistered_inputs
P0_input name=P0_EXPECT_UID value=1000
/dev/stdin: line 373: P0_STATE_UID: unbound variable
ASSERT_UNMET input=P0_STATE_UID mutation=precheck_and_backstop raw_rc=1 polarity=RED
CASE_OK
CHECK_RC=0
=== P0_STATE_GID / precheck_only / expect_GREEN ===
MUTATION_LINES_REMOVED input=P0_STATE_GID kind=precheck_only n=1
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
/dev/stdin: line 290: P0_STATE_GID: preregistered numeric gid of the mtc-bridge service account is required
ASSERT_MET input=P0_STATE_GID mutation=precheck_only raw_rc=1 polarity=GREEN
CASE_OK
CHECK_RC=0
=== P0_STATE_GID / precheck_and_backstop / expect_RED ===
MUTATION_LINES_REMOVED input=P0_STATE_GID kind=precheck_and_backstop n=2
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_prereq lib=sourced bootstrap=ran run_id=qa-rp6 stage=p0 dir=/qa-rp6 leaf=/qa-rp6/p0.log
P0_SECTION preregistered_inputs
P0_input name=P0_EXPECT_UID value=1000
P0_input name=P0_STATE_UID value=999
/dev/stdin: line 374: P0_STATE_GID: unbound variable
ASSERT_UNMET input=P0_STATE_GID mutation=precheck_and_backstop raw_rc=1 polarity=RED
CASE_OK
CHECK_RC=0
C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS
```

Reading, stated exactly: `MUTATION_LINES_REMOVED … n=1` / `n=2` proves each
mutation removed the lines it claims to. With only the pre-check removed, the
backstop fires at the block's own line with the named message. With the backstop
removed as well, the block runs on past the missing input through two more
sections and only dies later — at the first *use* of the variable — with
`P0_STATE_UID: unbound variable`, an unnamed `set -u` error carrying no
`P0_STOP reason=` and no adjudicated rc 3. The assertion is therefore unmet on
message, not on rc: rc is 1 in both cases. That is precisely what the backstop
buys — a named, early, reasoned refusal instead of a bare shell error several
sections later — and it is why the GREEN case is evidence about the backstop.

## C13 R3 artefact measurements (real, computed in-session)

- Repaired `RP6-P0.sh` SHA-256: `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`
- Repaired `RP6-P0.sh` byte count: `55467`
- Pre-R3 baseline (the C13 commit `cbaf3ec8`, audited by Codex) SHA-256:
  `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B —
  re-derived in-session and matched the kickoff exactly before editing.
- `bash -n MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh` → rc 0,
  `BASH_N=PASS`.
- `git diff --stat` for the R3 repair: 34 insertions, 12 deletions, one file.

## C13 R3 explicit local limit

The complete P0 block still was not run: it needs the accepted RP0
library/bootstrap, Linux `/proc` namespace objects, the preregistered per-SHA
venv, `getent`/`systemctl` on PATH, and a reachable system manager, none of which
exist in this Git Bash environment. Harness 1 sources the extracted arm plus the
block's own top-level driver lines, never the whole block; harness 2 sources the
whole block but dies inside input validation, before any external P0 probe.
Both harnesses write QA-only files under `/tmp` (a `getent` fixture and the
extracted variants) — outside the repository, and no file the block itself
creates. No host was contacted, no network command was run, and no host file
content was printed.

# C13 round 4 — repair of re-audit finding 1 (`RP6_C13_REAUDIT_CODEX_2026-08-10.md`)

Implementer: Claude Opus 5, bounded final round under the T0 cap. All output below
was captured in this session in a local Git Bash `--noprofile --norc` process. No
host was contacted, no network command was run.

## C13 R4 — repair decision

- **Finding 1 (HIGH), fixed in the block.** `p0_resolve_passwd` no longer captures
  getent with a plain `$( … )`, which deletes trailing newlines and therefore made
  a newline-only rc-2 capture indistinguishable from a truly empty one. The capture
  now appends a sentinel byte inside the substitution and strips it afterwards, so
  the complete merged stream survives; `had_bytes` is decided on those preserved
  bytes BEFORE any normalization. A newline-only rc-2 capture is now
  `P0_PW_OUTCOME=error` with `P0_PW_DIAG=newline_only_capture_at_rc2`, so the caller
  emits `identity_unresolvable … rc 3` for both accounts. Two supporting details:
  getent sits on the left of `||` inside the substitution so an inherited `set -e`
  cannot kill the subshell before the sentinel is written, and its own rc is carried
  out by re-exiting the subshell with it (a bare `; printf x` would always yield
  rc 0). If the sentinel is nevertheless absent, the capture was truncated by
  something other than getent, its trailing bytes are unknown, and the outcome is
  `error` / `capture_sentinel_lost` — fail closed, never a no-match.
- **Behaviour preservation.** After the emptiness question is answered, `raw` is
  normalized back to the value plain command substitution used to produce (trailing
  newlines stripped), so the rc-0 full-record parse and every diagnostic string are
  byte-identical to the R3-audited behaviour. Harness 1 below re-runs all sixteen R3
  cases against the R4 bytes unchanged to prove that.
- **Finding 2 (MEDIUM), no repair.** The Lead adjudicated the extra committed
  provenance log as a Lead-side deviation added at commit time, not by the round-3
  implementer; recorded as accepted, out of this round's scope, untouched.
- **Scope of the same pattern elsewhere.** `p0_resolve_passwd` is the only site in
  the block that adjudicates rc 2 as a distinct outcome (a `2)` case arm occurs
  exactly once in the file). Every other capture site treats any non-zero rc as an
  error, and every emptiness test elsewhere — e.g. `p0_capture_numeric`'s
  `[ -n "$raw" ] || p0_stop identity_probe_empty` — fails CLOSED on an empty
  capture, so newline stripping there can only produce a STOP, never a false
  admission. No other site was changed.

## C13 R4 — D026 harness 1, extended with the newline-only rc-2 fixture

The R3 harness 1 verbatim, plus: a fourth source variant `prer4` (the committed R3
bytes `ef205e20…`, 55467 B, which the re-audit falsified), three newline-only rc-2
shim modes, and an explicit reproduction probe printing the auditor's own
`FALSE_NOMATCH_REPRODUCED` / `REQUIRED_ERROR_OUTCOME_PRESENT` markers. Polarity
still decides: a `RED` case fails the run if its assertion is MET.

```bash
set -Eeuo pipefail
cd /c/LAB/Tradingview_LAB_CLEAN
blk=MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
pre_rev=cbaf3ec8    # the C13 commit  = PRE-R3 bytes cfdb23b8..., 54109 B
r3_rev=8d2f25a5     # the R3 commit   = PRE-R4 bytes ef205e20..., 55467 B
w=/tmp/rp6qa_c13r4; rm -rf "$w"; mkdir -p "$w"

# ---- QA-only getent fixture (production pins an absolute getent from the inventory).
cat > "$w/getent_shim.sh" <<'SHIMEOF'
#!/usr/bin/env bash
key="${2:-}"
case "$key" in
    gatea)
        case "${SHIM_MODE:-}" in
            wrong_gatea_uid) printf 'gatea:x:4242:%s:a:/h:/s\n' "$(id -g)"; exit 0 ;;
            dup_gatea) printf 'gatea:x:%s:%s:a:/h:/s\ngatea:x:%s:%s:b:/h:/s\n' "$(id -u)" "$(id -g)" "$(id -u)" "$(id -g)"; exit 0 ;;
            gatea_rc2_diag) printf 'getent: nss module returned SERVBUSY for gatea\n' >&2; exit 2 ;;
            gatea_rc2_newline) printf '\n' >&2; exit 2 ;;
            *) printf 'gatea:x:%s:%s:gatea route login:/home/gatea:/bin/bash\n' "$(id -u)" "$(id -g)"; exit 0 ;;
        esac ;;
    mtc-bridge)
        case "${SHIM_MODE:-}" in
            wrong_mtc_gid) printf 'mtc-bridge:x:999:989:svc:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
            mtc_nomatch) exit 2 ;;
            mtc_rc2_diag) printf 'getent: sss_nss: connection to the name service timed out\n' >&2; exit 2 ;;
            mtc_rc2_partial) printf 'mtc-bridge:x:999\n'; exit 2 ;;
            mtc_rc2_newline) printf '\n' >&2; exit 2 ;;
            mtc_rc2_newlines3) printf '\n\n\n'; exit 2 ;;
            *) printf 'mtc-bridge:x:999:988:mtc-bridge service:/var/lib/mtc-bridge:/usr/sbin/nologin\n'; exit 0 ;;
        esac ;;
esac
exit 2
SHIMEOF
chmod +x "$w/getent_shim.sh"

# ---- the four source variants under test --------------------------------------
cp "$blk" "$w/src_repaired.sh"                                   # R4-repaired bytes
git show "$pre_rev:$blk" > "$w/src_prerepair.sh"                 # pre-R3 bytes  (F1 unfixed)
git show "$r3_rev:$blk"  > "$w/src_prer4.sh"                     # pre-R4 bytes  (newline gap unfixed)
awk '$0!="p0_resolve_accounts"' "$blk" > "$w/src_nocall.sh"      # MUTATION: production integration call deleted

# ---- extract the arm AND the block's own top-level driver ---------------------
# The driver lines are taken from the source bytes by exact whole-line match, so
# the block - not this harness - decides whether the arm runs at all. Nothing
# here calls p0_resolve_accounts.
extract() {
    {
        sed -n '/^p0_stop() {/p'                "$1"
        sed -n '/^p0_sanitize()/,/^}/p'         "$1"
        sed -n '/^p0_count_substr()/,/^}/p'     "$1"
        sed -n '/^p0_capture_numeric()/,/^}/p'  "$1"
        sed -n '/^p0_resolve_passwd()/,/^}/p'   "$1"
        sed -n '/^p0_resolve_accounts()/,/^}/p' "$1"
        awk '$0=="printf '\''P0_SECTION accounts\\n'\''" || $0=="p0_resolve_accounts"' "$1"
    } > "$2"
}
for v in repaired prerepair prer4 nocall; do extract "$w/src_$v.sh" "$w/funcs_$v.sh"; done
printf 'DRIVER_LINES repaired=%s prerepair=%s prer4=%s nocall=%s\n' \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_repaired.sh")" \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_prerepair.sh")" \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_prer4.sh")" \
    "$(grep -c '^p0_resolve_accounts$' "$w/funcs_nocall.sh")"

arm_out() {   # variant mode -> stdout = arm output, rc = arm rc
    SHIM_MODE="$2" \
    P0_GETENT="$w/getent_shim.sh" \
    P0_ID="$(command -v id)" \
    P0_EXPECT_UID="$(id -u)" \
    P0_STATE_UID=999 \
    P0_STATE_GID=988 \
    bash --noprofile --norc -c '
        set -Eeuo pipefail
        . "$1"
    ' _ "$w/funcs_$1.sh"
}

CASES=0
run_case() {  # variant mode want_rc want_subst polarity
    local variant="$1" mode="$2" want_rc="$3" want_subst="$4" polarity="$5" out rc=0 ok=0
    CASES=$(( CASES + 1 ))
    out="$(arm_out "$variant" "$mode")" || rc=$?
    printf -- '--- variant=%s mode=%s\n%s\nARM_RC=%s\n' "$variant" "${mode:-<none>}" "$out" "$rc"
    if [ "$rc" = "$want_rc" ] && case "$out" in *"$want_subst"*) true ;; *) false ;; esac; then ok=1; fi
    if [ "$ok" -eq 1 ]; then
        printf 'ASSERT_MET variant=%s mode=%s expected_rc=%s subst=[%s] polarity=%s\n' \
            "$variant" "${mode:-<none>}" "$want_rc" "$want_subst" "$polarity"
    else
        printf 'ASSERT_UNMET variant=%s mode=%s expected_rc=%s subst=[%s] polarity=%s\n' \
            "$variant" "${mode:-<none>}" "$want_rc" "$want_subst" "$polarity"
    fi
    # GREEN cases must meet the assertion; RED cases (mutated/older bytes) must NOT.
    case "$polarity:$ok" in
        GREEN:1|RED:0) printf 'CASE_OK\n'; return 0 ;;
        *)             printf 'CASE_BAD\n'; return 1 ;;
    esac
}

probe() {  # variant mode want_false_nomatch want_required_error -- the re-audit's own markers
    local variant="$1" mode="$2" want_f="$3" want_r="$4" out rc=0 f=no r=no
    CASES=$(( CASES + 1 ))
    out="$(arm_out "$variant" "$mode")" || rc=$?
    case "$out" in *"observed_numeric=absent"*) f=yes ;; esac
    case "$out" in *"identity_unresolvable account=mtc-bridge"*) r=yes ;; esac
    printf -- '--- probe variant=%s mode=%s\nFIXTURE=mtc-bridge_rc2_stderr_single_newline_byte\n%s\nARM_RC=%s\nFALSE_NOMATCH_REPRODUCED=%s\nREQUIRED_ERROR_OUTCOME_PRESENT=%s\n' \
        "$variant" "$mode" "$out" "$rc" "$f" "$r"
    if [ "$f" = "$want_f" ] && [ "$r" = "$want_r" ]; then
        printf 'PROBE_OK variant=%s expected_false_nomatch=%s expected_required_error=%s\n' "$variant" "$want_f" "$want_r"
        return 0
    fi
    printf 'PROBE_BAD variant=%s expected_false_nomatch=%s expected_required_error=%s\n' "$variant" "$want_f" "$want_r"
    return 1
}

overall=0
set +e
# === A. R4 bytes, block-driven: the pre-existing five cases (regression) =======
run_case repaired ''               0 'P0_account_admitted account=mtc-bridge numeric=999:988'            GREEN || overall=1
run_case repaired wrong_mtc_gid    3 'state_account_resolution_unexpected account=mtc-bridge'            GREEN || overall=1
run_case repaired mtc_nomatch      3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' GREEN || overall=1
run_case repaired wrong_gatea_uid  3 'identity_unexpected account=gatea'                                 GREEN || overall=1
run_case repaired dup_gatea        3 'identity_unresolvable account=gatea'                               GREEN || overall=1

# === B. the production integration call is deleted -> every arm assertion must fail
run_case nocall   ''               0 'P0_account_admitted account=mtc-bridge numeric=999:988'            RED   || overall=1
run_case nocall   wrong_mtc_gid    3 'state_account_resolution_unexpected account=mtc-bridge'            RED   || overall=1
run_case nocall   mtc_rc2_diag     3 'identity_unresolvable account=mtc-bridge'                          RED   || overall=1
run_case nocall   mtc_rc2_newline  3 'identity_unresolvable account=mtc-bridge'                          RED   || overall=1

# === C. F1: rc 2 carrying text is a lookup error, not a valid no-match ========
run_case repaired mtc_rc2_diag     3 'identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]' GREEN || overall=1
run_case repaired mtc_rc2_partial  3 'identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]'                                          GREEN || overall=1
run_case repaired gatea_rc2_diag   3 'identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]'                 GREEN || overall=1
run_case prerepair mtc_rc2_diag    3 'identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]' RED || overall=1
run_case prerepair mtc_rc2_partial 3 'identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]'                                          RED || overall=1
run_case prerepair gatea_rc2_diag  3 'identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]'                 RED || overall=1
run_case prerepair mtc_rc2_diag    3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' GREEN || overall=1

# === D. the valid no-match arm still works after both narrowings (regression) ==
run_case repaired mtc_nomatch      3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match' GREEN || overall=1

# === E. R4 finding 1: a newline-only rc-2 capture is an error, not a no-match ==
#  GREEN on R4 bytes ...
run_case repaired mtc_rc2_newline   3 'identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]' GREEN || overall=1
run_case repaired mtc_rc2_newlines3 3 'identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]' GREEN || overall=1
run_case repaired gatea_rc2_newline 3 'identity_unresolvable account=gatea detail=[newline_only_capture_at_rc2]'      GREEN || overall=1
#  ... and RED on the committed R3 bytes the re-audit falsified.
run_case prer4    mtc_rc2_newline   3 'identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]' RED || overall=1
run_case prer4    mtc_rc2_newlines3 3 'identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]' RED || overall=1
run_case prer4    gatea_rc2_newline 3 'identity_unresolvable account=gatea detail=[newline_only_capture_at_rc2]'      RED || overall=1
#  What the R3 bytes emit instead, recorded positively as the defect:
run_case prer4    mtc_rc2_newline   3 'state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent' GREEN || overall=1
#  The R3 bytes remain sound on the text-bearing rc-2 cases (the R3 repair is not
#  being undone by this round):
run_case prer4    mtc_rc2_diag      3 'identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]' GREEN || overall=1

# === F. the re-audit's own reproduction markers, both directions ===============
probe prer4    mtc_rc2_newline yes no  || overall=1
probe repaired mtc_rc2_newline no  yes || overall=1
set -e

if [ "$overall" -eq 0 ]; then
    printf 'C13_R4_ARM_QA_SUMMARY cases=%s result=PASS\n' "$CASES"
else
    printf 'C13_R4_ARM_QA_SUMMARY cases=%s result=FAIL\n' "$CASES"
    exit 1
fi
```

### C13 R4 — D026 harness 1 (extended), real output

Captured 2026-08-10, Git Bash, run as `sed -n '1159,1324p' SELF_QA_RP6.md | bash
--noprofile --norc` against working-tree bytes
`bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 B.
Process rc 0.

```text
DRIVER_LINES repaired=1 prerepair=1 prer4=1 nocall=0
--- variant=repaired mode=<none>
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=988 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_account_admitted account=mtc-bridge numeric=999:988 matches=prereg_state_uid_gid name=diagnostic_only
ARM_RC=0
ASSERT_MET variant=repaired mode=<none> expected_rc=0 subst=[P0_account_admitted account=mtc-bridge numeric=999:988] polarity=GREEN
CASE_OK
--- variant=repaired mode=wrong_mtc_gid
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_account account=mtc-bridge outcome=resolved uid=999 gid=989 name_diag=[mtc-bridge] via=pinned_getent_passwd
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=999:989 expected_numeric=999:988
ARM_RC=3
ASSERT_MET variant=repaired mode=wrong_mtc_gid expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_nomatch
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_nomatch expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent] polarity=GREEN
CASE_OK
--- variant=repaired mode=wrong_gatea_uid
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4242 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_STOP reason=identity_unexpected account=gatea observed_numeric=4242:4096 expected_numeric=4096:4096,prereg_uid=4096
ARM_RC=3
ASSERT_MET variant=repaired mode=wrong_gatea_uid expected_rc=3 subst=[identity_unexpected account=gatea] polarity=GREEN
CASE_OK
--- variant=repaired mode=dup_gatea
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea detail=[gatea:x:4096:4096:a:/h:/s gatea:x:4096:4096:b:/h:/s]
ARM_RC=3
ASSERT_MET variant=repaired mode=dup_gatea expected_rc=3 subst=[identity_unresolvable account=gatea] polarity=GREEN
CASE_OK
--- variant=nocall mode=<none>
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=<none> expected_rc=0 subst=[P0_account_admitted account=mtc-bridge numeric=999:988] polarity=RED
CASE_OK
--- variant=nocall mode=wrong_mtc_gid
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=wrong_mtc_gid expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge] polarity=RED
CASE_OK
--- variant=nocall mode=mtc_rc2_diag
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge] polarity=RED
CASE_OK
--- variant=nocall mode=mtc_rc2_newline
P0_SECTION accounts
ARM_RC=0
ASSERT_UNMET variant=nocall mode=mtc_rc2_newline expected_rc=3 subst=[identity_unresolvable account=mtc-bridge] polarity=RED
CASE_OK
--- variant=repaired mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_rc2_partial
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_partial expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]] polarity=GREEN
CASE_OK
--- variant=repaired mode=gatea_rc2_diag
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]
ARM_RC=3
ASSERT_MET variant=repaired mode=gatea_rc2_diag expected_rc=3 subst=[identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]] polarity=GREEN
CASE_OK
--- variant=prerepair mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]] polarity=RED
CASE_OK
--- variant=prerepair mode=mtc_rc2_partial
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=mtc_rc2_partial expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[mtc-bridge:x:999]] polarity=RED
CASE_OK
--- variant=prerepair mode=gatea_rc2_diag
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea rc=2 detail=getent_valid_no_match_for_route_login
ARM_RC=3
ASSERT_UNMET variant=prerepair mode=gatea_rc2_diag expected_rc=3 subst=[identity_unresolvable account=gatea detail=[getent: nss module returned SERVBUSY for gatea]] polarity=RED
CASE_OK
--- variant=prerepair mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=prerepair mode=mtc_rc2_diag expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_nomatch
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_nomatch expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_rc2_newline
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_newline expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]] polarity=GREEN
CASE_OK
--- variant=repaired mode=mtc_rc2_newlines3
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]
ARM_RC=3
ASSERT_MET variant=repaired mode=mtc_rc2_newlines3 expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]] polarity=GREEN
CASE_OK
--- variant=repaired mode=gatea_rc2_newline
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea detail=[newline_only_capture_at_rc2]
ARM_RC=3
ASSERT_MET variant=repaired mode=gatea_rc2_newline expected_rc=3 subst=[identity_unresolvable account=gatea detail=[newline_only_capture_at_rc2]] polarity=GREEN
CASE_OK
--- variant=prer4 mode=mtc_rc2_newline
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prer4 mode=mtc_rc2_newline expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]] polarity=RED
CASE_OK
--- variant=prer4 mode=mtc_rc2_newlines3
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_UNMET variant=prer4 mode=mtc_rc2_newlines3 expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]] polarity=RED
CASE_OK
--- variant=prer4 mode=gatea_rc2_newline
P0_SECTION accounts
P0_STOP reason=identity_unresolvable account=gatea rc=2 detail=getent_valid_no_match_for_route_login
ARM_RC=3
ASSERT_UNMET variant=prer4 mode=gatea_rc2_newline expected_rc=3 subst=[identity_unresolvable account=gatea detail=[newline_only_capture_at_rc2]] polarity=RED
CASE_OK
--- variant=prer4 mode=mtc_rc2_newline
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
ASSERT_MET variant=prer4 mode=mtc_rc2_newline expected_rc=3 subst=[state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent] polarity=GREEN
CASE_OK
--- variant=prer4 mode=mtc_rc2_diag
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]
ARM_RC=3
ASSERT_MET variant=prer4 mode=mtc_rc2_diag expected_rc=3 subst=[identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]] polarity=GREEN
CASE_OK
--- probe variant=prer4 mode=mtc_rc2_newline
FIXTURE=mtc-bridge_rc2_stderr_single_newline_byte
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
FALSE_NOMATCH_REPRODUCED=yes
REQUIRED_ERROR_OUTCOME_PRESENT=no
PROBE_OK variant=prer4 expected_false_nomatch=yes expected_required_error=no
--- probe variant=repaired mode=mtc_rc2_newline
FIXTURE=mtc-bridge_rc2_stderr_single_newline_byte
P0_SECTION accounts
P0_account account=gatea outcome=resolved uid=4096 gid=4096 name_diag=[gatea] via=pinned_getent_passwd
P0_account_admitted account=gatea numeric=4096:4096 matches=live_id_and_prereg_uid name=diagnostic_only
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]
ARM_RC=3
FALSE_NOMATCH_REPRODUCED=no
REQUIRED_ERROR_OUTCOME_PRESENT=yes
PROBE_OK variant=repaired expected_false_nomatch=no expected_required_error=yes
C13_R4_ARM_QA_SUMMARY cases=27 result=PASS
```

What the output establishes, line by line:

- `DRIVER_LINES repaired=1 prerepair=1 prer4=1 nocall=0` — the arm is still driven by
  the block's own top-level call in all three real variants, and the `nocall`
  mutation really removed it.
- Block A + D: all six R3 cases (normal resolution, wrong gid, wrong uid, duplicate
  record, and the true empty-capture valid no-match with its exact
  `observed_numeric=absent … detail=getent_valid_no_match` line) are unchanged on R4
  bytes. The byte-preserving capture did not disturb the rc-0 record parse — the
  shim emits records with a trailing newline, which the R4 normalization strips back
  to the audited shape.
- Block B: with the block's integration call deleted, all four arm assertions —
  including the new newline one — go `ASSERT_UNMET` at rc 0. The new case is killed
  by the same mutation as the rest, so it is evidence about the block, not about the
  harness.
- Block C: the R3 F1 result is intact. Text-bearing rc-2 captures give
  `identity_unresolvable … detail=[<the text>]` on R4 bytes and on the R3 bytes
  (`prer4 mtc_rc2_diag` GREEN), and still fail on pre-R3 bytes, which instead emit
  the false `observed_numeric=absent`.
- Block E: the re-audit's gap is closed and its RED half is preserved. On R4 bytes a
  one-newline stderr capture, a three-newline stdout capture, and the same fixture on
  `gatea` all yield `identity_unresolvable … detail=[newline_only_capture_at_rc2]`
  rc 3. On the committed R3 bytes the identical fixtures do NOT produce that outcome
  (`ASSERT_UNMET … polarity=RED`), and the defect is recorded positively: they emit
  `state_account_resolution_unexpected … observed_numeric=absent`.
- Block F: the auditor's own two markers, reproduced in both directions from real
  runs — R3 bytes `FALSE_NOMATCH_REPRODUCED=yes` /
  `REQUIRED_ERROR_OUTCOME_PRESENT=no`, R4 bytes `no` / `yes`.
- `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, process rc 0.

## C13 R4 — harness 2 re-run (no regression in the `:?` backstop)

Harness 2 was re-run unchanged against the R4 bytes:
`sed -n '942,1025p' SELF_QA_RP6.md | bash --noprofile --norc`, process rc 0, final
line `C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS` (both
`precheck_only` cases `ASSERT_MET` GREEN, both `precheck_and_backstop` cases
`ASSERT_UNMET` RED). The R4 edit is confined to the interior of
`p0_resolve_passwd`, so the input-validation section is untouched.

## C13 R4 artefact measurements (real, computed in-session)

- Repaired `RP6-P0.sh` SHA-256: `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`
- Repaired `RP6-P0.sh` byte count: `57441`
- Pre-R4 baseline (the R3 commit `8d2f25a5`) SHA-256:
  `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`, 55467 B —
  re-derived in-session and matched the re-audit exactly before editing.
- Pre-R3 baseline (the C13 commit `cbaf3ec8`) SHA-256:
  `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B.
- `bash -n MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh` → rc 0,
  `BASH_N=PASS`.
- `git diff --stat` for the R4 repair of the block: 36 insertions, 5 deletions, one
  file.

## C13 R4 explicit local limit

The complete P0 block still was not run, for the same reasons recorded for R3: it
needs the accepted RP0 library/bootstrap, Linux `/proc` namespace objects, the
preregistered per-SHA venv, `getent`/`systemctl` on PATH, and a reachable system
manager, none of which exist in this Git Bash environment. The newline-only fixture
is a QA shim, not the real `getent`; what is proved locally is the block's
adjudication of an rc-2 capture whose bytes are a newline, not that any particular
NSS module ever emits one. The `set -e`-safety of the capture was checked in this
same Git Bash under `set -Eeuo pipefail`; other shells and other bash versions on
the target host are covered structurally (getent on the left of `||`) and, if the
sentinel is ever lost anyway, by the fail-closed `capture_sentinel_lost` arm rather
than by a test. Harness files are written under `/tmp`, outside the repository. No
host was contacted, no network command was run, and no host file content was
printed.

## C13 R4 — status of the earlier C13 records in this file

The R3 harness-1 fence and its recorded output above were captured against the R3
bytes `ef205e20…` and remain the honest record of that round; they are SUPERSEDED
as current evidence by the extended harness 1 in this R4 section, which contains
every R3 case verbatim plus the newline-only fixture and runs against the R4 bytes.
The two pre-R3 C13 fences stay labelled SUPPLEMENTAL. Neither earlier section was
edited by this round.

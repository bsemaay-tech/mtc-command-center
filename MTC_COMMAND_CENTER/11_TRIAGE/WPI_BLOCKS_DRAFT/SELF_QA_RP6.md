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

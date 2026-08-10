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

# SELF-QA - RP7-WPI-RO rows 1-9 extension over repair round 9

Status: `ROWS-1-9-EXTENDED-PENDING-REAUDIT`

## Rows 1-9 D026 rebuild - executed block-code evidence

The earlier matrix in this section was rejected because it was produced by a
Python re-implementation of the B2/B4 logic. This rebuild replaces it completely:
the fence below extracts `RP7-WPI-RO.sh` minus only the terminal
`wpi_main "$@"` call, asserts the block identity, sources the extracted block
functions, and drives the block's own B2/B4 row functions under
`bash --noprofile --norc` with captured `systemctl show` fixture files and
fixture unit fragments. No Python re-implementation of the block logic is used;
`python3 -I -S` appears only where the block itself invokes it.

Real execution exposed a block defect in row 6: the parser capture was being
overwritten by `wpi_mount_guard_end` before it was read. `RP7-WPI-RO.sh` was
therefore changed in this rebuild to preserve `parser_rc`, read the parser
capture first, and only then close the mount guard. The final identity asserted
by the fence is `126182` bytes /
`8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85`.

Published extraction command:

```bash
cd /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

```bash
# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN
set -Eeuo pipefail
set -f
export LC_ALL=C
REPO=/mnt/c/LAB/Tradingview_LAB_CLEAN
BLOCK="$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh"
EXPECTED_BYTES=126182
EXPECTED_SHA=8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85
ROOT=/tmp/rp7_rows_1_9_rebuild_evidence
case "$ROOT" in /tmp/rp7_rows_1_9_rebuild_evidence) rm -rf "$ROOT" ;; *) printf 'HARNESS_ABORT unsafe_root=%s\n' "$ROOT"; exit 97 ;; esac
mkdir -p "$ROOT/logs"
cleanup() { case "$ROOT" in /tmp/rp7_rows_1_9_rebuild_evidence) rm -rf "$ROOT" ;; esac; }
trap cleanup EXIT
block_bytes=$(wc -c < "$BLOCK" | tr -d ' ')
block_sha=$(sha256sum "$BLOCK" | awk '{print $1}')
block_cr=$(tr -cd '\r' < "$BLOCK" | wc -c | tr -d ' ')
[ "$block_bytes" = "$EXPECTED_BYTES" ] || { printf 'HARNESS_BLOCK_ID_MISMATCH stage=before bytes=%s expected=%s\n' "$block_bytes" "$EXPECTED_BYTES"; exit 98; }
[ "$block_sha" = "$EXPECTED_SHA" ] || { printf 'HARNESS_BLOCK_ID_MISMATCH stage=before sha256=%s expected=%s\n' "$block_sha" "$EXPECTED_SHA"; exit 98; }
[ "$block_cr" = 0 ] || { printf 'HARNESS_BLOCK_ID_MISMATCH stage=before cr_bytes=%s expected=0\n' "$block_cr"; exit 98; }
bash -n "$BLOCK"
printf 'HARNESS_BLOCK_ID stage=before bytes=%s sha256=%s cr_bytes=%s bash_n=0\n' "$block_bytes" "$block_sha" "$block_cr"
EXTRACT="$ROOT/RP7-WPI-RO.defs.sh"
sed '$d' "$BLOCK" | sed '1s/^\xEF\xBB\xBF//' > "$EXTRACT"
bash -n "$EXTRACT"
if grep -q '^wpi_main "\$@"$' "$EXTRACT"; then printf 'HARNESS_EXTRACT_MISMATCH terminal_call_present=yes\n'; exit 98; fi
grep -q '^wpi_assert_b2_rows_1_7()' "$EXTRACT" || { printf 'HARNESS_EXTRACT_MISSING function=wpi_assert_b2_rows_1_7\n'; exit 98; }
grep -q '^wpi_assert_b4_rows_8_9()' "$EXTRACT" || { printf 'HARNESS_EXTRACT_MISSING function=wpi_assert_b4_rows_8_9\n'; exit 98; }
printf 'HARNESS_EXTRACT method=sed_drop_terminal_wpi_main_call source=RP7-WPI-RO.sh functions_invoked=wpi_assert_b2_rows_1_7,wpi_assert_fragment_has_no_install_section,wpi_assert_regular_digest,wpi_assert_b4_rows_8_9\n'
. "$EXTRACT"
trap - ERR
WPI_ENV=/usr/bin/env
WPI_TIMEOUT=/usr/bin/timeout
WPI_SHA256SUM=/usr/bin/sha256sum
WPI_PYTHON3=/usr/bin/python3
WPI_STAT=/usr/bin/stat
WPI_READLINK=/usr/bin/readlink
WPI_FIND=/usr/bin/find
WPI_SS=/usr/bin/ss
WPI_CURL=/usr/bin/curl
WPI_SYSTEMCTL="$ROOT/fake_systemctl"
WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b
WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b
WPI_STATE_DIR=/var/lib/mtc-bridge
WPI_LOG_DIR=/var/log/mtc-bridge
WPI_CONF_DIR=/etc/mtc-bridge
WPI_MAINPID=189813
WPI_SWEEP_BUDGET_S=120
WPI_ATTESTED_MOUNTINFO_SHA256=0000000000000000000000000000000000000000000000000000000000000000
WPI_UNIT_FRAGMENT="$ROOT/unit/mtc-bridge-first-start.service"
mkdir -p "$(dirname "$WPI_UNIT_FRAGMENT")"
cat > "$WPI_SYSTEMCTL" <<'SH'
#!/usr/bin/env bash
rc=0
[ ! -f systemctl.rc ] || IFS= read -r rc < systemctl.rc || rc=0
[ ! -f systemctl.stdout ] || cat systemctl.stdout
[ ! -f systemctl.stderr ] || cat systemctl.stderr >&2
exit "$rc"
SH
chmod 755 "$WPI_SYSTEMCTL"
make_fragment() {
    local variant="$1" target="${2:-3736}" path="$WPI_UNIT_FRAGMENT" size need
    : > "$path"
    case "$variant" in
        clean) printf '[Unit]\nDescription=RP7 rows 1-9 fixture\n[Service]\nExecStart=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python -m bridge.app\n' > "$path" ;;
        comment_decoy) printf '# [Install]\n[Unit]\nDescription=comment decoy\n[Service]\nExecStart=/bin/true\n' > "$path" ;;
        continued_decoy) printf '[Unit]\nDescription=continued \\\n[Install]\n[Service]\nExecStart=/bin/true\n' > "$path" ;;
        case_variant) printf '[Unit]\nDescription=case variant\n[install]\nWantedBy=multi-user.target\n[Service]\nExecStart=/bin/true\n' > "$path" ;;
        real_install) printf '[Unit]\nDescription=real install\n[Install]\nWantedBy=multi-user.target\n[Service]\nExecStart=/bin/true\n' > "$path" ;;
        nul) printf '[Unit]\nDescription=nul\n\0\n[Service]\nExecStart=/bin/true\n' > "$path" ;;
        same_size_wrong_digest) printf '[Unit]\nDescription=RP7 rows 1-9 wrong digest fixture\n[Service]\nExecStart=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python -m bridge.app\n' > "$path" ;;
        *) printf 'HARNESS_ABORT unknown_fragment_variant=%s\n' "$variant"; exit 97 ;;
    esac
    if [ "$variant" != nul ]; then
        size=$(wc -c < "$path" | tr -d ' ')
        [ "$size" -le "$target" ] || { printf 'HARNESS_ABORT fragment_too_large variant=%s size=%s target=%s\n' "$variant" "$size" "$target"; exit 97; }
        need=$(( target - size ))
        if [ "$need" -eq 1 ]; then printf '\n' >> "$path"
        elif [ "$need" -gt 1 ]; then printf '#' >> "$path"; head -c $(( need - 2 )) /dev/zero | tr '\0' 'x' >> "$path"; printf '\n' >> "$path"; fi
    fi
    chmod 0644 "$path"
}
fragment_sha() { sha256sum "$WPI_UNIT_FRAGMENT" | awk '{print $1}'; }
fragment_bytes() { wc -c < "$WPI_UNIT_FRAGMENT" | tr -d ' '; }
make_fragment clean 3736
CLEAN_FRAGMENT_SHA=$(fragment_sha)
CLEAN_FRAGMENT_BYTES=$(fragment_bytes)
[ "$CLEAN_FRAGMENT_BYTES" = 3736 ] || { printf 'HARNESS_ABORT clean_fragment_bytes=%s\n' "$CLEAN_FRAGMENT_BYTES"; exit 97; }
WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"
WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"
WPI_PROBE_SEQ=0
EV_DIR="$ROOT/attest/evidence"; mkdir -p "$EV_DIR"
WPI_CAP_OUT_FD=""; WPI_CAP_ERR_FD=""; WPI_CAP_BIND_PREFIX=""; WPI_CAP_BIND_REASON=""; WPI_CAP_BIND_RC_STYLE=""; WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""; WPI_MOUNT_GUARD_ACTIVE=no; WPI_MOUNT_SNAPSHOT_SEQ=0
wpi_capture_mountinfo_snapshot
attest_snapshot="$WPI_LINE"
wpi_build_mount_projection "$attest_snapshot" >/dev/null
WPI_ATTESTED_MOUNTINFO_SHA256="$WPI_MOUNT_PROJECTION_DIGEST"
printf 'HARNESS_ATTESTED_MOUNTINFO sha256=%s fixture_root=%s unit_fragment=%s clean_fragment_bytes=%s clean_fragment_sha256=%s\n' "$WPI_ATTESTED_MOUNTINFO_SHA256" "$ROOT" "$WPI_UNIT_FRAGMENT" "$CLEAN_FRAGMENT_BYTES" "$CLEAN_FRAGMENT_SHA"
write_b2_show() {
    local active="${1:-active}" nrestarts="${2:-0}" restart="${3:-no}" mainpid="${4:-189813}" load_state="${5:-loaded}" fragment="${6:-$WPI_UNIT_FRAGMENT}" dropins="${7:-}" exec_path="${8:-$WPI_VENV_ROOT/bin/python}" final_newline="${9:-yes}"
    {
        printf 'ActiveState=%s\n' "$active"
        [ "$nrestarts" = __DELETE__ ] || printf 'NRestarts=%s\n' "$nrestarts"
        printf 'Restart=%s\n' "$restart"
        printf 'MainPID=%s\n' "$mainpid"
        printf 'LoadState=%s\n' "$load_state"
        printf 'FragmentPath=%s\n' "$fragment"
        printf 'DropInPaths=%s\n' "$dropins"
        printf 'ExecStart={ path=%s ; argv[]=%s -m bridge.app ; ignore_errors=no }\n' "$exec_path" "$WPI_VENV_ROOT/bin/python"
        if [ "$final_newline" = yes ]; then printf 'WorkingDirectory=%s/IBKR_PAPER_BRIDGE\n' "$WPI_RELEASE_ROOT"; else printf 'WorkingDirectory=%s/IBKR_PAPER_BRIDGE' "$WPI_RELEASE_ROOT"; fi
    } > "$EV_DIR/systemctl.stdout"
    : > "$EV_DIR/systemctl.stderr"
    printf '0\n' > "$EV_DIR/systemctl.rc"
}
write_b4_show() {
    local private_tmp="${1:-yes}" protect_system="${2:-strict}" env_value="${3:-MTC_BRIDGE_START_MODE=credential_free_disarmed}" delete_protect="${4:-no}"
    {
        printf 'PrivateTmp=%s\n' "$private_tmp"
        [ "$delete_protect" = yes ] || printf 'ProtectSystem=%s\n' "$protect_system"
        printf 'NoNewPrivileges=yes\nRestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX\nCapabilityBoundingSet=\nReadWritePaths=/var/lib/mtc-bridge /var/log/mtc-bridge\nKillSignal=15\nKillMode=mixed\nTimeoutStopUSec=45s\nFinalKillSignal=9\n'
        printf 'Environment=%s\n' "$env_value"
    } > "$EV_DIR/systemctl.stdout"
    : > "$EV_DIR/systemctl.stderr"
    printf '0\n' > "$EV_DIR/systemctl.rc"
}
prepare_case() {
    local case_id="$1"
    EV_DIR="$ROOT/cases/$case_id/evidence"
    rm -rf "$ROOT/cases/$case_id"
    mkdir -p "$EV_DIR"
    WPI_PROBE_SEQ=0
    WPI_CAP_OUT=""; WPI_CAP_ERR=""; WPI_CAP_OUT_FD=""; WPI_CAP_ERR_FD=""; WPI_CAP_FD=""; WPI_CAP_FD_SOURCE=""
    WPI_CAP_BIND_PREFIX=""; WPI_CAP_BIND_REASON=""; WPI_CAP_BIND_RC_STYLE=""; WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""
    WPI_CAP_RC=0; WPI_CAP_ELAPSED_MS=0; WPI_READ_DIAG=""; WPI_READ_DIAG_FD=""; WPI_LEAF_FD=""
    WPI_MOUNT_GUARD_ACTIVE=no; WPI_MOUNT_SNAPSHOT_SEQ=0; WPI_SHOW_VALUES=(); WPI_SHOW_SEEN=()
}
run_case() {
    local row="$1" arm="$2" mutation="$3" kind="$4" expected_rc="$5" expected_line="$6" case_id="$7" body="$8" out err rc line
    out="$ROOT/logs/$case_id.stdout.txt"; err="$ROOT/logs/$case_id.stderr.txt"
    set +e
    ( trap 'wpi_on_err' ERR; set -Eeuo pipefail; eval "$body" ) > "$out" 2> "$err"
    rc=$?
    set -e
    if [ -s "$err" ]; then sed 's/^/HARNESS_CASE_STDERR /' "$err"; fi
    line=$(grep -F -m1 -- "$expected_line" "$out" || true)
    if [ "$rc" != "$expected_rc" ] || [ -z "$line" ]; then
        printf 'HARNESS_CASE_FAIL row=%s arm=%s mutation=%s expected_rc=%s actual_rc=%s expected_line=[%s]\n' "$row" "$arm" "$mutation" "$expected_rc" "$rc" "$expected_line"
        sed 's/^/HARNESS_CASE_STDOUT /' "$out"
        exit 96
    fi
    printf 'D026 row=%s arm=%s mutation=%s %s rc=%s line=%s\n' "$row" "$arm" "$mutation" "$kind" "$rc" "$line"
}
run_case 1 inactive 'ActiveState=inactive' RED 1 'B2_FAIL reason=unit_not_active state=inactive expected=active' r1_inactive 'prepare_case r1_inactive; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show inactive; wpi_assert_b2_rows_1_7'
run_case 1 inactive repaired_expected GREEN 0 'B2_active state=active source=system_manager_show property=ActiveState' r1_green 'prepare_case r1_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 1 manager_stop systemctl_show_rc_7 RED 3 'B2_STOP reason=system_manager_unreachable operation=show rc=7 detail=unit_query_nonzero diagnostic_file=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r1_manager_stop/evidence/ro.0001.b2_unit_show.stderr' r1_manager_stop 'prepare_case r1_manager_stop; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; : > "$EV_DIR/systemctl.stdout"; printf "manager unavailable\n" > "$EV_DIR/systemctl.stderr"; printf "7\n" > "$EV_DIR/systemctl.rc"; wpi_assert_b2_rows_1_7'
run_case 1 manager_stop repaired_expected GREEN 0 'B2_active state=active source=system_manager_show property=ActiveState' r1_manager_green 'prepare_case r1_manager_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 2 missing_property delete_NRestarts RED 3 'B2_STOP reason=unit_property_unreadable prop=NRestarts rc=0 detail=property_record_absent query=NRestarts' r2_missing 'prepare_case r2_missing; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active __DELETE__; wpi_assert_b2_rows_1_7'
run_case 2 missing_property repaired_expected GREEN 0 'B2_restart_count prop=NRestarts value=0' r2_missing_green 'prepare_case r2_missing_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 2 wrong_value NRestarts_2 RED 1 'B2_FAIL reason=nrestarts_nonzero value=2 expected=0' r2_wrong 'prepare_case r2_wrong; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 2; wpi_assert_b2_rows_1_7'
run_case 2 wrong_value repaired_expected GREEN 0 'B2_restart_count prop=NRestarts value=0' r2_wrong_green 'prepare_case r2_wrong_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 3 wrong_value Restart_on-failure RED 1 'B2_FAIL reason=restart_policy value=on-failure expected=no' r3_wrong 'prepare_case r3_wrong; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 on-failure; wpi_assert_b2_rows_1_7'
run_case 3 wrong_value repaired_expected GREEN 0 'B2_restart_policy prop=Restart value=no' r3_green 'prepare_case r3_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 4 wrong_value MainPID_190000 RED 1 'B2_FAIL reason=mainpid_changed value=190000 expected=189813' r4_wrong 'prepare_case r4_wrong; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 190000; wpi_assert_b2_rows_1_7'
run_case 4 wrong_value repaired_expected GREEN 0 'B2_mainpid prop=MainPID value=189813 continuity=preregistered' r4_green 'prepare_case r4_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 5 wrong_fragment FragmentPath_wrong RED 1 'B2_FAIL reason=unit_not_bound_to_candidate field=FragmentPath observed=[/tmp/comment-only.service] expected=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service' r5_fragment 'prepare_case r5_fragment; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 189813 loaded /tmp/comment-only.service; wpi_assert_b2_rows_1_7'
row5_green="B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=$WPI_UNIT_FRAGMENT dropins=empty working_directory=$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE exec_path=$WPI_VENV_ROOT/bin/python argv_sha_bound=yes"
run_case 5 wrong_fragment repaired_expected GREEN 0 "$row5_green" r5_fragment_green 'prepare_case r5_fragment_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 5 dropin_override DropInPaths_override_conf RED 1 'B2_FAIL reason=unit_not_bound_to_candidate field=DropInPaths observed=[/etc/systemd/system/mtc-bridge-first-start.service.d/override.conf] expected=empty' r5_dropin 'prepare_case r5_dropin; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 189813 loaded "$WPI_UNIT_FRAGMENT" /etc/systemd/system/mtc-bridge-first-start.service.d/override.conf; wpi_assert_b2_rows_1_7'
run_case 5 dropin_override repaired_expected GREEN 0 "$row5_green" r5_dropin_green 'prepare_case r5_dropin_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 5 wrong_execstart ExecStart_path_tmp_comment_only RED 1 'B2_FAIL reason=unit_not_bound_to_candidate field=ExecStart.path observed=[/tmp/comment-only] expected=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python' r5_exec 'prepare_case r5_exec; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 189813 loaded "$WPI_UNIT_FRAGMENT" "" /tmp/comment-only; wpi_assert_b2_rows_1_7'
run_case 5 wrong_execstart repaired_expected GREEN 0 "$row5_green" r5_exec_green 'prepare_case r5_exec_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 5 not_found LoadState_not-found RED 1 'B2_FAIL reason=unit_not_loaded' r5_notfound 'prepare_case r5_notfound; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 189813 not-found; wpi_assert_b2_rows_1_7'
run_case 5 not_found repaired_expected GREEN 0 "$row5_green" r5_notfound_green 'prepare_case r5_notfound_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
run_case 5 truncated_show missing_final_newline RED 3 'B2_STOP reason=system_manager_unreachable operation=show rc=0 detail=unterminated_final_record source=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r5_truncated/evidence/ro.0001.b2_unit_show.stdout' r5_truncated 'prepare_case r5_truncated; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show active 0 no 189813 loaded "$WPI_UNIT_FRAGMENT" "" "$WPI_VENV_ROOT/bin/python" no; wpi_assert_b2_rows_1_7'
run_case 5 truncated_show repaired_expected GREEN 0 "$row5_green" r5_truncated_green 'prepare_case r5_truncated_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; write_b2_show; wpi_assert_b2_rows_1_7'
row6_green="B2_fragment_install_section path=$WPI_UNIT_FRAGMENT install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed"
run_case 6 comment_decoy comment_contains_install CONTROL 0 "$row6_green" r6_comment 'prepare_case r6_comment; make_fragment comment_decoy 3736; WPI_UNIT_FRAGMENT_BYTES=$(fragment_bytes); WPI_UNIT_FRAGMENT_SHA256=$(fragment_sha); wpi_assert_fragment_has_no_install_section'
run_case 6 continued_decoy continued_line_then_install CONTROL 0 "$row6_green" r6_continued 'prepare_case r6_continued; make_fragment continued_decoy 3736; WPI_UNIT_FRAGMENT_BYTES=$(fragment_bytes); WPI_UNIT_FRAGMENT_SHA256=$(fragment_sha); wpi_assert_fragment_has_no_install_section'
run_case 6 case_variant lower_case_install CONTROL 0 "$row6_green" r6_case 'prepare_case r6_case; make_fragment case_variant 3736; WPI_UNIT_FRAGMENT_BYTES=$(fragment_bytes); WPI_UNIT_FRAGMENT_SHA256=$(fragment_sha); wpi_assert_fragment_has_no_install_section'
run_case 6 real_install real_Install_section RED 1 "B2_FAIL reason=install_section_present path=$WPI_UNIT_FRAGMENT" r6_real 'prepare_case r6_real; make_fragment real_install 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_fragment_has_no_install_section'
run_case 6 real_install repaired_expected GREEN 0 "$row6_green" r6_real_green 'prepare_case r6_real_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_fragment_has_no_install_section'
run_case 6 nul NUL_byte RED 3 "B2_STOP reason=fragment_unreadable_or_unparseable rc=0 path=$WPI_UNIT_FRAGMENT detail=nul_byte" r6_nul 'prepare_case r6_nul; make_fragment nul; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_fragment_has_no_install_section'
run_case 6 nul repaired_expected GREEN 0 "$row6_green" r6_nul_green 'prepare_case r6_nul_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_fragment_has_no_install_section'
row7_green="B2_digest path=$WPI_UNIT_FRAGMENT bytes=3736 sha256=$CLEAN_FRAGMENT_SHA binding=component_and_mount"
run_case 7 one_byte_short bytes_3735 RED 1 'B2_FAIL reason=unit_fragment_digest_mismatch observed_bytes=3735 expected_bytes=3736' r7_short 'prepare_case r7_short; make_fragment clean 3735; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path'
run_case 7 one_byte_short repaired_expected GREEN 0 "$row7_green" r7_short_green 'prepare_case r7_short_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path'
make_fragment same_size_wrong_digest 3736
WRONG_FRAGMENT_SHA=$(fragment_sha)
[ "$WRONG_FRAGMENT_SHA" != "$CLEAN_FRAGMENT_SHA" ] || { printf 'HARNESS_ABORT wrong_fragment_sha_equal=yes\n'; exit 97; }
run_case 7 same_size_wrong_digest bytes_3736_wrong_sha RED 1 "B2_FAIL reason=unit_fragment_digest_mismatch observed=$WRONG_FRAGMENT_SHA expected=$CLEAN_FRAGMENT_SHA" r7_wrongsha 'prepare_case r7_wrongsha; make_fragment same_size_wrong_digest 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path'
run_case 7 same_size_wrong_digest repaired_expected GREEN 0 "$row7_green" r7_wrongsha_green 'prepare_case r7_wrongsha_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path'
run_case 7 unreadable chmod_000_as_nobody RED 3 "B2_STOP reason=fragment_unreadable path=$WPI_UNIT_FRAGMENT rc=1 detail=sha256sum_failed diagnostic_file=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r7_unreadable/evidence/ro.0016.sha256.stderr" r7_unreadable 'prepare_case r7_unreadable; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; chmod 000 "$WPI_UNIT_FRAGMENT"; chmod 777 "$EV_DIR"; child="$ROOT/cases/r7_unreadable/child.sh"; cat > "$child" <<SH
#!/usr/bin/env bash
set -Eeuo pipefail
set -f
export LC_ALL=C
. "$EXTRACT"
trap '"'"'wpi_on_err'"'"' ERR
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SHA256SUM=/usr/bin/sha256sum; WPI_PYTHON3=/usr/bin/python3; WPI_STAT=/usr/bin/stat; WPI_READLINK=/usr/bin/readlink; WPI_FIND=/usr/bin/find; WPI_SS=/usr/bin/ss; WPI_CURL=/usr/bin/curl; WPI_SYSTEMCTL="$WPI_SYSTEMCTL"
WPI_RELEASE_ROOT=$WPI_RELEASE_ROOT; WPI_VENV_ROOT=$WPI_VENV_ROOT; WPI_STATE_DIR=$WPI_STATE_DIR; WPI_LOG_DIR=$WPI_LOG_DIR; WPI_CONF_DIR=$WPI_CONF_DIR; WPI_MAINPID=189813; WPI_SWEEP_BUDGET_S=120
WPI_UNIT_FRAGMENT="$WPI_UNIT_FRAGMENT"; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; WPI_ATTESTED_MOUNTINFO_SHA256="$WPI_ATTESTED_MOUNTINFO_SHA256"; EV_DIR="$EV_DIR"
WPI_PROBE_SEQ=0; WPI_CAP_OUT=""; WPI_CAP_ERR=""; WPI_CAP_OUT_FD=""; WPI_CAP_ERR_FD=""; WPI_CAP_FD=""; WPI_CAP_FD_SOURCE=""; WPI_CAP_BIND_PREFIX=""; WPI_CAP_BIND_REASON=""; WPI_CAP_BIND_RC_STYLE=""; WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""; WPI_CAP_RC=0; WPI_CAP_ELAPSED_MS=0; WPI_READ_DIAG=""; WPI_READ_DIAG_FD=""; WPI_LEAF_FD=""; WPI_MOUNT_GUARD_ACTIVE=no; WPI_MOUNT_SNAPSHOT_SEQ=0
wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path
SH
chmod 755 "$child"; set +e; runuser -u nobody -- bash --noprofile --norc "$child"; rc=$?; set -e; chmod 0644 "$WPI_UNIT_FRAGMENT"; exit "$rc"'
run_case 7 unreadable repaired_expected GREEN 0 "$row7_green" r7_unreadable_green 'prepare_case r7_unreadable_green; make_fragment clean 3736; WPI_UNIT_FRAGMENT_BYTES="$CLEAN_FRAGMENT_BYTES"; WPI_UNIT_FRAGMENT_SHA256="$CLEAN_FRAGMENT_SHA"; wpi_assert_regular_digest B2 unit_fragment_absent unit_fragment_digest_mismatch "$WPI_UNIT_FRAGMENT" "$WPI_UNIT_FRAGMENT_BYTES" "$WPI_UNIT_FRAGMENT_SHA256" fragment unit_fragment_object_unexpected with_path'
run_case 8 mismatch PrivateTmp_no RED 1 'B4_FAIL reason=property_mismatch prop=PrivateTmp observed=[no] expected=[yes]' r8_mismatch 'prepare_case r8_mismatch; write_b4_show no; wpi_assert_b4_rows_8_9'
run_case 8 mismatch repaired_expected GREEN 0 'B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1' r8_mismatch_green 'prepare_case r8_mismatch_green; write_b4_show; wpi_assert_b4_rows_8_9'
run_case 8 missing_property delete_ProtectSystem RED 3 'B4_STOP reason=unit_property_unreadable prop=ProtectSystem rc=0 detail=property_record_absent query=ProtectSystem' r8_missing 'prepare_case r8_missing; write_b4_show yes strict MTC_BRIDGE_START_MODE=credential_free_disarmed yes; wpi_assert_b4_rows_8_9'
run_case 8 missing_property repaired_expected GREEN 0 'B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1' r8_missing_green 'prepare_case r8_missing_green; write_b4_show; wpi_assert_b4_rows_8_9'
run_case 9 duplicate two_start_mode_assignments RED 1 'B4_FAIL reason=start_mode_missing_or_altered observed=count=2 observed_sha256=' r9_duplicate 'prepare_case r9_duplicate; write_b4_show yes strict "MTC_BRIDGE_START_MODE=credential_free_disarmed MTC_BRIDGE_START_MODE=credential_free_disarmed"; wpi_assert_b4_rows_8_9'
run_case 9 duplicate repaired_expected GREEN 0 'B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1' r9_duplicate_green 'prepare_case r9_duplicate_green; write_b4_show; wpi_assert_b4_rows_8_9'
run_case 9 substring different_variable_contains_token RED 1 'B4_FAIL reason=start_mode_missing_or_altered observed=count=0 observed_sha256=' r9_substring 'prepare_case r9_substring; write_b4_show yes strict "OTHER_MTC_BRIDGE_START_MODE=credential_free_disarmed"; wpi_assert_b4_rows_8_9'
run_case 9 substring repaired_expected GREEN 0 'B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1' r9_substring_green 'prepare_case r9_substring_green; write_b4_show; wpi_assert_b4_rows_8_9'
run_case 9 quoted quoted_assignment CONTROL 0 'B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1' r9_quoted 'prepare_case r9_quoted; write_b4_show yes strict "\"MTC_BRIDGE_START_MODE=credential_free_disarmed\""; wpi_assert_b4_rows_8_9'
for cid in r8_mismatch_green r8_missing_green; do
    count=$(grep -c '^B4_property ' "$ROOT/logs/$cid.stdout.txt")
    [ "$count" = 10 ] || { printf 'HARNESS_CASE_FAIL case=%s expected_b4_property_count=10 actual=%s\n' "$cid" "$count"; exit 96; }
    printf 'D026_CONTROL row=8 case=%s executed_B4_property_lines=%s\n' "$cid" "$count"
done
after_bytes=$(wc -c < "$BLOCK" | tr -d ' ')
after_sha=$(sha256sum "$BLOCK" | awk '{print $1}')
after_cr=$(tr -cd '\r' < "$BLOCK" | wc -c | tr -d ' ')
[ "$after_bytes" = "$EXPECTED_BYTES" ] && [ "$after_sha" = "$EXPECTED_SHA" ] && [ "$after_cr" = 0 ] || { printf 'HARNESS_BLOCK_ID_MISMATCH stage=after bytes=%s sha256=%s cr_bytes=%s\n' "$after_bytes" "$after_sha" "$after_cr"; exit 98; }
printf 'HARNESS_BLOCK_ID stage=after bytes=%s sha256=%s cr_bytes=%s bash_n=0\n' "$after_bytes" "$after_sha" "$after_cr"
printf 'D026_SUMMARY rows=1-9 red_green_pairs=20 controls=4 result=PASS instrument=RP7-WPI-RO.sh extracted_block_functions=yes block_logic_reimplemented=no\n'
# RP7_ROWS_1_9_REBUILD_FENCE_END
```

Executed transcript from the published extraction command:

```text
HARNESS_BLOCK_ID stage=before bytes=126182 sha256=8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85 cr_bytes=0 bash_n=0
HARNESS_EXTRACT method=sed_drop_terminal_wpi_main_call source=RP7-WPI-RO.sh functions_invoked=wpi_assert_b2_rows_1_7,wpi_assert_fragment_has_no_install_section,wpi_assert_regular_digest,wpi_assert_b4_rows_8_9
HARNESS_ATTESTED_MOUNTINFO sha256=78388f0d1e330a9e2f49700f241d10c96c9df704f8dd99a15e3b01edb98b1e15 fixture_root=/tmp/rp7_rows_1_9_rebuild_evidence unit_fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service clean_fragment_bytes=3736 clean_fragment_sha256=8eec04c5ec03de14e53ed3188396c9df1e87eb248e4abf63be57aabfa86eaf49
D026 row=1 arm=inactive mutation=ActiveState=inactive RED rc=1 line=B2_FAIL reason=unit_not_active state=inactive expected=active
D026 row=1 arm=inactive mutation=repaired_expected GREEN rc=0 line=B2_active state=active source=system_manager_show property=ActiveState
D026 row=1 arm=manager_stop mutation=systemctl_show_rc_7 RED rc=3 line=B2_STOP reason=system_manager_unreachable operation=show rc=7 detail=unit_query_nonzero diagnostic_file=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r1_manager_stop/evidence/ro.0001.b2_unit_show.stderr
D026 row=1 arm=manager_stop mutation=repaired_expected GREEN rc=0 line=B2_active state=active source=system_manager_show property=ActiveState
D026 row=2 arm=missing_property mutation=delete_NRestarts RED rc=3 line=B2_STOP reason=unit_property_unreadable prop=NRestarts rc=0 detail=property_record_absent query=NRestarts
D026 row=2 arm=missing_property mutation=repaired_expected GREEN rc=0 line=B2_restart_count prop=NRestarts value=0
D026 row=2 arm=wrong_value mutation=NRestarts_2 RED rc=1 line=B2_FAIL reason=nrestarts_nonzero value=2 expected=0
D026 row=2 arm=wrong_value mutation=repaired_expected GREEN rc=0 line=B2_restart_count prop=NRestarts value=0
D026 row=3 arm=wrong_value mutation=Restart_on-failure RED rc=1 line=B2_FAIL reason=restart_policy value=on-failure expected=no
D026 row=3 arm=wrong_value mutation=repaired_expected GREEN rc=0 line=B2_restart_policy prop=Restart value=no
D026 row=4 arm=wrong_value mutation=MainPID_190000 RED rc=1 line=B2_FAIL reason=mainpid_changed value=190000 expected=189813
D026 row=4 arm=wrong_value mutation=repaired_expected GREEN rc=0 line=B2_mainpid prop=MainPID value=189813 continuity=preregistered
D026 row=5 arm=wrong_fragment mutation=FragmentPath_wrong RED rc=1 line=B2_FAIL reason=unit_not_bound_to_candidate field=FragmentPath observed=[/tmp/comment-only.service] expected=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service
D026 row=5 arm=wrong_fragment mutation=repaired_expected GREEN rc=0 line=B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service dropins=empty working_directory=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE exec_path=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python argv_sha_bound=yes
D026 row=5 arm=dropin_override mutation=DropInPaths_override_conf RED rc=1 line=B2_FAIL reason=unit_not_bound_to_candidate field=DropInPaths observed=[/etc/systemd/system/mtc-bridge-first-start.service.d/override.conf] expected=empty
D026 row=5 arm=dropin_override mutation=repaired_expected GREEN rc=0 line=B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service dropins=empty working_directory=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE exec_path=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python argv_sha_bound=yes
D026 row=5 arm=wrong_execstart mutation=ExecStart_path_tmp_comment_only RED rc=1 line=B2_FAIL reason=unit_not_bound_to_candidate field=ExecStart.path observed=[/tmp/comment-only] expected=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python
D026 row=5 arm=wrong_execstart mutation=repaired_expected GREEN rc=0 line=B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service dropins=empty working_directory=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE exec_path=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python argv_sha_bound=yes
D026 row=5 arm=not_found mutation=LoadState_not-found RED rc=1 line=B2_FAIL reason=unit_not_loaded
D026 row=5 arm=not_found mutation=repaired_expected GREEN rc=0 line=B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service dropins=empty working_directory=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE exec_path=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python argv_sha_bound=yes
D026 row=5 arm=truncated_show mutation=missing_final_newline RED rc=3 line=B2_STOP reason=system_manager_unreachable operation=show rc=0 detail=unterminated_final_record source=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r5_truncated/evidence/ro.0001.b2_unit_show.stdout
D026 row=5 arm=truncated_show mutation=repaired_expected GREEN rc=0 line=B2_unit_binding unit=mtc-bridge-first-start.service load_state=loaded fragment=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service dropins=empty working_directory=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE exec_path=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python argv_sha_bound=yes
D026 row=6 arm=comment_decoy mutation=comment_contains_install CONTROL rc=0 line=B2_fragment_install_section path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
D026 row=6 arm=continued_decoy mutation=continued_line_then_install CONTROL rc=0 line=B2_fragment_install_section path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
D026 row=6 arm=case_variant mutation=lower_case_install CONTROL rc=0 line=B2_fragment_install_section path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
D026 row=6 arm=real_install mutation=real_Install_section RED rc=1 line=B2_FAIL reason=install_section_present path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service
D026 row=6 arm=real_install mutation=repaired_expected GREEN rc=0 line=B2_fragment_install_section path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
D026 row=6 arm=nul mutation=NUL_byte RED rc=3 line=B2_STOP reason=fragment_unreadable_or_unparseable rc=0 path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service detail=nul_byte
D026 row=6 arm=nul mutation=repaired_expected GREEN rc=0 line=B2_fragment_install_section path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
D026 row=7 arm=one_byte_short mutation=bytes_3735 RED rc=1 line=B2_FAIL reason=unit_fragment_digest_mismatch observed_bytes=3735 expected_bytes=3736
D026 row=7 arm=one_byte_short mutation=repaired_expected GREEN rc=0 line=B2_digest path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service bytes=3736 sha256=8eec04c5ec03de14e53ed3188396c9df1e87eb248e4abf63be57aabfa86eaf49 binding=component_and_mount
D026 row=7 arm=same_size_wrong_digest mutation=bytes_3736_wrong_sha RED rc=1 line=B2_FAIL reason=unit_fragment_digest_mismatch observed=8de3d83e3be94a8d25db0b46bde93fd58b5b8473fe5f71aeaae157fa2cf5cf48 expected=8eec04c5ec03de14e53ed3188396c9df1e87eb248e4abf63be57aabfa86eaf49
D026 row=7 arm=same_size_wrong_digest mutation=repaired_expected GREEN rc=0 line=B2_digest path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service bytes=3736 sha256=8eec04c5ec03de14e53ed3188396c9df1e87eb248e4abf63be57aabfa86eaf49 binding=component_and_mount
D026 row=7 arm=unreadable mutation=chmod_000_as_nobody RED rc=3 line=B2_STOP reason=fragment_unreadable path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service rc=1 detail=sha256sum_failed diagnostic_file=/tmp/rp7_rows_1_9_rebuild_evidence/cases/r7_unreadable/evidence/ro.0016.sha256.stderr
D026 row=7 arm=unreadable mutation=repaired_expected GREEN rc=0 line=B2_digest path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service bytes=3736 sha256=8eec04c5ec03de14e53ed3188396c9df1e87eb248e4abf63be57aabfa86eaf49 binding=component_and_mount
D026 row=8 arm=mismatch mutation=PrivateTmp_no RED rc=1 line=B4_FAIL reason=property_mismatch prop=PrivateTmp observed=[no] expected=[yes]
D026 row=8 arm=mismatch mutation=repaired_expected GREEN rc=0 line=B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
D026 row=8 arm=missing_property mutation=delete_ProtectSystem RED rc=3 line=B4_STOP reason=unit_property_unreadable prop=ProtectSystem rc=0 detail=property_record_absent query=ProtectSystem
D026 row=8 arm=missing_property mutation=repaired_expected GREEN rc=0 line=B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
D026 row=9 arm=duplicate mutation=two_start_mode_assignments RED rc=1 line=B4_FAIL reason=start_mode_missing_or_altered observed=count=2 observed_sha256=e9cc545dfb074abf6ff63c26a42b6139c12f714e3b20bb87ba31283ceba1b7de
D026 row=9 arm=duplicate mutation=repaired_expected GREEN rc=0 line=B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
D026 row=9 arm=substring mutation=different_variable_contains_token RED rc=1 line=B4_FAIL reason=start_mode_missing_or_altered observed=count=0 observed_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
D026 row=9 arm=substring mutation=repaired_expected GREEN rc=0 line=B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
D026 row=9 arm=quoted mutation=quoted_assignment CONTROL rc=0 line=B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
D026_CONTROL row=8 case=r8_mismatch_green executed_B4_property_lines=10
D026_CONTROL row=8 case=r8_missing_green executed_B4_property_lines=10
HARNESS_BLOCK_ID stage=after bytes=126182 sha256=8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85 cr_bytes=0 bash_n=0
D026_SUMMARY rows=1-9 red_green_pairs=20 controls=4 result=PASS instrument=RP7-WPI-RO.sh extracted_block_functions=yes block_logic_reimplemented=no
```

Round 9 answers the Codex T0 part-B re-audit of the round-8 bytes
(`RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md`, BLOCK, five findings). Everything below ran
locally in **Git Bash (MSYS2)** on the workstation. It made no SSH/SCP call, opened no
network connection, contacted no staging host, minted no RUNID, and changed no repository
file outside the round-9 deliverables. Fixture writes were confined to `mktemp` directories
under `/tmp` whose prefix was checked before recursive removal.

**Read finding 1 first: the round-6 residual came due, and the reason is the one sentence
this round exists to absorb - an accurate disclosure is not a safety control.** Round 6
found that `ro.status.body` was create-once allocated and then handed to curl, to the digest
and to the parser by NAME, called closing it "a design change to the row-20 probe, not a
repair", and wrote the residual down. Round 8 repeated the note. Codex then executed both
halves of what the note admitted: a hard link at that name made curl overwrite an object
OUTSIDE the evidence tree at capture rc 0, and a replacement of that name between the digest
and the parser turned a child-produced ARMED body into an accepting DISARMED result whose
line carried the ARMED body's digest. The note was true and the block's own unqualified
sentences - `No host object outside that tree is changed`, `rows_10_23_read_only_predicates`
- were false beside it, inside rows 20-21 where the rows 10-19 scope boundary does not
reach. Round 9 makes the design change: curl writes to a duplicate of the creating
descriptor and the parser reads a descriptor derived from that same open before the child
exists, so no name is resolved on either side.

The other four findings are the same shape one level down - **a claim printed beside a fact
that does not support it**. F2 printed a caller-supplied `rc=0` literal for a child that had
returned 7. F3 attributed a diagnostic to the bounding wrapper on a stream the bounded body
could also write. F4 equated two counts and called it a one-to-one mapping. F5 emitted a row
STOP without the `detail` field the draft declares for it.

Two rules are in force from this round on, and every arm below is built to them:

1. **A carried fence changes only with a stated reason and a per-change discriminating-power
   argument.** Every change to a carried body is named in the section that carries it, and
   for each one the answer to "what input used to fail here, and does it still fail?" is
   given. Where the answer needed executing rather than asserting, it was executed: the
   round-8 fence runs the round-7 assertion and the round-8 assertion over the same three
   outputs and prints which accepts which (`ASSERTION_POWER`).
2. **Never justify a change by a claim about the old code without verifying it.** The false
   sentence round 7 wrote is corrected in `RP7_REPAIR_R7_REPORT.md` and restated correctly
   in the carried round-6 fence, and the executed matrix above is the verification the
   original claim never had.

The three standing disciplines from earlier rounds are unchanged:

1. **The RED is the audited artefact.** Every block arm runs twice - once against the frozen
   round-8 blob, materialised by `git cat-file blob bb8546e6:...` and re-derived inside the
   fence to 99903 B / `11621044...141a4`, and once against the repaired worktree file. The
   fence asserts both identities, both CR counts and both `bash -n` results before any arm
   runs. The F3 arms do the same for the published command *text*, RED being the round-8
   document's command extracted from the same commit. Each carried fence keeps its own
   older RED, so the round-8 fence still measures round 7, the round-7 fence round 6, and so
   on: a repair is not allowed to un-fix an earlier one.
2. **Every finding carries its own no-weakening control.** A repair that turns a
   substitutable write or read into a bound one is only correct if unsubstituted input still
   reaches the verdict it reached before: a clean `200` with a clean DISARMED body and a
   clean `net:[100]` must still be accepting on both subjects, and a deviant ARMED body must
   still FAIL on both; a bind failure after a child that really returned 0 must still print
   `rc=0`; a real kill-after must still be classified as a timeout; and a capture caller that
   preregisters no inability token of its own must still fail closed on the generic one.
3. **The published command can attribute what it reports, on a channel the reported-on
   party cannot write.** Each of the six wrappers runs with `--verbose`, and round 9 splits
   the two streams that round 8 merged: the bounded body's stderr goes to its own named file
   and the wrapper's stderr goes into an unnamed pipe read straight into a shell variable,
   which the body has no descriptor for and no name for. An rc of 137 is called this
   command's own kill-after event only when THAT stream recorded sending KILL. The bound the
   result line states is the one the wrappers actually enforce, and the line says in as many
   words that the command as a whole is unbounded.

## Exact command

The command selects each fenced body by the unique markers that open and close that body,
and stops at the closing marker. The marker text inside the command cannot re-open either
range: a marker only matches at the start of a line, and these lines start with `sed`.

Each fence runs under an explicit `timeout` bound of **900 s** with a **30 s kill grace**,
and the command's own rc is the rc of the fences: any nonzero fence makes the whole command
exit nonzero, and a fence stopped at its bound is reported as a distinct `timeout` result
rather than as a failure of the assertions.

Round 6 got the arithmetic and one of the two timeout outcomes wrong, and Codex executed
both errors (round-6 part B finding 4). `timeout --signal=TERM --kill-after=30s` has **two**
terminal outcomes, not one: a body that dies on TERM exits **124**, and a body that ignores
TERM and is killed after the grace exits **137**. Round 6 recognised only 124, so a fence
killed after the grace was reported as `fence_failed` - an assertion failure that never
happened. Both are now classified as timeouts and distinguished from each other by `kind=`,
and the command exits with the fence's own 124 or 137 rather than 1. One residual is stated
rather than claimed away: 137 is `SIGKILL`, so a fence body killed by something other than
this command's own kill-after grace is indistinguishable from inside the command and is
reported the same way.

Round 7 said `3720` "is an upper bound no execution of this command can exceed" and put
`aggregate_enforced_by=sequential_per_fence_bounds` on the result line. Codex round-7 part B
finding 3 executed the counter-example: a FIFO in place of this document makes the command
block in its own `sed` extraction, before the first wrapper starts, and an independent 3 s
timeout had to stop it. The six `timeout` calls bound six fence CALLS; they do not bound
the extractions, the `sha256sum`, the `wc -c` or the shell's own overhead, and no wrapper
encloses the command as a whole. **This round states only what is enforced.** Each fence runs
under `900 s` with a `30 s` kill grace; `6 * (900 + 30) = 5580` is therefore the
**fence-timeout budget**, and the result line says `fence_timeout_budget_s=5580
whole_command_bound=none prelude_bounded=no` instead of naming an enforcer that does not
exist. No outer wrapper is added: it would bound the same quantity a second time while
discarding the per-fence rcs the classification depends on, and the honest statement costs
nothing. Renaming the field would not have been enough on its own - round 7's error was
asserting enforcement, not choosing a poor word for it.

**Rc 137 is attributed on a stream the bounded body cannot write.** Round 7 printed
`kind=killed_after_grace` for every fence rc of 137, and Codex showed
`timeout ... bash -c 'exit 137'` finishing in about a second and being labelled that way:
the classifier saw only a number. Round 8 added `--verbose` and grepped the wrapper's
diagnostic - but the wrapper and the body it bounds shared one stderr file, so a body that
printed `timeout: sending signal KILL to command` and exited 137 was still called this
wrapper's kill-after event (Codex round-9 part B finding 3). Round 9 separates the two
writers. Each wrapper's own stderr goes into a command substitution - an unnamed pipe read
straight into `<FENCE>_W` - while the bounded body's stderr is redirected to its own file by
the `sh -c` shim BEFORE it execs the body:

    <FENCE>_W=$(timeout --verbose ... sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' <body> <body-err> 2>&1 1>&3)

The body therefore has fd 1 (the command's stdout, restored through fd 3), fd 2 (its own
named file), and **no descriptor and no name for the wrapper's stream**. A 137 is called
`killed_after_grace` only when that variable holds `sending signal KILL to command`; a 137
without it is `kind=sigkill_not_from_this_wrapper`, is **not** a timeout, and exits 1. Both
streams are echoed to stderr - the body's by `cat`, the wrapper's by `WRAPPER_STREAM` lines -
so nothing is hidden by being separated. What this still does **not** establish is unchanged
from round 8: a body killed by something else *while* the wrapper was also killing it is
reported as a kill-after event.

```bash
# RP7_EXACT_COMMAND_BEGIN
cd /c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_R9_FENCE_BEGIN$/,/^# RP7_R9_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r9-fence-body.sh
sed -n '/^# RP7_R8_FENCE_BEGIN$/,/^# RP7_R8_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r8-fence-body.sh
sed -n '/^# RP7_R7_FENCE_BEGIN$/,/^# RP7_R7_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r7-fence-body.sh
sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r6-fence-body.sh
sed -n '/^# RP7_QA_FENCE_BEGIN$/,/^# RP7_QA_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r5-fence-body.sh
sed -n '/^# RP7_R4_FENCE_BEGIN$/,/^# RP7_R4_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r4-fence-body.sh
sha256sum /tmp/rp7-r9-fence-body.sh /tmp/rp7-r8-fence-body.sh /tmp/rp7-r7-fence-body.sh /tmp/rp7-r6-fence-body.sh /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
wc -c /tmp/rp7-r9-fence-body.sh /tmp/rp7-r8-fence-body.sh /tmp/rp7-r7-fence-body.sh /tmp/rp7-r6-fence-body.sh /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
exec 3>&1
R9_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r9-fence-body.sh /tmp/rp7-r9-body.err 2>&1 1>&3); R9=$?
R8_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r8-fence-body.sh /tmp/rp7-r8-body.err 2>&1 1>&3); R8=$?
R7_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r7-fence-body.sh /tmp/rp7-r7-body.err 2>&1 1>&3); R7=$?
R6_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r6-fence-body.sh /tmp/rp7-r6-body.err 2>&1 1>&3); R6=$?
R5_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r5-fence-body.sh /tmp/rp7-r5-body.err 2>&1 1>&3); R5=$?
R4_W=$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' /tmp/rp7-r4-fence-body.sh /tmp/rp7-r4-body.err 2>&1 1>&3); R4=$?
cat /tmp/rp7-r9-body.err /tmp/rp7-r8-body.err /tmp/rp7-r7-body.err /tmp/rp7-r6-body.err /tmp/rp7-r5-body.err /tmp/rp7-r4-body.err >&2
printf 'R9_FENCE_RC=%s\nR8_FENCE_RC=%s\nR7_FENCE_RC=%s\nR6_FENCE_RC=%s\nR5_FENCE_RC=%s\nR4_FENCE_RC=%s\n' "$R9" "$R8" "$R7" "$R6" "$R5" "$R4"
classify() {
  f=$1; rc=$2; w=$3; sent_term=no; sent_kill=no
  printf 'WRAPPER_STREAM fence=%s bytes=%s [%s]\n' "$f" "${#w}" "$w" >&2
  case "$w" in *'sending signal TERM to command'*) sent_term=yes ;; esac
  case "$w" in *'sending signal KILL to command'*) sent_kill=yes ;; esac
  case "$rc" in
    0) return 0 ;;
    124) printf 'PUBLISHED_COMMAND_RESULT=timeout fence=%s kind=terminated_at_bound wrapper_sent_term=%s per_fence_bound_s=900\n' "$f" "$sent_term"; exit 124 ;;
    137) if [ "$sent_kill" = yes ]; then
           printf 'PUBLISHED_COMMAND_RESULT=timeout fence=%s kind=killed_after_grace wrapper_sent_term=%s wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30\n' "$f" "$sent_term"; exit 137
         else
           printf 'PUBLISHED_COMMAND_RESULT=fence_failed fence=%s rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no wrapper_stream=body_cannot_write\n' "$f"; exit 1
         fi ;;
    *) printf 'PUBLISHED_COMMAND_RESULT=fence_failed fence=%s rc=%s\n' "$f" "$rc"; exit 1 ;;
  esac
}
classify r9 "$R9" "$R9_W"
classify r8 "$R8" "$R8_W"
classify r7 "$R7" "$R7_W"
classify r6 "$R6" "$R6_W"
classify r5 "$R5" "$R5_W"
classify r4 "$R4" "$R4_W"
printf 'PUBLISHED_COMMAND_RESULT=pass fences=6 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=5580 whole_command_bound=none prelude_bounded=no wrapper_stream=unnamed_pipe_body_cannot_write\n'
# RP7_EXACT_COMMAND_END
```

That block is extractable and runnable by the same mechanism, so a third party never has
to retype it:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

It was executed exactly that way, from a fresh `bash --noprofile --norc`, and produced:

```text
9602bb0b6a129f509cba61150e81dc116f756af034983094c6745c839055848f */tmp/rp7-r9-fence-body.sh
f5caef75c68a84e396113dd60519d4b6df8c00feb7b90fd12dc73121e9b9b6ca */tmp/rp7-r8-fence-body.sh
9438700ec3b8e8f23d5b2c4cb95fac28db3e6ac69cf5032cc5604728a176efcf */tmp/rp7-r7-fence-body.sh
fa4897e752350ccc37efa4f178cfb7522677453f2b76de3d873a2c9bb204195b */tmp/rp7-r6-fence-body.sh
aa21ec19883274392427298e74541759c574009008aad86e3c169ee9cbc857c9 */tmp/rp7-r5-fence-body.sh
a0fd7291b89f9a28169bfa15432c66b6dba79cbda0d4a558fab1f981007073ab */tmp/rp7-r4-fence-body.sh
 28389 /tmp/rp7-r9-fence-body.sh
 31514 /tmp/rp7-r8-fence-body.sh
 23347 /tmp/rp7-r7-fence-body.sh
 38830 /tmp/rp7-r6-fence-body.sh
 21263 /tmp/rp7-r5-fence-body.sh
 79457 /tmp/rp7-r4-fence-body.sh
222800 total
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
R9_FENCE_RC=0
R8_FENCE_RC=0
R7_FENCE_RC=0
R6_FENCE_RC=0
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=6 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=5580 whole_command_bound=none prelude_bounded=no wrapper_stream=unnamed_pipe_body_cannot_write
```

Its stderr is not empty and is not meant to be: it carries the six
`WRAPPER_STREAM fence=<f> bytes=0 []` lines - one per fence, the wrapper stream the body
cannot write - plus whatever each bounded body wrote to its own stderr file, which in a clean
run is nothing.

All six fences abort with `QA_ASSERT_FAIL` and a nonzero exit on any unexpected result, so
`QA_PASS all_assertions=yes` is reachable only when every assertion in them held - and the
command reports that failure in its own exit status, and a fence stopped at its bound in a
`timeout` result distinct from it. The full per-fence output of that run is the six
transcripts below; its measured wall clock and byte counts are under
`### Literal re-run of the published command against this document`.

## What this environment can and cannot represent (disclosed in full)

MSYS2 has no root, and its NTFS mounts are `noacl`, so `chown 0:0` and `chmod 0555` are
silent no-ops; it also cannot create a POSIX symlink or a character device at an arbitrary
path. These fixture classes exist for exactly those gaps, and nothing else is substituted
anywhere in this suite:

| Fixture | Substitutes only | Everything else is real |
|---|---|---|
| `stat-shim` + variants (round-4 fence) | numeric ownership (rendered `0:0`), and for one named path per variant the `%F` kind or the `%u:%g` pair | the real GNU `stat` result for the real object: mode, `dev:inode`, size, exit status, ENOENT classification, stream discipline, and the wrapper's own `argv[0]` in its diagnostic |
| `stat-eacces-*` (round-4 fence) | nothing about the object | a real nonzero `stat` exit with a real `Permission denied` diagnostic for one named path, delegating every other path to `stat-shim` |
| `readlink-plain`, `readlink-cr` (round-4 fence) | the target string a real `readlink` would print for a symlink MSYS2 cannot create | the production symlink branch, the single-record reader and `wpi_sanitize` run unmodified |
| `wpi_capture` in the round-6 F1/F2/F3 arms | the child that would have run `ss` or `curl` on a real host, replaced by the exact bytes the audit fed | the whole of `wpi_assert_listener_set` / `wpi_assert_status` from the capture result onward - the reader, the byte accounting, the grammar and the verdict, which is what these three findings are about |
| `wpi_sha_file` in the round-6/7/8 F2 arms | the digests those arms do not measure, rendered as 64 zeroes. Round 9 removed the companion `wpi_alloc_leaf` stub with the function itself; the status body leaf is now allocated by the real `wpi_open_leaf` in every arm | the real `wpi_open_leaf` for every leaf including the status body, the real single-record reader, the real result grammar, and in the schema arm the real CPython child over the real production body |
| `wpi_capture` in the round-7 F1/F2 arms | the child that would have run `curl`, `readlink` or `ss` on a real host, replaced by the exact bytes the audit fed; the stub allocates the read descriptor the production capture allocates | the whole of `wpi_assert_status` / `wpi_assert_netns_binding` / `wpi_assert_listener_set` from the capture result onward - the single-record reader, the byte accounting, the queue-field grammar and the verdict |
| the round-7 F3 arms | nothing about the capture: `wpi_capture` is the real one, running a real child under the real cleared environment and the real bounding wrapper. Only `wpi_alloc_read_diag` is hooked, to replace the leaf name at the reader-allocation boundary - the same injection point the auditor used | real create-once leaf allocation, real descriptor binding, the real listener reader and the real verdict |
| `forge_capture` (the round-6, round-5 and round-4 fences) | the MSYS `env -i`/`timeout` exec plumbing, which rewrites POSIX-looking argv for a native Windows child, plus the Windows CRLF record terminator normalised to the LF a Debian CPython emits | the interpreter the production body **chose** (`a[0]`), the flag words it chose, real CPython, the real embedded driver source, the real digest-bound `verify_lock.py`, real exit codes |
| `wpi_lstat` shim in the finding-2 arms | numeric ownership and object kind, which NTFS cannot express | the production row-19 preflight, the production trusted driver, the production result grammar and the real verifier bytes |
| `rp0_require_safe_component` / `rp0_allocate_evidence_dir` in the finding-5 arms | the two RP0-LIB predicates, which are not present on this workstation, defined as no-op shell **functions** | the whole of `wpi_assert_prerequisites`, including the type check finding 4 introduced and the evidence-root descent check finding 5 introduced |
| `wpi_capture` in the round-8 F1/F2 arms | the child that would have run `curl` or `readlink` on a real host, replaced by the exact bytes the audit fed; the stub allocates the two read descriptors the production capture allocates, and in the `unbound` variant deliberately allocates neither | the whole of `wpi_assert_status` / `wpi_assert_netns_binding` from the capture result onward - the descriptor resolution, the single-record reader, the diagnostic-stream emptiness check, the status and namespace grammar and the verdict |
| the round-8 F1 and F4 arms | nothing about the capture: `wpi_capture` is the real one, running a real child under the real cleared environment and the real bounding wrapper. Only `wpi_clock_ms` is hooked - in F1 to replace the leaf with a hard link to a file outside the tree (the recovered round-5 fixture), in F4 to close the creating write descriptor through Bash's dynamic scoping, which is the deterministic way to make the `/dev/fd/<n>` re-open fail | real create-once leaf allocation, the real bind attempt, the real caller-declared inability token, and the real row adjudicator |
| the round-8 F1 `return 7` mutant | one inserted statement at the top of `wpi_capture` in a COPY of the repaired block; the copy is never delivered and its `bash -n` is asserted | everything else about the block, and both assertions under test are the literal ones from the round-7 and round-8 documents |

Production functions are replaced in only four places, each stated where it occurs and each
with its own subject elsewhere: `wpi_walk_components` in the write-bit arms (subject:
`find`-stdout classification and the FAIL-through-guard path), `wpi_assert_regular_digest`
in the parity arms (subject: row 19a, which has its own arms), `wpi_capture` where a child
must really execute, and `wpi_bind_tool`/`wpi_mount_guard_*` in the finding-1 arm - where
the *stub is the instrument*: it records what the real `wpi_main` asked it to bind and in
which window, and STOPs if and only if production asks it to bind `python3`.

Two production predicates really call `exit`, so the finding-1, finding-2, finding-4 and
finding-5 arms invoke them inside a subshell. Without that, an arm could not survive its
own STOP to report the STOP. Every round-6 arm does the same for the same reason.

Two arms execute a copy of a published artefact rather than the artefact itself: the
round-6 F4 propagation arm and the round-8 and round-9 F3 provenance arms run the exact
published command with substitutions - its `cd` target, the `/tmp` prefix of the fence-body
paths so that a nested run cannot overwrite the body of the run executing it, and in the
provenance arms the bound scaled from `900s`/`30s` to `1s`/`2s`. Both substitutions are asserted in the fence
before the copy runs, and the arm exists precisely because the first version of it, which
retargeted `cd` first and let the `/tmp` rule rewrite the new target, re-entered the real
document and had to be killed. Nothing else about the command is altered.

Not reproducible here, and not claimed: a real bind or overlay mount, and a real
`/proc/<MainPID>/ns/net`. As in rounds 3 and 4, those are falsified by appending to a real
captured `mountinfo` table the exact record such a mount would produce.

One round-7 behaviour is environment-dependent and is reported rather than asserted. The
round-7 read binding re-opens the capture's own descriptor through `/dev/fd/<n>`. On Linux
that succeeds even when the leaf name has been unlinked, because the re-open resolves
through the descriptor. MSYS2 cannot re-open the descriptor of an unlinked file, so the
carried round-6 leaf-replacement arm - which unlinks the leaf and hard-links a file from
outside the tree in its place - additionally reaches
`RP7_STOP reason=capture_stream_not_bindable` on this workstation, where on Linux it would
return rc 0. What that arm measures is unchanged and is what it asserts: the payload never
leaves the evidence tree.

**The `verify_lock.py` driven by every parity arm is the real candidate artifact.** The
round-4 fence LF-normalises the worktree copy and asserts its identity before use;
`VERIFIER_IDENTITY` in its transcript records 3735 bytes and `d951e0ee...a451e5`, which is
exactly `WPI_VERIFY_LOCK_SHA256`. The round-5 finding-2 arms feed the same file to the same
production driver.


## The round-9 fence

Five arm groups. Four take the block as their subject, with a real RED against the round-8
blob at `bb8546e6` and a real GREEN against the repaired bytes. The fifth is a static
comparison of two document texts, because finding 4 is about a carried assertion whose
replacement and whose executed mutant both live in the round-6 fence that carries it.

| Arm | RED | GREEN |
|---|---|---|
| F1 leaf name replaced with a hard link to an OUTSIDE object before curl runs | curl re-resolves the name and overwrites the outside object - `outside_bytes=197 outside_is_original=no` - and the row still returns rc 0 with `B5_status ... flags=expected` | `outside_is_original=yes`, and the row STOPs: `B5_STOP reason=status_endpoint_not_evaluable rc=23 detail=transport_error`. curl was given `/dev/fd/3`, not a name |
| F1 child writes an ARMED body, the name is replaced with a DISARMED body before any reader | rc 0 `B5_status ... flags=expected body_sha256=378c48e9...` - the accepting line carries the digest of bytes the child never wrote | rc 1 `B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a96...` - the object the create-once open created is what is adjudicated |
| F1 control: no substitution, clean DISARMED body | rc 0 accepting, `body_sha256=378c48e9...` | identical |
| F1 control: no substitution, ARMED body | rc 1 `flag_mismatch field=state` | identical |
| F2 production capture cannot bind its stdout descriptor after a child that exited 7 | `B6_STOP ... rc=0 detail=capture_stream_unbound` - the caller's literal, and it is false | `B6_STOP ... rc=7 detail=capture_stream_unbound` - the status the child returned |
| F2 control: the same bind failure after a child that exited 0 | `rc=0 detail=capture_stream_unbound` | identical - where the literal was true, nothing changed |
| F2 control: a caller that declares no token of its own | generic `RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe` | identical - the repair reports a measured rc, it does not widen a route |
| F2 control: nothing diverted, clean inventory | `B6_listener_inventory ... B6_listener_set port=8790 count=1` | identical |
| F3 fence body prints the wrapper's own KILL phrase and exits 137 | `kind=killed_after_grace`, command exits 137 - the body forged the wrapper's provenance | `fence_failed ... kind=sigkill_not_from_this_wrapper wrapper_stream=body_cannot_write`, exits 1 |
| F3 control: bare `exit 137` | `sigkill_not_from_this_wrapper`, exit 1 | identical |
| F3 control: TERM-ignoring body | `killed_after_grace`, exit 137 | identical - a real kill-after is still classified as one |
| F3 budget arithmetic | `wrappers=5 computed_s=4650 claimed_s=4650` | `wrappers=6 computed_s=5580 claimed_s=5580`, re-derived from the published text |
| F4 the carried mapping assertion | round-8 text still contains `expect_rc f4_every_body_wrapped` | it is gone and `expect_has f4_mapping_power` is present; the round-6 fence runs the omit-R8/duplicate-R7 mutant and prints `round8_on_mutant=accept round9_on_mutant=reject` |
| F5 nonzero readlink child, caller path and service path | `B6_STOP reason=service_netns_unreadable path=... rc=7` with no `detail=` | the same line with `detail=identity_read_child_failed diagnostic_file=<leaf>` |
| F5 control: two equal namespaces | `B6_netns ... binding=equal` rc 0 | identical |

### Every carried arm round 9 changed, and what each change costs

The standing rule is that a carried fence changes only with a per-change discriminating-power
argument: name the input that used to fail there and show it still fails. Eleven changes were
made and this is all of them.

| # | Fence | Change | Why it was forced | What input used to fail here, and does it still? |
|---|---|---|---|---|
| 1 | all five carried | GREEN identity constants move to the round-9 SHA-256 and byte count | The subject moved | Wrong subject bytes. **Still fails**, before any arm runs |
| 2 | round-8 F2 | the `status_json` accepting-record fixture is chosen per subject: `OK fields=8` for RED, `OK fields=8 sha256=<64 hex>` for GREEN | The parser's accepting record now carries the digest of the bytes it read, so a stub standing in for a parser must emit the record ITS OWN subject can emit | The name-reopen substitution. **Still fails**: `f2_red_status_swapped` still shows RED adjudicating `200` over a child-observed `500`, and `f2_green_status_swapped` still shows GREEN adjudicating the child's bytes. Both records are pinned constants, not read from the subject, so a block that changed its accepting grammar would fail rather than be accommodated |
| 3 | round-8 F4 | the injection is replaced: instead of closing the creating descriptor before the child, the stdout leaf's descriptor becomes a pipe write end, and the arm now asserts `child_ran=yes` and `escaped_stderr_bytes=0` | The round-8 injection stopped the child from running at all, so the arm never established the fact its token states (finding 2) | The generic-STOP regression - a block whose production bind failure exits as `RP7_STOP reason=capture_stream_not_bindable` where row 22 declares a `B6_STOP`. **Still fails**: `f4_red_generic` still shows exactly that on the round-7 blob. The arm now fails on two further inputs it could not previously detect: a child that did not run, and a raw shell diagnostic on stderr |
| 4 | round-7 F1 | the same per-subject accepting-record fixture as change 2 | Same | The three NUL fixtures. **Still fail** unchanged - `code_nul`, `record_nul` and the six netns reader dispositions are byte-identical, and only the `clean`/`code_nul` accepting record moved |
| 5 | round-6 F2 | `f2 ok` becomes `f2s ok` with a per-subject record, and two arms are ADDED: `ok_nodigest` (the round-8 record) and `ok_baddigest` | Same as change 2, plus the change itself needs falsifying | The eleven malformed and four legitimate result records. **All still produce their round-6 dispositions**, byte for byte. The two added arms are what make the fixture change honest: GREEN must REJECT the round-8 record (`detail=strict_json_or_parser_failure`) and a malformed digest (`detail=ok_record_digest`), and RED accepts the first - so the digest is required, not merely tolerated |
| 6 | round-6 F4 | `expect_rc f4_every_body_wrapped` (wrappers == extractions) is replaced by `map_check`, an exact per-fence mapping, and the omit-R8/duplicate-R7 mutant is added as a RED | Two equal counts are not a mapping; the mutant passes the old assertion (finding 4) | An unwrapped fence body - the case the count check existed for. **Still fails**, through `f4_bound_wrappers`/`f4_bound_extractions`/`f4_bound_classifiers` and through the per-fence rows. What newly fails is the mutant, and the fence records the comparison itself: `MAPPING_ASSERTION_POWER round8_on_mutant=accept round9_on_mutant=reject` |
| 7 | round-6, round-5, round-4 | `forge_capture` honours `WPI_CAP_CHILD_FD`/`WPI_CAP_CHILD_SLOT` by binding the child's stdin | Production now hands a child an already-open descriptor instead of a path, exactly as round 8 made these stubs supply `WPI_CAP_ERR_FD` | The `.pth` and `sitecustomize` forgeries and the `-S` mutants. **All still fail**: `pth_status_green_truthful`, `pth_status_greenvenv_truthful` and `nos_status_refused` are unchanged, because a stub that set only names would no longer be standing in for `wpi_capture` at all |
| 8 | round-5 F4(c), round-6 F2 schema arm | `wpi_alloc_leaf` becomes `wpi_open_leaf`, and the round-6 schema arm's no-op `wpi_alloc_leaf` stub is deleted with the function | The name-only allocator was DELETED - its last caller was the status body this round rebound, and leaving it available would leave the defect one call site away | Re-creating an existing leaf, and allocating outside `EV_DIR`. **Both still fail**, with the same two reason tokens and the same zero-byte diagnostic streams; only the function name moved, because there is now exactly one allocator |
| 9 | round-4 | `nos_status_refused` anchors its pattern at end of line instead of on a trailing space | The row-21 parser-failure STOP no longer carries a `body_sha256=` field, because the only digest this block has is the one the parser reports for bytes it accepted | A block whose `-S`-less parser is not refused. **Still fails**, and the anchored pattern is strictly stronger: it rejects any extra field as well |
| 10 | round-8 F3 | this group's GREEN becomes the round-8 command TEXT at `bb8546e6` instead of the live document | A carried group that re-adjudicates a moving subject stops measuring the transition it was written for: the live command now has six wrappers and a round-9 fence, so `fence=r8 scaled_wrappers=5` no longer describes it. Round 8 made exactly this change to the round-7 fence for exactly this reason | The round-7 misattribution of a bare `exit 137`. **Still fails**, on the frozen pair it was written for. The live text is not left unmeasured: the round-9 F3 group measures round-8 -> round-9 on it, including the new child-spoof input |
| 11 | round-4 | the frozen round-3 RED bodies are given a `wpi_alloc_leaf` definition of their own | Round 9 deleted that function from the block and three frozen round-3 bodies call it. Left alone the call failed as `command not found`: the allocation was silently skipped, seven raw shell diagnostics escaped to stderr, and the RED arms stopped exercising the round-3 behaviour they are the record of | Every round-3 defect these bodies carry. **All still fail** - the definition supplied is the round-3 one verbatim, so the RED arms are restored to the behaviour they recorded rather than changed. This is a repair to the fence, not a relaxation of it: before it, the fence was passing while leaking diagnostics |

Two injections are used and each is named where it occurs. The F1 substitution is a hooked
`wpi_clock_ms` at the status capture's own start and end clocks - the two windows the
auditor used, and not routes the block reaches on its own; what they measure is what the
block *establishes*. The F2 injection replaces the stdout capture leaf's descriptor with the
write end of a pipe, which is the one way to make `/dev/fd/<n>` unopenable deterministically
*after* the child has run: the round-8 arm closed that descriptor *before* the child's
redirection, so the child it claimed to test never ran (Codex round-9 part B finding 2), and
that arm has been rebuilt on this injection in the round-8 fence as well.

One environment limitation is stated rather than argued away. On Linux `/dev/fd/<n>`
resolves through the process's descriptor table, so GREEN's F1 outside arm would leave the
outside object untouched **and** complete the fetch into the created object at rc 0. MSYS2
resolves `/dev/fd/<n>` through the path instead, so once the name has been replaced the open
fails and GREEN STOPs at `rc=23 detail=transport_error`. Both dispositions establish the
property the row needs - no object outside the evidence tree is written and no accepting
line is produced over substituted bytes - and the arm asserts the MSYS2 one, which is the
one this workstation can reproduce. The reader side has no such dependency: its descriptor
is derived at creation time and is a real descriptor on both platforms, which is why the
F1 reader arm produces the truthful `B5_FAIL` here rather than a STOP.

```bash
# RP7_R9_FENCE_BEGIN
# Round-9 D026 fence for RP7-WPI-RO. Every arm drives the REAL production caller
# in a FRESH bash process, or the REAL published command TEXT, against two byte
# sets whose identity is asserted first:
#   RED   = the frozen round-8 blob at commit bb8546e6 (99903 B, 11621044...141a4)
#   GREEN = the repaired worktree file
# Round 9's block findings are all identity findings - an object addressed by a
# name instead of by the descriptor that created it, and an rc printed as a
# literal instead of measured - so every arm feeds a real child, lets it write,
# and then asks what the block says about what it wrote.
#
# Finding 4 is about a carried ASSERTION rather than about the block, and its
# repair and its executed falsification both live in the round-6 fence, where
# that assertion is. This fence asserts only that the replacement is present and
# the round-8 form is gone; the round-6 fence runs the mutant.
REPO=/c/LAB/Tradingview_LAB_CLEAN
DOC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
BLOCK=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
PYEXE=/c/Python314/python.exe
Q=$(mktemp -d /tmp/rp7-r9-qa.XXXXXX)
RED=$Q/RP7-WPI-RO.round8.sh
GREEN=$BLOCK

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_has(){ grep -q -- "$2" "$3" || { printf 'QA_ASSERT_FAIL name=%s missing=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_hasnt(){ grep -q -- "$2" "$3" && { printf 'QA_ASSERT_FAIL name=%s unexpected=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; return 0; }

printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_timeout=%s git=%s uid_gid=%s:%s python=%s\n' \
    "$BASH_VERSION" "$(/usr/bin/timeout --version | head -1 | sed 's/.* //')" \
    "$(git --version | sed 's/.* //')" "$(id -u)" "$(id -g)" \
    "$("$PYEXE" -c 'import sys;print(sys.version.split()[0])')"

# --- byte identity of both subjects -----------------------------------------
git -C "$REPO" cat-file blob bb8546e6:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$RED"
RED_SHA=$(sha256sum < "$RED" | cut -d' ' -f1);     RED_BYTES=$(wc -c < "$RED")
GREEN_SHA=$(sha256sum < "$GREEN" | cut -d' ' -f1); GREEN_BYTES=$(wc -c < "$GREEN")
RED_CR=$(tr -cd '\r' < "$RED" | wc -c);  GREEN_CR=$(tr -cd '\r' < "$GREEN" | wc -c)
bash --noprofile --norc -n "$RED";   RED_N=$?
bash --noprofile --norc -n "$GREEN"; GREEN_N=$?
printf 'BYTE_IDENTITY red_bytes=%s red_sha256=%s red_cr=%s red_bash_n=%s green_bytes=%s green_sha256=%s green_cr=%s green_bash_n=%s\n' \
    "$RED_BYTES" "$RED_SHA" "$RED_CR" "$RED_N" "$GREEN_BYTES" "$GREEN_SHA" "$GREEN_CR" "$GREEN_N"
expect_eq r9_red_sha256   "$RED_SHA"   11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4
expect_eq r9_red_bytes    "$RED_BYTES" 99903
expect_eq r9_green_sha256 "$GREEN_SHA" 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
expect_eq r9_green_bytes  "$GREEN_BYTES" 108301
expect_rc r9_red_cr "$RED_CR" 0
expect_rc r9_green_cr "$GREEN_CR" 0
expect_rc r9_red_bash_n "$RED_N" 0
expect_rc r9_green_bash_n "$GREEN_N" 0

# ===========================================================================
# FINDING 1 (BLOCK/HIGH) - `ro.status.body` was create-once allocated and then
# addressed three times by NAME: `--output "$body"` for curl, `wpi_sha_file
# "$body"` for the digest, and `argv[1]` for the parser. Nothing bound those to
# the created object or to each other, so the row was BOTH an outside-tree write
# primitive and a false-PASS primitive. Round 8 disclosed that accurately and
# left it standing.
#
# Both arms drive the REAL `wpi_assert_status`, the REAL `wpi_capture`, the REAL
# create-once allocator and the REAL pinned CPython parser. The ONLY child
# substitution is a local, no-network, curl-shaped program that opens exactly the
# `--output` operand it is given and writes the body there; the ONLY other
# substitution is the MSYS/native CRLF plumbing on the interpreter's stdout,
# which the round-4 fence already discloses. The ONLY injection is a hooked
# `wpi_clock_ms`, at the two boundaries the capture itself crosses: its call 1 is
# the status_get start clock (the body leaf exists, the child has not started) and
# its call 2 is that capture's end clock (the child has written, no reader has
# run). Those are the same two windows the auditor used.
#   mode=outside  the leaf name is replaced with a hard link to a file OUTSIDE
#                 the evidence tree, before the child starts.
#   mode=reader   the child writes an ARMED body; the name is then replaced with
#                 a complete DISARMED body before any reader runs.
#   mode=none / none_armed  the same fixtures with NO substitution - the
#                 no-weakening controls, which must reach identical dispositions
#                 on both subjects.
# ===========================================================================
DISARMED='{"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
ARMED='{"state":"ARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
cat > "$Q/py.sh" <<'PY'
#!/bin/sh
# The pinned interpreter on this workstation is a native Windows build and
# terminates its stdout lines with CRLF; the block's record reader is byte-exact
# by design. This strips CR and changes nothing else.
/c/Python314/python.exe "$@" > "$TMPDIR/rp7py.$$.out"; rc=$?
tr -d '\r' < "$TMPDIR/rp7py.$$.out"; rm -f "$TMPDIR/rp7py.$$.out"
exit $rc
PY
chmod 755 "$Q/py.sh"
mkcurl(){ # $1 tag, $2 body text - baked in, because the child runs under `env -i`
  { printf '#!/bin/sh\nout=""; prev=""\nfor a in "$@"; do\n'
    printf '  [ "$prev" = --output ] && out="$a"\n  prev="$a"\ndone\n'
    printf "printf '%%s\\\\n' '%s' > \"\$out\" || exit 23\n" "$2"
    printf 'printf "200\\n"\n'; } > "$Q/curl-$1.sh"
  chmod 755 "$Q/curl-$1.sh"
}
mkcurl dis "$DISARMED"
mkcurl arm "$ARMED"
cat > "$Q/f1_arm.sh" <<'ARM'
S="$1"; W="$2"; Q="$3"; mode="$4"; CURL="$5"; SWAPPED="$6"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=60
WPI_CURL="$CURL"; WPI_PYTHON3="$Q/py.sh"; WPI_SHA256SUM=/usr/bin/sha256sum
WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
BODY="$EV_DIR/ro.status.body"
OUTSIDE="$W/outside.txt"; printf 'ORIGINAL\n' > "$OUTSIDE"
HOOK=0
wpi_clock_ms(){
  HOOK=$((HOOK+1))
  case "$mode:$HOOK" in
    outside:1) rm -- "$BODY"; ln -- "$OUTSIDE" "$BODY" ;;
    reader:2)  cp -- "$BODY" "$W/child-body.json"; rm -- "$BODY"; printf '%s\n' "$SWAPPED" > "$BODY" ;;
  esac
  WPI_LINE="$HOOK"
}
wpi_assert_status
ARM
f1(){ # mode subject curl swapped
  local mode="$1" subject="$2" curl="$3" swapped="$4" S W rc child_sha name_sha
  if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
  W=$Q/f1-$mode-$subject; mkdir -p "$W"
  bash --noprofile --norc "$Q/f1_arm.sh" "$S" "$W" "$Q" "$mode" "$curl" "$swapped" > "$W.txt" 2>&1; rc=$?
  if [ -f "$W/child-body.json" ]; then child_sha=$(sha256sum < "$W/child-body.json" | cut -d' ' -f1); else child_sha=not_replaced; fi
  if [ -f "$W/ev/ro.status.body" ]; then name_sha=$(sha256sum < "$W/ev/ro.status.body" | cut -d' ' -f1); else name_sha=absent; fi
  printf 'BODY_BINDING mode=%s subject=%s rc=%s outside_bytes=%s outside_is_original=%s child_body_sha256=%s name_at_read_time_sha256=%s result=[%s]\n' \
    "$mode" "$subject" "$rc" "$(wc -c < "$W/outside.txt")" \
    "$([ "$(tr -d '\n' < "$W/outside.txt")" = ORIGINAL ] && echo yes || echo no)" \
    "$child_sha" "$name_sha" \
    "$(sed -e "s#$Q#<scratch>#g" "$W.txt" | tr '\n' ' ' | sed 's/ *$//')"
}
{ for s in red green; do f1 outside    "$s" "$Q/curl-dis.sh" "$DISARMED"; done
  for s in red green; do f1 reader     "$s" "$Q/curl-arm.sh" "$DISARMED"; done
  for s in red green; do f1 none       "$s" "$Q/curl-dis.sh" "$DISARMED"; done
  for s in red green; do f1 none_armed "$s" "$Q/curl-arm.sh" "$ARMED"; done; } > "$Q/f1.txt"
cat "$Q/f1.txt"
ARMED_SHA=$(printf '%s\n' "$ARMED" | sha256sum | cut -d' ' -f1)
DISARMED_SHA=$(printf '%s\n' "$DISARMED" | sha256sum | cut -d' ' -f1)
printf 'F1_FIXTURE_DIGESTS armed_body_sha256=%s disarmed_body_sha256=%s\n' "$ARMED_SHA" "$DISARMED_SHA"
# The outside object is 9 bytes of `ORIGINAL`. RED lets curl overwrite it with the
# 197-byte response body and still returns an accepting rc 0; GREEN leaves it
# untouched and STOPs, because curl was never given a name to re-resolve.
expect_has f1_red_writes_outside 'BODY_BINDING mode=outside subject=red rc=0 outside_bytes=197 outside_is_original=no child_body_sha256=not_replaced .* result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f1.txt"
expect_has f1_green_no_outside_write 'BODY_BINDING mode=outside subject=green rc=3 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced .* result=\[B5_STOP reason=status_endpoint_not_evaluable rc=23 detail=transport_error diagnostic_file=' "$Q/f1.txt"
# The child wrote ARMED. RED adjudicates the DISARMED bytes the NAME resolved to
# and prints the accepting line carrying THAT digest - the false PASS. GREEN
# adjudicates the object the create-once open created and reports the deviation.
expect_has f1_red_false_pass "BODY_BINDING mode=reader subject=red rc=0 outside_bytes=9 outside_is_original=yes child_body_sha256=$ARMED_SHA name_at_read_time_sha256=$DISARMED_SHA result=\[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=$DISARMED_SHA " "$Q/f1.txt"
expect_has f1_green_truthful_fail "BODY_BINDING mode=reader subject=green rc=1 outside_bytes=9 outside_is_original=yes child_body_sha256=$ARMED_SHA name_at_read_time_sha256=$DISARMED_SHA result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=" "$Q/f1.txt"
# The substitution really happened in both cases: the child's bytes and the bytes
# the NAME resolved to differ on BOTH subjects. Only the subject that resolves no
# name after creation is unaffected by that difference.
expect_eq f1_swap_effective "$([ "$ARMED_SHA" != "$DISARMED_SHA" ] && echo yes || echo no)" yes
# No-weakening: with no substitution at all, a clean DISARMED body reaches the
# accepting line on both subjects, and an ARMED body reaches the same truthful
# FAIL on both. The repair changed only what happens when a name is replaced.
expect_has f1_red_clean_accept   "BODY_BINDING mode=none subject=red rc=0 .* result=\[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=$DISARMED_SHA " "$Q/f1.txt"
expect_has f1_green_clean_accept "BODY_BINDING mode=none subject=green rc=0 .* result=\[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=$DISARMED_SHA " "$Q/f1.txt"
expect_has f1_red_armed_fail     'BODY_BINDING mode=none_armed subject=red rc=1 .* result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=' "$Q/f1.txt"
expect_has f1_green_armed_fail   'BODY_BINDING mode=none_armed subject=green rc=1 .* result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=' "$Q/f1.txt"
# The accepting digest is the digest of the bytes the PARSER read, not of a second
# read: GREEN's clean accepting line carries the digest of the exact body the
# child wrote, computed inside the parser child.
expect_has f1_green_digest_is_parsed_bytes "body_sha256=$DISARMED_SHA content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site" "$Q/f1.txt"
# ===========================================================================
# FINDING 2 (HIGH) - a caller-supplied `rc=0` literal in the descriptor-bind
# STOP. The block emitted it whatever the child had returned.
#
# The injection is the STDOUT capture leaf's descriptor - the one stream BOTH
# subjects bind. The leaf is created by the real allocator and its descriptor is
# then replaced with the write end of a pipe that drains into that same leaf.
# `/dev/fd/<n>` of a pipe cannot be re-opened on Linux or on MSYS2, so the
# POST-CHILD bind fails deterministically while the child runs to completion
# through the descriptor it inherits, leaving a marker and its own status.
# ===========================================================================
cat > "$Q/f2_arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"; ssrc="$4"; sserr="$5"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=60
{ printf '#!/bin/sh\nprintf x > "%s"\n' "$W/child-ran.marker"
  printf 'printf "LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\\n"\n'
  if [ "$sserr" = yes ]; then printf 'printf "ss: child diagnostic\\n" >&2\n'; fi
  printf 'exit %s\n' "$ssrc"; } > "$W/ss.sh"
chmod 755 "$W/ss.sh"; WPI_SS="$W/ss.sh"
eval "wpi_real_open_leaf() $(declare -f wpi_open_leaf | sed '1d')"
wpi_open_leaf(){
  wpi_real_open_leaf "$1"
  case "$mode:$1" in
    divert_*:*.listeners.stdout|undeclared:*.undeclared_probe.stdout)
      exec {WPI_LEAF_FD}> >(cat >> "$1") ;;
  esac
}
case "$mode" in
  undeclared) wpi_capture undeclared_probe "$WPI_SS" -H -ltn ;;
  *)          wpi_assert_listener_set ;;
esac
ARM
f2(){ # mode subject ssrc sserr
  local mode="$1" subject="$2" ssrc="$3" sserr="$4" S W rc
  if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
  W=$Q/f2-$mode-$subject; mkdir -p "$W"
  bash --noprofile --norc "$Q/f2_arm.sh" "$S" "$W" "$mode" "$ssrc" "$sserr" > "$W.out" 2> "$W.err"; rc=$?
  printf 'BIND_RC mode=%s subject=%s child_rc=%s rc=%s child_ran=%s escaped_stderr_bytes=%s stdout_lines=%s result=[%s]\n' \
    "$mode" "$subject" "$ssrc" "$rc" \
    "$([ -f "$W/child-ran.marker" ] && echo yes || echo no)" \
    "$(wc -c < "$W.err")" "$(grep -c . "$W.out")" \
    "$(sed -e "s#$Q#<scratch>#g" "$W.out" | tr '\n' ' ' | sed 's/ *$//')"
}
{ for s in red green; do f2 divert_rc7 "$s" 7 yes; done
  for s in red green; do f2 divert_rc0 "$s" 0 no;  done
  for s in red green; do f2 undeclared "$s" 7 yes; done
  for s in red green; do f2 clean      "$s" 0 no;  done; } > "$Q/f2.txt"
cat "$Q/f2.txt"
# RED prints a literal that is false; GREEN prints the status the child returned.
expect_has f2_red_false_rc   'BIND_RC mode=divert_rc7 subject=red child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound\]' "$Q/f2.txt"
expect_has f2_green_true_rc  'BIND_RC mode=divert_rc7 subject=green child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=7 detail=capture_stream_unbound\]' "$Q/f2.txt"
# No-weakening: where the literal happened to be TRUE, both subjects are identical.
expect_has f2_red_rc0    'BIND_RC mode=divert_rc0 subject=red child_rc=0 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound\]' "$Q/f2.txt"
expect_has f2_green_rc0  'BIND_RC mode=divert_rc0 subject=green child_rc=0 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound\]' "$Q/f2.txt"
# No-weakening: a caller that declares no token of its own still fails closed on
# the generic STOP - the repair reports a measured rc, it does not widen a route.
expect_has f2_red_undeclared   'BIND_RC mode=undeclared subject=red child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe ' "$Q/f2.txt"
expect_has f2_green_undeclared 'BIND_RC mode=undeclared subject=green child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=\[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe ' "$Q/f2.txt"
# No-weakening: with nothing diverted, a clean inventory reaches the identical
# accepting pair of lines on both subjects.
expect_has f2_red_clean   'BIND_RC mode=clean subject=red child_rc=0 rc=0 child_ran=yes escaped_stderr_bytes=0 stdout_lines=2 result=\[B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 .* B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\]' "$Q/f2.txt"
expect_has f2_green_clean 'BIND_RC mode=clean subject=green child_rc=0 rc=0 child_ran=yes escaped_stderr_bytes=0 stdout_lines=2 result=\[B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 .* B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\]' "$Q/f2.txt"

# ===========================================================================
# FINDING 3 (MEDIUM) - the published command's rc-137 provenance. `timeout
# --verbose` and the fence body wrote to the SAME stderr file, so a body that
# printed the wrapper's own phrase and exited 137 was called this wrapper's
# kill-after event. Both subjects are the published command TEXT: RED from commit
# bb8546e6, GREEN from this document. Each is retargeted into a scratch tree and
# its bound scaled from `900s`/`30s` to `1s`/`2s`; nothing else is altered.
# `child_spoof` is the new arm; `direct_137` and `ignore_term` are the round-8
# arms carried unchanged, because the repair must not disturb what round 8 fixed.
# ===========================================================================
git -C "$REPO" cat-file blob bb8546e6:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md > "$Q/SELF_QA_RP7.round8.md"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$Q/SELF_QA_RP7.round8.md" > "$Q/cmd-red.txt"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$DOC" > "$Q/cmd-green.txt"
for body in child_spoof direct_137 ignore_term; do
  for subject in red green; do
    T=$Q/f3-$body-$subject; mkdir -p "$T"
    case "$body" in
      child_spoof) PAYLOAD='printf "timeout: sending signal KILL to command\\n" >&2\nexit 137\n' ;;
      direct_137)  PAYLOAD='exit 137\n' ;;
      ignore_term) PAYLOAD="trap '' TERM\n/usr/bin/sleep 30\n" ;;
    esac
    # The newest fence of each subject carries the payload; every other fence
    # exits 0. RED has no round-9 fence, so its newest is the round-8 one.
    { if [ "$subject" = green ]; then printf "# RP7_R9_FENCE_BEGIN\n${PAYLOAD}# RP7_R9_FENCE_END\n"
                                       printf '# RP7_R8_FENCE_BEGIN\nexit 0\n# RP7_R8_FENCE_END\n'
      else printf '# RP7_R9_FENCE_BEGIN\nexit 0\n# RP7_R9_FENCE_END\n'
           printf "# RP7_R8_FENCE_BEGIN\n${PAYLOAD}# RP7_R8_FENCE_END\n"; fi
      printf '# RP7_R7_FENCE_BEGIN\nexit 0\n# RP7_R7_FENCE_END\n'
      printf '# RP7_R6_FENCE_BEGIN\nexit 0\n# RP7_R6_FENCE_END\n'
      printf '# RP7_QA_FENCE_BEGIN\nexit 0\n# RP7_QA_FENCE_END\n'
      printf '# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n'; } > "$T/SELF_QA_RP7.md"
    # The /tmp expression runs FIRST for the reason the round-6 fence documents:
    # this scratch tree is itself under /tmp/rp7-, so retargeting `cd` first would
    # let the /tmp rule rewrite the new target as well.
    sed -e "s#/tmp/rp7-#$T/body-#g" \
        -e "s#^cd /c/LAB/.*#cd $T#" \
        -e "s#--kill-after=30s 900s#--kill-after=2s 1s#g" \
        "$Q/cmd-$subject.txt" > "$T/run.sh"
    t0=$SECONDS
    timeout 120 bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
    printf 'RC137_PROVENANCE body=%s subject=%s cd_retargeted=%s real_fence_bodies=%s scaled_wrappers=%s rc=%s wall_s=%s spoof_text_in_command_stderr=%s result=[%s]\n' \
      "$body" "$subject" \
      "$(grep -c "^cd $T\$" "$T/run.sh")" \
      "$(grep -cE '/tmp/rp7-r[4-9]-fence-body\.sh' "$T/run.sh")" \
      "$(grep -c -- '--kill-after=2s 1s' "$T/run.sh")" \
      "$rc" "$((SECONDS-t0))" \
      "$(grep -c 'sending signal KILL to command' "$T/err.txt")" \
      "$(grep '^PUBLISHED_COMMAND_RESULT=' "$T/out.txt" | head -1 | sed 's/^PUBLISHED_COMMAND_RESULT=//')"
  done
done > "$Q/f3.txt"
cat "$Q/f3.txt"
# RED lets a fence BODY forge the wrapper's own diagnostic and calls the result a
# timeout. GREEN reads a stream the body cannot write and calls it what it is.
expect_has f3_red_spoofable   'RC137_PROVENANCE body=child_spoof subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=137 wall_s=[0-9] spoof_text_in_command_stderr=1 result=\[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=no wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"
expect_has f3_green_unspoofable 'RC137_PROVENANCE body=child_spoof subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=6 rc=1 wall_s=[0-9] spoof_text_in_command_stderr=1 result=\[fence_failed fence=r9 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no wrapper_stream=body_cannot_write\]' "$Q/f3.txt"
# Carried round-8 arms, unchanged: a bare 137 is still not a timeout on either
# subject, and a REAL kill-after is still classified as one on both.
expect_has f3_red_direct_137   'RC137_PROVENANCE body=direct_137 subject=red .* rc=1 .* result=\[fence_failed fence=r8 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no\]' "$Q/f3.txt"
expect_has f3_green_direct_137 'RC137_PROVENANCE body=direct_137 subject=green .* rc=1 .* result=\[fence_failed fence=r9 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no wrapper_stream=body_cannot_write\]' "$Q/f3.txt"
expect_has f3_red_real_kill    'RC137_PROVENANCE body=ignore_term subject=red .* rc=137 .* result=\[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"
expect_has f3_green_real_kill  'RC137_PROVENANCE body=ignore_term subject=green .* rc=137 .* result=\[timeout fence=r9 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"
# The budget is re-derived from the published text, not read from prose.
for subject in red green; do
  W=$(grep -cE 'timeout --verbose --signal=TERM --kill-after=30s 900s (bash --noprofile --norc|sh -c)' "$Q/cmd-$subject.txt")
  CLAIM=$(sed -n 's/.*fence_timeout_budget_s=\([0-9]*\).*/\1/p' "$Q/cmd-$subject.txt" | head -1)
  printf 'BUDGET_ARITHMETIC subject=%s wrappers=%s per_fence_nominal_s=900 kill_grace_s=30 computed_s=%s claimed_s=%s claim_true=%s\n' \
    "$subject" "$W" "$((W*(900+30)))" "$CLAIM" "$([ "$((W*(900+30)))" = "$CLAIM" ] && echo yes || echo no)"
done > "$Q/f3budget.txt"
cat "$Q/f3budget.txt"
expect_has f3_red_budget   'BUDGET_ARITHMETIC subject=red wrappers=5 per_fence_nominal_s=900 kill_grace_s=30 computed_s=4650 claimed_s=4650 claim_true=yes' "$Q/f3budget.txt"
expect_has f3_green_budget 'BUDGET_ARITHMETIC subject=green wrappers=6 per_fence_nominal_s=900 kill_grace_s=30 computed_s=5580 claimed_s=5580 claim_true=yes' "$Q/f3budget.txt"

# ===========================================================================
# FINDING 4 (MEDIUM) - a changed carried assertion equated two counts and called
# that a mapping. The replacement and its executed mutant live in the round-6
# fence, where the assertion is. Here the two texts are compared statically: the
# round-8 form must be gone and the mapping form present.
# ===========================================================================
R8_FORM=$(sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' "$Q/SELF_QA_RP7.round8.md" | grep -c 'expect_rc f4_every_body_wrapped')
R9_FORM=$(sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' "$DOC" | grep -c 'expect_rc f4_every_body_wrapped')
R9_MAP=$(sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' "$DOC" | grep -c 'expect_has f4_mapping_power')
printf 'MAPPING_ASSERTION_PRESENT round8_count_equality=%s round9_count_equality=%s round9_mapping_power=%s\n' \
  "$R8_FORM" "$R9_FORM" "$R9_MAP"
expect_rc f4_round8_had_count_equality "$R8_FORM" 1
expect_rc f4_round9_dropped_it "$R9_FORM" 0
expect_rc f4_round9_has_mapping "$R9_MAP" 1

# ===========================================================================
# FINDING 5 (MEDIUM) - draft row 22 declares `B6_STOP reason=
# service_netns_unreadable path=/proc/<pid>/ns/net rc=<n> detail=<d>`, and both
# nonzero readlink-child branches emitted `rc=<n>` and stopped there. The BLOCK
# was the wrong side: the detail field is mandatory on that reason and the
# diagnostic leaf that names the inability is already captured. Both branches are
# driven with a REAL child that fails, on the caller path and on the service path.
# ===========================================================================
cat > "$Q/f5_arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=60
WPI_MAINPID=123
{ printf '#!/bin/sh\ncase "$2" in\n'
  case "$mode" in
    caller)  printf '  /proc/self/ns/net) printf "readlink: bad link\\n" >&2; exit 7 ;;\n' ;;
    service) printf '  /proc/self/ns/net) printf "net:[100]\\n" ;;\n'
             printf '  /proc/123/ns/net) printf "readlink: bad link\\n" >&2; exit 7 ;;\n' ;;
    clean)   printf '  *) printf "net:[100]\\n" ;;\n' ;;
  esac
  printf '  *) printf "net:[999]\\n" ;;\nesac\n'; } > "$W/readlink.sh"
chmod 755 "$W/readlink.sh"
WPI_READLINK="$W/readlink.sh"
wpi_assert_netns_binding
ARM
f5(){ # mode subject
  local mode="$1" subject="$2" S W rc line
  if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
  W=$Q/f5-$mode-$subject; mkdir -p "$W"
  bash --noprofile --norc "$Q/f5_arm.sh" "$S" "$W" "$mode" > "$W.out" 2> "$W.err"; rc=$?
  line=$(sed -e "s#$Q#<scratch>#g" "$W.out" | tr '\n' ' ' | sed 's/ *$//')
  printf 'NETNS_DETAIL mode=%s subject=%s rc=%s detail_field_present=%s escaped_stderr_bytes=%s result=[%s]\n' \
    "$mode" "$subject" "$rc" \
    "$(printf '%s' "$line" | grep -c 'detail=')" "$(wc -c < "$W.err")" "$line"
}
{ for s in red green; do f5 caller  "$s"; done
  for s in red green; do f5 service "$s"; done
  for s in red green; do f5 clean   "$s"; done; } > "$Q/f5.txt"
cat "$Q/f5.txt"
expect_has f5_red_caller_no_detail    'NETNS_DETAIL mode=caller subject=red rc=3 detail_field_present=0 escaped_stderr_bytes=0 result=\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=7\]' "$Q/f5.txt"
expect_has f5_green_caller_detail     'NETNS_DETAIL mode=caller subject=green rc=3 detail_field_present=1 escaped_stderr_bytes=0 result=\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=7 detail=identity_read_child_failed diagnostic_file=<scratch>/f5-caller-green/ev/ro.0001.caller_netns.stderr\]' "$Q/f5.txt"
expect_has f5_red_service_no_detail   'NETNS_DETAIL mode=service subject=red rc=3 detail_field_present=0 escaped_stderr_bytes=0 result=\[B6_STOP reason=service_netns_unreadable path=/proc/123/ns/net rc=7\]' "$Q/f5.txt"
expect_has f5_green_service_detail    'NETNS_DETAIL mode=service subject=green rc=3 detail_field_present=1 escaped_stderr_bytes=0 result=\[B6_STOP reason=service_netns_unreadable path=/proc/123/ns/net rc=7 detail=identity_read_child_failed diagnostic_file=<scratch>/f5-service-green/ev/ro.0004.service_netns.stderr\]' "$Q/f5.txt"
# No-weakening: two equal namespaces still bind, identically on both subjects.
expect_has f5_red_clean   'NETNS_DETAIL mode=clean subject=red rc=0 detail_field_present=0 escaped_stderr_bytes=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f5.txt"
expect_has f5_green_clean 'NETNS_DETAIL mode=clean subject=green rc=0 detail_field_present=0 escaped_stderr_bytes=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f5.txt"

case "$Q" in /tmp/rp7-r9-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_SCRATCH_UNSAFE=%s\n' "$Q"; exit 97 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_R9_FENCE_END
```

### Round-9 transcript

```text
QA_ROOT=/tmp/rp7-r9-qa.zDE4zE
QA_ENV bash=5.2.37(1)-release coreutils_timeout=8.32 git=2.52.0.windows.1 uid_gid=4096:4096 python=3.14.2
BYTE_IDENTITY red_bytes=99903 red_sha256=11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4 red_cr=0 red_bash_n=0 green_bytes=108301 green_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62 green_cr=0 green_bash_n=0
BODY_BINDING mode=outside subject=red rc=0 outside_bytes=197 outside_is_original=no child_body_sha256=not_replaced name_at_read_time_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
BODY_BINDING mode=outside subject=green rc=3 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced name_at_read_time_sha256=9660b3303631e95817f72c7536939f0eca9e20c0d7b86382a39e4a98a1b26151 result=[B5_STOP reason=status_endpoint_not_evaluable rc=23 detail=transport_error diagnostic_file=<scratch>/f1-outside-green/ev/ro.0001.status_get.stderr]
BODY_BINDING mode=reader subject=red rc=0 outside_bytes=9 outside_is_original=yes child_body_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 name_at_read_time_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
BODY_BINDING mode=reader subject=green rc=1 outside_bytes=9 outside_is_original=yes child_body_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 name_at_read_time_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value]
BODY_BINDING mode=none subject=red rc=0 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced name_at_read_time_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
BODY_BINDING mode=none subject=green rc=0 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced name_at_read_time_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
BODY_BINDING mode=none_armed subject=red rc=1 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced name_at_read_time_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value]
BODY_BINDING mode=none_armed subject=green rc=1 outside_bytes=9 outside_is_original=yes child_body_sha256=not_replaced name_at_read_time_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value]
F1_FIXTURE_DIGESTS armed_body_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 disarmed_body_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821
BIND_RC mode=divert_rc7 subject=red child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
BIND_RC mode=divert_rc7 subject=green child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=7 detail=capture_stream_unbound]
BIND_RC mode=divert_rc0 subject=red child_rc=0 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
BIND_RC mode=divert_rc0 subject=green child_rc=0 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
BIND_RC mode=undeclared subject=red child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe leaf=<scratch>/f2-undeclared-red/ev/ro.0001.undeclared_probe.stdout]
BIND_RC mode=undeclared subject=green child_rc=7 rc=3 child_ran=yes escaped_stderr_bytes=0 stdout_lines=1 result=[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe leaf=<scratch>/f2-undeclared-green/ev/ro.0001.undeclared_probe.stdout]
BIND_RC mode=clean subject=red child_rc=0 rc=0 child_ran=yes escaped_stderr_bytes=0 stdout_lines=2 result=[B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 evidence_file=<scratch>/f2-clean-red/ev/ro.0001.listeners.stdout content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete]
BIND_RC mode=clean subject=green child_rc=0 rc=0 child_ran=yes escaped_stderr_bytes=0 stdout_lines=2 result=[B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 evidence_file=<scratch>/f2-clean-green/ev/ro.0001.listeners.stdout content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete]
RC137_PROVENANCE body=child_spoof subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=137 wall_s=0 spoof_text_in_command_stderr=1 result=[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=no wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30]
RC137_PROVENANCE body=child_spoof subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=6 rc=1 wall_s=1 spoof_text_in_command_stderr=1 result=[fence_failed fence=r9 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no wrapper_stream=body_cannot_write]
RC137_PROVENANCE body=direct_137 subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=1 wall_s=0 spoof_text_in_command_stderr=0 result=[fence_failed fence=r8 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no]
RC137_PROVENANCE body=direct_137 subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=6 rc=1 wall_s=1 spoof_text_in_command_stderr=0 result=[fence_failed fence=r9 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no wrapper_stream=body_cannot_write]
RC137_PROVENANCE body=ignore_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=137 wall_s=4 spoof_text_in_command_stderr=1 result=[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30]
RC137_PROVENANCE body=ignore_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=6 rc=137 wall_s=4 spoof_text_in_command_stderr=1 result=[timeout fence=r9 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30]
BUDGET_ARITHMETIC subject=red wrappers=5 per_fence_nominal_s=900 kill_grace_s=30 computed_s=4650 claimed_s=4650 claim_true=yes
BUDGET_ARITHMETIC subject=green wrappers=6 per_fence_nominal_s=900 kill_grace_s=30 computed_s=5580 claimed_s=5580 claim_true=yes
MAPPING_ASSERTION_PRESENT round8_count_equality=1 round9_count_equality=0 round9_mapping_power=1
NETNS_DETAIL mode=caller subject=red rc=3 detail_field_present=0 escaped_stderr_bytes=0 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=7]
NETNS_DETAIL mode=caller subject=green rc=3 detail_field_present=1 escaped_stderr_bytes=0 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=7 detail=identity_read_child_failed diagnostic_file=<scratch>/f5-caller-green/ev/ro.0001.caller_netns.stderr]
NETNS_DETAIL mode=service subject=red rc=3 detail_field_present=0 escaped_stderr_bytes=0 result=[B6_STOP reason=service_netns_unreadable path=/proc/123/ns/net rc=7]
NETNS_DETAIL mode=service subject=green rc=3 detail_field_present=1 escaped_stderr_bytes=0 result=[B6_STOP reason=service_netns_unreadable path=/proc/123/ns/net rc=7 detail=identity_read_child_failed diagnostic_file=<scratch>/f5-service-green/ev/ro.0004.service_netns.stderr]
NETNS_DETAIL mode=clean subject=red rc=0 detail_field_present=0 escaped_stderr_bytes=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
NETNS_DETAIL mode=clean subject=green rc=0 detail_field_present=0 escaped_stderr_bytes=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
QA_PASS all_assertions=yes
```

## The round-8 fence

Four arm groups. Three of them take the block as their subject, with a real RED against the
round-7 blob at `c708511f` and a real GREEN against the repaired bytes. The first takes an
**assertion** as its subject, because that is what finding 1 is about, and its RED is a
mutant block the assertion is supposed to reject.

| Arm | RED | GREEN |
|---|---|---|
| F1 `return 7` at the top of `wpi_capture` | the round-7 assertion `rc=[0-9]*` **accepts** the mutant: `ASSERTION_POWER round7_on_mutant=accept` | the round-8 assertion **rejects** it: `round8_on_mutant=reject`, because the mutant's rc is neither 0 with an empty capture result nor 3 with the exact documented STOP |
| F1 control: the repaired block itself | round-7 assertion accepts | round-8 assertion accepts - `green_kind=unlinked_leaf_not_rebindable_rc3` on this workstation, `descriptor_rebind_supported_rc0` on Linux, and nothing else |
| F1 control: the round-5 block, whose payload really escapes | both assertions **reject** it (`round7_on_escaping=reject`, `round8_on_escaping=reject`) - the repair did not trade one blind spot for another |
| F2 status leaf name replaced at the reader boundary | the name is re-opened: a child-observed `500` is adjudicated as `200` and `B5_status ... flags=expected` prints at rc 0 | the capture descriptor is read: `B5_FAIL reason=status_endpoint_unexpected_http code=500`, rc 1, unchanged by the substitution |
| F2 namespace leaf name replaced at the reader boundary | `B6_netns ... binding=equal`, rc 0 | `B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]`, rc 3 |
| F2 control: `swap=no` on both subjects | rc 1 `code=500` / rc 3 `netns_mismatch` | identical |
| F2 control: clean `200` + `OK fields=8`, clean equal namespaces | rc 0 accepting | rc 0 accepting - identical |
| F2 control: a stub that binds NO descriptor | reads the name and adjudicates it | `detail=capture_stream_unbound`, rc 3 - there is no fallback to a name |
| F3 fence body that is an immediate `exit 137` | `kind=killed_after_grace`, command exits 137, one second after it started | `fence_failed ... kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no`, command exits 1 |
| F3 control: TERM-ignoring fence body | `kind=killed_after_grace`, exit 137 | `kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes`, exit 137 - the real event is still classified as one, now on the wrapper's own evidence |
| F3 FIFO in place of the document | the prelude blocks outside every wrapper and an independent 3 s timeout stops it; the text claims `aggregate_enforced_by=sequential_per_fence_bounds` | the same behaviour, and the text says `whole_command_bound=none prelude_bounded=no` |
| F3 budget arithmetic | `wrappers=4 computed_s=3720 claimed_s=3720` | `wrappers=5 computed_s=4650 claimed_s=4650`, re-derived from the published text |
| F3 reader field label | the round-7 `READER_BINDING` printf emits an `adjudicated_name_<digest>=` field for bytes GREEN does not adjudicate | zero emissions of that field name; it is `name_at_read_time_sha256=` |
| F4 production capture cannot bind its stdout descriptor | `RP7_STOP reason=capture_stream_not_bindable label=listeners`, which no row preregisters | `B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound`, exactly as row 22 declares |
| F4 control: a caller that declares no token of its own | - | still the generic `RP7_STOP ... label=undeclared_probe`: the repair adds a route, it does not widen one |

Two injections are used and each is named where it occurs. The F2 substitution is injected at
the `wpi_alloc_read_diag` reader-allocation boundary, which is the boundary the auditor used,
so it is not a route the block reaches on its own; what it measures is what the block
*establishes*. The F4 close of the creating write descriptor is injected through a hooked
`wpi_clock_ms` and Bash's dynamic scoping, because it is the only way to make the bind fail
deterministically here - unlinking the leaf, which the carried leaf-race arm does, sometimes
still leaves `/dev/fd/<n>` resolvable on MSYS2, and an arm that reproduces its own
precondition only sometimes is not a fence arm.

```bash
# RP7_R8_FENCE_BEGIN
# Round-8 D026 fence for RP7-WPI-RO. Every arm drives the REAL production caller
# in a FRESH bash process, or the REAL published command TEXT, against two byte
# sets whose identity is asserted first:
#   RED   = the frozen round-7 blob at commit c708511f (92853 B, e695a67b...07f32)
#   GREEN = the repaired worktree file
# One of the four findings is about this document rather than about the block: a
# carried assertion that stopped discriminating. Its arm therefore runs an
# ASSERTION against a mutant, not only a block against an input.
REPO=/c/LAB/Tradingview_LAB_CLEAN
DOC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
BLOCK=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r8-qa.XXXXXX)
RED=$Q/RP7-WPI-RO.round7.sh
GREEN=$BLOCK

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_has(){ grep -q -- "$2" "$3" || { printf 'QA_ASSERT_FAIL name=%s missing=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_hasnt(){ grep -q -- "$2" "$3" && { printf 'QA_ASSERT_FAIL name=%s unexpected=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; return 0; }

printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_timeout=%s git=%s uid_gid=%s:%s\n' \
    "$BASH_VERSION" "$(/usr/bin/timeout --version | head -1 | sed 's/.* //')" \
    "$(git --version | sed 's/.* //')" "$(id -u)" "$(id -g)"

# --- byte identity of both subjects -----------------------------------------
git -C "$REPO" cat-file blob c708511f:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$RED"
RED_SHA=$(sha256sum < "$RED" | cut -d' ' -f1);     RED_BYTES=$(wc -c < "$RED")
GREEN_SHA=$(sha256sum < "$GREEN" | cut -d' ' -f1); GREEN_BYTES=$(wc -c < "$GREEN")
RED_CR=$(tr -cd '\r' < "$RED" | wc -c);  GREEN_CR=$(tr -cd '\r' < "$GREEN" | wc -c)
bash --noprofile --norc -n "$RED";   RED_N=$?
bash --noprofile --norc -n "$GREEN"; GREEN_N=$?
printf 'BYTE_IDENTITY red_bytes=%s red_sha256=%s red_cr=%s red_bash_n=%s green_bytes=%s green_sha256=%s green_cr=%s green_bash_n=%s\n' \
    "$RED_BYTES" "$RED_SHA" "$RED_CR" "$RED_N" "$GREEN_BYTES" "$GREEN_SHA" "$GREEN_CR" "$GREEN_N"
expect_eq r8_red_sha256   "$RED_SHA"   e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32
expect_eq r8_red_bytes    "$RED_BYTES" 92853
expect_eq r8_green_sha256 "$GREEN_SHA" 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
expect_eq r8_green_bytes  "$GREEN_BYTES" 108301
expect_rc r8_red_cr "$RED_CR" 0
expect_rc r8_green_cr "$GREEN_CR" 0
expect_rc r8_red_bash_n "$RED_N" 0
expect_rc r8_green_bash_n "$GREEN_N" 0

# ===========================================================================
# FINDING 1 (HIGH) - a carried assertion was relaxed to `rc=[0-9]*` and stopped
# rejecting an unrelated capture regression. The SUBJECT of this group is the
# ASSERTION, so the RED is a MUTANT BLOCK - `return 7` inserted at the top of
# `wpi_capture`, which never touches the leaf and is therefore invisible to any
# assertion that only inspects the outside file. The same three outputs are fed
# to both the round-7 assertion and the round-8 one. The round-6 fence carries
# the repaired assertion itself; this group is the executed proof that the
# repair restored power the round-7 edit removed.
# ===========================================================================
git -C "$REPO" cat-file blob 1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$Q/RP7-WPI-RO.round5.sh"
sed '/^wpi_capture() {/a\    return 7' "$GREEN" > "$Q/mutant-return7.sh"
bash --noprofile --norc -n "$Q/mutant-return7.sh"; MUT_N=$?
cat > "$Q/f1_arm.sh" <<'ARM'
S="$1"; W="$2"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10; WPI_PROBE_SEQ=0
OUTSIDE="$W/outside.txt"; printf 'ORIGINAL\n' > "$OUTSIDE"
HOOK=0
wpi_clock_ms(){
  HOOK=$((HOOK+1))
  if [ "$HOOK" -eq 1 ]; then rm -- "$WPI_CAP_OUT"; ln -- "$OUTSIDE" "$WPI_CAP_OUT"; fi
  WPI_LINE="$HOOK"
}
( wpi_capture leaf_race /usr/bin/printf 'CAPTURED\n' ) > "$W/cap.out" 2>&1
rc=$?
printf 'LEAF_RACE rc=%s outside_text=%s outside_bytes=%s payload_left_the_tree=%s capture_result=[%s]\n' \
  "$rc" "$(tr -d '\n' < "$OUTSIDE")" "$(wc -c < "$OUTSIDE")" \
  "$(grep -q CAPTURED "$OUTSIDE" && echo yes || echo no)" \
  "$(sed -e "s#$W#<scratch>#g" "$W/cap.out" | tr '\n' ' ' | sed 's/ *$//')"
ARM
r8_classify(){
  if grep -q 'LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=\[\]$' "$1"; then
    printf 'descriptor_rebind_supported_rc0\n'
  elif grep -q 'LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=\[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro\.0001\.leaf_race\.stdout\]$' "$1"; then
    printf 'unlinked_leaf_not_rebindable_rc3\n'
  else
    printf 'unclassified\n'
  fi
}
r8_new(){ case "$(r8_classify "$1")" in unclassified) printf 'reject\n' ;; *) printf 'accept\n' ;; esac; }
r8_old(){ if grep -q 'LEAF_RACE rc=[0-9]* outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no' "$1"; then printf 'accept\n'; else printf 'reject\n'; fi; }
for subject in escaping_round5 green mutant_return7; do
  case "$subject" in
    escaping_round5) S=$Q/RP7-WPI-RO.round5.sh ;;
    green)           S=$GREEN ;;
    mutant_return7)  S=$Q/mutant-return7.sh ;;
  esac
  bash --noprofile --norc "$Q/f1_arm.sh" "$S" "$Q/f1-$subject" > "$Q/f1-$subject.txt" 2>&1
  printf '%-16s %s\n' "$subject" "$(cat "$Q/f1-$subject.txt")"
done
printf 'ASSERTION_POWER mutant_bash_n=%s round7_on_green=%s round7_on_mutant=%s round7_on_escaping=%s round8_on_green=%s round8_on_mutant=%s round8_on_escaping=%s green_kind=%s\n' \
  "$MUT_N" \
  "$(r8_old "$Q/f1-green.txt")" "$(r8_old "$Q/f1-mutant_return7.txt")" "$(r8_old "$Q/f1-escaping_round5.txt")" \
  "$(r8_new "$Q/f1-green.txt")" "$(r8_new "$Q/f1-mutant_return7.txt")" "$(r8_new "$Q/f1-escaping_round5.txt")" \
  "$(r8_classify "$Q/f1-green.txt")"
expect_rc f1_mutant_parses "$MUT_N" 0
# The mutation is unrelated to what the arm is about, and the arm still shows the
# payload confined - which is exactly why only a status pin can catch it.
expect_has f1_mutant_confined 'payload_left_the_tree=no' "$Q/f1-mutant_return7.txt"
expect_has f1_escaping_red 'LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes' "$Q/f1-escaping_round5.txt"
expect_eq f1_round7_accepts_mutant "$(r8_old "$Q/f1-mutant_return7.txt")" accept
expect_eq f1_round8_rejects_mutant "$(r8_new "$Q/f1-mutant_return7.txt")" reject
expect_eq f1_round8_accepts_green  "$(r8_new "$Q/f1-green.txt")"          accept
expect_eq f1_both_reject_escaping  "$(r8_old "$Q/f1-escaping_round5.txt")$(r8_new "$Q/f1-escaping_round5.txt")" rejectreject

# ===========================================================================
# FINDING 2 (HIGH) - the status and namespace child observations were still read
# by NAME, so replacing the leaf name between the child's exit and the read
# turned an observed HTTP 500 into an accepting 200 and two unequal namespaces
# into an equal pair. The fixture is the auditor's: the ONLY hook is at the
# `wpi_alloc_read_diag` reader-allocation boundary, and the capture stub binds
# the same two descriptors production binds. `swap=no` is the control on every
# subject, and the clean-input controls below are the no-weakening arms.
# ===========================================================================
# ROUND-9 CHANGE, subject-specific fixture: the parser's accepting record gained
# the digest of the bytes the parser itself read, because round 8 rendered
# `body_sha256` from a separate `sha256sum` over the leaf NAME and an executed
# fixture made that field report the child's ARMED body beside an accepting
# DISARMED verdict (Codex round-8 part B finding 1). A stub standing in for a
# parser must emit the record ITS OWN subject's parser can emit, so the record is
# now chosen per subject and pinned as a constant for each - it is not read from
# the subject, which would make the check unfalsifiable. Every other fixture,
# mode and expected disposition in this group is unchanged.
cat > "$Q/f2_arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"; swap="$4"; OKREC="$5"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/false; WPI_PYTHON3=/usr/bin/false; WPI_READLINK=/usr/bin/false; WPI_MAINPID=123
WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
wpi_capture(){
  local label="$1"
  WPI_CAP_OUT="$W/$label.out"; WPI_CAP_ERR="$W/$label.err"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
  case "$label:$mode" in
    status_get:status|status_get:status_clean) printf '500\n' > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
    status_json:status|status_json:status_clean) printf '%s\n' "$OKREC" > "$WPI_CAP_OUT" ;;
    caller_netns:netns|caller_netns:netns_clean) printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
    service_netns:netns) printf 'net:[200]\n' > "$WPI_CAP_OUT" ;;
    service_netns:netns_clean) printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
    *) exit 96 ;;
  esac
  case "$mode" in
    status_clean) [ "$label" != status_get ] || printf '200\n' > "$WPI_CAP_OUT" ;;
  esac
  # The stub allocates the two descriptors production allocates. A stub that sets
  # only the NAMES is no longer standing in for `wpi_capture`, and GREEN STOPs on
  # it with detail=capture_stream_unbound rather than falling back to a name.
  case "$swap" in
    unbound) : ;;
    *) exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR" ;;
  esac
}
wpi_alloc_read_diag(){
  local label="$1"
  if [ "$swap" = yes ] && [ ! -f "$W/child-observation.out" ]; then
    case "$WPI_CAP_OUT" in
      */status_get.out) cp "$WPI_CAP_OUT" "$W/child-observation.out"; rm -- "$WPI_CAP_OUT"; printf '200\n' > "$WPI_CAP_OUT" ;;
      */service_netns.out) cp "$WPI_CAP_OUT" "$W/child-observation.out"; rm -- "$WPI_CAP_OUT"; printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
    esac
  fi
  WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1))
  WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
  wpi_open_leaf "$WPI_READ_DIAG"; WPI_READ_DIAG_FD="$WPI_LEAF_FD"
}
case "$mode" in
  status|status_clean) wpi_assert_status ;;
  netns|netns_clean)   wpi_assert_netns_binding ;;
esac
ARM
for mode in status netns; do
  for swap in no yes; do
    for subject in red green; do
      if [ "$subject" = red ]; then S="$RED"; OKREC='OK fields=8'
      else S="$GREEN"; OKREC='OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000'; fi
      W=$Q/f2-$mode-$swap-$subject
      bash --noprofile --norc "$Q/f2_arm.sh" "$S" "$W" "$mode" "$swap" "$OKREC" > "$W.txt" 2>&1; rc=$?
      case "$mode" in status) NAMEF="$W/status_get.out" ;; netns) NAMEF="$W/service_netns.out" ;; esac
      if [ -f "$W/child-observation.out" ]; then CH=$(sha256sum < "$W/child-observation.out" | cut -d' ' -f1); else CH=not_replaced; fi
      printf 'NAME_REOPEN mode=%s swap=%s subject=%s rc=%s child_sha256=%s name_at_read_time_sha256=%s result=[%s]\n' \
        "$mode" "$swap" "$subject" "$rc" "$CH" "$(sha256sum < "$NAMEF" | cut -d' ' -f1)" \
        "$(sed -e "s#$Q#<scratch>#g" "$W.txt" | tr '\n' ' ' | sed 's/ *$//')"
    done
  done
done > "$Q/f2.txt"
for mode in status_clean netns_clean; do
  for subject in red green; do
    if [ "$subject" = red ]; then S="$RED"; OKREC='OK fields=8'
    else S="$GREEN"; OKREC='OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000'; fi
    W=$Q/f2-$mode-$subject
    bash --noprofile --norc "$Q/f2_arm.sh" "$S" "$W" "$mode" no "$OKREC" > "$W.txt" 2>&1; rc=$?
    printf 'CLEAN_CONTROL mode=%s subject=%s rc=%s result=[%s]\n' "$mode" "$subject" "$rc" \
      "$(sed -e "s#$Q#<scratch>#g" "$W.txt" | tr '\n' ' ' | sed 's/ *$//')"
  done
done >> "$Q/f2.txt"
for mode in status netns; do
  for subject in red green; do
    if [ "$subject" = red ]; then S="$RED"; OKREC='OK fields=8'
    else S="$GREEN"; OKREC='OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000'; fi
    W=$Q/f2-$mode-unbound-$subject
    bash --noprofile --norc "$Q/f2_arm.sh" "$S" "$W" "$mode" unbound "$OKREC" > "$W.txt" 2>&1; rc=$?
    printf 'NO_NAME_FALLBACK mode=%s subject=%s rc=%s result=[%s]\n' "$mode" "$subject" "$rc" \
      "$(sed -e "s#$Q#<scratch>#g" "$W.txt" | tr '\n' ' ' | sed 's/ *$//')"
  done
done >> "$Q/f2.txt"
cat "$Q/f2.txt"
# RED: the substitution is executed and it changes the verdict.
expect_has f2_red_status_swapped  'NAME_REOPEN mode=status swap=yes subject=red rc=0 .* result=\[B5_status http=200 ' "$Q/f2.txt"
expect_has f2_red_netns_swapped   'NAME_REOPEN mode=netns swap=yes subject=red rc=0 .* result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f2.txt"
# GREEN: the same substitution changes nothing, because no name is resolved after
# the child exits. The child's own observation is what the row adjudicates.
expect_has f2_green_status_swapped 'NAME_REOPEN mode=status swap=yes subject=green rc=1 .* result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f2.txt"
expect_has f2_green_netns_swapped  'NAME_REOPEN mode=netns swap=yes subject=green rc=3 .* result=\[B6_STOP reason=netns_mismatch caller=net:\[100\] service=net:\[200\]\]' "$Q/f2.txt"
# swap=no controls: both subjects reach the same truthful verdict.
expect_has f2_red_status_plain   'NAME_REOPEN mode=status swap=no subject=red rc=1 child_sha256=not_replaced .* result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f2.txt"
expect_has f2_green_status_plain 'NAME_REOPEN mode=status swap=no subject=green rc=1 child_sha256=not_replaced .* result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f2.txt"
expect_has f2_red_netns_plain    'NAME_REOPEN mode=netns swap=no subject=red rc=3 child_sha256=not_replaced .* result=\[B6_STOP reason=netns_mismatch caller=net:\[100\] service=net:\[200\]\]' "$Q/f2.txt"
expect_has f2_green_netns_plain  'NAME_REOPEN mode=netns swap=no subject=green rc=3 child_sha256=not_replaced .* result=\[B6_STOP reason=netns_mismatch caller=net:\[100\] service=net:\[200\]\]' "$Q/f2.txt"
# No-weakening: clean input still reaches the accepting line on BOTH subjects.
expect_has f2_clean_status_red   'CLEAN_CONTROL mode=status_clean subject=red rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2.txt"
expect_has f2_clean_status_green 'CLEAN_CONTROL mode=status_clean subject=green rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2.txt"
expect_has f2_clean_netns_red    'CLEAN_CONTROL mode=netns_clean subject=red rc=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f2.txt"
expect_has f2_clean_netns_green  'CLEAN_CONTROL mode=netns_clean subject=green rc=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f2.txt"
# There is no fallback to a name: an unbound stream STOPs with the row's token.
expect_has f2_unbound_status_green 'NO_NAME_FALLBACK mode=status subject=green rc=3 result=\[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=capture_stream_unbound\]' "$Q/f2.txt"
expect_has f2_unbound_netns_green  'NO_NAME_FALLBACK mode=netns subject=green rc=3 result=\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=capture_stream_unbound\]' "$Q/f2.txt"
expect_has f2_unbound_status_red   'NO_NAME_FALLBACK mode=status subject=red rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f2.txt"
# The substitution really happened: the child's bytes and the bytes the NAME
# resolved to at read time differ on both subjects. Only the subject that reads
# the DESCRIPTOR is unaffected by that difference.
SW_RED=$(sed -n 's/^NAME_REOPEN mode=status swap=yes subject=red rc=[0-9]* child_sha256=\([0-9a-f]*\) name_at_read_time_sha256=\([0-9a-f]*\) .*/\1 \2/p' "$Q/f2.txt")
SW_GREEN=$(sed -n 's/^NAME_REOPEN mode=status swap=yes subject=green rc=[0-9]* child_sha256=\([0-9a-f]*\) name_at_read_time_sha256=\([0-9a-f]*\) .*/\1 \2/p' "$Q/f2.txt")
printf 'READER_SUBSTITUTION red_child_ne_name=%s green_child_ne_name=%s\n' \
  "$([ "${SW_RED% *}" != "${SW_RED#* }" ] && echo yes || echo no)" \
  "$([ "${SW_GREEN% *}" != "${SW_GREEN#* }" ] && echo yes || echo no)"
expect_eq f2_swap_effective_red   "$([ "${SW_RED% *}" != "${SW_RED#* }" ] && echo yes || echo no)" yes
expect_eq f2_swap_effective_green "$([ "${SW_GREEN% *}" != "${SW_GREEN#* }" ] && echo yes || echo no)" yes

# ===========================================================================
# FINDING 3 (MEDIUM) - the published command called every rc 137 its own
# kill-after event and claimed a bound over a command whose prelude no wrapper
# encloses. Both subjects are the published command TEXT: RED from commit
# c708511f, GREEN from this document. Each is retargeted into a scratch tree and
# its bound scaled from `900s`/`30s` to `1s`/`2s`; nothing else is altered.
# `ignore_term` is the control - a real kill-after must still be classified as
# one, on both subjects.
# ===========================================================================
git -C "$REPO" cat-file blob c708511f:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md > "$Q/SELF_QA_RP7.round7.md"
# ROUND-9 CHANGE, subject pinned: this group's GREEN is the round-8 command TEXT at
# `bb8546e6`, not the live document. Round 8 made exactly this change to the round-7
# fence, for exactly this reason - a carried group that re-adjudicates a moving
# subject stops measuring the transition it was written for. The round-9 fence
# measures round-8 -> round-9 on the live text; this group keeps measuring
# round-7 -> round-8 forever. RED is unchanged.
git -C "$REPO" cat-file blob bb8546e6:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md > "$Q/SELF_QA_RP7.round8.md"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$Q/SELF_QA_RP7.round7.md" > "$Q/cmd-red.txt"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$Q/SELF_QA_RP7.round8.md" > "$Q/cmd-green.txt"
for body in direct_137 ignore_term; do
  for subject in red green; do
    T=$Q/f3-$body-$subject; mkdir -p "$T"
    case "$body" in
      direct_137) PAYLOAD="exit 137\n" ;;
      ignore_term) PAYLOAD="trap '' TERM\n/usr/bin/sleep 30\n" ;;
    esac
    # The newest fence of each subject carries the payload; every other fence
    # exits 0. RED has no round-8 fence, so its newest is the round-7 one.
    { if [ "$subject" = green ]; then printf "# RP7_R8_FENCE_BEGIN\n${PAYLOAD}# RP7_R8_FENCE_END\n"
                                       printf '# RP7_R7_FENCE_BEGIN\nexit 0\n# RP7_R7_FENCE_END\n'
      else printf '# RP7_R8_FENCE_BEGIN\nexit 0\n# RP7_R8_FENCE_END\n'
           printf "# RP7_R7_FENCE_BEGIN\n${PAYLOAD}# RP7_R7_FENCE_END\n"; fi
      printf '# RP7_R6_FENCE_BEGIN\nexit 0\n# RP7_R6_FENCE_END\n'
      printf '# RP7_QA_FENCE_BEGIN\nexit 0\n# RP7_QA_FENCE_END\n'
      printf '# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n'; } > "$T/SELF_QA_RP7.md"
    # The /tmp expression runs FIRST for the reason the round-6 fence documents:
    # this scratch tree is itself under /tmp/rp7-, so retargeting `cd` first
    # would let the /tmp rule rewrite the new target as well.
    sed -e "s#/tmp/rp7-#$T/body-#g" \
        -e "s#^cd /c/LAB/.*#cd $T#" \
        -e "s#--kill-after=30s 900s#--kill-after=2s 1s#g" \
        "$Q/cmd-$subject.txt" > "$T/run.sh"
    t0=$SECONDS
    timeout 120 bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
    printf 'RC137_PROVENANCE body=%s subject=%s cd_retargeted=%s real_fence_bodies=%s scaled_wrappers=%s rc=%s wall_s=%s result=[%s]\n' \
      "$body" "$subject" \
      "$(grep -c "^cd $T\$" "$T/run.sh")" \
      "$(grep -cE '/tmp/rp7-r[4-8]-fence-body\.sh' "$T/run.sh")" \
      "$(grep -c -- '--kill-after=2s 1s' "$T/run.sh")" \
      "$rc" "$((SECONDS-t0))" \
      "$(grep '^PUBLISHED_COMMAND_RESULT=' "$T/out.txt" | head -1 | sed 's/^PUBLISHED_COMMAND_RESULT=//')"
  done
done > "$Q/f3.txt"
cat "$Q/f3.txt"
# RED calls an immediate `exit 137` its own kill-after event and exits 137.
expect_has f3_red_misattributes_137 'RC137_PROVENANCE body=direct_137 subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 wall_s=[0-9] result=\[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"
# GREEN calls it what it is: a 137 its own wrapper did not send, hence not a timeout.
expect_has f3_green_attributes_137 'RC137_PROVENANCE body=direct_137 subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=1 wall_s=[0-9] result=\[fence_failed fence=r8 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no\]' "$Q/f3.txt"
# Control: a REAL kill-after is still classified as one, and GREEN now says so on
# the evidence of the wrapper's own diagnostic rather than on the number alone.
expect_has f3_red_real_kill   'RC137_PROVENANCE body=ignore_term subject=red .* rc=137 .* result=\[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"
expect_has f3_green_real_kill 'RC137_PROVENANCE body=ignore_term subject=green .* rc=137 .* result=\[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f3.txt"

# The prelude of BOTH texts is outside every wrapper - a FIFO in place of the
# document blocks the first extraction and an INDEPENDENT timeout has to stop it.
# The difference the repair makes is not in the behaviour, it is in what the text
# CLAIMS about the behaviour.
for subject in red green; do
  T=$Q/f3-prelude-$subject; mkdir -p "$T"; mkfifo "$T/SELF_QA_RP7.md"
  sed -e "s#/tmp/rp7-#$T/body-#g" -e "s#^cd /c/LAB/.*#cd $T#" "$Q/cmd-$subject.txt" > "$T/run.sh"
  t0=$SECONDS
  timeout --signal=TERM --kill-after=1s 3s bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
  printf 'UNBOUNDED_PRELUDE subject=%s outer_test_rc=%s elapsed_s=%s stdout_bytes=%s outer_wrapper_in_text=%s claims_whole_command_bound=%s states_prelude_unbounded=%s\n' \
    "$subject" "$rc" "$((SECONDS-t0))" "$(wc -c < "$T/out.txt")" \
    "$(grep -c 'RP7_AGGREGATE_WRAPPER' "$Q/cmd-$subject.txt")" \
    "$(grep -c 'aggregate_enforced_by=sequential_per_fence_bounds' "$Q/cmd-$subject.txt")" \
    "$(grep -c 'prelude_bounded=no' "$Q/cmd-$subject.txt")"
done > "$Q/f3prelude.txt"
cat "$Q/f3prelude.txt"
# The gate is `outer_test_rc=124` with no stdout: an INDEPENDENT timeout had to stop the
# command before it produced anything, which is the whole claim. The wall clock is bounded
# to the outer 3 s window plus its 1 s grace and reported, not pinned to one integer - a
# pinned second would be a flaky assertion with no discriminating power of its own.
expect_has f3_red_claims_unenforced_bound 'UNBOUNDED_PRELUDE subject=red outer_test_rc=124 elapsed_s=[34] stdout_bytes=0 outer_wrapper_in_text=0 claims_whole_command_bound=1 states_prelude_unbounded=0' "$Q/f3prelude.txt"
expect_has f3_green_states_the_truth      'UNBOUNDED_PRELUDE subject=green outer_test_rc=124 elapsed_s=[34] stdout_bytes=0 outer_wrapper_in_text=0 claims_whole_command_bound=0 states_prelude_unbounded=1' "$Q/f3prelude.txt"

# The budget is re-derived from the published text, not read from prose.
for subject in red green; do
  W=$(grep -cE 'timeout (--verbose )?--signal=TERM --kill-after=30s 900s bash --noprofile --norc' "$Q/cmd-$subject.txt")
  CLAIM=$(sed -n 's/.*\(aggregate_bound_s\|fence_timeout_budget_s\)=\([0-9]*\).*/\2/p' "$Q/cmd-$subject.txt" | head -1)
  printf 'BUDGET_ARITHMETIC subject=%s wrappers=%s per_fence_nominal_s=900 kill_grace_s=30 computed_s=%s claimed_s=%s claim_true=%s\n' \
    "$subject" "$W" "$((W*(900+30)))" "$CLAIM" "$([ "$((W*(900+30)))" = "$CLAIM" ] && echo yes || echo no)"
done > "$Q/f3budget.txt"
cat "$Q/f3budget.txt"
expect_has f3_red_budget   'BUDGET_ARITHMETIC subject=red wrappers=4 per_fence_nominal_s=900 kill_grace_s=30 computed_s=3720 claimed_s=3720 claim_true=yes' "$Q/f3budget.txt"
expect_has f3_green_budget 'BUDGET_ARITHMETIC subject=green wrappers=5 per_fence_nominal_s=900 kill_grace_s=30 computed_s=4650 claimed_s=4650 claim_true=yes' "$Q/f3budget.txt"

# The mislabeled reader field: the round-7 fence printed `adjudicated_name_sha256`
# for a digest of bytes GREEN expressly does NOT adjudicate.
# The check is on EMISSIONS of the field - `<name>=` - not on mentions of it: this
# fence and the round-8 report both have to name the old field to say what was
# wrong with it, and a check that forbade the word would forbid the explanation.
# The token is assembled from two pieces so that these two lines do not themselves
# contain it: a self-counting pattern would make the check unfalsifiable.
OLDF='adjudicated_name''_sha256='
R7_FIELD=$(git -C "$REPO" cat-file blob c708511f:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md | grep -c -- "$OLDF")
R8_FIELD=$(grep -c -- "$OLDF" "$DOC")
# The renamed field is counted at its EMISSION SITE - the round-7 fence's printf - not
# across the document: a document-wide count would grow every time a transcript containing
# the field is pasted back in, and a number that moves when the file is edited cannot be
# reproduced by a third party running the same command.
R8_RENAMED=$(sed -n '/^# RP7_R7_FENCE_BEGIN$/,/^# RP7_R7_FENCE_END$/p' "$DOC" | grep -c 'name_at_read_time_sha256=')
printf 'READER_FIELD_LABEL round7_mislabeled_occurrences=%s round8_mislabeled_occurrences=%s round8_renamed_occurrences=%s\n' \
  "$R7_FIELD" "$R8_FIELD" "$R8_RENAMED"
expect_rc f3_r8_no_mislabel "$R8_FIELD" 0
[ "$R7_FIELD" -ge 1 ] || { printf 'QA_ASSERT_FAIL name=f3_r7_had_mislabel got=%s\n' "$R7_FIELD"; exit 90; }
[ "$R8_RENAMED" -ge 1 ] || { printf 'QA_ASSERT_FAIL name=f3_r8_renamed got=%s\n' "$R8_RENAMED"; exit 90; }

# ===========================================================================
# FINDING 4 (MEDIUM) - a PRODUCTION descriptor-bind inability exited inside
# `wpi_capture` as a generic `RP7_STOP`, so the row-22 STOP the draft declares
# was reachable only from a stub. This arm uses the REAL capture, the real
# production caller, the real bounding wrapper and a real child.
#
# ROUND-9 CHANGE, injection replaced because the round-8 injection was not valid
# closure evidence. Round 8 closed the creating write descriptor from a hooked
# `wpi_clock_ms` whose FIRST call happens BEFORE the child subshell's stdout
# redirection. Bash could then not establish that redirection, so the child this
# arm claims to exercise never ran at all, the resulting failure was discarded, a
# raw shell diagnostic escaped, and the arm passed on a token that says `rc=0`
# (Codex round-9 part B finding 2 - the same finding that made the block stop
# printing a caller-supplied rc literal).
#
# The injection is now the STDOUT capture leaf's descriptor - the one stream BOTH
# subjects bind, so both are measured on the same failure. The leaf is created by
# the real allocator and its descriptor is then replaced with the write end of
# a pipe that drains into that same leaf. `/dev/fd/<n>` of a pipe cannot be
# re-opened on Linux or on MSYS2, so the POST-CHILD bind fails deterministically -
# and the child runs to completion first, through the descriptor it inherits,
# leaving a marker and its own status. Unlinking the leaf, which the carried
# leaf-race arm does, is not deterministic here: MSYS2 sometimes still resolves
# `/dev/fd/<n>` for a leaf whose name has just been removed, and an arm that
# reproduces its own precondition only sometimes is not a fence arm.
#
# Nothing else is stubbed. The child's marker and its own rc are asserted, so the
# arm now establishes the fact its token states; the arm also asserts that NO
# unstructured line escapes. The third subject is the no-weakening control: a
# caller that declares NO row-specific token must still fail closed on the
# generic STOP, so the repair adds a route rather than widening one.
# ===========================================================================
cat > "$Q/f4_arm.sh" <<'ARM'
S="$1"; W="$2"; caller="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10
{ printf '#!/bin/sh\nprintf x > "%s"\n' "$W/child-ran.marker"
  printf 'printf "LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\\n"\n'; } > "$W/fake-ss.sh"
chmod 755 "$W/fake-ss.sh"; WPI_SS="$W/fake-ss.sh"
eval "wpi_real_open_leaf() $(declare -f wpi_open_leaf | sed '1d')"
wpi_open_leaf(){
  wpi_real_open_leaf "$1"
  case "$1" in *.listeners.stdout|*.undeclared_probe.stdout) exec {WPI_LEAF_FD}> >(cat >> "$1") ;; esac
}
case "$caller" in
  listeners)  wpi_assert_listener_set ;;
  undeclared) wpi_capture undeclared_probe "$WPI_SS" -H -ltn ;;
esac
ARM
for spec in 'red|listeners' 'green|listeners' 'green|undeclared'; do
  subject=${spec%%|*}; caller=${spec#*|}
  if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
  W=$Q/f4-$subject-$caller
  bash --noprofile --norc "$Q/f4_arm.sh" "$S" "$W" "$caller" > "$W.txt" 2> "$W.err"; rc=$?
  printf 'ROW22_BIND_INABILITY subject=%s caller=%s rc=%s child_ran=%s escaped_stderr_bytes=%s draft_declared_b6_token=%s generic_rp7_token=%s adjudicated_line=[%s]\n' \
    "$subject" "$caller" "$rc" \
    "$([ -f "$W/child-ran.marker" ] && echo yes || echo no)" "$(wc -c < "$W.err")" \
    "$(grep -c 'B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound' "$W.txt")" \
    "$(grep -c '^RP7_STOP reason=capture_stream_not_bindable ' "$W.txt")" \
    "$(grep -E '^(RP7|B6)_STOP ' "$W.txt" | head -1 | sed -e "s#$Q#<scratch>#g")"
done > "$Q/f4.txt"
cat "$Q/f4.txt"
expect_has f4_red_generic 'ROW22_BIND_INABILITY subject=red caller=listeners rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=\[RP7_STOP reason=capture_stream_not_bindable label=listeners leaf=<scratch>/f4-red-listeners/ev/ro.0001.listeners.stdout\]' "$Q/f4.txt"
expect_has f4_green_row_specific 'ROW22_BIND_INABILITY subject=green caller=listeners rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=1 generic_rp7_token=0 adjudicated_line=\[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound\]' "$Q/f4.txt"
expect_has f4_generic_still_reachable 'ROW22_BIND_INABILITY subject=green caller=undeclared rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=\[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe leaf=<scratch>/f4-green-undeclared/ev/ro.0001.undeclared_probe.stdout\]' "$Q/f4.txt"

case "$Q" in /tmp/rp7-r8-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_SCRATCH_UNSAFE=%s\n' "$Q"; exit 97 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_R8_FENCE_END
```

### Round-8 transcript

```text
QA_ROOT=/tmp/rp7-r8-qa.e2fQcs
QA_ENV bash=5.2.37(1)-release coreutils_timeout=8.32 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=92853 red_sha256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32 red_cr=0 red_bash_n=0 green_bytes=108301 green_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62 green_cr=0 green_bash_n=0
escaping_round5  LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes capture_result=[]
green            LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro.0001.leaf_race.stdout]
mutant_return7   LEAF_RACE rc=7 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[]
ASSERTION_POWER mutant_bash_n=0 round7_on_green=accept round7_on_mutant=accept round7_on_escaping=reject round8_on_green=accept round8_on_mutant=reject round8_on_escaping=reject green_kind=unlinked_leaf_not_rebindable_rc3
NAME_REOPEN mode=status swap=no subject=red rc=1 child_sha256=not_replaced name_at_read_time_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NAME_REOPEN mode=status swap=no subject=green rc=1 child_sha256=not_replaced name_at_read_time_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NAME_REOPEN mode=status swap=yes subject=red rc=0 child_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 name_at_read_time_sha256=c11e3f4837efde2441e23a7b9da02131f53bf59fddeb7147c4ab81afe400460f result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
NAME_REOPEN mode=status swap=yes subject=green rc=1 child_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 name_at_read_time_sha256=c11e3f4837efde2441e23a7b9da02131f53bf59fddeb7147c4ab81afe400460f result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NAME_REOPEN mode=netns swap=no subject=red rc=3 child_sha256=not_replaced name_at_read_time_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
NAME_REOPEN mode=netns swap=no subject=green rc=3 child_sha256=not_replaced name_at_read_time_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
NAME_REOPEN mode=netns swap=yes subject=red rc=0 child_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 name_at_read_time_sha256=48dc7f125f7cb9815afd6af30615b55fbdf17137a1128e4aec1ae9e4dd525c4b result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
NAME_REOPEN mode=netns swap=yes subject=green rc=3 child_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 name_at_read_time_sha256=48dc7f125f7cb9815afd6af30615b55fbdf17137a1128e4aec1ae9e4dd525c4b result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
CLEAN_CONTROL mode=status_clean subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
CLEAN_CONTROL mode=status_clean subject=green rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
CLEAN_CONTROL mode=netns_clean subject=red rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
CLEAN_CONTROL mode=netns_clean subject=green rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
NO_NAME_FALLBACK mode=status subject=red rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NO_NAME_FALLBACK mode=status subject=green rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=capture_stream_unbound]
NO_NAME_FALLBACK mode=netns subject=red rc=3 result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
NO_NAME_FALLBACK mode=netns subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=capture_stream_unbound]
READER_SUBSTITUTION red_child_ne_name=yes green_child_ne_name=yes
RC137_PROVENANCE body=direct_137 subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 wall_s=1 result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
RC137_PROVENANCE body=direct_137 subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=1 wall_s=0 result=[fence_failed fence=r8 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no]
RC137_PROVENANCE body=ignore_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 wall_s=4 result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
RC137_PROVENANCE body=ignore_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=5 rc=137 wall_s=4 result=[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30]
UNBOUNDED_PRELUDE subject=red outer_test_rc=124 elapsed_s=3 stdout_bytes=0 outer_wrapper_in_text=0 claims_whole_command_bound=1 states_prelude_unbounded=0
UNBOUNDED_PRELUDE subject=green outer_test_rc=124 elapsed_s=3 stdout_bytes=0 outer_wrapper_in_text=0 claims_whole_command_bound=0 states_prelude_unbounded=1
BUDGET_ARITHMETIC subject=red wrappers=4 per_fence_nominal_s=900 kill_grace_s=30 computed_s=3720 claimed_s=3720 claim_true=yes
BUDGET_ARITHMETIC subject=green wrappers=5 per_fence_nominal_s=900 kill_grace_s=30 computed_s=4650 claimed_s=4650 claim_true=yes
READER_FIELD_LABEL round7_mislabeled_occurrences=5 round8_mislabeled_occurrences=0 round8_renamed_occurrences=1
ROW22_BIND_INABILITY subject=red caller=listeners rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=[RP7_STOP reason=capture_stream_not_bindable label=listeners leaf=<scratch>/f4-red-listeners/ev/ro.0001.listeners.stdout]
ROW22_BIND_INABILITY subject=green caller=listeners rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=1 generic_rp7_token=0 adjudicated_line=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
ROW22_BIND_INABILITY subject=green caller=undeclared rc=3 child_ran=yes escaped_stderr_bytes=0 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe leaf=<scratch>/f4-green-undeclared/ev/ro.0001.undeclared_probe.stdout]
QA_PASS all_assertions=yes
```

What that transcript shows, line by line:

- `BYTE_IDENTITY` fixes both subjects before any arm runs: RED is exactly the audited 92853 B
  / `e695a67b...07f32`, GREEN is the delivered file, both LF-only and both `bash -n` clean.
- `ASSERTION_POWER` is finding 1, and it is the only line in this suite whose subject is an
  assertion rather than a block. `round7_on_mutant=accept round8_on_mutant=reject` is the
  executed statement that the round-7 edit removed discriminating power and that round 8
  restored it. `round7_on_escaping=reject round8_on_escaping=reject` is the control that the
  restoration did not trade one blind spot for another: the round-5 block, whose payload
  really does leave the evidence tree, is rejected by both. `green_kind` records which of the
  two legitimate outcomes this workstation produced, and the assertion accepts nothing else.
- The three `LEAF_RACE` lines above it are the raw material both assertions were applied to.
  The mutant's line is the important one: `payload_left_the_tree=no`, `outside_text=ORIGINAL`
  - everything the arm was watching is unchanged, and only `rc=7` gives the regression away.
  That is exactly why an assertion that does not pin the status cannot see it.
- `NAME_REOPEN ... subject=red` is finding 2 reproduced on the audited bytes: with the leaf
  name replaced at the reader boundary, a child-observed `500` is adjudicated as the
  accepting `B5_status http=200`, and two unequal child-observed namespaces are adjudicated
  as `binding=equal`. Both are rc 0 - the block reports success over an observation its child
  never made. `subject=green` is the same fixture against the repaired bytes: `code=500` at
  rc 1 and `netns_mismatch` at rc 3, unchanged by the substitution, because the descriptor
  the capture created resolves no name after the child exits.
- `READER_SUBSTITUTION red_child_ne_name=yes green_child_ne_name=yes` is the check that the
  fixture did its job on both subjects. Without it, `subject=green` passing would be
  consistent with the swap silently not happening.
- `swap=no` and `CLEAN_CONTROL` are the no-weakening arms: with nothing substituted, and with
  well-formed accepting input, RED and GREEN reach the same verdict token for token.
- `NO_NAME_FALLBACK ... subject=green rc=3 ... detail=capture_stream_unbound` is the arm that
  makes the repair a binding rather than a preference: given a capture that allocated no
  descriptor, GREEN STOPs with the row's own inability token instead of falling back to the
  name. RED reads the name and adjudicates it.
- `RC137_PROVENANCE body=direct_137` is finding 3. An immediate `exit 137` finishes in about
  a second; the round-7 command text calls it `kind=killed_after_grace` and exits 137, and
  the round-8 text calls it `kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no` and
  exits 1. `body=ignore_term` is the control: a real kill-after is still a timeout on both
  texts, and on GREEN it now carries the wrapper's own `wrapper_sent_term=yes
  wrapper_sent_kill=yes` as its evidence.
- `UNBOUNDED_PRELUDE` executes the auditor's FIFO on both texts. The behaviour is identical -
  `outer_test_rc=124` after 3 s with no stdout, stopped by a timeout that is not part of
  either command - and the difference is entirely in what the text claims:
  `claims_whole_command_bound=1` on RED, `states_prelude_unbounded=1` on GREEN.
- `BUDGET_ARITHMETIC` re-derives `wrappers * (900 + 30)` from each published text. Both texts
  are arithmetically self-consistent; round 7's error was the enforcement claim, which is why
  the arm above it is the one that matters and this one is bookkeeping.
- `READER_FIELD_LABEL round8_mislabeled_occurrences=0` is the field rename. The token is
  assembled from two pieces inside the fence so that the checking lines do not contain it and
  cannot count themselves.
- `ROW22_BIND_INABILITY` is finding 4, and all three lines are load-bearing. RED emits a
  generic `RP7_STOP` that no row preregisters; GREEN emits the exact `B6_STOP ...
  detail=capture_stream_unbound` the draft declares; and `caller=undeclared` shows that a
  capture caller with no token of its own still gets the generic fail-closed STOP, so the
  repair added a route rather than broadening a row-specific inability into a generic branch.


## The carried round-7 fence, re-run as a regression gate

The round-7 fence is reproduced below and re-executed against the round-9 bytes, so every
round-7 repair - the three NUL record STOPs, the two queue-field STOPs, the descriptor-bound
listener inventory and the kill-after classification - must still hold on these bytes, and
does. It is **not** byte-identical to round 7. Four changes are named here rather than left
to a diff, and each carries the argument the new rule demands: what input used to fail at
that arm, and whether it still fails.

| Change | Why | What used to fail here, and does it still? |
|---|---|---|
| 1. The two GREEN identity constants | They name the subject file by hash and byte count, so they have to name the round-9 bytes | A different subject file. **Still fails** - the assertion is still exact equality, and the fence aborts before any arm runs |
| 2. `adjudicated_name_sha256` -> `name_at_read_time_sha256` in the `READER_BINDING` printf | The field hashed the bytes at the leaf NAME, which GREEN expressly does not adjudicate; the label asserted the opposite of what the arm proves (finding 3) | Nothing was asserted on the field's NAME; the four `expect_has` patterns match `.*` there and are unchanged. The arm's discrimination is `bytes_field` vs `independent_wc_c` and the result token, all untouched. **A wildcard capture read through a substituted loopback name still fails** |
| 3. Both capture stubs allocate `WPI_CAP_ERR_FD` as well as `WPI_CAP_OUT_FD` | Production now binds both streams, so a stub that binds only stdout is no longer standing in for `wpi_capture` and the block STOPs on it | The stub feeds the same fixture bytes to the same production readers. **Every malformed record in this group still STOPs** - the three NUL cases and both queue cases are unchanged in the transcript below, token for token |
| 4. The F4 group's GREEN command text is the `c708511f` blob, not `$DOC` | A carried regression fence must not re-adjudicate a moving subject; with `$DOC` it had to be re-edited whenever the command changed, which is how assertions drift | **The round-6 misclassification still fails** exactly as before: `body=ignore_term subject=red` is still `fence_failed` at rc 1. What this group no longer covers - the CURRENT command text - is covered by the round-8 F3 group with a strictly stronger assertion |

Four arm groups, each a real RED against the round-6 blob at `3e2a976a` and a real GREEN
against the round-9 bytes, plus the no-weakening control in the same group as the repair it
guards:

| Arm | RED on round-6 bytes | GREEN on repaired bytes |
|---|---|---|
| F1 `2<NUL>00` status code | `read` drops the NUL, the record becomes `200`, `B5_status ... flags=expected` prints, rc 0 | `detail=nul_byte_in_record`, rc 3, no accepting line |
| F1 `O<NUL>K fields=8` parser result | the accepting parser record prints `B5_status`, rc 0 | `detail=nul_byte_in_record`, rc 3 |
| F1 `ne<NUL>t:[100]` namespace | `B6_netns ... binding=equal`, rc 0 | `detail=nul_byte_in_record`, rc 3 |
| F1 controls: clean `200`/`OK fields=8`/`net:[100]` | rc 0 accepting | identical, rc 0 accepting |
| F1 controls: the four other reader dispositions | `empty_or_read_error`, `unterminated_final_record`, `multiple_records`, `unterminated_extra_record` | identical tokens - the rewrite changed which records STOP, not which STOP reason a record gets |
| F2 `recvq=:` and `sendq=12:34` | `table=complete` and the accepting `B6_listener_set`, rc 0 | `detail=queue_grammar`, rc 3 |
| F2 controls: padded columns, real wildcard | rc 0 accepting / rc 1 `nonloopback_listener` | identical, plus `read_binding=capture_descriptor` and a `bytes=` field equal to an independent `wc -c` |
| F3 leaf replaced between the child's exit and the read, real `wpi_capture` | the reader re-opens the NAME: the child captured a wildcard, the block adjudicates the substituted loopback record and PASSes at rc 0 | the reader reads the capture DESCRIPTOR: the child's own wildcard bytes are adjudicated, `B6_FAIL reason=nonloopback_listener addr=0.0.0.0`, rc 1 |
| F3 control: no substitution | rc 0 accepting | rc 0 accepting, `bytes=` equal to an independent `wc -c` of the child's capture |
| F4 TERM-ignoring fence body | the round-6 published classifier calls rc 137 `PUBLISHED_COMMAND_RESULT=fence_failed`, exit 1 | `PUBLISHED_COMMAND_RESULT=timeout kind=killed_after_grace`, exit 137 |
| F4 control: TERM-honouring hang | `timeout` result, exit 124 | `timeout kind=terminated_at_bound`, exit 124 - unchanged |
| F4 aggregate arithmetic | `aggregate_bound_s=2700` against three 900 s bounds with three 30 s graces (`2790`) | `aggregate_bound_s=3720`, re-derived inside the fence as `wrappers * (900 + 30)` from the published text itself |

The F3 substitution is injected at the reader-allocation boundary, exactly as the auditor's
fixture injected it, so it is not a route the block reaches on its own. What it measures is
what the block *establishes*: round 6 established grammar over whatever the leaf name
resolved to at read time, and round 7 establishes it over the object the capture created.

```bash
# RP7_R7_FENCE_BEGIN
# Round-7 D026 fence for RP7-WPI-RO. Every arm drives the REAL production caller
# in a FRESH bash process against two byte sets whose identity is asserted first:
#   RED   = the frozen round-6 blob at commit 3e2a976a (88460 B, 6586698c...40709)
#   GREEN = the repaired worktree file
# Findings 1-3 are byte-identity defects - a value admitted, transformed or
# re-read, with a claim made about it stronger than what survived - so every arm
# feeds the exact bytes the audit fed and reads the production result line.
REPO=/c/LAB/Tradingview_LAB_CLEAN
DOC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
BLOCK=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r7-qa.XXXXXX)
RED=$Q/RP7-WPI-RO.round6.sh
GREEN=$BLOCK

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_has(){ grep -q -- "$2" "$3" || { printf 'QA_ASSERT_FAIL name=%s missing=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_hasnt(){ grep -q -- "$2" "$3" && { printf 'QA_ASSERT_FAIL name=%s unexpected=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; return 0; }

printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_timeout=%s git=%s uid_gid=%s:%s\n' \
    "$BASH_VERSION" "$(/usr/bin/timeout --version | head -1 | sed 's/.* //')" \
    "$(git --version | sed 's/.* //')" "$(id -u)" "$(id -g)"

# --- byte identity of both subjects -----------------------------------------
git -C "$REPO" cat-file blob 3e2a976a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$RED"
RED_SHA=$(sha256sum < "$RED" | cut -d' ' -f1);     RED_BYTES=$(wc -c < "$RED")
GREEN_SHA=$(sha256sum < "$GREEN" | cut -d' ' -f1); GREEN_BYTES=$(wc -c < "$GREEN")
RED_CR=$(tr -cd '\r' < "$RED" | wc -c);  GREEN_CR=$(tr -cd '\r' < "$GREEN" | wc -c)
bash --noprofile --norc -n "$RED";   RED_N=$?
bash --noprofile --norc -n "$GREEN"; GREEN_N=$?
printf 'BYTE_IDENTITY red_bytes=%s red_sha256=%s red_cr=%s red_bash_n=%s green_bytes=%s green_sha256=%s green_cr=%s green_bash_n=%s\n' \
    "$RED_BYTES" "$RED_SHA" "$RED_CR" "$RED_N" "$GREEN_BYTES" "$GREEN_SHA" "$GREEN_CR" "$GREEN_N"
expect_eq r7_red_sha256 "$RED_SHA" 6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
expect_eq r7_red_bytes "$RED_BYTES" 88460
expect_eq r7_green_sha256 "$GREEN_SHA" 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
expect_eq r7_green_bytes "$GREEN_BYTES" 108301
expect_rc r7_red_cr "$RED_CR" 0
expect_rc r7_green_cr "$GREEN_CR" 0
expect_rc r7_red_bash_n "$RED_N" 0
expect_rc r7_green_bash_n "$GREEN_N" 0

# ===========================================================================
# FINDING 1 (HIGH) - the common single-record reader deletes NUL, so a record
# the block cannot represent is normalised into an accepting observation. The
# three NUL fixtures are the auditor's own bytes. `clean`, `netns_clean` and the
# four reader-disposition cases are the no-weakening controls: the records the
# instruments really emit must keep their round-6 dispositions exactly, and a
# record that already STOPped must keep the SAME reason token.
#
# ROUND-9 CHANGE, subject-specific fixture: the parser's accepting record gained
# the digest of the bytes the parser itself read, because round 8 rendered
# `body_sha256` from a separate `sha256sum` over the leaf NAME and an executed
# fixture made that field report the child's ARMED body beside an accepting
# DISARMED verdict (Codex round-8 part B finding 1). A stub standing in for a
# parser must emit the record ITS OWN subject's parser can emit, so the record is
# now chosen per subject and pinned as a constant for each - it is not read from
# the subject, which would make the check unfalsifiable. Every other fixture,
# mode and expected disposition in this group is unchanged.
# ===========================================================================
cat > "$Q/f1_arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"; OKREC="$4"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/false; WPI_PYTHON3=/usr/bin/false; WPI_READLINK=/usr/bin/false; WPI_MAINPID=123
WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
wpi_capture(){
  local label="$1"
  WPI_CAP_OUT="$W/$label.out"; WPI_CAP_ERR="$W/$label.err"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
  case "$label:$mode" in
    status_get:code_nul)      printf '2\00000\n'        > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
    status_json:code_nul)     printf '%s\n' "$OKREC" > "$WPI_CAP_OUT" ;;
    status_get:record_nul)    printf '200\n'            > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
    status_json:record_nul)   printf 'O\000K fields=8\n' > "$WPI_CAP_OUT" ;;
    status_get:clean)         printf '200\n'            > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
    status_json:clean)        printf '%s\n' "$OKREC" > "$WPI_CAP_OUT" ;;
    caller_netns:netns_nul)   printf 'ne\000t:[100]\n'  > "$WPI_CAP_OUT" ;;
    caller_netns:netns_clean) printf 'net:[100]\n'      > "$WPI_CAP_OUT" ;;
    caller_netns:empty)       : > "$WPI_CAP_OUT" ;;
    caller_netns:unterminated) printf 'net:[100]'       > "$WPI_CAP_OUT" ;;
    caller_netns:multiple)    printf 'net:[100]\nnet:[100]\n' > "$WPI_CAP_OUT" ;;
    caller_netns:extra)       printf 'net:[100]\nnet:[' > "$WPI_CAP_OUT" ;;
    service_netns:*)          printf 'net:[100]\n'      > "$WPI_CAP_OUT" ;;
    *) exit 96 ;;
  esac
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
}
case "$mode" in
  code_nul|record_nul|clean) wpi_assert_status ;;
  *) wpi_assert_netns_binding ;;
esac
ARM
for mode in code_nul record_nul netns_nul clean netns_clean empty unterminated multiple extra; do
  for subject in red green; do
    if [ "$subject" = red ]; then S="$RED"; OKREC='OK fields=8'
    else S="$GREEN"; OKREC='OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000'; fi
    bash --noprofile --norc "$Q/f1_arm.sh" "$S" "$Q/f1-$mode-$subject" "$mode" "$OKREC" \
      > "$Q/f1-$mode-$subject.txt" 2>&1; rc=$?
    printf 'RECORD_BYTES mode=%s subject=%s rc=%s result=[%s]\n' "$mode" "$subject" "$rc" \
      "$(sed -e "s#$Q/f1-$mode-$subject#<scratch>#g" -e 's/[[:space:]]*$//' "$Q/f1-$mode-$subject.txt" | tr '\n' ' ' | sed 's/ *$//')"
  done
done > "$Q/f1.txt"
cat "$Q/f1.txt"
expect_has f1_red_code_nul_false_accept  'RECORD_BYTES mode=code_nul subject=red rc=0 result=\[B5_status http=200 json=strict required_fields=8' "$Q/f1.txt"
expect_has f1_green_code_nul_stop        'RECORD_BYTES mode=code_nul subject=green rc=3 result=\[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=nul_byte_in_record source=<scratch>/status_get.out\]' "$Q/f1.txt"
expect_has f1_red_record_nul_false_accept 'RECORD_BYTES mode=record_nul subject=red rc=0 result=\[B5_status http=200 json=strict required_fields=8' "$Q/f1.txt"
expect_has f1_green_record_nul_stop      'RECORD_BYTES mode=record_nul subject=green rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=nul_byte_in_record source=<scratch>/status_json.out\]' "$Q/f1.txt"
expect_has f1_red_netns_nul_false_accept 'RECORD_BYTES mode=netns_nul subject=red rc=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f1.txt"
expect_has f1_green_netns_nul_stop       'RECORD_BYTES mode=netns_nul subject=green rc=3 result=\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=nul_byte_in_record source=<scratch>/caller_netns.out\]' "$Q/f1.txt"
expect_has f1_red_clean_accept           'RECORD_BYTES mode=clean subject=red rc=0 result=\[B5_status http=200' "$Q/f1.txt"
expect_has f1_green_clean_accept         'RECORD_BYTES mode=clean subject=green rc=0 result=\[B5_status http=200' "$Q/f1.txt"
expect_has f1_red_netns_clean_accept     'RECORD_BYTES mode=netns_clean subject=red rc=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f1.txt"
expect_has f1_green_netns_clean_accept   'RECORD_BYTES mode=netns_clean subject=green rc=0 result=\[B6_netns caller=net:\[100\] service=net:\[100\] mainpid=123 binding=equal\]' "$Q/f1.txt"
# No-weakening: the four dispositions that already STOPped must STOP with the SAME token.
for mode in empty unterminated multiple extra; do
  case "$mode" in
    empty)        tok=empty_or_read_error ;;
    unterminated) tok=unterminated_final_record ;;
    multiple)     tok=multiple_records ;;
    extra)        tok=unterminated_extra_record ;;
  esac
  expect_has "f1_red_${mode}_stop"   "RECORD_BYTES mode=$mode subject=red rc=3 result=\\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=$tok " "$Q/f1.txt"
  expect_has "f1_green_${mode}_stop" "RECORD_BYTES mode=$mode subject=green rc=3 result=\\[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=$tok " "$Q/f1.txt"
done

# ===========================================================================
# FINDING 2 (HIGH) - the listener parser validated the CONCATENATION
# "$recvq:$sendq" against a class that permits the separator, so a queue field
# could be empty or itself contain a colon. `clean` (column-padded) and
# `wildcard` are the published controls and must not move.
# ===========================================================================
cat > "$Q/f2_arm.sh" <<'ARM'
S="$1"; W="$2"; rec="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no; WPI_SS=/usr/bin/false
printf '%s\n' "$rec" > "$W/ss.out"
wpi_capture(){
  WPI_CAP_OUT="$W/ss.out"; WPI_CAP_ERR="$W/ss.err"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
}
wpi_assert_listener_set
ARM
for spec in \
  'recv_colon|LISTEN : 128 127.0.0.1:8790 0.0.0.0:*' \
  'send_colon|LISTEN 0 12:34 127.0.0.1:8790 0.0.0.0:*' \
  'clean|LISTEN 0      128          127.0.0.1:8790       0.0.0.0:*' \
  'wildcard|LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*'; do
  name=${spec%%|*}; rec=${spec#*|}
  for subject in red green; do
    if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
    bash --noprofile --norc "$Q/f2_arm.sh" "$S" "$Q/f2-$name-$subject" "$rec" \
      > "$Q/f2-$name-$subject.txt" 2>&1; rc=$?
    printf 'QUEUE_FIELDS case=%s subject=%s rc=%s accepting=%s bytes=%s result=[%s]\n' \
      "$name" "$subject" "$rc" \
      "$(grep -c '^B6_listener_set ' "$Q/f2-$name-$subject.txt")" \
      "$(sed -n 's/.*B6_listener_inventory rows=[0-9]* port_8790_rows=[0-9]* bytes=\([0-9]*\) .*/\1/p' "$Q/f2-$name-$subject.txt")" \
      "$(grep -E '^B6_(STOP|FAIL) ' "$Q/f2-$name-$subject.txt" | head -1 | sed 's/^B6_[A-Z]* reason=//')"
  done
done > "$Q/f2.txt"
cat "$Q/f2.txt"
expect_has f2_red_recv_colon_accept  'QUEUE_FIELDS case=recv_colon subject=red rc=0 accepting=1 bytes=38 result=\[\]' "$Q/f2.txt"
expect_has f2_green_recv_colon_stop  'QUEUE_FIELDS case=recv_colon subject=green rc=3 accepting=0 bytes= result=\[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar\]' "$Q/f2.txt"
expect_has f2_red_send_colon_accept  'QUEUE_FIELDS case=send_colon subject=red rc=0 accepting=1 bytes=40 result=\[\]' "$Q/f2.txt"
expect_has f2_green_send_colon_stop  'QUEUE_FIELDS case=send_colon subject=green rc=3 accepting=0 bytes= result=\[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar\]' "$Q/f2.txt"
expect_has f2_red_clean_accept       'QUEUE_FIELDS case=clean subject=red rc=0 accepting=1 bytes=58 result=\[\]' "$Q/f2.txt"
expect_has f2_green_clean_accept     'QUEUE_FIELDS case=clean subject=green rc=0 accepting=1 bytes=58 result=\[\]' "$Q/f2.txt"
expect_has f2_red_wildcard_fail      'QUEUE_FIELDS case=wildcard subject=red rc=1 accepting=0 bytes=36 result=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f2.txt"
expect_has f2_green_wildcard_fail    'QUEUE_FIELDS case=wildcard subject=green rc=1 accepting=0 bytes=36 result=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f2.txt"
# The repaired inventory line must SAY which object it read, and the round-6 one must not.
expect_has    f2_green_read_binding 'read_binding=capture_descriptor' "$Q/f2-clean-green.txt"
expect_hasnt  f2_red_read_binding   'read_binding=' "$Q/f2-clean-red.txt"

# ===========================================================================
# FINDING 3 (HIGH) - row 22 claimed the adjudicated byte string IS the captured
# byte string while the reader re-opened the leaf by name. This arm runs the
# REAL wpi_capture (real create-once leaves, real cleared-environment child,
# real bounding wrapper) and replaces the leaf NAME at the reader-allocation
# boundary, exactly where the auditor injected it. `plain` is the control: with
# no substitution both subjects accept, and the repaired `bytes=` field is
# compared against an independent `wc -c` of the child's own capture.
# ===========================================================================
printf '#!/bin/sh\nprintf "LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*\\n"\n' > "$Q/fake-ss.sh"; chmod 755 "$Q/fake-ss.sh"
cat > "$Q/f3_arm.sh" <<'ARM'
S="$1"; W="$2"; SS="$3"; swap="$4"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=20; WPI_SS="$SS"
wpi_alloc_read_diag(){
  local label="$1"
  if [ "$label" = listener_rows ]; then
    cp -- "$WPI_CAP_OUT" "$W/child-captured.out"
    if [ "$swap" = yes ]; then
      rm -- "$WPI_CAP_OUT"
      printf 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\n' > "$WPI_CAP_OUT"
    fi
  fi
  WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1))
  WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
  wpi_open_leaf "$WPI_READ_DIAG"; WPI_READ_DIAG_FD="$WPI_LEAF_FD"
}
wpi_assert_listener_set
ARM
for swap in yes no; do
  for subject in red green; do
    if [ "$subject" = red ]; then S="$RED"; else S="$GREEN"; fi
    W=$Q/f3-$swap-$subject
    bash --noprofile --norc "$Q/f3_arm.sh" "$S" "$W" "$Q/fake-ss.sh" "$swap" > "$W.txt" 2>&1; rc=$?
    printf 'READER_BINDING swap=%s subject=%s rc=%s child_captured_sha256=%s name_at_read_time_sha256=%s bytes_field=%s independent_wc_c=%s result=[%s]\n' \
      "$swap" "$subject" "$rc" \
      "$(sha256sum < "$W/child-captured.out" | cut -d' ' -f1)" \
      "$(cat "$W"/ev/ro.*.listeners.stdout | sha256sum | cut -d' ' -f1)" \
      "$(sed -n 's/.*B6_listener_inventory rows=[0-9]* port_8790_rows=[0-9]* bytes=\([0-9]*\) .*/\1/p' "$W.txt")" \
      "$(wc -c < "$W/child-captured.out")" \
      "$(grep -E '^B6_(STOP|FAIL|listener_set) ' "$W.txt" | head -1 | sed -e 's/^B6_[A-Z]* reason=//' -e 's/^B6_listener_set /accepting /')"
  done
done > "$Q/f3.txt"
cat "$Q/f3.txt"
expect_has f3_red_adjudicates_substitute 'READER_BINDING swap=yes subject=red rc=0 .* bytes_field=38 independent_wc_c=36 result=\[accepting port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\]' "$Q/f3.txt"
expect_has f3_green_adjudicates_capture  'READER_BINDING swap=yes subject=green rc=1 .* bytes_field=36 independent_wc_c=36 result=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f3.txt"
expect_has f3_red_plain_fail             'READER_BINDING swap=no subject=red rc=1 .* bytes_field=36 independent_wc_c=36 result=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f3.txt"
expect_has f3_green_plain_fail           'READER_BINDING swap=no subject=green rc=1 .* bytes_field=36 independent_wc_c=36 result=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f3.txt"
# The swap really happened on both subjects: the child's bytes and the bytes the
# NAME resolved to at read time differ. Only the subject that reads the capture
# DESCRIPTOR is unaffected by that difference.
SWAP_RED_CHILD=$(sha256sum < "$Q/f3-yes-red/child-captured.out" | cut -d' ' -f1)
SWAP_RED_NAME=$(cat "$Q/f3-yes-red"/ev/ro.*.listeners.stdout | sha256sum | cut -d' ' -f1)
SWAP_GREEN_CHILD=$(sha256sum < "$Q/f3-yes-green/child-captured.out" | cut -d' ' -f1)
SWAP_GREEN_NAME=$(cat "$Q/f3-yes-green"/ev/ro.*.listeners.stdout | sha256sum | cut -d' ' -f1)
printf 'READER_SUBSTITUTION red_child_ne_name=%s green_child_ne_name=%s\n' \
  "$([ "$SWAP_RED_CHILD" != "$SWAP_RED_NAME" ] && echo yes || echo no)" \
  "$([ "$SWAP_GREEN_CHILD" != "$SWAP_GREEN_NAME" ] && echo yes || echo no)"
expect_eq f3_swap_effective_red   "$([ "$SWAP_RED_CHILD" != "$SWAP_RED_NAME" ] && echo yes || echo no)" yes
expect_eq f3_swap_effective_green "$([ "$SWAP_GREEN_CHILD" != "$SWAP_GREEN_NAME" ] && echo yes || echo no)" yes

# ===========================================================================
# FINDING 4 (MEDIUM) - the published command misclassified the kill-after
# outcome and documented an aggregate no arithmetic supports. Both subjects are
# the published command TEXT itself: RED is the round-6 document's command
# extracted from commit 3e2a976a, GREEN is the round-7 document's, extracted
# from commit c708511f. Each is retargeted into a scratch tree and its bound
# scaled from `900s`/`30s` to `1s`/`2s`, and nothing else is altered.
# `honour_term` is the control: the outcome round 6 already classified correctly
# must stay correct.
#
# ROUND-8 CHANGE, and the only one in this fence's F4 group: GREEN was `$DOC`,
# the LIVE document. That made a carried regression fence re-adjudicate a moving
# subject, so it had to be re-edited every time the published command changed -
# and a fence that has to be re-edited every round is a fence whose assertions
# drift. Both texts are now git blobs, so this group is byte-stable and pins the
# historical claim it was written for: round 6's classifier called a fence killed
# after its grace `fence_failed`, and round 7's called it a timeout. The CURRENT
# command text is adjudicated by the round-8 fence, whose F3 group asserts the
# strictly stronger property round 7's text does NOT have - that an rc of 137 is
# called a kill-after event only when that wrapper itself recorded sending KILL.
# ===========================================================================
git -C "$REPO" cat-file blob 3e2a976a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md > "$Q/SELF_QA_RP7.round6.md"
git -C "$REPO" cat-file blob c708511f:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md > "$Q/SELF_QA_RP7.round7.md"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$Q/SELF_QA_RP7.round6.md" > "$Q/published-red.txt"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$Q/SELF_QA_RP7.round7.md" > "$Q/published-green.txt"
printf '#!/bin/sh\ntrap "" TERM\nexec /usr/bin/sleep 30\n' > "$Q/ignore-term.sh"
printf '#!/bin/sh\nexec /usr/bin/sleep 30\n' > "$Q/honour-term.sh"
for body in ignore_term honour_term; do
  for subject in red green; do
    T=$Q/f4-$body-$subject; mkdir -p "$T"
    case "$body" in
      ignore_term) HANG="trap '' TERM\n/usr/bin/sleep 30\n" ;;
      honour_term) HANG="/usr/bin/sleep 30\n" ;;
    esac
    { [ "$subject" = green ] && printf "# RP7_R7_FENCE_BEGIN\n${HANG}# RP7_R7_FENCE_END\n"
      printf "# RP7_R6_FENCE_BEGIN\n"; [ "$subject" = red ] && printf "$HANG"; printf "# RP7_R6_FENCE_END\n"
      printf '# RP7_QA_FENCE_BEGIN\nexit 0\n# RP7_QA_FENCE_END\n'
      printf '# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n'; } > "$T/SELF_QA_RP7.md"
    # The /tmp expression runs FIRST for the reason the round-6 fence documents:
    # this scratch tree is itself under /tmp/rp7-, so retargeting `cd` first
    # would let the /tmp rule rewrite the new target as well.
    sed -e "s#/tmp/rp7-#$T/body-#g" \
        -e "s#^cd /c/LAB/.*#cd $T#" \
        -e "s#--kill-after=30s 900s#--kill-after=2s 1s#g" \
        "$Q/published-$subject.txt" > "$T/run.sh"
    timeout 120 bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
    printf 'TIMEOUT_CLASS body=%s subject=%s cd_retargeted=%s real_fence_bodies=%s scaled_wrappers=%s rc=%s fence_rcs=[%s] result=[%s]\n' \
      "$body" "$subject" \
      "$(grep -c "^cd $T\$" "$T/run.sh")" \
      "$(grep -cE '/tmp/rp7-r[4-7]-fence-body\.sh' "$T/run.sh")" \
      "$(grep -c -- '--kill-after=2s 1s' "$T/run.sh")" \
      "$rc" \
      "$(grep -E '^R[4-7]_FENCE_RC=' "$T/out.txt" | tr '\n' ' ' | sed 's/ *$//')" \
      "$(grep '^PUBLISHED_COMMAND_RESULT=' "$T/out.txt" | head -1 | sed 's/^PUBLISHED_COMMAND_RESULT=//')"
  done
done > "$Q/f4.txt"
cat "$Q/f4.txt"
expect_has f4_red_misclassifies_kill  'TIMEOUT_CLASS body=ignore_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=3 rc=1 fence_rcs=\[R6_FENCE_RC=137 R5_FENCE_RC=0 R4_FENCE_RC=0\] result=\[fence_failed\]' "$Q/f4.txt"
expect_has f4_green_classifies_kill   'TIMEOUT_CLASS body=ignore_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 fence_rcs=\[R7_FENCE_RC=137 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0\] result=\[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30\]' "$Q/f4.txt"
expect_has f4_red_honours_term        'TIMEOUT_CLASS body=honour_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=3 rc=124 fence_rcs=\[R6_FENCE_RC=124 R5_FENCE_RC=0 R4_FENCE_RC=0\] result=\[timeout per_fence_bound_s=900\]' "$Q/f4.txt"
expect_has f4_green_honours_term      'TIMEOUT_CLASS body=honour_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=124 fence_rcs=\[R7_FENCE_RC=124 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0\] result=\[timeout kind=terminated_at_bound per_fence_bound_s=900\]' "$Q/f4.txt"

# The aggregate is re-derived from the published text rather than read from the
# prose: wrappers * (nominal + grace), and the published claim must equal it.
for subject in red green; do
  W=$(grep -c -- 'timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc' "$Q/published-$subject.txt")
  CLAIM=$(sed -n 's/.*aggregate_bound_s=\([0-9]*\).*/\1/p' "$Q/published-$subject.txt" | head -1)
  OUTER=$(grep -c 'RP7_AGGREGATE_WRAPPER' "$Q/published-$subject.txt")
  printf 'BOUND_ARITHMETIC subject=%s wrappers=%s per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=%s claimed_s=%s claim_true=%s outer_wrapper=%s\n' \
    "$subject" "$W" "$((W*(900+30)))" "$CLAIM" \
    "$([ "$((W*(900+30)))" = "$CLAIM" ] && echo yes || echo no)" \
    "$([ "$OUTER" -gt 0 ] && echo present || echo absent)"
done > "$Q/f4bound.txt"
cat "$Q/f4bound.txt"
expect_has f4_red_bound_false  'BOUND_ARITHMETIC subject=red wrappers=3 per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=2790 claimed_s=2700 claim_true=no outer_wrapper=absent' "$Q/f4bound.txt"
expect_has f4_green_bound_true 'BOUND_ARITHMETIC subject=green wrappers=4 per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=3720 claimed_s=3720 claim_true=yes outer_wrapper=absent' "$Q/f4bound.txt"

case "$Q" in /tmp/rp7-r7-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_SCRATCH_UNSAFE=%s\n' "$Q"; exit 97 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_R7_FENCE_END
```

### Round-7 transcript

```text
QA_ROOT=/tmp/rp7-r7-qa.Muw5Jb
QA_ENV bash=5.2.37(1)-release coreutils_timeout=8.32 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=88460 red_sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709 red_cr=0 red_bash_n=0 green_bytes=108301 green_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62 green_cr=0 green_bash_n=0
RECORD_BYTES mode=code_nul subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
RECORD_BYTES mode=code_nul subject=green rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=nul_byte_in_record source=<scratch>/status_get.out]
RECORD_BYTES mode=record_nul subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
RECORD_BYTES mode=record_nul subject=green rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=nul_byte_in_record source=<scratch>/status_json.out]
RECORD_BYTES mode=netns_nul subject=red rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
RECORD_BYTES mode=netns_nul subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=nul_byte_in_record source=<scratch>/caller_netns.out]
RECORD_BYTES mode=clean subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
RECORD_BYTES mode=clean subject=green rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
RECORD_BYTES mode=netns_clean subject=red rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
RECORD_BYTES mode=netns_clean subject=green rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
RECORD_BYTES mode=empty subject=red rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=empty_or_read_error source=<scratch>/caller_netns.out read_rc=1]
RECORD_BYTES mode=empty subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=empty_or_read_error source=<scratch>/caller_netns.out read_rc=1]
RECORD_BYTES mode=unterminated subject=red rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=unterminated_final_record source=<scratch>/caller_netns.out read_rc=1]
RECORD_BYTES mode=unterminated subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=unterminated_final_record source=<scratch>/caller_netns.out read_rc=1]
RECORD_BYTES mode=multiple subject=red rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=multiple_records source=<scratch>/caller_netns.out]
RECORD_BYTES mode=multiple subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=multiple_records source=<scratch>/caller_netns.out]
RECORD_BYTES mode=extra subject=red rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=unterminated_extra_record source=<scratch>/caller_netns.out]
RECORD_BYTES mode=extra subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=unterminated_extra_record source=<scratch>/caller_netns.out]
QUEUE_FIELDS case=recv_colon subject=red rc=0 accepting=1 bytes=38 result=[]
QUEUE_FIELDS case=recv_colon subject=green rc=3 accepting=0 bytes= result=[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar]
QUEUE_FIELDS case=send_colon subject=red rc=0 accepting=1 bytes=40 result=[]
QUEUE_FIELDS case=send_colon subject=green rc=3 accepting=0 bytes= result=[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar]
QUEUE_FIELDS case=clean subject=red rc=0 accepting=1 bytes=58 result=[]
QUEUE_FIELDS case=clean subject=green rc=0 accepting=1 bytes=58 result=[]
QUEUE_FIELDS case=wildcard subject=red rc=1 accepting=0 bytes=36 result=[nonloopback_listener addr=0.0.0.0]
QUEUE_FIELDS case=wildcard subject=green rc=1 accepting=0 bytes=36 result=[nonloopback_listener addr=0.0.0.0]
READER_BINDING swap=yes subject=red rc=0 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc name_at_read_time_sha256=db4755ec151f8d59f9c069832b3b9ad602adfbb6d0a2c31e295e478e2378600d bytes_field=38 independent_wc_c=36 result=[accepting port=8790 count=1 local=127.0.0.1 wildcard=none table=complete]
READER_BINDING swap=yes subject=green rc=1 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc name_at_read_time_sha256=db4755ec151f8d59f9c069832b3b9ad602adfbb6d0a2c31e295e478e2378600d bytes_field=36 independent_wc_c=36 result=[nonloopback_listener addr=0.0.0.0]
READER_BINDING swap=no subject=red rc=1 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc name_at_read_time_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc bytes_field=36 independent_wc_c=36 result=[nonloopback_listener addr=0.0.0.0]
READER_BINDING swap=no subject=green rc=1 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc name_at_read_time_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc bytes_field=36 independent_wc_c=36 result=[nonloopback_listener addr=0.0.0.0]
READER_SUBSTITUTION red_child_ne_name=yes green_child_ne_name=yes
TIMEOUT_CLASS body=ignore_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=3 rc=1 fence_rcs=[R6_FENCE_RC=137 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[fence_failed]
TIMEOUT_CLASS body=ignore_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 fence_rcs=[R7_FENCE_RC=137 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
TIMEOUT_CLASS body=honour_term subject=red cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=3 rc=124 fence_rcs=[R6_FENCE_RC=124 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout per_fence_bound_s=900]
TIMEOUT_CLASS body=honour_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=124 fence_rcs=[R7_FENCE_RC=124 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout kind=terminated_at_bound per_fence_bound_s=900]
BOUND_ARITHMETIC subject=red wrappers=3 per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=2790 claimed_s=2700 claim_true=no outer_wrapper=absent
BOUND_ARITHMETIC subject=green wrappers=4 per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=3720 claimed_s=3720 claim_true=yes outer_wrapper=absent
QA_PASS all_assertions=yes
```

Reading the load-bearing lines:

- `BYTE_IDENTITY` proves the RED subject is the audited round-6 blob (88460 B,
  `6586698c...40709`) and the GREEN subject is the repaired round-9 file (108301 B, `0e93f90d...1e62`),
  both LF-only and both `bash -n` clean.
- The three `RECORD_BYTES ... subject=red rc=0` lines are Codex's finding 1 reproduced on the
  audited bytes: `2<NUL>00` prints an accepting `B5_status http=200`, `O<NUL>K fields=8`
  prints the same accepting line from the parser result, and `ne<NUL>t:[100]` prints
  `B6_netns ... binding=equal`. Each GREEN line is `rc=3` with
  `detail=nul_byte_in_record source=<scratch>/<stream>`, before any status, parser-result or
  namespace semantics were applied.
- `mode=clean` and `mode=netns_clean` are identical in RED and GREEN, and the four
  `empty`/`unterminated`/`multiple`/`extra` pairs are identical token for token. The reader
  rewrite changed which records STOP, not which reason a record that already STOPped gets.
- `QUEUE_FIELDS case=recv_colon` and `case=send_colon` are finding 2: on the round-6 bytes a
  queue field that is a bare `:` or `12:34` reaches `accepting=1` with a complete table, and
  on the repaired bytes each is `detail=queue_grammar` at rc 3 with no inventory line. The
  `clean` (column-padded) and `wildcard` rows are byte-identical between subjects apart from
  the new `read_binding=capture_descriptor` field, which the last two assertions in the group
  check is present on GREEN and absent on RED.
- `READER_BINDING swap=yes` is finding 3, and the two digests in it are the whole argument.
  `child_captured_sha256` is what the real child wrote; `name_at_read_time_sha256` is what
  the leaf NAME resolved to when the reader ran - **round 7 called that field
  `adjudicated_name_sha256`, which named the one thing GREEN expressly does not adjudicate**
  (Codex round-7 part B finding 3), and renaming it is round-8 change 2 to this fence. They differ on both subjects, which
  `READER_SUBSTITUTION` states explicitly. The round-6 bytes adjudicate the substituted
  record and PASS with `bytes_field=38`; the round-7 bytes adjudicate the child's own bytes
  and return `B6_FAIL reason=nonloopback_listener addr=0.0.0.0` with `bytes_field=36`, equal
  to the independent `wc -c` of the child's capture. `swap=no` is the control: with nothing
  substituted, both subjects reach the same verdict.
- `TIMEOUT_CLASS body=ignore_term` is finding 4. The round-6 published command text calls a
  fence killed after its grace `fence_failed` and exits 1; the round-7 text calls it
  `timeout kind=killed_after_grace` and exits 137. `body=honour_term` is the control: the
  outcome round 6 already classified correctly is still `timeout` at rc 124 on both.
- `BOUND_ARITHMETIC` re-derives the aggregate from the published text rather than from prose:
  three wrappers imply 2790 s and the round-6 text claimed 2700 (`claim_true=no`), four
  wrappers imply 3720 s and the round-7 text claims 3720 (`claim_true=yes`). Neither text
  contains an outer wrapper, and both say so.


## The carried round-6 fence, re-run as a regression gate

The round-6 fence is reproduced below and re-executed against the round-9 bytes, so every
round-6 repair - the listener NUL/address/port STOPs, the four status-result dispositions,
`000`/`099`/`600`, the `500` FAIL, the `401` STOP, rc propagation from the published
command, and the write-side leaf binding - must still hold on these bytes, and does. It is
**not** byte-identical to round 6. Six changes have now been made to it across rounds 7 and
8; each is named here with the argument the new rule demands.

**Round 7 made four changes, and one of them was wrong.** They were, and remain:

1. the two GREEN identity constants, which name the subject file by hash and byte count and
   therefore have to name the current bytes;
2. `expect_rc f4_bound_wrappers`, from `3` to `4`, because the published command grew a
   fourth fence;
3. the F1 listener stub, which allocates the read descriptor the production capture
   allocates - a stub that sets `WPI_CAP_OUT` without it is not standing in for
   `wpi_capture` any more, and the block STOPs on it rather than reading a name;
4. the F5 leaf-race arm, moved into a subshell so it survives the environment-dependent STOP
   described above and can still report the outside file - **and, in the same edit, its
   GREEN assertion relaxed from `rc=0` to `rc=[0-9]*`.**

Change 4's second half is Codex round-7 part B finding 1, and the round-7 report justified it
by saying the old assertion "never measured" the rc. **That statement was false.** The arm
printed `rc=%s` and the old `grep` pinned that field to `0`; the subshell was needed to
survive the STOP, and pinning the two legitimate statuses instead of any decimal string would
have survived it just as well. The relaxed assertion accepts an unrelated `return 7` at the
top of `wpi_capture` - a regression that never touches the leaf and is therefore invisible to
an assertion that only inspects the outside file. `RP7_REPAIR_R7_REPORT.md` is corrected, and
the round-8 fence executes the round-7 and round-8 assertions over the same three outputs so
the difference is measured rather than asserted.

**Round 8 makes two more changes, and repairs change 4:**

| Change | Why | What input used to fail here, and does it still? |
|---|---|---|
| 5. `expect_rc f4_bound_wrappers` 4 -> 5, the pattern gains `--verbose`, `DOCBOUND` looks for "fence-timeout budget", and a new `expect_rc f4_every_body_wrapped` asserts wrappers == extracted fence bodies | The published command runs five fences and instruments each wrapper so it can attribute an rc of 137 (finding 3) | A fence body run without a `timeout` wrapper. **Still fails**, and now fails harder: the count is no longer a bare constant but is tied to the number of bodies the command extracts, so adding an unwrapped fence fails even if the constant is updated with it |
| 6. The F5 GREEN assertion is an exact two-outcome classifier, and a `return 7` mutant of the block is added as a RED arm | Restore the discriminating power change 4 removed, without losing the subshell that made the MSYS2 STOP observable (finding 1) | The round-5 escape - `outside_text=CAPTURED payload_left_the_tree=yes` - **still fails**, under both the old and the new assertion (`f5_old_rejects_red`, `f5_new_rejects_red`). What newly fails is the mutant: `f5_old_accepts_mutant` and `f5_new_rejects_mutant` are both asserted, so the fence itself records that the old assertion was weaker |
| 7. Every capture stub in this fence that feeds a B5 or B6 assertion allocates `WPI_CAP_ERR_FD` as well as `WPI_CAP_OUT_FD` | Production binds both capture streams as of round 8, and the emptiness of the diagnostic stream is as much a child observation as the record (finding 2) | The stubs feed the same fixture bytes to the same production readers. **Every malformed record in this fence still STOPs with the same token** - the transcript below is unchanged for all of F1, F2 and F3 |

Everything else - every arm, every other assertion, and the RED blob at `1143a9ff` - is
byte-identical to round 6.

Five arm groups, each a real RED against the round-5 blob and a real GREEN against the
round-9 bytes, plus the no-weakening control in the same group as the repair it guards:

| Arm | RED on round-5 bytes | GREEN on repaired bytes |
|---|---|---|
| F1 `nul` record | `read` drops the NUL, `LIS<NUL>TEN` becomes `LISTEN`, `parse=complete_before_semantics` and the accepting listener line print, rc 0 | `detail=nul_byte_in_inventory`, rc 3, no inventory line |
| F1 `nonsense:8790` | rc 1 `listener_set_unexpected observed=non_preregistered_address` | `detail=local_address_grammar`, rc 3 |
| F1 port `99999` / `08790` / octet `300.1.1.1` | rc 1 host-state FAILs derived from records that state no port and no address | `detail=local_port_range` / `local_port_grammar` / `local_address_grammar`, rc 3 |
| F1 controls: padded columns, real wildcard | rc 0 accepting / rc 1 `nonloopback_listener` | unchanged, plus a `bytes=` field equal to an independent `wc -c` |
| F2 truncated/invented result records | `TYPE state str` → rc 1 FAIL with `expected_type=` empty; `MISMATCH state abc` → rc 1 FAIL on a 3-character digest; `MISMATCH rogue <64hex>` → rc 1 FAIL naming a field outside the schema | one `detail=*_record_*` STOP each, rc 3 |
| F2 controls: the four records the child can emit | `OK`/`TYPE`/`MISMATCH`/`MISSING` dispositions | identical |
| F2 schema declaration | (no schema is passed in round 5) | the child refuses a declaration that differs from its own table: `PARSE schema_declaration_mismatch`, rc 3 |
| F3 `000`, `099`, `600` | rc 1 `status_endpoint_unexpected_http` | `detail=http_code_no_response` / `http_code_grammar`, rc 3 |
| F3 controls: `500`, `401` | rc 1 FAIL / rc 3 access-denied STOP | identical |
| F4 published command | `bash; printf; bash; printf` returns 0 with inner rcs 7 and 9 | the published command returns 1 over failing fence bodies, carries one 900 s bound per fence (four of them as of round 7), and turns a hanging body into rc 124 |
| F5 recovered leaf-replacement test | the capture writes `CAPTURED` into a file outside the evidence tree, rc 0, no STOP | the outside file is untouched: `payload_left_the_tree=no` |

The F5 arm is the recovered test, and its status has not changed: the replacement is
injected through a hooked `wpi_clock_ms`, so it is not a route the block reaches on its own.
What it measures is what the block *establishes*. Round 5 allocated a leaf with `noclobber`
and then wrote to the name; the object written was never proven to be the object created.
Round 6 keeps the descriptor the creating open returned and writes through it, so the write
cannot land anywhere else. Two residuals survive and are stated under *What this QA does not
establish*, not covered by the file header.

```bash
# RP7_R6_FENCE_BEGIN
# Round-6 D026 fence for RP7-WPI-RO. Every arm drives the REAL production caller
# in a FRESH bash process against two byte sets whose identity is asserted first:
#   RED   = the frozen round-5 blob at commit 1143a9ff (77179 B, 393a16ce...b0ee)
#   GREEN = the repaired worktree file
# Findings 1-3 are byte-grammar defects, so every arm feeds the exact bytes the
# audit fed and reads the production result line, not a reimplementation of it.
REPO=/c/LAB/Tradingview_LAB_CLEAN
DOC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
BLOCK=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
PYEXE=/c/Python314/python.exe
Q=$(mktemp -d /tmp/rp7-r6-qa.XXXXXX)
RED=$Q/RP7-WPI-RO.round5.sh
GREEN=$BLOCK

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_has(){ grep -q -- "$2" "$3" || { printf 'QA_ASSERT_FAIL name=%s missing=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_hasnt(){ grep -q -- "$2" "$3" && { printf 'QA_ASSERT_FAIL name=%s unexpected=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; return 0; }

printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_stat=%s python=%s git=%s uid_gid=%s:%s\n' \
    "$BASH_VERSION" "$(/usr/bin/stat --version | head -1 | sed 's/.* //')" \
    "$("$PYEXE" -V | sed 's/.* //')" "$(git --version | sed 's/.* //')" "$(id -u)" "$(id -g)"

# --- byte identity of both subjects -----------------------------------------
git -C "$REPO" cat-file blob 1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$RED"
RED_SHA=$(sha256sum < "$RED" | cut -d' ' -f1);     RED_BYTES=$(wc -c < "$RED")
GREEN_SHA=$(sha256sum < "$GREEN" | cut -d' ' -f1); GREEN_BYTES=$(wc -c < "$GREEN")
RED_CR=$(tr -cd '\r' < "$RED" | wc -c);  GREEN_CR=$(tr -cd '\r' < "$GREEN" | wc -c)
bash --noprofile --norc -n "$RED";   RED_N=$?
bash --noprofile --norc -n "$GREEN"; GREEN_N=$?
printf 'BYTE_IDENTITY red_bytes=%s red_sha256=%s red_cr=%s red_bash_n=%s green_bytes=%s green_sha256=%s green_cr=%s green_bash_n=%s\n' \
    "$RED_BYTES" "$RED_SHA" "$RED_CR" "$RED_N" "$GREEN_BYTES" "$GREEN_SHA" "$GREEN_CR" "$GREEN_N"
expect_eq red_sha256 "$RED_SHA" 393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee
expect_eq red_bytes "$RED_BYTES" 77179
expect_eq green_sha256 "$GREEN_SHA" 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
expect_eq green_bytes "$GREEN_BYTES" 108301
expect_rc red_cr "$RED_CR" 0
expect_rc green_cr "$GREEN_CR" 0
expect_rc red_bash_n "$RED_N" 0
expect_rc green_bash_n "$GREEN_N" 0

# ===========================================================================
# FINDING 1 (HIGH) - a malformed listener record is normalised into a
# conformant one and reported as a complete PASS. The `nul` case is the audit's
# own fixture byte for byte. `clean` and `wildcard` are the no-weakening
# controls: real column-padded ss output must still parse, and a real wildcard
# listener must still be a host-state FAIL rather than a new STOP.
# ===========================================================================
cat > "$Q/f1_arm.sh" <<'ARM'
S="$1"; W="$2"; CASE="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no; WPI_SS=/usr/bin/ss
case "$CASE" in
  nul)        printf 'LIS\0TEN 0 128 127.0.0.1:8790 0.0.0.0:*\n' > "$W/ss.out" ;;
  address)    printf 'LISTEN 0 128 nonsense:8790 nonsense:*\n'   > "$W/ss.out" ;;
  port_range) printf 'LISTEN 0 128 127.0.0.1:99999 0.0.0.0:*\n'  > "$W/ss.out" ;;
  octet)      printf 'LISTEN 0 128 300.1.1.1:8790 0.0.0.0:*\n'   > "$W/ss.out" ;;
  leading0)   printf 'LISTEN 0 128 127.0.0.1:08790 0.0.0.0:*\n'  > "$W/ss.out" ;;
  clean)      printf 'LISTEN 0      128          127.0.0.1:8790       0.0.0.0:*\n' > "$W/ss.out" ;;
  wildcard)   printf 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*\n'     > "$W/ss.out" ;;
esac
wpi_capture(){ WPI_CAP_OUT="$W/ss.out"; WPI_CAP_ERR="$EV_DIR/capture.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
( wpi_assert_listener_set ) > "$W/out" 2> "$W/err"; rc=$?
printf 'LISTENER_BYTES case=%s rc=%s accepting=%s parsed_complete=%s stop=[%s] fail=[%s] stderr_bytes=%s\n' \
  "$CASE" "$rc" "$(grep -c '^B6_listener_set ' "$W/out")" \
  "$(grep -c 'parse=complete_before_semantics' "$W/out")" \
  "$(grep '^B6_STOP ' "$W/out" | head -1 | sed 's/^B6_STOP reason=//')" \
  "$(grep '^B6_FAIL ' "$W/out" | head -1 | sed 's/^B6_FAIL reason=//')" \
  "$(wc -c < "$W/err")"
ARM
for c in nul address port_range octet leading0 clean wildcard; do
  bash --noprofile --norc "$Q/f1_arm.sh" "$RED"   "$Q/f1-red-$c"   "$c" > "$Q/f1-red-$c.txt" 2>&1
  bash --noprofile --norc "$Q/f1_arm.sh" "$GREEN" "$Q/f1-green-$c" "$c" > "$Q/f1-green-$c.txt" 2>&1
  sed 's/^/RED   /' "$Q/f1-red-$c.txt"; sed 's/^/GREEN /' "$Q/f1-green-$c.txt"
done
expect_has f1_red_nul_false_pass    'LISTENER_BYTES case=nul rc=0 accepting=1 parsed_complete=1 stop=\[\] fail=\[\] stderr_bytes=0' "$Q/f1-red-nul.txt"
expect_has f1_green_nul_stop        'LISTENER_BYTES case=nul rc=3 accepting=0 parsed_complete=0 stop=\[listener_inventory_unreadable_or_unparseable rc=0 detail=nul_byte_in_inventory\] fail=\[\] stderr_bytes=0' "$Q/f1-green-nul.txt"
expect_has f1_red_addr_fail         'LISTENER_BYTES case=address rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790\]' "$Q/f1-red-address.txt"
expect_has f1_green_addr_stop       'LISTENER_BYTES case=address rc=3 accepting=0 parsed_complete=0 stop=\[listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar\] fail=\[\]' "$Q/f1-green-address.txt"
expect_has f1_red_port_fail         'LISTENER_BYTES case=port_range rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[listener_set_unexpected observed_count=0 expected=1x127.0.0.1:8790\]' "$Q/f1-red-port_range.txt"
expect_has f1_green_port_stop       'LISTENER_BYTES case=port_range rc=3 accepting=0 parsed_complete=0 stop=\[listener_inventory_unreadable_or_unparseable rc=0 detail=local_port_range port=99999\] fail=\[\]' "$Q/f1-green-port_range.txt"
expect_has f1_red_octet_fail        'LISTENER_BYTES case=octet rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[listener_set_unexpected observed=non_preregistered_address' "$Q/f1-red-octet.txt"
expect_has f1_green_octet_stop      'LISTENER_BYTES case=octet rc=3 accepting=0 parsed_complete=0 stop=\[listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar\]' "$Q/f1-green-octet.txt"
expect_has f1_red_leading0_fail     'LISTENER_BYTES case=leading0 rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[listener_set_unexpected observed_count=0' "$Q/f1-red-leading0.txt"
expect_has f1_green_leading0_stop   'LISTENER_BYTES case=leading0 rc=3 accepting=0 parsed_complete=0 stop=\[listener_inventory_unreadable_or_unparseable rc=0 detail=local_port_grammar\]' "$Q/f1-green-leading0.txt"
expect_has f1_red_clean_pass        'LISTENER_BYTES case=clean rc=0 accepting=1 parsed_complete=1 stop=\[\] fail=\[\]' "$Q/f1-red-clean.txt"
expect_has f1_green_clean_pass      'LISTENER_BYTES case=clean rc=0 accepting=1 parsed_complete=1 stop=\[\] fail=\[\]' "$Q/f1-green-clean.txt"
expect_has f1_red_wildcard_fail     'LISTENER_BYTES case=wildcard rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f1-red-wildcard.txt"
expect_has f1_green_wildcard_fail   'LISTENER_BYTES case=wildcard rc=1 accepting=0 parsed_complete=1 stop=\[\] fail=\[nonloopback_listener addr=0.0.0.0\]' "$Q/f1-green-wildcard.txt"
# The `bytes=` field on the inventory line is the block's own accounting of every
# byte it consumed. It is compared here against an independent `wc -c` of the
# captured file: equal counts are the conservation equation the NUL record broke,
# measured rather than asserted.
for c in clean wildcard; do
  WC=$(wc -c < "$Q/f1-green-$c/ss.out")
  FIELD=$(sed -n 's/.*B6_listener_inventory rows=[0-9]* port_8790_rows=[0-9]* bytes=\([0-9]*\) .*/\1/p' "$Q/f1-green-$c/out")
  printf 'LISTENER_CONSERVATION case=%s independent_wc_c=%s block_bytes_field=%s\n' "$c" "$WC" "$FIELD"
  expect_eq "listener_conservation_$c" "$FIELD" "$WC"
done

# ===========================================================================
# FINDING 2 (HIGH) - truncated or invented status-parser result records become
# semantic FAILs. The arm feeds one child result record and rc pair to the REAL
# wpi_assert_status. `type_ok`, `mismatch_ok`, `missing_ok` and `ok` are the
# no-weakening controls: the four records the child really can emit must keep
# their round-5 dispositions exactly.
# ===========================================================================
cat > "$Q/f2_arm.sh" <<'ARM'
S="$1"; W="$2"; REC="$3"; RC="$4"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
wpi_capture(){
  local label="$1"; WPI_CAP_OUT="$EV_DIR/$label.out"; WPI_CAP_ERR="$EV_DIR/$label.err"; : > "$WPI_CAP_ERR"
  case "$label" in
    status_get)  printf '200\n' > "$WPI_CAP_OUT"; WPI_CAP_RC=0 ;;
    status_json) printf '%s\n' "$REC" > "$WPI_CAP_OUT"; WPI_CAP_RC="$RC" ;;
  esac
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
}
( wpi_assert_status ) > "$W/out" 2> "$W/err"; rc=$?
printf 'STATUS_RECORD rec=[%s] child_rc=%s rc=%s result=[%s] stderr_bytes=%s\n' \
  "$REC" "$RC" "$rc" "$(grep -E '^B5_(FAIL|STOP|status) ' "$W/out" | head -1)" "$(wc -c < "$W/err")"
ARM
f2(){
  bash --noprofile --norc "$Q/f2_arm.sh" "$RED"   "$Q/f2-red-$1"   "$2" "$3" > "$Q/f2-red-$1.txt" 2>&1
  bash --noprofile --norc "$Q/f2_arm.sh" "$GREEN" "$Q/f2-green-$1" "$2" "$3" > "$Q/f2-green-$1.txt" 2>&1
  sed 's/^/RED   /' "$Q/f2-red-$1.txt"; sed 's/^/GREEN /' "$Q/f2-green-$1.txt"
}
DIG=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913
f2 type_short      'TYPE state str' 5
f2 type_expected   'TYPE state str int' 5
f2 type_selfsame   'TYPE state str str' 5
f2 type_field      'TYPE rogue str str' 5
f2 mismatch_short  'MISMATCH state abc' 1
f2 mismatch_field  "MISMATCH rogue $DIG" 1
f2 missing_field   'MISSING rogue' 4
f2 type_ok         'TYPE state_version str int' 5
f2 mismatch_ok     "MISMATCH state $DIG" 1
f2 missing_ok      'MISSING state_version' 4
# ROUND-9 CHANGE, subject-specific fixture: the parser's accepting record gained
# the digest of the bytes the parser itself read, because round 8 rendered
# `body_sha256` from a separate `sha256sum` over the leaf NAME and an executed
# fixture made that field report the child's ARMED body beside an accepting
# DISARMED verdict (Codex round-8 part B finding 1). A stub standing in for a
# parser must emit the record ITS OWN subject's parser can emit, so the record is
# now chosen per subject and pinned as a constant for each - it is not read from
# the subject, which would make the check unfalsifiable. Every other fixture,
# mode and expected disposition in this group is unchanged.
f2s(){ # the accepting record differs between the subjects; everything else does not
  bash --noprofile --norc "$Q/f2_arm.sh" "$RED"   "$Q/f2-red-$1"   "$2" "$4" > "$Q/f2-red-$1.txt" 2>&1
  bash --noprofile --norc "$Q/f2_arm.sh" "$GREEN" "$Q/f2-green-$1" "$3" "$4" > "$Q/f2-green-$1.txt" 2>&1
  sed 's/^/RED   /' "$Q/f2-red-$1.txt"; sed 's/^/GREEN /' "$Q/f2-green-$1.txt"
}
f2s ok             'OK fields=8' 'OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000' 0
f2 ok_nodigest     'OK fields=8' 0
f2 ok_baddigest    'OK fields=8 sha256=zz' 0
expect_has f2_red_type_short_fail   'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=\]' "$Q/f2-red-type_short.txt"
expect_has f2_green_type_short_stop 'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_grammar tokens=3\]' "$Q/f2-green-type_short.txt"
expect_has f2_red_type_exp_fail     'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=int\]' "$Q/f2-red-type_expected.txt"
expect_has f2_green_type_exp_stop   'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_expected_type field=state\]' "$Q/f2-green-type_expected.txt"
expect_has f2_red_type_same_fail    'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=str\]' "$Q/f2-red-type_selfsame.txt"
expect_has f2_green_type_same_stop  'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_not_a_deviation field=state\]' "$Q/f2-green-type_selfsame.txt"
expect_has f2_red_type_field_fail   'rc=1 result=\[B5_FAIL reason=flag_mismatch field=rogue observed_type=str expected_type=str\]' "$Q/f2-red-type_field.txt"
expect_has f2_green_type_field_stop 'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_field\]' "$Q/f2-green-type_field.txt"
expect_has f2_red_mis_short_fail    'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=abc expected=preregistered_typed_value\]' "$Q/f2-red-mismatch_short.txt"
expect_has f2_green_mis_short_stop  'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=mismatch_record_digest\]' "$Q/f2-green-mismatch_short.txt"
expect_has f2_red_mis_field_fail    "rc=1 result=\[B5_FAIL reason=flag_mismatch field=rogue observed_sha256=$DIG expected=preregistered_typed_value\]" "$Q/f2-red-mismatch_field.txt"
expect_has f2_green_mis_field_stop  'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=mismatch_record_field\]' "$Q/f2-green-mismatch_field.txt"
expect_has f2_red_missing_field     'rc=3 result=\[B5_STOP reason=schema_unexpected field=rogue\]' "$Q/f2-red-missing_field.txt"
expect_has f2_green_missing_field   'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=missing_record_field\]' "$Q/f2-green-missing_field.txt"
expect_has f2_red_type_ok           'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int\]' "$Q/f2-red-type_ok.txt"
expect_has f2_green_type_ok         'rc=1 result=\[B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int\]' "$Q/f2-green-type_ok.txt"
expect_has f2_red_mismatch_ok       "rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=$DIG expected=preregistered_typed_value\]" "$Q/f2-red-mismatch_ok.txt"
expect_has f2_green_mismatch_ok     "rc=1 result=\[B5_FAIL reason=flag_mismatch field=state observed_sha256=$DIG expected=preregistered_typed_value\]" "$Q/f2-green-mismatch_ok.txt"
expect_has f2_red_missing_ok        'rc=3 result=\[B5_STOP reason=schema_unexpected field=state_version\]' "$Q/f2-red-missing_ok.txt"
expect_has f2_green_missing_ok      'rc=3 result=\[B5_STOP reason=schema_unexpected field=state_version\]' "$Q/f2-green-missing_ok.txt"
expect_has f2_red_ok                'rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2-red-ok.txt"
expect_has f2_green_ok              'rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2-green-ok.txt"
# ROUND-9 ADDITION, and it is what makes the changed `ok` fixture honest: the
# digest in the accepting record is REQUIRED, not tolerated. The round-8 record
# and a record with a malformed digest both reach the accepting line on RED and
# neither reaches it on GREEN, so the fixture change did not simply relabel the
# input the arm feeds - it feeds an input the two subjects genuinely disagree on.
expect_has f2_red_ok_nodigest       'rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2-red-ok_nodigest.txt"
expect_has f2_green_ok_nodigest     'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=0\]' "$Q/f2-green-ok_nodigest.txt"
expect_has f2_green_ok_baddigest    'rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=ok_record_digest\]' "$Q/f2-green-ok_baddigest.txt"

# ---------------------------------------------------------------------------
# The schema is declared ONCE. The parent's grammar and the child's table are
# the same string, passed as argv[2], and the child refuses to answer if they
# differ - so the parent cannot drift into checking a contract the child is not
# executing (pattern 11). Real CPython, real production body; only the MSYS
# argv/CRLF plumbing is substituted, exactly as disclosed for rounds 4 and 5.
# ---------------------------------------------------------------------------
cat > "$Q/f2_schema_arm.sh" <<'ARM'
S="$1"; W="$2"; MUTATE="$3"; PYEXE="$4"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_PYTHON3="$PYEXE"
[ "$MUTATE" = no ] || WPI_STATUS_SCHEMA='state:int state_version:int mode:str network:str exchange_conn:str exchange_enabled:bool credential_lookup:str arm_enabled:bool'
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
CALL=0
forge_capture(){
  # ROUND-9 CHANGE: production hands a child an already-open descriptor for an
  # object it must not address by name, so this stub supplies the same one -
  # exactly as round 8 added the stderr capture descriptor to these stubs. The
  # fixtures, the interpreter, the flags and every expected outcome below are
  # unchanged; a stub that set only names would no longer be standing in for
  # `wpi_capture`.
  local cfd="$WPI_CAP_CHILD_FD" cslot="$WPI_CAP_CHILD_SLOT" sfd=""
  WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""
  local label="$1"; shift; local -a a=("$@"); local i exe
  CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/forge.$CALL.out"; WPI_CAP_ERR="$EV_DIR/forge.$CALL.err"
  WPI_CAP_RC=0; : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"
  exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
  for ((i=1; i<${#a[@]}; i++)); do
    case "${a[$i]}" in /*) [ ! -e "${a[$i]}" ] || a[$i]="$(cygpath -w "${a[$i]}")";; esac
  done
  if [ "$cslot" = in ]; then exec {sfd}<&0; exec <&"$cfd"; fi
  /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
  if [ -n "$sfd" ]; then exec <&"$sfd"; exec {sfd}<&-; sfd=""; fi
  tr -d '\r' < "$EV_DIR/raw.out" > "$WPI_CAP_OUT"; tr -d '\r' < "$EV_DIR/raw.err" > "$WPI_CAP_ERR"
}
wpi_capture(){
  if [ "$1" = status_json ]; then forge_capture "$@"
  else WPI_CAP_OUT="$EV_DIR/$1.out"; WPI_CAP_ERR="$EV_DIR/$1.err"; : > "$WPI_CAP_ERR"; printf '200\n' > "$WPI_CAP_OUT"; WPI_CAP_RC=0
       printf '{"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}' > "$EV_DIR/ro.status.body"; fi
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
}
( wpi_assert_status ) > "$W/out" 2> "$W/err"; rc=$?
printf 'STATUS_SCHEMA mutated=%s rc=%s result=[%s] child=[%s]\n' \
  "$MUTATE" "$rc" "$(grep -E '^B5_(FAIL|STOP|status) ' "$W/out" | head -1 | cut -c1-120)" "$(cat "$EV_DIR/forge.1.out" 2>&1 | head -1)"
ARM
bash --noprofile --norc "$Q/f2_schema_arm.sh" "$GREEN" "$Q/f2-schema-clean" no  "$PYEXE" > "$Q/f2-schema-clean.txt" 2>&1
bash --noprofile --norc "$Q/f2_schema_arm.sh" "$GREEN" "$Q/f2-schema-mut"   yes "$PYEXE" > "$Q/f2-schema-mut.txt" 2>&1
cat "$Q/f2-schema-clean.txt" "$Q/f2-schema-mut.txt"
expect_has f2_schema_clean 'STATUS_SCHEMA mutated=no rc=0 result=\[B5_status http=200 json=strict required_fields=8 flags=expected ' "$Q/f2-schema-clean.txt"
expect_has f2_schema_mut   'STATUS_SCHEMA mutated=yes rc=3 result=\[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3' "$Q/f2-schema-mut.txt"
expect_has f2_schema_mut_child 'child=\[PARSE schema_declaration_mismatch\]' "$Q/f2-schema-mut.txt"

# ===========================================================================
# FINDING 3 (MEDIUM) - invalid HTTP status tokens are reported as completed
# endpoint deviations. 500 and 401 are the no-weakening controls.
# ===========================================================================
cat > "$Q/f3_arm.sh" <<'ARM'
S="$1"; W="$2"; CODE="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_capture(){ WPI_CAP_OUT="$EV_DIR/code.out"; WPI_CAP_ERR="$EV_DIR/code.err"; printf '%s\n' "$CODE" > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
( wpi_assert_status ) > "$W/out" 2> "$W/err"; rc=$?
printf 'HTTP_CODE code=%s rc=%s result=[%s] stderr_bytes=%s\n' "$CODE" "$rc" "$(head -1 "$W/out")" "$(wc -c < "$W/err")"
ARM
for c in 000 099 600 500 401; do
  bash --noprofile --norc "$Q/f3_arm.sh" "$RED"   "$Q/f3-red-$c"   "$c" > "$Q/f3-red-$c.txt" 2>&1
  bash --noprofile --norc "$Q/f3_arm.sh" "$GREEN" "$Q/f3-green-$c" "$c" > "$Q/f3-green-$c.txt" 2>&1
  sed 's/^/RED   /' "$Q/f3-red-$c.txt"; sed 's/^/GREEN /' "$Q/f3-green-$c.txt"
done
expect_has f3_red_000_fail    'HTTP_CODE code=000 rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=000\]' "$Q/f3-red-000.txt"
expect_has f3_green_000_stop  'HTTP_CODE code=000 rc=3 result=\[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_no_response code=000\]' "$Q/f3-green-000.txt"
expect_has f3_red_099_fail    'HTTP_CODE code=099 rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=099\]' "$Q/f3-red-099.txt"
expect_has f3_green_099_stop  'HTTP_CODE code=099 rc=3 result=\[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_grammar\]' "$Q/f3-green-099.txt"
expect_has f3_red_600_fail    'HTTP_CODE code=600 rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=600\]' "$Q/f3-red-600.txt"
expect_has f3_green_600_stop  'HTTP_CODE code=600 rc=3 result=\[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_grammar\]' "$Q/f3-green-600.txt"
expect_has f3_red_500_fail    'HTTP_CODE code=500 rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f3-red-500.txt"
expect_has f3_green_500_fail  'HTTP_CODE code=500 rc=1 result=\[B5_FAIL reason=status_endpoint_unexpected_http code=500\]' "$Q/f3-green-500.txt"
expect_has f3_red_401_stop    'HTTP_CODE code=401 rc=3 result=\[B5_STOP reason=status_endpoint_access_denied code=401\]' "$Q/f3-red-401.txt"
expect_has f3_green_401_stop  'HTTP_CODE code=401 rc=3 result=\[B5_STOP reason=status_endpoint_access_denied code=401\]' "$Q/f3-green-401.txt"

# ===========================================================================
# FINDING 4 (MEDIUM) - the published command masked its own fence failures and
# carried no bound. Three arms:
#  (a) the round-5 `bash; printf; bash; printf` sequence, executed, returns 0
#      while both fences fail - the audit's own structural falsification;
#  (b) the CURRENT published command, extracted from this document and executed
#      with exactly two mechanical substitutions (its `cd` target, and the
#      /tmp fence-body prefix so a nested run cannot overwrite the bodies of
#      the run that is executing it) over a scratch document whose three fence
#      bodies are `exit 7`, `exit 9` and `exit 0`;
#  (c) the bound: the extracted command carries three explicit timeout wrappers,
#      and the same wrapper form with the bound scaled from 900s to 3s turns a
#      hanging body into rc 124 - a result distinct from both PASS and failure.
# ===========================================================================
cat > "$Q/f4_red.sh" <<'RED4'
Q="$1"
printf 'exit 7\n' > "$Q/r5.sh"
printf 'exit 9\n' > "$Q/r4.sh"
bash --noprofile --norc "$Q/r5.sh"; printf 'R5_FENCE_RC=%s\n' "$?"
bash --noprofile --norc "$Q/r4.sh"; printf 'R4_FENCE_RC=%s\n' "$?"
RED4
mkdir -p "$Q/f4red"
bash --noprofile --norc "$Q/f4_red.sh" "$Q/f4red" > "$Q/f4-red.txt" 2>&1; f4red=$?
sed 's/^/RED   /' "$Q/f4-red.txt"
printf 'PUBLISHED_RC_MASK round5_sequence_rc=%s inner_rcs=[%s]\n' "$f4red" "$(tr '\n' ',' < "$Q/f4-red.txt")"
expect_rc f4_red_masked "$f4red" 0

mkdir -p "$Q/fake"
{ printf '# RP7_R6_FENCE_BEGIN\nexit 7\n# RP7_R6_FENCE_END\n'
  printf '# RP7_QA_FENCE_BEGIN\nexit 9\n# RP7_QA_FENCE_END\n'
  printf '# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n'; } > "$Q/fake/SELF_QA_RP7.md"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$DOC" > "$Q/published.txt"
# The /tmp expression runs FIRST: sed applies every -e to the same line in order,
# so retargeting `cd` first would let the /tmp rule rewrite the new cd target as
# well - which leaves the command running in the real directory against the real
# document, i.e. re-entering this fence. Both substitutions are then asserted.
sed -e "s#/tmp/rp7-#$Q/fake/body-#g" -e "s#^cd /c/LAB/.*#cd $Q/fake#" "$Q/published.txt" > "$Q/f4_green.sh"
expect_rc f4_green_cd_retargeted "$(grep -c "^cd $Q/fake\$" "$Q/f4_green.sh")" 1
expect_rc f4_green_no_real_bodies "$(grep -c '/tmp/rp7-r6-fence-body.sh' "$Q/f4_green.sh")" 0
timeout 120 bash --noprofile --norc "$Q/f4_green.sh" > "$Q/f4-green.txt" 2>&1; f4green=$?
sed 's/^/GREEN /' "$Q/f4-green.txt"
printf 'PUBLISHED_RC_PROPAGATION round6_command_rc=%s substitutions=2\n' "$f4green"
expect_rc f4_green_propagates "$f4green" 1
expect_has f4_green_reports_fail 'PUBLISHED_COMMAND_RESULT=fence_failed' "$Q/f4-green.txt"
expect_has f4_green_rc6 'R6_FENCE_RC=7' "$Q/f4-green.txt"
expect_has f4_green_rc5 'R5_FENCE_RC=9' "$Q/f4-green.txt"

# ROUND-9 CHANGE, and the change is a RESTORATION of discriminating power the
# round-8 edit removed. Round 8 replaced a fixed wrapper count with
# `count(wrappers) == count(extractions)` and called that strictly stronger. It is
# not: two equal counts do not establish a one-to-one mapping. Codex round-9 part
# B finding 4 executed the counter-example - a document whose R8 wrapper names the
# R7 body runs the R7 body twice, never runs the R8 body at all, and passes that
# assertion with both counts still equal.
#
# The check below is the mapping itself. For each fence it requires EXACTLY one
# extraction line writing that fence's own body path, EXACTLY one wrapper line
# whose `sh -c` operand is that same body path and whose body-stderr operand and
# rc variable are that fence's own, that the body path occurs on EXACTLY one
# wrapper line anywhere in the command, and EXACTLY one classifier call binding
# that fence's rc variable to its own wrapper stream. The totals are then required
# equal to the table size, so a fence added without a wrapper - the case the count
# check was for - still fails here.
#
# The old assertion is kept alongside and run on the same mutant, so the claim
# `this change restored power` is executed rather than asserted.
map_check(){ # $1 = published command text, $2 = label; prints per-fence rows
  local cmd="$1" label="$2" spec marker rest tag var body err x w o c bad=0 xt=0 wt=0
  for spec in R9:r9:R9 R8:r8:R8 R7:r7:R7 R6:r6:R6 QA:r5:R5 R4:r4:R4; do
    marker=${spec%%:*}; rest=${spec#*:}; tag=${rest%%:*}; var=${rest##*:}
    body=/tmp/rp7-$tag-fence-body.sh; err=/tmp/rp7-$tag-body.err
    x=$(grep -c -F -x -- "sed -n '/^# RP7_${marker}_FENCE_BEGIN\$/,/^# RP7_${marker}_FENCE_END\$/p' SELF_QA_RP7.md > $body" "$cmd")
    w=$(grep -c -F -x -- "${var}_W=\$(timeout --verbose --signal=TERM --kill-after=30s 900s sh -c 'exec 2>\"\$1\"; exec bash --noprofile --norc \"\$0\"' $body $err 2>&1 1>&3); ${var}=\$?" "$cmd")
    o=$(grep -F -- 'timeout --verbose --signal=TERM' "$cmd" | grep -c -F -- " $body ")
    c=$(grep -c -F -x -- "classify $tag \"\$${var}\" \"\$${var}_W\"" "$cmd")
    printf 'PUBLISHED_MAP text=%s fence=%s extractions=%s wrappers=%s wrapper_operand_occurrences=%s classifier_calls=%s\n' \
      "$label" "$tag" "$x" "$w" "$o" "$c"
    [ "$x" -eq 1 ] && [ "$w" -eq 1 ] && [ "$o" -eq 1 ] && [ "$c" -eq 1 ] || bad=$((bad+1))
    xt=$((xt+x)); wt=$((wt+w))
  done
  MAP_BAD=$bad
  MAP_WRAPPERS=$(grep -c -F -- "timeout --verbose --signal=TERM --kill-after=30s 900s sh -c" "$cmd")
  MAP_EXTRACTIONS=$(grep -c -- 'FENCE_BEGIN[$]/,/^# RP7_' "$cmd")
  MAP_CLASSIFIERS=$(grep -c -- '^classify ' "$cmd")
  printf 'PUBLISHED_MAP_RESULT text=%s fences=6 per_fence_mismatches=%s total_wrappers=%s total_extractions=%s total_classifier_calls=%s bound_rows=%s\n' \
    "$label" "$bad" "$MAP_WRAPPERS" "$MAP_EXTRACTIONS" "$MAP_CLASSIFIERS" "$xt/$wt"
}
# The mutant: only the R8 wrapper's `sh -c` body operand is retargeted at the R7
# body. Both counts stay at 6; the mapping does not.
sed "s#' /tmp/rp7-r8-fence-body.sh /tmp/rp7-r8-body.err#' /tmp/rp7-r7-fence-body.sh /tmp/rp7-r8-body.err#" \
  "$Q/published.txt" > "$Q/published-mutant.txt"
expect_rc f4_map_mutant_differs "$(cmp -s "$Q/published.txt" "$Q/published-mutant.txt" && echo 0 || echo 1)" 1
map_check "$Q/published.txt" green > "$Q/map-green.txt"; GREEN_BAD=$MAP_BAD
GREEN_W=$MAP_WRAPPERS; GREEN_X=$MAP_EXTRACTIONS; GREEN_C=$MAP_CLASSIFIERS
map_check "$Q/published-mutant.txt" mutant > "$Q/map-mutant.txt"; MUT_BAD=$MAP_BAD
MUT_W=$MAP_WRAPPERS; MUT_X=$MAP_EXTRACTIONS
cat "$Q/map-green.txt" "$Q/map-mutant.txt"
# The old assertion accepts the mutant; the new one rejects it. Both accept the
# real command, so the repair added rejection without trading away acceptance.
printf 'MAPPING_ASSERTION_POWER round8_on_green=%s round8_on_mutant=%s round9_on_green=%s round9_on_mutant=%s\n' \
  "$([ "$GREEN_W" -eq "$GREEN_X" ] && echo accept || echo reject)" \
  "$([ "$MUT_W" -eq "$MUT_X" ] && echo accept || echo reject)" \
  "$([ "$GREEN_BAD" -eq 0 ] && echo accept || echo reject)" \
  "$([ "$MUT_BAD" -eq 0 ] && echo accept || echo reject)" > "$Q/map-power.txt"
cat "$Q/map-power.txt"
expect_has f4_mapping_power 'MAPPING_ASSERTION_POWER round8_on_green=accept round8_on_mutant=accept round9_on_green=accept round9_on_mutant=reject' "$Q/map-power.txt"
expect_rc f4_map_green_clean "$GREEN_BAD" 0
expect_rc f4_bound_wrappers "$GREEN_W" 6
expect_rc f4_bound_extractions "$GREEN_X" 6
expect_rc f4_bound_classifiers "$GREEN_C" 6
expect_has f4_map_mutant_omits_r8 'PUBLISHED_MAP text=mutant fence=r8 extractions=1 wrappers=0 wrapper_operand_occurrences=0 classifier_calls=1' "$Q/map-mutant.txt"
expect_has f4_map_mutant_duplicates_r7 'PUBLISHED_MAP text=mutant fence=r7 extractions=1 wrappers=1 wrapper_operand_occurrences=2 classifier_calls=1' "$Q/map-mutant.txt"
DOCBOUND=$(grep -c 'fence-timeout budget' "$DOC")
printf 'PUBLISHED_BOUND timeout_wrappers=%s extracted_fence_bodies=%s documented_budget_mentions=%s\n' "$GREEN_W" "$GREEN_X" "$DOCBOUND"
[ "$DOCBOUND" -ge 1 ] || { printf 'QA_ASSERT_FAIL name=f4_bound_documented got=%s\n' "$DOCBOUND"; exit 90; }
printf '/usr/bin/sleep 30\n' > "$Q/hang.sh"
t0=$SECONDS
timeout --signal=TERM --kill-after=30s 3s bash --noprofile --norc "$Q/hang.sh"; hangrc=$?
t1=$((SECONDS-t0))
printf 'PUBLISHED_BOUND_ENFORCED scaled_bound_s=3 rc=%s wall_s=%s\n' "$hangrc" "$t1"
expect_rc f4_bound_enforced "$hangrc" 124
[ "$t1" -le 8 ] || { printf 'QA_ASSERT_FAIL name=f4_bound_wall got=%s\n' "$t1"; exit 90; }

# ===========================================================================
# RECOVERED TEST (salvage from the interrupted round-5 review) - the capture
# leaf is replaced between allocation and write. The injection is through a
# hooked wpi_clock_ms, so this is not a route the block reaches on its own; the
# defensible statement is about what the block ESTABLISHES, and round 5
# established nothing about the identity of the object it wrote to.
# ===========================================================================
cat > "$Q/f5_arm.sh" <<'ARM'
S="$1"; W="$2"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10; WPI_PROBE_SEQ=0
OUTSIDE="$W/outside.txt"; printf 'ORIGINAL\n' > "$OUTSIDE"
HOOK=0
wpi_clock_ms(){
  HOOK=$((HOOK+1))
  if [ "$HOOK" -eq 1 ]; then rm -- "$WPI_CAP_OUT"; ln -- "$OUTSIDE" "$WPI_CAP_OUT"; fi
  WPI_LINE="$HOOK"
}
# Round 8 note: the capture runs in a SUBSHELL so the arm survives a STOP and can
# still report the outside file, which is what this arm measures. On this
# workstation the repaired block additionally STOPs here, because the read
# binding re-opens `/dev/fd/<n>` and MSYS2 cannot re-open the descriptor of a
# leaf whose name has just been unlinked; Linux can, and would return rc 0.
# Round 7 introduced the subshell and, in the same edit, relaxed the GREEN
# assertion from `rc=0` to the basic regex `rc=[0-9]*`, which accepts ANY decimal
# status. That was not needed to survive the STOP and it removed a control: Codex
# round-7 part B finding 1 inserted an unrelated `return 7` at the top of
# `wpi_capture` and the relaxed assertion passed where the predecessor failed.
# The status is pinned again below, to the exact set of two outcomes this arm can
# legitimately produce, and the auditor's mutation is now an arm of this fence.
( wpi_capture leaf_race /usr/bin/printf 'CAPTURED\n' ) > "$W/cap.out" 2>&1
rc=$?
printf 'LEAF_RACE rc=%s outside_text=%s outside_bytes=%s payload_left_the_tree=%s capture_result=[%s]\n' \
  "$rc" "$(tr -d '\n' < "$OUTSIDE")" "$(wc -c < "$OUTSIDE")" \
  "$(grep -q CAPTURED "$OUTSIDE" && echo yes || echo no)" \
  "$(sed -e "s#$W#<scratch>#g" "$W/cap.out" | tr '\n' ' ' | sed 's/ *$//')"
ARM
# The no-weakening mutant for the assertion itself: an unrelated regression that
# makes `wpi_capture` return 7 without ever touching the leaf. It leaves the
# outside file alone, so it is invisible to any assertion that only looks at the
# outside file - which is precisely why the round-7 regex accepted it.
sed '/^wpi_capture() {/a\    return 7' "$GREEN" > "$Q/f5-mutant-return7.sh"
bash --noprofile --norc -n "$Q/f5-mutant-return7.sh"; F5_MUT_N=$?
bash --noprofile --norc "$Q/f5_arm.sh" "$RED"                    "$Q/f5-red"    > "$Q/f5-red.txt"    2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN"                  "$Q/f5-green"  > "$Q/f5-green.txt"  2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$Q/f5-mutant-return7.sh" "$Q/f5-mutant" > "$Q/f5-mutant.txt" 2>&1
sed 's/^/RED    /' "$Q/f5-red.txt"; sed 's/^/GREEN  /' "$Q/f5-green.txt"; sed 's/^/MUTANT /' "$Q/f5-mutant.txt"
expect_has f5_red_escapes 'LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes' "$Q/f5-red.txt"

# The round-8 assertion. Exactly two outcomes are legitimate for a confined
# capture whose leaf name was unlinked under it, and each pins its status:
#   rc 0 with an EMPTY capture result - the /dev/fd re-open through the still-open
#     creating descriptor succeeded although the name was gone (Linux); or
#   rc 3 with EXACTLY the documented STOP and nothing else - MSYS2 cannot re-open
#     the descriptor of an unlinked leaf, so the capture STOPs before returning.
# Anything else - any other status, an empty status, or either status carrying
# unexpected output - is `unclassified` and fails the fence.
f5_classify(){
  if grep -q 'LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=\[\]$' "$1"; then
    printf 'descriptor_rebind_supported_rc0\n'
  elif grep -q 'LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=\[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro\.0001\.leaf_race\.stdout\]$' "$1"; then
    printf 'unlinked_leaf_not_rebindable_rc3\n'
  else
    printf 'unclassified\n'
  fi
}
f5_new_assert(){ case "$(f5_classify "$1")" in unclassified) printf 'reject\n' ;; *) printf 'accept\n' ;; esac; }
# The round-7 assertion verbatim, kept as a MEASURING INSTRUMENT, never as a gate:
# the fence asserts below that it accepts the mutant the round-8 assertion rejects,
# which is the executed demonstration that the round-7 edit removed discriminating
# power rather than a claim in prose that it did.
f5_old_assert(){
  if grep -q 'LEAF_RACE rc=[0-9]* outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no' "$1"; then
    printf 'accept\n'
  else
    printf 'reject\n'
  fi
}
F5_GREEN_KIND=$(f5_classify "$Q/f5-green.txt")
F5_MUT_KIND=$(f5_classify "$Q/f5-mutant.txt")
F5_RED_KIND=$(f5_classify "$Q/f5-red.txt")
printf 'LEAF_RACE_DISCRIMINATION mutant_bash_n=%s green_kind=%s mutant_kind=%s red_kind=%s new_on_green=%s new_on_mutant=%s new_on_red=%s old_on_green=%s old_on_mutant=%s old_on_red=%s\n' \
  "$F5_MUT_N" "$F5_GREEN_KIND" "$F5_MUT_KIND" "$F5_RED_KIND" \
  "$(f5_new_assert "$Q/f5-green.txt")" "$(f5_new_assert "$Q/f5-mutant.txt")" "$(f5_new_assert "$Q/f5-red.txt")" \
  "$(f5_old_assert "$Q/f5-green.txt")" "$(f5_old_assert "$Q/f5-mutant.txt")" "$(f5_old_assert "$Q/f5-red.txt")"
expect_rc f5_mutant_parses "$F5_MUT_N" 0
expect_eq f5_green_confined     "$(f5_new_assert "$Q/f5-green.txt")"  accept
expect_eq f5_new_rejects_mutant "$(f5_new_assert "$Q/f5-mutant.txt")" reject
expect_eq f5_new_rejects_red    "$(f5_new_assert "$Q/f5-red.txt")"    reject
expect_eq f5_old_accepts_mutant "$(f5_old_assert "$Q/f5-mutant.txt")" accept
expect_eq f5_old_rejects_red    "$(f5_old_assert "$Q/f5-red.txt")"    reject

# Static: no shell-side write in the block re-opens a leaf by name. The status
# body is the one disclosed exception, because curl is handed a path.
GREEN_APPEND=$(grep -v '^[[:space:]]*#' "$GREEN" | grep -c '>>"\$')
RED_APPEND=$(grep -v '^[[:space:]]*#' "$RED" | grep -c '>>"\$')
GREEN_OPEN=$(grep -c '^wpi_open_leaf() {' "$GREEN")
RED_OPEN=$(grep -c '^wpi_open_leaf() {' "$RED")
printf 'LEAF_WRITE_STATIC red_name_appends=%s green_name_appends=%s red_open_leaf=%s green_open_leaf=%s\n' \
  "$RED_APPEND" "$GREEN_APPEND" "$RED_OPEN" "$GREEN_OPEN"
expect_rc f5_red_appends "$RED_APPEND" 12
expect_rc f5_green_appends "$GREEN_APPEND" 0
expect_rc f5_red_open_leaf "$RED_OPEN" 0
expect_rc f5_green_open_leaf "$GREEN_OPEN" 1

case "$Q" in /tmp/rp7-r6-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_SCRATCH_UNSAFE=%s\n' "$Q"; exit 97 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_R6_FENCE_END
```

### Round-6 transcript

```text
QA_ROOT=/tmp/rp7-r6-qa.5kLrmK
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=77179 red_sha256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee red_cr=0 red_bash_n=0 green_bytes=108301 green_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62 green_cr=0 green_bash_n=0
RED   LISTENER_BYTES case=nul rc=0 accepting=1 parsed_complete=1 stop=[] fail=[] stderr_bytes=0
GREEN LISTENER_BYTES case=nul rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=nul_byte_in_inventory] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=address rc=1 accepting=0 parsed_complete=1 stop=[] fail=[listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790] stderr_bytes=0
GREEN LISTENER_BYTES case=address rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=port_range rc=1 accepting=0 parsed_complete=1 stop=[] fail=[listener_set_unexpected observed_count=0 expected=1x127.0.0.1:8790] stderr_bytes=0
GREEN LISTENER_BYTES case=port_range rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=local_port_range port=99999] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=octet rc=1 accepting=0 parsed_complete=1 stop=[] fail=[listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790] stderr_bytes=0
GREEN LISTENER_BYTES case=octet rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=leading0 rc=1 accepting=0 parsed_complete=1 stop=[] fail=[listener_set_unexpected observed_count=0 expected=1x127.0.0.1:8790] stderr_bytes=0
GREEN LISTENER_BYTES case=leading0 rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=local_port_grammar] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=clean rc=0 accepting=1 parsed_complete=1 stop=[] fail=[] stderr_bytes=0
GREEN LISTENER_BYTES case=clean rc=0 accepting=1 parsed_complete=1 stop=[] fail=[] stderr_bytes=0
RED   LISTENER_BYTES case=wildcard rc=1 accepting=0 parsed_complete=1 stop=[] fail=[nonloopback_listener addr=0.0.0.0] stderr_bytes=0
GREEN LISTENER_BYTES case=wildcard rc=1 accepting=0 parsed_complete=1 stop=[] fail=[nonloopback_listener addr=0.0.0.0] stderr_bytes=0
LISTENER_CONSERVATION case=clean independent_wc_c=58 block_bytes_field=58
LISTENER_CONSERVATION case=wildcard independent_wc_c=36 block_bytes_field=36
RED   STATUS_RECORD rec=[TYPE state str] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE state str] child_rc=5 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_grammar tokens=3] stderr_bytes=0
RED   STATUS_RECORD rec=[TYPE state str int] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=int] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE state str int] child_rc=5 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_expected_type field=state] stderr_bytes=0
RED   STATUS_RECORD rec=[TYPE state str str] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=str] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE state str str] child_rc=5 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_not_a_deviation field=state] stderr_bytes=0
RED   STATUS_RECORD rec=[TYPE rogue str str] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=rogue observed_type=str expected_type=str] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE rogue str str] child_rc=5 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=type_record_field] stderr_bytes=0
RED   STATUS_RECORD rec=[MISMATCH state abc] child_rc=1 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=abc expected=preregistered_typed_value] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISMATCH state abc] child_rc=1 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=mismatch_record_digest] stderr_bytes=0
RED   STATUS_RECORD rec=[MISMATCH rogue b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913] child_rc=1 rc=1 result=[B5_FAIL reason=flag_mismatch field=rogue observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISMATCH rogue b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913] child_rc=1 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=mismatch_record_field] stderr_bytes=0
RED   STATUS_RECORD rec=[MISSING rogue] child_rc=4 rc=3 result=[B5_STOP reason=schema_unexpected field=rogue] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISSING rogue] child_rc=4 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=missing_record_field] stderr_bytes=0
RED   STATUS_RECORD rec=[TYPE state_version str int] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE state_version str int] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int] stderr_bytes=0
RED   STATUS_RECORD rec=[MISMATCH state b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913] child_rc=1 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISMATCH state b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913] child_rc=1 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value] stderr_bytes=0
RED   STATUS_RECORD rec=[MISSING state_version] child_rc=4 rc=3 result=[B5_STOP reason=schema_unexpected field=state_version] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISSING state_version] child_rc=4 rc=3 result=[B5_STOP reason=schema_unexpected field=state_version] stderr_bytes=0
RED   STATUS_RECORD rec=[OK fields=8] child_rc=0 rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site] stderr_bytes=0
GREEN STATUS_RECORD rec=[OK fields=8 sha256=0000000000000000000000000000000000000000000000000000000000000000] child_rc=0 rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site] stderr_bytes=0
RED   STATUS_RECORD rec=[OK fields=8] child_rc=0 rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site] stderr_bytes=0
GREEN STATUS_RECORD rec=[OK fields=8] child_rc=0 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=0] stderr_bytes=0
RED   STATUS_RECORD rec=[OK fields=8 sha256=zz] child_rc=0 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=0 body_sha256=0000000000000000000000000000000000000000000000000000000000000000] stderr_bytes=0
GREEN STATUS_RECORD rec=[OK fields=8 sha256=zz] child_rc=0 rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=ok_record_digest] stderr_bytes=0
STATUS_SCHEMA mutated=no rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=e6b47cabfa9d22736f64be7720b0365759de97d24984] child=[OK fields=8 sha256=e6b47cabfa9d22736f64be7720b0365759de97d24984db95deedd9e9a5f8acf8]
STATUS_SCHEMA mutated=yes rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3] child=[PARSE schema_declaration_mismatch]
RED   HTTP_CODE code=000 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=000] stderr_bytes=0
GREEN HTTP_CODE code=000 rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_no_response code=000] stderr_bytes=0
RED   HTTP_CODE code=099 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=099] stderr_bytes=0
GREEN HTTP_CODE code=099 rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_grammar] stderr_bytes=0
RED   HTTP_CODE code=600 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=600] stderr_bytes=0
GREEN HTTP_CODE code=600 rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=http_code_grammar] stderr_bytes=0
RED   HTTP_CODE code=500 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500] stderr_bytes=0
GREEN HTTP_CODE code=500 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500] stderr_bytes=0
RED   HTTP_CODE code=401 rc=3 result=[B5_STOP reason=status_endpoint_access_denied code=401] stderr_bytes=0
GREEN HTTP_CODE code=401 rc=3 result=[B5_STOP reason=status_endpoint_access_denied code=401] stderr_bytes=0
RED   R5_FENCE_RC=7
RED   R4_FENCE_RC=9
PUBLISHED_RC_MASK round5_sequence_rc=0 inner_rcs=[R5_FENCE_RC=7,R4_FENCE_RC=9,]
GREEN e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 */tmp/rp7-r6-qa.5kLrmK/fake/body-r9-fence-body.sh
GREEN e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 */tmp/rp7-r6-qa.5kLrmK/fake/body-r8-fence-body.sh
GREEN e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 */tmp/rp7-r6-qa.5kLrmK/fake/body-r7-fence-body.sh
GREEN dc4eac6b791d148fe12b95e51bf31a92ead1c32f9dde48255f263a0d28dbcb4f */tmp/rp7-r6-qa.5kLrmK/fake/body-r6-fence-body.sh
GREEN def46450e739e132ca3b14d87e783aec6d75a838316dc78d6d24fbecb302cb81 */tmp/rp7-r6-qa.5kLrmK/fake/body-r5-fence-body.sh
GREEN 585c97d2fcbe0bc2e3fbca0f841e68a26934c5434ed00a8a691a4919dd85f82f */tmp/rp7-r6-qa.5kLrmK/fake/body-r4-fence-body.sh
GREEN   0 /tmp/rp7-r6-qa.5kLrmK/fake/body-r9-fence-body.sh
GREEN   0 /tmp/rp7-r6-qa.5kLrmK/fake/body-r8-fence-body.sh
GREEN   0 /tmp/rp7-r6-qa.5kLrmK/fake/body-r7-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.5kLrmK/fake/body-r6-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.5kLrmK/fake/body-r5-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.5kLrmK/fake/body-r4-fence-body.sh
GREEN 141 total
GREEN R9_FENCE_RC=0
GREEN R8_FENCE_RC=0
GREEN R7_FENCE_RC=0
GREEN R6_FENCE_RC=7
GREEN R5_FENCE_RC=9
GREEN R4_FENCE_RC=0
GREEN WRAPPER_STREAM fence=r9 bytes=0 []
GREEN WRAPPER_STREAM fence=r8 bytes=0 []
GREEN WRAPPER_STREAM fence=r7 bytes=0 []
GREEN WRAPPER_STREAM fence=r6 bytes=0 []
GREEN PUBLISHED_COMMAND_RESULT=fence_failed fence=r6 rc=7
PUBLISHED_RC_PROPAGATION round6_command_rc=1 substitutions=2
PUBLISHED_MAP text=green fence=r9 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=green fence=r8 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=green fence=r7 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=green fence=r6 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=green fence=r5 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=green fence=r4 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP_RESULT text=green fences=6 per_fence_mismatches=0 total_wrappers=6 total_extractions=6 total_classifier_calls=6 bound_rows=6/6
PUBLISHED_MAP text=mutant fence=r9 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r8 extractions=1 wrappers=0 wrapper_operand_occurrences=0 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r7 extractions=1 wrappers=1 wrapper_operand_occurrences=2 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r6 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r5 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r4 extractions=1 wrappers=1 wrapper_operand_occurrences=1 classifier_calls=1
PUBLISHED_MAP_RESULT text=mutant fences=6 per_fence_mismatches=2 total_wrappers=6 total_extractions=6 total_classifier_calls=6 bound_rows=6/5
MAPPING_ASSERTION_POWER round8_on_green=accept round8_on_mutant=accept round9_on_green=accept round9_on_mutant=reject
PUBLISHED_BOUND timeout_wrappers=6 extracted_fence_bodies=6 documented_budget_mentions=4
PUBLISHED_BOUND_ENFORCED scaled_bound_s=3 rc=124 wall_s=3
RED    LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes capture_result=[]
GREEN  LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro.0001.leaf_race.stdout]
MUTANT LEAF_RACE rc=7 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[]
LEAF_RACE_DISCRIMINATION mutant_bash_n=0 green_kind=unlinked_leaf_not_rebindable_rc3 mutant_kind=unclassified red_kind=unclassified new_on_green=accept new_on_mutant=reject new_on_red=reject old_on_green=accept old_on_mutant=accept old_on_red=reject
LEAF_WRITE_STATIC red_name_appends=12 green_name_appends=0 red_open_leaf=0 green_open_leaf=1
QA_PASS all_assertions=yes
```

Reading the load-bearing lines:

- `BYTE_IDENTITY` proves the RED subject is the audited round-5 blob and the GREEN subject is
  the repaired file, both LF-only and both `bash -n` clean.
- `LISTENER_BYTES case=nul rc=0 accepting=1 parsed_complete=1` is Codex's finding 1
  reproduced on the audited bytes: a record whose state field is `LIS<NUL>TEN` was normalised
  into `LISTEN` and reported as a complete parse and an accepting listener set. The GREEN row
  is `rc=3 ... detail=nul_byte_in_inventory` with no inventory line at all.
- The `address`, `port_range`, `octet` and `leading0` rows are the same defect in its other
  three shapes: each RED row is a host-state FAIL (`rc=1`) derived from a record that states
  no address or no port, and each GREEN row is the corresponding grammar STOP.
- `LISTENER_CONSERVATION case=<c> independent_wc_c=<n> block_bytes_field=<n>` is the
  conservation equation: the block's own count of the bytes it consumed equals `wc -c` of the
  file it consumed them from. That equality is what the NUL record broke.
- `LISTENER_BYTES case=clean` and `case=wildcard` are identical in RED and GREEN. Column
  padding still parses and a wildcard listener is still `B6_FAIL reason=nonloopback_listener`
  - the repair added no new STOP over well-formed input.
- The `STATUS_RECORD` pairs are finding 2. Every RED line for a malformed producer record is
  `rc=1` with a `B5_FAIL`; every GREEN line is `rc=3` with a `detail=*_record_*` STOP naming
  the grammar rule that failed. The four `*_ok` rows and the `ok` row are byte-identical
  between RED and GREEN.
- `STATUS_SCHEMA mutated=yes ... child=[PARSE schema_declaration_mismatch]` proves the schema
  is one declaration and not two: the parent's grammar table and the child's typed table are
  the same string, and the child refuses to answer if they differ.
- The `HTTP_CODE` pairs are finding 3, with `500` and `401` unchanged.
- `PUBLISHED_RC_MASK round5_sequence_rc=0 inner_rcs=[R5_FENCE_RC=7,R4_FENCE_RC=9,]` is
  finding 4 reproduced, and `PUBLISHED_RC_PROPAGATION round6_command_rc=1` is the repair,
  measured by executing the published command itself over a scratch document.
- `PUBLISHED_BOUND_ENFORCED scaled_bound_s=3 rc=124` is the bound doing work. Only the number
  differs from the published 900 s; the wrapper form is the published one.
- `LEAF_RACE ... payload_left_the_tree=yes` versus `no` is the recovered test, and
  `LEAF_WRITE_STATIC red_name_appends=12 green_name_appends=0` is the static half: no
  shell-side write in the repaired block re-opens a leaf by name. The GREEN row now also
  carries `rc=3` and `capture_result=[RP7_STOP reason=capture_stream_not_bindable ...]`,
  which is the MSYS2 limitation disclosed above and not a second finding: the block cannot
  re-open the descriptor of a leaf whose name has just been unlinked on this platform, so it
  STOPs instead of continuing. The assertion is on the outside file, which is untouched in
  both cases.

## The carried round-5 fence, re-run as a regression gate

The round-5 fence is reproduced below **unchanged except for the two GREEN identity
constants**, which name the subject file by hash and byte count and therefore have to name
the round-9 bytes. Everything else - every arm, every assertion, both anchor comments and
the RED blob at `d6a976aa` - is byte-identical to round 5, and its extracted body is
exactly 21263 B. The previous "same length" justification is deliberately withdrawn:
the body length is measured from the extracted fence body, not inferred from the changed
identity constants. Its one capture stub, `forge_capture`, drives only the `lock_parity`
child, whose readers are outside the round-8 binding change, so it needed no adaptation. The
discriminating-power argument for the one change is the same as it has always been: a
different subject file still fails, because the assertion is still exact equality and the
fence aborts before any arm runs. It is one half of the no-weakening gate: every round-5
repair (the tenth tool binding, package identity, the three `/dev/null` opens, evidence-root
provenance) must still hold on these bytes, and does.

Ten arm groups, each a real RED against the round-4 blob and a real GREEN against the
round-9 bytes:

| Arm | RED on round-4 bytes | GREEN on repaired bytes |
|---|---|---|
| F1 main-path binding | `python3_bound=no`, deviant pin ran, marker written, `RP7 PASS` | `python3_bound=yes`, real binding STOPs, no marker, no accepting line, no PASS |
| F1 window ordering | window opened and closed with nine tools bound | binding STOP occurs with the window still open |
| F2 clean universe | parity PASS | parity PASS (no regression) |
| F2 `Name` absent | accepting parity line for a universe never adjudicated | `B1_STOP ... detail=name_absent` |
| F2 `Version` absent | `B1_FAIL reason=lock_installed_parity` - a host finding for an unevaluable object | `B1_STOP ... detail=version_absent` |
| F2 duplicate canonical name | two distributions collapse to one, parity PASSes | `B1_STOP ... detail=canonical_name_duplicate` |
| F4 static | 3 non-comment `/dev/null` occurrences | 0 |
| F4 predicate check | satisfied by an *executable* named `rp0_require_safe_component` on PATH | refused; only a real shell function passes |
| F4 create-once | (unchanged) | second allocation STOPs, out-of-tree leaf STOPs, stderr stays empty with fd 2 closed |
| F5 evidence root | any `EV_DIR` accepted, constant absent | unfilled pin STOPs; descent accepted; outside and prefix-lookalike STOP |

```bash
# RP7_QA_FENCE_BEGIN
# Round-5 D026 fence for RP7-WPI-RO. Every arm drives the REAL production caller
# in a FRESH bash process against two byte sets whose identity is asserted first:
#   RED   = the frozen round-4 blob at commit d6a976aa (70941 B, 23e55667...01aad)
#   GREEN = the repaired worktree file
# No arm redeclares a production loop or a production predicate. Where an arm
# needs a stub it stubs the CALLEE and drives the real CALLER, so the arm fails
# if the caller stops calling it.
REPO=/c/LAB/Tradingview_LAB_CLEAN
BLOCK=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
REPO_VERIFIER=$REPO/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py
PYEXE=/c/Python314/python.exe
Q=$(mktemp -d /tmp/rp7-r5-qa.XXXXXX)
RED=$Q/RP7-WPI-RO.round4.sh
GREEN=$BLOCK

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_has(){ grep -q -- "$2" "$3" || { printf 'QA_ASSERT_FAIL name=%s missing=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_hasnt(){ grep -q -- "$2" "$3" && { printf 'QA_ASSERT_FAIL name=%s unexpected=[%s] file=%s\n' "$1" "$2" "$3"; exit 90; }; return 0; }

printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_stat=%s python=%s git=%s uid_gid=%s:%s\n' \
    "$BASH_VERSION" "$(/usr/bin/stat --version | head -1 | sed 's/.* //')" \
    "$("$PYEXE" -V | sed 's/.* //')" "$(git --version | sed 's/.* //')" "$(id -u)" "$(id -g)"

# --- byte identity of both subjects -----------------------------------------
git -C "$REPO" cat-file blob d6a976aa:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh > "$RED"
RED_SHA=$(sha256sum < "$RED" | cut -d' ' -f1);   RED_BYTES=$(wc -c < "$RED")
GREEN_SHA=$(sha256sum < "$GREEN" | cut -d' ' -f1); GREEN_BYTES=$(wc -c < "$GREEN")
RED_CR=$(tr -cd '\r' < "$RED" | wc -c);  GREEN_CR=$(tr -cd '\r' < "$GREEN" | wc -c)
bash --noprofile --norc -n "$RED";   RED_N=$?
bash --noprofile --norc -n "$GREEN"; GREEN_N=$?
printf 'BYTE_IDENTITY red_bytes=%s red_sha256=%s red_cr=%s red_bash_n=%s green_bytes=%s green_sha256=%s green_cr=%s green_bash_n=%s\n' \
    "$RED_BYTES" "$RED_SHA" "$RED_CR" "$RED_N" "$GREEN_BYTES" "$GREEN_SHA" "$GREEN_CR" "$GREEN_N"
expect_eq red_sha256 "$RED_SHA" 23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad
expect_eq red_bytes "$RED_BYTES" 70941
expect_eq green_sha256 "$GREEN_SHA" 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
expect_eq green_bytes "$GREEN_BYTES" 108301
expect_rc red_cr "$RED_CR" 0
expect_rc green_cr "$GREEN_CR" 0
expect_rc red_bash_n "$RED_N" 0
expect_rc green_bash_n "$GREEN_N" 0

# ===========================================================================
# FINDING 1 (BLOCK) - python3 is never bound in the production main path.
# The arm drives the REAL wpi_main. wpi_bind_tool is replaced by a recorder that
# STOPs if and only if production asks it to bind python3, and the mount guard is
# replaced by markers so the ORDER of the binding relative to the initial window
# is read out of the production body rather than asserted. The deviant pin writes
# a marker and forges `OK fields=8` over an ARMED body.
# ===========================================================================
cat > "$Q/f1_arm.sh" <<'ARM'
S="$1"; W="$2"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
cat > "$W/bad-python" <<EOF
#!/usr/bin/env bash
printf x > "$W/marker"
printf 'OK fields=8\n'
EOF
chmod +x "$W/bad-python"
cat > "$W/curl" <<'EOF'
#!/usr/bin/env bash
out=
while [ "$#" -gt 0 ]; do
  if [ "$1" = --output ]; then out="$2"; shift 2; else shift; fi
done
printf '{"state":"ARMED"}\n' > "$out"
printf '200\n'
EOF
chmod +x "$W/curl"
: > "$W/bound"
wpi_validate_inputs(){
  EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; EV_LOG="$EV_DIR/log"; : > "$EV_LOG"
  WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=5
  WPI_SHA256SUM=/usr/bin/sha256sum; WPI_CURL="$W/curl"; WPI_PYTHON3="$W/bad-python"
  WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_TOOL_PINS=dummy
  WPI_PROBE_SEQ=0; WPI_MOUNT_SNAPSHOT_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
}
wpi_map_get(){ WPI_LINE="/usr/bin/$2"; }
wpi_bind_tool(){ printf '%s\n' "$1" >> "$W/bound"; [ "$1" != python3 ] || { printf 'BINDING_WOULD_STOP_python3\n'; exit 3; }; }
wpi_mount_guard_begin(){ printf 'MOUNT_WINDOW_OPEN\n'; }
wpi_mount_guard_end(){ printf 'MOUNT_WINDOW_CLOSED\n'; }
for f in wpi_assert_prerequisites wpi_assert_evidence_leaf_bound wpi_assert_manager_ready \
  wpi_assert_tree wpi_assert_metadata_dir wpi_assert_regular_digest wpi_assert_interpreter \
  wpi_assert_metadata_readable wpi_assert_lock_parity wpi_assert_netns_binding \
  wpi_assert_listener_set wpi_record_external_probe_boundary; do eval "$f(){ :; }"; done
( wpi_main ) > "$W/main.log" 2>&1
rc=$?
BOUND=$(tr '\n' ',' < "$W/bound")
printf 'MAIN_BIND rc=%s bound=[%s] python3_bound=%s malicious_marker=%s accepted_status=%s rp7_pass=%s window_open=%s window_closed=%s binding_stop=%s\n' \
  "$rc" "$BOUND" "$(case ",$BOUND" in *,python3,*) echo yes;; *) echo no;; esac)" \
  "$([ -e "$W/marker" ] && echo present || echo absent)" \
  "$(grep -c '^B5_status .*parser=pinned_system_interpreter' "$W/main.log")" \
  "$(grep -c '^RP7 PASS$' "$W/main.log")" \
  "$(grep -c '^MOUNT_WINDOW_OPEN$' "$W/main.log")" \
  "$(grep -c '^MOUNT_WINDOW_CLOSED$' "$W/main.log")" \
  "$(grep -c '^BINDING_WOULD_STOP_python3$' "$W/main.log")"
ARM

bash --noprofile --norc "$Q/f1_arm.sh" "$RED"   "$Q/f1-red"   > "$Q/f1-red.txt" 2>&1;   f1red=$?
bash --noprofile --norc "$Q/f1_arm.sh" "$GREEN" "$Q/f1-green" > "$Q/f1-green.txt" 2>&1; f1green=$?
cat "$Q/f1-red.txt" "$Q/f1-green.txt"
printf 'F1_ARM_RCS red=%s green=%s\n' "$f1red" "$f1green"
expect_has f1_red_false_pass  'MAIN_BIND rc=0 bound=\[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,\] python3_bound=no malicious_marker=present accepted_status=1 rp7_pass=1 window_open=1 window_closed=1 binding_stop=0' "$Q/f1-red.txt"
expect_has f1_green_stop      'MAIN_BIND rc=3 bound=\[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,python3,\] python3_bound=yes malicious_marker=absent accepted_status=0 rp7_pass=0 window_open=1 window_closed=0 binding_stop=1' "$Q/f1-green.txt"
expect_hasnt f1_green_no_pass '^RP7 PASS$' "$Q/f1-green/main.log"

# ===========================================================================
# FINDING 2 (HIGH) - an admitted *.dist-info object whose package identity cannot
# be established is silently dropped (or dishonestly named) by the verifier.
# Each arm runs the production row-19 preflight AND the production trusted driver
# over the REAL digest-bound verify_lock.py. Only the MSYS-to-native argv plumbing
# and numeric ownership are substituted, exactly as disclosed for round 4.
# ===========================================================================
cat > "$Q/f2_arm.sh" <<'ARM'
S="$1"; W="$2"; CASE="$3"; REPO_VERIFIER="$4"; PYEXE="$5"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10
WPI_FIND=/usr/bin/find; WPI_SHA256SUM=/usr/bin/sha256sum; WPI_PYTHON3="$PYEXE"
WPI_VENV_ROOT="$W/venv"; WPI_RELEASE_ROOT="$W/release"; WPI_EXPECTED_PACKAGES=1
WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
WPI_VENV_WALK_COMPLETE=yes; WPI_INTERPRETER_RAN=yes; WPI_PROBE_SEQ=0
WPI_MOUNT_SNAPSHOT_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
SITE="$WPI_VENV_ROOT/lib/python3.12/site-packages"
VERDIR="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux"
mkdir -p "$SITE/a-demo-1.0.dist-info" "$VERDIR"
tr -d '\r' < "$REPO_VERIFIER" > "$VERDIR/verify_lock.py"
cat > "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" <<'EOF'
demo-pkg==1.0 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000000
EOF
printf 'Metadata-Version: 2.1\nName: demo-pkg\nVersion: 1.0\n' > "$SITE/a-demo-1.0.dist-info/METADATA"
printf '\n' > "$SITE/a-demo-1.0.dist-info/RECORD"
SUBJECT=none
case "$CASE" in
  name_absent)
    SUBJECT=z-ghost-9.0.dist-info; mkdir -p "$SITE/$SUBJECT"
    printf 'Metadata-Version: 2.1\nVersion: 9.0\n' > "$SITE/$SUBJECT/METADATA" ;;
  version_absent)
    SUBJECT=z-noversion-1.0.dist-info; mkdir -p "$SITE/$SUBJECT"
    printf 'Metadata-Version: 2.1\nName: ghost-pkg\n' > "$SITE/$SUBJECT/METADATA" ;;
  duplicate)
    SUBJECT=b-demo-1.0.dist-info; mkdir -p "$SITE/$SUBJECT"
    printf 'Metadata-Version: 2.1\nName: Demo_Pkg\nVersion: 1.0\n' > "$SITE/$SUBJECT/METADATA" ;;
esac
[ "$SUBJECT" = none ] || printf '\n' > "$SITE/$SUBJECT/RECORD"
eval "$(declare -f wpi_capture | sed '1s/^wpi_capture/prod_capture/')"
CALL=0
forge_capture(){
  # ROUND-9 CHANGE: production hands a child an already-open descriptor for an
  # object it must not address by name, so this stub supplies the same one -
  # exactly as round 8 added the stderr capture descriptor to these stubs. The
  # fixtures, the interpreter, the flags and every expected outcome below are
  # unchanged; a stub that set only names would no longer be standing in for
  # `wpi_capture`.
  local cfd="$WPI_CAP_CHILD_FD" cslot="$WPI_CAP_CHILD_SLOT" sfd=""
  WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""
  local label="$1"; shift; local -a a=("$@"); local i exe
  CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/forge.$CALL.out"; WPI_CAP_ERR="$EV_DIR/forge.$CALL.err"
  WPI_CAP_RC=0; : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"
  exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
  for ((i=1; i<${#a[@]}; i++)); do
    case "${a[$i]}" in /*) [ ! -e "${a[$i]}" ] || a[$i]="$(cygpath -w "${a[$i]}")";; esac
  done
  if [ "$cslot" = in ]; then exec {sfd}<&0; exec <&"$cfd"; fi
  /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
  if [ -n "$sfd" ]; then exec <&"$sfd"; exec {sfd}<&-; sfd=""; fi
  tr -d '\r' < "$EV_DIR/raw.out" > "$WPI_CAP_OUT"; tr -d '\r' < "$EV_DIR/raw.err" > "$WPI_CAP_ERR"
}
wpi_capture(){ if [ "$1" = lock_parity ]; then forge_capture "$@"; else prod_capture "$@"; fi; }
wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ :; }
wpi_lstat(){
  local p="$2"; wpi_render_path "$p"
  if [ ! -e "$p" ]; then WPI_META_KIND=absent; WPI_META_MODE=; WPI_META_OWNER=; WPI_META_ID=; WPI_META_SIZE=
  elif [ -d "$p" ]; then WPI_META_KIND=directory; WPI_META_MODE=755; WPI_META_OWNER=0:0; WPI_META_ID=1:1; WPI_META_SIZE=0
  else WPI_META_KIND='regular file'; WPI_META_MODE=644; WPI_META_OWNER=0:0; WPI_META_ID=1:2; WPI_META_SIZE=$(wc -c < "$p"); fi
}
wpi_assert_metadata_readable > "$W/preflight.log" 2>&1; preflight_rc=$?
wpi_assert_regular_digest(){ :; }
# Subshell: the production predicate really exits the process on FAIL/STOP, so an
# arm that called it directly could not survive to report its own result.
( wpi_assert_lock_parity ) > "$W/parity.log" 2>&1; parity_rc=$?
SUBJ_SHA=none
[ "$SUBJECT" = none ] || SUBJ_SHA=$(printf '%s' "$SUBJECT" | sha256sum | cut -d' ' -f1)
printf 'META_IDENTITY case=%s rc_preflight=%s rc_parity=%s dist_info_dirs=%s accepted_parity=%s parity_fail=%s identity_stop=%s subject_name_sha256=%s\n' \
  "$CASE" "$preflight_rc" "$parity_rc" \
  "$(find "$SITE" -maxdepth 1 -type d -name '*.dist-info' | wc -l)" \
  "$(grep -c '^B1_lock_parity result=pass packages=1 ' "$W/parity.log")" \
  "$(grep -c '^B1_FAIL reason=lock_installed_parity' "$W/parity.log")" \
  "$(grep -c '^B1_STOP reason=metadata_identity_unestablished stage=verifier ' "$W/parity.log")" \
  "$SUBJ_SHA"
grep '^B1_STOP reason=metadata_identity_unestablished' "$W/parity.log" || true
ARM

for c in clean name_absent version_absent duplicate; do
  bash --noprofile --norc "$Q/f2_arm.sh" "$RED"   "$Q/f2-red-$c"   "$c" "$REPO_VERIFIER" "$PYEXE" > "$Q/f2-red-$c.txt" 2>&1
  bash --noprofile --norc "$Q/f2_arm.sh" "$GREEN" "$Q/f2-green-$c" "$c" "$REPO_VERIFIER" "$PYEXE" > "$Q/f2-green-$c.txt" 2>&1
  sed 's/^/RED   /'   "$Q/f2-red-$c.txt"
  sed 's/^/GREEN /' "$Q/f2-green-$c.txt"
done
GHOST_SHA=$(printf '%s' 'z-ghost-9.0.dist-info' | sha256sum | cut -d' ' -f1)
NOVER_SHA=$(printf '%s' 'z-noversion-1.0.dist-info' | sha256sum | cut -d' ' -f1)
DUP_SHA=$(printf '%s' 'b-demo-1.0.dist-info' | sha256sum | cut -d' ' -f1)
expect_has f2_red_clean_pass        'META_IDENTITY case=clean rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0' "$Q/f2-red-clean.txt"
expect_has f2_green_clean_pass      'META_IDENTITY case=clean rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0' "$Q/f2-green-clean.txt"
expect_has f2_red_name_false_pass   'META_IDENTITY case=name_absent rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0' "$Q/f2-red-name_absent.txt"
expect_has f2_green_name_stop       'META_IDENTITY case=name_absent rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1' "$Q/f2-green-name_absent.txt"
expect_has f2_green_name_line       "^B1_STOP reason=metadata_identity_unestablished stage=verifier detail=name_absent name_sha256=$GHOST_SHA$" "$Q/f2-green-name_absent.txt"
expect_has f2_red_dup_false_pass    'META_IDENTITY case=duplicate rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0' "$Q/f2-red-duplicate.txt"
expect_has f2_green_dup_stop        'META_IDENTITY case=duplicate rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1' "$Q/f2-green-duplicate.txt"
expect_has f2_green_dup_line        "^B1_STOP reason=metadata_identity_unestablished stage=verifier detail=canonical_name_duplicate name_sha256=$DUP_SHA$" "$Q/f2-green-duplicate.txt"
expect_has f2_red_version_bad_fail  'META_IDENTITY case=version_absent rc_preflight=0 rc_parity=1 dist_info_dirs=2 accepted_parity=0 parity_fail=1 identity_stop=0' "$Q/f2-red-version_absent.txt"
expect_has f2_green_version_stop    'META_IDENTITY case=version_absent rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1' "$Q/f2-green-version_absent.txt"
expect_has f2_green_version_line    "^B1_STOP reason=metadata_identity_unestablished stage=verifier detail=version_absent name_sha256=$NOVER_SHA$" "$Q/f2-green-version_absent.txt"

# ===========================================================================
# FINDING 4 (LOW) - the three /dev/null write opens.
# (a) static: no non-comment /dev/null occurrence survives in GREEN.
# (b) executed: the prerequisite check is no longer satisfiable by an EXECUTABLE
#     of the predicate name on PATH - only by a real shell function.
# (c) executed: the leaf allocator keeps create-once semantics and still leaks no
#     diagnostic, with stderr CLOSED instead of redirected to /dev/null.
#     ROUND-9 CHANGE, name only: round 9 deleted `wpi_alloc_leaf`, the name-only
#     allocator whose one remaining caller was the status body that the round-8
#     audit turned into an outside-tree write. `wpi_open_leaf` is now the only
#     allocator, it runs the SAME `noclobber` test with fd 2 CLOSED, and it STOPs
#     with the same two reason tokens. The three inputs and the three expected
#     dispositions below are unchanged, so the arm still rejects any block that
#     re-creates an existing leaf, writes outside EV_DIR, or leaks a diagnostic.
# ===========================================================================
RED_DEVNULL=$(grep -v '^[[:space:]]*#' "$RED" | grep -c '/dev/null')
GREEN_DEVNULL=$(grep -v '^[[:space:]]*#' "$GREEN" | grep -c '/dev/null')
printf 'DEVNULL_STATIC red_non_comment=%s green_non_comment=%s\n' "$RED_DEVNULL" "$GREEN_DEVNULL"
expect_rc red_devnull "$RED_DEVNULL" 3
expect_rc green_devnull "$GREEN_DEVNULL" 0

cat > "$Q/f4_path_arm.sh" <<'ARM'
S="$1"; W="$2"
mkdir -p "$W/bin" "$W/ev"
printf '#!/usr/bin/env bash\nexit 0\n' > "$W/bin/rp0_require_safe_component"
printf '#!/usr/bin/env bash\nexit 0\n' > "$W/bin/rp0_allocate_evidence_dir"
chmod +x "$W/bin/rp0_require_safe_component" "$W/bin/rp0_allocate_evidence_dir"
PATH="$W/bin:$PATH"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
RUNID=r5probe; EV_STAGE_ID=ro; EV_DIR="$W/ev"; EV_LOG="$W/ev/ro.log"
WPI_FIXED_EVIDENCE_ROOT="$W"
( wpi_assert_prerequisites ) > "$W/prereq.out" 2> "$W/prereq.err"; rc=$?
printf 'PREREQ_PATH_SHADOW rc=%s stdout=[%s] stderr_bytes=%s\n' "$rc" "$(cat "$W/prereq.out")" "$(wc -c < "$W/prereq.err")"
ARM
bash --noprofile --norc "$Q/f4_path_arm.sh" "$RED"   "$Q/f4-red"   > "$Q/f4-red.txt" 2>&1
bash --noprofile --norc "$Q/f4_path_arm.sh" "$GREEN" "$Q/f4-green" > "$Q/f4-green.txt" 2>&1
cat "$Q/f4-red.txt" "$Q/f4-green.txt"
expect_has f4_red_path_accepted 'PREREQ_PATH_SHADOW rc=0 stdout=\[\] stderr_bytes=0' "$Q/f4-red.txt"
expect_has f4_green_path_refused 'PREREQ_PATH_SHADOW rc=3 stdout=\[RP7_STOP reason=rp0_lib_not_sourced predicate=rp0_require_safe_component\] stderr_bytes=0' "$Q/f4-green.txt"

cat > "$Q/f4_leaf_arm.sh" <<'ARM'
S="$1"; W="$2"
mkdir -p "$W/ev"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"
( wpi_open_leaf "$EV_DIR/leaf" ) > "$W/a1.out" 2> "$W/a1.err"; rc1=$?
( wpi_open_leaf "$EV_DIR/leaf" ) > "$W/a2.out" 2> "$W/a2.err"; rc2=$?
( wpi_open_leaf "$W/outside" )   > "$W/a3.out" 2> "$W/a3.err"; rc3=$?
printf 'ALLOC_LEAF rc_first=%s rc_second=%s rc_outside=%s err1=%s err2=%s err3=%s second_stdout=[%s] outside_stdout=[%s]\n' \
  "$rc1" "$rc2" "$rc3" "$(wc -c < "$W/a1.err")" "$(wc -c < "$W/a2.err")" "$(wc -c < "$W/a3.err")" \
  "$(cat "$W/a2.out")" "$(cat "$W/a3.out")"
ARM
bash --noprofile --norc "$Q/f4_leaf_arm.sh" "$GREEN" "$Q/f4-leaf" > "$Q/f4-leaf.txt" 2>&1
cat "$Q/f4-leaf.txt"
expect_has f4_leaf_create_once 'ALLOC_LEAF rc_first=0 rc_second=3 rc_outside=3 err1=0 err2=0 err3=0' "$Q/f4-leaf.txt"
expect_has f4_leaf_stop_text 'second_stdout=\[RP7_STOP reason=capture_leaf_not_create_once leaf=' "$Q/f4-leaf.txt"
expect_has f4_leaf_outside_text 'outside_stdout=\[RP7_STOP reason=capture_path_outside_evidence leaf=' "$Q/f4-leaf.txt"

# ===========================================================================
# FINDING 5 (MEDIUM) - evidence-root provenance is never proved.
# The arm drives the real wpi_assert_prerequisites. rp0_require_safe_component and
# rp0_allocate_evidence_dir are real shell FUNCTIONS here (RP0-LIB is not present
# on this workstation), which is the only substitution.
# ===========================================================================
cat > "$Q/f5_arm.sh" <<'ARM'
S="$1"; W="$2"; PIN="$3"; EVD="$4"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
rp0_require_safe_component(){ :; }
rp0_allocate_evidence_dir(){ :; }
RUNID=r5probe; EV_STAGE_ID=ro; EV_DIR="$EVD"; EV_LOG="$EVD/ro.log"
[ "$PIN" = keep ] || WPI_FIXED_EVIDENCE_ROOT="$PIN"
( wpi_assert_prerequisites ) > "$W/out" 2> "$W/err"; rc=$?
printf 'EV_ROOT pin=[%s] ev_dir=[%s] rc=%s stderr_bytes=%s stdout=[%s]\n' \
  "$PIN" "$EVD" "$rc" "$(wc -c < "$W/err")" "$(cat "$W/out")"
ARM
mkdir -p "$Q/base/evidence/runkit/RUN-RO" "$Q/base-evil/x" "$Q/other/x"
HAS_CONST_RED=$(grep -c '^WPI_FIXED_EVIDENCE_ROOT=' "$RED")
HAS_CONST_GREEN=$(grep -c '^WPI_FIXED_EVIDENCE_ROOT=' "$GREEN")
printf 'EV_ROOT_CONSTANT red=%s green=%s\n' "$HAS_CONST_RED" "$HAS_CONST_GREEN"
expect_rc ev_root_const_red "$HAS_CONST_RED" 0
expect_rc ev_root_const_green "$HAS_CONST_GREEN" 1
bash --noprofile --norc "$Q/f5_arm.sh" "$RED"   "$Q/f5-red"      keep         "$Q/other/x"                       > "$Q/f5-red.txt" 2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN" "$Q/f5-unfilled" keep         "$Q/other/x"                       > "$Q/f5-unfilled.txt" 2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN" "$Q/f5-inside"   "$Q/base"    "$Q/base/evidence/runkit/RUN-RO"   > "$Q/f5-inside.txt" 2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN" "$Q/f5-outside"  "$Q/base"    "$Q/other/x"                       > "$Q/f5-outside.txt" 2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN" "$Q/f5-lookalike" "$Q/base"   "$Q/base-evil/x"                   > "$Q/f5-lookalike.txt" 2>&1
cat "$Q/f5-red.txt" "$Q/f5-unfilled.txt" "$Q/f5-inside.txt" "$Q/f5-outside.txt" "$Q/f5-lookalike.txt"
expect_has f5_red_unbound     " rc=0 stderr_bytes=0 stdout=\[\]$" "$Q/f5-red.txt"
expect_has f5_green_unfilled  ' rc=3 stderr_bytes=0 stdout=\[RP7_STOP reason=evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT\]$' "$Q/f5-unfilled.txt"
expect_has f5_green_inside    " rc=0 stderr_bytes=0 stdout=\[\]$" "$Q/f5-inside.txt"
expect_has f5_green_outside   " rc=3 stderr_bytes=0 stdout=\[RP7_STOP reason=evidence_root_unattested ev_dir=$Q/other/x expected_root=$Q/base\]$" "$Q/f5-outside.txt"
expect_has f5_green_lookalike " rc=3 stderr_bytes=0 stdout=\[RP7_STOP reason=evidence_root_unattested ev_dir=$Q/base-evil/x expected_root=$Q/base\]$" "$Q/f5-lookalike.txt"

case "$Q" in /tmp/rp7-r5-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_SCRATCH_UNSAFE=%s\n' "$Q"; exit 97 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_QA_FENCE_END
```

### Round-5 transcript

```text
QA_ROOT=/tmp/rp7-r5-qa.RUMPX4
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=70941 red_sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad red_cr=0 red_bash_n=0 green_bytes=108301 green_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62 green_cr=0 green_bash_n=0
MAIN_BIND rc=0 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,] python3_bound=no malicious_marker=present accepted_status=1 rp7_pass=1 window_open=1 window_closed=1 binding_stop=0
MAIN_BIND rc=3 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,python3,] python3_bound=yes malicious_marker=absent accepted_status=0 rp7_pass=0 window_open=1 window_closed=0 binding_stop=1
F1_ARM_RCS red=0 green=0
RED   META_IDENTITY case=clean rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0 subject_name_sha256=none
GREEN META_IDENTITY case=clean rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0 subject_name_sha256=none
RED   META_IDENTITY case=name_absent rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0 subject_name_sha256=15bf31c7b03eb9c11445f7328f389f86f3cd1e0cdfc928adcfbf021f6566a1d6
GREEN META_IDENTITY case=name_absent rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1 subject_name_sha256=15bf31c7b03eb9c11445f7328f389f86f3cd1e0cdfc928adcfbf021f6566a1d6
GREEN B1_STOP reason=metadata_identity_unestablished stage=verifier detail=name_absent name_sha256=15bf31c7b03eb9c11445f7328f389f86f3cd1e0cdfc928adcfbf021f6566a1d6
RED   META_IDENTITY case=version_absent rc_preflight=0 rc_parity=1 dist_info_dirs=2 accepted_parity=0 parity_fail=1 identity_stop=0 subject_name_sha256=e399457a916a7494816a42e7374d8b8065b91f0e85695cf2810a2a56c684d764
GREEN META_IDENTITY case=version_absent rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1 subject_name_sha256=e399457a916a7494816a42e7374d8b8065b91f0e85695cf2810a2a56c684d764
GREEN B1_STOP reason=metadata_identity_unestablished stage=verifier detail=version_absent name_sha256=e399457a916a7494816a42e7374d8b8065b91f0e85695cf2810a2a56c684d764
RED   META_IDENTITY case=duplicate rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0 subject_name_sha256=13f2bc04e1b33fad9e8b0fab8b135e214120329fd63b87d6226a2c2b44455750
GREEN META_IDENTITY case=duplicate rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1 subject_name_sha256=13f2bc04e1b33fad9e8b0fab8b135e214120329fd63b87d6226a2c2b44455750
GREEN B1_STOP reason=metadata_identity_unestablished stage=verifier detail=canonical_name_duplicate name_sha256=13f2bc04e1b33fad9e8b0fab8b135e214120329fd63b87d6226a2c2b44455750
DEVNULL_STATIC red_non_comment=3 green_non_comment=0
PREREQ_PATH_SHADOW rc=0 stdout=[] stderr_bytes=0
PREREQ_PATH_SHADOW rc=3 stdout=[RP7_STOP reason=rp0_lib_not_sourced predicate=rp0_require_safe_component] stderr_bytes=0
ALLOC_LEAF rc_first=0 rc_second=3 rc_outside=3 err1=0 err2=0 err3=0 second_stdout=[RP7_STOP reason=capture_leaf_not_create_once leaf=/tmp/rp7-r5-qa.RUMPX4/f4-leaf/ev/leaf] outside_stdout=[RP7_STOP reason=capture_path_outside_evidence leaf=/tmp/rp7-r5-qa.RUMPX4/f4-leaf/outside ev_dir=/tmp/rp7-r5-qa.RUMPX4/f4-leaf/ev]
EV_ROOT_CONSTANT red=0 green=1
EV_ROOT pin=[keep] ev_dir=[/tmp/rp7-r5-qa.RUMPX4/other/x] rc=0 stderr_bytes=0 stdout=[]
EV_ROOT pin=[keep] ev_dir=[/tmp/rp7-r5-qa.RUMPX4/other/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT]
EV_ROOT pin=[/tmp/rp7-r5-qa.RUMPX4/base] ev_dir=[/tmp/rp7-r5-qa.RUMPX4/base/evidence/runkit/RUN-RO] rc=0 stderr_bytes=0 stdout=[]
EV_ROOT pin=[/tmp/rp7-r5-qa.RUMPX4/base] ev_dir=[/tmp/rp7-r5-qa.RUMPX4/other/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=/tmp/rp7-r5-qa.RUMPX4/other/x expected_root=/tmp/rp7-r5-qa.RUMPX4/base]
EV_ROOT pin=[/tmp/rp7-r5-qa.RUMPX4/base] ev_dir=[/tmp/rp7-r5-qa.RUMPX4/base-evil/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=/tmp/rp7-r5-qa.RUMPX4/base-evil/x expected_root=/tmp/rp7-r5-qa.RUMPX4/base]
QA_PASS all_assertions=yes
```

Reading the load-bearing lines:

- `BYTE_IDENTITY` proves the RED subject is the audited round-4 blob and the GREEN subject
  is the repaired file, both LF-only and both `bash -n` clean.
- `MAIN_BIND rc=0 ... python3_bound=no malicious_marker=present accepted_status=1
  rp7_pass=1 window_open=1 window_closed=1 binding_stop=0` is Codex's finding 1 reproduced
  on the audited bytes: the deviant executable ran, wrote a marker, forged `OK fields=8`
  over an `ARMED` body, and the block still reached `RP7 PASS`.
- `MAIN_BIND rc=3 ... python3_bound=yes malicious_marker=absent accepted_status=0
  rp7_pass=0 window_open=1 window_closed=0 binding_stop=1` is the repair: the real
  `wpi_main` loop asks for the tenth binding, the arm STOPs there, nothing was executed,
  and the mount window was still open - which is the ordering the kickoff required.
- The three `B1_STOP reason=metadata_identity_unestablished stage=verifier detail=<tok>
  name_sha256=<h>` lines are the finding-2 repair. Each `name_sha256` equals the SHA-256 of
  the offending directory's own name, which the arm re-derives independently and asserts.
- `META_IDENTITY case=version_absent ... rc_parity=1 parity_fail=1` on the round-4 bytes is
  the second half of finding 2 and a pattern-1 defect in its own right: an object whose
  version cannot be established was reported as a package-parity host finding. The repaired
  bytes STOP instead.
- `PREREQ_PATH_SHADOW rc=0` versus `rc=3 stdout=[RP7_STOP reason=rp0_lib_not_sourced ...]`
  shows the finding-4 replacement is not only redirection-free but strictly narrower than
  the `command -v` it replaces.
- Every `stderr_bytes=0` / `err1=0 err2=0 err3=0` field is the evidence that closing fd 2
  discards the `noclobber` diagnostic without opening anything.

## The carried round-4 fence, re-run as a regression gate

The round-4 fence is reproduced below **unchanged except for the two anchor comments and
the capture stubs that feed a B5 or B6 assertion**, and was re-executed against the round-9
bytes. Round 7 gave four of those stubs one statement each, `exec
{WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"`, because the listener reader had moved onto the capture
descriptor. Round 8 extends the same adaptation to the stderr descriptor and to the stubs
that feed the status and namespace rows, for the same reason and with the same consequence:
production binds both streams of a capture, a stub that sets only the NAMES is no longer
standing in for `wpi_capture`, and the block STOPs with `detail=capture_stream_unbound`
rather than reading a name it was not given.

No fixture byte, no arm and no assertion changed. That is the discriminating-power argument
for every one of these stub edits, and the transcript below is where it is checked: each
stub feeds the same bytes to the same production reader and the same result line comes back,
so what these edits changed is how the fixture hands bytes over, not which observations the
row accepts. It is the no-weakening gate for this round: every round-3 and round-4 arm - the
two real `python -m venv` forging environments, the projection-v2 attacks, the two-phase
listener parse, the row grammar, the `-S` guard, the tool-attestation disclosure, the
timeout-inside-cleared-environment ordering - must still reach `QA_PASS` on the round-8
bytes, and does.

```bash
# RP7_R4_FENCE_BEGIN
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
REPO_VERIFIER=/c/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py
Q=$(mktemp -d /tmp/rp7-r4-qa.XXXXXX)
PYEXE=/c/Python314/python.exe
CR=$'\r'
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E
set +e
set +u
set +o pipefail

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_ne(){ [ "$2" != "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected_not=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
common(){
    EV_DIR="$1"; mkdir -p "$EV_DIR"
    WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=5
    WPI_STAT=/usr/bin/stat; WPI_READLINK=/usr/bin/readlink
    WPI_FIND=/usr/bin/find; WPI_SHA256SUM=/usr/bin/sha256sum
    WPI_SYSTEMCTL=/usr/bin/systemctl; WPI_SS=/usr/bin/ss; WPI_CURL=/usr/bin/curl
    WPI_PYTHON3=/usr/bin/python3
    WPI_MOUNT_GUARD_ACTIVE=no; WPI_PROBE_SEQ=0; WPI_MOUNT_SNAPSHOT_SEQ=0
}
proj_globals(){
    common "$1"
    WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b
    WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b
    WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service
    WPI_STATE_DIR=/var/lib/mtc-bridge; WPI_LOG_DIR=/var/log/mtc-bridge
    WPI_CONF_DIR=/etc/mtc-bridge; WPI_MAINPID=189813
}
printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_stat=%s python=%s uid_gid=%s:%s live_mountinfo_records=%s symlinks=%s\n' \
    "$BASH_VERSION" "$(/usr/bin/stat --version | head -1 | sed 's/.* //')" "$("$PYEXE" -V | sed 's/.* //')" \
    "$(id -u)" "$(id -g)" "$(wc -l < /proc/self/mountinfo)" "not_representable_msys2"

# ---------------------------------------------------------------------------
# The round-3 bodies, carried VERBATIM (only the function names differ) as the
# RED arms for findings 1, 2, 3 and 5. Written by a quoted heredoc, so every
# character between the delimiters is literal.
#
# ROUND-9 ADDITION, and it is a repair to this fence rather than a change to an
# arm: round 9 DELETED `wpi_alloc_leaf` from the block, and three of the frozen
# round-3 bodies below call it. Left alone they would have run with that call
# failing as `command not found` - the allocation silently skipped, seven raw
# shell diagnostics escaping to stderr, and the RED arms no longer exercising the
# round-3 behaviour they are the record of. The round-3 definition is therefore
# supplied here, verbatim, as part of the frozen RED. It is a fixture for the old
# bodies only; the block under test has no such function and the round-5 fence
# asserts the create-once property against `wpi_open_leaf` instead.
cat > "$Q/r3-mutants.sh" <<'R3MUTANTS_EOF'
wpi_alloc_leaf() {
    local leaf="$1"
    case "$leaf" in "$EV_DIR"/*) : ;; *) wpi_stop RP7 "capture_path_outside_evidence leaf=$leaf ev_dir=$EV_DIR" ;; esac
    if ! ( set -o noclobber; : > "$leaf" ) 2>&-; then
        wpi_stop RP7 "capture_leaf_not_create_once leaf=$leaf"
    fi
}
mutant_assert_metadata_readable_r3() {
    local site="$WPI_VENV_ROOT/lib/python3.12/site-packages" out fd path="" rc=0 count=0 member diag
    [ "$WPI_VENV_WALK_COMPLETE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=venv_walk_not_complete"
    [ "$WPI_INTERPRETER_RAN" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=interpreter_not_run"
    wpi_mount_guard_begin
    wpi_walk_components B1 "$site" directory "" 0:0
    wpi_run_find B1 metadata_enumeration "$site" -mindepth 1 -maxdepth 1 -name '*.dist-info' -print0
    out="$WPI_CAP_OUT"
    wpi_alloc_read_diag metadata_paths; diag="$WPI_READ_DIAG"
    exec {fd}<"$out" || wpi_stop B1 "metadata_unreadable path=$site detail=enumeration_open_failed"
    while true; do
        path=""; rc=0; IFS= read -r -d '' -u "$fd" path 2>>"$diag" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-
            wpi_require_empty_file B1 "metadata_unreadable path=$site detail=enumeration_read_error" "$diag"
            [ -z "$path" ] || wpi_stop B1 "metadata_unreadable path=$site detail=unterminated_nul_record"
            break
        fi
        count=$(( count + 1 ))
        wpi_require_observed_path_grammar B1 "$path" metadata_enumeration
        wpi_lstat B1 "$path"
        [ "$WPI_META_KIND" != absent ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD detail=object_disappeared_after_complete_enumeration"
        [ "$WPI_META_KIND" = directory ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD detail=dist_info_kind_$WPI_META_KIND"
        [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD owner_numeric=$WPI_META_OWNER expected=0:0"
        wpi_walk_components B1 "$path" directory "" 0:0
        for member in METADATA RECORD; do
            wpi_lstat B1 "$path/$member"
            [ "$WPI_META_KIND" != absent ] || wpi_fail B1 "distribution_metadata_absent $WPI_PATH_FIELD"
            case "$WPI_META_KIND" in 'regular file'|'regular empty file') : ;; *) wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD detail=kind_$WPI_META_KIND" ;; esac
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD owner_numeric=$WPI_META_OWNER expected=0:0"
            wpi_sha_file B1 metadata_unreadable "$path/$member"
            WPI_MEMBER_DIGEST="$WPI_LINE"
            wpi_render_path "$path/$member"
            printf 'B1_metadata_readable %s bytes_digest=sha256:%s content=not_printed binding=window_open_pending_close\n' "$WPI_PATH_FIELD" "$WPI_MEMBER_DIGEST"
        done
    done
    wpi_mount_guard_end
    [ "$count" -ge 1 ] || wpi_stop B1 "metadata_unreadable path=$site detail=no_dist_info_directories"
    WPI_METADATA_READABLE=yes
    printf 'B1_metadata_preflight root=%s dist_info_dirs=%s complete=yes readable=yes\n' "$site" "$count"
}
mutant_assert_lock_parity_r3() {
    local verifier="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
    local lock="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" out err
    [ "$WPI_METADATA_READABLE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=metadata_preflight_not_complete"
    wpi_assert_regular_digest B1 verifier_absent verifier_digest_mismatch "$verifier" 3735 "$WPI_VERIFY_LOCK_SHA256" verifier verifier_object_unexpected
    wpi_capture lock_parity "$WPI_VENV_ROOT/bin/python" -I "$verifier" --lock "$lock" --check-installed
    if [ "$WPI_CAP_RC" -eq 0 ]; then
        wpi_require_empty_file B1 "verifier_not_evaluable rc=0" "$WPI_CAP_ERR"
        wpi_single_record B1 "verifier_not_evaluable rc=0" "$WPI_CAP_OUT"
        [ "$WPI_LINE" = "verify_lock: PASS: lock+installed; packages=$WPI_EXPECTED_PACKAGES" ] \
            || wpi_stop B1 "verifier_not_evaluable rc=0 detail=pass_grammar"
        printf 'B1_lock_parity result=pass packages=%s output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec\n' "$WPI_EXPECTED_PACKAGES"
        return 0
    fi
    wpi_require_empty_file B1 "verifier_not_evaluable rc=$WPI_CAP_RC detail=unexpected_stdout" "$WPI_CAP_OUT"
    wpi_single_record B1 "verifier_not_evaluable rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
    err="$WPI_LINE"
    if [ "$WPI_CAP_RC" -eq 1 ] && wpi_is_structured_parity_mismatch "$err"; then
        wpi_fail B1 "lock_installed_parity observed=positively_distinguished_named_set_mismatch"
    fi
    wpi_stop B1 "verifier_not_evaluable rc=$WPI_CAP_RC detail=unclassified_verifier_result diagnostic_file=$WPI_CAP_ERR"
}
mutant_assert_listener_set_r3() {
    local fd line="" rc=0 count=0 total=0 state recvq sendq localaddr peer extra addr port peer_addr peer_port diag
    wpi_capture listeners "$WPI_SS" -H -ltn
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=$WPI_CAP_RC detail=ss_failed"
    wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0" "$WPI_CAP_ERR"
    wpi_alloc_read_diag listener_rows; diag="$WPI_READ_DIAG"
    exec {fd}<"$WPI_CAP_OUT" || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=open_failed"
    while true; do
        line=""; rc=0; IFS= read -r -u "$fd" line 2>>"$diag" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-
            wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=hard_read_error" "$diag"
            [ -z "$line" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=unterminated_final_record"
            break
        fi
        [ -n "$line" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=blank_record"
        state=""; recvq=""; sendq=""; localaddr=""; peer=""; extra=""
        read -r state recvq sendq localaddr peer extra <<< "$line"
        [ -n "$state" ] && [ -n "$recvq" ] && [ -n "$sendq" ] && [ -n "$localaddr" ] && [ -n "$peer" ] && [ -z "$extra" ] \
            || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar"
        [ "$state" = LISTEN ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=state_grammar"
        case "$recvq:$sendq" in *[!0-9:]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar" ;; esac
        case "$localaddr:$peer" in *[![:graph:]]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=address_character_grammar" ;; esac
        case "$localaddr" in *:*) port="${localaddr##*:}"; addr="${localaddr%:*}" ;; *) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar" ;; esac
        case "$peer" in *:*) peer_port="${peer##*:}"; peer_addr="${peer%:*}" ;; *) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=peer_address_grammar" ;; esac
        case "$port" in ''|*[!0-9]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=local_port_grammar" ;; esac
        case "$peer_port" in '*'|[0-9]|[0-9][0-9]|[0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9][0-9]) : ;; *) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=peer_port_grammar" ;; esac
        [ -n "$addr" ] && [ -n "$peer_addr" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=empty_address"
        total=$(( total + 1 ))
        [ "$port" = 8790 ] || continue
        case "$addr" in '*'|0.0.0.0|'[::]'|'::'|"172.24.55.233") wpi_fail B6 "nonloopback_listener addr=$addr" ;; esac
        [ "$addr" = 127.0.0.1 ] || wpi_fail B6 "listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790"
        count=$(( count + 1 ))
    done
    [ "$count" -eq 1 ] || wpi_fail B6 "listener_set_unexpected observed_count=$count expected=1x127.0.0.1:8790"
    printf 'B6_listener_inventory rows=%s evidence_file=%s content=not_printed table=complete scope_applied_in_block=yes\n' "$total" "$WPI_CAP_OUT"
    printf 'B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\n'
}
mutant_assert_status_r3() {
    local body="$EV_DIR/ro.status.body" code_file json_out json_err
    wpi_alloc_leaf "$body"
    wpi_capture status_get "$WPI_CURL" --silent --show-error --connect-timeout 5 --max-time 10 \
        --request GET --output "$body" --write-out '%{http_code}\n' -- "$WPI_CONTROL_ENDPOINT"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B5 "status_endpoint_not_evaluable rc=$WPI_CAP_RC detail=transport_error diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_OUT"
    case "$WPI_LINE" in 401|403) wpi_stop B5 "status_endpoint_access_denied code=$WPI_LINE" ;; 200) : ;; [0-9][0-9][0-9]) wpi_fail B5 "status_endpoint_unexpected_http code=$WPI_LINE" ;; *) wpi_stop B5 "status_endpoint_not_evaluable rc=0 detail=http_code_grammar" ;; esac
    wpi_sha_file B5 status_body_unreadable_or_unparseable "$body"; WPI_BODY_SHA="$WPI_LINE"
    wpi_capture status_json "$WPI_VENV_ROOT/bin/python" -I -c '
import hashlib,json,sys
class Dup(Exception): pass
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d: raise Dup(k)
  d[k]=v
 return d
def bad_constant(x): raise ValueError("non_json_constant")
try:
 with open(sys.argv[1],"rb") as f: raw=f.read()
 obj=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=bad_constant)
 if type(obj) is not dict: print("PARSE top_level"); sys.exit(3)
 expected={"state":(str,"DISARMED"),"state_version":(int,1),"mode":(str,"credential_free_disarmed"),"network":(str,"disabled"),"exchange_conn":(str,"disabled"),"exchange_enabled":(bool,False),"credential_lookup":(str,"disabled"),"arm_enabled":(bool,False)}
 for k,(t,v) in expected.items():
  if k not in obj: print("MISSING "+k); sys.exit(4)
  if type(obj[k]) is not t: print("TYPE %s %s %s"%(k,type(obj[k]).__name__,t.__name__)); sys.exit(5)
  if obj[k] != v:
   h=hashlib.sha256(json.dumps(obj[k],sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
   print("MISMATCH %s %s"%(k,h)); sys.exit(1)
 print("OK fields=8")
except (OSError,UnicodeError,json.JSONDecodeError,Dup,ValueError) as e:
 print("PARSE "+type(e).__name__); sys.exit(3)
' "$body"
    wpi_require_empty_file B5 "status_body_unreadable_or_unparseable detail=parser_stderr" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_body_unreadable_or_unparseable" "$WPI_CAP_OUT"
    case "$WPI_CAP_RC:$WPI_LINE" in
        '0:OK fields=8') printf 'B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=%s content=not_printed\n' "$WPI_BODY_SHA" ;;
        4:'MISSING '*) wpi_stop B5 "schema_unexpected field=${WPI_LINE#MISSING }" ;;
        5:'TYPE '*)
            read -r _ WPI_JSON_FIELD WPI_JSON_TYPE WPI_JSON_EXPECTED_TYPE <<< "$WPI_LINE"
            case "$WPI_JSON_FIELD:$WPI_JSON_TYPE:$WPI_JSON_EXPECTED_TYPE" in *[!A-Za-z0-9_:.-]*) wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_grammar" ;; esac
            wpi_fail B5 "flag_mismatch field=$WPI_JSON_FIELD observed_type=$WPI_JSON_TYPE expected_type=$WPI_JSON_EXPECTED_TYPE" ;;
        1:'MISMATCH '*)
            read -r _ WPI_JSON_FIELD WPI_JSON_DIGEST <<< "$WPI_LINE"
            case "$WPI_JSON_FIELD:$WPI_JSON_DIGEST" in *[!A-Za-z0-9_:.-]*) wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_grammar" ;; esac
            wpi_fail B5 "flag_mismatch field=$WPI_JSON_FIELD observed_sha256=$WPI_JSON_DIGEST expected=preregistered_typed_value" ;;
        *) wpi_stop B5 "status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=$WPI_CAP_RC body_sha256=$WPI_BODY_SHA" ;;
    esac
}
R3MUTANTS_EOF
. "$Q/r3-mutants.sh"

# ---------------------------------------------------------------------------
# Fixture 1 - metadata shim. Renders the REAL metadata of the REAL object as
# reported by the real GNU coreutils stat, substituting only what MSYS2 cannot
# express: numeric ownership (this filesystem has no root) and, where a fixture
# demands it, the object kind. Mode, dev:inode, size, ENOENT classification,
# exit status and stream discipline are the unmodified real results.
# ---------------------------------------------------------------------------
make_stat_shim(){
    local w="$1"; shift
    cat > "$w" <<'SHIM_EOF'
#!/bin/sh
target=""
for a in "$@"; do target=$a; done
e="${TMPDIR:-/tmp}/.stat_shim.$$"
out=$(/usr/bin/stat "$@" 2>"$e"); rc=$?
if [ "$rc" -ne 0 ]; then
    msg=$(cat "$e"); rm -f "$e"
    case "$msg" in
        *"No such file or directory"*)
            printf "%s: cannot stat '%s': No such file or directory\n" "$0" "$target" >&2 ;;
        *) printf '%s\n' "$msg" >&2 ;;
    esac
    exit "$rc"
fi
rm -f "$e"
kind=${out%%|*}; rest=${out#*|}
mode=${rest%%|*}; rest=${rest#*|}
rest=${rest#*|}
ident=${rest%%|*}; size=${rest#*|}
owner=0:0
SHIM_EOF
    while [ "$#" -ge 3 ]; do
        printf 'if [ "$target" = %s ]; then %s=%s; fi\n' "'$1'" "$2" "'$3'" >> "$w"
        shift 3
    done
    printf '%s\n' 'printf "%s|%s|%s|%s|%s\n" "$kind" "$mode" "$owner" "$ident" "$size"' >> "$w"
    chmod 755 "$w"
}
make_stat_shim "$Q/stat-shim"

# A stat that really fails, for one named path, with a diagnostic the block does
# not classify as absence. Every other path is answered by the shim above.
make_stat_eacces(){
    local w="$1" t="$2"
    { printf '%s\n' '#!/bin/sh'
      printf '%s\n' 'target=""'
      printf '%s\n' 'for a in "$@"; do target=$a; done'
      printf 'if [ "$target" = %s ]; then printf "%%s: cannot stat '"'"'%%s'"'"': Permission denied\\n" "$0" "$target" >&2; exit 1; fi\n' "'$t'"
      printf 'exec %s "$@"\n' "'$Q/stat-shim'"
    } > "$w"
    chmod 755 "$w"
}

# ---------------------------------------------------------------------------
# F2(a) + F4 - ENOENT diagnostic acceptance. The primary GREEN arm uses the
# REAL GNU coreutils stat on a REAL absent object: that is the exact absolute
# argv[0] form the Debian 12 target produces and the form the round-2 uutils
# fence could never emit. The wrapper matrix then falsifies every other form,
# including the three basename spellings round 3 removed.
# ---------------------------------------------------------------------------
ABSENT="$Q/absent-leaf"
printf 'REAL_GNU_DIAGNOSTIC=[%s]\n' "$(/usr/bin/stat -c '%F' -- "$ABSENT" 2>&1 >/dev/null)"
( common "$Q/ev-diag-real"; wpi_lstat B3 "$ABSENT"; printf 'REAL_GNU_ABSENT kind=%s child_rc=%s\n' "$WPI_META_KIND" "$WPI_CAP_RC"; [ "$WPI_META_KIND" = absent ] || exit 95 ); realabsent=$?

make_stat_diag(){
    local w="$1" msg="$2"
    { printf '%s\n' '#!/bin/sh'
      printf "cat >&2 <<'DIAG_EOF'\n"
      printf '%s\n' "$msg"
      printf '%s\n' 'DIAG_EOF' 'exit 1'
    } > "$w"
    chmod 755 "$w"
}
diag_case(){
    local id="$1" w="$Q/stat-diag-$1" base="stat-diag-$1" msg
    case "$id" in
        abs_statx)  msg="$w: cannot statx '$ABSENT': No such file or directory" ;;
        abs_stat)   msg="$w: cannot stat '$ABSENT': No such file or directory" ;;
        abs_oserr)  msg="$w: cannot stat '$ABSENT': No such file or directory (os error 2)" ;;
        base_statx) msg="$base: cannot statx '$ABSENT': No such file or directory" ;;
        base_stat)  msg="$base: cannot stat '$ABSENT': No such file or directory" ;;
        base_oserr) msg="$base: cannot stat '$ABSENT': No such file or directory (os error 2)" ;;
        foreign)    msg="$w: cannot stat '$ABSENT': Permission denied" ;;
    esac
    make_stat_diag "$w" "$msg"
    ( common "$Q/ev-diag-$id"; WPI_STAT="$w"; wpi_lstat B3 "$ABSENT"; printf 'DIAG_ACCEPTED id=%s kind=%s\n' "$id" "$WPI_META_KIND" )
}
diag_case abs_statx; d1=$?
diag_case abs_stat; d2=$?
diag_case abs_oserr; d3=$?
diag_case base_statx; d4=$?
diag_case base_stat; d5=$?
diag_case base_oserr; d6=$?
diag_case foreign; d7=$?
printf 'STAT_DIAGNOSTIC_RCS real_gnu_absent=%s abs_statx=%s abs_stat=%s abs_oserr=%s base_statx=%s base_stat=%s base_oserr=%s foreign=%s\n' \
    "$realabsent" "$d1" "$d2" "$d3" "$d4" "$d5" "$d6" "$d7"
expect_rc diag_real "$realabsent" 0
expect_rc diag_abs_statx "$d1" 0; expect_rc diag_abs_stat "$d2" 0; expect_rc diag_abs_oserr "$d3" 0
expect_rc diag_base_statx "$d4" 3; expect_rc diag_base_stat "$d5" 3; expect_rc diag_base_oserr "$d6" 3
expect_rc diag_foreign "$d7" 3

# ---------------------------------------------------------------------------
# F1 - normalised_path_projection_v2 versus the round-2 v1 body, verbatim.
# N1 (bind/overlay inside a trusted subtree) and N2 (mount stacked on an
# existing mount point) are the auditor's two falsifications; both must now
# flip, and the v1 body must still be blind to both.
# ---------------------------------------------------------------------------
mutant_build_mount_projection_v1(){
    local snapshot="$1" projection path mp best=-1 best_len=-1 i len
    local -a paths=(
        "$WPI_STAT" "$WPI_READLINK" "$WPI_ENV" "$WPI_FIND" "$WPI_SHA256SUM"
        "$WPI_SYSTEMCTL" "$WPI_SS" "$WPI_CURL" "$WPI_TIMEOUT"
        "$WPI_RELEASE_ROOT" "$WPI_VENV_ROOT" "$WPI_UNIT_FRAGMENT"
        "$WPI_STATE_DIR" "$WPI_LOG_DIR" "$WPI_CONF_DIR"
        /proc/self/mountinfo /proc/self/ns/net "/proc/$WPI_MAINPID/ns/net"
    )
    wpi_parse_mountinfo "$snapshot"
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    projection="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").mount_projection_v1.tsv"
    wpi_alloc_leaf "$projection"
    for path in "${paths[@]}"; do
        best=-1; best_len=-1
        for ((i=0; i<${#WPI_MI_POINT[@]}; i++)); do
            mp="${WPI_MI_POINT[$i]}"
            if [ "$mp" = / ] || [ "$path" = "$mp" ] || [[ "$path" == "$mp/"* ]]; then
                len=${#mp}
                if [ "$len" -gt "$best_len" ]; then best="$i"; best_len="$len"; fi
            fi
        done
        [ "$best" -ge 0 ] || wpi_stop RP7 "mount_projection_unbound path=$path"
        printf 'path=%s\tdevice=%s\troot=%s\tmount_point=%s\tfstype=%s\tsource=%s\n' \
            "$path" "${WPI_MI_DEVICE[$best]}" "${WPI_MI_ROOT[$best]}" \
            "${WPI_MI_POINT[$best]}" "${WPI_MI_FSTYPE[$best]}" "${WPI_MI_SOURCE[$best]}" \
            >>"$projection" || wpi_stop RP7 "mount_projection_write_failed path=$projection"
    done
    wpi_sha_file RP7 mount_projection_unreadable "$projection"
    WPI_MOUNT_PROJECTION_DIGEST_V1="$WPI_LINE"
}
v2_digest(){ ( proj_globals "$Q/ev-$2" >/dev/null; wpi_build_mount_projection "$1" >/dev/null; printf '%s' "$WPI_MOUNT_PROJECTION_DIGEST" ); }
v1_digest(){ ( proj_globals "$Q/ev-$2" >/dev/null; mutant_build_mount_projection_v1 "$1" >/dev/null; printf '%s' "$WPI_MOUNT_PROJECTION_DIGEST_V1" ); }

proj_globals "$Q/ev-snapshot"
wpi_capture_mountinfo_snapshot; REAL_SNAP="$WPI_LINE"
cp "$REAL_SNAP" "$Q/n1-clean"
cp "$REAL_SNAP" "$Q/n1-decoy"
printf '%s\n' "900 0 0:99 / $WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE rw - tmpfs decoy_bind rw" >> "$Q/n1-decoy"
cp "$REAL_SNAP" "$Q/n1-venv-decoy"
printf '%s\n' "901 0 0:98 / $WPI_VENV_ROOT/lib/python3.12/site-packages rw - tmpfs decoy_overlay rw" >> "$Q/n1-venv-decoy"
n1_clean_v2=$(v2_digest "$Q/n1-clean" n1a)
n1_decoy_v2=$(v2_digest "$Q/n1-decoy" n1b)
n1_venv_v2=$(v2_digest "$Q/n1-venv-decoy" n1c)
n1_repeat_v2=$(v2_digest "$Q/n1-clean" n1d)
n1_clean_v1=$(v1_digest "$Q/n1-clean" n1e)
n1_decoy_v1=$(v1_digest "$Q/n1-decoy" n1f)
n1_venv_v1=$(v1_digest "$Q/n1-venv-decoy" n1g)
printf 'N1_REAL_MOUNTINFO records=%s captured_by=wpi_capture_mountinfo_snapshot\n' "$(wc -l < "$REAL_SNAP")"
printf 'N1_V2 clean=%s decoy_bind_under_release=%s decoy_overlay_under_venv=%s repeat_clean=%s\n' \
    "$n1_clean_v2" "$n1_decoy_v2" "$n1_venv_v2" "$n1_repeat_v2"
printf 'N1_V1_ROUND2 clean=%s decoy_bind_under_release=%s decoy_overlay_under_venv=%s\n' \
    "$n1_clean_v1" "$n1_decoy_v1" "$n1_venv_v1"
expect_ne n1_v2_bind_detected "$n1_decoy_v2" "$n1_clean_v2"
expect_ne n1_v2_overlay_detected "$n1_venv_v2" "$n1_clean_v2"
expect_eq n1_v2_deterministic "$n1_repeat_v2" "$n1_clean_v2"
expect_eq n1_v1_bind_blind "$n1_decoy_v1" "$n1_clean_v1"
expect_eq n1_v1_overlay_blind "$n1_venv_v1" "$n1_clean_v1"

printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw' > "$Q/n2-clean"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '37 36 0:99 / / rw - tmpfs /dev/decoy rw'; } > "$Q/n2-stacked"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '38 36 0:32 / /usr/bin rw - ext4 /dev/root rw'
  printf '%s\n' '39 36 0:97 / /usr/bin rw - tmpfs /dev/decoytools rw'; } > "$Q/n2-tool-stacked"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '38 36 0:32 / /usr/bin rw - ext4 /dev/root rw'; } > "$Q/n2-tool-clean"
n2_clean_v2=$(v2_digest "$Q/n2-clean" n2a)
n2_stacked_v2=$(v2_digest "$Q/n2-stacked" n2b)
n2_tool_clean_v2=$(v2_digest "$Q/n2-tool-clean" n2c)
n2_tool_stacked_v2=$(v2_digest "$Q/n2-tool-stacked" n2d)
n2_clean_v1=$(v1_digest "$Q/n2-clean" n2e)
n2_stacked_v1=$(v1_digest "$Q/n2-stacked" n2f)
n2_tool_clean_v1=$(v1_digest "$Q/n2-tool-clean" n2g)
n2_tool_stacked_v1=$(v1_digest "$Q/n2-tool-stacked" n2h)
printf 'N2_V2 clean_root=%s stacked_on_root=%s clean_usr_bin=%s stacked_on_usr_bin=%s\n' \
    "$n2_clean_v2" "$n2_stacked_v2" "$n2_tool_clean_v2" "$n2_tool_stacked_v2"
printf 'N2_V1_ROUND2 clean_root=%s stacked_on_root=%s clean_usr_bin=%s stacked_on_usr_bin=%s\n' \
    "$n2_clean_v1" "$n2_stacked_v1" "$n2_tool_clean_v1" "$n2_tool_stacked_v1"
expect_ne n2_v2_stacked_detected "$n2_stacked_v2" "$n2_clean_v2"
expect_ne n2_v2_tool_stacked_detected "$n2_tool_stacked_v2" "$n2_tool_clean_v2"
expect_eq n2_v1_stacked_blind "$n2_stacked_v1" "$n2_clean_v1"
expect_eq n2_v1_tool_stacked_blind "$n2_tool_stacked_v1" "$n2_tool_clean_v1"

v2_digest "$Q/n2-tool-stacked" shape >/dev/null
SHAPE="$Q/ev-shape/ro.0002.mount_projection.tsv"
printf 'V2_RECORD_SHAPE points=%s subtree=%s subtree_count=%s\n' \
    "$(grep -c '^kind=point' "$SHAPE")" "$(grep -c '^kind=subtree	' "$SHAPE")" "$(grep -c '^kind=subtree_count' "$SHAPE")"
printf 'V2_EFFECTIVE_MOUNT %s\n' "$(grep -m1 '^kind=point	path=/usr/bin/stat	' "$SHAPE" | tr '\t' ' ')"
printf 'V2_TRUSTED_PYTHON_POINT %s\n' "$(grep -m1 '^kind=point	path=/usr/bin/python3	' "$SHAPE" | tr '\t' ' ')"
printf 'V2_SUBTREE_USR_BIN %s\n' "$(grep '^kind=subtree_count	subtree_root=/usr/bin	' "$SHAPE" | tr '\t' ' ')"
expect_rc v2_points "$(grep -c '^kind=point' "$SHAPE")" 21
expect_rc v2_subtree_counts "$(grep -c '^kind=subtree_count' "$SHAPE")" 6
expect_rc v2_python_point "$(grep -c '^kind=point	path=/usr/bin/python3	' "$SHAPE")" 1

# ---------------------------------------------------------------------------
# F2(b) - the real pre-fix wpi_fail body versus production. MOUNT_WINDOW_CLOSED
# is emitted by a wrapper AROUND the real guard-close, not by a stub replacing
# it, so its absence proves the window really was left open.
# ---------------------------------------------------------------------------
eval "$(declare -f wpi_mount_guard_end | sed '1s/^wpi_mount_guard_end/wpi_real_mount_guard_end/')"
mark_guard_end(){ wpi_mount_guard_end(){ wpi_real_mount_guard_end; printf 'MOUNT_WINDOW_CLOSED\n'; }; }
compute_attestation(){ wpi_capture_mountinfo_snapshot >/dev/null; wpi_build_mount_projection "$WPI_LINE" >/dev/null; WPI_ATTESTED_MOUNTINFO_SHA256="$WPI_MOUNT_PROJECTION_DIGEST"; }
proj_globals "$Q/ev-guard-attest"
wpi_capture_mountinfo_snapshot >/dev/null; GSNAP="$WPI_LINE"
ATTESTED=$(v2_digest "$GSNAP" attest)
printf 'COMPUTED_ATTESTATION sha256=%s format=normalised_path_projection_v2\n' "$ATTESTED"
(
    proj_globals "$Q/ev-fail-mutant"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; mark_guard_end
    wpi_fail(){ printf '%s_FAIL reason=%s\n' "$1" "${*:2}"; exit 1; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
) > "$Q/fail-mutant.log" 2>&1; failmutant=$?
(
    proj_globals "$Q/ev-fail-green"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; mark_guard_end
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
) > "$Q/fail-green.log" 2>&1; failgreen=$?
cat "$Q/fail-mutant.log" "$Q/fail-green.log"
mutclosed=$(grep -c '^MOUNT_WINDOW_CLOSED$' "$Q/fail-mutant.log")
greenclosed=$(grep -c '^MOUNT_WINDOW_CLOSED$' "$Q/fail-green.log")
printf 'FAIL_GUARD_CLOSE mutant_rc=%s mutant_window_closed=%s production_rc=%s production_window_closed=%s\n' \
    "$failmutant" "$mutclosed" "$failgreen" "$greenclosed"
expect_rc fail_mutant_rc "$failmutant" 1; expect_rc fail_mutant_closed "$mutclosed" 0
expect_rc fail_green_rc "$failgreen" 1; expect_rc fail_green_closed "$greenclosed" 1

(
    proj_globals "$Q/ev-guard-changed"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; SNAP=0
    wpi_capture_mountinfo_snapshot(){ SNAP=$((SNAP+1)); if [ "$SNAP" -eq 1 ]; then WPI_LINE="$GSNAP"; else WPI_LINE="$Q/n1-decoy"; fi; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
); guardchanged=$?
(
    proj_globals "$Q/ev-guard-mismatch"; WPI_ATTESTED_MOUNTINFO_SHA256=$(printf '%064d' 0)
    wpi_mount_guard_begin
); guardmismatch=$?
printf 'MOUNT_GUARD_RCS changed_downgrade=%s attestation_mismatch=%s\n' "$guardchanged" "$guardmismatch"
expect_rc guard_changed "$guardchanged" 3; expect_rc guard_mismatch "$guardmismatch" 3

# ---------------------------------------------------------------------------
# F2(d) - the unsafe-pathname and interpreter arms run the REAL mount guard
# against a computed attestation. No guard stub remains anywhere in this file.
# ---------------------------------------------------------------------------
mutant_observed_path_grammar(){ case "$2" in *[[:space:]]*) wpi_stop "$1" "structured_path_unparseable source=$3 detail=unsafe_character" ;; esac; }
( mutant_observed_path_grammar B3 '/fixture/write me' find_stdout ); spacered=$?
(
    proj_globals "$Q/ev-space"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"
    wpi_walk_components(){ :; }
    wpi_run_find(){ WPI_CAP_OUT="$EV_DIR/find.out"; WPI_CAP_ERR="$EV_DIR/find.err"; WPI_CAP_ELAPSED_MS=4; : > "$WPI_CAP_ERR"; printf '/fixture/write me\0' > "$WPI_CAP_OUT"; }
    wpi_assert_tree /fixture release
); spacegreen=$?
mkdir -p "$Q/imm/sub"; : > "$Q/imm/sub/write me"
(
    proj_globals "$Q/ev-realfind"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"
    wpi_walk_components(){ :; }
    wpi_assert_tree "$Q/imm/sub" release
); realfind=$?
printf 'UNSAFE_PATH_RCS mutant_stop=%s suppressed_render_fail=%s real_find_fail=%s\n' "$spacered" "$spacegreen" "$realfind"
expect_rc space_mutant "$spacered" 3; expect_rc space_green "$spacegreen" 1; expect_rc real_find "$realfind" 1

# ---------------------------------------------------------------------------
# F3 (round 3) - attestation disclosure on all TEN tool bindings.
# ---------------------------------------------------------------------------
mkdir -p "$Q/tools"
for t in stat readlink env find sha256sum systemctl ss curl timeout python3; do
    printf '#!/bin/sh\nexit 0\n' > "$Q/tools/$t"; chmod 755 "$Q/tools/$t"
done
mutant_bind_tool_no_attestation(){
    local name="$1" path="$2"
    wpi_require_absolute "WPI_TOOL_PINS.$name" "$path"
    [ -x "$path" ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=not_executable"
    wpi_walk_components RP7 "$path" regular "" 0:0 path_absent path_metadata_mismatch stop "tool_not_evaluable tool=$name"
    printf 'MUTANT_RP7_tool name=%s path=%s owner_numeric=0:0 mode=%s kind=regular resolution=pinned_absolute\n' "$name" "$path" "$WPI_META_MODE"
}
( common "$Q/ev-bind-mutant"; WPI_STAT="$Q/stat-shim"; mutant_bind_tool_no_attestation stat "$Q/tools/stat" ) > "$Q/bind-mutant.log" 2>&1; bindmutant=$?
(
    common "$Q/ev-bind"; WPI_STAT="$Q/stat-shim"
    for t in stat readlink env find sha256sum systemctl ss curl timeout python3; do
        wpi_bind_tool "$t" "$Q/tools/$t"
    done
) > "$Q/bind.log" 2>&1; bindrc=$?
cat "$Q/bind-mutant.log" "$Q/bind.log"
mutattest=$(grep -c 'attestation=' "$Q/bind-mutant.log")
selfcount=$(grep -c 'attestation=self$' "$Q/bind.log")
boundcount=$(grep -c 'attestation=bound_instrument$' "$Q/bind.log")
selfnames=$(grep 'attestation=self$' "$Q/bind.log" | sed 's/^RP7_tool name=\([a-z0-9]*\) .*/\1/' | tr '\n' ',')
printf 'TOOL_ATTESTATION mutant_rc=%s mutant_attestation_fields=%s production_rc=%s self=%s bound_instrument=%s self_names=%s\n' \
    "$bindmutant" "$mutattest" "$bindrc" "$selfcount" "$boundcount" "$selfnames"
expect_rc bind_mutant_rc "$bindmutant" 0; expect_rc bind_mutant_attest "$mutattest" 0
expect_rc bind_rc "$bindrc" 0; expect_rc bind_self "$selfcount" 4; expect_rc bind_bound "$boundcount" 6
expect_eq bind_self_names "$selfnames" "stat,env,sha256sum,timeout,"

# The trusted interpreter is bound with the same non-symlink discipline as the
# other nine, so /usr/bin/python3 - a symlink on the target family - cannot be
# the pinned leaf. That is why the pin is a freeze-gate input.
make_stat_shim "$Q/stat-pysym" "$Q/tools/python3" kind 'symbolic link'
( common "$Q/ev-bind-pysym"; WPI_STAT="$Q/stat-pysym"; wpi_bind_tool python3 "$Q/tools/python3" ) > "$Q/bind-pysym.log" 2>&1; bindpysym=$?
grep -h '_STOP' "$Q/bind-pysym.log"
printf 'TRUSTED_PYTHON_PIN symlinked_pin_rc=%s symlink_rejected=%s\n' \
    "$bindpysym" "$(grep -c 'tool_not_evaluable tool=python3 detail=path_metadata_mismatch .* kind=symlink ' "$Q/bind-pysym.log")"
expect_rc pin_symlink_rc "$bindpysym" 3
expect_rc pin_symlink_rejected "$(grep -c 'tool_not_evaluable tool=python3 detail=path_metadata_mismatch .* kind=symlink ' "$Q/bind-pysym.log")" 1

# ---------------------------------------------------------------------------
# F5 (round 3) - multi-word %F values are routed through wpi_kind_token.
# ---------------------------------------------------------------------------
( common "$Q/ev-devnull"; wpi_lstat B1 /dev/null; wpi_kind_token "$WPI_META_KIND"; printf 'REAL_CHARDEV raw=[%s] token=[%s]\n' "$WPI_META_KIND" "$WPI_LINE"; [ "$WPI_LINE" = other ] || exit 96 ); devnull=$?
make_stat_shim "$Q/stat-rootchar" / kind 'character special file'
mkdir -p "$Q/venv/bin"
printf '#!/bin/sh\nprintf "Python 3.12.9\\n"\n' > "$Q/venv/bin/python"; chmod 755 "$Q/venv/bin/python"
make_stat_shim "$Q/stat-pychar" "$Q/venv/bin/python" kind 'character special file'
printf 'MUTANT_B3_STOP reason=path_not_evaluable path=/ detail=root_kind_%s\n' 'character special file'
printf 'MUTANT_B1_STOP reason=interpreter_object_unbound kind=%s target=none\n' 'character special file'
( common "$Q/ev-rootchar"; WPI_STAT="$Q/stat-rootchar"; wpi_walk_components B3 "$Q/imm" directory '' 0:0 ) > "$Q/rootchar.log" 2>&1; rootchar=$?
(
    proj_globals "$Q/ev-pychar"
    WPI_STAT="$Q/stat-pychar"; WPI_VENV_ROOT="$Q/venv"; compute_attestation
    wpi_assert_interpreter
) > "$Q/pychar.log" 2>&1; pychar=$?
grep '_STOP' "$Q/rootchar.log" "$Q/pychar.log" | sed 's/^[^:]*://'
printf 'KIND_TOKEN_RCS real_chardev=%s root_kind_stop=%s interpreter_kind_stop=%s root_token_ok=%s interpreter_token_ok=%s\n' \
    "$devnull" "$rootchar" "$pychar" \
    "$(grep -c 'detail=root_kind_other$' "$Q/rootchar.log")" \
    "$(grep -c 'kind=other target=none$' "$Q/pychar.log")"
expect_rc kind_devnull "$devnull" 0; expect_rc kind_root "$rootchar" 3; expect_rc kind_py "$pychar" 3
expect_rc kind_root_token "$(grep -c 'detail=root_kind_other$' "$Q/rootchar.log")" 1
expect_rc kind_py_token "$(grep -c 'kind=other target=none$' "$Q/pychar.log")" 1

# ---------------------------------------------------------------------------
# F6 (round 3) - the bounding wrapper runs INSIDE the cleared environment, and
# still bounds. RED is the round-2 ordering, verbatim.
# ---------------------------------------------------------------------------
export WPI_QA_ENV_MARKER=present
mutant_capture_timeout_outside_env(){
    local label="$1"; shift
    local start end rc=0
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_CAP_OUT="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stdout"
    WPI_CAP_ERR="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stderr"
    wpi_alloc_leaf "$WPI_CAP_OUT"; wpi_alloc_leaf "$WPI_CAP_ERR"
    wpi_clock_ms; start="$WPI_LINE"
    (
        cd "$EV_DIR" || exit 125
        exec "$WPI_TIMEOUT" --signal=TERM --kill-after=5s "${WPI_SWEEP_BUDGET_S}s" \
            "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@"
    ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"
    WPI_CAP_RC="$rc"; WPI_CAP_ELAPSED_MS=$(( end - start ))
}
make_timeout_probe(){
    local w="$1" out="$2"
    { printf '%s\n' '#!/bin/sh'; printf "/usr/bin/env > '%s'\n" "$out"; printf '%s\n' 'exec /usr/bin/timeout "$@"'; } > "$w"
    chmod 755 "$w"
}
make_timeout_probe "$Q/timeout-probe-red" "$Q/timeout-env-red.txt"
make_timeout_probe "$Q/timeout-probe-green" "$Q/timeout-env-green.txt"
( common "$Q/ev-env-red"; WPI_TIMEOUT="$Q/timeout-probe-red"; mutant_capture_timeout_outside_env envprobe /usr/bin/true ) >/dev/null 2>&1
( common "$Q/ev-env-green"; WPI_TIMEOUT="$Q/timeout-probe-green"; wpi_capture envprobe /usr/bin/true ) >/dev/null 2>&1
redmarker=$(grep -c '^WPI_QA_ENV_MARKER=present$' "$Q/timeout-env-red.txt")
greenmarker=$(grep -c '^WPI_QA_ENV_MARKER=present$' "$Q/timeout-env-green.txt")
printf 'TIMEOUT_ENV mutant_marker=%s mutant_vars=%s production_marker=%s production_vars=%s\n' \
    "$redmarker" "$(wc -l < "$Q/timeout-env-red.txt")" "$greenmarker" "$(wc -l < "$Q/timeout-env-green.txt")"
expect_rc timeout_env_red "$redmarker" 1; expect_rc timeout_env_green "$greenmarker" 0

printf '#!/bin/sh\n/usr/bin/sleep 8\n' > "$Q/slow-find"; chmod 755 "$Q/slow-find"
mutant_capture_unbounded(){
    local label="$1"; shift; local start end rc=0
    WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1)); WPI_CAP_OUT="$EV_DIR/mutant.stdout"; WPI_CAP_ERR="$EV_DIR/mutant.stderr"
    : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; wpi_clock_ms; start="$WPI_LINE"
    ( cd "$EV_DIR"; exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@" ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"; WPI_CAP_RC=$rc; WPI_CAP_ELAPSED_MS=$((end-start))
}
mutant_run_find(){ mutant_capture_unbounded slow "$WPI_FIND" /fixture -perm /222 -print0; wpi_stop B3 "sweep_budget_exceeded root=/fixture elapsed_s=$((WPI_CAP_ELAPSED_MS/1000)) elapsed_ms=$WPI_CAP_ELAPSED_MS budget_s=2"; }
start=$SECONDS; ( common "$Q/ev-time-red"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=2; mutant_run_find ); timered=$?; redwall=$((SECONDS-start))
start=$SECONDS; ( common "$Q/ev-time-green"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=2; wpi_run_find B3 slow /fixture -perm /222 -print0 ); timegreen=$?; greenwall=$((SECONDS-start))
printf 'TIMEOUT_RCS mutant=%s production=%s mutant_wall_s=%s production_wall_s=%s budget_s=2 child_sleep_s=8\n' "$timered" "$timegreen" "$redwall" "$greenwall"
expect_rc timeout_mutant "$timered" 3; expect_rc timeout_green "$timegreen" 3
[ "$redwall" -ge 8 ] && [ "$greenwall" -le 4 ] || { printf 'QA_ASSERT_FAIL name=timeout_wall red=%s green=%s\n' "$redwall" "$greenwall"; exit 92; }

# ---------------------------------------------------------------------------
# Interpreter arms with the REAL guard and the computed attestation.
# ---------------------------------------------------------------------------
mkdir -p "$Q/venvlink/bin"; printf '#!/bin/sh\nexit 0\n' > "$Q/venvlink/bin/python"; chmod 755 "$Q/venvlink/bin/python"
make_stat_shim "$Q/stat-pylink" "$Q/venvlink/bin/python" kind 'symbolic link'
make_readlink_shim(){ local w="$1" t="$2"; printf '#!/bin/sh\n' > "$w"; printf "printf '%s\\\\n'\n" "$t" >> "$w"; chmod 755 "$w"; }
make_readlink_shim "$Q/readlink-plain" '/decoy/target'
make_readlink_shim "$Q/readlink-cr" '/decoy\rB1_interpreter path=spoofed exec=ok'
(
    proj_globals "$Q/ev-py-good"
    WPI_STAT="$Q/stat-shim"; WPI_VENV_ROOT="$Q/venv"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-good.log" 2>&1; pygood=$?
(
    proj_globals "$Q/ev-py-link"
    WPI_STAT="$Q/stat-pylink"; WPI_READLINK="$Q/readlink-plain"; WPI_VENV_ROOT="$Q/venvlink"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-link.log" 2>&1; pylink=$?
(
    proj_globals "$Q/ev-py-cr"
    WPI_STAT="$Q/stat-pylink"; WPI_READLINK="$Q/readlink-cr"; WPI_VENV_ROOT="$Q/venvlink"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-cr.log" 2>&1; pycr=$?
grep -h -E '^(B1_interpreter|B1_STOP)' "$Q/py-good.log" "$Q/py-link.log" "$Q/py-cr.log"
crforged=$(grep -c '^B1_interpreter' "$Q/py-cr.log")
crstop=$(grep -c '^B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok$' "$Q/py-cr.log")
printf 'INTERPRETER_RCS regular_pass=%s symlink_stop=%s cr_stop=%s cr_forged_lines=%s cr_single_sanitised_line=%s\n' \
    "$pygood" "$pylink" "$pycr" "$crforged" "$crstop"
expect_rc interpreter_good "$pygood" 0; expect_rc interpreter_link "$pylink" 3; expect_rc interpreter_cr "$pycr" 3
expect_rc interpreter_cr_forged "$crforged" 0; expect_rc interpreter_cr_single "$crstop" 1

# ===========================================================================
# ROUND 4 - Codex finding 1 (BLOCK). Venv site startup executes unbound code
# before both adjudicators. Two REAL venvs are built by the real `python -m
# venv`; one carries a forging *.pth, the other a forging sitecustomize.py.
# Each forge writes a marker file (mutation) and prints the exact accepted
# result line, then exits 0 before the intended child body can run.
# ===========================================================================
"$PYEXE" -m venv --without-pip "$Q/svenv" >/dev/null 2>&1; svenvrc=$?
"$PYEXE" -m venv --without-pip "$Q/pvenv" >/dev/null 2>&1; pvenvrc=$?
cp -r "$Q/svenv/Scripts" "$Q/svenv/bin"
cp -r "$Q/pvenv/Scripts" "$Q/pvenv/bin"
PTH_MARKER="$Q/pth.marker"; SC_MARKER="$Q/sitecustomize.marker"
printf 'import os,sys; open(r"%s","w").write("1"); sys.stdout.write("OK fields=8"+chr(10)); sys.stdout.flush(); os._exit(0)\n' \
    "$(cygpath -w "$PTH_MARKER")" > "$Q/svenv/Lib/site-packages/zzforge.pth"
{ printf 'import os,sys\n'
  printf 'open(r"%s","w").write("1")\n' "$(cygpath -w "$SC_MARKER")"
  printf 'sys.stdout.write("verify_lock: PASS: lock+installed; packages=2"+chr(10))\n'
  printf 'sys.stdout.flush()\n'
  printf 'os._exit(0)\n'; } > "$Q/pvenv/Lib/site-packages/sitecustomize.py"
printf 'FORGE_FIXTURES venv_rc=%s,%s pth=[%s] sitecustomize_lines=%s\n' "$svenvrc" "$pvenvrc" \
    "$(cat "$Q/svenv/Lib/site-packages/zzforge.pth")" "$(wc -l < "$Q/pvenv/Lib/site-packages/sitecustomize.py")"

# The block's own wpi_capture execs through MSYS `env -i`/`timeout`, which
# rewrites POSIX-looking argv for a native Windows child. That plumbing, and
# only that plumbing, is substituted here: the stub honours the interpreter and
# the flags the production or mutant body chose (a[0] and the flag words), runs
# the real CPython, and normalises the Windows CRLF record terminator to the LF
# a Debian CPython emits. Nothing about interpreter selection is simulated.
forge_capture(){
    # ROUND-9 CHANGE: production hands a child an already-open descriptor for an
    # object it must not address by name, so this stub supplies the same one -
    # exactly as round 8 added the stderr capture descriptor to these stubs. The
    # fixtures, the interpreter, the flags and every expected outcome below are
    # unchanged; a stub that set only names would no longer be standing in for
    # `wpi_capture`.
    local cfd="$WPI_CAP_CHILD_FD" cslot="$WPI_CAP_CHILD_SLOT" sfd=""
    WPI_CAP_CHILD_FD=""; WPI_CAP_CHILD_SLOT=""
    local label="$1"; shift; local -a a=("$@"); local i exe; CALL=$((CALL+1))
    WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; : > "$WPI_CAP_OUT"
    case "$label" in
        status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '%s\n' "$BODY_JSON" > "$EV_DIR/ro.status.body"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; return 0 ;;
        sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; return 0 ;;
    esac
    exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
    for ((i=1; i<${#a[@]}; i++)); do
        case "${a[$i]}" in /*) if [ -e "${a[$i]}" ]; then a[$i]="$(cygpath -w "${a[$i]}")"; fi ;; esac
    done
    if [ "$cslot" = in ]; then exec {sfd}<&0; exec <&"$cfd"; fi
    /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
    if [ -n "$sfd" ]; then exec <&"$sfd"; exec {sfd}<&-; sfd=""; fi
    tr -d '\r' < "$EV_DIR/raw.out" > "$WPI_CAP_OUT"
    tr -d '\r' < "$EV_DIR/raw.err" > "$WPI_CAP_ERR"
    exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
}

# --- 1(a) status parser. The body is DEVIANT (state=ARMED), so a truthful
# adjudication is B5_FAIL rc 1. The .pth forges the accepted OK line instead.
DEVIANT_BODY='{"state":"ARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
run_status_forge(){
    local mode="$1" d="$Q/forge-status-$1"; mkdir -p "$d"
    (
        EV_DIR="$d"; CALL=0; WPI_CURL=/usr/bin/curl; WPI_SHA256SUM=/usr/bin/sha256sum
        WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
        WPI_VENV_ROOT="$Q/svenv"; BODY_JSON="$DEVIANT_BODY"
        # `greenvenv` isolates the single variable: production bytes, but pinned to
        # the SAME interpreter the RED arm used. Only -S differs.
        if [ "$mode" = greenvenv ]; then WPI_PYTHON3="$Q/svenv/bin/python"; else WPI_PYTHON3="$PYEXE"; fi
        wpi_capture(){ forge_capture "$@"; }
        if [ "$mode" = red ]; then mutant_assert_status_r3; else wpi_assert_status; fi
    )
    return $?
}
rm -f "$PTH_MARKER"; run_status_forge red > "$Q/forge-status-red.log" 2>&1; fsred=$?
fsredmark=0; [ -f "$PTH_MARKER" ] && fsredmark=1
rm -f "$PTH_MARKER"; run_status_forge green > "$Q/forge-status-green.log" 2>&1; fsgreen=$?
fsgreenmark=0; [ -f "$PTH_MARKER" ] && fsgreenmark=1
rm -f "$PTH_MARKER"; run_status_forge greenvenv > "$Q/forge-status-greenvenv.log" 2>&1; fsgv=$?
fsgvmark=0; [ -f "$PTH_MARKER" ] && fsgvmark=1
cat "$Q/forge-status-red.log" "$Q/forge-status-green.log" "$Q/forge-status-greenvenv.log"
printf 'PTH_FORGE_STATUS red_rc=%s red_marker=%s red_false_pass=%s green_rc=%s green_marker=%s green_truthful_fail=%s\n' \
    "$fsred" "$fsredmark" "$(grep -c '^B5_status .* flags=expected ' "$Q/forge-status-red.log")" \
    "$fsgreen" "$fsgreenmark" "$(grep -c '^B5_FAIL reason=flag_mismatch field=state ' "$Q/forge-status-green.log")"
expect_rc pth_status_red_rc "$fsred" 0
expect_rc pth_status_red_marker "$fsredmark" 1
expect_rc pth_status_red_false_pass "$(grep -c '^B5_status .* flags=expected ' "$Q/forge-status-red.log")" 1
expect_rc pth_status_green_rc "$fsgreen" 1
expect_rc pth_status_green_marker "$fsgreenmark" 0
expect_rc pth_status_green_truthful "$(grep -c '^B5_FAIL reason=flag_mismatch field=state ' "$Q/forge-status-green.log")" 1
printf 'PTH_FORGE_SAME_INTERPRETER green_venv_interpreter_rc=%s green_venv_marker=%s green_venv_truthful_fail=%s isolated_variable=minus_S
'     "$fsgv" "$fsgvmark" "$(grep -c '^B5_FAIL reason=flag_mismatch field=state ' "$Q/forge-status-greenvenv.log")"
expect_rc pth_status_greenvenv_rc "$fsgv" 1
expect_rc pth_status_greenvenv_marker "$fsgvmark" 0
expect_rc pth_status_greenvenv_truthful "$(grep -c '^B5_FAIL reason=flag_mismatch field=state ' "$Q/forge-status-greenvenv.log")" 1

# --- 1(b) lock parity. The venv metadata universe is DEVIANT against the lock
# (one distribution at the wrong version), so a truthful adjudication is
# B1_FAIL rc 1. sitecustomize.py forges the accepted PASS line instead.
REL="$Q/rel"; SITE="$Q/pvenv/lib/python3.12/site-packages"
mkdir -p "$REL/IBKR_PAPER_BRIDGE/deploy/linux" "$SITE/demo_pkg-1.0.dist-info" "$SITE/other-2.5.dist-info" "$SITE/plainpkg"
tr -d '\r' < "$REPO_VERIFIER" > "$REL/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
printf 'VERIFIER_IDENTITY bytes=%s sha256=%s source=candidate_worktree_lf_normalised\n' \
    "$(wc -c < "$REL/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py")" \
    "$(sha256sum "$REL/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" | cut -d' ' -f1)"
expect_eq verifier_digest "$(sha256sum "$REL/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" | cut -d' ' -f1)" d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
mk_dist(){ printf 'Metadata-Version: 2.1\nName: %s\nVersion: %s\n' "$2" "$3" > "$1/METADATA"; printf '\n' > "$1/RECORD"; }
mk_dist "$SITE/demo_pkg-1.0.dist-info" demo-pkg 1.0
mk_dist "$SITE/other-2.5.dist-info" other 2.5
cat > "$REL/IBKR_PAPER_BRIDGE/requirements.lock" <<'LOCK_EOF'
demo-pkg==1.0 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000001
other==2.5 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000002
LOCK_EOF
cat > "$Q/deviant.lock" <<'LOCK_EOF'
demo-pkg==9.9 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000001
other==2.5 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000002
LOCK_EOF
run_parity_forge(){
    local mode="$1" lock="$2" d="$Q/forge-parity-$1-$3"; mkdir -p "$d"
    (
        EV_DIR="$d"; CALL=0; WPI_METADATA_READABLE=yes
        WPI_RELEASE_ROOT="$REL"; WPI_VENV_ROOT="$Q/pvenv"; WPI_EXPECTED_PACKAGES=2
        if [ "$mode" = greenvenv ]; then WPI_PYTHON3="$Q/pvenv/bin/python"; else WPI_PYTHON3="$PYEXE"; fi
        cp -f "$lock" "$REL/IBKR_PAPER_BRIDGE/requirements.lock"
        wpi_assert_regular_digest(){ :; }
        wpi_capture(){ forge_capture "$@"; }
        if [ "$mode" = red ]; then mutant_assert_lock_parity_r3; else wpi_assert_lock_parity; fi
    )
    return $?
}
rm -f "$SC_MARKER"; run_parity_forge red "$Q/deviant.lock" dev > "$Q/forge-parity-red.log" 2>&1; fpred=$?
fpredmark=0; [ -f "$SC_MARKER" ] && fpredmark=1
rm -f "$SC_MARKER"; run_parity_forge green "$Q/deviant.lock" dev > "$Q/forge-parity-green.log" 2>&1; fpgreen=$?
fpgreenmark=0; [ -f "$SC_MARKER" ] && fpgreenmark=1
cat > "$Q/rel-good.lock" <<'LOCK_EOF'
demo-pkg==1.0 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000001
other==2.5 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000002
LOCK_EOF
rm -f "$SC_MARKER"; run_parity_forge green "$Q/rel-good.lock" ok2 > "$Q/forge-parity-ok.log" 2>&1; fpok=$?
fpokmark=0; [ -f "$SC_MARKER" ] && fpokmark=1
rm -f "$SC_MARKER"; run_parity_forge greenvenv "$Q/deviant.lock" gv > "$Q/forge-parity-greenvenv.log" 2>&1; fpgv=$?
fpgvmark=0; [ -f "$SC_MARKER" ] && fpgvmark=1
cat "$Q/forge-parity-red.log" "$Q/forge-parity-green.log" "$Q/forge-parity-greenvenv.log" "$Q/forge-parity-ok.log"
printf 'SITECUSTOMIZE_FORGE_PARITY red_rc=%s red_marker=%s red_false_pass=%s green_rc=%s green_marker=%s green_truthful_fail=%s clean_rc=%s clean_marker=%s clean_pass=%s\n' \
    "$fpred" "$fpredmark" "$(grep -c '^B1_lock_parity result=pass' "$Q/forge-parity-red.log")" \
    "$fpgreen" "$fpgreenmark" "$(grep -c '^B1_FAIL reason=lock_installed_parity ' "$Q/forge-parity-green.log")" \
    "$fpok" "$fpokmark" "$(grep -c '^B1_lock_parity result=pass packages=2 .* adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe$' "$Q/forge-parity-ok.log")"
expect_rc sc_parity_red_rc "$fpred" 0
expect_rc sc_parity_red_marker "$fpredmark" 1
expect_rc sc_parity_red_false_pass "$(grep -c '^B1_lock_parity result=pass' "$Q/forge-parity-red.log")" 1
expect_rc sc_parity_green_rc "$fpgreen" 1
expect_rc sc_parity_green_marker "$fpgreenmark" 0
expect_rc sc_parity_green_truthful "$(grep -c '^B1_FAIL reason=lock_installed_parity ' "$Q/forge-parity-green.log")" 1
expect_rc sc_parity_clean_rc "$fpok" 0
expect_rc sc_parity_clean_marker "$fpokmark" 0
printf 'SITECUSTOMIZE_FORGE_SAME_INTERPRETER green_venv_interpreter_rc=%s green_venv_marker=%s green_venv_truthful_fail=%s isolated_variable=minus_S
'     "$fpgv" "$fpgvmark" "$(grep -c '^B1_FAIL reason=lock_installed_parity ' "$Q/forge-parity-greenvenv.log")"
expect_rc sc_parity_greenvenv_rc "$fpgv" 1
expect_rc sc_parity_greenvenv_marker "$fpgvmark" 0
expect_rc sc_parity_greenvenv_truthful "$(grep -c '^B1_FAIL reason=lock_installed_parity ' "$Q/forge-parity-greenvenv.log")" 1
expect_rc sc_parity_clean_pass "$(grep -c '^B1_lock_parity result=pass packages=2 .* adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe$' "$Q/forge-parity-ok.log")" 1

# --- 1(c) both adjudicators REFUSE to proceed when site is not provably off.
# The mutants are production bytes with `-S` deleted, which is exactly the
# round-3 startup, so the guards are load-bearing rather than decorative.
eval "$(declare -f wpi_assert_lock_parity | sed '1s/^wpi_assert_lock_parity/mutant_lock_parity_no_S/; s/ -I -S -c / -I -c /')"
eval "$(declare -f wpi_assert_status | sed '1s/^wpi_assert_status/mutant_status_no_S/; s/ -I -S -c / -I -c /')"
(
    EV_DIR="$Q/nos-parity"; mkdir -p "$EV_DIR"; CALL=0; WPI_METADATA_READABLE=yes
    WPI_RELEASE_ROOT="$REL"; WPI_VENV_ROOT="$Q/pvenv"; WPI_PYTHON3="$PYEXE"; WPI_EXPECTED_PACKAGES=2
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ forge_capture "$@"; }
    mutant_lock_parity_no_S
) > "$Q/nos-parity.log" 2>&1; nosparity=$?
(
    EV_DIR="$Q/nos-status"; mkdir -p "$EV_DIR"; CALL=0; WPI_CURL=/usr/bin/curl; WPI_SHA256SUM=/usr/bin/sha256sum
    WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_VENV_ROOT="$Q/pvenv"; WPI_PYTHON3="$PYEXE"
    BODY_JSON='{"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
    wpi_capture(){ forge_capture "$@"; }
    mutant_status_no_S
) > "$Q/nos-status.log" 2>&1; nosstatus=$?
cat "$Q/nos-parity.log" "$Q/nos-status.log"
printf 'NO_SITE_GUARD parity_rc=%s parity_refused=%s status_rc=%s status_refused=%s\n' \
    "$nosparity" "$(grep -c 'verifier_not_evaluable rc=4 detail=trusted_startup_unproven$' "$Q/nos-parity.log")" \
    "$nosstatus" "$(grep -c 'detail=strict_json_or_parser_failure parser_rc=3$' "$Q/nos-status.log")"
expect_rc nos_parity_rc "$nosparity" 3
expect_rc nos_parity_refused "$(grep -c 'verifier_not_evaluable rc=4 detail=trusted_startup_unproven$' "$Q/nos-parity.log")" 1
expect_rc nos_status_rc "$nosstatus" 3
# ROUND-9 CHANGE, anchor only: this STOP no longer carries a trailing
# `body_sha256=` field, because round 9's only body digest is the one the parser
# reports for bytes it accepted and this branch is the one where it accepted
# none. The pattern is therefore anchored at end of line instead of relying on a
# trailing space, which is STRICTLY stronger: it still requires the exact detail
# token and the exact parser rc, and it now also rejects any extra field.
expect_rc nos_status_refused "$(grep -c 'detail=strict_json_or_parser_failure parser_rc=3$' "$Q/nos-status.log")" 1

# ===========================================================================
# ROUND 4 - Codex finding 2 (HIGH). Row 22 must parse the whole table before
# any semantic FAIL. The same two records in both orders; both contain one
# malformed record, so neither order is evaluable and both must reach rc 3.
# ===========================================================================
{ printf '%s\n' 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*'; printf '%s\n' 'LISTEN 0 128'; } > "$Q/ss-wildcard-first"
{ printf '%s\n' 'LISTEN 0 128'; printf '%s\n' 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*'; } > "$Q/ss-malformed-first"
{ printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*'; printf '%s\n' 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*'; } > "$Q/ss-wildcard-complete"
{ printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*'; printf '%s\n' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*'; } > "$Q/ss-good"
run_listener(){
    local mode="$1" table="$2" d="$Q/ss-$3-$1"; mkdir -p "$d"
    (
        EV_DIR="$d"; WPI_SS=/usr/bin/ss
        wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; cp "$table" "$WPI_CAP_OUT"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
        if [ "$mode" = red ]; then mutant_assert_listener_set_r3; else wpi_assert_listener_set; fi
    )
    return $?
}
run_listener red "$Q/ss-wildcard-first" wcfirst > "$Q/ss-red-wcfirst.log" 2>&1; lrw=$?
run_listener red "$Q/ss-malformed-first" mfirst > "$Q/ss-red-mfirst.log" 2>&1; lrm=$?
run_listener green "$Q/ss-wildcard-first" wcfirst > "$Q/ss-green-wcfirst.log" 2>&1; lgw=$?
run_listener green "$Q/ss-malformed-first" mfirst > "$Q/ss-green-mfirst.log" 2>&1; lgm=$?
run_listener green "$Q/ss-wildcard-complete" wccomplete > "$Q/ss-green-complete.log" 2>&1; lgc=$?
run_listener green "$Q/ss-good" good > "$Q/ss-green-good.log" 2>&1; lgg=$?
cat "$Q/ss-red-wcfirst.log" "$Q/ss-red-mfirst.log" "$Q/ss-green-wcfirst.log" "$Q/ss-green-mfirst.log" "$Q/ss-green-complete.log" "$Q/ss-green-good.log"
printf 'LISTENER_ORDER red_wildcard_first_rc=%s red_malformed_first_rc=%s green_wildcard_first_rc=%s green_malformed_first_rc=%s expected_both_stop=3\n' \
    "$lrw" "$lrm" "$lgw" "$lgm"
printf 'LISTENER_COMPLETE_TABLE wildcard_fail_rc=%s good_rc=%s inventory_before_verdict=%s\n' \
    "$lgc" "$lgg" "$(grep -c '^B6_listener_inventory rows=2 port_8790_rows=1 .* parse=complete_before_semantics ' "$Q/ss-green-complete.log")"
expect_rc listener_red_wcfirst "$lrw" 1
expect_rc listener_red_mfirst "$lrm" 3
expect_rc listener_green_wcfirst "$lgw" 3
expect_rc listener_green_mfirst "$lgm" 3
expect_rc listener_green_wildcard_fail "$lgc" 1
expect_rc listener_green_good "$lgg" 0
expect_rc listener_inventory_first "$(grep -c '^B6_listener_inventory rows=2 port_8790_rows=1 .* parse=complete_before_semantics ' "$Q/ss-green-complete.log")" 1
expect_eq listener_green_wcfirst_reason "$(head -1 "$Q/ss-green-wcfirst.log")" 'B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar'
expect_eq listener_red_wcfirst_reason "$(head -1 "$Q/ss-red-wcfirst.log")" 'B6_FAIL reason=nonloopback_listener addr=0.0.0.0'

# ===========================================================================
# ROUND 4 - Codex finding 3 (HIGH). Row 19's preflight must cover the whole
# discovery universe of its own verifier. The enumeration is now unfiltered and
# every non-preregistered metadata format or location is a STOP.
# ===========================================================================
f3_site(){ printf '%s' "$Q/f3-$1/venv/lib/python3.12/site-packages"; }
f3_build(){
    local name="$1" s; s="$(f3_site "$name")"; mkdir -p "$s/demo_pkg-1.0.dist-info" "$s/other-2.5.dist-info" "$s/plainpkg"
    mk_dist "$s/demo_pkg-1.0.dist-info" demo-pkg 1.0
    mk_dist "$s/other-2.5.dist-info" other 2.5
    printf 'x\n' > "$s/plainpkg/__init__.py"
}
f3_run(){
    local mode="$1" name="$2" tag="$3" statexe="${4:-$Q/stat-shim}"
    (
        proj_globals "$Q/f3-ev-$tag"
        WPI_STAT="$statexe"; WPI_VENV_ROOT="$Q/f3-$name/venv"
        WPI_VENV_WALK_COMPLETE=yes; WPI_INTERPRETER_RAN=yes
        compute_attestation
        if [ "$mode" = red ]; then mutant_assert_metadata_readable_r3; else wpi_assert_metadata_readable; fi
    )
    return $?
}
f3_build clean
f3_build egg; mkdir -p "$(f3_site egg)/ghost.egg-info"; printf 'Metadata-Version: 2.1\nName: ghost\nVersion: 1.0\n' > "$(f3_site egg)/ghost.egg-info/PKG-INFO"
f3_build pth; printf 'import os\n' > "$(f3_site pth)/evil.pth"
f3_build hook; printf 'x=1\n' > "$(f3_site hook)/sitecustomize.py"
f3_build zip; printf 'PK\n' > "$(f3_site zip)/wheelhouse.zip"
f3_build filedi; : > "$(f3_site filedi)/broken-1.0.dist-info"
f3_build absent; mkdir -p "$(f3_site absent)/gone-1.0.dist-info"; printf '\n' > "$(f3_site absent)/gone-1.0.dist-info/RECORD"
f3_build unread
make_stat_eacces "$Q/stat-eacces-meta" "$(f3_site unread)/demo_pkg-1.0.dist-info/METADATA"
make_stat_shim "$Q/stat-chardi" "$(f3_site clean)/other-2.5.dist-info" kind 'character special file'
make_stat_shim "$Q/stat-charmeta" "$(f3_site clean)/other-2.5.dist-info/METADATA" kind 'character special file'
f3_run green clean t01 > "$Q/f3-clean.log" 2>&1; f3clean=$?
f3_run red egg t02 > "$Q/f3-egg-red.log" 2>&1; f3eggred=$?
f3_run green egg t03 > "$Q/f3-egg-green.log" 2>&1; f3egg=$?
f3_run green pth t04 > "$Q/f3-pth.log" 2>&1; f3pth=$?
f3_run green hook t05 > "$Q/f3-hook.log" 2>&1; f3hook=$?
f3_run green zip t06 > "$Q/f3-zip.log" 2>&1; f3zip=$?
f3_run green filedi t07 > "$Q/f3-filedi.log" 2>&1; f3filedi=$?
f3_run green absent t08 > "$Q/f3-absent.log" 2>&1; f3absent=$?
f3_run green unread t09 "$Q/stat-eacces-meta" > "$Q/f3-unread.log" 2>&1; f3unread=$?
f3_run red clean t10 "$Q/stat-chardi" > "$Q/f3-chardi-red.log" 2>&1; f3chardired=$?
f3_run green clean t11 "$Q/stat-chardi" > "$Q/f3-chardi.log" 2>&1; f3chardi=$?
f3_run red clean t12 "$Q/stat-charmeta" > "$Q/f3-charmeta-red.log" 2>&1; f3charmetared=$?
f3_run green clean t13 "$Q/stat-charmeta" > "$Q/f3-charmeta.log" 2>&1; f3charmeta=$?
grep -h -E '^(B1_metadata_universe|B1_metadata_preflight|B1_STOP|B1_FAIL)' \
    "$Q/f3-clean.log" "$Q/f3-egg-red.log" "$Q/f3-egg-green.log" "$Q/f3-pth.log" "$Q/f3-hook.log" \
    "$Q/f3-zip.log" "$Q/f3-filedi.log" "$Q/f3-absent.log" "$Q/f3-unread.log" \
    "$Q/f3-chardi-red.log" "$Q/f3-chardi.log" "$Q/f3-charmeta-red.log" "$Q/f3-charmeta.log"
printf 'METADATA_UNIVERSE_RCS clean=%s egg_red=%s egg_green=%s pth=%s hook=%s zip=%s dist_info_file=%s member_absent=%s member_unreadable=%s chardev_dir_red=%s chardev_dir=%s chardev_member_red=%s chardev_member=%s\n' \
    "$f3clean" "$f3eggred" "$f3egg" "$f3pth" "$f3hook" "$f3zip" "$f3filedi" "$f3absent" "$f3unread" \
    "$f3chardired" "$f3chardi" "$f3charmetared" "$f3charmeta"
expect_rc f3_clean "$f3clean" 0
expect_rc f3_clean_universe "$(grep -c '^B1_metadata_universe .* entries=3 dist_info_dirs=2 non_metadata_entries=1 enumeration=unfiltered_maxdepth_1 universe=explicit_dist_info_only$' "$Q/f3-clean.log")" 1
expect_rc f3_egg_red_blind "$f3eggred" 0
expect_rc f3_egg_red_declared_complete "$(grep -c '^B1_metadata_preflight .* dist_info_dirs=2 complete=yes readable=yes$' "$Q/f3-egg-red.log")" 1
expect_rc f3_egg_green "$f3egg" 3
expect_rc f3_egg_green_reason "$(grep -c 'metadata_universe_unexpected stage=preflight .* format=egg_info$' "$Q/f3-egg-green.log")" 1
expect_rc f3_pth "$f3pth" 3
expect_rc f3_pth_reason "$(grep -c 'metadata_universe_unexpected stage=preflight .* format=pth$' "$Q/f3-pth.log")" 1
expect_rc f3_hook "$f3hook" 3
expect_rc f3_hook_reason "$(grep -c 'metadata_universe_unexpected stage=preflight .* format=startup_hook$' "$Q/f3-hook.log")" 1
expect_rc f3_zip "$f3zip" 3
expect_rc f3_zip_reason "$(grep -c 'metadata_universe_unexpected stage=preflight .* format=zip$' "$Q/f3-zip.log")" 1
expect_rc f3_filedi "$f3filedi" 3
expect_rc f3_filedi_reason "$(grep -c 'metadata_universe_unexpected stage=preflight .* format=dist_info_kind_regular$' "$Q/f3-filedi.log")" 1
expect_rc f3_absent "$f3absent" 1
expect_rc f3_absent_reason "$(grep -c '^B1_FAIL reason=distribution_metadata_absent ' "$Q/f3-absent.log")" 1
expect_rc f3_unread "$f3unread" 3
expect_rc f3_unread_reason "$(grep -c '^B1_STOP reason=metadata_unreadable .* detail=unclassified_diagnostic ' "$Q/f3-unread.log")" 1
expect_rc f3_chardi_red "$f3chardired" 3
expect_rc f3_chardi_red_raw "$(grep -c 'detail=dist_info_kind_character special file$' "$Q/f3-chardi-red.log")" 1
expect_rc f3_chardi "$f3chardi" 3
expect_rc f3_chardi_token "$(grep -c 'format=dist_info_kind_other$' "$Q/f3-chardi.log")" 1
expect_rc f3_charmeta_red "$f3charmetared" 3
expect_rc f3_charmeta_red_raw "$(grep -c 'detail=kind_character special file$' "$Q/f3-charmeta-red.log")" 1
expect_rc f3_charmeta "$f3charmeta" 3
expect_rc f3_charmeta_token "$(grep -c 'detail=kind_other$' "$Q/f3-charmeta.log")" 1

# The trusted driver rejects the SAME set from its own independent scan, so no
# accepting result can rest on a format only one side enumerated.
run_driver_universe(){
    local name="$1" d="$Q/drvu-$1"; mkdir -p "$d"
    (
        EV_DIR="$d"; CALL=0; WPI_METADATA_READABLE=yes
        WPI_RELEASE_ROOT="$REL"; WPI_VENV_ROOT="$Q/f3-$name/venv"; WPI_PYTHON3="$PYEXE"; WPI_EXPECTED_PACKAGES=2
        cp -f "$Q/rel-good.lock" "$REL/IBKR_PAPER_BRIDGE/requirements.lock"
        wpi_assert_regular_digest(){ :; }; wpi_capture(){ forge_capture "$@"; }
        wpi_assert_lock_parity
    )
    return $?
}
run_driver_universe egg > "$Q/drvu-egg.log" 2>&1; du1=$?
run_driver_universe hook > "$Q/drvu-hook.log" 2>&1; du2=$?
run_driver_universe clean > "$Q/drvu-clean.log" 2>&1; du3=$?
cat "$Q/drvu-egg.log" "$Q/drvu-hook.log" "$Q/drvu-clean.log"
printf 'DRIVER_UNIVERSE egg_rc=%s hook_rc=%s clean_rc=%s\n' "$du1" "$du2" "$du3"
expect_rc drv_egg "$du1" 3
expect_rc drv_egg_reason "$(grep -c 'metadata_universe_unexpected stage=verifier format=egg_info name_sha256=[0-9a-f]\{64\}$' "$Q/drvu-egg.log")" 1
expect_rc drv_hook "$du2" 3
expect_rc drv_hook_reason "$(grep -c 'metadata_universe_unexpected stage=verifier format=startup_hook name_sha256=[0-9a-f]\{64\}$' "$Q/drvu-hook.log")" 1
expect_rc drv_clean "$du3" 0

# ===========================================================================
# ROUND 4 - Codex finding 4 (MEDIUM). Only the row-22 netns PREFLIGHT inversion
# is preregistered. The GREEN order is not re-declared here: it is EXTRACTED
# from the frozen wpi_main body at run time, so this arm cannot pass if the
# block's call order is wrong.
# ===========================================================================
B5B6_ORDER=$(declare -f wpi_main | grep -o -E 'wpi_assert_(netns_binding|status|listener_set)' | tr '\n' ',')
printf 'B5B6_DECLARED_ORDER %s\n' "$B5B6_ORDER"
expect_eq b5b6_declared_order "$B5B6_ORDER" "wpi_assert_netns_binding,wpi_assert_status,wpi_assert_listener_set,"
run_two_deviation(){
    local mode="$1" d="$Q/order-$1"; mkdir -p "$d"
    (
        EV_DIR="$d"; CALL=0; WPI_READLINK=/usr/bin/readlink; WPI_SS=/usr/bin/ss; WPI_CURL=/usr/bin/curl
        WPI_MAINPID=189813; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
        wpi_capture(){
            local label="$1"; CALL=$((CALL+1))
            WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"
            case "$label" in
                caller_netns|service_netns) printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
                status_get) printf '500\n' > "$WPI_CAP_OUT" ;;
                listeners) printf '%s\n' 'LISTEN 0 128 10.0.0.5:8790 0.0.0.0:*' > "$WPI_CAP_OUT" ;;
                *) : > "$WPI_CAP_OUT" ;;
            esac
            exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
        }
        if [ "$mode" = red ]; then
            wpi_assert_netns_binding; wpi_assert_listener_set; wpi_assert_status
        else
            for f in $(declare -f wpi_main | grep -o -E 'wpi_assert_(netns_binding|status|listener_set)'); do "$f"; done
        fi
    )
    return $?
}
run_two_deviation red > "$Q/order-red.log" 2>&1; ordred=$?
run_two_deviation green > "$Q/order-green.log" 2>&1; ordgreen=$?
cat "$Q/order-red.log" "$Q/order-green.log"
printf 'TWO_DEVIATION red_rc=%s red_first_result=[%s] green_rc=%s green_first_result=[%s]\n' \
    "$ordred" "$(grep -m1 -E '_(FAIL|STOP) ' "$Q/order-red.log")" \
    "$ordgreen" "$(grep -m1 -E '_(FAIL|STOP) ' "$Q/order-green.log")"
expect_rc order_red_rc "$ordred" 1; expect_rc order_green_rc "$ordgreen" 1
expect_eq order_red_first "$(grep -m1 -E '_(FAIL|STOP) ' "$Q/order-red.log")" 'B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790'
expect_eq order_green_first "$(grep -m1 -E '_(FAIL|STOP) ' "$Q/order-green.log")" 'B5_FAIL reason=status_endpoint_unexpected_http code=500'

# ===========================================================================
# ROUND 4 - Codex finding 5 (LOW). Row-specific unreadable reasons, the row-17
# kind-only rendering, and the row-specific numeric-ownership deviation forms.
# RED is the round-3 call contract, in which the generic helper reason reached
# the evidence line.
# ===========================================================================
LOCKDIR="$Q/f5/release/IBKR_PAPER_BRIDGE"; VDIR="$LOCKDIR/deploy/linux"
mkdir -p "$VDIR"
printf 'lockbytes\n' > "$LOCKDIR/requirements.lock"
printf 'verifierbytes\n' > "$VDIR/verify_lock.py"
LOCKSIZE=$(wc -c < "$LOCKDIR/requirements.lock"); LOCKSHA=$(sha256sum "$LOCKDIR/requirements.lock" | cut -d' ' -f1)
VSIZE=$(wc -c < "$VDIR/verify_lock.py"); VSHA=$(sha256sum "$VDIR/verify_lock.py" | cut -d' ' -f1)
make_stat_eacces "$Q/stat-eacces-lock" "$LOCKDIR/requirements.lock"
make_stat_eacces "$Q/stat-eacces-verifier" "$VDIR/verify_lock.py"
make_stat_shim "$Q/stat-lockdir" "$LOCKDIR/requirements.lock" kind 'directory'
make_stat_shim "$Q/stat-lockowner" "$LOCKDIR/requirements.lock" owner '1000:1000'
make_stat_shim "$Q/stat-verifierowner" "$VDIR/verify_lock.py" owner '1000:1000'
f5_row17(){
    (
        proj_globals "$Q/f5-ev-$2"; WPI_STAT="$1"; compute_attestation
        wpi_assert_regular_digest B1a installed_lock_absent installed_lock_digest_mismatch \
            "$LOCKDIR/requirements.lock" "$LOCKSIZE" "$LOCKSHA" installed_lock installed_lock_object_unexpected kind_only
    )
    return $?
}
f5_row19a(){
    (
        proj_globals "$Q/f5-ev-$2"; WPI_STAT="$1"; compute_attestation
        wpi_assert_regular_digest B1 verifier_absent verifier_digest_mismatch \
            "$VDIR/verify_lock.py" "$VSIZE" "$VSHA" verifier verifier_object_unexpected with_path
    )
    return $?
}
# RED: the round-3 call shape, in which no caller-specific reason was threaded
# through the walk and the leaf rendering carried the path.
f5_row17_red(){
    (
        proj_globals "$Q/f5-ev-$2"; WPI_STAT="$1"; compute_attestation
        wpi_mount_guard_begin
        wpi_walk_components B1a "$LOCKDIR/requirements.lock" regular "" 0:0 installed_lock_absent installed_lock_object_unexpected
    )
    return $?
}
f5_row19a_red(){
    (
        proj_globals "$Q/f5-ev-$2"; WPI_STAT="$1"; compute_attestation
        wpi_mount_guard_begin
        wpi_walk_components B1 "$VDIR/verify_lock.py" regular "" 0:0 verifier_absent verifier_object_unexpected
    )
    return $?
}
f5_row17_red "$Q/stat-eacces-lock" r17unread_red > "$Q/f5-r17-unread-red.log" 2>&1; a1=$?
f5_row17 "$Q/stat-eacces-lock" r17unread > "$Q/f5-r17-unread.log" 2>&1; a2=$?
f5_row19a_red "$Q/stat-eacces-verifier" r19aunread_red > "$Q/f5-r19a-unread-red.log" 2>&1; a3=$?
f5_row19a "$Q/stat-eacces-verifier" r19aunread > "$Q/f5-r19a-unread.log" 2>&1; a4=$?
f5_row17_red "$Q/stat-lockdir" r17kind_red > "$Q/f5-r17-kind-red.log" 2>&1; a5=$?
f5_row17 "$Q/stat-lockdir" r17kind > "$Q/f5-r17-kind.log" 2>&1; a6=$?
f5_row17_red "$Q/stat-lockowner" r17owner_red > "$Q/f5-r17-owner-red.log" 2>&1; a7=$?
f5_row17 "$Q/stat-lockowner" r17owner > "$Q/f5-r17-owner.log" 2>&1; a8=$?
f5_row19a_red "$Q/stat-verifierowner" r19aowner_red > "$Q/f5-r19a-owner-red.log" 2>&1; a9=$?
f5_row19a "$Q/stat-verifierowner" r19aowner > "$Q/f5-r19a-owner.log" 2>&1; a10=$?
grep -h -E '_(STOP|FAIL) ' "$Q/f5-r17-unread-red.log" "$Q/f5-r17-unread.log" "$Q/f5-r19a-unread-red.log" "$Q/f5-r19a-unread.log" \
    "$Q/f5-r17-kind-red.log" "$Q/f5-r17-kind.log" "$Q/f5-r17-owner-red.log" "$Q/f5-r17-owner.log" \
    "$Q/f5-r19a-owner-red.log" "$Q/f5-r19a-owner.log"
printf 'ROW_GRAMMAR_RCS r17_unread_red=%s r17_unread=%s r19a_unread_red=%s r19a_unread=%s r17_kind_red=%s r17_kind=%s r17_owner_red=%s r17_owner=%s r19a_owner_red=%s r19a_owner=%s\n' \
    "$a1" "$a2" "$a3" "$a4" "$a5" "$a6" "$a7" "$a8" "$a9" "$a10"
expect_rc f5_r17_unread_red_generic "$(grep -c '^B1a_STOP reason=path_not_evaluable ' "$Q/f5-r17-unread-red.log")" 1
expect_rc f5_r17_unread_row "$(grep -c '^B1a_STOP reason=installed_lock_unreadable .* detail=unclassified_diagnostic ' "$Q/f5-r17-unread.log")" 1
expect_rc f5_r19a_unread_red_generic "$(grep -c '^B1_STOP reason=path_not_evaluable ' "$Q/f5-r19a-unread-red.log")" 1
expect_rc f5_r19a_unread_row "$(grep -c '^B1_STOP reason=verifier_unreadable .* detail=unclassified_diagnostic ' "$Q/f5-r19a-unread.log")" 1
expect_rc f5_r17_kind_red_path "$(grep -c '^B1a_FAIL reason=installed_lock_object_unexpected path=.* kind=directory$' "$Q/f5-r17-kind-red.log")" 1
expect_rc f5_r17_kind_exact "$(grep -c '^B1a_FAIL reason=installed_lock_object_unexpected kind=directory$' "$Q/f5-r17-kind.log")" 1
expect_rc f5_r17_owner_red_generic "$(grep -c '^B1a_FAIL reason=path_metadata_mismatch ' "$Q/f5-r17-owner-red.log")" 1
expect_rc f5_r17_owner_row "$(grep -c '^B1a_FAIL reason=installed_lock_owner_unexpected owner_numeric=1000:1000 expected=0:0$' "$Q/f5-r17-owner.log")" 1
expect_rc f5_r19a_owner_red_generic "$(grep -c '^B1_FAIL reason=path_metadata_mismatch ' "$Q/f5-r19a-owner-red.log")" 1
expect_rc f5_r19a_owner_row "$(grep -c '^B1_FAIL reason=verifier_owner_unexpected path=.* owner_numeric=1000:1000 expected=0:0$' "$Q/f5-r19a-owner.log")" 1
expect_rc f5_r17_unread_rc "$a2" 3; expect_rc f5_r19a_unread_rc "$a4" 3
expect_rc f5_r17_kind_rc "$a6" 1; expect_rc f5_r17_owner_rc "$a8" 1; expect_rc f5_r19a_owner_rc "$a10" 1

# ---------------------------------------------------------------------------
# Regression sweep carried from round 3.
# ---------------------------------------------------------------------------
printf '%s\n' '40 25 0:32 / /mnt/* rw - ext4 /dev/* rw' > "$Q/mount-glob"
mutant_split_mount_field(){ local pre='40 25 0:32 / /mnt/* rw'; set +f; set -- $pre; printf 'MUTANT_MOUNT_POINT=%s\n' "$5"; set -f; }
mutant_split_mount_field
common "$Q/ev-mount-glob"; wpi_parse_mountinfo "$Q/mount-glob"; globrc=$?
printf 'PRODUCTION_MOUNT_POINT=%s GLOB_PARSE_RC=%s\n' "${WPI_MI_POINT[0]}" "$globrc"
[ "${WPI_MI_POINT[0]}" = '/mnt/*' ] || exit 91; expect_rc glob_parse "$globrc" 0

run_json_case(){
    local name="$1" json="$2" mode="${3:-production}" d
    d="$Q/json-$name"; mkdir -p "$d"
    (
        EV_DIR="$d"; WPI_CURL=/usr/bin/curl; WPI_SHA256SUM=/usr/bin/sha256sum
        WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_VENV_ROOT=/fixture; WPI_PYTHON3="$PYEXE"
        BODY_JSON="$json"; CALL=0
        if [ "$mode" = mutant ]; then wpi_fail(){ wpi_stop B5 "mutant_wrong_type_classification $*"; }; fi
        wpi_capture(){ forge_capture "$@"; }
        wpi_assert_status
    )
    return $?
}
base='"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false'
wrong_type='{ "state":"DISARMED","state_version":"1","mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false }'
run_json_case type-red "$wrong_type" mutant; typered=$?
run_json_case good "{$base}" > "$Q/json-good.log" 2>&1; jgood=$?
run_json_case nan "{$base,\"extra\":NaN}"; jnan=$?
run_json_case infinity "{$base,\"extra\":Infinity}"; jinf=$?
run_json_case wrong-type "$wrong_type"; jtype=$?
run_json_case top-array '[]'; jtop=$?
run_json_case mismatch '{"state":"ARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'; jmis=$?
run_json_case missing '{"state":"DISARMED"}'; jmissing=$?
printf 'JSON_RCS mutant_wrong_type=%s good=%s nan=%s infinity=%s wrong_type=%s top_array=%s mismatch=%s missing=%s\n' "$typered" "$jgood" "$jnan" "$jinf" "$jtype" "$jtop" "$jmis" "$jmissing"
expect_rc type_mutant "$typered" 3; expect_rc json_good "$jgood" 0; expect_rc json_nan "$jnan" 3; expect_rc json_inf "$jinf" 3
expect_rc json_good_discloses "$(grep -c '^B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=[0-9a-f]\{64\} content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site$' "$Q/json-good.log")" 1
expect_rc json_type "$jtype" 1; expect_rc json_top "$jtop" 3; expect_rc json_mismatch "$jmis" 1; expect_rc json_missing "$jmissing" 3

(
    EV_DIR="$Q/ev-listener-red"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'MUTANT_SS_ARGV=%s\n' "$*"; WPI_CAP_RC=0; }
    wpi_capture listeners "$WPI_SS" -H -ltn 'sport = :8790'
); listenerred=$?
(
    EV_DIR="$Q/ev-listener-green"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'PRODUCTION_SS_ARGV=%s\n' "$*"; WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
    wpi_assert_listener_set
); listenergreen=$?
(
    EV_DIR="$Q/ev-listener-addr"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 10.0.0.5:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
    wpi_assert_listener_set
); listeneraddr=$?
printf 'LISTENER_RCS mutant_filtered=%s production_full_inventory=%s non_preregistered_address=%s\n' "$listenerred" "$listenergreen" "$listeneraddr"
expect_rc listener_mutant "$listenerred" 0; expect_rc listener_green "$listenergreen" 0; expect_rc listener_addr "$listeneraddr" 1

printf '#!/bin/sh\nprintf "Access denied\\n" >&2\nexit 5\n' > "$Q/systemctl-denied"; chmod 755 "$Q/systemctl-denied"
printf '#!/bin/sh\nprintf "/fixture/writable\\0"\nprintf "find denied\\n" >&2\nexit 1\n' > "$Q/find-partial"; chmod 755 "$Q/find-partial"
( common "$Q/ev-manager"; WPI_SYSTEMCTL="$Q/systemctl-denied"; wpi_assert_manager_ready ); manager=$?
( common "$Q/ev-partial"; WPI_FIND="$Q/find-partial"; wpi_run_find B3 partial /fixture -perm /222 -print0 ); partial=$?
(
    EV_DIR="$Q/ev-parity-fail"; mkdir -p "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56; WPI_PYTHON3=/usr/bin/python3
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: missing-or-wrong=demo-pkg' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); parityfail=$?
(
    EV_DIR="$Q/ev-parity-stop"; mkdir -p "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56; WPI_PYTHON3=/usr/bin/python3
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: Permission denied' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); paritystop=$?
(
    EV_DIR="$Q/ev-netns"; mkdir -p "$EV_DIR"; WPI_READLINK=/usr/bin/readlink; WPI_MAINPID=189813; CALL=0
    wpi_capture(){ CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; if [ "$CALL" -eq 1 ]; then printf 'net:[100]\n' > "$WPI_CAP_OUT"; else printf 'net:[200]\n' > "$WPI_CAP_OUT"; fi; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
    wpi_assert_netns_binding
); netns=$?
(
    EV_DIR="$Q/ev-http"; mkdir -p "$EV_DIR"; WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=0; printf '500\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"; }
    wpi_assert_status
); http=$?
printf 'REGRESSION_RCS manager_stop=%s partial_walk_stop=%s parity_fail=%s parity_generic_stop=%s netns_stop=%s http_fail=%s\n' "$manager" "$partial" "$parityfail" "$paritystop" "$netns" "$http"
expect_rc manager "$manager" 3; expect_rc partial "$partial" 3; expect_rc parity_fail "$parityfail" 1
expect_rc parity_stop "$paritystop" 3; expect_rc netns "$netns" 3; expect_rc http "$http" 1

/usr/bin/bash -n "$SCRIPT"; syntax=$?
printf 'BASH_N_RC=%s BYTES=%s SHA256=%s\n' "$syntax" "$(wc -c < "$SCRIPT")" "$(sha256sum "$SCRIPT" | cut -d' ' -f1)"
expect_rc bash_n "$syntax" 0
case "$Q" in /tmp/rp7-r4-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_ASSERT_FAIL unsafe_cleanup=%s\n' "$Q"; exit 93 ;; esac
printf 'QA_PASS all_assertions=yes\n'
# RP7_R4_FENCE_END
```

### Round-4 regression transcript (repaired bytes)

```text
QA_ROOT=/tmp/rp7-r4-qa.9gO8dw
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 uid_gid=4096:4096 live_mountinfo_records=4 symlinks=not_representable_msys2
REAL_GNU_DIAGNOSTIC=[/usr/bin/stat: cannot stat '/tmp/rp7-r4-qa.9gO8dw/absent-leaf': No such file or directory]
REAL_GNU_ABSENT kind=absent child_rc=1
DIAG_ACCEPTED id=abs_statx kind=absent
DIAG_ACCEPTED id=abs_stat kind=absent
DIAG_ACCEPTED id=abs_oserr kind=absent
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-diag-base_statx/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-diag-base_stat/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-diag-base_oserr/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-diag-foreign/ro.0001.lstat.stderr
STAT_DIAGNOSTIC_RCS real_gnu_absent=0 abs_statx=0 abs_stat=0 abs_oserr=0 base_statx=3 base_stat=3 base_oserr=3 foreign=3
N1_REAL_MOUNTINFO records=4 captured_by=wpi_capture_mountinfo_snapshot
N1_V2 clean=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 decoy_bind_under_release=74a1831126d71500bb26b663bc0923e5714679858bcb3d8c8bfa6898897a23e2 decoy_overlay_under_venv=7cb133713b58ce45a82b8180809b07e1f97032763f730e5ab578b3fc7657c6de repeat_clean=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359
N1_V1_ROUND2 clean=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf decoy_bind_under_release=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf decoy_overlay_under_venv=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf
N2_V2 clean_root=deda9484d62433422ff6245fcd96e1ac63868cbef5be8ad8540f2eb6cab82933 stacked_on_root=b165f1102f30d355d4e64d8bcdfab674c6d5ebc43b7f8c96ec958bbe1e285853 clean_usr_bin=ecab5e94c103cc51f91affcd987a611b69323da8000c076edbb24d1285e7d6b9 stacked_on_usr_bin=4b3ed988969beefa2893c51f96f22048c31f3df322a0b5d09f0e76852af9646a
N2_V1_ROUND2 clean_root=309e1645500547dc8b370dc621e9bc1ba984ea6f36b1debcd4ccf6c3473ea2bc stacked_on_root=309e1645500547dc8b370dc621e9bc1ba984ea6f36b1debcd4ccf6c3473ea2bc clean_usr_bin=8b4f25af2e3c8977afee2f1844e10e1a0d1849959a7736f0d73b364ffb3a8638 stacked_on_usr_bin=8b4f25af2e3c8977afee2f1844e10e1a0d1849959a7736f0d73b364ffb3a8638
V2_RECORD_SHAPE points=21 subtree=2 subtree_count=6
V2_EFFECTIVE_MOUNT kind=point path=/usr/bin/stat device=0:97 root=/ mount_point=/usr/bin fstype=tmpfs source=/dev/decoytools shared_mount_point_records=2
V2_TRUSTED_PYTHON_POINT kind=point path=/usr/bin/python3 device=0:97 root=/ mount_point=/usr/bin fstype=tmpfs source=/dev/decoytools shared_mount_point_records=2
V2_SUBTREE_USR_BIN kind=subtree_count subtree_root=/usr/bin records=2
COMPUTED_ATTESTATION sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 format=normalised_path_projection_v2
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-fail-mutant/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-fail-mutant/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=fixture_deviation
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-fail-green/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-fail-green/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-fail-green/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-fail-green/ro.0008.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
MOUNT_WINDOW_CLOSED
B3_FAIL reason=fixture_deviation
FAIL_GUARD_CLOSE mutant_rc=1 mutant_window_closed=0 production_rc=1 production_window_closed=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-guard-attest/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-guard-changed/ro.0002.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=5 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=5 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/n1-decoy projection=/tmp/rp7-r4-qa.9gO8dw/ev-guard-changed/ro.0006.mount_projection.tsv sha256=74a1831126d71500bb26b663bc0923e5714679858bcb3d8c8bfa6898897a23e2 content=not_printed
RP7_STOP reason=mount_topology_changed before=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 after=74a1831126d71500bb26b663bc0923e5714679858bcb3d8c8bfa6898897a23e2 format=normalised_path_projection_v2
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-guard-mismatch/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-guard-mismatch/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_STOP reason=mount_topology_mismatch observed=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 attested=0000000000000000000000000000000000000000000000000000000000000000 format=normalised_path_projection_v2
MOUNT_GUARD_RCS changed_downgrade=3 attestation_mismatch=3
B3_STOP reason=structured_path_unparseable source=find_stdout detail=unsafe_character
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-space/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-space/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-space/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-space/ro.0012.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=[unrenderable] path_sha256=565603d319c5019948e7655e2da5b2f006639a9ad9d087d2ed6cba5a41948f2e count=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-realfind/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-realfind/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.9gO8dw/ev-realfind/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.9gO8dw/ev-realfind/ro.0013.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=/tmp/rp7-r4-qa.9gO8dw/imm/sub count=2
UNSAFE_PATH_RCS mutant_stop=3 suppressed_render_fail=1 real_find_fail=1
MUTANT_RP7_tool name=stat path=/tmp/rp7-r4-qa.9gO8dw/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute
RP7_tool name=stat path=/tmp/rp7-r4-qa.9gO8dw/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=readlink path=/tmp/rp7-r4-qa.9gO8dw/tools/readlink owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=env path=/tmp/rp7-r4-qa.9gO8dw/tools/env owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=find path=/tmp/rp7-r4-qa.9gO8dw/tools/find owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=sha256sum path=/tmp/rp7-r4-qa.9gO8dw/tools/sha256sum owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=systemctl path=/tmp/rp7-r4-qa.9gO8dw/tools/systemctl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=ss path=/tmp/rp7-r4-qa.9gO8dw/tools/ss owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=curl path=/tmp/rp7-r4-qa.9gO8dw/tools/curl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=timeout path=/tmp/rp7-r4-qa.9gO8dw/tools/timeout owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=python3 path=/tmp/rp7-r4-qa.9gO8dw/tools/python3 owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
TOOL_ATTESTATION mutant_rc=0 mutant_attestation_fields=0 production_rc=0 self=4 bound_instrument=6 self_names=stat,env,sha256sum,timeout,
RP7_STOP reason=tool_not_evaluable tool=python3 detail=path_metadata_mismatch path=/tmp/rp7-r4-qa.9gO8dw/tools/python3 kind=symlink mode=755 owner_numeric=0:0 expected=regular,any,0:0
TRUSTED_PYTHON_PIN symlinked_pin_rc=3 symlink_rejected=1
REAL_CHARDEV raw=[character special file] token=[other]
MUTANT_B3_STOP reason=path_not_evaluable path=/ detail=root_kind_character special file
MUTANT_B1_STOP reason=interpreter_object_unbound kind=character special file target=none
B3_STOP reason=path_not_evaluable path=/ detail=root_kind_other
B1_STOP reason=interpreter_object_unbound kind=other target=none
KIND_TOKEN_RCS real_chardev=0 root_kind_stop=3 interpreter_kind_stop=3 root_token_ok=1 interpreter_token_ok=1
TIMEOUT_ENV mutant_marker=1 mutant_vars=104 production_marker=0 production_vars=10
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=8 elapsed_ms=8070 budget_s=2
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=2 elapsed_ms=2040 budget_s=2
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=8 production_wall_s=2 budget_s=2 child_sleep_s=8
B1_interpreter path=/tmp/rp7-r4-qa.9gO8dw/venv/bin/python object=non_symlink_regular preexec_binding=component_and_mount_window_closed exec_binding=separate_bounded_exec version_family=3.12 env=cleared isolated=yes
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy/target
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok
INTERPRETER_RCS regular_pass=0 symlink_stop=3 cr_stop=3 cr_forged_lines=0 cr_single_sanitised_line=1
FORGE_FIXTURES venv_rc=0,0 pth=[import os,sys; open(r"C:\Users\BARSEM~1\AppData\Local\Temp\rp7-r4-qa.9gO8dw\pth.marker","w").write("1"); sys.stdout.write("OK fields=8"+chr(10)); sys.stdout.flush(); os._exit(0)] sitecustomize_lines=5
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
PTH_FORGE_STATUS red_rc=0 red_marker=1 red_false_pass=1 green_rc=1 green_marker=0 green_truthful_fail=1
PTH_FORGE_SAME_INTERPRETER green_venv_interpreter_rc=1 green_venv_marker=0 green_venv_truthful_fail=1 isolated_variable=minus_S
VERIFIER_IDENTITY bytes=3735 sha256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5 source=candidate_worktree_lf_normalised
B1_lock_parity result=pass packages=2 output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_lock_parity result=pass packages=2 output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe
SITECUSTOMIZE_FORGE_PARITY red_rc=0 red_marker=1 red_false_pass=1 green_rc=1 green_marker=0 green_truthful_fail=1 clean_rc=0 clean_marker=0 clean_pass=1
SITECUSTOMIZE_FORGE_SAME_INTERPRETER green_venv_interpreter_rc=1 green_venv_marker=0 green_venv_truthful_fail=1 isolated_variable=minus_S
B1_STOP reason=verifier_not_evaluable rc=4 detail=trusted_startup_unproven
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3
NO_SITE_GUARD parity_rc=3 parity_refused=1 status_rc=3 status_refused=1
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_listener_inventory rows=2 port_8790_rows=1 bytes=70 evidence_file=/tmp/rp7-r4-qa.9gO8dw/ss-wccomplete-green/ss.out content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_listener_inventory rows=2 port_8790_rows=1 bytes=72 evidence_file=/tmp/rp7-r4-qa.9gO8dw/ss-good-green/ss.out content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
LISTENER_ORDER red_wildcard_first_rc=1 red_malformed_first_rc=3 green_wildcard_first_rc=3 green_malformed_first_rc=3 expected_both_stop=3
LISTENER_COMPLETE_TABLE wildcard_fail_rc=1 good_rc=0 inventory_before_verdict=1
B1_metadata_universe root=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages entries=3 dist_info_dirs=2 non_metadata_entries=1 enumeration=unfiltered_maxdepth_1 universe=explicit_dist_info_only
B1_metadata_preflight root=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages dist_info_dirs=2 complete=yes readable=yes
B1_metadata_preflight root=/tmp/rp7-r4-qa.9gO8dw/f3-egg/venv/lib/python3.12/site-packages dist_info_dirs=2 complete=yes readable=yes
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-egg/venv/lib/python3.12/site-packages/ghost.egg-info format=egg_info
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-pth/venv/lib/python3.12/site-packages/evil.pth format=pth
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-hook/venv/lib/python3.12/site-packages/sitecustomize.py format=startup_hook
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-zip/venv/lib/python3.12/site-packages/wheelhouse.zip format=zip
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-filedi/venv/lib/python3.12/site-packages/broken-1.0.dist-info format=dist_info_kind_regular
B1_FAIL reason=distribution_metadata_absent path=/tmp/rp7-r4-qa.9gO8dw/f3-absent/venv/lib/python3.12/site-packages/gone-1.0.dist-info/METADATA
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f3-unread/venv/lib/python3.12/site-packages/demo_pkg-1.0.dist-info/METADATA rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/f3-ev-t09/ro.0049.lstat.stderr
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info detail=dist_info_kind_character special file
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info format=dist_info_kind_other
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info/METADATA detail=kind_character special file
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info/METADATA detail=kind_other
METADATA_UNIVERSE_RCS clean=0 egg_red=0 egg_green=3 pth=3 hook=3 zip=3 dist_info_file=3 member_absent=1 member_unreadable=3 chardev_dir_red=3 chardev_dir=3 chardev_member_red=3 chardev_member=3
B1_STOP reason=metadata_universe_unexpected stage=verifier format=egg_info name_sha256=cf1057a30e78603c62e83b18e1c5697aca2bfeac81a18a4707b550f2e8b99132
B1_STOP reason=metadata_universe_unexpected stage=verifier format=startup_hook name_sha256=1dc3332b767b1b60ea953e5dfdd81df90bf3449d9c313c945bbdb29e78f45ff8
B1_lock_parity result=pass packages=2 output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe
DRIVER_UNIVERSE egg_rc=3 hook_rc=3 clean_rc=0
B5B6_DECLARED_ORDER wpi_assert_netns_binding,wpi_assert_status,wpi_assert_listener_set,
B6_netns caller=net:[100] service=net:[100] mainpid=189813 binding=equal
B6_listener_inventory rows=1 port_8790_rows=1 bytes=37 evidence_file=/tmp/rp7-r4-qa.9gO8dw/order-red/3.out content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes
B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790
B6_netns caller=net:[100] service=net:[100] mainpid=189813 binding=equal
B5_FAIL reason=status_endpoint_unexpected_http code=500
TWO_DEVIATION red_rc=1 red_first_result=[B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790] green_rc=1 green_first_result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
B1a_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/requirements.lock rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/f5-ev-r17unread_red/ro.0023.lstat.stderr
B1a_STOP reason=installed_lock_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/requirements.lock rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/f5-ev-r17unread/ro.0023.lstat.stderr
B1_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/f5-ev-r19aunread_red/ro.0027.lstat.stderr
B1_STOP reason=verifier_unreadable path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/f5-ev-r19aunread/ro.0027.lstat.stderr
B1a_FAIL reason=installed_lock_object_unexpected path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/requirements.lock kind=directory
B1a_FAIL reason=installed_lock_object_unexpected kind=directory
B1a_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/requirements.lock kind=regular mode=644 owner_numeric=1000:1000 expected=regular,any,0:0
B1a_FAIL reason=installed_lock_owner_unexpected owner_numeric=1000:1000 expected=0:0
B1_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py kind=regular mode=644 owner_numeric=1000:1000 expected=regular,any,0:0
B1_FAIL reason=verifier_owner_unexpected path=/tmp/rp7-r4-qa.9gO8dw/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py owner_numeric=1000:1000 expected=0:0
ROW_GRAMMAR_RCS r17_unread_red=3 r17_unread=3 r19a_unread_red=3 r19a_unread=3 r17_kind_red=1 r17_kind=1 r17_owner_red=1 r17_owner=1 r19a_owner_red=1 r19a_owner=1
MUTANT_MOUNT_POINT=/mnt/*
RP7_mount_table parsed=yes records=1 content=not_printed
PRODUCTION_MOUNT_POINT=/mnt/* GLOB_PARSE_RC=0
B5_STOP reason=mutant_wrong_type_classification B5 flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3
B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
B5_STOP reason=schema_unexpected field=state_version
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
MUTANT_SS_ARGV=listeners /usr/bin/ss -H -ltn sport = :8790
PRODUCTION_SS_ARGV=listeners /usr/bin/ss -H -ltn
B6_listener_inventory rows=2 port_8790_rows=1 bytes=72 evidence_file=/tmp/rp7-r4-qa.9gO8dw/ev-listener-green/ss.out content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
B6_listener_inventory rows=1 port_8790_rows=1 bytes=37 evidence_file=/tmp/rp7-r4-qa.9gO8dw/ev-listener-addr/ss.out content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes
B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790
LISTENER_RCS mutant_filtered=0 production_full_inventory=0 non_preregistered_address=1
RP7_STOP reason=system_manager_unreachable rc=5 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-manager/ro.0001.system_manager.stderr
B3_STOP reason=walk_incomplete root=/fixture rc=1 detail=diagnostic_captured diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-partial/ro.0001.partial.stderr partial_stdout_discarded=/tmp/rp7-r4-qa.9gO8dw/ev-partial/ro.0001.partial.stdout
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_STOP reason=verifier_not_evaluable rc=1 detail=unclassified_verifier_result diagnostic_file=/tmp/rp7-r4-qa.9gO8dw/ev-parity-stop/err
B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]
B5_FAIL reason=status_endpoint_unexpected_http code=500
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
BASH_N_RC=0 BYTES=108301 SHA256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
QA_PASS all_assertions=yes
```

Its final line re-derives the round-9 identity from inside the round-4 fence:
`BASH_N_RC=0 BYTES=108301 SHA256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`.

Two lines in that transcript now read differently from round 4 and are expected to:
`TOOL_ATTESTATION ... self=4 bound_instrument=6` still holds because the attestation
vocabulary did not change, and `V2_TRUSTED_PYTHON_POINT` still shows the trusted
interpreter as a projection point. What changed in the block is *where* that interpreter is
bound, which the round-4 fence never observed - that is what the round-5 F1 arm is for.

### Literal re-run of the published command against this document

The published command was executed verbatim **twice**: once to produce the six transcripts
above, and once more against **this file as delivered**, after they had been pasted in and
the prose rewritten. Its wall clock is not pinned here, because pinning it would mean editing
the file after the run it describes; everything else about it is. Both runs returned rc 0;
all six fences printed `QA_PASS all_assertions=yes`
(`R9_FENCE_RC=0`, `R8_FENCE_RC=0`, `R7_FENCE_RC=0`, `R6_FENCE_RC=0`, `R5_FENCE_RC=0`,
`R4_FENCE_RC=0`) followed by the command's own summary line
`PUBLISHED_COMMAND_RESULT=pass fences=6 per_fence_bound_s=900 kill_grace_s=30
fence_timeout_budget_s=5580 whole_command_bound=none prelude_bounded=no
wrapper_stream=unnamed_pipe_body_cannot_write`.

**The command's stderr is no longer empty, and that is the round-9 change rather than a
regression.** It carries exactly the six `WRAPPER_STREAM fence=<f> bytes=<n> [<text>]` lines -
one per fence, `bytes=0 []` in a clean run - plus whatever each bounded body wrote to its own
stderr file. Round 8 merged those two writers into one file per fence and a body could
therefore forge the wrapper's diagnostic; round 9 separates them and prints both, so nothing
is hidden by the separation. `RUN_ONE_STDERR_BYTES` below is the whole of it.

Pasting transcripts and editing prose changed no byte inside any marker range, which is why
the fence-body digests and byte counts are identical in both runs. Run one recorded:

```text
RUN_ONE_RC=0 RUN_ONE_WALL_S=229 RUN_ONE_STDOUT_BYTES=66458 RUN_ONE_STDERR_BYTES=210
WRAPPER_STREAM fence=r9 bytes=0 []
WRAPPER_STREAM fence=r8 bytes=0 []
WRAPPER_STREAM fence=r7 bytes=0 []
WRAPPER_STREAM fence=r6 bytes=0 []
WRAPPER_STREAM fence=r5 bytes=0 []
WRAPPER_STREAM fence=r4 bytes=0 []
9602bb0b6a129f509cba61150e81dc116f756af034983094c6745c839055848f */tmp/rp7-r9-fence-body.sh   28389 B
f5caef75c68a84e396113dd60519d4b6df8c00feb7b90fd12dc73121e9b9b6ca */tmp/rp7-r8-fence-body.sh   31514 B
9438700ec3b8e8f23d5b2c4cb95fac28db3e6ac69cf5032cc5604728a176efcf */tmp/rp7-r7-fence-body.sh   23347 B
fa4897e752350ccc37efa4f178cfb7522677453f2b76de3d873a2c9bb204195b */tmp/rp7-r6-fence-body.sh   38830 B
aa21ec19883274392427298e74541759c574009008aad86e3c169ee9cbc857c9 */tmp/rp7-r5-fence-body.sh   21263 B
a0fd7291b89f9a28169bfa15432c66b6dba79cbda0d4a558fab1f981007073ab */tmp/rp7-r4-fence-body.sh   79457 B
RUN_TWO_AND_THREE=recorded_in_RP7_REPAIR_R9_REPORT.md reason=a_run_pinned_inside_the_file_it_reads_is_not_a_fixed_point
```

**Two outputs had to be made fixed points for that to be true, and both changes are stated
rather than assumed.** The round-8 `READER_FIELD_LABEL` line counts the renamed reader field
inside the round-7 fence body rather than across the whole document, because a document-wide
count grows every time a transcript containing the field is pasted back in - a number that
moves when the file is edited is not reproducible by a third party. The round-8
`UNBOUNDED_PRELUDE` assertion bounds its wall clock to the outer window rather than pinning
one integer, because `SECONDS` rounding makes a 3 s window read as 3 or 4; the gate is
`outer_test_rc=124` with no stdout, which is the claim, and the second is reported evidence.

Each run took a little under four minutes, which is inside the enforced 900 s bound of any
one fence by an order of magnitude. It is **not** compared against the 5580 s fence-timeout
budget as though that were a bound on the command: nothing bounds this command as a whole,
the result line says so, and the round-8 F3 arm demonstrates it.

A diff of the recorded run against the final one, ignoring the `mktemp` scratch names, is
confined to the handful of measured wall clocks and Windows scratch paths that are the only
non-deterministic outputs in the suite. Every rc, digest, reason token and result line is
identical, and the six fence-body digests above are byte-for-byte the same in both.

## What this QA does not establish

- No accepting `wpi_validate_inputs` arm exists and none can exist before freeze: three
  freeze-gate constants (`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
  `WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_EVIDENCE_ROOT`) are still `<PIN-AT-FREEZE>` and
  deliberately refuse the accepting arm until the deploy channel supplies them.
- **CLOSED IN ROUND 9 - the status body is no longer addressed by name at all.** Round 8
  listed this here as an accurate residual; Codex round-9 part B finding 1 executed both
  halves of it and made it a BLOCK, on the principle this round is built around: a
  disclosure is not a control. The leaf is now opened by `wpi_open_leaf`, curl is given
  `--output /dev/fd/3` where fd 3 is a duplicate of the creating descriptor installed in the
  child, and the parser's stdin is a descriptor derived from that same open BEFORE the child
  exists. The parser digests exactly the bytes it parses and reports that digest, so
  `body_sha256` cannot disagree with the verdict beside it. `wpi_alloc_leaf`, the name-only
  allocator, is deleted rather than left available. What remains disclosed is narrower and
  the deletion is statically pinned here: `rg -n "wpi_alloc_leaf"
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` returns no matches
  (occurrence count 0), while the single create-once write open is now
  `wpi_open_leaf()` at `RP7-WPI-RO.sh:272` with the only allocator write-open
  statement `{ exec {WPI_LEAF_FD}>"$leaf"; }` at `RP7-WPI-RO.sh:281`.
  The remaining disclosure is stated in the round-9 fence: on Linux `/dev/fd/<n>` resolves through the process's
  descriptor table, which is the binding this repair rests on; MSYS2 resolves it through the
  path, so on THIS workstation the outside-write arm's GREEN disposition is a fail-closed
  `rc=23 detail=transport_error` rather than the Linux `rc=0` completion. Both establish
  that no object outside the tree is written and no accepting line is produced over
  substituted bytes; only the first is reproducible here.
- **Readers outside rows 20-24 still open by name, and that boundary is now the residual.**
  Round 7 bound one reader - the listener inventory - and left the rest of its class on the
  name; an executed substitution then turned a child-observed HTTP 500 into an accepting 200
  and two unequal namespaces into an equal pair (Codex round-7 part B finding 2). Round 8
  closes the class **for this band**: the row-20 status code, the row-21 parser result, both
  row-22 namespace identities, the row-22 inventory, and the emptiness of the diagnostic
  stream each of those is conditioned on, are all read through the descriptor `wpi_capture`
  re-derived from its own creating write descriptor. All five are falsified above by executed
  substitutions the round-7 bytes adjudicate and the round-8 bytes do not, and by a stub that
  binds nothing, which the round-8 bytes refuse rather than fall back on a name.
  **What is still open, precisely:**
  - the rows 10-19 readers - `wpi_lstat`, `wpi_assert_manager_ready`,
    `wpi_assert_evidence_leaf_bound`, the `find`-stdout walkers in `wpi_assert_tree` and the
    metadata enumeration, the interpreter `-V` record and the verifier's stdout and stderr -
    all still resolve the leaf name after the child has run. Rows 10-19 were out of scope for
    the round-6 and round-7 audit bands, and no row among them states captured identity for
    its bytes; what the block establishes about their content is exactly what their record
    grammar establishes, which is why each STOPs on a record it cannot represent byte for
    byte, including NUL, rather than adjudicating it. This is the obvious next candidate and
    it is named here as such, not argued away: the mechanism now exists
    (`wpi_captured_record`, `wpi_require_empty_captured`) and applying it is a matter of
    scope, not of design.
  - **C1 mount-projection digest residual, stated separately.** The mount-projection writer
    creates its evidence leaf through `wpi_open_leaf`, but the guard then calls
    `wpi_sha_file` on the projection path. That digest is computed over a re-resolved name,
    so the mount-guard gate compares a digest of whatever that name resolves to at digest
    time. This rows-1-9 round intentionally does not change the mount-projection code; the
    repair belongs with the next rows-10-19 reader class.
  - the read-diagnostic leaves. Every reader above redirects `read`'s own stderr into a
    create-once leaf and then requires that leaf empty **by name**. Those bytes are not a
    child observation - only this shell's `read` ever writes them - but the name is resolved
    a second time, so the same substitution route exists for the hard-read-error check.
  - (round 8 also listed `wpi_sha_file "$body"` here. That call no longer exists: row 21's
    digest is computed inside the parser child over the bytes it read from the bound
    descriptor, and there is no second read of the body to bind.)
- The binding re-derives each read descriptor from its write descriptor **after** the child
  exits and **before** the write descriptor is closed, so no name is resolved in between and
  the child never inherits the read side. What it does not establish is the window between
  the `O_CREAT|O_EXCL` open and the child's own writes: that window is covered by the write
  binding, not by this one, and the round-6 F5 arm is what measures it.
- **The published command bounds six fence calls and nothing else.** `6 * (900 + 30) = 5580`
  is a fence-timeout budget, not a bound on the command: the six `sed` extractions, the
  `sha256sum`, the `wc -c`, the `cat` of the captured body diagnostics and the shell's own
  overhead are outside every wrapper, and the round-8 F3 arm demonstrates that with a FIFO
  that blocks the first extraction before any wrapper starts. The result line states this in
  as many words (`whole_command_bound=none prelude_bounded=no`). Round 7 claimed 3720 was
  "an upper bound no execution of this command can exceed"; that claim is withdrawn, not
  reworded.
- **An rc of 137 is attributed from the wrapper's own stream, and only that far.**
  `--verbose` makes GNU `timeout` announce the signals it sends, and round 9 moved that
  announcement onto a channel the bounded body has neither a descriptor nor a name for: an
  unnamed pipe read into a shell variable, with the body's own stderr redirected to a
  separate file by the `sh -c` shim before it execs. Round 8 grepped a stderr file BOTH
  wrote, and Codex round-9 part B finding 3 executed the forgery - a body printing
  `timeout: sending signal KILL to command` and exiting 137 was called this wrapper's
  kill-after event. That input is now `kind=sigkill_not_from_this_wrapper`. What this still
  does **not** establish is that no other SIGKILL reached the fence: a body killed by
  something else *while* the wrapper was also killing it is reported as a kill-after event.
  Nor does it establish anything about a body that can write arbitrary files: the claim is
  that the body cannot write THIS stream, which is true because the stream has no name.
- An ownership/mode precondition on `EV_DIR` (which would bound *who* could race) was also
  considered and rejected: the mode of the evidence directory is not a preregistered input,
  RP0-BOOTSTRAP allocates it, and a block that STOPs on a group-writable evidence directory
  would fail the run for a condition no accepted document requires.
- The `evidence_root=<root> root_binding=frozen_prefix_descent` fields on the
  `RP7_evidence_bound` line are rendered from the constant that
  `wpi_assert_prerequisites` proved; that proof is falsified above, the rendering is not
  separately falsified here.
- The IPv6 address grammar admits any literal that satisfies the group/compression/zone
  rules. It is a grammar check, not an assertion that the kernel would have produced that
  particular rendering, and no arm feeds a real IPv6 listener from a real `ss`.
- No real bind or overlay mount, no real staging host, no real `/proc/<MainPID>/ns/net`,
  no root, no POSIX symlink, no character device at an arbitrary path.
- `shellcheck` is not installed on this workstation; no ShellCheck result is claimed.

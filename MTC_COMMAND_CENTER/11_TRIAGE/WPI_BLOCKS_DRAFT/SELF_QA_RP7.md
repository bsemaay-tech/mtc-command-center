# SELF-QA — RP7-WPI-RO.sh

Status: `SELF-QA-COMPLETE-PENDING-INDEPENDENT-AUDIT`

This QA was run locally in Git Bash/MSYS. It made no SSH/SCP call, opened no
network connection, contacted no host, minted no RUNID, and changed no host
object. All fixture writes were below a fresh `/tmp/rp7-final-qa.*` directory.

The accepted library was verified before its conventions were read:

```text
bytes=18968
sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48
```

## Test method and falsification boundary

The executable fence below is self-contained. `source <(sed '$d' "$SCRIPT")`
loads the final RP7 function definitions byte-for-byte and removes only the
last invocation line, `wpi_main "$@"`, so focused fixtures can call a single
production function without touching preregistered host paths. Deliberately
wrong pre-fix behavior exists only in the two functions whose names begin
`mutant_`; their RED results are compared with the final production functions'
STOP results using the same shims.

The Windows Python used by Git Bash writes CRLF. The strict-JSON fixture's
`status_json` arm therefore uses the recorded `sed 's/\r$//'` pipe solely to
emulate the Linux interpreter's LF stdout interface. The pipeline status vector
is captured immediately and both components are adjudicated. The Python code
being tested is the exact `-c` argument supplied by `wpi_assert_status`.

## Exact paste-and-run command

Paste the following entire fence into Git Bash from the repository root:

```bash
ROOT=/c/LAB/Tradingview_LAB_CLEAN
SCRIPT=$ROOT/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
LIB=$ROOT/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP0-LIB.sh
Q=$(mktemp -d /tmp/rp7-final-qa.XXXXXX)
source <(sed '$d' "$SCRIPT")
trap - ERR
set +Eeuo pipefail
printf 'QA_ROOT=%s\n' "$Q"

printf '%s\n' '#!/usr/bin/env bash' 'printf "Access denied\\n" >&2' 'exit 5' > "$Q/systemctl-denied"
printf '%s\n' '#!/usr/bin/env bash' 'printf "/fixture/writable\\0"' 'printf "find: /fixture/denied: Permission denied\\n" >&2' 'exit 1' > "$Q/find-partial"
chmod 700 "$Q/systemctl-denied" "$Q/find-partial"

mkdir "$Q/manager-red" "$Q/manager-green" "$Q/manager-missing"
(
 EV_DIR="$Q/manager-red"; WPI_ENV=/usr/bin/env; WPI_STAT=/usr/bin/stat; WPI_SYSTEMCTL="$Q/systemctl-denied"
 mutant_manager_compare_first(){ wpi_capture manager_mutant "$WPI_SYSTEMCTL" --system show --property=Version; [ "$WPI_CAP_RC" -eq 0 ] || wpi_fail B4 'property_mismatch prop=Version observed=empty expected=manager_response'; }
 mutant_manager_compare_first
); mr=$?
(
 EV_DIR="$Q/manager-green"; WPI_ENV=/usr/bin/env; WPI_STAT=/usr/bin/stat; WPI_SYSTEMCTL="$Q/systemctl-denied"
 wpi_assert_manager_ready
); mg=$?
(
 EV_DIR="$Q/manager-missing"; WPI_ENV=/usr/bin/env; WPI_STAT=/usr/bin/stat; WPI_SYSTEMCTL="$Q/does-not-exist"
 wpi_assert_manager_ready
); mm=$?
printf 'MANAGER_RCS mutant=%s denied=%s missing=%s\n' "$mr" "$mg" "$mm"

mkdir "$Q/walk-red" "$Q/walk-green"
(
 EV_DIR="$Q/walk-red"; WPI_ENV=/usr/bin/env; WPI_STAT=/usr/bin/stat; WPI_TIMEOUT=/usr/bin/timeout; WPI_FIND="$Q/find-partial"; WPI_SWEEP_BUDGET_S=120
 mutant_partial_stdout_first(){ wpi_capture mutant "$WPI_TIMEOUT" 121 "$WPI_FIND" /fixture -perm /222 -print0; if [ -s "$WPI_CAP_OUT" ]; then wpi_fail B3 'writable_path_inside_immutable_tree path=/fixture/writable'; fi; [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B3 "walk_incomplete root=/fixture rc=$WPI_CAP_RC"; }
 mutant_partial_stdout_first
); wr=$?
(
 EV_DIR="$Q/walk-green"; WPI_ENV=/usr/bin/env; WPI_STAT=/usr/bin/stat; WPI_FIND="$Q/find-partial"; WPI_SWEEP_BUDGET_S=120
 wpi_run_find B3 partial_walk /fixture -perm /222 -print0
); wg=$?
printf 'PARTIAL_WALK_RCS mutant=%s accepted=%s\n' "$wr" "$wg"

mkdir "$Q/b3-red" "$Q/b1a-red" "$Q/b1-red" "$Q/b1-stop" "$Q/b5-red" "$Q/b6-red" "$Q/netns"
(
 EV_DIR="$Q/b3-red"; wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ :; }
 wpi_run_find(){ WPI_CAP_OUT="$EV_DIR/find.out"; WPI_CAP_ERR="$EV_DIR/find.err"; WPI_CAP_ELAPSED_MS=4; : > "$WPI_CAP_ERR"; printf '/fixture/writable\0' > "$WPI_CAP_OUT"; }
 wpi_assert_tree /fixture release
); b3r=$?
(
 EV_DIR="$Q/b1a-red"; wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ WPI_META_SIZE=117762; }; wpi_sha_file(){ WPI_LINE=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff; }
 wpi_assert_regular_digest B1a installed_lock_absent installed_lock_digest_mismatch /fixture/requirements.lock 117762 a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e installed_lock installed_lock_object_unexpected
); b1ar=$?
(
 EV_DIR="$Q/b1-red"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5; WPI_EXPECTED_PACKAGES=56
 wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/parity.out"; WPI_CAP_ERR="$EV_DIR/parity.err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: missing-or-wrong=demo-pkg' > "$WPI_CAP_ERR"; }
 wpi_assert_lock_parity
); b1r=$?
(
 EV_DIR="$Q/b1-stop"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5; WPI_EXPECTED_PACKAGES=56
 wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/parity.out"; WPI_CAP_ERR="$EV_DIR/parity.err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: Permission denied' > "$WPI_CAP_ERR"; }
 wpi_assert_lock_parity
); b1s=$?
(
 EV_DIR="$Q/b5-red"; WPI_CURL=/fixture/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
 wpi_capture(){ WPI_CAP_OUT="$EV_DIR/http.out"; WPI_CAP_ERR="$EV_DIR/http.err"; WPI_CAP_RC=0; printf '500\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
 wpi_assert_status
); b5r=$?
(
 EV_DIR="$Q/b6-red"; WPI_SS=/fixture/ss
 wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; printf '%s\n' 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
 wpi_assert_listener_set
); b6r=$?
(
 EV_DIR="$Q/netns"; WPI_READLINK=/fixture/readlink; WPI_MAINPID=189813; CALL=0
 wpi_capture(){ CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/ns.$CALL.out"; WPI_CAP_ERR="$EV_DIR/ns.$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; if [ "$CALL" -eq 1 ]; then printf 'net:[100]\n' > "$WPI_CAP_OUT"; else printf 'net:[200]\n' > "$WPI_CAP_OUT"; fi; }
 wpi_assert_netns_binding
); nsr=$?
printf 'MAJOR_RED_RCS B3=%s B1a=%s B1=%s B5=%s B6=%s B1_generic_error=%s netns_mismatch=%s\n' "$b3r" "$b1ar" "$b1r" "$b5r" "$b6r" "$b1s" "$nsr"

mkdir "$Q/b3-green" "$Q/b1a-green" "$Q/b1-green" "$Q/b5-green" "$Q/b6-green"
(
 EV_DIR="$Q/b3-green"; wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ :; }
 wpi_run_find(){ WPI_CAP_OUT="$EV_DIR/find.out"; WPI_CAP_ERR="$EV_DIR/find.err"; WPI_CAP_ELAPSED_MS=3; : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
 wpi_assert_tree /fixture release
); b3g=$?
(
 EV_DIR="$Q/b1a-green"; wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ WPI_META_SIZE=117762; }; wpi_sha_file(){ WPI_LINE=a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e; }
 wpi_assert_regular_digest B1a installed_lock_absent installed_lock_digest_mismatch /fixture/requirements.lock 117762 a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e installed_lock installed_lock_object_unexpected
); b1ag=$?
(
 EV_DIR="$Q/b1-green"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5; WPI_EXPECTED_PACKAGES=56
 wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/parity.out"; WPI_CAP_ERR="$EV_DIR/parity.err"; WPI_CAP_RC=0; printf '%s\n' 'verify_lock: PASS: lock+installed; packages=56' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
 wpi_assert_lock_parity
); b1g=$?
(
 EV_DIR="$Q/b5-green"; WPI_CURL=/fixture/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; CALL=0
 wpi_capture(){ local label="$1"; CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; case "$label" in status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;; sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT" ;; status_json) printf 'OK fields=8\n' > "$WPI_CAP_OUT" ;; esac; }
 wpi_assert_status
); b5g=$?
(
 EV_DIR="$Q/b6-green"; WPI_SS=/fixture/ss
 wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; printf '%s\n' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
 wpi_assert_listener_set
); b6g=$?
printf 'MAJOR_GREEN_RCS B3=%s B1a=%s B1=%s B5=%s B6=%s\n' "$b3g" "$b1ag" "$b1g" "$b5g" "$b6g"

mkdir "$Q/json-good" "$Q/json-dup"
run_json_case(){
 local root="$1" json="$2"; (
  EV_DIR="$root"; WPI_CURL=/fixture/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_VENV_ROOT=/fixture/venv; CALL=0; BODY_JSON="$json"
  wpi_capture(){
   local label="$1"; local -a ps; shift; CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"
   case "$label" in
    status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '%s\n' "$BODY_JSON" > "$EV_DIR/ro.status.body" ;;
    sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT" ;;
    status_json) shift; set +e; python "$@" 2> "$WPI_CAP_ERR" | sed 's/\r$//' > "$WPI_CAP_OUT"; ps=("${PIPESTATUS[@]}"); set -e; [ "${ps[1]}" -eq 0 ] || return 99; WPI_CAP_RC=${ps[0]} ;;
   esac
  }
  wpi_assert_status
 ); return $?
}
GOOD='{"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
DUP='{"state":"DISARMED","state":"ARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'
run_json_case "$Q/json-good" "$GOOD"; jg=$?
run_json_case "$Q/json-dup" "$DUP"; jd=$?
printf 'STRICT_JSON_RCS good=%s duplicate_key=%s\n' "$jg" "$jd"

mkdir "$Q/read-ev1" "$Q/read-ev2" "$Q/read-dir"
printf '%s' '36 25 0:32 / / rw - ext4 /dev/root rw' > "$Q/mount-no-final-newline"
( EV_DIR="$Q/read-ev1"; wpi_parse_mountinfo "$Q/mount-no-final-newline" ); rn=$?
( EV_DIR="$Q/read-ev2"; wpi_parse_mountinfo "$Q/read-dir" ); rd=$?
printf 'LINE_READER_RCS no_final_newline=%s directory_source=%s\n' "$rn" "$rd"

mkdir "$Q/input-ev"; : > "$Q/input-ev/ro.log"
(
 RUNID=QA-RP7-INPUT; EV_STAGE_ID=ro; EV_DIR="$Q/input-ev"; EV_LOG="$Q/input-ev/ro.log"
 . "$LIB"; . "$SCRIPT"
); im=$?
printf 'INPUT_MISSING_RC=%s\n' "$im"
```

## Real captured output

```text
QA_ROOT=/tmp/rp7-final-qa.9e7JqZ
B4_FAIL reason=property_mismatch prop=Version observed=empty expected=manager_response
RP7_STOP reason=system_manager_unreachable rc=5 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-final-qa.9e7JqZ/manager-green/ro.0001.system_manager.stderr
RP7_STOP reason=system_manager_unreachable rc=127 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-final-qa.9e7JqZ/manager-missing/ro.0001.system_manager.stderr
MANAGER_RCS mutant=1 denied=3 missing=3
B3_FAIL reason=writable_path_inside_immutable_tree path=/fixture/writable
B3_STOP reason=walk_incomplete root=/fixture rc=1 detail=diagnostic_captured diagnostic_file=/tmp/rp7-final-qa.9e7JqZ/walk-green/ro.0001.partial_walk.stderr partial_stdout_discarded=/tmp/rp7-final-qa.9e7JqZ/walk-green/ro.0001.partial_walk.stdout
PARTIAL_WALK_RCS mutant=1 accepted=3
B3_path path=/fixture kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount
B3_FAIL reason=writable_path_inside_immutable_tree path=/fixture/writable
B1a_FAIL reason=installed_lock_digest_mismatch observed=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff expected=a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_STOP reason=verifier_not_evaluable rc=1 detail=unclassified_verifier_result diagnostic_file=/tmp/rp7-final-qa.9e7JqZ/b1-stop/parity.err
B5_FAIL reason=status_endpoint_unexpected_http code=500
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]
MAJOR_RED_RCS B3=1 B1a=1 B1=1 B5=1 B6=1 B1_generic_error=3 netns_mismatch=3
B3_path path=/fixture kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount
B3_sweep root=/fixture complete=yes elapsed_ms=3 writable_paths=0
B1a_digest path=/fixture/requirements.lock bytes=117762 sha256=a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e binding=component_and_mount
B1_lock_parity result=pass packages=56 output=structurally_parsed
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
MAJOR_GREEN_RCS B3=0 B1a=0 B1=0 B5=0 B6=0
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
STRICT_JSON_RCS good=0 duplicate_key=3
RP7_STOP reason=mount_table_unterminated_final_record path=/tmp/rp7-final-qa.9e7JqZ/mount-no-final-newline records=0
RP7_STOP reason=mount_table_read_error path=/tmp/rp7-final-qa.9e7JqZ/read-dir records=0 detail=diagnostic_stream_nonempty diagnostic_file=/tmp/rp7-final-qa.9e7JqZ/read-ev2/ro.0001.mount_table.read.stderr
LINE_READER_RCS no_final_newline=3 directory_source=3
RP7_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP7-WPI-RO stage=ro
RP0_NOTE component_ok name=RUNID value=QA-RP7-INPUT
RP0_NOTE component_ok name=EV_STAGE_ID value=ro
RP7_STOP reason=prereg_input_missing name=WPI_CANDIDATE_SHA
INPUT_MISSING_RC=3
```

## Coverage interpretation

- Manager RED/accepted pair: the deliberate compare-first mutant emits a false
  B4 FAIL; both a denied manager and a missing `systemctl` path produce RP7 STOP
  before any B3/B1/B5/B6 comparison.
- Partial-walk RED/accepted pair: the stdout-first mutant emits the forbidden
  B3 FAIL; final `wpi_run_find` discards the pathname and returns B3 STOP.
- Major groups: one deliberate deviant fixture each produces rc 1 for B3s,
  B1a, B1, B5, and B6. Corresponding conforming fixtures return rc 0.
- A generic verifier error is rc 3, not package-drift FAIL. A namespace mismatch
  is rc 3 before either listener or endpoint output can be interpreted.
- Strict JSON accepts the typed expected object and rejects a duplicate key.
- Both an unterminated final mount record and a directory/read-error source are
  rc 3. Missing preregistered input is rc 3 with
  `reason=prereg_input_missing`.

## Final-byte checks

Exact PowerShell command:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' -n 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
$rc=$LASTEXITCODE
"bash_n_rc=$rc"
$i=Get-Item -LiteralPath 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
"bytes=$($i.Length)"
"sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $i.FullName).Hash.ToLowerInvariant())"
```

Real output:

```text
bash_n_rc=0
bytes=44198
sha256=81a292418d78a2fb6ed94435fb05d1e2b70124af0a469f73611b7a259cdc6c3c
```

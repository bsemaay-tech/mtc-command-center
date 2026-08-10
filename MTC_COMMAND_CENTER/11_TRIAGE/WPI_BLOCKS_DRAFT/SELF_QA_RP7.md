# SELF-QA - RP7-WPI-RO repair round 6

Status: `SELF-QA-EXECUTED-PENDING-INDEPENDENT-REAUDIT`

Round 6 answers the Codex T0 part-B audit of the round-5 bytes
(`RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md`, BLOCK, four findings) together with the one
executed test recovered from the review the provider interrupted
(`RP7_R5_SALVAGE_FROM_INTERRUPTED_AUDIT_2026-08-10.md`). Everything below ran locally in
**Git Bash (MSYS2)** on the workstation. It made no SSH/SCP call, opened no network
connection, contacted no staging host, minted no RUNID, and changed no repository file
outside the round-6 deliverables. Fixture writes were confined to `mktemp` directories under
`/tmp` whose prefix was checked before recursive removal.

Three findings out of four are byte-grammar defects in which a record the block could not
parse was repaired into one it could, and then adjudicated as host state. Every round-6 arm
therefore feeds the audit's own bytes to the real production predicate and reads the
production result line:

1. **The RED is the audited artefact.** Every arm runs twice - once against the frozen
   round-5 blob, materialised by `git cat-file blob 1143a9ff:...` and re-derived inside the
   fence to 77179 B / `393a16ce...b0ee`, and once against the repaired worktree file. The
   fence asserts both identities, both CR counts and both `bash -n` results before any arm
   runs.
2. **Every finding carries its own no-weakening control.** A repair that turns malformed
   input into a STOP is only correct if well-formed input still reaches the same verdict it
   reached before: column-padded `ss` output must still parse, a real wildcard listener must
   still be a host-state FAIL, `500` must still be a FAIL, `401` must still be a STOP, and
   the four result records the status child really emits must keep their round-5
   dispositions exactly. Those controls are arms, not assertions in prose.
3. **The published command can now fail.** Round 5's could not: each fence invocation was
   followed by a `printf`, so the command returned the `printf` status. That is repaired,
   and the repair is falsified by running the published command over a scratch document
   whose fence bodies exit nonzero.

## Exact command

The command selects each fenced body by the unique markers that open and close that body,
and stops at the closing marker. The marker text inside the command cannot re-open either
range: a marker only matches at the start of a line, and these lines start with `sed`.

Each fence runs under an explicit `timeout` bound of **900 s**, and the command's own rc is
the rc of the fences: any nonzero fence makes the whole command exit nonzero, and a fence
killed at its bound is reported as a distinct `timeout` result rather than as a failure of
the assertions. The **aggregate bound is 2700 s** - three fences at 900 s each, plus the
`--kill-after=30s` grace per fence. The measured run below is far inside it; the bound is
what the command enforces, not what it happened to take.

```bash
# RP7_EXACT_COMMAND_BEGIN
cd /c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r6-fence-body.sh
sed -n '/^# RP7_QA_FENCE_BEGIN$/,/^# RP7_QA_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r5-fence-body.sh
sed -n '/^# RP7_R4_FENCE_BEGIN$/,/^# RP7_R4_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r4-fence-body.sh
sha256sum /tmp/rp7-r6-fence-body.sh /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
wc -c /tmp/rp7-r6-fence-body.sh /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc /tmp/rp7-r6-fence-body.sh; R6=$?
timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc /tmp/rp7-r5-fence-body.sh; R5=$?
timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc /tmp/rp7-r4-fence-body.sh; R4=$?
printf 'R6_FENCE_RC=%s\nR5_FENCE_RC=%s\nR4_FENCE_RC=%s\n' "$R6" "$R5" "$R4"
for rc in "$R6" "$R5" "$R4"; do
  case "$rc" in
    0) ;;
    124) printf 'PUBLISHED_COMMAND_RESULT=timeout per_fence_bound_s=900\n'; exit 124 ;;
    *) printf 'PUBLISHED_COMMAND_RESULT=fence_failed\n'; exit 1 ;;
  esac
done
printf 'PUBLISHED_COMMAND_RESULT=pass fences=3 per_fence_bound_s=900 aggregate_bound_s=2700\n'
# RP7_EXACT_COMMAND_END
```

That block is extractable and runnable by the same mechanism, so a third party never has
to retype it:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

It was executed exactly that way, from a fresh `bash --noprofile --norc`, and produced:

```text
022607b81a89213953b01e5499aad4d2a1aaf4892023c32dc293b191fba0130a */tmp/rp7-r6-fence-body.sh
719077959650f4b5ad4b94c3c122bfe9058ffa469b6c59161e5886271913c9e2 */tmp/rp7-r5-fence-body.sh
94101ef7fdf70d0f4628685811160389227cbba3c10e999e1942e8eb82bb56e0 */tmp/rp7-r4-fence-body.sh
 26681 /tmp/rp7-r6-fence-body.sh
 20050 /tmp/rp7-r5-fence-body.sh
 76710 /tmp/rp7-r4-fence-body.sh
123441 total
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
...
QA_PASS all_assertions=yes
R6_FENCE_RC=0
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=3 per_fence_bound_s=900 aggregate_bound_s=2700
```

All three fences abort with `QA_ASSERT_FAIL` and a nonzero exit on any unexpected result, so
`QA_PASS all_assertions=yes` is reachable only when every assertion in them held - and the
command now reports that failure in its own exit status.

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
| `wpi_alloc_leaf` + `wpi_sha_file` in the round-6 F2 arms | leaf allocation for the status body, which the arm pre-writes, and the body digest, rendered as 64 zeroes | the real `wpi_open_leaf` for every diagnostic leaf, the real single-record reader, the real result grammar, and in the schema arm the real CPython child over the real production body |
| `forge_capture` (all three fences) | the MSYS `env -i`/`timeout` exec plumbing, which rewrites POSIX-looking argv for a native Windows child, plus the Windows CRLF record terminator normalised to the LF a Debian CPython emits | the interpreter the production body **chose** (`a[0]`), the flag words it chose, real CPython, the real embedded driver source, the real digest-bound `verify_lock.py`, real exit codes |
| `wpi_lstat` shim in the finding-2 arms | numeric ownership and object kind, which NTFS cannot express | the production row-19 preflight, the production trusted driver, the production result grammar and the real verifier bytes |
| `rp0_require_safe_component` / `rp0_allocate_evidence_dir` in the finding-5 arms | the two RP0-LIB predicates, which are not present on this workstation, defined as no-op shell **functions** | the whole of `wpi_assert_prerequisites`, including the type check finding 4 introduced and the evidence-root descent check finding 5 introduced |

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

One round-6 arm executes a copy of a published artefact rather than the artefact itself:
the F4 propagation arm runs the exact published command with two substitutions - its `cd`
target, and the `/tmp` prefix of the three fence-body paths so that a nested run cannot
overwrite the body of the run executing it. Both substitutions are asserted in the fence
before the copy runs, and the arm exists precisely because the first version of it, which
retargeted `cd` first and let the `/tmp` rule rewrite the new target, re-entered the real
document and had to be killed. Nothing else about the command is altered.

Not reproducible here, and not claimed: a real bind or overlay mount, and a real
`/proc/<MainPID>/ns/net`. As in rounds 3 and 4, those are falsified by appending to a real
captured `mountinfo` table the exact record such a mount would produce.

**The `verify_lock.py` driven by every parity arm is the real candidate artifact.** The
round-4 fence LF-normalises the worktree copy and asserts its identity before use;
`VERIFIER_IDENTITY` in its transcript records 3735 bytes and `d951e0ee...a451e5`, which is
exactly `WPI_VERIFY_LOCK_SHA256`. The round-5 finding-2 arms feed the same file to the same
production driver.


## The round-6 fence

Five arm groups, each a real RED against the round-5 blob and a real GREEN against the
repaired bytes, plus the no-weakening control in the same group as the repair it guards:

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
| F4 published command | `bash; printf; bash; printf` returns 0 with inner rcs 7 and 9 | the published command returns 1 over failing fence bodies, carries three 900 s bounds, and turns a hanging body into rc 124 |
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
expect_eq green_sha256 "$GREEN_SHA" 6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
expect_eq green_bytes "$GREEN_BYTES" 88460
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
wpi_capture(){ WPI_CAP_OUT="$W/ss.out"; WPI_CAP_ERR="$EV_DIR/capture.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; }
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
f2 ok              'OK fields=8' 0
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
  local label="$1"; shift; local -a a=("$@"); local i exe
  CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/forge.$CALL.out"; WPI_CAP_ERR="$EV_DIR/forge.$CALL.err"
  WPI_CAP_RC=0; : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"
  exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
  for ((i=1; i<${#a[@]}; i++)); do
    case "${a[$i]}" in /*) [ ! -e "${a[$i]}" ] || a[$i]="$(cygpath -w "${a[$i]}")";; esac
  done
  /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
  tr -d '\r' < "$EV_DIR/raw.out" > "$WPI_CAP_OUT"; tr -d '\r' < "$EV_DIR/raw.err" > "$WPI_CAP_ERR"
}
wpi_capture(){
  if [ "$1" = status_json ]; then forge_capture "$@"
  else WPI_CAP_OUT="$EV_DIR/$1.out"; WPI_CAP_ERR="$EV_DIR/$1.err"; : > "$WPI_CAP_ERR"; printf '200\n' > "$WPI_CAP_OUT"; WPI_CAP_RC=0
       printf '{"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}' > "$EV_DIR/ro.status.body"; fi
}
wpi_alloc_leaf(){ :; }
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
wpi_capture(){ WPI_CAP_OUT="$EV_DIR/code.out"; WPI_CAP_ERR="$EV_DIR/code.err"; printf '%s\n' "$CODE" > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0; }
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

BOUNDS=$(grep -c 'timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc' "$Q/published.txt")
DOCBOUND=$(grep -c 'aggregate bound' "$DOC")
printf 'PUBLISHED_BOUND timeout_wrappers=%s documented_aggregate_bound_mentions=%s\n' "$BOUNDS" "$DOCBOUND"
expect_rc f4_bound_wrappers "$BOUNDS" 3
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
wpi_capture leaf_race /usr/bin/printf 'CAPTURED\n'
rc=$?
printf 'LEAF_RACE rc=%s outside_text=%s outside_bytes=%s payload_left_the_tree=%s\n' \
  "$rc" "$(tr -d '\n' < "$OUTSIDE")" "$(wc -c < "$OUTSIDE")" \
  "$(grep -q CAPTURED "$OUTSIDE" && echo yes || echo no)"
ARM
bash --noprofile --norc "$Q/f5_arm.sh" "$RED"   "$Q/f5-red"   > "$Q/f5-red.txt" 2>&1
bash --noprofile --norc "$Q/f5_arm.sh" "$GREEN" "$Q/f5-green" > "$Q/f5-green.txt" 2>&1
sed 's/^/RED   /' "$Q/f5-red.txt"; sed 's/^/GREEN /' "$Q/f5-green.txt"
expect_has f5_red_escapes    'LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes' "$Q/f5-red.txt"
expect_has f5_green_confined 'LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no' "$Q/f5-green.txt"

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
QA_ROOT=/tmp/rp7-r6-qa.HT8l8W
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=77179 red_sha256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee red_cr=0 red_bash_n=0 green_bytes=88460 green_sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709 green_cr=0 green_bash_n=0
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
GREEN STATUS_RECORD rec=[OK fields=8] child_rc=0 rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site] stderr_bytes=0
STATUS_SCHEMA mutated=no rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=00000000000000000000000000000000000000000000] child=[OK fields=8]
STATUS_SCHEMA mutated=yes rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=000000] child=[PARSE schema_declaration_mismatch]
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
GREEN dc4eac6b791d148fe12b95e51bf31a92ead1c32f9dde48255f263a0d28dbcb4f */tmp/rp7-r6-qa.HT8l8W/fake/body-r6-fence-body.sh
GREEN def46450e739e132ca3b14d87e783aec6d75a838316dc78d6d24fbecb302cb81 */tmp/rp7-r6-qa.HT8l8W/fake/body-r5-fence-body.sh
GREEN 585c97d2fcbe0bc2e3fbca0f841e68a26934c5434ed00a8a691a4919dd85f82f */tmp/rp7-r6-qa.HT8l8W/fake/body-r4-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.HT8l8W/fake/body-r6-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.HT8l8W/fake/body-r5-fence-body.sh
GREEN  47 /tmp/rp7-r6-qa.HT8l8W/fake/body-r4-fence-body.sh
GREEN 141 total
GREEN R6_FENCE_RC=7
GREEN R5_FENCE_RC=9
GREEN R4_FENCE_RC=0
GREEN PUBLISHED_COMMAND_RESULT=fence_failed
PUBLISHED_RC_PROPAGATION round6_command_rc=1 substitutions=2
PUBLISHED_BOUND timeout_wrappers=3 documented_aggregate_bound_mentions=2
PUBLISHED_BOUND_ENFORCED scaled_bound_s=3 rc=124 wall_s=3
RED   LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes
GREEN LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no
LEAF_WRITE_STATIC red_name_appends=12 green_name_appends=0 red_open_leaf=0 green_open_leaf=1
QA_PASS all_assertions=yes
R6_FENCE_RC=0
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
  shell-side write in the repaired block re-opens a leaf by name.

## The carried round-5 fence, re-run as a regression gate

The round-5 fence is reproduced below **unchanged except for the two GREEN identity
constants**, which name the subject file by hash and byte count and therefore have to name
the round-6 bytes. Everything else - every arm, every assertion, both anchor comments and
the RED blob at `d6a976aa` - is byte-identical to round 5. It is one half of the
no-weakening gate: every round-5 repair (the tenth tool binding, package identity, the
three `/dev/null` opens, evidence-root provenance) must still hold on these bytes, and does.

Ten arm groups, each a real RED against the round-4 blob and a real GREEN against the
repaired bytes:

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
expect_eq green_sha256 "$GREEN_SHA" 6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
expect_eq green_bytes "$GREEN_BYTES" 88460
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
  local label="$1"; shift; local -a a=("$@"); local i exe
  CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/forge.$CALL.out"; WPI_CAP_ERR="$EV_DIR/forge.$CALL.err"
  WPI_CAP_RC=0; : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"
  exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
  for ((i=1; i<${#a[@]}; i++)); do
    case "${a[$i]}" in /*) [ ! -e "${a[$i]}" ] || a[$i]="$(cygpath -w "${a[$i]}")";; esac
  done
  /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
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
# (c) executed: wpi_alloc_leaf keeps create-once semantics and still leaks no
#     diagnostic, with stderr CLOSED instead of redirected to /dev/null.
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
( wpi_alloc_leaf "$EV_DIR/leaf" ) > "$W/a1.out" 2> "$W/a1.err"; rc1=$?
( wpi_alloc_leaf "$EV_DIR/leaf" ) > "$W/a2.out" 2> "$W/a2.err"; rc2=$?
( wpi_alloc_leaf "$W/outside" )   > "$W/a3.out" 2> "$W/a3.err"; rc3=$?
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
QA_ROOT=/tmp/rp7-r5-qa.tB0r92
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 git=2.52.0.windows.1 uid_gid=4096:4096
BYTE_IDENTITY red_bytes=70941 red_sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad red_cr=0 red_bash_n=0 green_bytes=88460 green_sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709 green_cr=0 green_bash_n=0
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
ALLOC_LEAF rc_first=0 rc_second=3 rc_outside=3 err1=0 err2=0 err3=0 second_stdout=[RP7_STOP reason=capture_leaf_not_create_once leaf=/tmp/rp7-r5-qa.tB0r92/f4-leaf/ev/leaf] outside_stdout=[RP7_STOP reason=capture_path_outside_evidence leaf=/tmp/rp7-r5-qa.tB0r92/f4-leaf/outside ev_dir=/tmp/rp7-r5-qa.tB0r92/f4-leaf/ev]
EV_ROOT_CONSTANT red=0 green=1
EV_ROOT pin=[keep] ev_dir=[/tmp/rp7-r5-qa.tB0r92/other/x] rc=0 stderr_bytes=0 stdout=[]
EV_ROOT pin=[keep] ev_dir=[/tmp/rp7-r5-qa.tB0r92/other/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT]
EV_ROOT pin=[/tmp/rp7-r5-qa.tB0r92/base] ev_dir=[/tmp/rp7-r5-qa.tB0r92/base/evidence/runkit/RUN-RO] rc=0 stderr_bytes=0 stdout=[]
EV_ROOT pin=[/tmp/rp7-r5-qa.tB0r92/base] ev_dir=[/tmp/rp7-r5-qa.tB0r92/other/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=/tmp/rp7-r5-qa.tB0r92/other/x expected_root=/tmp/rp7-r5-qa.tB0r92/base]
EV_ROOT pin=[/tmp/rp7-r5-qa.tB0r92/base] ev_dir=[/tmp/rp7-r5-qa.tB0r92/base-evil/x] rc=3 stderr_bytes=0 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=/tmp/rp7-r5-qa.tB0r92/base-evil/x expected_root=/tmp/rp7-r5-qa.tB0r92/base]
QA_PASS all_assertions=yes
R5_FENCE_RC=0
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

The round-4 fence is reproduced below **unchanged except for the two anchor comments**, and
was re-executed against the repaired bytes. It is the no-weakening gate for this round:
every round-3 and round-4 arm - the two real `python -m venv` forging environments, the
projection-v2 attacks, the two-phase listener parse, the row grammar, the `-S` guard, the
tool-attestation disclosure, the timeout-inside-cleared-environment ordering - must still
reach `QA_PASS` on the round-5 bytes, and does.

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
# ---------------------------------------------------------------------------
cat > "$Q/r3-mutants.sh" <<'R3MUTANTS_EOF'
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
    local label="$1"; shift; local -a a=("$@"); local i exe; CALL=$((CALL+1))
    WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; : > "$WPI_CAP_OUT"
    case "$label" in
        status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '%s\n' "$BODY_JSON" > "$EV_DIR/ro.status.body"; return 0 ;;
        sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT"; return 0 ;;
    esac
    exe="${a[0]}"; [ -x "$exe" ] || exe="$exe.exe"
    for ((i=1; i<${#a[@]}; i++)); do
        case "${a[$i]}" in /*) if [ -e "${a[$i]}" ]; then a[$i]="$(cygpath -w "${a[$i]}")"; fi ;; esac
    done
    /usr/bin/timeout 30 "$exe" "${a[@]:1}" > "$EV_DIR/raw.out" 2> "$EV_DIR/raw.err" || WPI_CAP_RC=$?
    tr -d '\r' < "$EV_DIR/raw.out" > "$WPI_CAP_OUT"
    tr -d '\r' < "$EV_DIR/raw.err" > "$WPI_CAP_ERR"
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
    "$nosstatus" "$(grep -c 'detail=strict_json_or_parser_failure parser_rc=3 ' "$Q/nos-status.log")"
expect_rc nos_parity_rc "$nosparity" 3
expect_rc nos_parity_refused "$(grep -c 'verifier_not_evaluable rc=4 detail=trusted_startup_unproven$' "$Q/nos-parity.log")" 1
expect_rc nos_status_rc "$nosstatus" 3
expect_rc nos_status_refused "$(grep -c 'detail=strict_json_or_parser_failure parser_rc=3 ' "$Q/nos-status.log")" 1

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
        wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; cp "$table" "$WPI_CAP_OUT"; }
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
    wpi_capture(){ printf 'PRODUCTION_SS_ARGV=%s\n' "$*"; WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; }
    wpi_assert_listener_set
); listenergreen=$?
(
    EV_DIR="$Q/ev-listener-addr"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 10.0.0.5:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; }
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
    wpi_capture(){ CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; if [ "$CALL" -eq 1 ]; then printf 'net:[100]\n' > "$WPI_CAP_OUT"; else printf 'net:[200]\n' > "$WPI_CAP_OUT"; fi; }
    wpi_assert_netns_binding
); netns=$?
(
    EV_DIR="$Q/ev-http"; mkdir -p "$EV_DIR"; WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=0; printf '500\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
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
QA_ROOT=/tmp/rp7-r4-qa.vEBNeC
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 python=3.14.2 uid_gid=4096:4096 live_mountinfo_records=4 symlinks=not_representable_msys2
REAL_GNU_DIAGNOSTIC=[/usr/bin/stat: cannot stat '/tmp/rp7-r4-qa.vEBNeC/absent-leaf': No such file or directory]
REAL_GNU_ABSENT kind=absent child_rc=1
DIAG_ACCEPTED id=abs_statx kind=absent
DIAG_ACCEPTED id=abs_stat kind=absent
DIAG_ACCEPTED id=abs_oserr kind=absent
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-diag-base_statx/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-diag-base_stat/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-diag-base_oserr/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-diag-foreign/ro.0001.lstat.stderr
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
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-fail-mutant/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-fail-mutant/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=fixture_deviation
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-fail-green/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-fail-green/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-fail-green/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-fail-green/ro.0008.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
MOUNT_WINDOW_CLOSED
B3_FAIL reason=fixture_deviation
FAIL_GUARD_CLOSE mutant_rc=1 mutant_window_closed=0 production_rc=1 production_window_closed=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-guard-attest/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-guard-changed/ro.0002.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=5 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=5 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/n1-decoy projection=/tmp/rp7-r4-qa.vEBNeC/ev-guard-changed/ro.0006.mount_projection.tsv sha256=74a1831126d71500bb26b663bc0923e5714679858bcb3d8c8bfa6898897a23e2 content=not_printed
RP7_STOP reason=mount_topology_changed before=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 after=74a1831126d71500bb26b663bc0923e5714679858bcb3d8c8bfa6898897a23e2 format=normalised_path_projection_v2
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-guard-mismatch/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-guard-mismatch/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_STOP reason=mount_topology_mismatch observed=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 attested=0000000000000000000000000000000000000000000000000000000000000000 format=normalised_path_projection_v2
MOUNT_GUARD_RCS changed_downgrade=3 attestation_mismatch=3
B3_STOP reason=structured_path_unparseable source=find_stdout detail=unsafe_character
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-space/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-space/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-space/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-space/ro.0012.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=[unrenderable] path_sha256=565603d319c5019948e7655e2da5b2f006639a9ad9d087d2ed6cba5a41948f2e count=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-realfind/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-realfind/ro.0003.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=21 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r4-qa.vEBNeC/ev-realfind/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r4-qa.vEBNeC/ev-realfind/ro.0013.mount_projection.tsv sha256=2e6b24b88ee4353f8eb93831f1ead7c2ef56b78e698c4c5cd47980680e91d359 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=/tmp/rp7-r4-qa.vEBNeC/imm/sub count=2
UNSAFE_PATH_RCS mutant_stop=3 suppressed_render_fail=1 real_find_fail=1
MUTANT_RP7_tool name=stat path=/tmp/rp7-r4-qa.vEBNeC/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute
RP7_tool name=stat path=/tmp/rp7-r4-qa.vEBNeC/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=readlink path=/tmp/rp7-r4-qa.vEBNeC/tools/readlink owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=env path=/tmp/rp7-r4-qa.vEBNeC/tools/env owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=find path=/tmp/rp7-r4-qa.vEBNeC/tools/find owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=sha256sum path=/tmp/rp7-r4-qa.vEBNeC/tools/sha256sum owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=systemctl path=/tmp/rp7-r4-qa.vEBNeC/tools/systemctl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=ss path=/tmp/rp7-r4-qa.vEBNeC/tools/ss owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=curl path=/tmp/rp7-r4-qa.vEBNeC/tools/curl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=timeout path=/tmp/rp7-r4-qa.vEBNeC/tools/timeout owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=python3 path=/tmp/rp7-r4-qa.vEBNeC/tools/python3 owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
TOOL_ATTESTATION mutant_rc=0 mutant_attestation_fields=0 production_rc=0 self=4 bound_instrument=6 self_names=stat,env,sha256sum,timeout,
RP7_STOP reason=tool_not_evaluable tool=python3 detail=path_metadata_mismatch path=/tmp/rp7-r4-qa.vEBNeC/tools/python3 kind=symlink mode=755 owner_numeric=0:0 expected=regular,any,0:0
TRUSTED_PYTHON_PIN symlinked_pin_rc=3 symlink_rejected=1
REAL_CHARDEV raw=[character special file] token=[other]
MUTANT_B3_STOP reason=path_not_evaluable path=/ detail=root_kind_character special file
MUTANT_B1_STOP reason=interpreter_object_unbound kind=character special file target=none
B3_STOP reason=path_not_evaluable path=/ detail=root_kind_other
B1_STOP reason=interpreter_object_unbound kind=other target=none
KIND_TOKEN_RCS real_chardev=0 root_kind_stop=3 interpreter_kind_stop=3 root_token_ok=1 interpreter_token_ok=1
TIMEOUT_ENV mutant_marker=1 mutant_vars=103 production_marker=0 production_vars=10
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=8 elapsed_ms=8070 budget_s=2
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=2 elapsed_ms=2180 budget_s=2
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=9 production_wall_s=2 budget_s=2 child_sleep_s=8
B1_interpreter path=/tmp/rp7-r4-qa.vEBNeC/venv/bin/python object=non_symlink_regular preexec_binding=component_and_mount_window_closed exec_binding=separate_bounded_exec version_family=3.12 env=cleared isolated=yes
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy/target
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok
INTERPRETER_RCS regular_pass=0 symlink_stop=3 cr_stop=3 cr_forged_lines=0 cr_single_sanitised_line=1
FORGE_FIXTURES venv_rc=0,0 pth=[import os,sys; open(r"C:\Users\BARSEM~1\AppData\Local\Temp\rp7-r4-qa.vEBNeC\pth.marker","w").write("1"); sys.stdout.write("OK fields=8"+chr(10)); sys.stdout.flush(); os._exit(0)] sitecustomize_lines=5
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
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
NO_SITE_GUARD parity_rc=3 parity_refused=1 status_rc=3 status_refused=1
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
B6_listener_inventory rows=2 port_8790_rows=1 bytes=70 evidence_file=/tmp/rp7-r4-qa.vEBNeC/ss-wccomplete-green/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_listener_inventory rows=2 port_8790_rows=1 bytes=72 evidence_file=/tmp/rp7-r4-qa.vEBNeC/ss-good-green/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
LISTENER_ORDER red_wildcard_first_rc=1 red_malformed_first_rc=3 green_wildcard_first_rc=3 green_malformed_first_rc=3 expected_both_stop=3
LISTENER_COMPLETE_TABLE wildcard_fail_rc=1 good_rc=0 inventory_before_verdict=1
B1_metadata_universe root=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages entries=3 dist_info_dirs=2 non_metadata_entries=1 enumeration=unfiltered_maxdepth_1 universe=explicit_dist_info_only
B1_metadata_preflight root=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages dist_info_dirs=2 complete=yes readable=yes
B1_metadata_preflight root=/tmp/rp7-r4-qa.vEBNeC/f3-egg/venv/lib/python3.12/site-packages dist_info_dirs=2 complete=yes readable=yes
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-egg/venv/lib/python3.12/site-packages/ghost.egg-info format=egg_info
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-pth/venv/lib/python3.12/site-packages/evil.pth format=pth
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-hook/venv/lib/python3.12/site-packages/sitecustomize.py format=startup_hook
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-zip/venv/lib/python3.12/site-packages/wheelhouse.zip format=zip
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-filedi/venv/lib/python3.12/site-packages/broken-1.0.dist-info format=dist_info_kind_regular
B1_FAIL reason=distribution_metadata_absent path=/tmp/rp7-r4-qa.vEBNeC/f3-absent/venv/lib/python3.12/site-packages/gone-1.0.dist-info/METADATA
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f3-unread/venv/lib/python3.12/site-packages/demo_pkg-1.0.dist-info/METADATA rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/f3-ev-t09/ro.0049.lstat.stderr
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info detail=dist_info_kind_character special file
B1_STOP reason=metadata_universe_unexpected stage=preflight path=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info format=dist_info_kind_other
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info/METADATA detail=kind_character special file
B1_STOP reason=metadata_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f3-clean/venv/lib/python3.12/site-packages/other-2.5.dist-info/METADATA detail=kind_other
METADATA_UNIVERSE_RCS clean=0 egg_red=0 egg_green=3 pth=3 hook=3 zip=3 dist_info_file=3 member_absent=1 member_unreadable=3 chardev_dir_red=3 chardev_dir=3 chardev_member_red=3 chardev_member=3
B1_STOP reason=metadata_universe_unexpected stage=verifier format=egg_info name_sha256=cf1057a30e78603c62e83b18e1c5697aca2bfeac81a18a4707b550f2e8b99132
B1_STOP reason=metadata_universe_unexpected stage=verifier format=startup_hook name_sha256=1dc3332b767b1b60ea953e5dfdd81df90bf3449d9c313c945bbdb29e78f45ff8
B1_lock_parity result=pass packages=2 output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe
DRIVER_UNIVERSE egg_rc=3 hook_rc=3 clean_rc=0
B5B6_DECLARED_ORDER wpi_assert_netns_binding,wpi_assert_status,wpi_assert_listener_set,
B6_netns caller=net:[100] service=net:[100] mainpid=189813 binding=equal
B6_listener_inventory rows=1 port_8790_rows=1 bytes=37 evidence_file=/tmp/rp7-r4-qa.vEBNeC/order-red/3.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790
B6_netns caller=net:[100] service=net:[100] mainpid=189813 binding=equal
B5_FAIL reason=status_endpoint_unexpected_http code=500
TWO_DEVIATION red_rc=1 red_first_result=[B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790] green_rc=1 green_first_result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
B1a_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/requirements.lock rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/f5-ev-r17unread_red/ro.0023.lstat.stderr
B1a_STOP reason=installed_lock_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/requirements.lock rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/f5-ev-r17unread/ro.0023.lstat.stderr
B1_STOP reason=path_not_evaluable path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/f5-ev-r19aunread_red/ro.0027.lstat.stderr
B1_STOP reason=verifier_unreadable path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/f5-ev-r19aunread/ro.0027.lstat.stderr
B1a_FAIL reason=installed_lock_object_unexpected path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/requirements.lock kind=directory
B1a_FAIL reason=installed_lock_object_unexpected kind=directory
B1a_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/requirements.lock kind=regular mode=644 owner_numeric=1000:1000 expected=regular,any,0:0
B1a_FAIL reason=installed_lock_owner_unexpected owner_numeric=1000:1000 expected=0:0
B1_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py kind=regular mode=644 owner_numeric=1000:1000 expected=regular,any,0:0
B1_FAIL reason=verifier_owner_unexpected path=/tmp/rp7-r4-qa.vEBNeC/f5/release/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py owner_numeric=1000:1000 expected=0:0
ROW_GRAMMAR_RCS r17_unread_red=3 r17_unread=3 r19a_unread_red=3 r19a_unread=3 r17_kind_red=1 r17_kind=1 r17_owner_red=1 r17_owner=1 r19a_owner_red=1 r19a_owner=1
MUTANT_MOUNT_POINT=/mnt/*
RP7_mount_table parsed=yes records=1 content=not_printed
PRODUCTION_MOUNT_POINT=/mnt/* GLOB_PARSE_RC=0
B5_STOP reason=mutant_wrong_type_classification B5 flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
B5_STOP reason=schema_unexpected field=state_version
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
MUTANT_SS_ARGV=listeners /usr/bin/ss -H -ltn sport = :8790
PRODUCTION_SS_ARGV=listeners /usr/bin/ss -H -ltn
B6_listener_inventory rows=2 port_8790_rows=1 bytes=72 evidence_file=/tmp/rp7-r4-qa.vEBNeC/ev-listener-green/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
B6_listener_inventory rows=1 port_8790_rows=1 bytes=37 evidence_file=/tmp/rp7-r4-qa.vEBNeC/ev-listener-addr/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790
LISTENER_RCS mutant_filtered=0 production_full_inventory=0 non_preregistered_address=1
RP7_STOP reason=system_manager_unreachable rc=5 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-manager/ro.0001.system_manager.stderr
B3_STOP reason=walk_incomplete root=/fixture rc=1 detail=diagnostic_captured diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-partial/ro.0001.partial.stderr partial_stdout_discarded=/tmp/rp7-r4-qa.vEBNeC/ev-partial/ro.0001.partial.stdout
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_STOP reason=verifier_not_evaluable rc=1 detail=unclassified_verifier_result diagnostic_file=/tmp/rp7-r4-qa.vEBNeC/ev-parity-stop/err
B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]
B5_FAIL reason=status_endpoint_unexpected_http code=500
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
BASH_N_RC=0 BYTES=88460 SHA256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
QA_PASS all_assertions=yes
R4_FENCE_RC=0
```

Its final line re-derives the round-5 identity from inside the round-4 fence:
`BASH_N_RC=0 BYTES=77179 SHA256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`.

Two lines in that transcript now read differently from round 4 and are expected to:
`TOOL_ATTESTATION ... self=4 bound_instrument=6` still holds because the attestation
vocabulary did not change, and `V2_TRUSTED_PYTHON_POINT` still shows the trusted
interpreter as a projection point. What changed in the block is *where* that interpreter is
bound, which the round-4 fence never observed - that is what the round-5 F1 arm is for.

### Literal re-run of the published command against this document

The published command was executed verbatim **three** times: once to produce the transcripts
above (214 s), once after they had been pasted in (186 s), and once more against **this file
as delivered**, after the last prose edit (179 s). Every run returned rc 0 with empty stderr
and 38464 stdout bytes; all three fences printed `QA_PASS all_assertions=yes`
(`R6_FENCE_RC=0`, `R5_FENCE_RC=0`, `R4_FENCE_RC=0`) followed by the command's own summary
line `PUBLISHED_COMMAND_RESULT=pass fences=3 per_fence_bound_s=900 aggregate_bound_s=2700`;
and every run re-derived the same three fence-body digests and byte counts
(`022607b8...0130a` / 26681 B, `71907795...3c9e2` / 20050 B, `94101ef7...56e0` / 76710 B).
Pasting transcripts and editing prose changed no byte inside any marker range, which is why
the digests are stable across all three runs. The longest run is an order of magnitude inside
the enforced 900 s per-fence bound.

A diff of the recorded run against the final one, ignoring the `mktemp` scratch names, is
confined to two lines, and they are the only non-deterministic outputs in the suite - the
measured wall clock of the budget arm: `elapsed_ms=2180` versus `2050` and `mutant_wall_s=9`
versus `8`. Every rc, digest, reason token and result line is identical. (The second run
differed in one further line, a round-4 fixture path that embeds its own Windows scratch
directory name.)

## What this QA does not establish

- No accepting `wpi_validate_inputs` arm exists and none can exist before freeze: three
  freeze-gate constants (`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
  `WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_EVIDENCE_ROOT`) are still `<PIN-AT-FREEZE>` and
  deliberately refuse the accepting arm until the deploy channel supplies them.
- **The status body leaf is written by name, not by descriptor.** Every other shell-side
  write in the block goes through the descriptor its `O_CREAT|O_EXCL` open returned, which is
  what the round-6 F5 arm measures. `curl --output <path>` is handed a name, so the one leaf
  this block cannot bind that way is `ro.status.body`: it is create-once allocated and then
  opened again, by name, by curl. Substituting that name between the two steps is the same
  route the recovered test demonstrated for the capture leaves, and it is not closed for this
  leaf. Closing it needs a curl invocation that writes to an inherited descriptor, which is a
  design change, not a repair.
- **Readers re-open by name.** The write side is bound to the created object; the read side
  (`wpi_single_record`, the listener reader, `wpi_require_empty_file`, `wpi_sha_file`) opens
  the leaf path again after the child has run. A concurrent writer with write access to
  `EV_DIR` could therefore still present a different object to the reader. What the block
  establishes about that content is only what its record grammar establishes - which is why
  every reader STOPs on a record it cannot parse rather than adjudicating it. A per-capture
  `/proc/self/fd` identity re-check was considered and rejected: it makes every capture spawn
  a second capture to stat the first, which is recursive, and doubles both the child count
  and the leaf count. Reading through a descriptor opened at creation is the real fix and is
  a signature change to every reader in the block.
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

# BLOCK: 4

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh independent T0 flagship slot.
This was a local audit only. No host contact, network, SSH/SCP, RUNID, service,
credential, deployment, trading, or commit action occurred.

The round-6 subject identity is exact and the four named round-5 examples are
substantially repaired: the published fence turns the prior listener NUL/address/port
cases into STOPs, malformed `TYPE`/`MISMATCH` records into STOPs, `000`/`099`/`600`
into STOPs, and preserves the required padded-listener, wildcard, `500`, `401`, and
four real status-result dispositions. The leaf descriptor repair also binds a
shell-side write to the object its create-once open created.

The band is nevertheless non-accepting. The common single-record reader still deletes
NUL bytes and normalises malformed row-20, row-21, and row-22 records into accepting
ones; the listener parser accepts nonnumeric queue fields; the row-22 draft claims
captured/adjudicated byte equality that its disclosed reader-by-name residual does not
establish; and the published command's timeout classification and 2700-second aggregate
claim are false.

## Row results

| Row | Result | Executed/read evidence |
|---|---|---|
| **20 - B5 endpoint** | **FAIL** | Exact controls held: `000`/`099`/`600` STOP, `500` FAIL, `401` STOP. But `2<NUL>00\n` is normalised by `wpi_single_record` into `200`; with an `OK` parser result the block prints the accepting `B5_status` line at rc 0 (finding 1). |
| **21 - B5 flags** | **FAIL** | The exact truncated/invented round-5 cases now STOP and the real `OK`/`TYPE`/`MISMATCH`/`MISSING` dispositions are preserved. But `O<NUL>K fields=8\n` is normalised into `OK fields=8` and reaches accepting `B5_status`, rc 0 (finding 1). |
| **22 - netns/listener set** | **FAIL** | The original listener NUL/address/port cases now STOP; padded columns still PASS; wildcard still FAILs; `bytes=` equals an independent `wc -c` for the clean controls. However `ne<NUL>t:[100]` becomes `net:[100]` and passes namespace binding; queue fields `:` and `12:34` both reach complete listener PASS; and a post-capture path replacement can make the adjudicated bytes differ from the child's captured bytes while still PASSing (findings 1-3). |
| **23 - no wildcard** | **FAIL (inherited from row 22)** | A real wildcard remains a truthful `B6_FAIL reason=nonloopback_listener`, but row 23 is conditioned on row 22's complete structural parse. The queue-grammar false PASS and the reopen-by-name substitution mean that precondition is not established. |
| **24 - external closed** | **PASS** | `B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no reason=network_domain_separation` remains a boundary record only; `RP7_claim does_not_establish` names `row_24_operator_side_result`. |

## Evidence/QA and leaf-binding results

| Check | Result | Evidence |
|---|---|---|
| Subject/predecessor identity | **PASS** | Current: 88460 B, SHA-256 `6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709`, 0 CR bytes, `bash -n` rc 0. Predecessor was materialised only with `git cat-file blob '1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'`: blob `0b743084267c419737ba030f339d938e77bf09a3`, 77179 B, SHA-256 `393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 0 CR bytes, `bash -n` rc 0. |
| Published command on good fences | **PASS** | Executed exactly as published from `WPI_BLOCKS_DRAFT`; rc 0 in 209.9 s. All three fence hashes/byte counts matched; all printed `QA_PASS all_assertions=yes`; final rcs were `0,0,0`. |
| Published command on a failing fence | **PASS** | A scratch copy with one fence `exit 7` and only the documented path retargeting returned rc 1, printed `R6_FENCE_RC=7`, and printed `PUBLISHED_COMMAND_RESULT=fence_failed`. |
| Timeout/aggregate contract | **FAIL** | A TERM-ignoring fence reaches the kill-after arm and returns 137, which the published case statement labels `fence_failed`, not `timeout`. Three sequential `900s` bounds each carry 30 s kill grace: `3*(900+30)=2790`, not 2700, and there is no aggregate wrapper (finding 4). |
| Shell-side leaf write binding | **PASS for the narrowed write claim** | `wpi_open_leaf` keeps the fd returned by the noclobber create and all non-status-body shell writes use it. The verbatim fence reproduced `LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes` on the predecessor and `LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no` on round 6. |
| Disclosed residual 1 | **Accurate** | `ro.status.body` is allocated create-once, then `curl --output <path>` re-opens the name. Round 6 does not close this route and does not claim it closed. |
| Disclosed residual 2 | **Accurate as a limitation, but inconsistent with row 22** | Readers re-open names. The disclosure is honest, but draft row 22 simultaneously says the adjudicated byte string *is* the captured byte string. The executed replacement fixture proves that stronger sentence false (finding 3). |

## Baseline identity commands and output

Current identity, command rc 0:

```powershell
$p = 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
$bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $p))
$hash = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
$cr = ($bytes | Where-Object { $_ -eq 13 }).Count
"SHA256=$hash"
"BYTES=$($bytes.Length)"
"CR_BYTES=$cr"
bash -n 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
"BASH_N_RC=$LASTEXITCODE"
```

```text
SHA256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
BYTES=88460
CR_BYTES=0
BASH_N_RC=0
```

Predecessor materialisation/identity, executed under a fresh
`bash --noprofile --norc` in a checked `mktemp -d` tree, command rc 0:

```bash
git cat-file blob '1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh' > "$Q/predecessor.sh"
git rev-parse '1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
sha256sum "$Q/predecessor.sh"
wc -c "$Q/predecessor.sh"
LC_ALL=C tr -cd '\r' < "$Q/predecessor.sh" | wc -c
bash -n "$Q/predecessor.sh"
```

```text
PREDECESSOR_BLOB_OID=0b743084267c419737ba030f339d938e77bf09a3
PREDECESSOR_SHA256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee
PREDECESSOR_BYTES=77179
PREDECESSOR_CR_BYTES=0
PREDECESSOR_BASH_N_RC=0
```

Every multi-line fixture below was passed byte-for-byte to a fresh inner Bash with:

```powershell
$test | & 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -c 'tail -c +4 | bash --noprofile --norc -s'
```

`tail -c +4` removes only the PowerShell UTF-8 BOM before the fresh inner shell reads
stdin. Every fixture allocated a checked `mktemp -d /tmp/rp7-r6-audit-*.XXXXXX`
tree and removed it. The three fixed `/tmp/rp7-r[456]-fence-body.sh` leaves created
by the verbatim published command were also removed after the evidence tests.

## Findings

### 1. The common single-record reader normalises NUL-bearing B5/B6 records into accepting observations - HIGH

**Locations:** `RP7-WPI-RO.sh:294-310`, called for netns at `:1113,:1117`, HTTP
status at `:1313`, and parser result at `:1364`; draft rows 20-22 at
`WPI_PREREGISTRATION_DRAFT.md:701-703`.

`wpi_single_record` uses Bash `read`, which silently discards NUL, and performs no
byte-preserving preflight like the new listener reader. Consequently:

- `2<NUL>00\n` becomes a valid `200` status;
- `O<NUL>K fields=8\n` becomes the parser's accepting record; and
- `ne<NUL>t:[100]\n` becomes a valid namespace identity.

This is Pattern 13: a byte admitted by capture has no terminal disposition and vanishes
before grammar. It leaves the broad round-5 findings 2 and 3 unclosed, even though their
published non-NUL examples are repaired.

Exact comparative command (the arm sources either the `git cat-file blob` predecessor
or the current file, stubs only the child capture, and drives the real production reader
and adjudicator):

```bash
GREEN=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r6-audit-nul-redgreen.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-r6-audit-nul-redgreen.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
git cat-file blob '1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh' > "$Q/red.sh"
cat > "$Q/arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/false; WPI_PYTHON3=/usr/bin/python3
WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
WPI_READLINK=/usr/bin/false; WPI_MAINPID=123
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
wpi_capture(){
 local label="$1"
 WPI_CAP_OUT="$W/$label.out"; WPI_CAP_ERR="$W/$label.err"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
 case "$label:$mode" in
  status_get:code_nul) printf '2\00000\n' > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
  status_json:code_nul) printf 'OK fields=8\n' > "$WPI_CAP_OUT" ;;
  status_get:record_nul) printf '200\n' > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
  status_json:record_nul) printf 'O\000K fields=8\n' > "$WPI_CAP_OUT" ;;
  caller_netns:netns_nul) printf 'ne\000t:[100]\n' > "$WPI_CAP_OUT" ;;
  service_netns:netns_nul) printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
  *) exit 96 ;;
 esac
}
case "$mode" in
 code_nul|record_nul) wpi_assert_status ;;
 netns_nul) wpi_assert_netns_binding ;;
esac
ARM
printf 'RED_SHA256=%s GREEN_SHA256=%s\n' \
 "$(sha256sum "$Q/red.sh" | cut -d ' ' -f1)" \
 "$(sha256sum "$GREEN" | cut -d ' ' -f1)"
for mode in code_nul record_nul netns_nul; do
  for subject in red green; do
    [ "$subject" = red ] && S="$Q/red.sh" || S="$GREEN"
    bash --noprofile --norc "$Q/arm.sh" "$S" "$Q/$mode-$subject" "$mode" \
      > "$Q/$mode-$subject.txt" 2>&1; rc=$?
    printf 'NUL_RED_GREEN mode=%s subject=%s rc=%s result=[' "$mode" "$subject" "$rc"
    tr '\n' ' ' < "$Q/$mode-$subject.txt"; printf ']\n'
  done
done
```

Outer command rc 0; each driven subject rc was 0. Observed output:

```text
RED_SHA256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee GREEN_SHA256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
NUL_RED_GREEN mode=code_nul subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site ]
NUL_RED_GREEN mode=code_nul subject=green rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site ]
NUL_RED_GREEN mode=record_nul subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site ]
NUL_RED_GREEN mode=record_nul subject=green rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site ]
NUL_RED_GREEN mode=netns_nul subject=red rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
NUL_RED_GREEN mode=netns_nul subject=green rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
```

Independent byte dumps on the current subject were
`320030300a` (`2<NUL>00\n`), `4f004b206669656c64733d380a`
(`O<NUL>K fields=8\n`), and `6e6500743a5b3130305d0a`
(`ne<NUL>t:[100]\n`).

**Required repair:** make every use of `wpi_single_record` byte-preserving before Bash
can delete NUL (and account for every captured byte). NUL or any other unrepresentable
record must STOP before status, parser-result, or namespace semantics. Add real
predecessor/current RED/GREEN arms for all three records above.

### 2. Nonnumeric listener queue fields reach a complete accepting listener set - HIGH

**Locations:** `RP7-WPI-RO.sh:1260-1266`, especially `:1265`; draft row 22 at
`WPI_PREREGISTRATION_DRAFT.md:703`.

The parser validates the combined string `"$recvq:$sendq"` against a class that permits
digits and colon. It never requires *each* queue field to be one or more decimal digits.
Thus `recvq=:` and `sendq=12:34` are admitted as structurally complete. Both fixtures
then print `table=complete` and the accepting listener line at rc 0.

Exact fixture, run twice under a checked scratch tree; outer rc 0 and both arm rcs 0:

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r6-audit-queue.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-r6-audit-queue.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
cat > "$Q/arm.sh" <<'ARM'
S="$1"; W="$2"; rec="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0
WPI_MOUNT_GUARD_ACTIVE=no; WPI_SS=/usr/bin/false
printf '%s\n' "$rec" > "$W/ss.out"
wpi_capture(){
 WPI_CAP_OUT="$W/ss.out"; WPI_CAP_ERR="$W/ss.err"
 : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
}
wpi_assert_listener_set
ARM
for spec in \
 'recv_colon|LISTEN : 128 127.0.0.1:8790 0.0.0.0:*' \
 'send_colon|LISTEN 0 12:34 127.0.0.1:8790 0.0.0.0:*'; do
  name=${spec%%|*}; rec=${spec#*|}
  bash --noprofile --norc "$Q/arm.sh" "$SCRIPT" "$Q/$name" "$rec" \
    > "$Q/$name.txt" 2>&1; rc=$?
  printf 'QUEUE_CASE=%s RC=%s INPUT_HEX=' "$name" "$rc"
  od -An -tx1 "$Q/$name/ss.out" | tr -d ' \n'; printf '\n'
  cat "$Q/$name.txt"
done
```

Observed output:

```text
QUEUE_CASE=recv_colon RC=0 INPUT_HEX=4c495354454e203a20313238203132372e302e302e313a3837393020302e302e302e303a2a0a
B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 evidence_file=/tmp/rp7-r6-audit-queue.zP0XPU/recv_colon/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
QUEUE_CASE=send_colon RC=0 INPUT_HEX=4c495354454e20302031323a3334203132372e302e302e313a3837393020302e302e302e303a2a0a
B6_listener_inventory rows=1 port_8790_rows=1 bytes=40 evidence_file=/tmp/rp7-r6-audit-queue.zP0XPU/send_colon/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
```

**Required repair:** validate `recvq` and `sendq` separately as nonempty decimal-digit
fields before any inventory-complete line. Add RED/GREEN for empty/colon-bearing queue
tokens while retaining the published column-padding and wildcard controls.

### 3. Draft row 22 claims captured/adjudicated byte identity that the disclosed reader residual does not establish - HIGH

**Locations:** `WPI_PREREGISTRATION_DRAFT.md:703` versus `:1069-1078` and
`SELF_QA_RP7.md:2436-2445`; implementation re-open at `RP7-WPI-RO.sh:1246`.

The round-6 draft says the inventory is read as one string "so that the byte string
adjudicated is the byte string captured." The child capture closes its descriptors, and
the listener reader later opens `WPI_CAP_OUT` by name. A replacement in that interval
therefore changes the subject. The implementer's residual-2 disclosure states exactly
that limitation, so the disclosure is accurate; the row-22 sentence and the associated
meaning of `bytes=` are the overclaim.

Executed fixture: the capture writes and preserves a wildcard child result, then a hook
at the real reader-allocation boundary replaces the name with a valid loopback record.
The real production listener reader/adjudicator is otherwise unchanged:

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r6-audit-reader-reopen.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-r6-audit-reader-reopen.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
source <(sed '/^wpi_main "\$@"$/d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0
WPI_MOUNT_GUARD_ACTIVE=no; WPI_SS=/usr/bin/false
wpi_capture(){
  WPI_CAP_OUT="$Q/ss.out"; WPI_CAP_ERR="$Q/ss.err"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0
  printf 'LISTEN 0 128 0.0.0.0:8790 0.0.0.0:*\n' > "$WPI_CAP_OUT"
  cp "$WPI_CAP_OUT" "$Q/child-captured.out"
}
wpi_alloc_read_diag(){
  local label="$1"
  rm -- "$WPI_CAP_OUT"
  printf 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\n' > "$WPI_CAP_OUT"
  WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1))
  WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
  wpi_open_leaf "$WPI_READ_DIAG"; WPI_READ_DIAG_FD="$WPI_LEAF_FD"
}
wpi_assert_listener_set
printf 'REOPEN_RACE_RC=0 captured_sha256=%s adjudicated_sha256=%s same=%s\n' \
 "$(sha256sum "$Q/child-captured.out" | cut -d ' ' -f1)" \
 "$(sha256sum "$Q/ss.out" | cut -d ' ' -f1)" \
 "$([ "$(sha256sum "$Q/child-captured.out" | cut -d ' ' -f1)" = "$(sha256sum "$Q/ss.out" | cut -d ' ' -f1)" ] && echo yes || echo no)"
```

Command rc 0. Observed output:

```text
B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 evidence_file=/tmp/rp7-r6-audit-reader-reopen.80PbUh/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
REOPEN_RACE_RC=0 captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc adjudicated_sha256=db4755ec151f8d59f9c069832b3b9ad602adfbb6d0a2c31e295e478e2378600d same=no
```

This injected swap is not claimed as an autonomous production action; like the recovered
leaf-replacement test, it measures what the block establishes. It establishes grammar
over the re-opened object, not equality with the object/bytes the child wrote.

**Required repair:** either keep/read the capture descriptor (and bind the read to the
created object), or narrow row 22 and the `bytes=` description to the re-opened evidence
object actually adjudicated. Do not state captured/adjudicated equality while residual 2
remains.

### 4. The evidence command propagates assertion failure but misclassifies kill-after timeout and does not enforce its claimed aggregate - MEDIUM

**Locations:** `SELF_QA_RP7.md:41-45`, exact command `:49-68`.

The exact good command was run verbatim from `WPI_BLOCKS_DRAFT`:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Command rc 0, wall 209.9 s. The following are exact, non-contiguous load-bearing
lines selected from the complete output; no line is abbreviated:

```text
022607b81a89213953b01e5499aad4d2a1aaf4892023c32dc293b191fba0130a */tmp/rp7-r6-fence-body.sh
719077959650f4b5ad4b94c3c122bfe9058ffa469b6c59161e5886271913c9e2 */tmp/rp7-r5-fence-body.sh
94101ef7fdf70d0f4628685811160389227cbba3c10e999e1942e8eb82bb56e0 */tmp/rp7-r4-fence-body.sh
 26681 /tmp/rp7-r6-fence-body.sh
 20050 /tmp/rp7-r5-fence-body.sh
 76710 /tmp/rp7-r4-fence-body.sh
123441 total
BYTE_IDENTITY red_bytes=77179 red_sha256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee red_cr=0 red_bash_n=0 green_bytes=88460 green_sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709 green_cr=0 green_bash_n=0
GREEN LISTENER_BYTES case=clean rc=0 accepting=1 parsed_complete=1 stop=[] fail=[] stderr_bytes=0
GREEN LISTENER_BYTES case=wildcard rc=1 accepting=0 parsed_complete=1 stop=[] fail=[nonloopback_listener addr=0.0.0.0] stderr_bytes=0
GREEN STATUS_RECORD rec=[TYPE state_version str int] child_rc=5 rc=1 result=[B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISMATCH state b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913] child_rc=1 rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value] stderr_bytes=0
GREEN STATUS_RECORD rec=[MISSING state_version] child_rc=4 rc=3 result=[B5_STOP reason=schema_unexpected field=state_version] stderr_bytes=0
GREEN STATUS_RECORD rec=[OK fields=8] child_rc=0 rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site] stderr_bytes=0
GREEN HTTP_CODE code=500 rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500] stderr_bytes=0
GREEN HTTP_CODE code=401 rc=3 result=[B5_STOP reason=status_endpoint_access_denied code=401] stderr_bytes=0
GREEN LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no
QA_PASS all_assertions=yes
QA_PASS all_assertions=yes
QA_PASS all_assertions=yes
R6_FENCE_RC=0
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=3 per_fence_bound_s=900 aggregate_bound_s=2700
```

Independent failing-fence falsification used a scratch `SELF_QA_RP7.md` with R6
`exit 7`, R5/R4 `exit 0`, and only the command's `cd` target and fixed body prefix
retargeted into the scratch tree:

```bash
DOC=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
Q=$(mktemp -d /tmp/rp7-r6-audit-fencefail.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-r6-audit-fencefail.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
mkdir -p "$Q/fake"
{
 printf '# RP7_R6_FENCE_BEGIN\nexit 7\n# RP7_R6_FENCE_END\n'
 printf '# RP7_QA_FENCE_BEGIN\nexit 0\n# RP7_QA_FENCE_END\n'
 printf '# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n'
} > "$Q/fake/SELF_QA_RP7.md"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' \
 "$DOC" > "$Q/published.txt"
sed -e "s#/tmp/rp7-#$Q/fake/body-#g" \
 -e "s#^cd /c/LAB/.*#cd $Q/fake#" "$Q/published.txt" > "$Q/run.sh"
printf 'SUBSTITUTIONS cd=%s body_prefix_refs=%s timeout_wrappers=%s\n' \
 "$(grep -c "^cd $Q/fake\$" "$Q/run.sh")" \
 "$(grep -c "$Q/fake/body-" "$Q/run.sh")" \
 "$(grep -c 'timeout --signal=TERM --kill-after=30s 900s' "$Q/run.sh")"
bash --noprofile --norc "$Q/run.sh" > "$Q/out.txt" 2> "$Q/err.txt"; rc=$?
printf 'MUTATED_PUBLISHED_RC=%s STDERR_BYTES=%s\n' "$rc" "$(wc -c < "$Q/err.txt")"
cat "$Q/out.txt"
```

Command rc 0 for the evidence wrapper; mutated published-command rc 1, stderr empty:

```text
SUBSTITUTIONS cd=1 body_prefix_refs=8 timeout_wrappers=3
R6_FENCE_RC=7
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=fence_failed
MUTATED_PUBLISHED_RC=1 STDERR_BYTES=0
```

Thus ordinary failure propagation is closed. Timeout distinction is not. The published
classifier recognizes only rc 124. The same wrapper/classifier with duration scaled to
1 s and kill grace to 2 s, driving a TERM-ignoring body, was executed exactly as follows:

```bash
DOC=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
Q=$(mktemp -d /tmp/rp7-r6-audit-timeout.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-r6-audit-timeout.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
cat > "$Q/ignore-term.sh" <<'ARM'
trap '' TERM
/usr/bin/sleep 30
ARM
cat > "$Q/classify.sh" <<'ARM'
Q="$1"
timeout --signal=TERM --kill-after=2s 1s bash --noprofile --norc "$Q/ignore-term.sh"; R6=$?
R5=0; R4=0
printf 'R6_FENCE_RC=%s\nR5_FENCE_RC=%s\nR4_FENCE_RC=%s\n' "$R6" "$R5" "$R4"
for rc in "$R6" "$R5" "$R4"; do
  case "$rc" in
    0) ;;
    124) printf 'PUBLISHED_COMMAND_RESULT=timeout per_fence_bound_s=1\n'; exit 124 ;;
    *) printf 'PUBLISHED_COMMAND_RESULT=fence_failed\n'; exit 1 ;;
  esac
done
ARM
bash --noprofile --norc "$Q/classify.sh" "$Q" > "$Q/out.txt" 2> "$Q/err.txt"; rc=$?
printf 'TERM_IGNORING_CLASSIFIER_RC=%s STDERR_BYTES=%s\n' "$rc" "$(wc -c < "$Q/err.txt")"
cat "$Q/out.txt"
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$DOC" > "$Q/published.txt"
wrappers=$(grep -c 'timeout --signal=TERM --kill-after=30s 900s bash --noprofile --norc' "$Q/published.txt")
claimed=$(grep -c 'aggregate_bound_s=2700' "$Q/published.txt")
printf 'BOUND_ARITHMETIC wrappers=%s per_fence_nominal_s=900 kill_grace_s=30 computed_three_fence_max_s=%s claimed_2700_lines=%s aggregate_wrapper=absent\n' \
 "$wrappers" "$((wrappers*(900+30)))" "$claimed"
```

Outer command rc 0; classifier rc 1. Observed output:

```text
TERM_IGNORING_CLASSIFIER_RC=1 STDERR_BYTES=169
R6_FENCE_RC=137
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=fence_failed
BOUND_ARITHMETIC wrappers=3 per_fence_nominal_s=900 kill_grace_s=30 computed_three_fence_max_s=2790 claimed_2700_lines=1 aggregate_wrapper=absent
```

**Required repair:** classify the timeout wrapper's kill-after outcomes distinctly from
assertion failure (including rc 137 for this executed path), and either add a real outer
aggregate bound or document/enforce a truthful bound that includes every 30-second grace.
Add a TERM-ignoring fence to the published D026 failure evidence.

## Out of scope and freeze-gate acknowledgement

Rows 10-19, the five round-5 repairs, rows 1-9, trading/Pine/parity/MTC behavior,
transport, deployment, and all host state were out of scope and were not adjudicated.
The carried fences cover those older bands only as regression gates; this report does not
re-open or accept them.

`WPI_FIXED_TRUSTED_PYTHON`,
`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT`, and the accepting `wpi_validate_inputs` branch remain
`<PIN-AT-FREEZE>`. The absence of a whole-block accepting run is expected and is not a
finding. Section 8.2 rows 1-9 remain implemented by no block and are a separate owner
decision.

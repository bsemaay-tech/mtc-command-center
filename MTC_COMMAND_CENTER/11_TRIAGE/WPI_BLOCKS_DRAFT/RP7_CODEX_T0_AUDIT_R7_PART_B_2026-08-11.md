# BLOCK: 4

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh independent T0 flagship slot.
This was a local, read-only audit. No host contact, network, SSH/SCP, RUNID,
service, credential, deployment, trading, or commit action occurred. The only
repository write is this report.

The four round-6 repair sites are not all acceptable as a package. The delivered
round-7 fence independently reproduces RED/GREEN for the common NUL reader, the
two queue-field cases, the listener descriptor substitution, and the intended
TERM-ignoring timeout path. The specific NUL, queue and listener-descriptor code
changes retain their stated clean/wildcard/record-disposition controls.

The band is nevertheless blocked. One of the four changes to the carried round-6
fence weakens an existing assertion: an unrelated mutation that makes
`wpi_capture` return 7 now passes the changed leaf-race assertion, whereas the old
assertion rejects it. More importantly, the Pattern-13 defect was moved rather
than closed: the listener inventory is descriptor-bound, but the shared
single-record reader still re-opens the status-code and namespace-result names.
Executed substitutions turn a child-observed HTTP 500 into accepting HTTP 200
and unequal child-observed namespaces into accepting equality. The published
evidence command also still labels every rc 137 as its own kill-after event and
still claims a 3720-second bound for the whole command even though its extraction,
hashing and byte-counting prelude is outside all four wrappers. Finally, the
production capture-bind inability emits a generic `RP7_STOP` that is not the
row-22 `B6_STOP` preregistered in the draft.

## Row results

| Row | Result | Executed/read evidence |
|---|---|---|
| **20 - B5 endpoint** | **FAIL** | The round-6 NUL repair works: `2<NUL>00` is now `B5_STOP ... detail=nul_byte_in_record`, while clean `200` remains accepting. But the real `wpi_single_record` re-opens `WPI_CAP_OUT` by name. Replacing a captured `500\n` with `200\n` at that reader boundary changes `B5_FAIL ... code=500` into the accepting `B5_status` line at rc 0 (finding 2). |
| **21 - B5 flags** | **FAIL (inherited from row 20)** | `O<NUL>K fields=8` now STOPs and clean `OK fields=8` remains accepting. Row 21 is unreachable as a truthful accepting row when row 20's claimed HTTP observation is not bound to the child output. Other disclosed status-body/name residuals were not re-opened as separate findings in this band. |
| **22 - netns/listener set** | **FAIL** | Queue fields `:` and `12:34` now STOP with `detail=queue_grammar`; padded columns still accept; wildcard still FAILs; the listener substitution reads the child's wildcard bytes through the descriptor and `bytes=36` equals independent `wc -c`. But the namespace single-record reader is still name-based: replacing child `net:[200]` with `net:[100]` changes `B6_STOP reason=netns_mismatch` into accepting `B6_netns ... binding=equal` (finding 2). A real capture-stream bind inability also prints the wrong preregistered STOP prefix/token (finding 4). |
| **23 - no wildcard** | **FAIL (inherited from row 22)** | After a complete bound listener parse, a real wildcard remains the truthful `B6_FAIL reason=nonloopback_listener addr=0.0.0.0`, rc 1. Row 23 cannot be accepted for this band because its row-22 namespace precondition can still be manufactured by a name substitution. |
| **24 - external closed** | **PASS as a boundary record only** | `B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no reason=network_domain_separation` is honest, and the final `does_not_establish` line names `row_24_operator_side_result`. RP7 does not claim to execute row 24. |

## Evidence and QA results

| Check | Result | Evidence |
|---|---|---|
| Subject identity | **PASS** | Current bytes are exactly 92853 B, SHA-256 `e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`, 0 CR bytes, `bash -n` rc 0. The round-6 predecessor was materialised with `git cat-file blob 3e2a976a:...`, never checkout: 88460 B, SHA-256 `6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709`, 0 CR bytes, `bash -n` rc 0. Commit `c708511f` contains the audited subject blob; the current worktree copy has no diff from it. |
| Delivered round-7 RED/GREEN fence | **PASS for the four stated repair arms** | Direct extraction/execution returned rc 0 and `QA_PASS all_assertions=yes`. It reproduced all three round-6 NUL false accepts on RED and STOPs on GREEN, both queue false accepts on RED and STOPs on GREEN, the listener name substitution false PASS on RED and wildcard FAIL over descriptor-bound child bytes on GREEN, rc 137 misclassification on the round-6 command text and the intended kill-after classification on round 7. Its clean, namespace-clean, four prior record dispositions, padded listener, wildcard, and TERM-honouring controls held. |
| Carried round-6 fence | **FAIL - weakened** | The body is not byte-identical. Three change classes preserve their local discrimination; the F5 leaf-race change does not. A deliberate unrelated `return 7` mutation produces `outside_text=ORIGINAL ... payload_left_the_tree=no`; the new regex accepts it and the predecessor rc-0 assertion rejects it (finding 1). |
| Carried round-5 and round-4 fences | **Neither is byte-identical** | Round 5 changed only the two GREEN identity constants: `71907795...13c9e2`, 20050 B -> `6a5a80fe...507a6`, 20050 B. Round 4 changed four capture stubs to allocate `WPI_CAP_OUT_FD`: `94101ef7...56e0`, 76710 B -> `ceb45f11...28159`, 76873 B. These immediate round-6-to-round-7 diffs are interface/identity adaptations, not byte-identical carries. |
| Reader-binding measurement | **Substantive listener result PASS; label FAIL** | The child copy, result disposition and independent `wc -c` make the listener substitution discriminating: GREEN reads 36 wildcard bytes and FAILs although the name holds 38 loopback bytes. But the printed field `adjudicated_name_sha256` hashes the re-resolved name, which GREEN expressly does **not** adjudicate. The prose later defines it as "what the leaf NAME resolved to"; the field must say `name_at_read_time_sha256`, or the descriptor bytes must actually be hashed. This wording defect is included in finding 3. |
| Timeout classification and aggregate | **FAIL** | The intended TERM-ignoring path is now distinct from ordinary assertion failure: it returns/classifies rc 137 as requested. The classifier cannot infer that provenance from rc 137, however: an immediate `exit 137` finishes in about one second and is still printed as `kind=killed_after_grace`. A FIFO at the first extraction makes the command remain in its unwrapped prelude until an independent 3-second timeout stops it; no published outer wrapper exists. The four wrappers enforce four fence-call budgets, not the stated upper bound that "no execution of this command can exceed" (finding 3). |
| Draft/block exact conformance | **FAIL** | Rows 20-24 otherwise match the repaired NUL/queue/listener/row-24 wording, and `bytes=` is honestly described as the block's own accounting of bytes consumed from the capture descriptor. But a production descriptor-bind failure exits inside `wpi_capture` as `RP7_STOP reason=capture_stream_not_bindable`; it cannot reach row 22's declared `B6_STOP ... detail=capture_stream_unbound` (finding 4). |

## Baseline identity commands and output

Current identity, command rc 0:

```powershell
$p = Resolve-Path -LiteralPath 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
$bytes = [System.IO.File]::ReadAllBytes($p)
$hash = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
$cr = ($bytes | Where-Object { $_ -eq 13 }).Count
"SHA256=$hash"
"BYTES=$($bytes.Length)"
"CR_BYTES=$cr"
bash -n /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
"BASH_N_RC=$LASTEXITCODE"
```

```text
SHA256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32
BYTES=92853
CR_BYTES=0
BASH_N_RC=0
```

Predecessor materialisation, command rc 0:

```bash
Q=$(mktemp -d /tmp/rp7-r7-audit-identity.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-identity.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
git cat-file blob '3e2a976a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh' > "$Q/round6.sh"
printf 'BLOB=%s\n' "$(git rev-parse '3e2a976a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh')"
sha256sum "$Q/round6.sh"
wc -c "$Q/round6.sh"
LC_ALL=C tr -cd '\r' < "$Q/round6.sh" | wc -c
bash -n "$Q/round6.sh"; printf 'BASH_N_RC=%s\n' "$?"
```

```text
BLOB=2bc44445142e0259c14116111df69719b5e0b8ad
6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709  <scratch>/round6.sh
88460
0
BASH_N_RC=0
```

The first local syntax attempt used an untranslated Windows path with WSL Bash and
returned 127 (`/bin/bash: C:LAB...: No such file or directory`). It did not parse the
subject. The valid `/mnt/c/...` invocation above is the syntax evidence.

## Direct round-7 fence execution

Exact command, rc 0:

```bash
cd /c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_R7_FENCE_BEGIN$/,/^# RP7_R7_FENCE_END$/p' SELF_QA_RP7.md |
  bash --noprofile --norc
```

Load-bearing output (all omitted lines were other arms from this same successful
execution, not errors):

```text
BYTE_IDENTITY red_bytes=88460 red_sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709 red_cr=0 red_bash_n=0 green_bytes=92853 green_sha256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32 green_cr=0 green_bash_n=0
RECORD_BYTES mode=code_nul subject=red rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
RECORD_BYTES mode=code_nul subject=green rc=3 result=[B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=nul_byte_in_record source=<scratch>/status_get.out]
RECORD_BYTES mode=record_nul subject=green rc=3 result=[B5_STOP reason=status_body_unreadable_or_unparseable detail=nul_byte_in_record source=<scratch>/status_json.out]
RECORD_BYTES mode=netns_nul subject=green rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=0 detail=nul_byte_in_record source=<scratch>/caller_netns.out]
QUEUE_FIELDS case=recv_colon subject=green rc=3 accepting=0 bytes= result=[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar]
QUEUE_FIELDS case=send_colon subject=green rc=3 accepting=0 bytes= result=[listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar]
QUEUE_FIELDS case=clean subject=green rc=0 accepting=1 bytes=58 result=[]
QUEUE_FIELDS case=wildcard subject=green rc=1 accepting=0 bytes=36 result=[nonloopback_listener addr=0.0.0.0]
READER_BINDING swap=yes subject=red rc=0 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc adjudicated_name_sha256=db4755ec151f8d59f9c069832b3b9ad602adfbb6d0a2c31e295e478e2378600d bytes_field=38 independent_wc_c=36 result=[accepting port=8790 count=1 local=127.0.0.1 wildcard=none table=complete]
READER_BINDING swap=yes subject=green rc=1 child_captured_sha256=97783a08dd5b7cc4ca2c11dcfcbf60e4604df8462292cad1a37b830564dfa2fc adjudicated_name_sha256=db4755ec151f8d59f9c069832b3b9ad602adfbb6d0a2c31e295e478e2378600d bytes_field=36 independent_wc_c=36 result=[nonloopback_listener addr=0.0.0.0]
TIMEOUT_CLASS body=ignore_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=137 fence_rcs=[R7_FENCE_RC=137 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
TIMEOUT_CLASS body=honour_term subject=green cd_retargeted=1 real_fence_bodies=0 scaled_wrappers=4 rc=124 fence_rcs=[R7_FENCE_RC=124 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout kind=terminated_at_bound per_fence_bound_s=900]
BOUND_ARITHMETIC subject=green wrappers=4 per_fence_nominal_s=900 kill_grace_s=30 computed_max_s=3720 claimed_s=3720 claim_true=yes outer_wrapper=absent
QA_PASS all_assertions=yes
```

## Findings

### 1. The changed carried-fence leaf-race assertion accepts an unrelated capture regression - HIGH

**Locations:** `SELF_QA_RP7.md:996-1014`; change described at
`RP7_REPAIR_R7_REPORT.md:176-179` and `SELF_QA_RP7.md:630-632`.

The predecessor assertion required the repaired GREEN capture to return rc 0 and
leave the outside file untouched. Round 7 moves the call into a subshell, which is
reasonable for observing an MSYS2 STOP, but changes the assertion to the basic-regex
`rc=[0-9]*`. That accepts any decimal status (and even an empty status) as long as
the outside file remains unchanged. The report's statement that the old assertion
"never measured" rc is false: rc was printed by the arm and the old grep pinned it
to zero.

The falsification inserts an unrelated `return 7` at the start of `wpi_capture`,
runs the delivered leaf arm, and applies the new and old assertions to the same
output. Exact command, outer rc 0:

```bash
BLOCK=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r7-audit-carried.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-carried.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
sed '/^wpi_capture() {/a\    return 7' "$BLOCK" > "$Q/mutant-return7.sh"
bash -n "$Q/mutant-return7.sh"; mutant_n=$?
cat > "$Q/leaf-arm.sh" <<'ARM'
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
bash --noprofile --norc "$Q/leaf-arm.sh" "$Q/mutant-return7.sh" "$Q/leaf" > "$Q/leaf.txt" 2>&1
arm_rc=$?
grep -q 'LEAF_RACE rc=[0-9]* outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no' "$Q/leaf.txt"; new_assert_rc=$?
grep -q 'LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no' "$Q/leaf.txt"; old_assert_rc=$?
printf 'CARRIED_F5_MUTATION mutant_bash_n=%s arm_rc=%s new_assert_rc=%s old_assert_rc=%s output=[%s]\n' \
  "$mutant_n" "$arm_rc" "$new_assert_rc" "$old_assert_rc" "$(cat "$Q/leaf.txt")"
```

```text
CARRIED_F5_MUTATION mutant_bash_n=0 arm_rc=0 new_assert_rc=0 old_assert_rc=1 output=[LEAF_RACE rc=7 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[]]
```

This is exactly the kickoff's priority case: a changed carried fence permits a
previously rejected, unrelated regression. **Required repair:** retain the
subshell, but accept only rc 0 on Linux, or rc 3 with the exact documented
`RP7_STOP reason=capture_stream_not_bindable label=leaf_race ...` on MSYS2. Every
other rc must fail the fence. Add this `return 7` mutation as the no-weakening RED.

### 2. Status and namespace child observations can still be replaced by name and become accepting - HIGH

**Locations:** `RP7-WPI-RO.sh:339-343`, called at `:1162`, `:1166`, `:1380`
and `:1431`; claim narrowing at `:21-27`; draft rows 20 and 22 at
`WPI_PREREGISTRATION_DRAFT.md:701,703`.

The listener reader repair is real: it consumes `WPI_CAP_OUT_FD`. The shared
single-record reader instead executes `exec {fd}<"$file"`, re-resolving the name
after the child exits. Calling this merely a grammar claim does not make it
truthful. Row 20 says what the GET returned; row 22 says what the two `readlink`
children returned. Those semantic claims require the parsed bytes to remain bound
to the producer observation.

The exact fixture below drives the real `wpi_single_record` and real row
adjudicators. The only hook is at the delivered `wpi_alloc_read_diag` boundary,
the same reader boundary used in the round-6 listener audit. Each no-swap control
first shows the deviant child result. Exact command, outer rc 0:

```bash
BLOCK=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r7-audit-name-readers.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-name-readers.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
cat > "$Q/arm.sh" <<'ARM'
S="$1"; W="$2"; mode="$3"; swap="$4"
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
    status_get:status) printf '500\n' > "$WPI_CAP_OUT"; printf '{}\n' > "$EV_DIR/ro.status.body" ;;
    status_json:status) printf 'OK fields=8\n' > "$WPI_CAP_OUT" ;;
    caller_netns:netns) printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
    service_netns:netns) printf 'net:[200]\n' > "$WPI_CAP_OUT" ;;
    *) exit 96 ;;
  esac
}
wpi_alloc_read_diag(){
  local label="$1"
  if [ "$label" = single_record ] && [ "$swap" = yes ]; then
    case "$WPI_CAP_OUT" in
      */status_get.out) cp "$WPI_CAP_OUT" "$W/child-observation.out"; rm -- "$WPI_CAP_OUT"; printf '200\n' > "$WPI_CAP_OUT" ;;
      */service_netns.out) cp "$WPI_CAP_OUT" "$W/child-observation.out"; rm -- "$WPI_CAP_OUT"; printf 'net:[100]\n' > "$WPI_CAP_OUT" ;;
    esac
  fi
  WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1))
  WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
  wpi_open_leaf "$WPI_READ_DIAG"; WPI_READ_DIAG_FD="$WPI_LEAF_FD"
}
case "$mode" in status) wpi_assert_status ;; netns) wpi_assert_netns_binding ;; esac
ARM
for mode in status netns; do
  for swap in no yes; do
    W=$Q/$mode-$swap
    bash --noprofile --norc "$Q/arm.sh" "$BLOCK" "$W" "$mode" "$swap" > "$W.txt" 2>&1; rc=$?
    [ -f "$W/child-observation.out" ] && child_sha=$(sha256sum < "$W/child-observation.out" | cut -d' ' -f1) || child_sha=not_replaced
    case "$mode" in status) name_file="$W/status_get.out";; netns) name_file="$W/service_netns.out";; esac
    printf 'NAME_REOPEN mode=%s swap=%s rc=%s child_sha256=%s name_at_read_sha256=%s result=[%s]\n' \
      "$mode" "$swap" "$rc" "$child_sha" "$(sha256sum < "$name_file" | cut -d' ' -f1)" \
      "$(sed -e "s#$Q#<scratch>#g" "$W.txt" | tr '\n' ' ' | sed 's/ *$//')"
  done
done
```

```text
NAME_REOPEN mode=status swap=no rc=1 child_sha256=not_replaced name_at_read_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NAME_REOPEN mode=status swap=yes rc=0 child_sha256=792376c209f338959be4cf00c54dbf82662b90516082e23106faec4c43c69e49 name_at_read_sha256=c11e3f4837efde2441e23a7b9da02131f53bf59fddeb7147c4ab81afe400460f result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
NAME_REOPEN mode=netns swap=no rc=3 child_sha256=not_replaced name_at_read_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
NAME_REOPEN mode=netns swap=yes rc=0 child_sha256=e7802787bd95105c8563387a8e49780d3e6c082b769bf1e09b476c45eaaa3722 name_at_read_sha256=48dc7f125f7cb9815afd6af30615b55fbdf17137a1128e4aec1ae9e4dd525c4b result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
```

This is Pattern 13: the child observation is admitted, the name is re-read, and
the original member has no terminal disposition. **Required repair:** use the
already-created capture read descriptor for every captured single-record result
whose semantics are attributed to its child (at minimum the status-code and both
namespace records), and add these exact no-swap/swap RED/GREEN arms. Re-audit the
separately disclosed status-body path before claiming row 21 provenance; this
report does not assert a separate executed body substitution.

### 3. The evidence command still overclaims rc 137 provenance and a whole-command aggregate; one reader-arm field is also mislabeled - MEDIUM

**Locations:** `SELF_QA_RP7.md:47-72`, exact command `:75-96`, classifier
`:88-93`, reader output `:434-440`, explanation `:596-603`.

The intended TERM-ignoring fixture is repaired and was executed: it reaches rc
137 and is no longer called an assertion failure. But the case statement sees
only a numeric rc. `timeout ... bash -c 'exit 137'` also returns 137 immediately,
and the command prints `kind=killed_after_grace` although no TERM or grace
occurred. The disclosure about another SIGKILL does not make that printed causal
claim true.

The four per-fence wrappers also do not enclose the four `sed` extractions,
`sha256sum`, `wc -c`, or shell overhead. Sequential composition supports a
3720-second **fence-timeout budget**; it does not support the prose statement
that 3720 "is an upper bound no execution of this command can exceed." A FIFO at
the first extraction demonstrates the missing boundary before any fence starts.

Exact combined falsification, outer rc 0:

```bash
REPO=/c/LAB/Tradingview_LAB_CLEAN
DOC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
Q=$(mktemp -d /tmp/rp7-r7-audit-evidence-contract.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-evidence-contract.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$DOC" > "$Q/published.txt"

T=$Q/direct137; mkdir -p "$T"
printf '# RP7_R7_FENCE_BEGIN\nexit 137\n# RP7_R7_FENCE_END\n# RP7_R6_FENCE_BEGIN\nexit 0\n# RP7_R6_FENCE_END\n# RP7_QA_FENCE_BEGIN\nexit 0\n# RP7_QA_FENCE_END\n# RP7_R4_FENCE_BEGIN\nexit 0\n# RP7_R4_FENCE_END\n' > "$T/SELF_QA_RP7.md"
sed -e "s#/tmp/rp7-#$T/body-#g" -e "s#^cd /c/LAB/.*#cd $T#" "$Q/published.txt" > "$T/run.sh"
SECONDS=0; bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
printf 'DIRECT_137_CLASSIFIER command_rc=%s elapsed_s=%s stderr_bytes=%s fence_rcs=[%s] result=[%s]\n' \
  "$rc" "$SECONDS" "$(wc -c < "$T/err.txt")" \
  "$(grep -E '^R[4-7]_FENCE_RC=' "$T/out.txt" | tr '\n' ' ' | sed 's/ *$//')" \
  "$(grep '^PUBLISHED_COMMAND_RESULT=' "$T/out.txt" | head -1 | sed 's/^PUBLISHED_COMMAND_RESULT=//')"

T=$Q/prelude; mkdir -p "$T"; mkfifo "$T/SELF_QA_RP7.md"
sed -e "s#/tmp/rp7-#$T/body-#g" -e "s#^cd /c/LAB/.*#cd $T#" "$Q/published.txt" > "$T/run.sh"
SECONDS=0; timeout --signal=TERM --kill-after=1s 3s bash --noprofile --norc "$T/run.sh" > "$T/out.txt" 2> "$T/err.txt"; rc=$?
printf 'UNBOUNDED_PRELUDE outer_test_rc=%s elapsed_s=%s stdout_bytes=%s stderr_bytes=%s extracted_fence_files=%s published_outer_wrapper=%s\n' \
  "$rc" "$SECONDS" "$(wc -c < "$T/out.txt")" "$(wc -c < "$T/err.txt")" \
  "$(find "$T" -maxdepth 1 -type f -name 'body-*-fence-body.sh' | wc -l)" \
  "$(grep -c RP7_AGGREGATE_WRAPPER "$Q/published.txt")"
```

```text
DIRECT_137_CLASSIFIER command_rc=137 elapsed_s=1 stderr_bytes=0 fence_rcs=[R7_FENCE_RC=137 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
UNBOUNDED_PRELUDE outer_test_rc=124 elapsed_s=3 stdout_bytes=0 stderr_bytes=0 extracted_fence_files=1 published_outer_wrapper=0
```

The reader-binding arm has a separate wording error visible in the successful
round-7 fence output above. On GREEN, `adjudicated_name_sha256=db4755...` hashes
the loopback object at the leaf name, while `bytes_field=36` and the wildcard FAIL
show that those name bytes were not adjudicated. The later prose accurately calls
this "what the leaf NAME resolved to," so the measurement is useful but its field
name is false.

**Required repair:** either instrument the wrapper so it can distinguish its own
timer event from an arbitrary 137, or print an honest ambiguous classification.
Add an outer bound if the claim is about the whole command; otherwise rename and
narrow the field/prose to `aggregate_fence_timeout_budget_s=3720` and expressly
exclude unwrapped setup/overhead. Rename `adjudicated_name_sha256` to
`name_at_read_time_sha256`, or hash the bytes actually consumed from the
descriptor.

### 4. The production listener bind-inability branch cannot emit the row-22 STOP declared by the draft - MEDIUM

**Locations:** `RP7-WPI-RO.sh:296-298` and `:1305-1306`; draft row 22 at
`WPI_PREREGISTRATION_DRAFT.md:703`.

The draft declares a descriptor-binding inability as
`B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound`.
That branch exists at line 1306, but production `wpi_capture` exits first at line
298 as generic `RP7_STOP reason=capture_stream_not_bindable`. The row-specific
branch is reachable only from a stub or other state that returns from capture
without a descriptor; it is not the production inability path.

The fixture uses the real capture and the same unlink mechanism the delivered
leaf-race arm says produces this inability on MSYS2. Exact command, outer rc 0;
driven row rc 3:

```bash
BLOCK=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r7-audit-carried.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-carried.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
printf '#!/bin/sh\nprintf "LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\\n"\n' > "$Q/fake-ss.sh"
chmod 755 "$Q/fake-ss.sh"
cat > "$Q/bind-arm.sh" <<'ARM'
S="$1"; W="$2"; SS="$3"
mkdir -p "$W"
source <(sed '/^wpi_main "\$@"$/d' "$S")
trap - ERR; set +E; set +e; set +u; set +o pipefail
EV_DIR="$W/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10; WPI_SS="$SS"
HOOK=0
wpi_clock_ms(){ HOOK=$((HOOK+1)); if [ "$HOOK" -eq 1 ]; then rm -- "$WPI_CAP_OUT"; fi; WPI_LINE="$HOOK"; }
wpi_assert_listener_set
ARM
bash --noprofile --norc "$Q/bind-arm.sh" "$BLOCK" "$Q/bind" "$Q/fake-ss.sh" > "$Q/bind.txt" 2>&1; bind_rc=$?
printf 'ROW22_BIND_INABILITY rc=%s output=[%s] draft_declared_b6_token_present=%s production_rp7_token_present=%s\n' \
  "$bind_rc" "$(sed -e "s#$Q#<scratch>#g" "$Q/bind.txt" | tr '\n' ' ' | sed 's/ *$//')" \
  "$(grep -c 'B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound' "$Q/bind.txt")" \
  "$(grep -c '^RP7_STOP reason=capture_stream_not_bindable label=listeners ' "$Q/bind.txt")"
```

```text
ROW22_BIND_INABILITY rc=3 output=[RP7_STOP reason=capture_stream_not_bindable label=listeners leaf=<scratch>/bind/ev/ro.0001.listeners.stdout] draft_declared_b6_token_present=0 production_rp7_token_present=1
```

**Required repair:** make capture binding failure return information to the row
adjudicator so listener capture emits the exact preregistered B6 STOP (and other
callers emit their own row-specific inability), or change the preregistration and
all exact-output contracts to the actually reachable token without broadening a
row-specific inability into an unclassified generic branch. Add a production,
not stub-only, arm for this path.

## Dedicated adjudication of the four changed round-6 fence classes

Immediate comparison is the round-6 document at commit `3e2a976a` against the
round-7 document at commit `c708511f`.

| Named change | Byte-diff fact | Discriminating-power verdict |
|---|---|---|
| Two GREEN identity constants | Only expected GREEN SHA-256 and byte count move from round 6 to exact round-7 identity. | **PRESERVES.** Both assertions remain exact; a different subject still fails before arms run. |
| `f4_bound_wrappers` 3 -> 4 | The published command adds a fourth fenced body and a fourth matching timeout call. | **PRESERVES the original wrapper-count check only.** It still detects a missing count relative to four fences. It does **not** establish the stronger whole-command aggregate claim; that separate defect is finding 3. |
| F1 listener stub opens `WPI_CAP_OUT_FD` | The stub opens the same exact fixture file it already wrote; fixture bytes, expected rc, STOP/FAIL tokens and listener assertions are unchanged. | **PRESERVES.** This is a necessary interface adaptation to production's descriptor-required reader, not a change to the tested malformed/clean/wildcard observations. |
| F5 leaf-race call moved to a subshell and GREEN rc assertion relaxed | The call can now survive the documented MSYS2 STOP, but `rc=0` became `rc=[0-9]*`. | **WEAKENS.** Executed `return 7` mutation passes the new assertion and fails the old one. This is finding 1 and outranks the remaining findings under the kickoff. |

Exact fence-identity command, rc 0:

```bash
REPO=/c/LAB/Tradingview_LAB_CLEAN; cd "$REPO"
Q=$(mktemp -d /tmp/rp7-r7-audit-fences.XXXXXX) || exit 97
trap 'case "$Q" in /tmp/rp7-r7-audit-fences.*) rm -rf -- "$Q";; *) exit 98;; esac' EXIT
QA=MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md
git cat-file blob "3e2a976a:$QA" > "$Q/old"
git cat-file blob "c708511f:$QA" > "$Q/new"
for spec in '6|RP7_R6' '5|RP7_QA' '4|RP7_R4'; do
  r=${spec%%|*}; marker=${spec#*|}
  sed -n "/^# ${marker}_FENCE_BEGIN$/,/^# ${marker}_FENCE_END$/p" "$Q/old" > "$Q/r$r.old"
  sed -n "/^# ${marker}_FENCE_BEGIN$/,/^# ${marker}_FENCE_END$/p" "$Q/new" > "$Q/r$r.new"
  if cmp -s "$Q/r$r.old" "$Q/r$r.new"; then same=yes; cmp_rc=0; else same=no; cmp_rc=1; fi
  printf 'FENCE_IDENTITY round=%s old_sha256=%s old_bytes=%s new_sha256=%s new_bytes=%s cmp_rc=%s byte_identical=%s\n' \
    "$r" "$(sha256sum "$Q/r$r.old"|cut -d' ' -f1)" "$(wc -c < "$Q/r$r.old")" \
    "$(sha256sum "$Q/r$r.new"|cut -d' ' -f1)" "$(wc -c < "$Q/r$r.new")" "$cmp_rc" "$same"
done
```

```text
FENCE_IDENTITY round=6 old_sha256=022607b81a89213953b01e5499aad4d2a1aaf4892023c32dc293b191fba0130a old_bytes=26681 new_sha256=b080dad4315281d0447baff10dae26797ba04998bc7c9e32fb2bbbd15a570a06 new_bytes=27355 cmp_rc=1 byte_identical=no
FENCE_IDENTITY round=5 old_sha256=719077959650f4b5ad4b94c3c122bfe9058ffa469b6c59161e5886271913c9e2 old_bytes=20050 new_sha256=6a5a80fef963c6506af93891cec362ce8e74fd6bde64f01d81bcb54cbe6507a6 new_bytes=20050 cmp_rc=1 byte_identical=no
FENCE_IDENTITY round=4 old_sha256=94101ef7fdf70d0f4628685811160389227cbba3c10e999e1942e8eb82bb56e0 old_bytes=76710 new_sha256=ceb45f11f071bd61055a894deb72af229b253cb0eff3931c9ea46a0628028159 new_bytes=76873 cmp_rc=1 byte_identical=no
```

Thus **none** of the round-6, round-5, or round-4 carried bodies is byte-identical
to its immediate round-6-document predecessor. Round 5's two identity edits and
round 4's four descriptor-stub edits preserve their local tests; round 6's F5
assertion does not.

## Round-6 finding dispositions

| Round-6 finding | Round-7 disposition |
|---|---|
| 1. Common reader deletes NUL | **Specific repair confirmed with no-weakening controls.** All three NUL records now STOP; clean status/parser/netns and the four earlier record dispositions hold. The same reader still has a separate producer-identity false-PASS defect (new finding 2). |
| 2. Queue fields not separately numeric | **Confirmed repaired.** Both exact malformed fields STOP before an inventory line; padded clean and wildcard controls are unchanged. |
| 3. Row-22 listener capture/adjudication identity | **Specific listener repair confirmed.** The descriptor-bound listener remains on child wildcard bytes under name substitution and `bytes=36` matches independent `wc -c`. Pattern 13 is not closed for status/netns single-record results (new finding 2), and the arm's `adjudicated_name_sha256` label is inaccurate (finding 3). |
| 4. Timeout classification/aggregate | **Partially repaired, still non-accepting.** The requested TERM-ignoring arm reaches a distinct rc-137 timeout line, and four fence-call budgets sum arithmetically to 3720. Rc 137 provenance and the claimed whole-command upper bound remain unsupported (finding 3). |

## Scope boundaries

Rows 10-19, the round-5 repairs, rows 1-9, transport, deployment, staging/host
state, credentials, ARM, broker/exchange/trading behavior, Pine, parity, MTC
behavior, and the operator-side execution of row 24 were out of scope and were
not adjudicated. The carried round-4/5/6 fences were examined only for byte
identity and regression-fence weakening; their older product bands were not
re-opened or accepted.

The `<PIN-AT-FREEZE>` constants and the accepting `wpi_validate_inputs` branch
remain known freeze-gate items, not findings. No whole-block accepting run is
possible before freeze. Section 8.2 rows 1-9 remain implemented by no block and
remain a separate owner decision.

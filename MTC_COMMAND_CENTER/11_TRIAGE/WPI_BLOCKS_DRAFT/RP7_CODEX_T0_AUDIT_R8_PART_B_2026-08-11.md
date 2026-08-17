# BLOCK: 5

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh independent T0 flagship slot.
This was a local, read-only audit. No host contact, network, SSH/SCP, RUNID,
service, credential, deployment, trading, Git mutation, or commit action occurred.
The only repository write is this report.

Round 8 does not accept for rows 20-24. The status-code, parser-result,
namespace and listener capture streams are now descriptor-bound, the exact
two-outcome carried assertion rejects the `return 7` mutant, and the current
published command really extracts and runs the five files it names. Those
repairs are real but the band remains blocked.

The most severe survivor is inside the band, not in the disclosed rows 10-19
residual: `ro.status.body` is still handed to curl and later to the parser by
name. An executed replacement made curl overwrite an object outside the
evidence tree, and a second executed replacement changed a child-produced ARMED
body into an accepting DISARMED result. Disclosure does not make either
`No host object outside that tree is changed` or `rows_10_23_read_only_predicates`
true.

The round-8 row-22 bind-inability fence also does not run the child it says it
runs. It closes the capture stdout descriptor before the child's redirection,
so Bash reports `Bad file descriptor`, the child marker is absent, and the block
still emits the hard-coded `rc=0 detail=capture_stream_unbound`. The current
published classifier can still have its alleged wrapper diagnostic forged by a
fence body on the shared stderr stream. A changed carried assertion equates two
counts but does not bind each extracted fence body to its own wrapper; a mutant
that never runs the R8 body passes that fence. Finally, the round-8 draft added a
mandatory `detail=<d>` to namespace-read failures while both nonzero child-rc
branches omit it.

## Row results

| Row | Result | Executed/read evidence |
|---|---|---|
| **20 - B5 endpoint** | **FAIL for the row-band safety contract** | The status-code record and its diagnostic stream are descriptor-bound, and the published substitution arm keeps a child-observed 500 at `B5_FAIL`. But the same curl invocation receives the response-body leaf by name. Replacing that name after create-once allocation made the child overwrite a hard-linked outside object at capture rc 0. The endpoint operation therefore does not preserve the block's read-only/evidence-tree boundary. |
| **21 - B5 flags** | **FAIL** | A no-swap ARMED body produces truthful `B5_FAIL ... field=state`, rc 1. Replacing the body name after its digest but before the parser makes the same child body produce `B5_status ... flags=expected`, rc 0. The accepting line even carries the ARMED body's digest while the parser consumed different DISARMED bytes. |
| **22 - B5/B6 netns/listener** | **FAIL** | The status/netns/listener stdout and stderr descriptor repairs work on their published substitutions. The declared listener bind-inability token is textually reachable, but the published reachability arm prevents the child from executing, discards that failure, emits an extra raw shell diagnostic, and prints `rc=0`. Separately, a readlink-child rc 7 produces no `detail=` although draft row 22 requires it. |
| **23 - no wildcard** | **FAIL inherited from row 22** | After a complete descriptor-bound parse, wildcard remains the truthful `B6_FAIL reason=nonloopback_listener`; no new listener-semantic defect was found. Row 23 cannot be accepted while its row-22 prerequisite/evidence contract is non-accepting. |
| **24 - external closed** | **PASS as a boundary record only** | `B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no reason=network_domain_separation` is honest. RP7 does not claim to execute row 24, and its final limitation line names the omission. |

## Subject and baseline evidence

| Check | Result | Evidence |
|---|---|---|
| Round-8 identity | **PASS** | SHA-256 `11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`, 99903 B, 0 CR bytes, 1661 LF bytes, `bash -n` rc 0. The worktree bytes are the subject committed by `bb8546e6`. |
| Round-7 predecessor | **PASS** | Materialised only with `git cat-file blob c708511f:...`, never checkout: SHA-256 `e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`, 92853 B, 0 CR bytes, `bash -n` rc 0. |
| Published command | **PASS on its delivered inputs, non-accepting as a complete evidence contract** | Verbatim Git-Bash entrypoint rc 0 in 251.7 s; five `QA_PASS`, five fence rcs 0 and the stated pass line. Findings 3-4 show two missing falsifications in its causal/mapping evidence. |
| Draft edits | **FAIL exact conformance** | Rows 20-22 accurately describe the new descriptor-bound record readers, but row 22's mandatory `detail=<d>` is absent from the two nonzero readlink-rc branches. |

Identity commands, rc 0:

```powershell
$p = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
$b = [System.IO.File]::ReadAllBytes($p)
(Get-FileHash -Algorithm SHA256 -LiteralPath $p).Hash.ToLowerInvariant()
$b.Length
($b | Where-Object { $_ -eq 13 }).Count
($b | Where-Object { $_ -eq 10 }).Count
bash -n 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
```

```text
11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4
99903
0
1661
BASH_N_RC=0
```

Predecessor materialisation produced:

```text
PRED_SHA256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32
PRED_BYTES=92853
PRED_CR_BYTES=0
PRED_BASH_N_RC=0
```

## Findings

### 1. The in-band status-body name remains both an outside-tree write primitive and a false-PASS primitive - BLOCK/HIGH

**Locations:** `RP7-WPI-RO.sh:9-21`, `:1492-1497`, `:1514`,
`:1521-1552`, `:1656`; `SELF_QA_RP7.md:3663-3670,3697-3699`;
draft row 21 at `WPI_PREREGISTRATION_DRAFT.md:702`.

`wpi_alloc_leaf` establishes only that `ro.status.body` was absent when an empty
leaf was created. Curl later receives the name through `--output "$body"`; the
digest and Python parser also receive the name. Nothing binds the object curl
writes or the object the parser opens to the create-once leaf or to each other.

The disclosure at `SELF_QA_RP7.md:3663-3670` is accurate, but it is not a safety
control. It directly contradicts the block's unqualified statements that no
outside object is changed and that rows 10-23 are read-only predicates. It is
also inside rows 20-21, so the separate rows 10-19 scope boundary does not apply.

First executed arm: real create-once allocation and real `wpi_capture`; the only
child substitution is a local no-network curl-shaped program that opens the
exact `--output` argument it is given. The `wpi_clock_ms` hook replaces the body
name with a hard link after allocation and before the child starts.

```bash
body="$EV_DIR/ro.status.body"
OUTSIDE="$W/outside.txt"
printf 'ORIGINAL\n' > "$OUTSIDE"
wpi_alloc_leaf "$body"
HOOK=0
wpi_clock_ms(){
  HOOK=$((HOOK+1))
  if [ "$HOOK" -eq 1 ]; then rm -- "$body"; ln -- "$OUTSIDE" "$body"; fi
  WPI_LINE="$HOOK"
}
wpi_capture status_get "$FAKE_CURL" --silent --show-error \
  --connect-timeout 5 --max-time 10 --request GET --output "$body" \
  --write-out '%{http_code}\n' -- http://127.0.0.1:8790/api/status
```

Command rc 0; arm rc 0:

```text
CURL_BODY_WRITE_RACE arm_rc=0 result=[CURL_NAME_WRITE capture_rc=0 outside_text=CURL_BODY outside_bytes=10 same_inode=yes status_record=200]
```

Second executed arm: the real `wpi_assert_status`, its exact embedded parser and
the same pinned-interpreter flags. Only the MSYS/native CRLF plumbing is
normalised, the same substitution already disclosed by the delivered QA. The
status child writes an ARMED body and `200`; in `swap=yes`, the body name is
replaced with a complete DISARMED body after `wpi_sha_file` but immediately
before the real parser runs.

```bash
for swap in no yes; do
  bash --noprofile --norc "$Q/arm.sh" "$BLOCK" "$Q/$swap" "$swap"
done
```

Outer command rc 0. Driven row outputs:

```text
STATUS_BODY_NAME_SWAP swap=no rc=1 child_body_sha256=not_replaced name_at_parser_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 result=[B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value]
STATUS_BODY_NAME_SWAP swap=yes rc=0 child_body_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 name_at_parser_sha256=378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821 result=[B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site]
```

The two different SHA-256 values prove the substitution; the accepting line's
`body_sha256` proves the digest and parser adjudicated different objects.

**Required repair:** bind the curl body write to the create-once object and bind
the digest/parser reads to that same object, with no name fallback. If the chosen
curl interface cannot write to an inherited descriptor while preserving all
other contracts, the row must STOP or the design must change; an admitted false
PASS and outside-tree overwrite cannot remain a documented residual. Add both
outside-write and ARMED-to-DISARMED RED/GREEN arms.

### 2. The row-22 bind-inability fence prevents the named child from running and emits a false rc 0 - HIGH

**Locations:** `RP7-WPI-RO.sh:300-342`; `SELF_QA_RP7.md:632-682`.

The fence says it uses the real capture, wrapper and child. Its first
`wpi_clock_ms` call occurs at block line 312, before the child subshell's stdout
redirection at line 317. The hook at self-QA line 662 closes `ofd` there. Bash
therefore cannot establish the child redirection; the child is never executed.
The resulting nonzero capture rc is not assigned to `WPI_CAP_RC` before the
bind-failure exit at lines 336-338, and the caller-supplied literal says `rc=0`.

Executed marker control and falsification:

```bash
printf '#!/bin/sh\nprintf x > "%s"\nprintf "LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*\\n"\n' \
  "$Q/child-ran.marker" > "$Q/fake-ss.sh"
chmod 755 "$Q/fake-ss.sh"
wpi_clock_ms(){
  HOOK=$((HOOK+1))
  if [ "$mode" = close ] && [ "$HOOK" -eq 1 ]; then eval "exec ${ofd}>&-"; fi
  WPI_LINE="$HOOK"
}
wpi_assert_listener_set
```

Outer command rc 0. Control rc 0; driven inability rc 3:

```text
ROW22_BIND_CHILD_EXEC mode=control rc=0 child_ran=yes result=[B6_listener_inventory rows=1 port_8790_rows=1 bytes=38 evidence_file=<scratch>/control/ev/ro.0001.listeners.stdout content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete]
ROW22_BIND_CHILD_EXEC mode=close rc=3 child_ran=no result=[/dev/fd/63: line 317: "$ofd": Bad file descriptor B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
```

The line matches the declared form textually, but the demonstrated branch does
not establish the fact that form states. It also emits a raw shell diagnostic in
addition to the machine-readable line.

**Required repair:** adjudicate the real child/capture rc before any
caller-specific bind token, and make the row-specific token report only facts
that held. Replace the fence with a deterministic post-child bind failure whose
marker proves the child ran and whose captured rc/diagnostics prove the child
completed; assert that no unstructured line escapes. If that state cannot be
constructed, classify the current test as supplemental, not closure evidence.

### 3. A fence body can forge the alleged wrapper-owned rc-137 diagnostic - MEDIUM

**Locations:** `SELF_QA_RP7.md:114-131`, especially the shared stderr files and
substring greps at `:124-125`; round-8 F3 at `:522-610`.

`timeout --verbose` and the fence body write to the same stderr file. The
classifier does not establish which writer emitted `sending signal KILL to
command`; it only greps the combined stream. A fence body that prints the phrase
and immediately exits 137 is therefore called this wrapper's kill-after event.

Executed current-command falsification; only `cd` and `/tmp/rp7-` paths were
retargeted, exactly as the delivered F3 arm does:

```bash
printf '# RP7_R8_FENCE_BEGIN\nprintf "timeout: sending signal KILL to command\\n" >&2\nexit 137\n# RP7_R8_FENCE_END\n' > "$T/SELF_QA_RP7.md"
# Four remaining marker bodies are `exit 0`.
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' "$DOC" > "$Q/published.txt"
sed -e "s#/tmp/rp7-#$T/body-#g" -e "s#^cd /c/LAB/.*#cd $T#" \
  "$Q/published.txt" > "$T/run.sh"
bash --noprofile --norc "$T/run.sh"
```

Outer command rc 0; published command rc 137:

```text
RC137_STDERR_SPOOF command_rc=137 wrapper_generated_kill=no child_spoof_present=1 fence_rcs=[R8_FENCE_RC=137 R7_FENCE_RC=0 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0] result=[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=no wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30] stderr=[timeout: sending signal KILL to command]
```

The misclassification remains non-accepting, but its printed provenance is
false, which is exactly the round-7 finding's claim boundary.

**Required repair:** obtain wrapper-only signal evidence on a channel the body
cannot write, or withdraw the causal classification and report an ambiguous rc
137. Add a child-stderr spoof arm alongside `direct_137` and `ignore_term`.

### 4. The changed carried wrapper/body assertion accepts a command that never runs the R8 body - MEDIUM

**Locations:** `SELF_QA_RP7.md:1597-1610`.

The new `f4_every_body_wrapped` assertion proves only
`count(timeout lines) == count(extraction lines)`. It does not prove a one-to-one
mapping. A command with five extracted bodies and five wrappers can omit one body
and execute another twice.

Executed mutation: in a copy of the delivered document, change only the R8
wrapper's script operand from `rp7-r8-fence-body.sh` to
`rp7-r7-fence-body.sh`, then run the delivered round-6 carried fence against
that document.

```bash
sed "0,/^timeout --verbose .*rp7-r8-fence-body\.sh/{s#bash --noprofile --norc /tmp/rp7-r8-fence-body.sh#bash --noprofile --norc /tmp/rp7-r7-fence-body.sh#}" \
  "$DOC" > "$Q/mutant.md"
sed -n '/^# RP7_R6_FENCE_BEGIN$/,/^# RP7_R6_FENCE_END$/p' "$Q/mutant.md" |
  sed "s#^DOC=.*#DOC=$Q/mutant.md#" > "$Q/r6-mutant.sh"
timeout 180 bash --noprofile --norc "$Q/r6-mutant.sh"
```

Outer command rc 0; carried-fence rc 0:

```text
WRAPPER_MAPPING_MUTANT rc=0 original_r8_runs=1 mutant_r8_runs=0 mutant_r7_runs=2 qa_pass=1 stderr_bytes=0 bound_line=[PUBLISHED_BOUND timeout_wrappers=5 extracted_fence_bodies=5 documented_budget_mentions=4] propagation_line=[PUBLISHED_RC_PROPAGATION round6_command_rc=1 substitutions=2]
```

The current published command itself maps all five bodies correctly; the defect
is the changed carried assertion's claimed discriminating power.

**Required repair:** parse and compare exact per-fence mappings: each extracted
body path must occur as exactly one wrapper operand, each wrapper must write/read
the matching per-fence stderr path and rc variable, and no body may be duplicated
or omitted. Add this exact duplicate-R7/omit-R8 mutant as RED.

### 5. Draft row 22 requires `detail=<d>` on namespace-read failure, but both nonzero child-rc branches omit it - MEDIUM

**Locations:** `RP7-WPI-RO.sh:1263-1274`; draft row 22 at
`WPI_PREREGISTRATION_DRAFT.md:703`.

Round 8 changed the draft to declare
`B6_STOP reason=service_netns_unreadable path=/proc/<pid>/ns/net rc=<n> detail=<d>`.
The capture-bind, record, grammar and read-diagnostic branches carry a detail.
The two immediate nonzero `readlink` child branches emit only `rc=<n>`.

Executed real caller with a capture callee returning rc 7:

```bash
wpi_capture(){
  WPI_CAP_OUT="$W/out"; WPI_CAP_ERR="$W/err"
  : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"
  exec {WPI_CAP_OUT_FD}<"$WPI_CAP_OUT"; exec {WPI_CAP_ERR_FD}<"$WPI_CAP_ERR"
  WPI_CAP_RC=7
}
wpi_assert_netns_binding
```

Outer command rc 0; driven row rc 3:

```text
NETNS_CHILD_NONZERO rc=3 result=[B6_STOP reason=service_netns_unreadable path=/proc/self/ns/net rc=7] detail_field_present=0
```

**Required repair:** either add the exact preregistered detail token to both
nonzero branches or narrow the draft so `detail` is not claimed for them. Re-run
both caller and service-path nonzero branches.

## Published-command integrity

The only third-party entrypoint published as a command is:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

It has no Bash script operand, so Bash executes the piped program; it does not
repeat the RP6 error where a filename operand caused stdin to be ignored. Inside
the extracted program, the delivered lines map correctly and uniquely:

| Marker range | Extracted file | Wrapper operand | rc variable |
|---|---|---|---|
| `RP7_R8` | `/tmp/rp7-r8-fence-body.sh` | same | `R8` |
| `RP7_R7` | `/tmp/rp7-r7-fence-body.sh` | same | `R7` |
| `RP7_R6` | `/tmp/rp7-r6-fence-body.sh` | same | `R6` |
| `RP7_QA` | `/tmp/rp7-r5-fence-body.sh` | same | `R5` |
| `RP7_R4` | `/tmp/rp7-r4-fence-body.sh` | same | `R4` |

Verbatim execution under `C:\Program Files\Git\bin\bash.exe` returned rc 0 in
251.7 s. Load-bearing output:

```text
dada2eaa8ce970c75ffec583ebff5fcb1d41d928fcce511dbc5b990322007f98 */tmp/rp7-r8-fence-body.sh
2a2eb8932352ea865022daf8c4be566b50bde61977339cfac91a71020ff327ff */tmp/rp7-r7-fence-body.sh
0dc6213799d422f0921b0742a28840334c7453697087b205ced56d48ecfd2fb1 */tmp/rp7-r6-fence-body.sh
a3fb4b346d1fbb8785b20eefd7b6c96be1ae79adcf74ac4804e3323906d3fc56 */tmp/rp7-r5-fence-body.sh
4ddfa8b51bf31c99db560b07aac8572579020c231682201add643ea1f07c4cd1 */tmp/rp7-r4-fence-body.sh
R8_FENCE_RC=0
R7_FENCE_RC=0
R6_FENCE_RC=0
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=5 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=4650 whole_command_bound=none prelude_bounded=no
```

`fence_timeout_budget_s=4650` is truthful arithmetic for five wrapper windows.
`whole_command_bound=none prelude_bounded=no` is an honest admission, not a
required repair in this audit: the command does not promise a whole-command
bound, and the delivered FIFO arm proves the limitation. A future operator may
choose an outer watchdog, but adding one is not necessary to make the current
sentence true. Finding 3 is separate: the command still overstates who emitted a
diagnostic inside a per-fence stderr stream.

## Changed carried-arm adjudication

Immediate comparison: round-7 document at `c708511f` versus round-8 document at
`bb8546e6`.

| Fence/change | Independent byte fact | Discriminating-power verdict |
|---|---|---|
| R7 identity constants | R7 body `d4c730e5...0dbe`, 21450 B -> `2a2eb893...27ff`, 22522 B. Exact GREEN SHA/bytes move to round 8. | **PRESERVES.** Wrong subject bytes fail before arms. |
| R7 status/listener stubs add `WPI_CAP_ERR_FD` | Two interface sites; fixture bytes and expected outcomes unchanged. | **PRESERVES locally.** Both stdout and stderr are now supplied to the production reader contract. |
| R7 reader field rename | `adjudicated_name_sha256` -> `name_at_read_time_sha256`. | **PRESERVES and corrects wording.** Result/byte assertions are unchanged. |
| R7 F4 GREEN freezes `c708511f` instead of live `$DOC` | Historical command subject becomes stable. | **PRESERVES the historical round-6/round-7 distinction.** Current command has an R8 arm, but that arm misses finding 3. |
| R6 identity constants | R6 body `b080dad4...a06`, 27355 B -> `0dc62137...d2fb1`, 32069 B. | **PRESERVES.** Exact identity gate. |
| R6 descriptor adaptations | Status/listener stubs add both capture descriptors. | **PRESERVES locally.** Published dispositions reproduced. |
| R6 wrapper pattern/count + `BODIES` equality | Pattern gains `--verbose`, 4 -> 5, and compares two counts. | **WEAKENS the claimed mapping guarantee.** It accepts omit-R8/duplicate-R7 (finding 4). The current command mapping itself is correct. |
| R6 F5 exact classifier + `return 7` mutant | Subshell retained; exact rc-0/empty or exact rc-3/STOP outcomes; same three outputs fed to old/new assertions. | **RESTORES.** Executed output shows old accepts mutant, new rejects mutant, both reject escaping round-5, new accepts legitimate GREEN. |
| R5 identity constants | R5 body `6a5a80fe...07a6`, 20050 B -> `a3fb4b34...c56`, 20050 B. | **PRESERVES.** No arm changed. |
| R4 descriptor allocation class | R4 body `ceb45f11...8159`, 76873 B -> `4ddfa8b5...c4cd1`, 77408 B; the B5/B6 stubs now provide stderr descriptors as required by production. | **PRESERVES locally.** Same fixtures reach the same row dispositions in the verbatim green run. |

The restored assertion itself is confirmed:

```text
escaping_round5  LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes capture_result=[]
green            LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro.0001.leaf_race.stdout]
mutant_return7   LEAF_RACE rc=7 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[]
ASSERTION_POWER mutant_bash_n=0 round7_on_green=accept round7_on_mutant=accept round7_on_escaping=reject round8_on_green=accept round8_on_mutant=reject round8_on_escaping=reject green_kind=unlinked_leaf_not_rebindable_rc3
```

## Round-7 finding dispositions

| Round-7 finding | Round-8 audit disposition |
|---|---|
| 1. Changed carried assertion accepted `return 7` | **Specific repair confirmed.** Exact two-outcome pin rejects the mutant in both R8 and carried R6 fences. New changed-carried mapping weakness is finding 4 above. |
| 2. Status/netns observations replaceable by name | **Specific capture-stream repair confirmed, band still non-accepting.** Status code, parser result, both namespace records, listener inventory and their child diagnostic streams are descriptor-bound with no fallback. The separately disclosed in-band status body remains name-bound and produces finding 1. The disclosed rows 10-19 and read-diagnostic list is otherwise accurate and remains out of scope. |
| 3. rc-137 provenance / aggregate / reader label | **Aggregate and label repaired; provenance not closed.** `prelude_bounded=no` is honest and the label is correct. Shared stderr permits a fence body to forge the alleged wrapper diagnostic (finding 3). |
| 4. Listener bind inability could not emit declared STOP | **Textual reachability added, closure evidence invalid.** The exact token appears, but the delivered arm prevents the child from running and lies about rc 0 (finding 2). |

## Scope boundaries

Rows 10-19, rows 1-9, the earlier product repairs, transport, deployment,
staging/host state, credentials, ARM, broker/exchange/trading behavior, Pine,
parity, MTC behavior, and operator-side execution of row 24 were out of scope
and were not adjudicated. The rows 10-19 and read-diagnostic name-opened readers
were checked only to judge the disclosure's accuracy; they were not re-opened as
findings.

The `<PIN-AT-FREEZE>` constants and the accepting `wpi_validate_inputs` branch
remain known freeze-gate items, not findings. Section 8.2 rows 1-9 remain
implemented by no block and remain a separate owner decision.

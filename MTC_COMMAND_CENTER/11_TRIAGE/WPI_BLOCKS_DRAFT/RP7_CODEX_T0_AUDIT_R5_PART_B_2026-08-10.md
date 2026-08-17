# BLOCK: 4 findings

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh-session flagship T0 slot. This was a
local, read-only audit. No host, network, SSH/SCP, RUNID, credential, service,
deployment, trading, or commit action occurred.

Audited subject: `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, round-5 worktree bytes traced
to commit `1143a9ff`. The kickoff identity re-derived exactly:

```text
SHA256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee
BYTES=77179
CR_BYTES=0
BASH_N_RC=0
```

The band is not accepting. The preregistered B5/B6 order, ordinary two-phase
listener test, pinned-interpreter isolation wording, and row-24 boundary are
correct. However, a NUL-bearing listener record is silently normalised by Bash
`read` and reaches the row-22/23 accepting lines; malformed structured parser
records and invalid HTTP codes are reported as host-state FAILs instead of
STOPs; and the published QA command masks failing fence statuses in its own rc
and has no documented/enforced aggregate bound.

The five round-5 repairs and rows 10-19 were out of scope for this run. They were
not re-adjudicated here.

## Row results

| Row | Result | Executed/read evidence |
|---|---|---|
| **20 - B5 endpoint** | **FAIL** | Runtime order is correctly `netns -> status -> listener`. Valid `500` becomes FAIL, `401` becomes STOP, and a short code becomes grammar STOP. But rc-0 code `000` and `600` both become `B5_FAIL`; they are not valid completed HTTP statuses under the section 8.2 contract and must STOP (finding 3). |
| **21 - B5 flags** | **FAIL** | The actual child is requested with `-I -S`, checks `sys.flags.isolated`, `sys.flags.no_site`, and absence of `site`/startup-hook modules before parsing, and the accepting wording is limited to the bound interpreter plus that child-reported state. Strict JSON, duplicate-key, non-JSON-constant, missing-field, type, and value branches in the published fence reproduce. But the parent accepts truncated or invented `TYPE`/`MISMATCH` result records as semantic FAILs (finding 2). |
| **22 - B5/B6 netns and listener set** | **FAIL** | Netns binding precedes B5/B6. A wildcard record followed by a short malformed record STOPs rc 3 in both permutations, and a complete wildcard table is adjudicated only after the inventory line. But a NUL-bearing record, a nonnumeric address record, and an out-of-range-port record all reached `B6_listener_set ...` rc 0. The table was not strictly parsed to its original byte grammar (finding 1). |
| **23 - B6 no wildcard** | **FAIL (inherited from row 22)** | Wildcard semantics are deferred until after the ordinary grammar loop, but the shared parser can silently admit malformed bytes and then claim `table=complete`. Row 23 therefore lacks the complete-parse precondition required for its accepting result. |
| **24 - B6 external closed** | **PASS** | The block prints `B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no reason=network_domain_separation`, and its final negative claim includes `row_24_operator_side_result`. It neither probes nor silently claims row 24. |

## Evidence/QA contract result

| Check | Result | Evidence |
|---|---|---|
| Published command runs verbatim | **PASS for the current bytes** | From `WPI_BLOCKS_DRAFT` in fresh Git Bash, the exact published `sed ... | bash --noprofile --norc` command returned rc 0 in 188,127 ms, emitted 28,346 stdout bytes, and emitted zero stderr bytes. Both fence hashes, byte counts, `QA_PASS` lines, and `R5_FENCE_RC=0` / `R4_FENCE_RC=0` matched the record. |
| No absolute line ranges | **PASS** | Static scan found exactly three `sed -n` commands, all content-anchored; numeric `sed`/`NR`/PowerShell range hits: 0. |
| Anchor self-reopening | **PASS** | Each of the six exact marker lines occurs once. Invocation text starts with `sed`, not `#`, so it cannot re-open any anchored range. |
| Recorded summary and stderr | **PASS** | Re-derived fence identities are `0263067e...5b62f` / 20,050 B and `94101ef7...56e0` / 76,710 B. Both fences ended `QA_PASS all_assertions=yes`; stderr was empty. Timing-only variation stayed within the document's disclosed nondeterminism. |
| Command rc and documented bound | **FAIL** | The two fence invocations are followed by `printf`, so the overall command returns the final `printf` status even when either fence fails. No outer timeout or aggregate bound is present or documented. The current run terminated, but that does not establish the claimed bounded/fail-closed command contract (finding 4). |

## Baseline commands and observed output

Identity command (PowerShell byte count plus Git Bash syntax check), rc 0:

```powershell
$f='MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
$bytes=[System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $f))
$cr=($bytes | Where-Object { $_ -eq 13 }).Count
$hash=(Get-FileHash -Algorithm SHA256 -LiteralPath $f).Hash.ToLowerInvariant()
"SHA256=$hash"
"BYTES=$($bytes.Length)"
"CR_BYTES=$cr"
& 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -n '/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
"BASH_N_RC=$LASTEXITCODE"
```

Observed output is the four-line identity block at the start of this report.

Published command, executed exactly as written with cwd
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT`
inside fresh Git Bash:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Observed command rc and summary:

```text
COMMAND_RC=0
ELAPSED_MS=188127
STDOUT_BYTES=28346
STDERR_BYTES=0
0263067e4bb41d8c4c6bbfd96bd35b8a83cc48d1eedc14c1acdc886ee7a5b62f */tmp/rp7-r5-fence-body.sh
94101ef7fdf70d0f4628685811160389227cbba3c10e999e1942e8eb82bb56e0 */tmp/rp7-r4-fence-body.sh
20050 /tmp/rp7-r5-fence-body.sh
76710 /tmp/rp7-r4-fence-body.sh
96760 total
...
QA_PASS all_assertions=yes
R5_FENCE_RC=0
...
QA_PASS all_assertions=yes
R4_FENCE_RC=0
```

Anchor/range scan, rc 0:

```text
ANCHOR_COUNT marker=[# RP7_EXACT_COMMAND_BEGIN] count=1
ANCHOR_COUNT marker=[# RP7_EXACT_COMMAND_END] count=1
ANCHOR_COUNT marker=[# RP7_QA_FENCE_BEGIN] count=1
ANCHOR_COUNT marker=[# RP7_QA_FENCE_END] count=1
ANCHOR_COUNT marker=[# RP7_R4_FENCE_BEGIN] count=1
ANCHOR_COUNT marker=[# RP7_R4_FENCE_END] count=1
SED_N_COUNT=3
ABSOLUTE_LINE_RANGE_HITS=0
```

The complete published run also reproduced:

```text
LISTENER_ORDER red_wildcard_first_rc=1 red_malformed_first_rc=3 green_wildcard_first_rc=3 green_malformed_first_rc=3 expected_both_stop=3
B5B6_DECLARED_ORDER wpi_assert_netns_binding,wpi_assert_status,wpi_assert_listener_set,
TWO_DEVIATION ... green_first_result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
```

## Findings

### 1. A malformed listener record can be silently normalised and reported as a complete PASS - HIGH

**Locations:** `RP7-WPI-RO.sh:1093`, `:1100-1112`, `:1129-1135`.

Bash `read` discards NUL bytes. The parser does not compare the consumed/reconstructed
record against the original bytes or preflight the captured evidence leaf for NUL. An
input record whose state bytes are `LIS<NUL>TEN` is therefore read as `LISTEN`; the block
prints both `parse=complete_before_semantics` and the accepting listener-set line. This
violates the row-22 rule that a table with any malformed record STOPs before semantic
adjudication. Independent companion cases also admitted `nonsense:22 nonsense:*` and
local port `99999` while claiming a complete parse.

The following body was passed exactly to a fresh `bash --noprofile --norc -s` process
inside a PowerShell here-string. The transport invocation was
`$s | & 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -c 'tail -c +4 | bash --noprofile --norc -s'`;
`tail -c +4` removes only PowerShell's UTF-8 BOM before the fresh inner shell reads stdin.

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-partb-nul.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-partb-nul.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no; WPI_SS=/usr/bin/ss
printf 'LIS\0TEN 0 128 127.0.0.1:8790 0.0.0.0:*\n' > "$Q/ss.out"
wpi_capture(){ WPI_CAP_OUT="$Q/ss.out"; WPI_CAP_ERR="$EV_DIR/capture.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; }
wpi_assert_listener_set
```

Command rc: **0**. Observed output:

```text
B6_listener_inventory rows=1 port_8790_rows=1 evidence_file=/tmp/rp7-partb-nul.0t2kQN/ss.out content=not_printed table=complete parse=complete_before_semantics scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
COMMAND_RC=0
```

**Required repair:** perform a byte-preserving grammar preflight before Bash `read` can
discard NUL, and validate the numeric address and port grammar/range for every captured
row. Any NUL, invalid address, invalid port, truncation, or other record-grammar deviation
must STOP before `B6_listener_inventory ... parse=complete` is printed. Add D026 RED/GREEN
for the NUL record and at least one invalid-address/out-of-range-port record.

### 2. Truncated or invented status-parser result records become semantic FAILs instead of STOP - HIGH

**Locations:** `RP7-WPI-RO.sh:1185-1193`.

The parent checks only for disallowed characters. It does not require exact token count,
an expected field name, a field-specific expected type, or a 64-hex mismatch digest.
Consequently `TYPE state str` (missing `expected_type`) becomes an rc-1 host-state FAIL;
`MISMATCH state abc` and `MISMATCH rogue <64hex>` also become FAIL. These records do not
prove that a required response field was present with a wrong type/value. They are grammar
deviations and must STOP.

Executed body (same fresh-shell transport convention as finding 1):

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-partb-type.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-partb-type.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_sha_file(){ WPI_LINE=0000000000000000000000000000000000000000000000000000000000000000; }
wpi_capture(){ local label="$1"; WPI_CAP_OUT="$EV_DIR/$label.out"; WPI_CAP_ERR="$EV_DIR/$label.err"; : > "$WPI_CAP_ERR"; case "$label" in status_get) printf '200\n' > "$WPI_CAP_OUT"; WPI_CAP_RC=0 ;; status_json) printf 'TYPE state str\n' > "$WPI_CAP_OUT"; WPI_CAP_RC=5 ;; esac; }
wpi_assert_status
```

Command rc: **1**. Observed output:

```text
B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=
COMMAND_RC=1
```

**Required repair:** define and enforce the exact child-result grammar before semantic
classification. `MISSING` must name exactly one preregistered field; `TYPE` must carry
exactly the field, actual type, and the correct field-specific expected type; `MISMATCH`
must carry exactly a preregistered field and 64 lowercase hex. All other shapes STOP. Add
D026 cases for missing tokens, surplus tokens, unknown fields, wrong expected-type tokens,
and short/non-hex digests.

### 3. Invalid HTTP status tokens are reported as completed endpoint deviations - MEDIUM

**Location:** `RP7-WPI-RO.sh:1145`.

The case arm treats every three-decimal-digit string as a valid HTTP response. The
preregistration permits FAIL only for a complete, valid non-200 response and assigns
incomplete/malformed response evidence to STOP. `000` (curl's no-response sentinel) and
`600` are outside the admitted HTTP status range, yet both become B5 FAIL.

Executed body (same fresh-shell transport convention):

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-partb-http.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-partb-http.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"; WPI_PROBE_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
wpi_capture(){ WPI_CAP_OUT="$EV_DIR/code.out"; WPI_CAP_ERR="$EV_DIR/code.err"; printf '000\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; WPI_CAP_RC=0; }
wpi_assert_status
```

Command rc: **1**. Observed output:

```text
B5_FAIL reason=status_endpoint_unexpected_http code=000
COMMAND_RC=1
```

**Required repair:** accept only valid HTTP status grammar/range before applying the
401/403/200/other classification; at minimum, `000` and values outside 100-599 must STOP.
Add D026 RED/GREEN for `000`, `099`, `600`, and one valid non-200 control.

### 4. The published evidence command masks fence failures and is not bounded - MEDIUM

**Locations:** `SELF_QA_RP7.md:25`, `:41-42`, `:50`.

The current command is content-anchored and presently reproduces, but each fence command
is followed by `printf`. Therefore the overall extracted command returns the final
`printf` rc, not the failing fence rc. It can report both inner failures while returning
0. The same two `bash` invocations have no outer timeout, and the document supplies no
aggregate bound; the successful 188.127-second run proves termination only for this run,
not the claimed bounded command contract.

Executed structural falsification of the published `bash; printf; bash; printf` sequence:

```bash
Q=$(mktemp -d /tmp/rp7-partb-rcmask.XXXXXX) || exit 97
cleanup(){ case "$Q" in /tmp/rp7-partb-rcmask.*) rm -rf -- "$Q" ;; *) exit 98 ;; esac; }
trap cleanup EXIT
printf 'exit 7\n' > "$Q/r5.sh"
printf 'exit 9\n' > "$Q/r4.sh"
bash --noprofile --norc "$Q/r5.sh"; printf 'R5_FENCE_RC=%s\n' "$?"
bash --noprofile --norc "$Q/r4.sh"; printf 'R4_FENCE_RC=%s\n' "$?"
```

Command rc: **0**. Observed output:

```text
R5_FENCE_RC=7
R4_FENCE_RC=9
OUTER_COMMAND_RC=0
```

Static bound inspection, rc 0:

```text
EXACT_BLOCK_BASH_FENCE_INVOCATIONS=2
EXACT_BLOCK_OUTER_TIMEOUT_WRAPPERS=0
DOCUMENTED_AGGREGATE_BOUND_MENTIONS=0
```

**Required repair:** capture both fence rc values, print them, and exit nonzero if either
is nonzero. Put each fence (or the whole two-fence run) under an explicit enforced timeout
with a documented aggregate bound and a distinct timeout result. Re-run the exact command
from fresh Git Bash and record outer rc, inner rc values, elapsed time, summary, and stderr.
Add a falsification showing a deliberately failing/hanging extracted fence makes the
published command return nonzero within the declared bound.

## Confirmed conforming points

- The two accepting adjudicators use the bound `WPI_PYTHON3` with requested `-I -S`.
  Each child refuses output unless `sys.flags.isolated`, `sys.flags.no_site`, and absence
  of `site`, `sitecustomize`, and `usercustomize` are reported from inside the child. The
  accepting isolation wording does not claim more than the bound path, requested flags,
  and child-reported startup state.
- Runtime B5/B6 order is real: `wpi_main` executes netns binding, then status, then the
  listener set. The published runtime extraction and an independent stubbed-main run both
  returned `netns,status,listener`.
- The ordinary two-record permutation required by round 4 is correct: both orders STOP
  on a short malformed record before any semantic FAIL. Finding 1 is a separate byte-
  grammar hole that bypasses that field-count check.
- Row 24 is explicitly operator-side and not evaluated or claimed by RP7.
- All published evidence extractors are content-anchored, their own invocation text cannot
  re-open a range, and no absolute line range remains in `SELF_QA_RP7.md`.

## Freeze-gate items acknowledged, not findings

`WPI_FIXED_TRUSTED_PYTHON`,
`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT`, and the accepting `wpi_validate_inputs` branch remain
`<PIN-AT-FREEZE>`. No whole-block accepting run was expected or attempted. Section 8.2
rows 1-9 are implemented by no block and were not reviewed in this Part B run.

Minimum accepting Part-B repair set: make listener parsing byte-preserving and strict;
make every malformed child-result and invalid HTTP status STOP; make the published command
propagate fence failure and enforce/document its bound; then repeat this Part-B audit on
one frozen byte identity. The five round-5 repairs and rows 10-19 remain outside this
report's scope.

# WP-I transport set self-QA

Status: **PASS — AUTHORED-PENDING-AUDIT**

Date: 2026-08-10. Scope was local authoring and local fixtures only. No SSH,
SCP, host IP, remote host, credential, service, broker, exchange, or trading
operation was contacted or executed. The only sockets opened were temporary
`127.0.0.1` listeners/connect attempts for op-06 classification fixtures.
No RUNID was allocated; every `<ALLOCATE-AT-DISPATCH>` marker remains literal.

Random `mktemp`/GUID roots in the real output below are rendered as `<QA>`.
This is the only normalization. Commands are complete paste-and-run commands;
no undeclared shell state or hand substitution is required.

## 1. Accepted-source identity precondition

Command (PowerShell 5.1):

```powershell
$b='MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08'
$p=@("$b\02_PREREG\transport_runner.ps1","$b\04_PREREG_R45B\transport_runner.ps1","$b\02_PREREG\remote_setup.sh","$b\02_PREREG\remote_extract_verify.sh","$b\02_PREREG\remote_close_tree.sh")
foreach($f in $p){$i=Get-Item -LiteralPath $f; "$(Split-Path $f -Leaf)`t$($i.Length)`t$((Get-FileHash -Algorithm SHA256 -LiteralPath $f).Hash.ToLowerInvariant())"}
```

Real output:

```text
transport_runner.ps1  18095  c5bdb47c9adf5cb65405656786d9da6b649d5ba66cc5ef2618244f098e0b25ed
transport_runner.ps1  17849  a48ddc93ace627630b5c95e578799d60e56ae8aaaf75e35660a682234c841b9b
remote_setup.sh        4976   faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5
remote_extract_verify.sh 8270 ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3
remote_close_tree.sh   7470   87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
```

Verdict: PASS. The derivations below started from the accepted bytes.

## 2. Derivation minimality — full diffs

Commands:

```powershell
git diff --no-index -- 'MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG\remote_setup.sh' 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\remote_setup_wpi.sh'
git diff --no-index -- 'MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG\remote_extract_verify.sh' 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\remote_extract_verify_wpi.sh'
```

Full setup diff (the three-byte prefix contraction is the only change):

```diff
@@ -12,7 +12,7 @@
 # evaluate — never re-read as "absent" or as success).
 set -Eeuo pipefail
 
-EXPECT_PREFIX='/home/gatea/wpl_p2_staging_'
+EXPECT_PREFIX='/home/gatea/wpi_staging_'
 EXPECT_OWNER='gatea:gatea'
 EXPECT_MODE='700'
```

Full extractor diff (all executable changes are the WP-I archive constants,
their six-member count literals, and their truthful result text):

```diff
@@ -4,12 +4,12 @@
 #   bash -s -- <REMOTE_ARCHIVE> <EXTRACT_DIR> <EXPECTED_ARCHIVE_SHA256>
 #
 # It re-hashes the archive BEFORE reading its member list, refuses any member
-# that is not one of the nine preregistered basenames, extracts into a fresh
+# that is not one of the six preregistered basenames, extracts into a fresh
 # create-once directory, makes every extracted file read-only, and verifies
-# the nine block hashes frozen in Stage 1.
+# the six block hashes frozen in Stage 1.
 #
 # It NEVER executes a proposal block. Sourcing, running, `bash -n`-ing or
-# `python3`-ing a block is out of scope here: this operation ends with nine
+# `python3`-ing a block is out of scope here: this operation ends with six
 # verified read-only files on disk and nothing having been evaluated.
@@ -25,26 +25,20 @@
-# --- Stage 1 frozen identities (source commit 4c0d5fc5aeb1e069cd6171c11d143ac2a49a6e2c)
-EXPECT_ARCHIVE_BYTES='102400'
+# --- WP-I STAGE 1 FREEZE CONSTANTS: replace placeholders, change no logic ---
+EXPECT_ARCHIVE_BYTES='<PIN-AT-FREEZE>'
 MEMBERS='RP0-LIB.sh
 RP0-BOOTSTRAP.sh
-RP1-B3.sh
-RP3-C2A-POST.sh
-RP3-C2B-POST.sh
-RP4-C3.py
-RP5-C4A.sh
-RP5-C4B.sh
-RP5-C4C.sh'
-HASHES='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48  RP0-LIB.sh
-e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33  RP0-BOOTSTRAP.sh
-f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af  RP1-B3.sh
-e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27  RP3-C2A-POST.sh
-26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412  RP3-C2B-POST.sh
-0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5  RP4-C3.py
-a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2  RP5-C4A.sh
-10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e  RP5-C4B.sh
-de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8  RP5-C4C.sh'
+RP6-P0.sh
+RP7-WPI-RO.sh
+run_p0.sh
+run_ro.sh'
+HASHES='<PIN-AT-FREEZE>  RP0-LIB.sh
+<PIN-AT-FREEZE>  RP0-BOOTSTRAP.sh
+<PIN-AT-FREEZE>  RP6-P0.sh
+<PIN-AT-FREEZE>  RP7-WPI-RO.sh
+<PIN-AT-FREEZE>  run_p0.sh
+<PIN-AT-FREEZE>  run_ro.sh'
@@
-# --- 2. member list: exactly nine regular members, exact names, exact order --
+# --- 2. member list: exactly six regular members, exact names, exact order --
@@
-# or a member count other than nine is a FAIL, not a warning.
+# or a member count other than six is a FAIL, not a warning.
@@
-[ "$TYPE_COUNT" -eq 9 ] || fail "tar_member_count=$TYPE_COUNT expected=9"
+[ "$TYPE_COUNT" -eq 6 ] || fail "tar_member_count=$TYPE_COUNT expected=6"
@@
-[ "$NAME_COUNT" -eq 9 ] || fail "tar_name_count=$NAME_COUNT expected=9"
+[ "$NAME_COUNT" -eq 6 ] || fail "tar_name_count=$NAME_COUNT expected=6"
@@
-note "members_exact count=9 order=stage1"
+note "members_exact count=6 order=stage1"
@@
-# The extracted tree must be exactly nine regular files and nothing else: no
+# The extracted tree must be exactly six regular files and nothing else: no
@@
-[ "$FILE_COUNT" -eq 9 ] || fail "extracted_file_count=$FILE_COUNT expected=9"
+[ "$FILE_COUNT" -eq 6 ] || fail "extracted_file_count=$FILE_COUNT expected=6"
@@
-# --- 6. the nine Stage 1 hashes ---------------------------------------------
+# --- 6. the six Stage 1 hashes ----------------------------------------------
@@
-printf 'EXTRACT PASS archive=%s archive_sha256=%s dir=%s members=9 verified=9 executed=0\n' \
+printf 'EXTRACT PASS archive=%s archive_sha256=%s dir=%s members=6 verified=6 executed=0\n' \
```

Verdict: PASS. `RP1-B3.sh` is absent. Ordering is exactly RP0-LIB,
RP0-BOOTSTRAP, RP6-P0, RP7-WPI-RO, run_p0, run_ro. Concrete bytes and member
digests remain `<PIN-AT-FREEZE>`.

## 3. Wrapper symlink and ssh-stdin RED/GREEN

Exact command (PowerShell 5.1; it sends an UTF-8 test program to local WSL):

```powershell
$bash=@'
set -Eeuo pipefail
D=/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
Q=$(mktemp -d); trap 'rm -rf -- "$Q"' EXIT
make_case(){ kind=$1; C="$Q/$kind"; E="$C/extracted"; mkdir -p "$E" "$C/evidence/runkit"; printf 'rp0_require_safe_component(){ return 0; }\nrp0_allocate_evidence_dir(){ return 0; }\n' >"$E/RP0-LIB.sh"; printf 'EV_DIR="$EV_RUNKIT/$RUNID"\nmkdir -m 0700 -- "$EV_DIR"\nEV_LOG="$EV_DIR/${EV_STAGE_ID}.log"\n: >"$EV_LOG"\nexec >>"$EV_LOG" 2>&1\n' >"$E/RP0-BOOTSTRAP.sh"; if [ "$kind" = p0 ]; then T=RP6-P0.sh; P=P0W; W=run_p0.sh; else T=RP7-WPI-RO.sh; P=ROW; W=run_ro.sh; fi; printf 'if IFS= read -r stolen; then printf '\''%s_FIXTURE stdin=stolen\\n'\''; exit 1; fi\nprintf '\''%s_FIXTURE stdin=eof\\n'\''\n' "$P" "$P" >"$E/$T.real"; L=$(sha256sum "$E/RP0-LIB.sh"); L=${L%% *}; B=$(sha256sum "$E/RP0-BOOTSTRAP.sh"); B=${B%% *}; H=$(sha256sum "$E/$T.real"); H=${H%% *}; sed -e "s|^BASE_RUN=.*|BASE_RUN='QA'|" -e "s|^REMOTE_BASE=.*|REMOTE_BASE='$C'|" -e "s|^EXTRACT_DIR=.*|EXTRACT_DIR='$E'|" -e "s|^RUNID=.*|RUNID='QA-$kind'|" -e "s|^EV_PARENT=.*|EV_PARENT='$C/evidence'|" -e "s|^EV_RUNKIT=.*|EV_RUNKIT='$C/evidence/runkit'|" -e "s|^RP0_LIB_SHA=.*|RP0_LIB_SHA='$L'|" -e "s|^RP0_BOOTSTRAP_SHA=.*|RP0_BOOTSTRAP_SHA='$B'|" -e "s|^RP6_P0_SHA=.*|RP6_P0_SHA='$H'|" -e "s|^RP7_WPI_RO_SHA=.*|RP7_WPI_RO_SHA='$H'|" "$D/$W" >"$C/wrapper.sh"; printf '%s|%s|%s\n' "$C" "$E" "$T"; }
stream(){ { cat "$1"; printf "printf 'TAIL_EXECUTED\\n'\\n"; } | bash --noprofile --norc -s; }
for k in p0 ro; do IFS='|' read -r C E T < <(make_case "$k"); ln -s "$T.real" "$E/$T"; sed '/\[ ! -L "\$path" \] ||/d' "$C/wrapper.sh" >"$C/red-link.sh"; echo "=== $k LINK RED ==="; set +e; stream "$C/red-link.sh"; r=$?; set -e; cat "$C/evidence/runkit/QA-$k/$k.log"; echo RC=$r; rm -rf "$C/evidence/runkit/QA-$k"; echo "=== $k LINK GREEN ==="; set +e; stream "$C/wrapper.sh"; r=$?; set -e; echo RC=$r; rm "$E/$T"; cp "$E/$T.real" "$E/$T"; sed "s|\. \"\$EXTRACT_DIR/$T\" </dev/null|. \"\$EXTRACT_DIR/$T\"|" "$C/wrapper.sh" >"$C/red-stdin.sh"; echo "=== $k STDIN RED ==="; set +e; stream "$C/red-stdin.sh"; r=$?; set -e; cat "$C/evidence/runkit/QA-$k/$k.log"; echo RC=$r; rm -rf "$C/evidence/runkit/QA-$k"; echo "=== $k STDIN GREEN ==="; set +e; stream "$C/wrapper.sh"; r=$?; set -e; cat "$C/evidence/runkit/QA-$k/$k.log"; echo RC=$r; done
'@
$bash=$bash -replace "`r`n","`n"
$b64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($bash))
wsl.exe bash -c "printf %s '$b64' | base64 -d | bash -s"
```

Real result (both wrappers produced the same polarity):

```text
=== p0 LINK RED ===
P0W_FIXTURE stdin=eof
P0W done runid=QA-p0
TAIL_EXECUTED
RC=0
=== p0 LINK GREEN ===
P0W_STOP reason=block_is_symlink path=<QA>/p0/extracted/RP6-P0.sh
RC=3
=== p0 STDIN RED ===
P0W_FIXTURE stdin=stolen
RC=1
=== p0 STDIN GREEN ===
P0W_FIXTURE stdin=eof
P0W done runid=QA-p0
TAIL_EXECUTED
RC=0
=== ro LINK RED ===
ROW_FIXTURE stdin=eof
ROW done runid=QA-ro
TAIL_EXECUTED
RC=0
=== ro LINK GREEN ===
ROW_STOP reason=block_is_symlink path=<QA>/ro/extracted/RP7-WPI-RO.sh
RC=3
=== ro STDIN RED ===
ROW_FIXTURE stdin=stolen
RC=1
=== ro STDIN GREEN ===
ROW_FIXTURE stdin=eof
ROW done runid=QA-ro
TAIL_EXECUTED
RC=0
```

Verdict: PASS. Removing `-L` refusal admits the symlink (RED); current bytes
STOP. Removing only the target-block `</dev/null` lets the child consume the
wrapper stream (RED); current bytes preserve the tail (GREEN).

## 4. Wrapper STOP-first propagation

The same wrapper fixture generator was run with RP6 emitting
`P0_STOP reason=missing_tool tool=systemctl; exit 3` and RP7 first emitting a
partial writable-path fixture line, then
`B3_STOP reason=walk_incomplete ...; exit 3`.

Real output:

```text
=== P0_STOP_FIRST_PROPAGATION ===
P0_STOP reason=missing_tool tool=systemctl
RC=3
=== RO_STOP_FIRST_PROPAGATION ===
B3_fixture_partial_stdout path=/fixture/writable
B3_STOP reason=walk_incomplete root=/fixture rc=13 detail=fixture_partial_stdout_discarded
RC=3
```

Verdict: PASS. Neither wrapper turns inability-to-evaluate into FAIL/PASS, and
the RO fixture does not classify the earlier partial stdout as a writable-path
FAIL.

## 5. Changed setup/extractor constants — RED/GREEN

The exact local fixture commands create only `mktemp` trees, rewrite only the
prefix/owner for a sandbox-equivalent setup success, and replace only freeze
placeholders with fixture values for extraction. No host path is created.

Real setup output:

```text
=== RED_OLD_REFUSES_WPI ===
SETUP_FAIL reason=base_prefix base=[/home/gatea/wpi_staging_SAFE] expected_prefix=[/home/gatea/wpl_p2_staging_]
RC=1
=== GREEN_NEW_ACCEPTS_WPI_SANDBOX ===
SETUP_NOTE base_component_ok value=SAFE
SETUP PASS base=<QA>/wpi_staging_SAFE ... owner=root:root mode=700
RC=0
=== RED_OLD_ACCEPTS_WPL_SANDBOX ===
SETUP_NOTE base_component_ok value=SAFE
SETUP PASS base=<QA>/wpl_p2_staging_SAFE ... owner=root:root mode=700
RC=0
=== GREEN_NEW_REFUSES_WPL ===
SETUP_FAIL reason=base_prefix base=[/home/gatea/wpl_p2_staging_SAFE] expected_prefix=[/home/gatea/wpi_staging_]
RC=1
```

Additional current-byte refusals:

```text
REFUSE_DOTDOT     SETUP_FAIL reason=base_component_reserved value=[..]       RC=1
REFUSE_NESTED     SETUP_FAIL reason=base_component_charset value=[safe/nested] RC=1
REFUSE_EMPTY_SUFFIX SETUP_FAIL reason=base_component_reserved value=[]      RC=1
REFUSE_EMPTY_ARG  SETUP_FAIL reason=base_prefix base=[] expected_prefix=[/home/gatea/wpi_staging_] RC=1
```

Real extractor output:

```text
=== RED_OLD_ACCEPTS_NINE_WITH_RP1 ===
EXTRACT_NOTE members_exact count=9 order=stage1
EXTRACT PASS ... members=9 verified=9 executed=0
RC=0
=== GREEN_NEW_REFUSES_NINE_WITH_RP1 ===
EXTRACT_FAIL reason=tar_member_count=9 expected=6
RC=1
=== RED_OLD_REFUSES_WPI_SIX ===
EXTRACT_FAIL reason=tar_member_count=6 expected=9
RC=1
=== GREEN_NEW_ACCEPTS_WPI_SIX ===
EXTRACT_NOTE members_exact count=6 order=stage1
EXTRACT PASS ... members=6 verified=6 executed=0
RC=0
```

Verdict: PASS. The old constants make both WP-I operations impossible; the
new constants reverse exactly those outcomes and exclude RP1-B3.

## 6. Runner TSV reader — all three completion cases

The executed PowerShell fixture copied the runner to a GUID directory, replaced
only its directory/record/hash pins, emptied the archive pin list, and supplied
a one-row local `tcp_probe` plan. It used `File.WriteAllText` with explicit
UTF-8-no-BOM and LF.

Real output:

```text
=== CLEAN EOF ===
TR_PLAN_READ completion=clean_eof records=2
TR_DRY_RUN no_process_was_started no_connection_was_opened
RC=0
=== UNTERMINATED FINAL RECORD ===
TR_STOP reason=plan_unterminated_final_record path=<QA>\TRANSPORT_PLAN.tsv
RC=3
=== HARD READ ERROR ===
TR_STOP reason=plan_read_error detail=System.Management.Automation.MethodInvocationException path=<QA>\TRANSPORT_PLAN.tsv
RC=3
```

Verdict: PASS. Clean EOF is accepted; a populated unterminated record and a
directory-as-source hard read error are distinct STOPs. No partial row reached
the parser.

## 7. Runner first-FAIL RED/GREEN and per-op capture

The local-only fixture plan used four loopback probes. Op 01 deliberately
expected rc 1 while a closed port classified rc 0; op 02 was `sequence_ok`;
ops 03/04 were `always`. RED replaced only the skip predicate with `$false`.

```text
=== FIRST_FAIL_RED ===
TR_FIRST_FAIL id=01 rc=0 expected=1 later_sequence_ops=skip always_ops=run
TR_OP_BEGIN id=02 kind=tcp_probe cwd=<QA>
TR_OP_BEGIN id=03 kind=tcp_probe cwd=<QA>
TR_OP_BEGIN id=04 kind=tcp_probe cwd=<QA>
RC=1
=== FIRST_FAIL_GREEN ===
TR_FIRST_FAIL id=01 rc=0 expected=1 later_sequence_ops=skip always_ops=run
TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
TR_OP_BEGIN id=03 kind=tcp_probe cwd=<QA>
TR_OP_BEGIN id=04 kind=tcp_probe cwd=<QA>
RC=1
```

The GREEN record contained, for every op, `.argv`, `.stdout`, `.stderr`, `.rc`
and `.elapsed_ms`. `02.rc=skipped`, `02.elapsed_ms=0`, and
`TRANSPORT_SHA256SUMS.txt` contained `TRANSPORT_RECORD.txt`.

Verdict: PASS. The mutation proves the fixture detects the sequencing defect;
current code skips the later conditional op and still executes every `always`
op.

## 8. External TCP probe classification

All endpoints were loopback fixtures. No payload was sent. RED changed only
the enum compared with `ConnectionRefused` to `TimedOut`.

```text
=== PROBE_REFUSED_RED_WRONG_ENUM_MUTATION ===
B6_STOP reason=external_probe_not_evaluable outcome=socket_error rc=3 detail=ConnectionRefused
RC=1
=== PROBE_REFUSED_GREEN ===
B6_external row=24 outcome=connection_refused host=127.0.0.1 port=58341 payload_bytes=0
RC=0
=== PROBE_CONNECTED ===
B6_FAIL reason=host_reachable_8790 outcome=connected host=127.0.0.1 port=64404 payload_bytes=0
RC=0
=== PROBE_NOT_EVALUABLE ===
B6_STOP reason=external_probe_not_evaluable outcome=port_invalid rc=3 detail=port_range
RC=0
```

The runner also has a bounded `timeout` arm returning expected rc 0. A reliable
loopback-only timeout fixture is not available: a closed local port terminates
as `connection_refused`, while a listener terminates as `connected`. The branch
is therefore code-reviewed but not claimed as independently driven.

Verdict: PASS for the locally evaluable classifications. The RED mutation proves
the refused fixture discriminates the exact socket-error class. Windows
PowerShell 5.1's `MethodInvocationException` is unwrapped by type to its inner
`SocketException`; no localized diagnostic text is matched.

## 9. Syntax, plan grammar, placeholders, and draft fail-closed behavior

Commands:

```powershell
$d='MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
$e=$null; [Management.Automation.Language.Parser]::ParseFile((Resolve-Path "$d\transport_runner.ps1"),[ref]$null,[ref]$e)|Out-Null; if($e.Count){$e;exit 1}else{'POWERSHELL_5_1_PARSE PASS'}
$linux='/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT'
wsl.exe bash -n "$linux/run_p0.sh" "$linux/run_ro.sh" "$linux/remote_setup_wpi.sh" "$linux/remote_extract_verify_wpi.sh"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$d\transport_runner.ps1"; "RC=$LASTEXITCODE"
```

Real output:

```text
POWERSHELL_5_1_PARSE PASS
BASH_N PASS
TR_PLAN_READ completion=clean_eof records=13
TR_PLAN path=...\TRANSPORT_PLAN.tsv sha256=bcc10a6a71456580a93eb0da6c1f9bc03da154ae59cf14a0821e6b8bd6edd3b5
TR_STOP reason=plan_pin_unfilled expected=64_lower_hex
RC=3
```

Plan inspection: 12 ordered rows, nine fields each; kinds/run conditions are
`01 ssh_stdin sequence_ok`, `02 scp_up sequence_ok`, `03 ssh_stdin
sequence_ok`, `04 ssh_stdin sequence_ok`, `05 ssh_stdin sequence_ok`, `06
tcp_probe sequence_ok`, `07-08 ssh_stdin always`, `09-10 scp_down always`,
`11-12 local_bind always`. The TSV is LF-terminated and contains zero CR bytes.
The draft runner STOPs before any process/socket because its plan pin is still
unfilled; this is the required pre-freeze state.

## 10. Authored artifact identities

Command:

```powershell
$d='MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
foreach($n in 'run_p0.sh','run_ro.sh','transport_runner.ps1','TRANSPORT_PLAN.tsv','remote_setup_wpi.sh','remote_extract_verify_wpi.sh'){$p=Join-Path $d $n;$i=Get-Item $p;"$n`t$($i.Length)`t$((Get-FileHash -Algorithm SHA256 $p).Hash.ToLowerInvariant())"}
```

Real output:

```text
run_p0.sh                    3693   8b2c520aa342f3f49fc9f0ad543b6c8a918c995b66e1cae8a1dd1c543b9dbfe9
run_ro.sh                    4407   88f9f736e68c4978cc15d29621082d0395dc49de97a4c8efc79893fc536ad3e0
transport_runner.ps1        28946  84942683a6c25973f1785e48dc8ed76aea99be27c9ee50bf1ed5f7726b518cdc
TRANSPORT_PLAN.tsv           4575   bcc10a6a71456580a93eb0da6c1f9bc03da154ae59cf14a0821e6b8bd6edd3b5
remote_setup_wpi.sh          4973   5b2598184b228eef5d93c7f4ef7a5aa8a627ffbdea8c71e6cc093b416ebb0a34
remote_extract_verify_wpi.sh 7689   17ed8f3f8d80a79fc1b132ff1ef55cf0677da13c551da30e0db7531935c1f6f2
```

These are authoring identities only. Stage 1 changes marked placeholders,
re-runs this QA as applicable, and pins the resulting frozen bytes. No hash in
this section is a dispatch pin.

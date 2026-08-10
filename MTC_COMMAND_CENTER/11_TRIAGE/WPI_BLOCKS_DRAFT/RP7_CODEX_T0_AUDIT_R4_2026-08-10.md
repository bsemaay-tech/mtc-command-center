# BLOCK: 3 findings

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh-session flagship T0 slot. Direct
review under owner amendments A2/A2a; no delegation or sub-delegation.

Audited executable: `RP7-WPI-RO.sh` round-4 bytes at commit `d6a976aa`.
Worktree, commit blob and kickoff identity agree: 70,941 bytes, SHA-256
`23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`.
`bash -n` returned 0. No staging/live host was contacted, no network connection,
SSH/SCP, RUNID, credential, service action, deployment or repository source edit
was performed. The reported falsification fixtures used checked `/tmp/rp7-*`
trees and removed them.

The round-4 repairs for the two-phase listener parser, B5/B6 semantic order and
row-specific result grammar reproduce. Projection v2 also survives independent
subtree, prefix-boundary, escaped-field, last-tie, stacked-mount and malformed-
record probes. Acceptance is nevertheless blocked. The production main path never
binds the new `python3` tool, so an untrusted executable can forge an accepting
parser result and reach `RP7 PASS`. Separately, a readable but malformed
`*.dist-info` object is admitted by both universe gates and then silently omitted
by `verify_lock.py`, allowing a false parity PASS. Finally, the QA document's only
published “Exact command” contains a literal placeholder and is not executable or
content-anchored.

## V-row results

| V | Result | Evidence |
|---|---|---|
| **V1 - frozen-byte identity and syntax** | **PASS** | Worktree and `d6a976aa` blob both re-derived as 70,941 B / `23e55667...01aad`; `git diff --exit-code d6a976aa -- RP7-WPI-RO.sh` and Git Bash `bash -n` returned 0. |
| **V2 - published QA and D026 evidence** | **FAIL (evidence contract); executable assertions PASS** | The fence body, extracted by the `## The fence` and closing-fence content anchors, ran in Git Bash 5.2.37 / GNU coreutils 8.32 and ended `QA_PASS all_assertions=yes`, rc 0. The five round-3 RED/GREEN repairs reproduced. But `SELF_QA_RP7.md` publishes only `bash <fence-file>` as its “Exact command”; executed literally it is a syntax error, rc 2 (finding 3). Its ten-tool test is also a separately declared loop and therefore misses finding 1 in the real `wpi_main`. |
| **V3 - rows 10-24 and exact grammar** | **FAIL** | Rows 10-18, 19a and 20-24 match the preregistered principal FAIL/STOP forms; row 24 remains operator-side only. Row 19 can print the exact accepting parity line while one admitted `*.dist-info/METADATA` has no `Name` and was never adjudicated (finding 2). |
| **V4 - ordering rules** | **PASS** | Executed `B5B6_DECLARED_ORDER` is `netns,status,listener`; the two-deviation fixture yields B5 first. Both listener record permutations containing one malformed row STOP rc 3; a complete wildcard table still FAILs rc 1 only after `B6_listener_inventory ... parse=complete_before_semantics`. |
| **V5 - path-object binding and projection v2** | **FAIL for executed-tool binding; projection PASS** | The independent projection fixture changed digest for a mount below the release root, ignored a prefix lookalike, preserved `\\040`/`\\011`/`\\134`, selected the last equal-length mount, counted the stack, and STOPped duplicate IDs and an unterminated record. But `wpi_main` binds only nine tools and executes `WPI_PYTHON3` without the preregistered object binding (finding 1). |
| **V6 - STOP-vs-FAIL truthfulness** | **FAIL** | A malformed admitted metadata object whose package identity cannot be established is neither STOPped nor failed; it disappears from `installed_distributions()` and the block PASSes (finding 2). Listener, manager, walk, generic-verifier and network-namespace error classifications otherwise reproduced. |
| **V7 - probe execution environment and read-only scope** | **FAIL** | `-I -S`, cleared environment, fixed cwd and startup guards work when the selected executable is trustworthy. The executable is not bound in the real main path, however; an executable that ignores those flags wrote a marker, forged `OK fields=8`, and was reported as `parser=pinned_system_interpreter isolation=isolated_no_site` (finding 1). |
| **V8 - structured parsing and complete readers** | **FAIL** | Strict status JSON and the two-phase `ss` reader reproduced. The metadata driver enumerates the malformed object but does not validate a nonempty package identity or duplicates before handing it to a verifier that silently skips missing `Name` values (finding 2). |
| **V9 - local/read-only declared scope** | **FAIL only through finding 1** | Static scan found no forbidden row-16 descendant prefix and no implementation of operator-side row 24. Ordinary writes remain evidence leaves, but the unbound adjudicator can write anywhere the caller can; the fixture created a marker and still reached `RP7 PASS`. |

## Independently executed baseline evidence

### Frozen bytes, syntax and published fence

Commands:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
(Get-Item -LiteralPath 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh').Length
& 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -n '/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
& 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -c 'sed -n ''/^## The fence$/,/^```$/p'' /c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md | sed ''1,3d;$d'' | bash --noprofile --norc'
```

Observed rc/output:

```text
sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad
bytes=70941
bash_n_rc=0
...
BASH_N_RC=0 BYTES=70941 SHA256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad
QA_PASS all_assertions=yes
QA_FENCE_RC=0
```

The fence run took 159.9 s. Its load-bearing outputs included:

```text
PTH_FORGE_STATUS red_rc=0 red_marker=1 red_false_pass=1 green_rc=1 green_marker=0 green_truthful_fail=1
SITECUSTOMIZE_FORGE_PARITY red_rc=0 red_marker=1 red_false_pass=1 green_rc=1 green_marker=0 green_truthful_fail=1 clean_rc=0 clean_marker=0 clean_pass=1
NO_SITE_GUARD parity_rc=3 parity_refused=1 status_rc=3 status_refused=1
LISTENER_ORDER red_wildcard_first_rc=1 red_malformed_first_rc=3 green_wildcard_first_rc=3 green_malformed_first_rc=3 expected_both_stop=3
B5B6_DECLARED_ORDER wpi_assert_netns_binding,wpi_assert_status,wpi_assert_listener_set,
ROW_GRAMMAR_RCS r17_unread_red=3 r17_unread=3 r19a_unread_red=3 r19a_unread=3 r17_kind_red=1 r17_kind=1 r17_owner_red=1 r17_owner=1 r19a_owner_red=1 r19a_owner=1
```

### Independent projection-v2 attack

The production parser/projector was sourced by deleting only the content-anchored
`wpi_main "$@"` invocation. Synthetic tables contained: root only; a mount under the
release root with escaped root/mount/source fields; a release-root prefix lookalike; a
second mount stacked at `/`; duplicate mount IDs; and a newline-unterminated record.

Observed rc/output:

```text
PROJECTION_FALSIFICATION base=f3689267ee61071ddf6888e6f3d0299fe690b3c07bded7844f21d5939aa03e5f escaped=815bb57fb0ea78e5e16bb2f0fdeac3e28f7a01228b500a8084c952dac8b3fa28 outside=f3689267ee61071ddf6888e6f3d0299fe690b3c07bded7844f21d5939aa03e5f tie=fe378263de2b2e2fdf2ae614d8078b462198d018e6771dcfabcdd5d3318febea subtree_sensitive=yes boundary_clean=yes last_tie_sensitive=yes
kind=subtree subtree_root=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b seq=1 device=8:2 root=/src\040root mount_point=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/sub\011dir fstype=ext4 source=/dev/src\134x
kind=point path=/usr/bin/stat device=8:4 root=/ mount_point=/ fstype=tmpfs source=/dev/second shared_mount_point_records=2
RP7_STOP reason=mount_table_malformed ... record=2 detail=duplicate_mount_id
RP7_STOP reason=mount_table_unterminated_final_record ... records=0
PROJECTION_GRAMMAR duplicate_id_rc=3 unterminated_rc=3
```

No projection-v2 finding remains.

## Findings

### 1. The production main path never binds `python3`, so an untrusted executable can forge both “isolated” accepting claims and mutate state - BLOCK

**Locations:** `RP7-WPI-RO.sh:594-614` accepts and assigns the tenth pin;
`:443-456` includes it in projection v2; `:546-562` defines the required binding;
but the only production binding loop at `:1134-1137` lists
`stat readlink env find sha256sum systemctl ss curl timeout` and omits `python3`.
The unbound executable is then run at `:907` and `:1074`, and the accepting lines at
`:947` and `:1105` claim `adjudicator=pinned_system_interpreter` /
`parser=pinned_system_interpreter isolation=isolated_no_site`. This contradicts the
preregistration's trusted-interpreter requirement (§4) and instrument-attestation
vocabulary (§8.2).

The mount projection binds only mount topology, not the executable's leaf kind, numeric
ownership, mode or executable identity. `-I -S` and `sys.flags` are meaningful only if
the selected program is actually Python; a deviant executable can ignore the flags and
emit the exact accepted line. The published QA hid this because lines 541-556 declare a
new independent ten-name loop and call `wpi_bind_tool` directly rather than exercising
the tool list in `wpi_main`—Pattern 10, evidence that tests a helper but not its real
caller.

**Executed falsification command.** The following body was passed byte-for-byte to a
fresh `bash --noprofile --norc` process (the outer PowerShell step only Base64-encoded
the body to preserve quoting). All unrelated row functions are explicit no-ops. The
production `wpi_main`, `wpi_assert_status`, capture, stream-shape checks and acceptance
logic remain real. The `wpi_bind_tool` fixture would STOP if production called it for
`python3`; the deviant executable writes a marker and forges `OK fields=8` over an
`ARMED` body.

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-main-bind.XXXXXX)
source <(sed '/^wpi_main "\$@"$/d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
cat > "$Q/bad-python" <<EOF
#!/usr/bin/env bash
printf x > "$Q/marker"
printf 'OK fields=8\n'
EOF
chmod +x "$Q/bad-python"
cat > "$Q/curl" <<'EOF'
#!/usr/bin/env bash
out=
while [ "$#" -gt 0 ]; do
  if [ "$1" = --output ]; then out="$2"; shift 2; else shift; fi
done
printf '{"state":"ARMED"}\n' > "$out"
printf '200\n'
EOF
chmod +x "$Q/curl"
BOUND=
wpi_validate_inputs(){
  EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"; EV_LOG="$EV_DIR/log"; : > "$EV_LOG"
  WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=5
  WPI_SHA256SUM=/usr/bin/sha256sum; WPI_CURL="$Q/curl"; WPI_PYTHON3="$Q/bad-python"
  WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_TOOL_PINS=dummy
  WPI_PROBE_SEQ=0; WPI_MOUNT_SNAPSHOT_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
}
wpi_map_get(){ WPI_LINE="/usr/bin/$2"; }
wpi_bind_tool(){ BOUND="$BOUND$1,"; [ "$1" != python3 ] || { echo BINDING_WOULD_STOP_python3; exit 3; }; }
for f in wpi_assert_prerequisites wpi_mount_guard_begin wpi_mount_guard_end \
  wpi_assert_evidence_leaf_bound wpi_assert_manager_ready wpi_assert_tree \
  wpi_assert_metadata_dir wpi_assert_regular_digest wpi_assert_interpreter \
  wpi_assert_metadata_readable wpi_assert_lock_parity wpi_assert_netns_binding \
  wpi_assert_listener_set wpi_record_external_probe_boundary; do eval "$f(){ :; }"; done
wpi_main > "$Q/main.log" 2>&1
rc=$?
cat "$Q/main.log"
printf 'MAIN_BIND_FALSIFICATION rc=%s bound=[%s] python3_bound=%s malicious_marker=%s accepted_status=%s rp7_pass=%s\n' \
  "$rc" "$BOUND" "$(case "$BOUND" in *python3,*) echo yes;; *) echo no;; esac)" \
  "$([ -e "$Q/marker" ] && echo present || echo absent)" \
  "$(grep -c '^B5_status .*parser=pinned_system_interpreter' "$Q/main.log")" \
  "$(grep -c '^RP7 PASS$' "$Q/main.log")"
case "$Q" in /tmp/rp7-main-bind.*) rm -rf -- "$Q";; *) exit 97;; esac
```

Command rc: **0**. Observed output:

```text
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=8d3962231270c4a4099e67316f9ab15aad67dd86425feab010c00ad3b47e5360 content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site
RP7_claim establishes=rows_10_23_read_only_predicates_with_attested_preexec_objects_and_service_network_domain;executed_objects_use_separate_bounded_exec_after_preexec_mount_window
RP7 PASS
MAIN_BIND_FALSIFICATION rc=0 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,] python3_bound=no malicious_marker=present accepted_status=1 rp7_pass=1
FIXTURE_RC=0
```

**Required repair.** Add `python3` to the production `wpi_main` binding loop before the
initial mount window closes. Add D026 evidence that extracts or instruments the actual
main-path tool list rather than redeclaring it: current bytes must show the malicious
pin reaches an accepting line (RED), repaired bytes must call the real binding and STOP
before either adjudicator runs (GREEN). Keep the existing `-I -S` and startup guards;
they close the earlier venv-startup defect once the executable that interprets them is
actually bound.

### 2. A malformed admitted `*.dist-info` object is silently dropped, so row 19 can false-PASS a universe it did not semantically adjudicate - HIGH

**Locations:** `RP7-WPI-RO.sh:797-859` proves only object kind, ownership and byte
readability; the trusted driver at `:919-940` constructs a `PathDistribution` for every
admitted directory but does not require a valid `Name`/`Version` or unique canonical
name. The pinned verifier's `installed_distributions()` at
`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:68-74` silently skips every object whose
`METADATA` lacks `Name` and overwrites duplicate canonical names in a dictionary.

The preregistered universe is every direct-child `*.dist-info` directory, and its rule
says open/parse failures are STOP. A readable object whose package identity is absent is
not evidence that the installed set matches the lock. The round-4 report says malformed
cases are present, but the fence's `filedi` case is a non-directory object-kind case;
there is no malformed METADATA identity case. This is a real false PASS, not only a QA
coverage gap.

**Executed falsification command.** This content-anchored Git Bash fixture uses the
production metadata preflight, production trusted driver and real digest-bound
`verify_lock.py`. Only NTFS-unrepresentable numeric ownership/component/mount binding
and the MSYS-to-native Python argv plumbing are substituted, the same disclosed fixture
classes as the published QA. It creates one valid distribution matching the lock and a
second admitted/readable `z-ghost-9.0.dist-info` whose METADATA has `Version` but no
`Name`.

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
REPO_VERIFIER=/c/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py
Q=$(mktemp -d /tmp/rp7-meta-malformed.XXXXXX)
source <(sed '/^wpi_main "\$@"$/d' "$SCRIPT")
trap - ERR
set +E; set +e; set +u; set +o pipefail
EV_DIR="$Q/ev"; mkdir -p "$EV_DIR"
WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=10
WPI_FIND=/usr/bin/find; WPI_SHA256SUM=/usr/bin/sha256sum; WPI_PYTHON3=/c/Python314/python.exe
WPI_VENV_ROOT="$Q/venv"; WPI_RELEASE_ROOT="$Q/release"; WPI_EXPECTED_PACKAGES=1
WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
WPI_VENV_WALK_COMPLETE=yes; WPI_INTERPRETER_RAN=yes; WPI_PROBE_SEQ=0
WPI_MOUNT_SNAPSHOT_SEQ=0; WPI_MOUNT_GUARD_ACTIVE=no
SITE="$WPI_VENV_ROOT/lib/python3.12/site-packages"
VERDIR="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux"
mkdir -p "$SITE/a-demo-1.0.dist-info" "$SITE/z-ghost-9.0.dist-info" "$VERDIR"
tr -d '\r' < "$REPO_VERIFIER" > "$VERDIR/verify_lock.py"
cat > "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" <<'EOF'
demo-pkg==1.0 \
    --hash=sha256:0000000000000000000000000000000000000000000000000000000000000000
EOF
printf 'Metadata-Version: 2.1\nName: demo-pkg\nVersion: 1.0\n' > "$SITE/a-demo-1.0.dist-info/METADATA"
printf '\n' > "$SITE/a-demo-1.0.dist-info/RECORD"
printf 'Metadata-Version: 2.1\nVersion: 9.0\n' > "$SITE/z-ghost-9.0.dist-info/METADATA"
printf '\n' > "$SITE/z-ghost-9.0.dist-info/RECORD"
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
wpi_assert_metadata_readable > "$Q/preflight.log" 2>&1; preflight_rc=$?
wpi_assert_regular_digest(){ :; }
wpi_assert_lock_parity > "$Q/parity.log" 2>&1; parity_rc=$?
cat "$Q/preflight.log" "$Q/parity.log"
printf 'MALFORMED_METADATA_FALSIFICATION rc_preflight=%s rc_parity=%s metadata_dirs=%s malformed_name_fields=%s accepted_parity=%s\n' \
  "$preflight_rc" "$parity_rc" "$(find "$SITE" -maxdepth 1 -type d -name '*.dist-info' | wc -l)" \
  "$(grep -c '^Name:' "$SITE/z-ghost-9.0.dist-info/METADATA")" \
  "$(grep -c '^B1_lock_parity result=pass packages=1 ' "$Q/parity.log")"
case "$Q" in /tmp/rp7-meta-malformed.*) rm -rf -- "$Q";; *) exit 97;; esac
```

Command rc: **0**. Observed output:

```text
B1_metadata_readable path=.../z-ghost-9.0.dist-info/METADATA bytes_digest=sha256:ea16a1836e42d0ad9e46003d32c26c7ad59b352b8ad552620fa10c433a7854ea content=not_printed binding=window_open_pending_close
B1_metadata_universe root=.../site-packages entries=2 dist_info_dirs=2 non_metadata_entries=0 enumeration=unfiltered_maxdepth_1 universe=explicit_dist_info_only
B1_metadata_preflight root=.../site-packages dist_info_dirs=2 complete=yes readable=yes
B1_lock_parity result=pass packages=1 output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe
MALFORMED_METADATA_FALSIFICATION rc_preflight=0 rc_parity=0 metadata_dirs=2 malformed_name_fields=0 accepted_parity=1
FIXTURE_RC=0
```

**Required repair.** Before the verifier can emit any result, validate every admitted
`PathDistribution`: its METADATA must parse to one nonempty, grammar-valid `Name` and
`Version`, and canonical names must be unique. Missing/unparseable/ambiguous identity is
STOP, not a silently absent distribution and not a named mismatch. Add D026 fixtures for
missing Name, missing Version and duplicate canonical names; current bytes must false-
PASS where applicable, repaired bytes must STOP, and a valid unique universe must still
PASS.

### 3. The published “Exact command” is a literal placeholder and cannot rerun the QA fence - MEDIUM

**Location:** `SELF_QA_RP7.md:26-37`. The document calls the following its exact
command:

```text
bash <fence-file>            # exit status 0, terminal line QA_PASS all_assertions=yes
```

That is neither literal nor content-anchored: `<fence-file>` is a placeholder and the
shell parses its trailing `>` as an incomplete redirection. The document later says the
fence was re-extracted and byte-identically rerun, but records no extraction command or
digest. I independently built an anchored extractor and the fence PASSed; that proves
the body is runnable, not that the published evidence command meets the contract.

**Exact command run:**

```powershell
& 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -c 'cd /tmp && bash <fence-file>'
```

Command rc: **2**. Observed output:

```text
/usr/bin/bash: -c: line 1: syntax error near unexpected token `newline'
/usr/bin/bash: -c: line 1: `cd /tmp && bash <fence-file>'
LITERAL_QA_COMMAND_RC=2
```

**Required repair.** Publish the real content-anchored extraction-and-execution command
that selects the fenced body under the unique `## The fence` heading and stops at its
closing fence, with no line numbers and no placeholder. Record the extracted-body digest,
command rc and terminal `QA_PASS` from a fresh shell. The independently working command
used in this audit is shown in the baseline section and is one admissible form.

## Freeze-gate items acknowledged, not findings

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256='<PIN-AT-FREEZE>'` deliberately prevents
   the accepting `wpi_validate_inputs` arm until the deploy-channel value exists.
2. `WPI_FIXED_TRUSTED_PYTHON='<PIN-AT-FREEZE>'` is likewise deliberate. The absence of
   the final resolved `/usr/bin/python3.<minor>` value is not finding 1; finding 1 is that
   even a filled value is never passed through production `wpi_bind_tool`.
3. Row 24 remains correctly operator-side and is not evaluated by RP7.

## Audit limits

- No staging execution or real bind/overlay mount was attempted or authorised.
- The projection probes used exact synthetic mountinfo records with the production
  parser/projector.
- Native Python fixtures ran on local CPython 3.14.2; the repaired runtime guards are
  self-checking, and finding 1 does not depend on Python-version semantics because the
  deviant executable is reached before any trustworthy flag report exists.
- `shellcheck` is not installed; no ShellCheck result is claimed.

Minimum accepting repair set: bind `python3` in the real main path and falsify that
caller; semantically validate every admitted distribution identity before parity; and
replace the QA placeholder with a literal anchored rerun command. Then rerun both fresh
T0 flagship slots on one frozen byte identity.

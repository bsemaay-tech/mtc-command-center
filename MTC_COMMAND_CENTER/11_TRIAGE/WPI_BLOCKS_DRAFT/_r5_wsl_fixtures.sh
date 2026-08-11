#!/usr/bin/env bash
# Transport round-5 shell fixtures: BA-1 post-creation cleanup coverage, and the
# BA-2 falsification of the bare no-argument `declare -F` claim.
#
# Runs on a local Linux kernel (WSL2 Ubuntu). NO HOST IS CONTACTED and no
# network connection is made: every path is under $FIX on the local filesystem.
#
# D026. RED is the PRE-REPAIR close script read from the repository commit, not
# a reconstruction; GREEN is the working-tree file. Both arms are driven through
# the SAME deliberately mutated `mkdir` instrument, so the only variable is the
# delivered bytes.
#
# DECLARED FIXTURE RETARGETING, and nothing else, is applied to the delivered
# bytes to make them executable here - identical to round 4:
#   * every TOOL_* pin except TOOL_BASH is retargeted from /usr/bin/<t> to
#     $FIX/tools/<t>, because on this distribution the /usr/bin coreutils names
#     are symlinks and the delivered `require_tool` correctly refuses a symlink;
#     the copies are regular, root-owned, mode 0755. TOOL_BASH and the attested
#     interpreter stay /usr/bin/bash, which IS a regular root-owned file here.
#   * EXPECT_UID/EXPECT_GID are filled with this login's numeric identity.
#   * EXPECT_LAUNCH_HOME is filled with this login's HOME.
# One further mutation is DECLARED PER ARM and named in the banner: the admitted
# `mkdir` instrument, or the admitted `rm` instrument, is replaced by a wrapper
# with a stated behaviour. No predicate, classification, ordering or emitted
# record of the delivered bytes is altered.
set -u

CUR="$1"          # the WPI_BLOCKS_DRAFT directory (round-5 working-tree bytes)
PRE="$2"          # a directory holding the PRE-REPAIR round-4 close script
FIX=/root/wpi_r5

banner() { printf '\n########## %s\n' "$*"; }
run()    { printf '$ %s\n' "$*"; }

rm -rf "$FIX"
mkdir -p "$FIX/tools"
for t in stat sha256sum tr readlink find sort cmp rm mkdir env; do
    cp -L "/usr/bin/$t" "$FIX/tools/$t"
    chown 0:0 "$FIX/tools/$t"
    chmod 0755 "$FIX/tools/$t"
done
MYUID="$(id -u)"; MYGID="$(id -g)"; MYHOME="$HOME"
LAUNCH_ENV="$FIX/tools/env"
RUNID='WPIR5-FIXTURE-P0'

banner 'FIXTURE ENVIRONMENT'
run 'uname -sr; id -u; id -g; bash --version | head -1'
uname -sr; id -u; id -g; bash --version | head -1
run 'sha256sum <the two close scripts under test>'
sha256sum "$CUR/remote_close_tree_wpi.sh" "$PRE/remote_close_tree_wpi.sh"

mkfix() {
    local in="$1" out="$2"
    sed -e "s#^\(TOOL_\(STAT\|SHA256SUM\|TR\|READLINK\|FIND\|SORT\|CMP\|RM\|MKDIR\|ENV\)=\)'/usr/bin/\(.*\)'#\1'$FIX/tools/\3'#" \
        -e "s#^EXPECT_UID='<PIN-AT-FREEZE>'#EXPECT_UID='$MYUID'#" \
        -e "s#^EXPECT_GID='<PIN-AT-FREEZE>'#EXPECT_GID='$MYGID'#" \
        -e "s#^EXPECT_LAUNCH_HOME='/home/gatea'#EXPECT_LAUNCH_HOME='$MYHOME'#" \
        "$in" > "$out"
}
mkfix "$CUR/remote_close_tree_wpi.sh" "$FIX/close_green.sh"
mkfix "$PRE/remote_close_tree_wpi.sh" "$FIX/close_red.sh"

# Assert both anchors were actually hit, so a missed substitution throws instead
# of silently producing a false RED or GREEN.
for s in "$FIX/close_green.sh" "$FIX/close_red.sh"; do
    grep -q "^TOOL_MKDIR='$FIX/tools/mkdir'$" "$s" || { echo "ANCHOR MISS TOOL_MKDIR in $s" >&2; exit 9; }
    grep -q "^EXPECT_UID='$MYUID'$"            "$s" || { echo "ANCHOR MISS EXPECT_UID in $s" >&2; exit 9; }
done
echo 'RETARGET_ANCHORS=hit_in_both_arms'

# ---------------------------------------------------------------- instruments
# INSTRUMENT 1 (BA-1's exact case). A `mkdir` that CREATES the requested
# directory exactly as the real tool would, emits ONE diagnostic, and returns 0.
cat > "$FIX/tools/mkdir_diag" <<EOF
#!/usr/bin/bash
$FIX/tools/mkdir "\$@"
rc=\$?
printf 'injected_success_diagnostic\n' >&2
exit \$rc
EOF
# INSTRUMENT 2. A `mkdir` that creates NOTHING and returns 1.
cat > "$FIX/tools/mkdir_fail_clean" <<EOF
#!/usr/bin/bash
printf 'injected_failure_no_object_created\n' >&2
exit 1
EOF
# INSTRUMENT 3. A `mkdir` that CREATES the directory and then returns 1 - the
# case the repaired bytes deliberately do NOT claim to cover.
cat > "$FIX/tools/mkdir_fail_dirty" <<EOF
#!/usr/bin/bash
$FIX/tools/mkdir "\$@" 2>/dev/null
printf 'injected_failure_after_object_created\n' >&2
exit 1
EOF
# INSTRUMENT 4. An `rm` that reports success and removes nothing, to show the
# removal adjudication is live on the newly covered path.
cat > "$FIX/tools/rm_noop" <<EOF
#!/usr/bin/bash
exit 0
EOF
for i in mkdir_diag mkdir_fail_clean mkdir_fail_dirty rm_noop; do
    chown 0:0 "$FIX/tools/$i"; chmod 0755 "$FIX/tools/$i"
done

with_tool() {   # with_tool <src> <TOOL_NAME> <instrument> <dst>
    sed "s#^TOOL_$2='$FIX/tools/[a-z0-9]*'#TOOL_$2='$FIX/tools/$3'#" "$1" > "$4"
    grep -q "^TOOL_$2='$FIX/tools/$3'$" "$4" || { echo "ANCHOR MISS TOOL_$2 in $4" >&2; exit 9; }
}

mk_tree() {
    local base="$1"
    rm -rf "$base"
    mkdir -m 0700 -p "$base/evidence/runkit/$RUNID" "$base/work"
    chmod 0700 "$base" "$base/evidence" "$base/evidence/runkit" "$base/evidence/runkit/$RUNID" "$base/work"
    printf 'alpha\n' > "$base/evidence/runkit/$RUNID/a.txt"
    printf 'beta\n'  > "$base/evidence/runkit/$RUNID/b.txt"
}

launch() {   # launch <script> <args...> : the frozen round-4/5 launch domain
    local s="$1"; shift
    "$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
        /usr/bin/bash --noprofile --norc "$s" "$@"
}

# arm <label> <script> <base>  -- runs one arm and reports rc + residue
arm() {
    local label="$1" script="$2" base="$3"
    local ev="$base/evidence/runkit/$RUNID" work="$base/work" rc=0
    launch "$script" "$ev" "$RUNID" "$work" > "$FIX/$label.out" 2> "$FIX/$label.err" || rc=$?
    printf 'SCRIPT_RC=%s\n' "$rc"
    grep -E '^CLOSE_STOP |^CLOSE_FAIL ' "$FIX/$label.err" || printf '(no CLOSE_STOP/CLOSE_FAIL on stderr)\n'
    if [ -e "$work/close_work_$RUNID" ] || [ -L "$work/close_work_$RUNID" ]; then
        printf 'RESIDUE_PRESENT=yes path=%s\n' "$work/close_work_$RUNID"
        printf 'RESIDUE_LISTING:\n'; find "$work" | sort | sed 's/^/  /'
    else
        printf 'RESIDUE_PRESENT=no\n'
    fi
    printf 'EVIDENCE_TREE_AFTER:\n'; find "$ev" | sort | sed 's/^/  /'
}

banner 'BA-1 RED - PRE-REPAIR bytes + INSTRUMENT 1 (mkdir creates, warns, rc 0)'
echo '# Codex round-4 Band A reproduced SCRIPT_RC=3 ... RESIDUE_PRESENT=yes here:'
echo '# the directory is created at :401, the diagnostic branch stops at :402, and'
echo '# the cleanup trap is not installed until :424.'
with_tool "$FIX/close_red.sh" MKDIR mkdir_diag "$FIX/red_diag.sh"
mk_tree "$FIX/red_diag"
run 'env -i PATH=... LC_ALL=C HOME=... /usr/bin/bash --noprofile --norc close_red.sh <EV_DIR> <RUNID> <WORK_ROOT>'
arm red_diag "$FIX/red_diag.sh" "$FIX/red_diag"

banner 'BA-1 GREEN - REPAIRED bytes + THE SAME INSTRUMENT 1'
echo '# Same deviant tool output, same launch, same argv. The reasoned STOP is'
echo '# retained byte-for-byte (reason=work_dir_mkdir_diagnostics with the same'
echo '# detail), and the directory is gone because the cleanup is armed on the'
echo '# zero status BEFORE the diagnostic is adjudicated.'
with_tool "$FIX/close_green.sh" MKDIR mkdir_diag "$FIX/green_diag.sh"
mk_tree "$FIX/green_diag"
run 'env -i PATH=... LC_ALL=C HOME=... /usr/bin/bash --noprofile --norc close_green.sh <EV_DIR> <RUNID> <WORK_ROOT>'
arm green_diag "$FIX/green_diag.sh" "$FIX/green_diag"

banner 'BA-1 FENCE DISCRIMINATING POWER - old and new assertion, same deviant output'
echo '# The carried fence is `[ -z "$MKDIR_OUT" ] || stop work_dir_mkdir_diagnostics`.'
echo '# It was NOT weakened: the predicate and the reason token are unchanged, and'
echo '# both the pre-repair and the repaired assertion refuse the same injected'
echo '# diagnostic. Quoted from the two arms above:'
printf 'OLD_ASSERTION_LINE : %s\n' "$(grep -n 'MKDIR_OUT" \] || stop' "$PRE/remote_close_tree_wpi.sh")"
printf 'NEW_ASSERTION_LINE : %s\n' "$(grep -n 'MKDIR_OUT" \] || stop' "$CUR/remote_close_tree_wpi.sh")"
printf 'OLD_REFUSAL        : %s\n' "$(grep -h '^CLOSE_STOP ' "$FIX/red_diag.err" | tail -1)"
printf 'NEW_REFUSAL        : %s\n' "$(grep -h '^CLOSE_STOP ' "$FIX/green_diag.err" | tail -1)"

banner 'BA-1 REGRESSION - clean run, PRE-REPAIR bytes, no instrument'
mk_tree "$FIX/red_clean"
arm red_clean "$FIX/close_red.sh" "$FIX/red_clean"
grep -E '^CLOSE_NOTE scratch |^CLOSE PASS ' "$FIX/red_clean.out"

banner 'BA-1 REGRESSION - clean run, REPAIRED bytes, no instrument'
echo '# rc 0, the same record, no residue: the repair did not change the happy path.'
mk_tree "$FIX/green_clean"
arm green_clean "$FIX/close_green.sh" "$FIX/green_clean"
grep -E '^CLOSE_NOTE scratch |^CLOSE PASS ' "$FIX/green_clean.out"

banner 'BA-1 - a nonzero mkdir that created NOTHING: PRE-REPAIR vs REPAIRED'
echo '# Both STOP. The repaired arm additionally records the tool rc, the captured'
echo '# diagnostic, and whether an object is present - the round-4 message carried'
echo '# only the path.'
with_tool "$FIX/close_red.sh"   MKDIR mkdir_fail_clean "$FIX/red_failclean.sh"
with_tool "$FIX/close_green.sh" MKDIR mkdir_fail_clean "$FIX/green_failclean.sh"
mk_tree "$FIX/red_failclean";   arm red_failclean   "$FIX/red_failclean.sh"   "$FIX/red_failclean"
mk_tree "$FIX/green_failclean"; arm green_failclean "$FIX/green_failclean.sh" "$FIX/green_failclean"

banner 'BA-1 - THE DECLARED UNCOVERED CASE: a nonzero mkdir that DID create'
echo '# The repaired bytes deliberately do NOT arm cleanup here: a nonzero status'
echo '# is not evidence that the object at that path is the one this run created,'
echo '# and `rm -rf` on an object it cannot prove it created is the wrong answer.'
echo '# The header, the create block and the CLOSE_NOTE scratch field all say so.'
echo '# Residue in this arm is the honest scope of the claim, not a hidden failure:'
echo '# the record now NAMES it (object_after_failed_create=present).'
with_tool "$FIX/close_green.sh" MKDIR mkdir_fail_dirty "$FIX/green_faildirty.sh"
mk_tree "$FIX/green_faildirty"; arm green_faildirty "$FIX/green_faildirty.sh" "$FIX/green_faildirty"

banner 'BA-1 - the removal adjudication is LIVE on the newly covered path'
echo '# Instrument 1 (create + diagnostic + rc 0) plus an `rm` that reports success'
echo '# and removes nothing. The newly armed cleanup must not accept that.'
with_tool "$FIX/green_diag.sh" RM rm_noop "$FIX/green_diag_rmnoop.sh"
mk_tree "$FIX/green_rmnoop"; arm green_rmnoop "$FIX/green_diag_rmnoop.sh" "$FIX/green_rmnoop"

banner 'BA-1 - cleanup still covers a later refusal after a clean create'
echo '# A work-directory mode disagreement STOPs well after the create. Both arms'
echo '# had cleanup armed by then, so this is a control showing the repair did not'
echo '# move an exit path that round 4 already covered.'
for A in red green; do
    mk_tree "$FIX/${A}_mode"
    chmod 0755 "$FIX/${A}_mode/work"
    chmod 0700 "$FIX/${A}_mode/work"
    cp "$FIX/close_$A.sh" "$FIX/${A}_mode.sh"
    # The delivered `-m 0700` is honoured, so the refusal is driven by a wrapper
    # that widens the mode immediately after the real create returns 0.
    cat > "$FIX/tools/mkdir_wide_$A" <<EOF
#!/usr/bin/bash
$FIX/tools/mkdir "\$@"
rc=\$?
for a in "\$@"; do case "\$a" in /*) /usr/bin/chmod 0750 "\$a" 2>/dev/null ;; esac; done
exit \$rc
EOF
    chown 0:0 "$FIX/tools/mkdir_wide_$A"; chmod 0755 "$FIX/tools/mkdir_wide_$A"
    with_tool "$FIX/${A}_mode.sh" MKDIR "mkdir_wide_$A" "$FIX/${A}_mode_run.sh"
    printf '\n--- arm=%s\n' "$A"
    arm "${A}_mode" "$FIX/${A}_mode_run.sh" "$FIX/${A}_mode"
done

banner 'F1 OPEN - the outer account-shell boundary, reproduced locally'
echo '# SCOPE OF THIS ARM, STATED FIRST. This is NOT closure evidence and is NOT'
echo '# the real transport path. No host is contacted, no socket is opened and no'
echo '# ssh/sshd process is started. It is a LOCAL MODEL of one composition step'
echo '# that Codex round-4 Band B judged on the bytes: sshd does not execute the'
echo '# remote command string itself - it hands the string to the account shell,'
echo '# which processes its own startup environment BEFORE the string first token'
echo '# runs. The model is `BASH_ENV=<plant> /usr/bin/bash -c "<the frozen command'
echo '# string>" < <the delivered script>`. The command string is byte-identical to'
echo '# the frozen $REMOTE_LAUNCH_DOMAIN, and the delivered script is the REPAIRED'
echo '# round-5 file - so this shows the boundary is not closed BY the repair.'
mk_tree "$FIX/f1outer"
EV_O="$FIX/f1outer/evidence/runkit/$RUNID"
cat > "$FIX/plant_outer.sh" <<EOF
printf 'OUTER_ACCOUNT_SHELL_PLANT_RAN\n' >> $FIX/f1outer/hit
printf 'CLOSE PASS runid=%s dir=%s files=2 wrote_into_evidence_tree=0\n' "$RUNID" "$EV_O"
exit 0
EOF
rm -f "$FIX/f1outer/hit"
CMDSTR="/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=$MYHOME /usr/bin/bash --noprofile --norc -s -- $EV_O $RUNID $FIX/f1outer/work"
run "BASH_ENV=<exiting plant> /usr/bin/bash -c '<frozen command string>' < close_green.sh"
printf 'COMMAND_STRING=%s\n' "$CMDSTR"
BASH_ENV="$FIX/plant_outer.sh" /usr/bin/bash -c "$CMDSTR" \
    < "$FIX/close_green.sh" > "$FIX/f1outer.out" 2> "$FIX/f1outer.err"
printf 'RC=%s\n' "$?"
printf 'OUTER_PLANT_RAN=%s\n' "$( [ -f "$FIX/f1outer/hit" ] && echo yes || echo no )"
printf 'STDOUT:\n'; sed 's/^/  /' "$FIX/f1outer.out"
printf 'STDERR:\n'; sed 's/^/  /' "$FIX/f1outer.err"
printf 'DELIVERED_SCRIPT_RECORD_LINES=%s   (CLOSE_NOTE emitted by the real program)\n' \
    "$(grep -c '^CLOSE_NOTE ' "$FIX/f1outer.out")"
echo '# The runner would ACCEPT this capture: transport_runner.ps1 registers the'
echo '# prefixes CLOSE_ and "CLOSE " for the stdin leaf remote_close_tree_wpi.sh,'
echo '# and the forged line starts with one of them at an in-grammar rc 0. Marker'
echo '# SHAPE is bound to the plan row, not the process that produced it.'
echo '# CONTROL 1 - what the inner-child domain DOES still close. A plant that lets'
echo '# the delivered script RUN - the only kind that could forge a REAL-looking'
echo '# record rather than a bare line - is refused by name, because BASH_ENV is'
echo '# still in the exec environment the kernel recorded for the inner child:'
cat > "$FIX/plant_quiet.sh" <<EOF
printf 'QUIET_PLANT_RAN\n' >> $FIX/f1outer/hit_quiet
EOF
rm -f "$FIX/f1outer/hit_quiet"
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" "BASH_ENV=$FIX/plant_quiet.sh" \
    /usr/bin/bash --noprofile --norc "$FIX/close_green.sh" "$EV_O" "$RUNID" "$FIX/f1outer/work" 2>&1 | tail -1
printf 'RC=%s  QUIET_PLANT_RAN=%s\n' "${PIPESTATUS[0]}" \
    "$( [ -f "$FIX/f1outer/hit_quiet" ] && echo yes || echo no )"
echo '# CONTROL 2 - and what it does NOT close, even when BASH_ENV is delivered'
echo '# INSIDE the domain: an EXITING plant still forges, at rc 0. Round 4 recorded'
echo '# this case and (correctly) noted the frozen plan cannot introduce BASH_ENV'
echo '# into the env -i list. What round 4 got wrong, and Band B caught, is that'
echo '# the plan is not the only way in: the OUTER account shell above needs no'
echo '# plan row at all.'
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" "BASH_ENV=$FIX/plant_outer.sh" \
    /usr/bin/bash --noprofile --norc "$FIX/close_green.sh" "$EV_O" "$RUNID" "$FIX/f1outer/work" 2>&1 | tail -1
printf 'RC=%s\n' "${PIPESTATUS[0]}"

banner 'BA-2 - the claimed second `declare -F` defect, executed'
echo '# The round-4 report and five delivered scripts said bare `declare -F` exits 1'
echo '# when no function exists and would end the run under `set -Eeuo pipefail`.'
echo '# Arm D proves set -e IS armed in the same shell shape, so arm B falsifies'
echo '# the claim rather than merely failing to trigger it. Arm F is the'
echo '# discriminating-power check for KEEPING the guard as no-op hardening.'
printf 'BASH_VERSION=%s\n' "$BASH_VERSION"

printf '\n===== A. DIRECT no-argument declare -F in a function-free shell =====\n'
/usr/bin/bash --noprofile --norc -c 'declare -F; printf "DIRECT_RC=%s\n" "$?"'
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== B. UNGUARDED assignment under set -Eeuo pipefail (the claimed RED) =====\n'
/usr/bin/bash --noprofile --norc -c 'set -Eeuo pipefail; LD_FUNCS="$(declare -F)"; printf "AFTER_ASSIGN len=%s\n" "${#LD_FUNCS}"; printf "STILL_RUNNING=yes\n"'
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== C. CONTROL: a NAMED lookup of a missing function DOES exit 1 =====\n'
/usr/bin/bash --noprofile --norc -c 'set -Eeuo pipefail; LD_FUNCS="$(declare -F no_such_function_xyz)"; printf "REACHED_UNEXPECTEDLY\n"'
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== D. CONTROL: set -e really is armed in arm B (deliberate rc-1 command) =====\n'
/usr/bin/bash --noprofile --norc -c 'set -Eeuo pipefail; LD_FUNCS="$(false)"; printf "REACHED_UNEXPECTEDLY\n"'
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== E. The delivered guarded form, same function-free shell =====\n'
/usr/bin/bash --noprofile --norc -c 'set -Eeuo pipefail; LD_FUNCS="$(declare -F 2>/dev/null || :)"; printf "AFTER_ASSIGN len=%s\n" "${#LD_FUNCS}"'
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== F. DISCRIMINATING POWER: both forms still SEE an inherited function =====\n'
/usr/bin/bash --noprofile --norc -c 'foo() { :; }; export -f foo; /usr/bin/bash --noprofile --norc -c '"'"'set -Eeuo pipefail; U="$(declare -F)"; G="$(declare -F 2>/dev/null || :)"; printf "UNGUARDED=[%s]\nGUARDED=[%s]\n" "$U" "$G"'"'"''
printf 'PROCESS_RC=%s\n' "$?"

printf '\n===== G. the delivered scripts still refuse an inherited exported function =====\n'
mk_tree "$FIX/ba2fn"
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
    "BASH_FUNC_a_plant%%=() { :; }" \
    /usr/bin/bash --noprofile --norc "$FIX/close_green.sh" \
    "$FIX/ba2fn/evidence/runkit/$RUNID" "$RUNID" "$FIX/ba2fn/work" 2>&1 | tail -1
printf 'RC=%s\n' "${PIPESTATUS[0]}"

banner 'DONE'

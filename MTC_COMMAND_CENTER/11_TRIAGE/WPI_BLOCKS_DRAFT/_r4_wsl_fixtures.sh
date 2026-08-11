#!/usr/bin/env bash
# Transport round-4 shell fixtures: F1 launch domain, F2 run-owned scratch,
# F3 exact absence classification, T6 close-script composition.
#
# Runs on a local Linux kernel (WSL2 Ubuntu). NO HOST IS CONTACTED and no
# network connection is made: every path is under $FIX on the local filesystem.
#
# DECLARED FIXTURE RETARGETING, and nothing else, is applied to the delivered
# bytes to make them executable here:
#   * every TOOL_* pin except TOOL_BASH is retargeted from /usr/bin/<t> to
#     $FIX/tools/<t>, because on this distribution the /usr/bin coreutils names
#     are symlinks and the delivered `require_tool` correctly refuses a symlink;
#     the copies are regular, root-owned, mode 0755. TOOL_BASH and the attested
#     interpreter stay /usr/bin/bash, which IS a regular root-owned file here.
#   * EXPECT_UID/EXPECT_GID are filled with this login's numeric identity.
#   * EXPECT_LAUNCH_HOME is filled with this login's HOME.
# No predicate, classification, ordering or emitted record is altered.
set -u

SRC="$1"          # the WPI_BLOCKS_DRAFT directory (round-4 bytes)
R3="$2"           # a directory holding the round-3 bytes from commit 78173bfd
SUPER="$3"        # a directory holding the superseded cf049b6b close script
FIX=/root/wpi_r4

banner() { printf '\n########## %s\n' "$*"; }
sub()    { printf '\n--- %s\n' "$*"; }
run()    { printf '$ %s\n' "$*"; }

rm -rf "$FIX"
mkdir -p "$FIX/tools"
for t in stat sha256sum tr readlink find sort cmp rm mkdir env mktemp; do
    cp -L "/usr/bin/$t" "$FIX/tools/$t"
    chown 0:0 "$FIX/tools/$t"
    chmod 0755 "$FIX/tools/$t"
done
MYUID="$(id -u)"; MYGID="$(id -g)"; MYHOME="$HOME"
LAUNCH_ENV="$FIX/tools/env"

banner 'FIXTURE ENVIRONMENT'
run 'uname -sr; id -u; id -g'
uname -sr; id -u; id -g
run 'ls -l /usr/bin/bash /usr/bin/stat /usr/bin/env'
ls -l /usr/bin/bash /usr/bin/stat /usr/bin/env
run "ls -l $FIX/tools | head -4"
ls -l "$FIX/tools" | head -4

# Retarget the declared pins only.
mkfix() {
    local in="$1" out="$2"
    sed -e "s#^\(TOOL_\(STAT\|SHA256SUM\|TR\|READLINK\|FIND\|SORT\|CMP\|RM\|MKDIR\|ENV\|MKTEMP\)=\)'/usr/bin/\(.*\)'#\1'$FIX/tools/\3'#" \
        -e "s#^EXPECT_UID='<PIN-AT-FREEZE>'#EXPECT_UID='$MYUID'#" \
        -e "s#^EXPECT_GID='<PIN-AT-FREEZE>'#EXPECT_GID='$MYGID'#" \
        -e "s#^EXPECT_LAUNCH_HOME='/home/gatea'#EXPECT_LAUNCH_HOME='$MYHOME'#" \
        "$in" > "$out"
}
mkfix "$SRC/remote_close_tree_wpi.sh"   "$FIX/close_r4.sh"
mkfix "$R3/remote_close_tree_wpi.sh"    "$FIX/close_r3.sh"
mkfix "$SUPER/remote_close_tree_wpi.sh" "$FIX/close_super.sh"
mkfix "$SRC/remote_setup_wpi.sh"        "$FIX/setup_r4.sh"

# The round-3 close script compares the RENDERED owner name, so its fixture
# needs the rendered pair rather than the numeric one.
sed -i "s#^EXPECT_OWNER='gatea:gatea'#EXPECT_OWNER='$(id -un):$(id -gn)'#" "$FIX/close_r3.sh"

# The superseded edit refuses its own clean launch, so a second, EXPLICITLY
# MUTATED copy with only that self-refusal deleted is kept: it is the only way
# to observe what the rest of that edit does with a two-argument invocation.
sed -e '/^LD_FUNCS="\$(declare -F)"$/d' \
    -e '/^\[ -z "\$LD_FUNCS" \] || ld_stop "launch_domain_inherited_shell_function"$/d' \
    "$FIX/close_super.sh" > "$FIX/close_super_nofunc.sh"
printf 'superseded_selfstop_lines_deleted=%s\n' \
    "$(( $(wc -l < "$FIX/close_super.sh") - $(wc -l < "$FIX/close_super_nofunc.sh") ))"

# A tree to close: <parent>/runkit/<RUNID> with two regular files.
RUNID='WPIR4-FIXTURE-P0'
mk_tree() {
    local base="$1"
    rm -rf "$base"
    mkdir -m 0700 -p "$base/evidence/runkit/$RUNID" "$base/work"
    chmod 0700 "$base" "$base/evidence" "$base/evidence/runkit" "$base/evidence/runkit/$RUNID" "$base/work"
    printf 'alpha\n' > "$base/evidence/runkit/$RUNID/a.txt"
    printf 'beta\n'  > "$base/evidence/runkit/$RUNID/b.txt"
}

launch4() {   # launch4 <script> [args...] : the frozen round-4 launch domain
    local s="$1"; shift
    "$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
        /usr/bin/bash --noprofile --norc "$s" "$@"
}

banner 'F2 RED - round-3 bytes, TMPDIR pointed at the evidence tree'
echo '# The accepted round-3 close script inherits TMPDIR and calls mktemp. With'
echo '# TMPDIR set to the tree it is measuring it writes and hashes its own files'
echo '# inside evidence while printing wrote_into_evidence_tree=0.'
mk_tree "$FIX/f2red"
EV="$FIX/f2red/evidence/runkit/$RUNID"
run "TMPDIR=\$EV bash close_r3.sh \$EV $RUNID"
TMPDIR="$EV" /usr/bin/bash "$FIX/close_r3.sh" "$EV" "$RUNID" > "$FIX/f2red.out" 2> "$FIX/f2red.err"
echo "RC=$?"
echo '--- CLOSE_DIGEST lines (note the tmp.* member inside the evidence tree):'
grep -E '^CLOSE_DIGEST |^CLOSE PASS ' "$FIX/f2red.out" || true
echo '--- stderr:'; cat "$FIX/f2red.err"

banner 'F2 GREEN - round-4 bytes, same TMPDIR injection'
echo '# TMPDIR is not an entry the frozen launch domain delivers, so the class 5'
echo '# sweep refuses it by name before any external program runs. Independently,'
echo '# the round-4 bytes contain no mktemp at all.'
mk_tree "$FIX/f2green"
EV="$FIX/f2green/evidence/runkit/$RUNID"
run "env -i PATH=... LC_ALL=C HOME=... TMPDIR=\$EV /usr/bin/bash --noprofile --norc close_r4.sh \$EV $RUNID \$WORK"
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" "TMPDIR=$EV" \
    /usr/bin/bash --noprofile --norc "$FIX/close_r4.sh" "$EV" "$RUNID" "$FIX/f2green/work" \
    > "$FIX/f2green.out" 2> "$FIX/f2green.err"
echo "RC=$?"
cat "$FIX/f2green.err"
run "grep -cE '^[^#]*mktemp' close_r4.sh ; grep -cE '^[^#]*mktemp' close_r3.sh   # code lines only"
printf 'round4_mktemp_code_lines=%s\n' "$(grep -cE '^[^#]*mktemp' "$FIX/close_r4.sh")"
printf 'round3_mktemp_code_lines=%s\n' "$(grep -cE '^[^#]*mktemp' "$FIX/close_r3.sh")"

banner 'F2/T6 GREEN - clean run under the frozen launch domain and plan argv'
mk_tree "$FIX/clean"
EV="$FIX/clean/evidence/runkit/$RUNID"
WORK="$FIX/clean/work"
run "env -i ... /usr/bin/bash --noprofile --norc close_r4.sh $EV $RUNID $WORK"
launch4 "$FIX/close_r4.sh" "$EV" "$RUNID" "$WORK" > "$FIX/clean.out" 2> "$FIX/clean.err"
echo "RC=$?"
grep -E '^CLOSE_NOTE (launch_domain|work_root_ok|scratch|evidence_files|digest_set_stable)|^CLOSE_BINDING |^CLOSE_DIGEST |^CLOSE PASS ' "$FIX/clean.out"
echo '--- stderr:'; cat "$FIX/clean.err"
echo '--- the evidence tree after the run (no scratch residue, no new member):'
find "$EV" | sort
echo '--- the work root after the run (the run-owned work directory was removed):'
find "$WORK" | sort

banner 'F3 RED - round-3 bytes, mixed ENOENT+EACCES probe diagnostic'
echo '# A stat wrapper that answers the evidence-directory probe with a combined'
echo '# diagnostic. Round 3 substring-matches "No such file or directory" and'
echo '# reports a completed observation of MISSING EVIDENCE at rc 1.'
mk_tree "$FIX/f3"
EV="$FIX/f3/evidence/runkit/$RUNID"
cat > "$FIX/tools/stat_mixed" <<EOF
#!/usr/bin/bash
for a in "\$@"; do
    if [ "\$a" = "$EV" ]; then
        printf '%s: No such file or directory; Permission denied\n' "$EV" >&2
        exit 1
    fi
done
exec $FIX/tools/stat "\$@"
EOF
chown 0:0 "$FIX/tools/stat_mixed"; chmod 0755 "$FIX/tools/stat_mixed"
sed "s#^TOOL_STAT='$FIX/tools/stat'#TOOL_STAT='$FIX/tools/stat_mixed'#" "$FIX/close_r3.sh" > "$FIX/close_r3_mixed.sh"
sed "s#^TOOL_STAT='$FIX/tools/stat'#TOOL_STAT='$FIX/tools/stat_mixed'#" "$FIX/close_r4.sh" > "$FIX/close_r4_mixed.sh"
run "bash close_r3_mixed.sh \$EV $RUNID"
/usr/bin/bash "$FIX/close_r3_mixed.sh" "$EV" "$RUNID" > "$FIX/f3red.out" 2> "$FIX/f3red.err"
echo "RC=$?"
tail -2 "$FIX/f3red.err"

banner 'F3 GREEN - round-4 bytes, same mixed diagnostic'
echo '# The absence template is calibrated once from this run own pinned stat and'
echo '# compared as a whole string, corroborated by the kernel. A mixed diagnostic'
echo '# is an inability to evaluate: CLOSE_STOP at rc 3.'
run "env -i ... close_r4_mixed.sh \$EV $RUNID \$WORK"
launch4 "$FIX/close_r4_mixed.sh" "$EV" "$RUNID" "$FIX/f3/work" > "$FIX/f3green.out" 2> "$FIX/f3green.err"
echo "RC=$?"
tail -2 "$FIX/f3green.err"

banner 'F1 RED - a fake bash first on PATH under the round-3 launch (bare `bash -s --`)'
mkdir -p "$FIX/plant"
cat > "$FIX/plant/bash" <<EOF
#!/usr/bin/bash
cat > /dev/null
printf 'PLANT_RAN argv=%s\n' "\$*" >> $FIX/plant/hit
printf 'CLOSE PASS runid=%s dir=%s files=2 wrote_into_evidence_tree=0\n' "$RUNID" "/forged"
exit 0
EOF
chmod 0755 "$FIX/plant/bash"
rm -f "$FIX/plant/hit"
mk_tree "$FIX/f1"
EV="$FIX/f1/evidence/runkit/$RUNID"
run 'PATH=$FIX/plant:$PATH bash -s -- <EV_DIR> <RUNID>   # the round-3 plan argv'
PATH="$FIX/plant:$PATH" bash -s -- "$EV" "$RUNID" < "$FIX/close_r3.sh" > "$FIX/f1red.out" 2> "$FIX/f1red.err"
echo "PATH_RC=$?"
echo "PATH_HIT=$( [ -f "$FIX/plant/hit" ] && echo yes || echo no )"
cat "$FIX/f1red.out"

banner 'F1 RED - inherited BASH_ENV under an absolute interpreter, no env -i'
cat > "$FIX/plant/startup.sh" <<EOF
printf 'STARTUP_PLANT_RAN\n' >> $FIX/plant/hit2
printf 'CLOSE PASS runid=%s dir=%s files=2 wrote_into_evidence_tree=0\n' "$RUNID" "/forged"
exit 0
EOF
rm -f "$FIX/plant/hit2"
run 'BASH_ENV=$FIX/plant/startup.sh /usr/bin/bash -s -- <EV_DIR> <RUNID>'
BASH_ENV="$FIX/plant/startup.sh" /usr/bin/bash -s -- "$EV" "$RUNID" < "$FIX/close_r3.sh" > "$FIX/f1red2.out" 2> "$FIX/f1red2.err"
echo "BASH_ENV_RC=$?"
echo "BASH_ENV_HIT=$( [ -f "$FIX/plant/hit2" ] && echo yes || echo no )"
cat "$FIX/f1red2.out"

banner 'F1 GREEN - the frozen launch domain neutralises both plants'
rm -f "$FIX/plant/hit" "$FIX/plant/hit2"
run 'the frozen argv, with the plant still first on the OUTER PATH and BASH_ENV still set'
PATH="$FIX/plant:$PATH" BASH_ENV="$FIX/plant/startup.sh" \
    "$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
    /usr/bin/bash --noprofile --norc "$FIX/close_r4.sh" "$EV" "$RUNID" "$FIX/f1/work" \
    > "$FIX/f1green.out" 2> "$FIX/f1green.err"
echo "RC=$?"
echo "PATH_HIT=$( [ -f "$FIX/plant/hit" ] && echo yes || echo no ) STARTUP_HIT=$( [ -f "$FIX/plant/hit2" ] && echo yes || echo no )"
grep -E '^CLOSE_NOTE launch_domain |^CLOSE PASS ' "$FIX/f1green.out"

banner 'F1 RESIDUAL - a launch domain that CARRIES BASH_ENV, with an exiting plant'
echo '# MEASURED LIMIT, not a repair. bash reads $BASH_ENV before the first byte'
echo '# of the delivered script; --norc/--noprofile do not disable that channel.'
echo '# A startup plant that exits therefore forges the record before any'
echo '# in-script attestation can run. NOTHING inside a stdin-delivered script'
echo '# can close this - it is closed on the plan/runner side, by env -i with an'
echo '# explicit complete variable list that the runner enforces verbatim, so no'
echo '# plan row can introduce BASH_ENV at all. This case is unreachable from the'
echo '# frozen plan; it is recorded because the claim must be scoped honestly.'
run 'env -i PATH=... LC_ALL=C HOME=... BASH_ENV=<exiting plant> /usr/bin/bash --noprofile --norc close_r4.sh ...'
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" "BASH_ENV=$FIX/plant/startup.sh" \
    /usr/bin/bash --noprofile --norc "$FIX/close_r4.sh" "$EV" "$RUNID" "$FIX/f1/work" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"

banner 'F1 GREEN - a launch domain that carries BASH_ENV, with a NON-exiting plant'
echo '# The stealthier plant - one that mutates state and lets the delivered'
echo '# script run so the real record is produced - IS refused: BASH_ENV is still'
echo '# in the exec environment the kernel recorded, and the class 5 sweep names'
echo '# it. Only the plant that destroys the run outright escapes the sweep, and'
echo '# it destroys the very output it was trying to forge into.'
cat > "$FIX/plant/startup_quiet.sh" <<EOF
printf 'QUIET_STARTUP_PLANT_RAN\n' >> $FIX/plant/hit3
EOF
rm -f "$FIX/plant/hit3"
run 'env -i PATH=... LC_ALL=C HOME=... BASH_ENV=<non-exiting plant> ... close_r4.sh ...'
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" "BASH_ENV=$FIX/plant/startup_quiet.sh" \
    /usr/bin/bash --noprofile --norc "$FIX/close_r4.sh" "$EV" "$RUNID" "$FIX/f1/work" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"
echo "QUIET_PLANT_HIT=$( [ -f "$FIX/plant/hit3" ] && echo yes || echo no )"

banner 'F1 GREEN - the same script refuses an inherited exported shell function'
run 'env -i ... BASH_FUNC_a_plant%%=() { :; } /usr/bin/bash --noprofile --norc close_r4.sh ...'
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
    "BASH_FUNC_a_plant%%=() { :; }" \
    /usr/bin/bash --noprofile --norc "$FIX/close_r4.sh" "$EV" "$RUNID" "$FIX/f1/work" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"

banner 'T6 - the superseded cf049b6b close script under its own clean launch'
echo '# The addendum records this edit as SUPERSEDED. Driven exactly as its own'
echo '# header prescribes, it refuses its own clean execution.'
run 'env -i ... /usr/bin/bash --noprofile --norc close_super.sh <EV_DIR> <RUNID> <WORK_ROOT>'
launch4 "$FIX/close_super.sh" "$EV" "$RUNID" "$FIX/f1/work" 2>&1 | tail -2
echo "RC=${PIPESTATUS[0]}"

banner 'T6 - argv arity: two arguments against a three-argument contract'
echo '# The superseded edit called fail() for a wrong argument count, so an'
echo '# operator-side composition error arrived at the runner as a HOST deviation'
echo '# at rc 1. The round-4 bytes classify it as an inability to evaluate.'
run 'close_super.sh <EV_DIR> <RUNID>    (no work root)'
"$LAUNCH_ENV" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
    /usr/bin/bash --noprofile --norc "$FIX/close_super_nofunc.sh" "$EV" "$RUNID" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"
run 'close_r4.sh <EV_DIR> <RUNID>       (no work root)'
launch4 "$FIX/close_r4.sh" "$EV" "$RUNID" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"

banner 'F2/class 6 - a work root inside the evidence tree is refused before mkdir'
mk_tree "$FIX/overlap"
EV="$FIX/overlap/evidence/runkit/$RUNID"
mkdir -m 0700 "$EV/inner"
run 'close_r4.sh <EV_DIR> <RUNID> <EV_DIR>/inner'
launch4 "$FIX/close_r4.sh" "$EV" "$RUNID" "$EV/inner" 2>&1 | tail -1
echo "RC=${PIPESTATUS[0]}"
echo '--- the evidence tree is unchanged (no work directory was created in it):'
find "$EV" | sort

banner 'T6 - op 01 allocates the work root the plan passes to ops 07/08'
echo '# Two further FIXTURE-ONLY retargetings are declared here, because op 01 is'
echo '# path- and mount-bound to the real host: EXPECT_PREFIX/EXPECT_PARENT are'
echo '# moved under $FIX, and EXPECT_PARENT_MOUNT is filled from the projection'
echo '# this kernel reports. Filling that pin from an observation would be'
echo '# ILLEGITIMATE in production - the value is a deploy-channel attestation'
echo '# (owner grant #6) and must never be learned from the session under test -'
echo '# so this step proves the allocation shape ONLY, not the mount binding.'
rm -rf "$FIX/alloc"
mkdir -m 0700 "$FIX/alloc"
sed -e "s#^EXPECT_PREFIX='/home/gatea/wpi_staging_'#EXPECT_PREFIX='$FIX/alloc/wpi_staging_'#" \
    -e "s#^EXPECT_PARENT='/home/gatea'#EXPECT_PARENT='$FIX/alloc'#" \
    "$FIX/setup_r4.sh" > "$FIX/setup_fix.sh"
echo '# Pass 1 carries a grammar-valid DECOY projection, because the unfilled-pin'
echo '# gate runs before the projection is taken; the STOP then reports what this'
echo '# kernel actually projects.'
sed -i "s#^EXPECT_PARENT_MOUNT='<PIN-AT-FREEZE>'#EXPECT_PARENT_MOUNT='device=0:0 root=/decoy mount_point=/decoy fstype=decoy source=decoy shared_mount_point_records=1'#" "$FIX/setup_fix.sh"
run 'setup_fix.sh <BASE>   # first pass: decoy mount pin'
launch4 "$FIX/setup_fix.sh" "$FIX/alloc/wpi_staging_FIXTURE" > "$FIX/alloc1.out" 2> "$FIX/alloc1.err"
echo "RC=$?"
tail -1 "$FIX/alloc1.err"
OBSERVED="$(sed -n 's#.*observed=\[\(.*\)\] attested=.*#\1#p' "$FIX/alloc1.err" | tail -1)"
printf 'OBSERVED_PROJECTION=[%s]\n' "$OBSERVED"
echo '--- nothing was created by the refused pass (STOP precedes the first mkdir):'
ls -A "$FIX/alloc" | sed 's/^/  /'
sed "s#^EXPECT_PARENT_MOUNT='device=0:0 root=/decoy mount_point=/decoy fstype=decoy source=decoy shared_mount_point_records=1'#EXPECT_PARENT_MOUNT='$OBSERVED'#" \
    "$FIX/setup_fix.sh" > "$FIX/setup_fix2.sh"
run 'setup_fix2.sh <BASE>  # second pass: mount pin filled from the first pass'
launch4 "$FIX/setup_fix2.sh" "$FIX/alloc/wpi_staging_FIXTURE" > "$FIX/alloc2.out" 2> "$FIX/alloc2.err"
echo "RC=$?"
grep -E '^SETUP_NOTE (launch_domain|allocated|work_root_allocated) |^SETUP PASS ' "$FIX/alloc2.out"
tail -1 "$FIX/alloc2.err"
echo '--- what op 01 actually created:'
find "$FIX/alloc/wpi_staging_FIXTURE" | sort

banner 'T6 - the allocated work root is exactly what the plan passes to ops 07/08'
run 'close_r4.sh <BASE>/evidence/runkit/<RUNID> <RUNID> <BASE>/work'
BASE="$FIX/alloc/wpi_staging_FIXTURE"
mkdir -m 0700 "$BASE/evidence/runkit/$RUNID"
printf 'gamma\n' > "$BASE/evidence/runkit/$RUNID/c.txt"
launch4 "$FIX/close_r4.sh" "$BASE/evidence/runkit/$RUNID" "$RUNID" "$BASE/work" > "$FIX/compose.out" 2> "$FIX/compose.err"
echo "RC=$?"
grep -E '^CLOSE_NOTE work_root_ok |^CLOSE_NOTE scratch |^CLOSE PASS ' "$FIX/compose.out"
tail -1 "$FIX/compose.err"
echo '--- the plan row the runner will send (argv tail after the launch domain):'
awk -F'\t' '$1=="07"{n=split($8,a," "); printf "%s %s %s\n", a[n-2], a[n-1], a[n]}' "$SRC/TRANSPORT_PLAN.tsv"

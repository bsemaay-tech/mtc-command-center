#!/usr/bin/env bash
# Transport round-4 item T5: prove the run_p0.sh -> RP6-P0.sh composition.
#
# The claim under test is NOT "the five names appear in the wrapper". It is:
# the wrapper EXPORTS five P0_ATTESTED_* values into the scope the block is
# sourced into, in a grammar the block's own gate accepts, so the composition
# no longer STOPs before any host observation.
#
# It is proved in two executed halves, with the connection stubbed:
#   A. the REAL wrapper is launched under the frozen remote launch domain with
#      EXTRACT_DIR pointed at probe stubs, and the environment it hands to the
#      sourced block is captured from the block position itself;
#   B. the REAL RP6-P0.sh row-8 gate bytes are extracted verbatim and executed
#      against exactly that captured environment.
# RED uses the round-3 wrapper (commit 78173bfd); GREEN uses the round-4 bytes.
#
# No host is contacted and no network connection is made.
set -u

SRC="$1"     # WPI_BLOCKS_DRAFT (round-4 bytes + the real RP6-P0.sh)
R3="$2"      # round-3 bytes from commit 78173bfd
FIX=/root/wpi_r4_t5

banner() { printf '\n########## %s\n' "$*"; }
run()    { printf '$ %s\n' "$*"; }

rm -rf "$FIX"; mkdir -p "$FIX/tools" "$FIX/extract" "$FIX/out"
for t in stat sha256sum env; do
    cp -L "/usr/bin/$t" "$FIX/tools/$t"; chown 0:0 "$FIX/tools/$t"; chmod 0755 "$FIX/tools/$t"
done
MYHOME="$HOME"

banner 'A. probe stubs standing in for the three sourced artifacts'
# RP0-LIB and RP0-BOOTSTRAP are replaced by stubs because they open the evidence
# leaf and redirect stdout on a real host; the wrapper only needs EV_DIR/EV_LOG
# from them. RP6-P0 is replaced by an ENVIRONMENT PROBE that records exactly what
# the wrapper exported at the moment of sourcing. Nothing about the wrapper is
# changed.
cat > "$FIX/extract/RP0-LIB.sh" <<'EOF'
: "${RUNID:=unset}"
EOF
cat > "$FIX/extract/RP0-BOOTSTRAP.sh" <<EOF
EV_DIR="$FIX/out/evidence_\$RUNID"
EV_LOG="\$EV_DIR/stage.log"
EOF
cat > "$FIX/extract/RP6-P0.sh" <<EOF
# environment probe: record the P0_* environment this block was sourced into
env | grep '^P0_' | sort > "$FIX/out/p0_env.txt"
printf 'P0W_PROBE sourced_with_P0_names=%s\n' "\$(env | grep -c '^P0_')"
EOF
ls -l "$FIX/extract"

mkwrapper() {   # mkwrapper <in> <out>
    sed -e "s#^EXTRACT_DIR='.*'#EXTRACT_DIR='$FIX/extract'#" \
        -e "s#^BASE_RUN='<ALLOCATE-AT-DISPATCH>'#BASE_RUN='T5FIXTURE'#" \
        -e "s#^RUNID='<ALLOCATE-AT-DISPATCH>-P0'#RUNID='T5FIXTURE-P0'#" \
        -e "s#^EXPECT_LAUNCH_HOME='/home/gatea'#EXPECT_LAUNCH_HOME='$MYHOME'#" \
        -e "s#^\(TOOL_\(STAT\|SHA256SUM\|ENV\)=\)'/usr/bin/\(.*\)'#\1'$FIX/tools/\3'#" \
        -e "s#^P0_EXPECT_UID='<PIN-AT-FREEZE>'#P0_EXPECT_UID='1001'#" \
        -e "s#^P0_TOOL_PINS='<PIN-AT-FREEZE>'#P0_TOOL_PINS='placeholder'#" \
        -e "s#^RP0_LIB_SHA='.*'#RP0_LIB_SHA='$(sha256sum "$FIX/extract/RP0-LIB.sh" | cut -d' ' -f1)'#" \
        -e "s#^RP0_BOOTSTRAP_SHA='.*'#RP0_BOOTSTRAP_SHA='$(sha256sum "$FIX/extract/RP0-BOOTSTRAP.sh" | cut -d' ' -f1)'#" \
        -e "s#^RP6_P0_SHA='<PIN-AT-FREEZE>'#RP6_P0_SHA='$(sha256sum "$FIX/extract/RP6-P0.sh" | cut -d' ' -f1)'#" \
        "$1" > "$2"
}
mkwrapper "$R3/run_p0.sh"  "$FIX/run_p0_r3.sh"
mkwrapper "$SRC/run_p0.sh" "$FIX/run_p0_r4_unfilled.sh"
# GREEN also needs the five deploy-channel values PRESENT. They are placeholders
# with the block's own grammar, not real host values: the point is the wiring.
sed -e "s#^P0_ATTESTED_USER_NS='<PIN-AT-FREEZE>'#P0_ATTESTED_USER_NS='user:[4026531837]'#" \
    -e "s#^P0_ATTESTED_MNT_NS='<PIN-AT-FREEZE>'#P0_ATTESTED_MNT_NS='mnt:[4026531841]'#" \
    -e "s#^P0_ATTESTED_PID_NS='<PIN-AT-FREEZE>'#P0_ATTESTED_PID_NS='pid:[4026531836]'#" \
    -e "s#^P0_ATTESTED_NET_NS='<PIN-AT-FREEZE>'#P0_ATTESTED_NET_NS='net:[4026531840]'#" \
    -e "s#^P0_ATTESTED_ROOT_MOUNT_ID='<PIN-AT-FREEZE>'#P0_ATTESTED_ROOT_MOUNT_ID='2049:2'#" \
    "$FIX/run_p0_r4_unfilled.sh" > "$FIX/run_p0_r4.sh"

launch() { "$FIX/tools/env" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "HOME=$MYHOME" \
             /usr/bin/bash --noprofile --norc "$@"; }

banner 'A-RED. round-3 wrapper: which P0_* names reach the block?'
run 'env -i ... /usr/bin/bash --noprofile --norc run_p0_r3.sh'
rm -f "$FIX/out/p0_env.txt"
launch "$FIX/run_p0_r3.sh" > "$FIX/out/r3.out" 2> "$FIX/out/r3.err"
echo "RC=$?"
tail -2 "$FIX/out/r3.out"; cat "$FIX/out/r3.err"
cp "$FIX/out/p0_env.txt" "$FIX/out/p0_env_r3.txt" 2>/dev/null || : > "$FIX/out/p0_env_r3.txt"
echo '--- P0_* environment the round-3 wrapper handed to the block:'
sed 's/^/  /' "$FIX/out/p0_env_r3.txt"
printf 'P0_ATTESTED_names_exported=%s\n' "$(grep -c '^P0_ATTESTED_' "$FIX/out/p0_env_r3.txt")"

banner 'A-GREEN. round-4 wrapper, deploy-channel values present'
run 'env -i ... /usr/bin/bash --noprofile --norc run_p0_r4.sh'
rm -f "$FIX/out/p0_env.txt"
launch "$FIX/run_p0_r4.sh" > "$FIX/out/r4.out" 2> "$FIX/out/r4.err"
echo "RC=$?"
grep -E '^P0W_(launch_domain|attested_inputs|PROBE)|^P0W done' "$FIX/out/r4.out"
cat "$FIX/out/r4.err"
cp "$FIX/out/p0_env.txt" "$FIX/out/p0_env_r4.txt"
echo '--- P0_* environment the round-4 wrapper handed to the block:'
sed 's/^/  /' "$FIX/out/p0_env_r4.txt"
printf 'P0_ATTESTED_names_exported=%s\n' "$(grep -c '^P0_ATTESTED_' "$FIX/out/p0_env_r4.txt")"

banner 'B. the REAL RP6-P0.sh row-8 gate, extracted verbatim'
BLOCK="$SRC/RP6-P0.sh"
START="$(grep -n '^\[ -n "\${P0_ATTESTED_USER_NS:-}" \] \\$' "$BLOCK" | cut -d: -f1)"
END="$(grep -n 'detail=prelude_value_differs_from_frozen_pin"$' "$BLOCK" | tail -1 | cut -d: -f1)"
FIXEDLINES="$(grep -n '^P0_FIXED_ATTESTED_' "$BLOCK" | cut -d: -f1 | tr '\n' ',')"
printf 'BLOCK path=%s sha256=%s\n' "$BLOCK" "$(sha256sum "$BLOCK" | cut -d' ' -f1)"
printf 'GATE_REGION lines=%s-%s\n' "$START" "$END"
printf 'FIXED_LITERAL_LINES=%s\n' "$FIXEDLINES"
{
    printf 'p0_stop() { printf "P0_STOP reason=%%s\\n" "$*" >&2; exit 3; }\n'
    grep '^P0_FIXED_ATTESTED_' "$BLOCK"
    sed -n "${START},${END}p" "$BLOCK"
    printf 'printf "P0_GATE_PASSED all_five_attested_inputs_accepted\\n"\n'
} > "$FIX/gate.sh"
printf 'GATE_EXTRACT sha256=%s bytes=%s\n' "$(sha256sum "$FIX/gate.sh" | cut -d' ' -f1)" "$(wc -c < "$FIX/gate.sh")"

drive_gate() {   # drive_gate <env-file> <label>
    local envfile="$1" label="$2" args=()
    while IFS= read -r line; do args+=("$line"); done < "$envfile"
    printf '\n$ env -i %s bash gate.sh   # %s\n' "P0_ATTESTED_*=..." "$label"
    "$FIX/tools/env" -i "PATH=/usr/bin:/bin" "LC_ALL=C" "${args[@]}" \
        /usr/bin/bash --noprofile --norc "$FIX/gate.sh" 2>&1 | tail -1
    printf 'RC=%s\n' "${PIPESTATUS[0]}"
}

banner 'B-RED. the real gate, driven with the round-3 wrapper environment'
drive_gate "$FIX/out/p0_env_r3.txt" 'round-3: no P0_ATTESTED_* exported'

banner 'B-GREEN. the real gate, driven with the round-4 wrapper environment'
drive_gate "$FIX/out/p0_env_r4.txt" 'round-4: five values exported'
echo '# The frozen P0_FIXED_ATTESTED_* literals in the block are still'
echo '# <PIN-AT-FREEZE>, so the gate now reaches the freeze-pin arm instead of'
echo '# the missing-input arm. That is the correct draft-stage state: the block'
echo '# side is a Stage-1 fill, not a wrapper defect. The next case fills both.'

banner 'B-GREEN2. both sides filled - the gate passes end to end'
sed -e "s#^P0_FIXED_ATTESTED_USER_NS='<PIN-AT-FREEZE>'#P0_FIXED_ATTESTED_USER_NS='user:[4026531837]'#" \
    -e "s#^P0_FIXED_ATTESTED_MNT_NS='<PIN-AT-FREEZE>'#P0_FIXED_ATTESTED_MNT_NS='mnt:[4026531841]'#" \
    -e "s#^P0_FIXED_ATTESTED_PID_NS='<PIN-AT-FREEZE>'#P0_FIXED_ATTESTED_PID_NS='pid:[4026531836]'#" \
    -e "s#^P0_FIXED_ATTESTED_NET_NS='<PIN-AT-FREEZE>'#P0_FIXED_ATTESTED_NET_NS='net:[4026531840]'#" \
    -e "s#^P0_FIXED_ATTESTED_ROOT_MOUNT_ID='<PIN-AT-FREEZE>'#P0_FIXED_ATTESTED_ROOT_MOUNT_ID='2049:2'#" \
    "$FIX/gate.sh" > "$FIX/gate_filled.sh"
cp "$FIX/gate_filled.sh" "$FIX/gate.sh"
drive_gate "$FIX/out/p0_env_r4.txt" 'round-4 environment, block literals filled to match'
drive_gate "$FIX/out/p0_env_r3.txt" 'round-3 environment, block literals filled: still missing input'

banner 'B-GREEN3. a wrapper value that disagrees with the frozen literal'
sed 's#^P0_ATTESTED_PID_NS=.*#P0_ATTESTED_PID_NS=pid:[9999999999]#' \
    "$FIX/out/p0_env_r4.txt" > "$FIX/out/p0_env_r4_disagree.txt"
drive_gate "$FIX/out/p0_env_r4_disagree.txt" 'one value differs from the frozen pin'

# ===== BLOCK-ID: RP0-BOOTSTRAP ===== [EXECUTABLE PROPOSAL BLOCK]
# Runs after RP0-LIB is sourced. Preregistered inputs only; nothing is derived
# at run time, nothing is defaulted, nothing is created with `mkdir -p`.
set -Eeuo pipefail

: "${RUNID:?preregistered run identifier is required}"
: "${EV_PARENT:?preregistered evidence parent is required}"
: "${EV_PARENT_OWNER:?preregistered evidence parent owner:group is required}"
: "${EV_PARENT_MODE:?preregistered evidence parent octal mode is required}"
: "${EV_RUNKIT:?preregistered runkit directory is required}"
: "${EV_RUNKIT_OWNER:?preregistered runkit owner:group is required}"
: "${EV_RUNKIT_MODE:?preregistered runkit octal mode is required}"
: "${EV_STAGE_ID:?preregistered stage identifier is required}"

# Non-empty is NOT sufficient. Both identifiers name ONE component each; a
# separator or `..` would put the active evidence leaf outside the tree that
# §1.5 hashes, so the remote/local binding would attest to the wrong bytes.
rp0_require_safe_component RUNID       "$RUNID"       || exit $?
rp0_require_safe_component EV_STAGE_ID "$EV_STAGE_ID" || exit $?

# Parent chain first: canonical, non-link, preregistered owner and mode.
rp0_require_canonical_dir "$EV_PARENT" "$EV_PARENT_OWNER" "$EV_PARENT_MODE" || exit $?
rp0_require_canonical_dir "$EV_RUNKIT" "$EV_RUNKIT_OWNER" "$EV_RUNKIT_MODE" || exit $?

# One-shot create-once allocation; the run ID is burned on any failure.
EV_DIR="$EV_RUNKIT/$RUNID"
rp0_require_leaf_inside "$EV_RUNKIT" "$EV_DIR" || exit $?
rp0_allocate_evidence_dir "$EV_DIR" || exit $?

# Only now may output be redirected, and only into the directory just created,
# after the derived leaf is PROVEN to be a direct child of it.
EV_LOG="$EV_DIR/${EV_STAGE_ID}.log"
rp0_require_leaf_inside "$EV_DIR" "$EV_LOG" || exit $?
rp0_open_evidence_leaf "$EV_LOG" || exit $?

printf 'RP0_EVIDENCE run_id=%s dir=%s leaf=%s\n' "$RUNID" "$EV_DIR" "$EV_LOG"

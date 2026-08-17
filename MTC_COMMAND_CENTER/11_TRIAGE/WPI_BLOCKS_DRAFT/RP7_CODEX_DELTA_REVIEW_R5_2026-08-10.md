# RP7 round-5 Codex delta review — text-level only

Date: 2026-08-10

Subject: `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`

Scope: round-4 commit `d6a976aa` versus round-5 commit `1143a9ff`

## Result

The measured executable delta is exactly **`+93/-7`**. Every non-comment changed line is
accounted for by repairs 1, 2, 4, or 5. Repair 3 changes the published QA command in
`SELF_QA_RP7.md` and therefore has no hunk in this shell-file delta. There are **no
unexplained hunks**.

No changed hunk weakens a round-4 check. No condition was removed without replacement, no
comparison was loosened, no STOP became a warning, and no error path became non-fatal.

This run performed **no behavioural testing**. It did not run the block or any part of it,
construct fixtures, contact a host, or use the network. This is a text-level verification
only.

## Measured identities and diff statistics

The round-4 bytes were retrieved with `git cat-file blob` rather than checkout.

| Version | Commit | Bytes | Measured SHA-256 |
|---|---|---:|---|
| Round 4 | `d6a976aa` | 70,941 | `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad` |
| Round 5 | `1143a9ff` | 77,179 | `393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee` |

`git diff --no-index --numstat` measured:

```text
93	7	RP7-WPI-RO.sh
```

`git diff --no-index --shortstat` measured:

```text
1 file changed, 93 insertions(+), 7 deletions(-)
```

For classification, the diff was rendered with zero context. That produces 11 contiguous
change groups and prevents a pure comment change from being hidden in a larger contextual
hunk. With four context lines the same delta displays as nine hunks; the statistics are
identical.

## Per-hunk classification

| ID | Zero-context location, round 4 → round 5 | `+/-` | Bucket | Reason |
|---|---|---:|---|---|
| H1 | `10` → `10-14` | `+5/-1` | Comment-only | Documents repair 5's evidence-root claim; no executable line changes in this group. |
| H2 | after `53` → `58-66` | `+9/-0` | Repair 5 | Adds the frozen evidence-root constant and its freeze-order explanation. |
| H3 | `183` → `196-200` | `+5/-1` | Repair 4 | Replaces the `/dev/null` stderr open with fd 2 closure; the noclobber condition remains. |
| H4 | `624-625` → `641-647` | `+7/-2` | Repair 4 | Replaces PATH-satisfiable `command -v` probes and `/dev/null` opens with exact function-type checks. |
| H5 | after `630` → `653-663` | `+11/-0` | Repair 5 | Requires `EV_DIR` to be an absolute strict descendant of the frozen evidence root before leaf allocation. |
| H6 | `663` → `696` | `+1/-1` | Repair 5 | Adds the established root and binding mechanism to the evidence-bound result. |
| H7 | after `900` → `934-945` | `+12/-0` | Comment-only | Documents repair 2's admitted-member identity gap; no executable line changes in this group. |
| H8 | `908` → `953` | `+1/-1` | Repair 2 | Imports the parser and regex modules needed for package-identity adjudication. |
| H9 | after `933` → `979-999` | `+21/-0` | Repair 2 | Adjudicates exactly one valid Name and Version and rejects duplicate canonical identities before parity. |
| H10 | after `967` → `1034-1046` | `+13/-0` | Repair 2 | Maps the new driver rc 6 grammar to a reasoned metadata-identity STOP. |
| H11 | `1134` → `1213-1220` | `+8/-1` | Repair 1 | Adds `python3` to the production binding loop before either adjudicator can run. |
| **Total** |  | **`+93/-7`** |  |  |

Pure comment-only groups: **2**, totaling `+17/-1` (H1 and H7).

Whitespace-only groups: **0**.

Repair 3 shell-file groups: **0**; its published-command change is outside this subject.

### H1 — comment-only, repair 5 commentary

```diff
-# which RP0-BOOTSTRAP allocated before this block. No host object is changed.
+# which RP0-BOOTSTRAP allocated before this block. EV_DIR is itself proven, at
+# the first predicate and before any leaf is allocated, to be a strict
+# descendant of the frozen evidence root below <REMOTE_BASE>; every leaf is then
+# proven to be inside EV_DIR. No host object outside that tree is changed, and
+# no path outside it is opened for writing - including /dev/null.
```

This is comment-only and describes the narrower, root-bound mutation claim introduced by
repair 5.

### H2 — repair 5: frozen evidence root

```diff
+# The only tree this block may write into. RP0-BOOTSTRAP allocates EV_DIR as
+# <REMOTE_BASE>/evidence/runkit/<RUNID>, and the block proved EV_LOG below EV_DIR
+# and every capture leaf below EV_DIR - but nothing proved EV_DIR itself descends
+# from the run's own base, so the whole create-once chain hung from an unattested
+# root supplied by the same channel it was meant to bound. The frozen prefix below
+# closes that, and is a freeze-gate input exactly like the two pins above it:
+# <REMOTE_BASE> is allocated, so Stage 1 must allocate it BEFORE it freezes these
+# bytes. Until the pin is filled the block STOPs rather than claiming provenance.
+WPI_FIXED_EVIDENCE_ROOT='<PIN-AT-FREEZE>'
```

The only production addition is the constant required by repair 5; the remaining lines
explain its provenance and freeze ordering.

### H3 — repair 4: remove the noclobber `/dev/null` open

```diff
-    if ! ( set -o noclobber; : > "$leaf" ) 2>/dev/null; then
+    # stderr is CLOSED, not redirected to /dev/null: /dev/null is outside both the
+    # run evidence tree and the section-10.1 allowlist, so opening it for writing
+    # would be an unpreregistered write open. Closing fd 2 discards the noclobber
+    # diagnostic with no open at all and leaves the noclobber test itself intact.
+    if ! ( set -o noclobber; : > "$leaf" ) 2>&-; then
```

The write-open target is removed while the create-once noclobber predicate and its fatal
branch remain unchanged.

### H4 — repair 4: remove prerequisite `/dev/null` opens

```diff
-    command -v rp0_require_safe_component >/dev/null 2>&1 || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_require_safe_component"
-    command -v rp0_allocate_evidence_dir >/dev/null 2>&1 || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir"
+    # `builtin type -t` is the non-overridable form and needs no redirection: with
+    # -t an undefined name prints nothing on either stream and returns 1, so no
+    # /dev/null write open is required to silence it, and `builtin` bypasses any
+    # function named `type`. It is also strictly narrower than `command -v`, which
+    # would have been satisfied by an executable of the same name on PATH.
+    [ "$(builtin type -t rp0_require_safe_component)" = function ] || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_require_safe_component"
+    [ "$(builtin type -t rp0_allocate_evidence_dir)" = function ] || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir"
```

Both former write opens disappear, and the replacement requires the two names to resolve
specifically as shell functions rather than accepting an executable found on PATH.

### H5 — repair 5: bind `EV_DIR` before leaf allocation

```diff
+    # Evidence-root provenance, established BEFORE any leaf can be allocated. The
+    # two existing containments (EV_LOG below EV_DIR, every capture leaf below
+    # EV_DIR) are relative; this is the absolute one they hang from.
+    wpi_require_absolute EV_DIR "$EV_DIR"
+    [ "$WPI_FIXED_EVIDENCE_ROOT" != '<PIN-AT-FREEZE>' ] || \
+        wpi_stop RP7 "evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT"
+    wpi_require_absolute WPI_FIXED_EVIDENCE_ROOT "$WPI_FIXED_EVIDENCE_ROOT"
+    case "$EV_DIR" in
+        "$WPI_FIXED_EVIDENCE_ROOT"/*) : ;;
+        *) wpi_stop RP7 "evidence_root_unattested ev_dir=$EV_DIR expected_root=$WPI_FIXED_EVIDENCE_ROOT" ;;
+    esac
```

This is repair 5's fail-closed absolute/canonical prefix binding, placed in the first
prerequisite predicate before any evidence leaf can be allocated.

### H6 — repair 5: report the root binding

```diff
-    printf 'RP7_evidence_bound leaf=%s object_id=%s stdout_path=[%s] mechanism=dev_inode_identity\n' "$EV_LOG" "$logid" "$WPI_SAFE"
+    printf 'RP7_evidence_bound leaf=%s object_id=%s stdout_path=[%s] mechanism=dev_inode_identity evidence_root=%s root_binding=frozen_prefix_descent\n' "$EV_LOG" "$logid" "$WPI_SAFE" "$WPI_FIXED_EVIDENCE_ROOT"
```

The accepting evidence line now names the root proven by repair 5; its existing object-ID
comparison is not removed or loosened.

### H7 — comment-only, repair 2 commentary

```diff
+#
+# Admission is not adjudication (Codex round-4 finding 2). The row-19 preflight and
+# the driver's own scan prove object kind, ownership, byte readability and format -
+# none of which is the object's package IDENTITY. verify_lock.py:68-74 skips every
+# distribution whose METADATA carries no Name and overwrites duplicate canonical
+# names in a dict, so an admitted-but-malformed object silently leaves the universe
+# it was admitted into and parity can print the accepting line for a set it never
+# adjudicated. The driver therefore establishes exactly one grammar-valid Name and
+# Version per admitted object, and a unique canonical name across them, BEFORE any
+# distribution object is handed to the verifier. Absent, ambiguous, unparseable or
+# duplicate identity is an inability to evaluate: rc 6, STOP - never a silent
+# omission and never a named-mismatch FAIL.
```

This is comment-only and describes the repair-2 ordering and disposition contract.

### H8 — repair 2: identity-adjudication dependencies

```diff
-import hashlib,os,sys
+import email,hashlib,os,re,sys
```

The added modules are consumed only by repair 2's METADATA parsing and canonical-name
grammar below.

### H9 — repair 2: adjudicate every admitted package identity

```diff
+NAME_RE=re.compile("[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?")
+VER_RE=re.compile("[0-9][0-9A-Za-z.!+_-]*")
+canon={}
+for p in accepted:
+ h=hashlib.sha256(p.name.encode("utf-8","surrogateescape")).hexdigest()
+ t=" name_sha256="+h
+ try:
+  raw=(p/"METADATA").read_bytes()
+ except OSError:
+  die(6,"distribution_identity_unestablished"," detail=metadata_unreadable"+t)
+ msg=email.message_from_string(raw.decode("utf-8","surrogateescape"))
+ nm=msg.get_all("Name") or []
+ vs=msg.get_all("Version") or []
+ if len(nm)!=1: die(6,"distribution_identity_unestablished"," detail=name_"+("absent" if not nm else "ambiguous")+t)
+ if len(vs)!=1: die(6,"distribution_identity_unestablished"," detail=version_"+("absent" if not vs else "ambiguous")+t)
+ nv=str(nm[0]).strip(); vv=str(vs[0]).strip()
+ if not NAME_RE.fullmatch(nv): die(6,"distribution_identity_unestablished"," detail=name_grammar"+t)
+ if not VER_RE.fullmatch(vv): die(6,"distribution_identity_unestablished"," detail=version_grammar"+t)
+ c=re.sub("[-_.]+","-",nv).lower()
+ if c in canon: die(6,"distribution_identity_unestablished"," detail=canonical_name_duplicate"+t)
+ canon[c]=h
```

Every member of the already-admitted universe receives one identity disposition before
`PathDistribution` construction; missing, ambiguous, malformed, or duplicate identity
exits through the new rc 6 path.

### H10 — repair 2: adjudicate rc 6 as STOP

```diff
+    if [ "$WPI_CAP_RC" -eq 6 ]; then
+        case "$err" in
+            'verify_lock_driver: distribution_identity_unestablished detail='*' name_sha256='*)
+                fields="${err#verify_lock_driver: distribution_identity_unestablished }"
+                ufmt="${fields%% *}"; udigest="${fields#* }"
+                case "$ufmt" in detail=[a-z][a-z_0-9]*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
+                case "$udigest" in name_sha256=?*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
+                case "${udigest#name_sha256=}" in ''|*[!0-9a-f]*) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
+                [ "${#udigest}" -eq 76 ] || wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR"
+                wpi_stop B1 "metadata_identity_unestablished stage=verifier $ufmt $udigest" ;;
+            *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;;
+        esac
+    fi
```

The new driver result is validated field by field and terminates as a reasoned STOP; no
round-4 FAIL or accepting branch is weakened.

### H11 — repair 1: bind `python3` in the production loop

```diff
-    for wpi_tool in stat readlink env find sha256sum systemctl ss curl timeout; do
+    # ALL TEN pins are bound here, inside that window, and the tenth is the
+    # trusted adjudicating python3. Round 4 accepted the tenth pin, added it to
+    # projection v2 and defined its binding, but never passed it through this
+    # loop: the executable ran at both adjudicators while `-I -S`, the startup
+    # guards and every `pinned_system_interpreter` token rested on an object no
+    # production line had ever bound (Codex round-4 finding 1). Those flags are
+    # only meaningful once the program that interprets them is the bound one.
+    for wpi_tool in stat readlink env find sha256sum systemctl ss curl timeout python3; do
```

The production caller now submits the tenth accepted pin to the unchanged binding body,
inside the existing mount window and before either adjudicator.

## Unexplained list

**Empty.** All 11 zero-context change groups are classified above. The two pure
comment-only groups are explicitly counted rather than discarded, and there are no
whitespace-only changes.

## Weakening review

**Empty.** Review of every deleted line found no weakened round-4 check:

- H1 narrows and documents the mutation claim while repair 5 adds the missing root check.
- H3 preserves the noclobber/create-once condition and changes only the stderr sink from a
  `/dev/null` open to a closed descriptor.
- H4 replaces two broad `command -v` checks with stricter shell-function identity checks;
  both still STOP on failure.
- H6 preserves the existing evidence object-identity fields and adds root-binding fields.
- H8 only extends the import set.
- H11 preserves all nine prior binding-loop members and adds `python3` as the tenth.

There is no removed condition, loosened comparison, STOP-to-warning conversion, or newly
non-fatal error path in the delta.

## `/dev/null` grep result

All three round-4 write-open sites are gone. The round-5 file has **four textual
occurrences across three lines**, all in comments; line 196 contains the token twice.
There is no executable `/dev/null` redirection left.

```text
12-# descendant of the frozen evidence root below <REMOTE_BASE>; every leaf is then
13-# proven to be inside EV_DIR. No host object outside that tree is changed, and
14:# no path outside it is opened for writing - including /dev/null.
15-# File content is never printed: result lines contain paths, metadata, counts,
16-# classifications, and digests only.
--
194-    local leaf="$1"
195-    case "$leaf" in "$EV_DIR"/*) : ;; *) wpi_stop RP7 "capture_path_outside_evidence leaf=$leaf ev_dir=$EV_DIR" ;; esac
196:    # stderr is CLOSED, not redirected to /dev/null: /dev/null is outside both the
197-    # run evidence tree and the section-10.1 allowlist, so opening it for writing
198-    # would be an unpreregistered write open. Closing fd 2 discards the noclobber
--
641-    # `builtin type -t` is the non-overridable form and needs no redirection: with
642-    # -t an undefined name prints nothing on either stream and returns 1, so no
643:    # /dev/null write open is required to silence it, and `builtin` bypasses any
644-    # function named `type`. It is also strictly narrower than `command -v`, which
645-    # would have been satisfied by an executable of the same name on PATH.
```

The repair report's sentence saying there are “three remaining `/dev/null` strings” is
textually off by one: grep finds three matching lines but four string occurrences. Its
substantive write-open claim is correct because every survivor is a comment.

## `SELF_QA_RP7.md` absolute line-range grep result

No absolute numeric `sed -n '123,456p'`-style range survives. No numeric
`Select-Object -Skip <n> -First <n>` range survives. The only `sed -n` evidence commands
are content-anchored:

```text
37:sed -n '/^# RP7_QA_FENCE_BEGIN$/,/^# RP7_QA_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r5-fence-body.sh
38:sed -n '/^# RP7_R4_FENCE_BEGIN$/,/^# RP7_R4_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r4-fence-body.sh
50:sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Both targeted numeric-range grep commands returned no matches.

# DESIGN NOTES - B3-GAP-ENV Option 1 design repair, round 1

Implements the authorized Option 1 repair described in
`KICKOFF_B3_GAP_ENV_OPTION1.md`, against the gap adjudicated in
`03_TRANSPORT/B3_STOP_ADJUDICATION.md`. Round 1 deliverables:

| File | Role |
|---|---|
| `round1/RP1-B3.sh` | repaired unprivileged block, full file (226 lines) |
| `round1/RPD-VERIFY.sh` | NEW root-side deploy-time verify block, full file (169 lines) |
| `round1/DESIGN_NOTES.md` | this file |
| `round1/SELF_QA.md` | syntax evidence, arm walk, no-content audit |

sha256 as delivered (round 1):

```
03152789e7cc3deb5adff113f6a81bff3cdaf04ff4311730ab82d02d5d9622a7  RP1-B3.sh
610996deec81dc25ef7252b77a6a585779df16acb0ce9258a634e54bd08a98ba  RPD-VERIFY.sh
```

Nothing outside `round1/` was created, modified or deleted. No remote host was
contacted. `RP0-LIB.sh` is unmodified.

## 1. Where every check of the original block landed

Line numbers are the accepted block `01_RUNKIT/RP1-B3.sh` (117 lines).

| # | Original check (line) | Landed | One-sentence why |
|---|---|---|---|
| 1 | release tree `0555 root:root` (98) | unprivileged | `/opt` and `/opt/mtc-bridge/releases` are searchable by the route user, so mode and owner are fully evaluable without privilege. |
| 2 | release tree `/222` sweep (99) | unprivileged | The tree is `0555` and world-readable/searchable, so `find` walks it as the route user; the STOP that occurred was never in this section. |
| 3 | venv tree `0555 root:root` (102) | unprivileged | Same reachability as #1. |
| 4 | venv tree `/222` sweep (103) | unprivileged | Same reachability as #2. |
| 5 | `STATE_DIR` `0750 mtc-bridge:mtc-bridge` (106) | unprivileged | `stat` on the directory itself needs only search on `/var/lib`, which the route user has; the block never enters it. |
| 6 | `LOG_DIR` `0750 mtc-bridge:mtc-bridge` (107) | unprivileged | Same as #5, via `/var/log`. |
| 7 | `CONF_DIR` `0750 root:root` (108) | unprivileged | `stat /etc/mtc-bridge` needs only search on `/etc`; that is exactly the asymmetry the accepted block failed to distinguish from entering the directory. |
| 8 | `ENV_FILE` `0600 root:root` (109) | root-side (`RPD-VERIFY`) | Reading the metadata of any name under `/etc/mtc-bridge` requires search on that `0750 root:root` directory, which the unprivileged route user structurally cannot have. |
| 9 | `INSTALL_MANIFEST` `0640 root:root` (110) | root-side (`RPD-VERIFY`) | Same denial as #8; the name cannot even be resolved unprivileged. |
| 10 | `UNIT_FILE` `0644 root:root` (111) | unprivileged | `/usr/local/lib/systemd/system` is world-searchable and the unit fragment is `0644`, so mode and owner are evaluable unprivileged. |
| 11 | manifest binds `release_sha` + `release_manifest_sha256` (113-114) | root-side (`RPD-VERIFY`) | The predicate must READ a `0640 root:root` file inside the opaque directory; no unprivileged formulation of it exists on this host. |
| 12 | (new) `CONF_DIR` opaque to the caller | unprivileged only | A demonstrated denial is the strongest honest statement an unprivileged operator can make about that directory, and the claim is meaningless when made as root. |

Checks #1-#7 and #10 keep the accepted predicate strength verbatim. Checks #8, #9
and #11 keep their predicate strength too - they are relocated, not relaxed: the
same exact-mode/exact-owner comparison and the same silent three-outcome
`grep -qsF` binding test now run as root in `RPD-VERIFY.sh`.

## 2. Exact-diff summary, `RP1-B3.sh` old vs new

Mechanical diff: 30 old lines replaced by 139 new lines (`diff` old-side 30,
new-side 139; comments dominate the growth).

### 2.1 Removed - code

Verbatim old-side code lines that no longer exist anywhere in the new block:

```
INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"
: "${B3_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required}"
b3_assert_manifest_binding() { ... }            # whole function, old 75-93
b3_assert_mode_owner "$ENV_FILE"         0600 root:root      # old 109
b3_assert_mode_owner "$INSTALL_MANIFEST" 0640 root:root      # old 110
printf 'B3_SECTION manifest_binding\n'                       # old 113
b3_assert_manifest_binding "$INSTALL_MANIFEST" "$CAND" "$B3_RELEASE_MANIFEST_SHA256"   # old 114
```

That is the complete removal set: two `stat` admissions, the manifest-binding
function and its invocation, its section header, the manifest path variable, and
the `B3_RELEASE_MANIFEST_SHA256` input guard. Every one of them reappears in
`RPD-VERIFY.sh` (the input as `RPD_RELEASE_MANIFEST_SHA256`).

### 2.2 Removed - comments

The old function-header comment block for `b3_assert_manifest_binding`
(old 70-74, the `verify.sh:129-135` provenance) is removed from this block and
carried, unchanged in substance, into `RPD-VERIFY.sh:120-127`.

### 2.3 Added - functions

| New function (new line) | Purpose |
|---|---|
| `b3_assert_unprivileged` (120) | uid 0 is STOP; discloses `uid` and the numeric supplementary gid list as `B3_identity`. |
| `b3_assert_not_in_dir_group` (135) | Takes `CONF_DIR`'s own numeric gid via `stat -c '%g'` and STOPs if the caller is a member; no group name and no gid literal is assumed. |
| `b3_assert_conf_dir_opaque` (171) | The boundary probe: EACCES is the pass arm (`B3_conf_dir_opaque_to_operator`), a successful `stat` is FAIL, every other error class is STOP. |

### 2.4 Added - non-function lines

- `CONF_ABSENT_PROBE` (34): second probe name, so the denial is shown to be
  name-independent rather than a statement about one file.
- `DEFERRED_INSTALL_MANIFEST` (36): used only by the deferral log lines.
- Two `command -v rp0_probe_path` / `rp0_monotonic_ms` guards (54-55).
- Section `conf_dir_boundary` (211-214): group exclusion plus two probes.
- Section `deferred` (219-222): three `B3_deferred` evidence lines.
- `B3_claim` line (225), immediately before the unchanged terminal `B3 PASS`.

### 2.5 Changed - comments only

Header lines 2 and 5 of the accepted block: `stat`/`find`/silent `grep` becomes
`stat`/`find` (no `grep` remains in the unprivileged block - verified, zero
occurrences of the string), and the scope-reduction paragraph is added. Two
accepted comment lines that contained a U+2014 em dash were rewritten with an
ASCII hyphen to satisfy the ASCII-only constraint; both are comments, and no
code line changed as a result.

### 2.6 Preserved byte-identical

- `b3_assert_mode_owner` (15 lines) - byte-identical to the accepted block,
  verified by extraction and `diff`.
- `b3_assert_no_writable_paths` (17 lines) - byte-identical, verified the same
  way. Its `find ... ! -type l -perm /222 -print -quit` predicate, the F2
  rationale and the budget STOP are untouched.
- `set -Eeuo pipefail`, `b3_stop`/`b3_fail`, the `B3_`/`RP0_` prefixes, the
  0/1/3 rc contract, the `B3_SWEEP_BUDGET_S` guard in its accepted `:?` form,
  the `common.sh:80-93` / `common.sh:95-105` provenance comments, the
  `B3_SECTION` cadence and the terminal `B3 PASS` line.

Rationale for byte-identity rather than refactoring: the two surviving
predicates already carry exercised falsifications, and this repo's convention
(RP0-LIB `rp0_cgroup_survivors` vs `rp0_cgroup_inventory`) is to leave an
accepted predicate untouched rather than share code with a new one.

## 3. Additions beyond the kickoff's explicit list

Each is a strengthening, each is reversible, and each is called out so an
auditor does not have to discover it.

1. **`command -v` RP0-LIB guards** (both blocks). Without RP0-LIB sourced the
   first predicate call aborts under `set -e` with rc 127 and no reason string,
   which is neither FAIL nor STOP. The kickoff requires the 0/1/3 rc contract;
   these two lines are what make it true. Reversible: delete the lines and the
   blocks behave exactly as the accepted block did.
2. **`b3_assert_unprivileged` / `b3_assert_not_in_dir_group`**. Without them the
   boundary probe's FAIL arm is unsound: run as root, or as a member of
   `CONF_DIR`'s group, the probe would succeed and the block would report "the
   directory is more open than the accepted host state" when the true cause is a
   wrong caller. Both misattributions are now STOP before the probe runs.
3. **Second probe name** (`CONF_ABSENT_PROBE`). Makes the pass arm a
   falsification: EACCES is name-independent, so if entry were in fact permitted
   the two names would diverge (success vs ENOENT) and both non-pass arms catch
   it.
4. **`B3_deferred` and `B3_claim` evidence lines**. A scope reduction that is
   silent in the evidence is a coverage loss waiting to be misread; the log now
   states which three checks moved and where. The terminal `B3 PASS` string is
   deliberately unchanged so nothing that greps for it breaks.
5. **Numeric identity only** (`id -u`, `id -G`; no `id -un`, no `id -nG`, in
   either block). `id -nG` exits 1 with `cannot find name for group ID <n>`
   whenever a supplementary gid has no name-service entry - a healthy-host
   condition on directory-backed hosts - which would have introduced a brand-new
   STOP arm on a path the accepted block completed. It was observed for real
   during self-QA. Numeric ids need no name service, and they also keep
   non-ASCII account names out of an evidence log that must stay ASCII.
6. **`rpd_require_hex` format guard** (RPD-VERIFY). Load-bearing, not cosmetic:
   `grep -F` treats a multi-line pattern as a SET of alternatives, so a value
   carrying a newline can make the binding test match an unrelated manifest line.
   Reproduced during self-QA against a manifest-shaped fixture (SELF_QA.md
   section 6); the guard rejects it before either `grep` runs.
7. **rc-3 pre-check on the two RPD inputs**, in front of the retained `:?`
   guards. A bare `: "${VAR:?msg}"` aborts a non-interactive shell with rc 1 -
   the code this contract reserves for "host state is deviant" - for what is
   really an operator plumbing error. The pre-check classifies it as STOP and
   puts a reason string on stdout. `RP1-B3.sh` deliberately keeps the accepted
   `:?`-only form for `B3_SWEEP_BUDGET_S`, because the kickoff requires that
   guard block preserved; see open item O2.
8. **`dir` is not an accepted kind in `rpd_assert_regular_mode_owner`.** Both
   root-side paths are files, so accepting `regular|dir` (as the shared
   RP1-B3 helper must, since it also guards trees) would be looser than needed.

## 4. Admission claims after the repair

**`RP1-B3.sh` claims, and claims only:**

> As the unprivileged route identity `uid=<n>` with numeric groups `<list>`, and
> for candidate `2ce41e34...321b`: the release tree and the venv tree are
> `0555 root:root` with no write bit anywhere in either tree, both sweeps inside
> the preregistered budget; `/var/lib/mtc-bridge` and `/var/log/mtc-bridge` are
> `0750 mtc-bridge:mtc-bridge`; `/etc/mtc-bridge` is `0750 root:root`; the unit
> fragment is `0644 root:root`; this caller is not in `/etc/mtc-bridge`'s group
> and `/etc/mtc-bridge` denied it entry for two distinct names.

It explicitly does NOT claim: that `/etc/mtc-bridge/mtc-bridge.env` exists, that
it is spelled that way, that its mode is `0600`, that the install manifest
exists, or that any binding holds. Those three are named in the evidence as
`B3_deferred ... to=RPD-VERIFY`.

**`RPD-VERIFY.sh` claims, and claims only:**

> As `uid=0` at deploy time, with the candidate SHA and the accepted
> `RELEASE_SHA256SUMS` sha256 supplied from preregistration and never derived on
> the host: `/etc/mtc-bridge/mtc-bridge.env` is a regular file, `0600 root:root`;
> `/etc/mtc-bridge/install_manifest.json` is a regular file, `0640 root:root`;
> and that manifest binds BOTH `"release_sha": "<candidate>"` and
> `"release_manifest_sha256": "<preregistered>"`.

It explicitly does NOT claim anything about the trees, the sweeps, the ancillary
directories, the unit fragment, service state, or the env file's CONTENT - the
env file is never opened.

Together the two blocks reconstitute the accepted block's full admission set.
Neither alone does, and neither pretends to.

## 5. RPD-VERIFY is design-only in this unit

`RPD-VERIFY.sh` is **not executed tonight and has no execution path in this
unit.** There is no runner, no argv entry, no preregistration row and no
evidence leaf for it. It enters the runkit as a frozen, non-executed block
exactly like RP3/RP5: hashed and preregistered as an artifact, never invoked.
Its `[EXECUTABLE PROPOSAL BLOCK]` tag marks the block class, not an authorization
to run. Executing it requires root at install/deploy time through the deploy
channel, which is a separate authority from tonight's staging run. Its header
states this in the file itself so the file cannot be separated from the caveat.

Consequence for the current unit: the B3 admission set stays incomplete until a
deploy-time run happens. That is the honest cost of Option 1 and it is not
hidden by anything in these deliverables.

## 6. Preregistration impact (for the re-freeze cycle)

Not applied here - `02_PREREG/PREREGISTRATION.md` is immutable and outside
`round1/`. Recorded so the next preregistration can carry it:

- Section 2: `B3_RELEASE_MANIFEST_SHA256` is no longer consumed by `RP1-B3`. The
  same value (`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`)
  becomes `RPD_RELEASE_MANIFEST_SHA256`, consumed by `RPD-VERIFY` at deploy time.
  `RPD_CANDIDATE_SHA` (`2ce41e34bceb599d80af24c5c33d835820ec321b`) is a new named
  input of the same kind. `B3_SWEEP_BUDGET_S` = 120 is unchanged.
- Section 8: rows #4 and #5 move from B3's expectation table to RPD-VERIFY's.
  B3 gains one row: "`/etc/mtc-bridge` denies entry to the route user", first
  divergence `B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[...] expected=EACCES`.
- Section 8 #4's **named risk is not resolved by this repair.** The `bridge.env`
  vs `mtc-bridge.env` naming question is invisible to an EACCES denial, by
  construction. It is answerable only by the root-side block. Any reading of a
  future `B3 PASS` as settling that name is wrong.
- Section 3: both blocks are new artifacts needing new expected hashes; the
  accepted `RP1-B3` hash `f40411b0...` is superseded by
  `03152789e7cc3deb5adff113f6a81bff3cdaf04ff4311730ab82d02d5d9622a7` if this
  round is accepted. Repairing a frozen adversarially-accepted block requires a
  new re-audit and re-freeze, as the adjudication states.

## 7. Residuals and open items for the Lead

- **O1. ENOENT is routed to STOP, not FAIL.** An ENOENT from the boundary probe
  proves the directory search SUCCEEDED, which contradicts the accepted state
  just as a successful `stat` does, so FAIL is arguably the truer
  classification. The kickoff's instruction is "any other error class is STOP",
  so ENOENT gets a STOP with its own reason string
  (`conf_dir_search_permitted_name_absent`) rather than being folded into the
  unclassified arm. The choice is escalation-neutral - section 8 makes any B3
  FAIL a STOP requiring Lead adjudication either way - and it never yields a
  PASS. Reversal is a one-line change if the Lead prefers FAIL.
- **O2. Asymmetric missing-input rc.** `RP1-B3` exits 1 on a missing
  `B3_SWEEP_BUDGET_S` (accepted `:?` behaviour, preserved as instructed);
  `RPD-VERIFY` exits 3. If the Lead wants symmetry, the rc-3 pre-check pattern
  from `RPD-VERIFY:48-51` should be added to `RP1-B3:44`.
- **O3. `mktemp` is the one filesystem write in either block.** Both the
  accepted sweep and the new boundary probe allocate a temp file under `TMPDIR`
  to capture stderr, and remove it. `rp0_probe_path` does the same. No verified
  path is written, no host configuration is touched; this is disclosed rather
  than described as "no writes at all". `RPD-VERIFY` writes nothing itself and
  only inherits this through `rp0_probe_path`.
- **O4. Exotic entry grants are not distinguished.** A POSIX ACL entry, a MAC
  policy, or a file capability on the operator's shell could grant search on
  `CONF_DIR` without appearing in `id -u`/`id -G`. The probe reports the
  observation (entry was permitted) and names the accepted state it contradicts;
  it does not assert a cause.
- **O5. `tr` failure inside a reason string.** `detail="$(tr -d '\r\n' <"$errf")"`
  can, under `set -e`, exit with `tr`'s rc instead of 1 or 3. This is the
  accepted pattern from `RP0-LIB:49` and `RP1-B3:59` (old numbering), inherited
  deliberately rather than diverging mid-repair. Flagged, not fixed.
- **O6. PID/ownership-free claim.** Neither block says anything about processes,
  service state or listeners; the B3 subcheck never did. Unchanged.
- **O7. `RPD-VERIFY` has never been executed as root anywhere.** Its non-root
  STOP arm was exercised for real during self-QA; its PASS path has only been
  exercised through stubbed predicates. First real run must be treated as a
  first run, not as a re-run of a proven block.

# WP-L Phase 2 Stage 2 — candidate payload-manifest derivation record

Result: **DERIVED and CROSS-CHECKED**

This record explains how `CANDIDATE_RELEASE_SHA256SUMS` in this directory was
produced, why it is byte-identical to the payload manifest the candidate's own
`package.sh` emits, and why its `sha256` is the correct preregistered value for
`B3_RELEASE_MANIFEST_SHA256`.

## 1. What was derived

| Item | Value |
|---|---|
| Frozen candidate | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Candidate subject | `fix(deploy): reject start-mode env override`, 2026-08-08 |
| Artifact | `CANDIDATE_RELEASE_SHA256SUMS`, 1181804 bytes |
| **`sha256` (the preregistered `B3_RELEASE_MANIFEST_SHA256`)** | **`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`** |
| Manifest entries | 7059 (7058 tree blobs + `./RELEASE_SHA`) |
| Payload bytes hashed | 1032180677 (1032180636 tree + 41 for `RELEASE_SHA`) |
| Derivation tool | `derive_candidate_release_manifest.py` (this directory) |

`install.sh` records this exact value as `release_manifest_sha256` in
`/etc/mtc-bridge/install_manifest.json` (`install.sh:112-114` computes it from
the payload's `RELEASE_SHA256SUMS`; `:410` writes it). `RP1-B3` then requires it
as a preregistered input and checks the binding with a silent `grep -qsF`
(`RP1-B3.sh`, proposals §2.2).

## 2. Why `package.sh` was not run

`package.sh` refuses to run unless the repository **HEAD is the release sha** and
the worktree is clean, then exports that commit with `git archive` into a
directory outside the worktree. Satisfying it would mean moving `HEAD` off the
working branch — outside this unit's authority and outside its constraints.

The derivation therefore reads the frozen commit's **objects** directly with
`git show <sha>:<path> --`. It never resolves, reads or moves `HEAD`, never
touches a ref, the index, or any working-tree file, and never writes to git.
That is **strictly stronger** than package.sh's own precondition: a dirty or
unrelated worktree cannot influence the result, because the worktree is never
consulted.

The trailing `--` is load-bearing on Windows. Without it git treats the argument
as a possible working-tree filename and `stat`s it, which fails with
`ENAMETOOLONG` on this repository's deepest paths. With it, the argument is
unambiguously a revision.

## 3. What package.sh does, and how each step was reproduced

| package.sh step | Reproduction here |
|---|---|
| `git -c core.autocrlf=false -c core.eol=lf -c tar.umask=0022 archive <sha>` piped into `tar -x` | `git show <sha>:<path> --` per file. Both yield the blob bytes as stored in git. |
| inventory + size cross-check against `git ls-tree -rz --long` | every file's byte length is compared to the length `git ls-tree --long` records |
| `assert_regular_directory_tree` (no symlink/device/socket/FIFO) | every tree entry is asserted to be a regular-file blob; all 7058 are mode `100644` |
| `printf '%s\n' "$RELEASE_SHA" > "$OUT/RELEASE_SHA"` **before** the manifest | `./RELEASE_SHA` is a manifest member with content `<sha>` + `LF` (41 bytes) |
| CR-byte refusal for LF-required files | 12 files under `IBKR_PAPER_BRIDGE/deploy/linux/` and 14 other `*.sh` inspected; **0 CR bytes**; both inventories non-empty, as package.sh requires |
| `find . -type f '!' -name RELEASE_SHA256SUMS -print0 \| sort -z \| xargs -0 sha256sum` under `LC_ALL=C` | member names spelled `./<path>`, ordered by C-locale byte comparison, one `sha256sum` line each |

`git archive` reproduces the commit tree exactly here: the candidate's
`.gitattributes` carries only `* text=auto` plus one `eol=lf` pin — **no
`export-ignore`, no `export-subst`** — and package.sh independently re-asserts
that the exported inventory and sizes equal the commit tree.

## 4. Byte-fidelity proof (per file, not per sample)

For every one of the 7058 blobs the derivation recomputes **git's own object
id** over the bytes it received — `sha1("blob <len>\0" + bytes)` — and requires
it to equal the object id `git ls-tree` recorded for that path. A single
altered, added, dropped or line-ending-converted byte changes that id.

```
DERIVE_object_id_proof blobs_verified=7058 method=sha1(blob_len_nul_bytes)
```

The repository's object format was checked to be `sha1` before relying on this.

## 5. The separator rendering, and why `binary` is the preregistered one

GNU `sha256sum` writes `<64 hex><space><space><name>` in **text** mode (its
default on Linux) and `<64 hex><space>*<name>` in **binary** mode (its default
where text and binary differ, i.e. Windows/git-bash). The candidate's own
parsers strip either — `sed -E 's/^[0-9a-f]{64} [ *]//'` at `install.sh:116` and
`common.sh:135` — so the candidate itself anticipates both forms.

Both renderings of the identical content were computed:

| Rendering | Bytes | sha256 |
|---|---:|---|
| text (`  `) | 1181804 | `e74aae91482d49cbb5d7c4d665d749743f04164c89d4095f78da726065b1e4de` |
| **binary (` *`)** | 1181804 | **`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`** |

**The binary rendering is the one the real payload carries.** This is not a
preference; it is an independent match:

- `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md` records an offline A-0
  identity check run **against the real frozen payload tar** for this candidate
  (`RELEASE_SHA` exactly `2ce41e34…321b`). It recorded manifest SHA
  `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` over
  **7059 manifest entries**, 7060 regular files and 1033362481 total payload
  bytes.
- This derivation reproduces that digest and that entry count **from git objects
  only, without ever reading the tar**, and the byte totals reconcile exactly:
  1032180677 hashed members + 1181804 manifest file = **1033362481**, and 7059
  members + the manifest file itself = **7060 regular files**.

Four independent quantities agree. The pinned value is therefore a *derived*
value that also *matches recorded reality*, not a quoted one.

## 6. Fail-closed predicates

The derivation refuses rather than emits if any of these hold: the pinned sha
does not resolve to a commit object or resolves to a different id; the object
format is not `sha1`; any tree entry is not a regular-file blob; any path
contains a newline or backslash (GNU `sha256sum` escapes such names and prefixes
the line with a backslash, so the naive line form would not be byte-exact); any
basename is `RELEASE_SHA256SUMS`, or the tree already carries `RELEASE_SHA`; a
byte count or recomputed object id disagrees with `git ls-tree`; a CR byte
appears in an LF-required file; or either LF-required inventory is empty. A
non-zero rc never leaves a partial manifest at `--out`, and an existing output
path is refused rather than clobbered.

Checked and clean: 0 paths with a newline or backslash; 71 paths are non-ASCII
UTF-8 and 147 contain spaces, neither of which `sha256sum` escapes; no tree
entry named `RELEASE_SHA` or `RELEASE_SHA256SUMS`.

## 7. Determinism and format assertions (real output)

Four full derivations were run. The two under the final tool are byte-identical:

```
cmp <02_PREREG>/CANDIDATE_RELEASE_SHA256SUMS <scratch>/CANDIDATE_RELEASE_SHA256SUMS.finalpass2
  -> final pass1 == pass2 byte-identical
```

Format assertions over the emitted manifest:

```
bytes                                        = 1181804
cr bytes                                     = 0
ends with exactly one final LF               = True
line count                                   = 7059
lines not matching '^<64hex> [ *]./'         = 0
lines the candidate's own sed would not strip= 0
unique member names                          = 7059 of 7059
LC_ALL=C byte order                          = True
contains ./RELEASE_SHA                       = True
contains ./IBKR_PAPER_BRIDGE/deploy/linux/package.sh = True
```

## 8. Residual risk, stated plainly

This derivation attests to what `package.sh` **would** emit for this commit, and
it agrees with the manifest digest recorded for the real payload tar. It does
**not** read `/etc/mtc-bridge/install_manifest.json`, and it must not: a manifest
cannot attest to its own acceptance. If B3 reports
`install manifest does not bind release_manifest_sha256`, that is a genuine
divergence between the host and the frozen candidate and is a **STOP requiring
Lead adjudication** (proposals §2.2 FAIL disposition) — not a reason to retry
with a different rendering, and not a documentation outcome.

## 9. Provenance correction

The partial `run_b3.sh` preserved from the timed-out first attempt pinned this
same value but described its provenance as "derived LOCALLY in Stage 2 by
running the candidate's own `package.sh` in a clean detached clone". No such
derivation record existed, and that method is not available under this unit's
constraints. The value is correct; the provenance claim was not evidenced. The
comment now states the actual method, and this record supplies the evidence.

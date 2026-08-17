# WP-L Phase 2 — Stage 2 preregistration self-QA record

Result: **COMPLETE — every check executed, real output recorded, zero host contact**

Scope of this record: every self-QA command run while producing the Stage 2
preregistration, with its real result. Nothing below reached a network, a host,
a service, a credential, or any repository path outside `02_PREREG/`.

`PREREG_SHA256SUMS.txt` (the immutable checksum set covering the other 13 files
in this directory) hashes to
`a48730e1c83326f7b8edf53f8166a2e24f79f748b4ab3eaab2be760e8904e187`. This record
is deliberately outside that set: it is evidence *about* the preregistration.

---

## Q1 — `bash -n` on every delivered shell script (final bytes)

```
bash -n remote_setup.sh            rc=0 output=[]
bash -n remote_extract_verify.sh   rc=0 output=[]
bash -n run_b3.sh                  rc=0 output=[]
bash -n run_r45.sh                 rc=0 output=[]
bash -n remote_close_tree.sh       rc=0 output=[]
```

## Q2 — `py_compile` with an explicit cfile in OS temp (no repo `__pycache__`)

```
py_compile R4_5_runner.py                        rc=0  cfile=<ostemp>/R4_5_runner.pyc
py_compile derive_candidate_release_manifest.py  rc=0  cfile=<ostemp>/derive_candidate_release_manifest.pyc
ls -a 02_PREREG | grep -i pycache  ->  no __pycache__ in 02_PREREG
```

One earlier `python -m py_compile` did create a `__pycache__/` in this directory;
it was removed immediately and the check above confirms the directory is clean.

## Q3 — PowerShell parse + byte audit

```
[System.Management.Automation.Language.Parser]::ParseFile(transport_runner.ps1)
  parse_errors=0
transport_runner.ps1: bytes=18095 non_ascii=0 cr=0    <- ASCII-only as required
```

Byte audit of every file in this directory (final bytes):

| File | Bytes | CR | BOM | non-ASCII | final LF |
|---|---:|---:|---|---:|---|
| `CANDIDATE_RELEASE_DERIVATION.md` | 8970 | 0 | no | 34 | yes |
| `CANDIDATE_RELEASE_SHA256SUMS` | 1181804 | 0 | no | 150 | yes |
| `PREREGISTRATION.md` | 19430 | 0 | no | 162 | yes |
| `PREREG_SHA256SUMS.txt` | 1145 | 0 | no | **0** | yes |
| `R4_5_runner.py` | 16170 | 0 | no | 6 | yes |
| `STAGE2_PREREG_FAILURE_RECORD.md` | 2622 | 0 | no | 11 | yes |
| `TRANSPORT_PLAN.tsv` | 5817 | 0 | no | **0** | yes |
| `derive_candidate_release_manifest.py` | 16353 | 0 | no | 3 | yes |
| `remote_close_tree.sh` | 7470 | 0 | no | 5 | yes |
| `remote_extract_verify.sh` | 8270 | 0 | no | 9 | yes |
| `remote_setup.sh` | 4976 | 0 | no | 6 | yes |
| `run_b3.sh` | 5194 | 0 | no | 6 | yes |
| `run_r45.sh` | 4219 | 0 | no | 3 | yes |
| `transport_runner.ps1` | 18095 | 0 | no | **0** | yes |

**Zero CR bytes and zero BOMs anywhere** — a CRLF in a script delivered to `bash`
on ssh stdin would break its very first `set -Eeuo pipefail` line. Non-ASCII
codepoint inventory across the directory:

```
U+0131 'ı' x63   U+2014 '—' x57   U+00A7 '§' x18   U+2026 '…' x13
U+00F6 'ö' x7    U+00FC 'ü' x2    U+00B7 '·' x1    U+2192 '→' x1
```

All are inside comments, prose, or — for `ı/ö/ü` — inside real repository
pathnames that `CANDIDATE_RELEASE_SHA256SUMS` must reproduce byte-exactly. The
three files where ASCII-only matters (`transport_runner.ps1`,
`TRANSPORT_PLAN.tsv`, `PREREG_SHA256SUMS.txt`) contain none.

## Q4 — candidate payload-manifest derivation

Full record in `CANDIDATE_RELEASE_DERIVATION.md`. Key executed results:

```
DERIVE_candidate sha=2ce41e34…321b object=commit resolved=self object_format=sha1
DERIVE_inventory blobs=7058 modes=['100644', '100755']
DERIVE_lf_required deploy=12 other_sh=14 cr_bytes=0
DERIVE_rendering text   bytes=1181804 sha256=e74aae91482d49cbb5d7c4d665d749743f04164c89d4095f78da726065b1e4de
DERIVE_rendering binary bytes=1181804 sha256=edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26
DERIVE_corroboration a0_recorded_sha256=edb0fd34… a0_entries=7059 binary_matches=True entries_match=True
DERIVE_object_id_proof blobs_verified=7058 method=sha1(blob_len_nul_bytes)
DERIVE_members total=7059 payload_bytes_hashed=1032180677
DERIVE PASS candidate=2ce41e34…321b rendering=binary release_manifest_sha256=edb0fd34…
```

Determinism — four full derivations were run (two under an earlier text-mode
default, two under the final tool):

```
cmp <02_PREREG>/CANDIDATE_RELEASE_SHA256SUMS <scratch>/CANDIDATE_RELEASE_SHA256SUMS.finalpass2
  -> final pass1 == pass2 byte-identical
```

Format assertions over the emitted manifest:

```
bytes=1181804  cr bytes=0  ends with exactly one final LF=True  line count=7059
lines not matching '^<64hex> [ *]./'                  = 0
lines the candidate's own sed would not strip          = 0
unique names=7059 of 7059     LC_ALL=C byte order=True
contains ./RELEASE_SHA=True   contains ./IBKR_PAPER_BRIDGE/deploy/linux/package.sh=True
```

Independent corroboration (four quantities, all agreeing) against the offline
A-0 identity check recorded in `GATE_A_LOCAL_RUN_KIT_2026-08-08B.md` for the
**real frozen payload tar**: manifest sha `edb0fd34…`; 7059 manifest entries;
1032180677 + 1181804 = **1033362481** total payload bytes; 7059 members + the
manifest file = **7060** regular files.

## Q5 — transport runner dry run (final bytes)

```
TR_PLAN  sha256=0850f24fb2da47ea406ec328706a4ed2dc6d171af2032ac7cc32f032705a5239
TR_PLAN_ROWS count=12
TR_STDIN op=01 remote_setup.sh          faee3725…   (matches plan)
TR_STDIN op=04 remote_extract_verify.sh ba0bef0e…   (matches plan)
TR_STDIN op=05 run_b3.sh                0e54b0bf…   (matches plan)
TR_STDIN op=06 remote_close_tree.sh     87157f0e…   (matches plan)
TR_STDIN op=07 run_r45.sh               4b9e5e68…   (matches plan)
TR_STDIN op=08 remote_close_tree.sh     87157f0e…   (matches plan)
TR_PINNED runkit.tar     618f7640…      (matches pin)
TR_PINNED R4_5_runner.py 8519e2bf…      (matches pin)
TR_PROGRAM ssh resolved=C:\Windows\System32\OpenSSH\ssh.exe
TR_PROGRAM scp resolved=C:\Windows\System32\OpenSSH\scp.exe
TR_DRY_RUN no_process_was_started no_connection_was_opened
EXITCODE=0        record_root_exists=False
```

All twelve ops printed their full argv. No process was started.

## Q6-Q9 — falsifications (a guard is not evidence until it has been shown to fire)

### Q6 · transport runner preregistration guards

Each mutation was byte-restored and the restoration re-verified by sha256 in a
`finally` block.

| Case | What was broken | Observed | rc |
|---|---|---|---|
| F6 | runner executed from a copy outside `02_PREREG` | `TR_STOP reason=runner_not_in_preregistered_directory here=… expected=…` | 3 |
| F7 | one byte changed in `TRANSPORT_PLAN.tsv` | `TR_STOP reason=plan_sha256_mismatch actual=e18fec76… expected=0850f24f…` | 3 |
| F8 | one LF appended to `run_b3.sh` | `TR_STOP reason=stdin_sha256_mismatch op=05 actual=8f595a37… expected=0e54b0bf…` | 3 |
| F9 | `-Execute` with a wrong confirmation token | dry run only; `record_root_created=False` | 0 |

```
RESTORED plan sha256=0850f24fb2da47ea406ec328706a4ed2dc6d171af2032ac7cc32f032705a5239 matches_original=True
RESTORED run_b3.sh sha256=0e54b0bf08d620035c98986a8fc4872dc7cc59d31788d608028b0c91751aa782 matches_original=True
```

### Q7 · `remote_close_tree.sh` rehearsed against a synthetic closed tree

Run locally against a three-file synthetic evidence tree. The sandbox variant
differs from the preregistered script by **exactly two constants** — the two
host-identity values that cannot hold on a Windows workstation — and the diff was
printed:

```
31,32c31,32
< EXPECT_OWNER='gatea:gatea'          > EXPECT_OWNER='AzureAD+BarışSemaay:UNKNOWN'
< EXPECT_MODE='700'                   > EXPECT_MODE='755'
```

Every other predicate ran unmodified.

| Case | Expectation | Observed | rc |
|---|---|---|---|
| 1 | normal closed tree | `CLOSE_NOTE digest_set_stable passes=2`, 3 `CLOSE_DIGEST` + 3 `CLOSE_SIZE` lines, `CLOSE_DIGEST_SET_SHA256 … 05eae48b…`, `CLOSE PASS … wrote_into_evidence_tree=0` | 0 |
| 2 | absent evidence dir | `CLOSE_FAIL reason=evidence_dir_absent path=…` | 1 |
| 3 | basename ≠ RUNID | `CLOSE_FAIL reason=evdir_basename=…-SBX runid=…-OTHER` | 1 |
| 4 | RUNID escapes its component | `CLOSE_FAIL reason=runid_charset value=[../escaped]` | 1 |
| 5 | tree with no regular file | `CLOSE_FAIL reason=evidence_tree_has_no_regular_file path=…` | 1 |
| 6 | wrong argc | `CLOSE_FAIL reason=usage remote_close_tree.sh <EV_DIR> <RUNID> argc=1` | 1 |

### Q8 · end-to-end runner rehearsal, honest vs tampered

Two sandbox runners, differing from the preregistered runner **only in
constants** (directories, plan hash, pinned-file list, allowed program — diff
printed in the log), driven against local `bash` ops instead of ssh/scp. This
exercised the real code paths: plan parse, stdin hashing, `Start-Process`
stdin/stdout/stderr redirection, rc capture, `local_bind`, digest-set
reconstruction, and the record set.

Run A — honest fetch:

```
TR_OP_END id=01 rc=0 expect_rc=0 stdout_sha256=5cc5c6fd… stderr_sha256=e3b0c442…
TR_OP_END id=02 rc=0 expect_rc=0
TR_BIND_COUNTS op=03 remote=3 local=3
TR_BIND_SET op=03 remote_set_sha256=05eae48b… reconstructed=05eae48b…
TR_BIND_PASS op=03 files=3
TR_RUN PASS   EXITCODE=0
```

Run B — one byte appended to one fetched evidence file:

```
TR_BIND_DIFF op=03 digest_differs=notes.txt remote=1b398e8f… local=b5714d68…
TR_OP_END id=03 rc=1 expect_rc=0
TR_OP_MISMATCH id=03 rc=1 expected=0 first_fail_stopping=engaged
TR_RUN FAIL   EXITCODE=1
```

**Defect found and fixed by this rehearsal.** The runner originally trimmed the
final newline when reconstructing the remote digest file, so `TR_BIND_SET` would
have disagreed on *every* honest run and trained the reader to ignore it. The
remote file ends with LF after its last line; the reconstruction now reproduces
that exactly, and a mismatch is now a hard `TR_BIND_STOP` (rc 3) rather than a
note. Run A above is the post-fix result: the two values are equal.

### Q9 · first-FAIL stopping and create-once record root

Sandbox case C — op 01 (`sequence_ok`) made to fail, op 02 (`sequence_ok`), op 03
(`always`):

```
TR_OP_END id=01 rc=1 expect_rc=0
TR_OP_MISMATCH id=01 rc=1 expected=0 first_fail_stopping=engaged
TR_OP_SKIPPED id=02 reason=prior_op_did_not_produce_its_preregistered_rc
TR_OP_END id=03 rc=0 expect_rc=0
TR_RESULT id=01 rc=1 / id=02 rc=skipped / id=03 rc=0
TR_RUN FAIL   EXITCODE=1
```

The failing stage stopped the sequence while the evidence-preservation op still
ran, which is the whole point of the `always` class.

Create-once record root — the sandbox PASS case re-run a second time:

```
TR_STOP reason=record_root_already_exists path=… (the record root is create-once; a rerun needs a new preregistration)
EXITCODE=3        ops executed on the rerun: 0
```

**Not falsified live against the real plan, deliberately.** Proving that guard
with the real plan would require passing `-Execute` with the correct token; if
the guard were defective, op 01 would contact the staging host. The constraint is
zero host contact, so the guard was proven in the sandbox, where argv[0] is
`bash` and reaching a host is impossible.

## Q10 — R4-5 mutant derivation, exercised locally against the frozen block

`R4_5_runner.derive_mutant` was run against the frozen `RP4-C3.py` on this
workstation (no symlinks, no `/tmp`, no host):

```
rp4 sha256   = 0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5  (== expected)
rp4 lines    = 295 (== expected)
guard 0-based index = 123  (1-based lines 124-125)
removed[0] = '    if dst_path.is_symlink():'
removed[1] = '        raise Fail(f"restore destination is a symlink: {dst_path}")'
accepted bytes = 12770   mutant bytes = 12672   delta = 98
mutant sha256  = ca98be3563a58edd540cbd7203255429ff9697ff13395e578a2f8a486d50c408
only-those-two-lines-differ = True
mutant py_compile = OK       accepted py_compile = OK
QA_DERIVE_MUTANT PASS
```

The guard text is unique file-wide (`RP4-C3.py:124`; the other two
`is_symlink()` occurrences at `:205` and `:214` have different text), so the
mutation cannot land anywhere else. The RED mutant is valid Python, so the RED
arm cannot fail as an import error dressed up as a result. `RP4-C3.py` was also
confirmed to have no module-level side effects: import-time code is imports,
constants, class and function definitions, and an `if __name__` guard only.

## Q11 — every embedded block hash equals the frozen identity table

All 16 block-hash constants embedded across the support scripts were matched
against `01_RUNKIT/BLOCK_IDENTITIES.tsv`:

```
remote_extract_verify.sh embeds all nine identities            OK
run_b3.sh                embeds RP0-LIB, RP0-BOOTSTRAP, RP1-B3 OK
run_r45.sh               embeds RP0-LIB, RP0-BOOTSTRAP, RP4-C3 OK
R4_5_runner.py           embeds RP4-C3                         OK
matched block-identity embeddings: 16
```

The only other 64-hex constants in the scripts are
`edb0fd34…` (the derived manifest hash, in `run_b3.sh`) and `8519e2bf…` (the
R4-5 runner hash, in `run_r45.sh`) — both accounted for above.

## Q12 — preregistered identifiers tested against the ACCEPTED predicate

`RP0-LIB.sh` was sourced and its own `rp0_require_safe_component` called:

```
value=WPLP2-20260809T125940Z-8dc78f08-B3   rc=0
value=WPLP2-20260809T125940Z-8dc78f08-R45  rc=0
value=b3                                   rc=0
value=r45                                  rc=0
```

RP0 §1.6 falsification (7), evidence-tree escape — all refused:

```
[../escaped] rc=1   [a/b] rc=1   [.] rc=1   [..] rc=1
[-lead] rc=1        []    rc=1   [bad name] rc=1
```

Leaf-containment spelling (the string half of `rp0_require_leaf_inside`, which is
all that can be checked without the remote filesystem):

```
EV_DIR is spelled as a direct child of EV_RUNKIT: yes
EV_LOG is spelled as a direct child of EV_DIR:    yes
```

## Q13 — checksum set self-verification

```
sha256sum -c --strict PREREG_SHA256SUMS.txt
  CANDIDATE_RELEASE_DERIVATION.md: OK      CANDIDATE_RELEASE_SHA256SUMS: OK
  PREREGISTRATION.md: OK                   R4_5_runner.py: OK
  STAGE2_PREREG_FAILURE_RECORD.md: OK      TRANSPORT_PLAN.tsv: OK
  derive_candidate_release_manifest.py: OK remote_close_tree.sh: OK
  remote_extract_verify.sh: OK             remote_setup.sh: OK
  run_b3.sh: OK                            run_r45.sh: OK
  transport_runner.ps1: OK
check rc=0   (13 files)
```

## Q14 — scope and cleanliness

```
01_RUNKIT/runkit.tar           618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53  (unchanged)
01_RUNKIT/BLOCK_IDENTITIES.tsv 68e833aa4a6b8eb02c17237b1f36914e81827c88c253cba82021403c0bac45c5  (unchanged)

git status --porcelain
 M …/02_PREREG/run_b3.sh
 M …/02_PREREG/run_r45.sh
?? …/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md
?? …/02_PREREG/CANDIDATE_RELEASE_SHA256SUMS
?? …/02_PREREG/PREREGISTRATION.md
?? …/02_PREREG/PREREG_SHA256SUMS.txt
?? …/02_PREREG/TRANSPORT_PLAN.tsv
?? …/02_PREREG/derive_candidate_release_manifest.py
?? …/02_PREREG/remote_close_tree.sh
?? …/02_PREREG/transport_runner.ps1
?? tmprepo_map_inventory.md
```

Every modification and addition is inside `02_PREREG/`. `tmprepo_map_inventory.md`
was already untracked before this unit began and was not touched.
`STAGE2_PREREG_FAILURE_RECORD.md` is unmodified — it does not appear as ` M`.

A git-ignored `.impeccable/hook.cache.json` (27 bytes, editor-harness cache,
covered by `.gitignore:171`) appeared in this directory during editing and was
removed; it is not part of the preregistration.

No `git add`, `git commit`, `git push`, checkout, branch, worktree or any other
Git write was performed. Git sequencing belongs to the Lead.

## Q15 — safety state

- SSH/SCP/remote invocation count: **0**. No socket was opened toward the staging
  host and no `ssh`/`scp` process was ever spawned; the only `TR_PROGRAM` lines
  are path resolutions of the executables.
- Every proposal block: **not executed, not sourced, not `bash -n`-ed** in this
  unit. `bash -n` here covered only the operator's own support scripts;
  `RP0-LIB.sh` was sourced **locally, read-only, for its pure string predicate**
  in Q12 — it defines functions and performs no filesystem, service, network,
  credential or economic action on sourcing.
- Service stop/start/enable/mask, reboot, rollback rehearsal, unit write: **none**.
- Credential read, ARM, order, broker/exchange, TESTNET/mainnet, master merge,
  KVM2/WP-V, payload-archive deletion, host reprovisioning: **none**.
- The transport record root
  `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` does **not**
  exist, which is itself evidence that no transport ran.

## Q16 — known limitations of this self-QA, stated plainly

1. **Nothing here proves the host's state.** Q4 attests to what `package.sh`
   would emit for the frozen candidate and to its agreement with a recorded
   identity check on the real payload tar. It does not read the host, and the
   preregistration deliberately forbids reading `install_manifest.json` to
   decide what to assert.
2. **The sandbox rehearsals used constant-substituted copies.** The diffs are
   printed in the logs and are limited to constants; no predicate, control-flow
   or ordering change was made. The preregistered scripts themselves were run
   unmodified only where the workstation permits (`bash -n`, `py_compile`,
   parse, dry run) — and were byte-verified after every temporary mutation.
3. **The remote-side behaviour of `remote_setup.sh`, `remote_extract_verify.sh`,
   `run_b3.sh` and `run_r45.sh` is unexercised.** Windows offers no `gatea:gatea`
   ownership, no `0700` semantics, no real symlinks without privilege, and no
   `/proc/uptime`, so their host predicates cannot be honestly rehearsed here.
   They are syntax-clean, hash-pinned and reviewed; that is the claim, and it is
   not a claim that they have run.
4. **The evidence-tree quiescence check is a two-pass stability test, not a proof
   of exit.** The proof that the stage process has exited is structural: the
   close-tree op is a separate ssh invocation issued after the stage connection
   returned.

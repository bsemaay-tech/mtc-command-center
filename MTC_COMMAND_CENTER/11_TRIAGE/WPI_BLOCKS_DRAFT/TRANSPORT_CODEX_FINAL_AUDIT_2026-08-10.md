# REQUEST_CHANGES — 4 required findings

The round-3 transport bytes at commit `78173bfd` are **not acceptable for freeze**. The specifically reported round-3 repairs reproduce under their standard fixtures, except that the broader V1 cleanup-failure claim is still false. Independent whole-set falsification found four required defects: an unpinned remote interpreter/provenance boundary, evidence-tree writes through inherited `TMPDIR`, an ambiguous close-tree probe incorrectly reported as `FAIL`, and an over-broad `always` dependency rule that hides a genuine independent cleanup deviation.

## Audit identity and scope

- Audit tier: **T0**, Codex flagship slot, `gpt-5.6-sol`, xhigh, fresh independent audit.
- Scope: the nine transport targets and the cited contracts at commit `78173bfd`.
- The current worktree's tracked target bytes were compared with `78173bfd`; there was no target drift. Tests used byte-exact blobs read from that commit. I rejected an initial `git archive` extraction after detecting line-ending conversion and repeated the work from raw `git cat-file` blobs.
- No staging/production host was contacted. No network connection was made. The only real OpenSSH executions were local configuration/argv evaluation and local-to-local `scp`, as explicitly allowed by the kickoff.
- I did not rely on the other flagship's verdict and did not delegate any part of this audit.

## V1–V9 verdicts

| ID | Result | Independent evidence |
|---|---|---|
| **V1** | **NOT CLOSED** | The round-3 runner correctly turns an early unmarked failure, `ssh` rc 255, an rc outside `{0,1,3}`, `ssh` rc 0 without a remote marker, and failed `scp` rc 1 into `TR_RUN STOP` / rc 3. A genuine marked remote rc 1 remains `TR_RUN FAIL` / rc 1. However, the derived close script still converts an ambiguous native path-probe failure into `CLOSE_FAIL` / rc 1; see F3. The claimed “every native transport/cleanup failure” closure is therefore false. |
| **V2** | **PASS for the reported configuration repair** | Real pinned `ssh.exe` evaluation reproduced the one-variable failure: no constructed `PROGRAMDATA` returned 255, while adding the constructed value returned 0. A hostile ambient system config activated `ProxyCommand SYSTEM_CONFIG_HIJACK`; the exact round-3 `-F none` option block suppressed it. A hostile explicit per-user config was honored in the red control and suppressed in the round-3 command. The evaluated round-3 configuration retained the pinned identity/known-hosts paths and restrictive options. Real pinned local-to-local `scp` through the runner passed and copied byte-identical content. |
| **V3** | **PASS for the reported internal-tool PATH repair** | The accepted original close script was byte-identical to SHA-256 `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e`. With hostile PATH-first `sha256sum`, the original executed the plant five times, mutated evidence, and printed `CLOSE PASS`. The derived script consulted no PATH plant: as shipped it stopped on the WSL symlink attestation, and with only the declared tool pins retargeted to attested regular copies it produced the correct digest without mutation. This narrow result does not cure the separate remote `bash` launch defect in F1. |
| **V4** | **PASS** | A bind-mounted decoy at the allocation parent, matched for canonical spelling, owner, and mode, caused the round-2 setup to create four directories in the decoy. The round-3 setup returned rc 3 with `parent_mount_differs` and created zero directories. The no-mount control returned rc 0 and created the expected four directories. Unfilled pins, empty/short/malformed mountinfo, and no covering mount all stopped before `mkdir`; a complete final mountinfo record without a trailing LF was consumed successfully. |
| **V5** | **PASS** | The revised census is correct: the seven executable/plan targets contain 36 `<ALLOCATE-AT-DISPATCH>` and 33 `<PIN-AT-FREEZE>` occurrences. Per-file counts and identities are reproduced below. |
| **V6** | **PASS for bounded derivation; contract needs expansion** | I diffed all five delivered derived shell outputs against their four accepted bases. Numstats were setup `+278/-51`, extractor `+246/-69`, close `+115/-30`, P0 wrapper `+86/-62`, and RO wrapper `+100/-64`. The actual changes are confined to WP-I constants/program identity, pinned tools/PATH removal, setup mount attestation, status-before-stdout handling, and wrapper role/stdin safety. I found no unrelated trading/runtime drift. The new defects arise because the four-class contract omits the interpreter environment, inherited `TMPDIR`, and exact ambiguous-probe semantics—not because of an unrelated diff. |
| **V7** | **FAIL** | The 12-operation preregistration order matches the plan; all operations, including skipped ones, get `.argv`, `.stdout`, `.stderr`, `.rc`, and `.elapsed_ms` records; first mismatch and later `always` execution are retained; the row-24 TCP refusal control classified as the expected rc 0 without payload; and the reviewed byte readers cover final unterminated records. V7 nevertheless fails: F1 defeats program provenance, F2 violates read-only scope, F3 violates STOP truth, and F4 masks an independent cleanup failure. |
| **V8** | **PASS with required freeze procedure** | Blind global replacement of literal `<PIN-AT-FREEZE>` would also rewrite `transport_runner.ps1`'s `$UNFILLED_MARKERS` member at line 174, making real filled values appear unfilled and safely stopping the run. The disclosure plus an explicit **per-constant/per-field fill** procedure is sufficient for this draft because different pins cannot safely be globally substituted anyway. The delivered unfilled runner was independently observed to stop with `reason=unfilled_marker field=BASE_RUN`, rc 3. Composing the marker string rather than storing the literal would be optional hardening, not a freeze blocker. |
| **V9** | **PASS** | Required placeholders remain literal, no concrete WP-I RUNID was minted on executable/plan surfaces, all target hashes/byte counts matched, all five delivered shell files passed `bash -n`, Windows PowerShell 5.1.26100.8875 parsed the runner with zero errors, and every target had zero CR bytes. |

## Required findings

### F1 — CRITICAL: the remote interpreter is selected outside the pinned program domain, and the runner accepts an unrelated marker family

**Affected surfaces:** `TRANSPORT_PLAN.tsv:2`, `:4-6`, `:8-9`; `transport_runner.ps1:165-172`, `:873-888`, `:894-927`; preregistration `§5` at lines 479 and 483-490.

The six stdin-script operations invoke bare `bash -s --`. The plan pins the local `ssh.exe` and its client configuration, but it neither pins nor externally attests the remote interpreter and its startup environment. The runner then treats any line-start prefix in one global marker set as program provenance, rather than binding the allowed terminal grammar to the operation and stdin artifact.

I executed two no-network falsifications with the exact delivered setup bytes on stdin:

1. With a fake `bash` first on PATH, `bash -s -- ...` returned 0, recorded that the plant ran, ignored the delivered script, and printed a forged `SETUP PASS ...`. Result: `PATH_RC=0`, `PATH_HIT=yes`, zero stderr.
2. Replacing the command with absolute `/usr/bin/bash -s --` was still insufficient under inherited `BASH_ENV`: the startup plant ran first, returned 0, ignored the delivered script, and printed the same forged marker. Result: `BASH_ENV_RC=0`, plant hit, zero stderr.

The clean absolute-interpreter control actually parsed the exact setup script and returned rc 3 at its WSL tool-attestation gate, proving that the forged rc 0 did not come from the delivered program. Separately, the exact runner fixture accepted `SETUP PASS` from the generic marked stub for close operations 07/08 as `class=match`; this demonstrates that the global prefix test does not establish which planned script ran.

This defeats the core evidence claim: a launch-domain plant can mutate gatea-writable state and forge the rc/marker pair that the operator accepts. Pinning only the local SSH client does not make the remote program identity closed.

**Required repair:** expand the freeze contract to cover the remote command interpreter and launch environment. Invoke an absolute, attested interpreter through a clean, explicitly constructed environment that excludes `BASH_ENV`, exported functions, and similar startup influences, while accounting for the outer SSH login-shell/startup boundary. Bind each operation to its own expected marker family and terminal grammar; for example, close operations must not accept `SETUP PASS`. Add and record D026 RED/GREEN falsifications for both the PATH fake interpreter and `BASH_ENV`, plus a wrong-marker-family case. The RED cases above are verified; no GREEN exists, so this finding remains open.

### F2 — HIGH: inherited `TMPDIR` makes the close script write inside evidence and falsely report read-only behavior

**Affected surface:** `remote_close_tree_wpi.sh:41-42`, `:72`, `:143`, `:188`, `:250-252`.

The close script explicitly inherits `TMPDIR`, then uses `/usr/bin/mktemp` for probe files and its work directory. With `TMPDIR` set to the evidence directory, the program creates its own temporary state inside the tree it is measuring.

I ran the exact derived logic with only the required local owner/tool-pin retargeting and `TMPDIR=$EV_DIR`. It returned rc 0 and printed, in part:

```text
CLOSE_BINDING files=2
CLOSE_DIGEST ... a.txt
CLOSE_DIGEST ... tmp.YIAAbpvchp/raw.0
CLOSE PASS ... wrote_into_evidence_tree=0
```

Before and after normal completion, the visible evidence tree contained only `a.txt`, because cleanup removed the temporary directory. During measurement, however, the script had written and hashed its own files inside evidence while claiming `wrote_into_evidence_tree=0`. Interruption can leave residue, and normal completion manufactures a later operator-side binding mismatch because the temporary digest describes a file that is no longer fetched.

**Required repair:** ignore/unset inherited `TMPDIR` or bind a trusted scratch root outside all evidence paths before the first `mktemp`; prove canonical non-overlap before mutation and install cleanup handling. Expand §4 to authorize and specify this semantic repair. Add a D026 RED/GREEN fixture with `TMPDIR=$EV_DIR`. The RED case is verified; no GREEN exists.

### F3 — HIGH: a mixed close-tree probe error is classified as evidence absence and therefore `FAIL`, not `STOP`

**Affected surface:** `remote_close_tree_wpi.sh:141-164`.

`probe_path` concatenates stat diagnostics and classifies any text containing `No such file or directory` as `absent`, regardless of additional diagnostics. The caller maps `absent` for the evidence directory to `CLOSE_FAIL` / rc 1. This reintroduces the exact STOP-truth class that round 3 was meant to close.

I retargeted only the declared `stat` tool pin to an owner-attested wrapper. It delegated normally except for the evidence-directory probe, where it returned rc 1 and the combined diagnostic `No such file or directory; Permission denied`. The derived close script returned rc 1 and emitted:

```text
CLOSE_FAIL reason=evidence_dir_absent ...
```

The control with the same fixture and ordinary stat behavior returned rc 0 and `CLOSE PASS`. A diagnostic/permission/tool ambiguity is not evidence that the preregistered tree is absent; the runner will accept the `CLOSE_` provenance and count this as a scientific deviation (`FAIL`).

**Required repair:** calibrate and match the exact expected absence diagnostic with independent corroboration, as the setup/extractor repairs do, or classify every ambiguous/mixed diagnostic as `CLOSE_STOP` / rc 3. Add the executed mixed-diagnostic case as D026 RED/GREEN evidence. RED is verified; no GREEN exists.

### F4 — HIGH: the broad `always` rule suppresses a genuine independent RO cleanup deviation

**Affected surface:** `transport_runner.ps1:939-941`, `:968-979`; preregistered broad cleanup rule in §5/§7.

The runner snapshots one global `$sequenceOk` value as `$prerequisiteEstablished` for every operation. Once any prior operation is non-match, every subsequent `always` rc 1 can be demoted to `not_evaluable` as “cleanup after unestablished prerequisite,” even if that later cleanup's own evidence branch was established successfully.

I extended the independent standard runner harness without changing the classifier:

- operations 01-06 all matched, so both P0 and RO stages were established;
- P0 close operation 07 returned a genuine marked `CLOSE_STOP` / rc 3;
- independent RO close operation 08 returned a genuine marked `CLOSE_FAIL` / rc 1.

The exact classifier reported operation 08 as `not_evaluable reason=cleanup_after_unestablished_prerequisite`, produced `deviant=0`, and ended `TR_RUN STOP` / rc 3. The RO deviation was erased solely because the unrelated P0 close had stopped first.

**Adjudication:** the broad rule should **not** be ratified. “Always run” is an execution policy, not a declaration that all cleanup rows share one prerequisite. Model prerequisites per branch and operation: P0 close depends on P0 stage establishment; RO close on RO stage establishment; each fetch on its corresponding close; each local bind on its corresponding close/fetch. An unrelated branch's failure must not make a genuine marked rc 1 non-evaluable. Add this case as D026 RED/GREEN evidence. RED is verified; no GREEN exists.

## Executed closure matrix

The following were driven against the raw round-3 runner or exact target logic; `R2` controls used the cited pre-repair bytes where applicable.

| Fixture | R2/control observation | Round-3 observation |
|---|---|---|
| Early operation-01 non-match with later `always` rows | `deviant=4`, `not_evaluable=3`, `TR_RUN FAIL` rc 1 | `deviant=0`, `not_evaluable=7`, all `always` rows retained, `TR_RUN STOP` rc 3 |
| Real `ssh`-kind child rc 255 | `TR_RUN FAIL` rc 1 | `reason=ssh_transport_failure_rc255`, STOP rc 3 |
| Remote observed rc 2 | `TR_RUN FAIL` rc 1 | `reason=rc_outside_outcome_grammar`, STOP rc 3 |
| Remote rc 0 with empty output | — | `reason=no_remote_program_marker_in_capture`, STOP rc 3 |
| Genuine marked remote rc 1 | — | `deviant`, `TR_RUN FAIL` rc 1 |
| Failed `scp` rc 1 | `TR_RUN FAIL` rc 1 | `reason=scp_transfer_did_not_complete`, STOP rc 3 |
| Real pinned `ssh`, exact R2 environment | rc 255, empty streams | — |
| Real pinned `ssh`, round-3 environment/options | config evaluation rc 0; hostile config excluded | runner stopped because the local config evaluation emitted no remote marker, as required |
| Real pinned local-to-local `scp` through runner | — | `TR_RUN PASS` rc 0; destination bytes identical |
| Setup bind-mounted decoy | rc 0; four directories created in decoy | rc 3 `parent_mount_differs`; zero directories |
| Close hostile PATH-first `sha256sum` | accepted original mutated `a.txt` and printed PASS | derived script never consulted plant; no mutation |

For the mountinfo reader, I additionally tested empty input, short input, missing separator, no covering record, and a populated final record without LF. All malformed/absent cases stopped before `mkdir`; the complete unterminated final record was consumed and the control setup completed.

## Frozen identities, census, and syntax evidence

| Target | Bytes | SHA-256 | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` | CR bytes |
|---|---:|---|---:|---:|---:|
| `run_p0.sh` | 5,215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` | 6 | 3 | 0 |
| `run_ro.sh` | 5,933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` | 6 | 5 | 0 |
| `transport_runner.ps1` | 57,826 | `13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4` | 4 | 8 | 0 |
| `TRANSPORT_PLAN.tsv` | 7,219 | `2a1cd2a65d447526dee8748b17a762dfe85e88de686a8f7d337dff8830161650` | 20 | 7 | 0 |
| `remote_setup_wpi.sh` | 17,775 | `c0b7caa7f856db6b6d8aad4d407d42d450064a9e55a9cbbacf464f28e97b8d74` | 0 | 3 | 0 |
| `remote_extract_verify_wpi.sh` | 16,614 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` | 0 | 7 | 0 |
| `remote_close_tree_wpi.sh` | 12,039 | `fc183751c634c7fd6d1d9bd75143b7229357e52b7eec5f25a8eec0192bd1f75f` | 0 | 0 | 0 |
| `SELF_QA_TRANSPORT.md` | 100,406 | `84730522fd77b4a754d35556b740f6438a0bd0bc68e3d90340cb348b715c27da` | 6 | 10 | 0 |
| `STATUS_TRANSPORT.md` | 7,445 | `dfdf7fb931905e3f6404c14bb32dd3c93f0323c812dc5ae10c1fb3c9c2be23a7` | 1 | 1 | 0 |

The seven executable/plan rows total **36 allocation markers and 33 pin markers**, matching N1. The accepted derivation bases independently hashed as:

- `remote_setup.sh`: 4,976 bytes, `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5`
- `remote_extract_verify.sh`: 8,270 bytes, `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3`
- `remote_close_tree.sh`: 7,470 bytes, `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e`
- accepted wrapper base `run_r45.sh`: 4,219 bytes, `4b9e5e68cc5959bfdefc2b9996556a986e4004e553b410dc2cfcf65e50c44a7b`

All five delivered shell targets passed `bash -n`; the accepted original close script also passed as a control. Windows PowerShell 5.1 parsing of `transport_runner.ps1` reported `PARSE_ERRORS=0`.

## Optional nits

1. Preregistration §4 says “Four scripts are reused” and later “four derived scripts,” but the enumerated/frozen set contains five delivered derived shell files (`remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`, `remote_close_tree_wpi.sh`, `run_p0.sh`, and `run_ro.sh`) derived from four accepted bases. Normalize the count to prevent a freeze inventory ambiguity.
2. After the required repairs, composing the runner's unfilled-marker sentinel instead of storing the exact globally filled literal would make Stage-1 tooling less brittle. The current behavior is fail-closed, so this is optional.

## Acceptance condition

Do not freeze or execute the transport set until F1-F4 are repaired and independently re-audited under the T0 policy. Each new regression test offered as closure evidence must include recorded RED output against the vulnerable behavior (or an equivalent mutation) and GREEN output with the fix, per D026.

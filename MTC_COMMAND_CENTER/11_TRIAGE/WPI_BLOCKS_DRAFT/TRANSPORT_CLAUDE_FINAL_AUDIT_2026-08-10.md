Audit complete. Full report follows.

---

# T0 FLAGSHIP ACCEPTANCE AUDIT — WP-I transport set, round-3 bytes

## VERDICT: **PASS-WITH-NITS**

**Slot:** Claude flagship, `claude-opus-5`, xhigh, fresh session, 2026-08-10.
**Targets:** the nine transport files at commit `78173bfd`, plus the three accepted Stage-2 derivation bases.
**Method:** every V-row below was re-driven by fixtures I wrote in this session. I did not reuse a single arm, transcript, or fixture from `SELF_QA_TRANSPORT.md`, `TRANSPORT_REPAIR_R3_REPORT.md`, or either round-2 re-audit. Where an implementer arm and mine agree, that is convergence, not citation.

**Safety state.** No host contact. No SSH/SCP connection was attempted; no host key was offered; no credential was read. The only hostname passed to `ssh` was the non-resolving literal `qa-target` under `-G`, which returns before name resolution. The only sockets were loopback (`127.0.0.1:9`, and one ephemeral listener I opened and closed myself). The real pinned `ssh.exe` and `scp.exe` were executed locally without connecting, which the kickoff put in scope. No RUNID was minted — `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry. Nothing in the repository was modified: `git status` over `WPI_BLOCKS_DRAFT`, `02_PREREG` and `WPI_PREREG_DRAFT_ROUND1` shows no change attributable to this session, and all twelve target blobs are byte-identical across `78173bfd`, the concurrent `HEAD` (`286d8fce`), and the worktree. All fixtures lived in `C:\tmp\wpiaudit` and `/wpiaud_*` (removed). `RP6-P0.sh`, `RP7-WPI-RO.sh` and the pathscope files were neither read nor written — they moved under me during the audit and my targets did not.

---

## 1. V-rows

| V | Result | Independent evidence |
|---|---|---|
| **V1 — F1, transport/cleanup failure never becomes FAIL** | **CLOSED** | Nine of my own runner arms (`X1`–`X9`) driving the delivered classifier through a freeze-simulated fixture. Detail in §2. |
| **V2 — F2, the real pinned OpenSSH runs, ambient config cannot influence it** | **CLOSED** | `M1/M2` + an 8-way one-variable-out bisect + four hijack arms + two runner arms (`K1/K2`) with the real programs. Detail in §3. |
| **V3 — F3, close script consults no inherited PATH; PATH-first `sha256sum` cannot mutate evidence while reporting PASS** | **CLOSED** | RED on the accepted bytes reproduced the mutation-with-PASS; GREEN on the derived script refused it; three PATH-independence arms. Accepted original re-derives to `87157f0e…` / 7470 B, untouched. Detail in §4. |
| **V4 — F4, decoy bind mount at the allocation parent refused before any `mkdir`** | **CLOSED** | Real `mount --bind` under WSL root. RED (mount binding removed) put four directories in the decoy; GREEN STOPped with zero directories anywhere. Detail in §5. |
| **V5 — N1, placeholder census accurate** | **CLOSED** | Re-derived: **36 / 33** over the seven executable/plan files — exactly the repair report's §4 table. Rejected-baseline figures **36 / 27** (six files) and **41 / 33** (all eight) re-derive and match both round-2 re-audits. |
| **V6 — derivation minimality, four-class contract** | **PASS** | Full `diff -u` of all three `_wpi` scripts against their accepted bases. Every non-comment delta falls inside classes 1–4. No drift. Detail in §6. (The kickoff says "FOUR `_wpi` scripts"; there are **three** — see nit N-b.) |
| **V7 — whole-set sweep, independent of the finding lists** | **PASS** | §5 op-list ↔ plan fidelity 12/12; first-mismatch ordering with `always` retention; per-op capture complete; line-reader completion conditions; row-24 probe classification; STOP-before-mutation; read-only scope. Detail in §7. |
| **V8 — freeze safety of `$UNFILLED_MARKERS`** | **JUDGED: disclosure sufficient; repair recommended as a nit, not required** | Executed both directions (`Z1`/`Z2`). Detail in §8. |
| **V9 — identities, placeholders, syntax, byte hygiene** | **PASS** | Table in §9. Zero CR **bytes** (counted per byte, not per matching line) in all seven executable/plan files. `bash -n` passes on all five in-scope shell files and all three accepted originals. `[Parser]::ParseFile` → **0 errors** under Windows PowerShell 5.1.26100.8875; no `&&`, `\|\|`, or ternary. Placeholders literal, no RUNID minted. |

---

## 2. V1 — F1, executed falsification

I built a fixture copy of `transport_runner.ps1` in which **only frozen constants** were substituted (allocation tokens, the four directory pins, plan/kit/program/config digests, and the option block). `Get-OpOutcomeClass`, `Invoke-ExternalProcess`, `Invoke-LocalBind`, `Invoke-TcpProbe`, the classification loop and the rollup are byte-identical to the delivered file. Each substitution was asserted unique before it was applied (17 anchors, all matched exactly once). `cmd.exe` (`65ec268a…`) stood in for the transport programs in the X family purely to produce deterministic native exit statuses; the K family in §3 uses the real programs.

All arms ran the full 12-row plan shape unless noted.

| arm | what it drives | result | runner exit |
|---|---|---|---|
| **X1** | op 01 STOPs (rc 3, marker present); ops 02–06 skipped; both closes return 1; both retrievals return 1; both binds STOP | `deviant=0 not_evaluable=7` → **`TR_RUN STOP`** | **3** |
| **X2** | op 01 native rc **255**, zero output | `reason=ssh_transport_failure_rc255` → **STOP** | **3** |
| **X3** | op 01 rc **2**, marker present | `reason=rc_outside_outcome_grammar` → **STOP** | **3** |
| **X4** | op 01 rc **0** with no output at all | `reason=no_remote_program_marker_in_capture` → **STOP**, ops 02–05 never ran | **3** |
| **X5** | op 01 rc **1** *with* a remote marker | `class=deviant` → **`TR_RUN FAIL`** | **1** |
| **X6** | op 02 `scp_up` rc **1** | `reason=scp_transfer_did_not_complete` → **STOP** | **3** |
| **X7** | full happy path, real close records bound against a real retrieved tree | 12/12 `class=match`, `TR_BIND_PASS files=2`, remote and reconstructed set digests equal | **0** |
| **X8** | ops 01–06 all match, then `always` op 07 rc 1 with marker | `class=deviant` → **`TR_RUN FAIL`** | **1** |
| **X9** | op 06 STOPs (rc 3), then `always` op 07 genuinely observes rc 1 | `reason=cleanup_after_unestablished_prerequisite` → **STOP** | **3** |

X1 is the exact case Codex named: one honest STOP at op 01, four consequences of itself, and the round-2 classifier turned that into `TR_RUN FAIL`. It is now `deviant=0 not_evaluable=7`, exit 3, with every not-evaluable op individually enumerated by `TR_OP_NOT_EVALUABLE`, so the STOP is never silently absorbed.

X5 and X8 are the arms that matter for not over-correcting: FAIL is still reachable, both for a `sequence_ok` op and for an `always` op whose prerequisite sequence completed. The repair did not buy STOP-everywhere by throwing away the FAIL class.

X9 is the arm I built specifically for the open adjudication — see §10.

## 3. V2 — F2, executed falsification

Real `C:\Windows\System32\OpenSSH\ssh.exe` = `8607ff933e769e77534b1244e39965bcf1c904dbfd4b9da819bbb71034cfef88`, `scp.exe` = `7758d689e2203c5e459fa5b8251f8a3ce27c3c8f0b5dcf6c2313909f25c2cb13`. Environments were built with `EnvironmentVariables.Clear()` and repopulated exactly as the runner does.

```
M1  round-2 constructed environment (no PROGRAMDATA)     rc=255  stdout=0  stderr=0
M2  round-3 environment (+ run-owned empty PROGRAMDATA)  rc=0    stdout=4076
```

One-variable-out bisect over the round-3 set — `SystemRoot`, `windir`, `ComSpec`, `PATHEXT`, `PATH`, `TEMP`, `TMP`, `PROGRAMDATA`:

```
without_SystemRoot rc=0   without_windir rc=0   without_ComSpec rc=0   without_PATHEXT rc=0
without_PATH       rc=0   without_TEMP   rc=0   without_TMP     rc=0
without_PROGRAMDATA rc=255 stdout=0 stderr=0
```

`PROGRAMDATA` is the only load-bearing variable. The round-2 environment could not have reached a remote block, and F1 would then have reported that as host FAIL. Both halves of the round-2 defect are real and both are now closed.

Hijack pair (my own hostile files, none planted in the operator's real profile):

```
H1  hostile system-wide ssh_config reachable via PROGRAMDATA, no -F
      rc=255  "Bad owner or permissions on __PROGRAMDATA__\ssh/ssh_config"   <- the file WAS consulted
H2  same file + -F none
      rc=0, no proxycommand, file never consulted
H3  -F <hostile per-user config>
      rc=0, effective config carries: proxycommand C:\evil\PERUSER_CONFIG_HIJACK.exe %h %p
H4  -F none
      rc=0, no proxycommand line at all
```

H1/H2 prove `-F none` makes the system-wide file unreachable; H3/H4 prove `-F none` selects **no** configuration file, which is the channel the per-user `ssh_config` travels on. I also independently tested the load-bearing claim behind dropping `USERPROFILE`/`HOMEDRIVE`/`HOMEPATH`:

```
H5  HOME + USERPROFILE + HOMEDRIVE + HOMEPATH all pointed at a fixture home
    containing .ssh\config with a ProxyCommand, run WITHOUT -F
      rc=0, no proxycommand -> this build resolves the home directory from the OS token,
      not from the environment. Carrying those variables never closed that channel;
      only -F none plus the pinned files does. The repair report's claim holds.
```

Full pinned block in effect under the round-3 environment (`ssh -G`): `batchmode yes`, `stricthostkeychecking true`, `identitiesonly yes`, `connecttimeout 20`, `controlmaster false`, `permitlocalcommand no`, `forwardagent no`, `forwardx11 no`, `clearallforwardings yes`, `userknownhostsfile`/`globalknownhostsfile`/`identityfile` all at the pinned paths, no `proxycommand`, no `controlpath`.

Driven through the runner's own `Invoke-ExternalProcess`:

```
K1  real ssh.exe, pinned block + -G qa-target
      TR_PROGRAM name=ssh sha256=8607ff93... resolution=pinned_absolute chain=trusted
      TR_OP_END id=01 rc=0 (real output)
      TR_OP_CLASS class=not_evaluable reason=no_remote_program_marker_in_capture
      TR_RUN STOP, exit 3
K2  real scp.exe, local-to-local through the runner, no socket
      TR_OP_CLASS class=match -> TR_RUN PASS, exit 0
      source_sha == copy_sha (bytes actually moved)
```

K1 is worth stating plainly: the real program now *runs*, and the provenance gate still correctly refuses to read its rc 0 as a probe result because no remote program spoke. That is the F1 and F2 repairs holding at the same time, on the real binary.

**Scope limit, stated rather than implied.** This establishes initialisation, option parsing and option effect under the constructed environment, and a real byte-moving `scp`. It does not establish that the host accepts the pinned key, that the credential authenticates, or that a remote `bash -s` runs. The prereg and STATUS both say so.

## 4. V3 — F3, executed falsification

Accepted `remote_close_tree.sh` re-derives to **7470 B / `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e`** — byte-identical to the pinned identity, and `git status` shows no change under `02_PREREG/`. It was not edited.

My attack: a `sha256sum` first on `PATH` that appends one line to the evidence leaf `a.txt` exactly once, then `exec`s the real tool. Owner constant substituted to `root:root` (fixture only); nothing else changed.

```
RED   accepted bytes + plant
        RC=0   PATH_PLANT_CONSULTED=yes calls=5   MUTATED=yes
        PRE_SHA =8da7359a1d20ce6c976e7a3e2536dafd56f53367e4ce153f0765222b1e91fc70
        POST_SHA=8e4d50b9292855abd3f22f2cfd86c5e2673db47a2250a82cbf29ddc552189847
        CLOSE_DIGEST 8e4d50b9...  a.txt          <- the POST-mutation digest
        CLOSE PASS runid=QAP0 ... wrote_into_evidence_tree=0

G0    derived, exactly as shipped, on this host
        RC=3   CLOSE_STOP reason=tool_is_symlink path=/usr/bin/stat   MUTATED=no

GREEN derived, pins retargeted to root-owned regular copies, same plant
        RC=0   PATH_PLANT_CONSULTED=no calls=0   MUTATED=no
        CLOSE_DIGEST 8da7359a...  a.txt          <- the true value
```

PATH-independence, three arms, all rc 0, all nine pinned-tool admissions emitted, no mutation:

```
PATH=""                    RC=0  MUTATED=no  pinned_tool_admission_notes=9
PATH="/nonexistent-dir-xyz" RC=0  MUTATED=no  pinned_tool_admission_notes=9
PATH="/usr/bin:/bin"        RC=0  MUTATED=no  pinned_tool_admission_notes=9
```

The script runs identically with `PATH` empty. Static sweep for a surviving bare invocation of `mktemp`/`stat`/`tr`/`readlink`/`find`/`sort`/`sha256sum`/`cmp`/`rm` outside a `TOOL_` pin: **NONE**.

G0 reproduces deviation **D-3** independently: this QA kernel ships `/usr/bin/{stat,mkdir,readlink,mktemp,tr,sort,sha256sum,rm}` as symlinks (mode 777), and the scripts refuse them. That is the safe direction and STATUS already records it as a hard Stage-1 precondition on `GATEA-STAGING`.

## 5. V4 — F4, executed falsification

Real bind mount, WSL root, with the parent chain and mount pin filled as at freeze. I derived the attested projection **independently** with my own `mountinfo` parser and confirmed the script's own projection is identical (`device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1`).

```
PIN   shipped bytes, EXPECT_PARENT_MOUNT still a placeholder
        RC=3  SETUP_STOP reason=mount_pin_unfilled field=EXPECT_PARENT_MOUNT

CTL   no decoy, shipped logic
        RC=0  parent_mount_bound ... attestation=deploy_channel_before_op_01
        accepted_object_dirs=4  decoy_object_dirs=0

RED   decoy bind-mounted over the parent, ONLY bind_parent_mount removed
        RC=0  SETUP PASS ... owner_numeric=0:0 owner_name=root:root mode=700
        DIRS_CREATED_IN_DECOY=4   DIRS_CREATED_IN_ACCEPTED_OBJECT=0

GREEN decoy bind-mounted over the parent, shipped logic
        RC=3  SETUP_STOP reason=parent_mount_differs
              observed=[... root=/wpiaud_f4/decoy mount_point=/wpiaud_f4/parent ...]
              attested=[... root=/ mount_point=/ ...]
        zero directories anywhere, mounted or unmounted
```

The RED arm is the finding in one line: `readlink -f` answered the expected path, the owner and mode were the expected ones, every component predicate passed, and all four allocations landed inside the substituted object. The mount binding runs at line 322, before the first `allocate` at line 333.

## 6. V6 — derivation minimality

Full `diff -u` against each accepted base:

| derived | insertions / deletions | non-comment |
|---|---:|---:|
| `remote_setup_wpi.sh` ← `remote_setup.sh` | +268 / −50 | +174 / −37 |
| `remote_extract_verify_wpi.sh` ← `remote_extract_verify.sh` | +234 / −69 | +182 / −55 |
| `remote_close_tree_wpi.sh` ← `remote_close_tree.sh` | +110 / −30 | +62 / −17 |

I read every non-comment deletion and mapped it to a class. **No delta falls outside the four-class contract.**

*Close script* — the 17 non-comment deletions are 16 bare tool invocations replaced by the same invocation through its pin, plus the `usage` diagnostic string that names the script. No predicate, rc, ordering, comparison or emitted record changed. `rm` is pinned too although it was not in the kickoff's enumeration; the accepted bytes invoke it three times, so pinning it is required for class 2 to be complete. Entirely class 2.

*Setup* — constants (class 1); `probe_path` → `calibrate_absence` + `probe_leaf` (class 3); rendered `%U:%G` → numeric `%u:%g` with the name kept diagnostic (class 3); allocate/assert interleaved so no object is created through an unverified parent (class 3); mount projection and binding (class 3, added this round); bare tools → pins (class 2). The `SETUP PASS` line changed shape only to carry `owner_numeric` — a consequence of class 3, not an independent change.

*Extractor* — byte-identical to the rejected baseline, as claimed. Constants and the member/hash block (class 1); the literal `9` removed everywhere in favour of `MEMBER_COUNT` derived from `MEMBERS` (class 1 — "no member-count literal may exist"); `run_capture` status/diagnostic/termination adjudication before stdout is parsed (class 4); bare tools → pins including `TOOL_CHMOD` (class 2). I specifically checked that the extraction hardening did not quietly drop behaviour: `chmod 0444` is retained (line 325, pinned, with a diagnostics check added) and `sha256sum -c --strict` is retained (line 339, pinned). Nothing was removed.

I also confirmed the claim that `remote_extract_verify_wpi.sh`, `run_p0.sh` and `run_ro.sh` are byte-identical to the rejected baseline `9ef4437d`, and that `transport_runner.ps1`, `TRANSPORT_PLAN.tsv` and `remote_setup_wpi.sh` are not. Both halves are true.

## 7. V7 — whole-set sweep

**§5 op list ↔ plan fidelity: 12/12.** Every row's kind, `run_when`, `expect_rc`, working directory, stdin artefact and post-option argv matches §5's table, including the two `always` closes now naming `PREREG:remote_close_tree_wpi.sh`, the two `scp_down` rows running from `<record>\evidence` with a bare `.` destination, and both `local_bind` rows naming their close/fetch pair. Every row preregisters `expect_rc = 0`. No scp argument contains a drive-letter colon.

**First-mismatch ordering with `always` retention** — X1, X5, X6, X8 above: on the first non-match, remaining `sequence_ok` ops are skipped and every `always` op still runs; `prerequisiteEstablished` is latched *before* the op executes.

**Line reader, three completion conditions plus byte hygiene** — driven through the plan:

```
clean LF-terminated       TR_PLAN_READ completion=clean_eof records=3   exit 0
CRLF                      TR_STOP plan_carriage_return_not_allowed      exit 3
no final LF               TR_STOP plan_unterminated_final_record        exit 3
zero bytes                TR_STOP plan_empty_input                      exit 3
raw 0xC3 0xA9             TR_STOP plan_non_ascii_byte                   exit 3
raw 0x07                  TR_STOP plan_control_byte_7                   exit 3
```

**Row-24 probe classification**, against a loopback listener I opened and then closed:

```
port open      B6_FAIL reason=host_reachable_8790 outcome=connected   rc=1 -> class=deviant -> TR_RUN FAIL exit 1
port closed    B6_external row=24 outcome=connection_refused          rc=0 -> match       -> TR_RUN PASS exit 0
port invalid   B6_STOP  outcome=port_invalid                          rc=3 -> not_evaluable -> STOP exit 3
```

`rc 1` on `tcp_probe` is a genuine completed observation and correctly survives as FAIL — the kind rule does not over-absorb it.

**STOP before mutation, and the interlocks:**

```
record root create-once    second run: TR_STOP record_root_already_exists   exit 3
no switches                TR_DRY_RUN no_process_was_started no_connection_was_opened  exit 0
-Execute + wrong token     TR_DRY_RUN no_process_was_started no_connection_was_opened  exit 0
plan digest mismatch       TR_STOP plan_sha256_mismatch                    exit 3
stdin digest mismatch      TR_STOP stdin_sha256_mismatch op=01             exit 3
unknown stdin root         TR_STOP stdin_root_unknown=NOSUCH               exit 3
traversal in stdin leaf    TR_STOP stdin_leaf_unsafe (PREREG:../stdin_a.txt) exit 3
cwd off the allowlist      TR_STOP plan_row_cwd_not_preregistered cwd=C:\Windows exit 3
kind/program disagreement  TR_STOP plan_row_kind_program_mismatch kind=scp_up program=ssh exit 3
```

**The frozen option block is a property of the runner, not of the plan** — three separate mutations, all refused before any process starts:

```
drop '-F none'                 TR_STOP plan_row_pinned_option_differs index=1  actual=[-i] expected=[-F]
re-point UserKnownHostsFile    TR_STOP plan_row_pinned_option_differs index=14 actual=[...C:\evil\kh]
reinstate ProxyCommand         TR_STOP plan_row_pinned_option_differs index=18 actual=[ProxyCommand=C:\evil\p.exe]
```

**Per-op capture** — the X7 record carries 12 each of `.argv`, `.stdout`, `.stderr`, `.rc`, `.elapsed_ms`, a 123-line `TRANSPORT_RECORD.txt`, and a 64-line `TRANSPORT_SHA256SUMS.txt` covering every record file except itself.

**Read-only scope** — every write the runner performs is under `RECORD_ROOT`. Nothing is written into the preregistration directory, the runkit directory, or the accepted Stage-2 directory. The binder (ops 11/12) enumerates, hashes and compares only.

**No regression in the binder after the F1 refactor** — X7 drove a real close record against a real retrieved tree: `TR_BIND_COUNTS remote=2 local=2`, `TR_BIND_SET` remote and reconstructed digests equal, `TR_BIND_PASS files=2`, and the `$Matches` latching from round 2 still holds.

## 8. V8 — freeze safety: my judgement

**Judgement: the disclosure plus the per-constant-fill requirement is sufficient. The runner does not need a required repair. I recommend the one-line change anyway, as a nit.**

The reason is that the destroyed guard fails **closed**, and I drove both directions to be sure rather than reasoning about it:

```
Z1  per-constant fill (the correct procedure)
      TR_MARKER_GATE constants=marker_free ... TR_RUN PASS   exit 0

Z2  blind global replacement of the allocation placeholder, as the implementer warns
      TR_STOP reason=unfilled_marker field=BASE_RUN          exit 3
      $UNFILLED_MARKERS = @('WPIAUD', '<PIN-AT-FREEZE>')
```

Three things follow. First, the failure is deterministic, not probabilistic: after a global fill, `$UNFILLED_MARKERS[0]` *is* the RUNID, `$BASE_RUN` *is* the RUNID, so the very first `Assert-MarkerFree` fires. There is no fill value that escapes it. Second, it fires before the record root is created and before any path is evaluated, so nothing is allocated and no host is contacted. Third — and this is the part that decides it — the pin half of the guard survives: `$UNFILLED_MARKERS[1]` is still `<PIN-AT-FREEZE>`, so a genuinely unfilled digest is still caught, and `Test-HexSha256` is a second independent gate on every digest constant. There is no fail-open direction.

What it costs is a correctly frozen set STOPping with a diagnostic that says the opposite of the truth (`unfilled_marker field=BASE_RUN` on a filled `BASE_RUN`), and — under §1's one-use rule — a burned RUNID at the moment the operator is least equipped to read the reason. `remote_setup_wpi.sh` already solves this in one line (`PIN_MARKER="$(printf '<PIN-%s>' 'AT-FREEZE')"`). The set is internally inconsistent for no benefit, and the fix is smaller than the disclosure paragraph describing it. See nit N-g.

## 9. V9 — identities, placeholders, syntax

| file | bytes | CR bytes | high bytes | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` | SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| `transport_runner.ps1` | 57826 | 0 | 0 | 4 | 8 | `13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4` |
| `TRANSPORT_PLAN.tsv` | 7219 | 0 | 0 | 20 | 7 | `2a1cd2a65d447526dee8748b17a762dfe85e88de686a8f7d337dff8830161650` |
| `remote_setup_wpi.sh` | 17775 | 0 | 6 | 0 | 3 | `c0b7caa7f856db6b6d8aad4d407d42d450064a9e55a9cbbacf464f28e97b8d74` |
| `remote_extract_verify_wpi.sh` | 16614 | 0 | 9 | 0 | 7 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` |
| `remote_close_tree_wpi.sh` | 12039 | 0 | 5 | 0 | 0 | `fc183751c634c7fd6d1d9bd75143b7229357e52b7eec5f25a8eec0192bd1f75f` |
| `run_p0.sh` | 5215 | 0 | 0 | 6 | 3 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` |
| `run_ro.sh` | 5933 | 0 | 0 | 6 | 5 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` |
| **seven executable/plan files** | | **0** | | **36** | **33** | |
| `SELF_QA_TRANSPORT.md` | 100406 | 0 | 362 | 6 | 10 | `84730522fd77b4a754d35556b740f6438a0bd0bc68e3d90340cb348b715c27da` |
| `STATUS_TRANSPORT.md` | 7445 | 0 | 40 | 1 | 1 | `dfdf7fb931905e3f6404c14bb32dd3c93f0323c812dc5ae10c1fb3c9c2be23a7` |

Accepted derivation bases, re-verified unchanged and unedited:

| file | bytes | SHA-256 |
|---|---:|---|
| `02_PREREG/remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` |
| `02_PREREG/remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` |
| `02_PREREG/remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` |

`bash -n` OK on all five in-scope shell files and all three accepted originals (GNU bash 5.3.9). PowerShell 5.1.26100.8875 parse: 0 errors. The delivered runner, executed exactly as it ships, emits `TR_STOP reason=unfilled_marker field=BASE_RUN` at exit 3 before evaluating a path — `STATUS_TRANSPORT.md:16–18` is accurate.

---

## 10. Open adjudication — the deliberately broad `always`-cleanup rule

**My opinion: ratify it as written. The Lead should ratify the rule, not merely tolerate it.** The reasoning, with the arm that makes the trade-off concrete:

The rule is narrower than "deliberately broad" suggests. It only engages when `prerequisiteEstablished` is false, i.e. when some earlier op already failed to match. X8 shows the other side: with the sequence intact through op 06, an `always` op that ran and returned 1 is still `class=deviant` and still produces `TR_RUN FAIL` at exit 1. The rule does not blanket-immunise cleanup rows; it immunises them only downstream of a break.

The cost is real and X9 is it. Op 06 STOPped (a probe that could not be evaluated — not a host-state finding). Op 07 then ran and genuinely observed rc 1 on the P0 evidence tree. Because the sequence was already broken, that observation was recorded as `cleanup_after_unestablished_prerequisite` and the run reported STOP rather than FAIL. A true statement about host state was downgraded to "could not evaluate."

I would still ratify, for three reasons. First, the asymmetry of harm is the right way round: a spurious FAIL is an accusation against the staging host recorded after one-use RUNIDs are spent and unrecoverable — exactly the `[B3-ADJ Classification]` hand-adjudication the preregistration exists to eliminate — whereas a downgraded FAIL costs a re-run. Second, nothing is lost from the record: X9 still emits `TR_OP_CLASS id=07 rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite` and counts it in `TR_RUN_CLASS`, so the operator can see precisely what happened and why it was not counted. The rule changes the verdict, not the evidence. Third, the alternative — deciding per-op whether a cleanup's failure is independent of the earlier break — requires the runner to know *why* op 07 returned 1, which it cannot; that is the kind of inference that produced the round-2 defect in the first place.

One refinement, if the Lead wants the record sharper without changing the verdict: the reason token is the same whether the earlier break was a STOP or a FAIL, and those are different situations. Distinguishing `cleanup_after_unestablished_prerequisite` from `cleanup_after_earlier_deviation` would cost one branch and make X9's transcript self-explaining. That is a nit, not a condition.

---

## 11. Nits — none gates acceptance

**N-a — `WPI_PREREGISTRATION_DRAFT.md` §4 contradicts itself, and it is the section the Lead is being asked to ratify.** Line 216 still reads *"Four scripts are reused from the accepted Stage 2 set at their recorded digests"*; line 231 reads *"Reused-script disposition (round 3, superseding the round-1.5 wording): **no accepted Stage-2 script travels unchanged any more.**"* Both sentences are in the same section, fifteen lines apart. The second is correct and dated; the first is stale round-1.5 text that survived the round-3 edit. A reader who stops at the opening paragraph will believe four accepted scripts travel byte-identical, which is precisely the claim round 3 falsified. This is documentation, not runtime, but §4 *is* the derivation contract this audit binds against — I would fix it before ratification rather than after.

**N-b — the "four derived scripts" count does not re-derive from its own enumeration.** §4 calls `remote_close_tree_wpi.sh` the *"Fourth derived script"* and then says *"There are now four derived scripts — `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh` and `remote_close_tree_wpi.sh`, plus `run_p0.sh` and `run_ro.sh` as new wrappers"* — three named derivations followed by two wrappers, under the heading "four". There are **three** `_wpi` derived scripts. The error has propagated: `STATUS_TRANSPORT.md:22`, `TRANSPORT_REPAIR_R3_REPORT.md` §1 F3, and this audit's own kickoff (*"the FOUR `_wpi` scripts"*) all carry it. Pattern 10: a count in the closure document that does not re-derive.

**N-c — `SELF_QA_TRANSPORT.md` §9 cross-reference is off by two sections.** It sends the reader to `TRANSPORT_REPAIR_R3_REPORT.md` **§6** for the round-3 delivered figures; the table is in **§4**, and §6 is "Round-2 findings: no regression".

**N-d — the set is internally inconsistent on numeric identity, deliberately.** `remote_setup_wpi.sh` was required to compare `%u:%g` numerically with the rendered name kept diagnostic (Pattern 8). `remote_close_tree_wpi.sh` still compares the rendered `%U:%G` against `gatea:gatea`, because making it numeric would be a class-3 change and this derivation is class-2-only. That is correct process and it is disclosed in §4 and in the repair report's residual list — but it leaves the same defect the audit chain closed on one script open on another, on the operation that produces the evidence binding. I would ask the Lead to authorise a narrow class-3 exception for this one predicate in the successor rather than carry it indefinitely.

**N-e — `TR_ENV_POLICY … ambient_ssh_config=disabled_by_-F_none` is asserted, not derived.** It is a fixed string; nothing checks that `$SSH_PINNED_OPTIONS` still begins with `-F none`. It is true of the delivered bytes (I verified), and the per-row verbatim check enforces the plan side, so the exposure is limited to a future edit of the constant. A record line should state what it measured.

**N-f — the `ACCEPTED` stdin root is registered but no longer used.** `$STDIN_ROOTS` still maps `ACCEPTED` → the Stage-2 directory although no plan row names it now that ops 07/08 resolve through `PREREG`. Harmless while the plan is digest-pinned inside the runner; the repair report explains the retention as documenting the derivation basis. Worth one sentence in §4 so a later reader does not treat it as a live path.

**N-g — compose the runner's `$UNFILLED_MARKERS` entries, as `remote_setup_wpi.sh` already does.** See §8. One line, removes a fail-closed-in-the-wrong-place trap that costs a one-use RUNID and prints a diagnostic that contradicts itself.

**N-h — distinguish the two `always`-cleanup reasons.** See §10.

---

## 12. Observations — recorded so the Lead adjudicates them rather than discovering them

1. **`mktemp` in the close script still honours the login `TMPDIR`** (disclosed residual 2). I traced the worst case rather than accepting the disclosure: if `TMPDIR` pointed *inside* `EV_DIR`, the work directory's `raw.0` would be enumerated into the digest set and then removed by `rm -rf -- "$WORK"` before op 09 retrieves the tree, so the local binder would report `missing_locally` and the run would end FAIL, not PASS. It cannot produce a false attestation. It is also barely reachable: `EV_DIR` is created by op 01 during the run at mode 0700. Low risk, correctly disclosed, and the successor deploy-channel item covers it.

2. **The mount binding is a point-in-time statement about the allocation parent only.** The four created directories are not themselves mount-bound, and nothing prevents a mount being stacked between `allocate "$BASE"` and `allocate "$EV_PARENT"`. That requires concurrent root on the host, and RP6's full `normalised_path_projection_v2` covers the later stages. This is what F4 asked for and what the Lead adjudicated; I note the boundary, not a defect.

3. **Remote tool bytes are not bound** (disclosed residual 1). The pins bind a locator and that object's metadata; the runtime digests are emitted as evidence and explicitly not compared. The scripts say so in their own `CLOSE_NOTE tool_digest_limit …` line. Correct handling of a limit that cannot be closed before host contact.

4. **D-3 is a hard Stage-1 precondition and I reproduced it.** `GATEA-STAGING` must carry every `/usr/bin/<tool>` in the pin set as a regular, root-owned, not-group/other-writable file, or ops 01, 03, 07 and 08 STOP at dispatch. On this QA kernel eight of ten are symlinks and the scripts refuse them — the safe direction, but not the target host's state.

## 13. What I did not verify

- Real connection behaviour against `GATEA-STAGING`: host key acceptance, credential authentication, remote `bash -s` execution, and the remote scripts' behaviour on the real host. `ssh -G` and a local `scp` bound the configuration and program identity; the transport itself is unverified until dispatch.
- `Invoke-TcpProbe`'s `timeout`, `connect_incomplete` and `local_exception` arms — they need socket states loopback will not produce, or a destination outside this envelope. All three fail toward rc 3.
- `Test-TrustedProgramChain`'s reparse-point branch (needs a reparse point under `%SystemRoot%`, i.e. elevation). I did confirm the predicate **accepts** the real `ssh.exe`, `scp.exe` and `cmd.exe` on this host, so it is not vacuously fail-closed.
- The six-member happy path against the real WP-I `runkit.tar` — the kit does not exist before Stage 1; `01_RUNKIT` is absent from the draft directory and the runner STOPs at `pinned_file_pin_unfilled` until it is built.
- `RP6-P0.sh`, `RP7-WPI-RO.sh`, and the pathscope files — separate slots, under concurrent repair, and not transport targets. They changed under me during this audit; my twelve targets did not.

## 14. Required next action

The five round-3 findings are closed, each against a falsification I built and executed myself, and the whole-set sweep found no runtime defect. The set is **acceptable on the runtime evidence**.

Before freeze, I would have the Lead do three things, none of which needs another repair round: ratify §4 as amended (four-class contract, fourth-script clause, mount-object clause, configuration-identity paragraph); ratify the `always`-cleanup rule per §10; and have nits **N-a** and **N-b** corrected first, because §4 currently contradicts itself in the paragraph that defines what may travel, and a ratification should not be recorded against a self-contradicting text. N-c through N-h are optional.

This report grants no host, freeze, allocation, execution, dispatch, or Git authority, and modified nothing.

---

**Recommended next steps**

1. **Default path** — send N-a and N-b to the implementer as a documentation-only correction (no code change, no new round of the T0 cap), then put §4 and the `always` rule to the Lead for ratification.
2. Compare this report against the Codex flagship slot's; both slots audited identical bytes at `78173bfd`, so any divergence in verdict is itself a finding worth resolving before freeze.
3. If both slots converge on PASS-family, the remaining blockers to freeze are the five freeze-gate inputs (`EXPECT_PARENT_MOUNT` via owner grant #6 ordered before op 01, the two `known_hosts` files + digests, the credential digest, and the Stage-1 digest of `remote_close_tree_wpi.sh`) — all owner-gated, none of them mine to spend.
4. Optional cleanup: N-g (compose the runner's marker array) is a one-line change I would fold into whatever touches the runner next.

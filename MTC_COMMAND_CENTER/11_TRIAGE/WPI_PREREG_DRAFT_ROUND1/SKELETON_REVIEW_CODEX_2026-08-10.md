# NEEDS-WORK: 13 items

## Gap 1 — the freeze-input ledger is incomplete and the P0 attestation inputs are not wired

The skeleton names the RP7 projection digest and the row-8 identities only by category. It
does not name either trusted-interpreter consumer, the paired wrapper/block copies of the
attestations, either complete tool-pin map, the three OpenSSH configuration digests, or the
derived close-script identity. More seriously, current `run_p0.sh` defines and exports none
of the five `P0_ATTESTED_*` inputs that `RP6-P0.sh` requires, so the current composition must
STOP before a host observation even if the five embedded `P0_FIXED_ATTESTED_*` literals are
filled.

Add this clause:

> **Exhaustive fill manifest.** Stage 1 maintains one per-consumer fill manifest and proves
> every entry is populated before any operation: (a) the same projection-v2 digest in
> `RP7-WPI-RO.sh:WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` and
> `run_ro.sh:WPI_ATTESTED_MOUNTINFO_SHA256`; (b) the same resolved non-symlink system-Python
> leaf in `RP6-P0.sh:P0_FIXED_TRUSTED_PYTHON`,
> `RP7-WPI-RO.sh:WPI_FIXED_TRUSTED_PYTHON`, and the `python3=` entry of both
> `P0_TOOL_PINS` and `WPI_TOOL_PINS`; (c) all five row-8 values in both the embedded
> `P0_FIXED_ATTESTED_{USER_NS,MNT_NS,PID_NS,NET_NS,ROOT_MOUNT_ID}` literals and the
> wrapper-supplied/exported `P0_ATTESTED_{USER_NS,MNT_NS,PID_NS,NET_NS,ROOT_MOUNT_ID}`
> inputs; (d) the exact 12-entry P0 and 10-entry RP7 tool-pin maps; (e)
> `remote_setup_wpi.sh:EXPECT_PARENT_MOUNT`; (f) bytes and SHA-256 for
> `wpi_known_hosts`, bytes and SHA-256 for `wpi_known_hosts_global`, SHA-256 for
> `gatea_ed25519` without printing its bytes, and bytes and SHA-256 for
> `remote_close_tree_wpi.sh`; and (g) the carried-forward allocation values, plan digest,
> runkit digest, `ssh.exe`/`scp.exe` digests, five distinct stdin-file digests,
> `EXPECT_UID`/`EXPECT_GID`, archive bytes, six archive-member digests, block digests, and
> wrapper digests. Equality across every duplicated consumer is checked, not assumed.

## Gap 2 — the fill procedure merely invites care; it does not prevent a blind replacement

The skeleton contains no mechanical per-constant procedure. A global replacement would
rewrite `transport_runner.ps1`'s literal `$UNFILLED_MARKERS` value and can make a correctly
frozen runner STOP.

Add this clause:

> **Targeted fills only.** The freeze tool accepts an allowlist of exact
> `(file, constant-or-table-field)` edit sites and refuses a file-wide or repository-wide
> marker replacement. It changes consumer assignments and table cells one at a time. After
> filling, it proves byte-for-byte that
> `$UNFILLED_MARKERS = @('<ALLOCATE-AT-DISPATCH>', '<PIN-AT-FREEZE>')` and every other
> marker-comparison guard is unchanged, while separately proving that no allocation or
> freeze marker remains in any consumer value, argv, plan field, archive constant, or hash
> field. Marker literals retained solely inside guards are expected and are not classified
> as unfilled inputs.

## Gap 3 — attestation, preregistration, and commit ordering is circular

Checklist item 2 obtains the pins before checklist item 5 commits the successor, while the
opening says the successor is committed before any invocation. Section 5 says only that
the grant-#6 command runs before the RO stage; it does not put it unambiguously before op
01 or require its exact command set to be committed before that command runs.

Add this clause:

> **Two-commit attestation order.** Grant #6 is a pre-operation input-acquisition action,
> not an operation in `TRANSPORT_PLAN.tsv`. Before grant #6 is invoked, commit a
> pre-attestation record containing its exact root command bytes, target and execution
> domain, permitted read-only opens, output grammar, capture path, failure/STOP rules, and
> output-hash procedure. Invoke that committed command set once in the grant-#3 root
> session; preserve and hash its output; then fill each named consumer separately, complete
> the successor, and commit the final successor plus its checksum set. No op 01-12, block,
> wrapper, transport process, or host-side allocation may start before that final commit.

## Gap 4 — section 10.2 still describes a per-block proof that cannot close the real composition

The Lead's reproducible run STOPs at rc 3 where `RUNID`, `EV_STAGE_ID`, and
`rp0_require_safe_component` cross the evidence-allocation boundary. The current analyzer
is also under `REQUEST_CHANGES`; its output is a lower bound, not acceptance evidence.

Add this clause:

> **Composite path-scope proof.** The Stage-1 proof unit is each complete frozen same-shell
> composition: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and
> `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`, with the concrete allocation
> and freeze manifest applied. A block-only result is supplemental. The accepted analyzer
> must follow sourced values and registered function contracts; derive `RUNID`,
> `EV_STAGE_ID`, `EV_DIR`, and `EV_LOG` from the exact frozen `REMOTE_BASE`; enumerate every
> reachable path-bearing argument, redirection, test, executable object, and endpoint; and
> reduce the result to a finite closed set. Any unresolved or dynamic construction is
> freeze STOP. The current prover's lower-bound output cannot satisfy this gate until its
> T1 review accepts the repaired analyzer and the exact composite RED/GREEN commands are
> recorded.

## Gap 5 — the skeleton has no place for the 11 required section-10.1 extensions

Add this clause and its rules:

> **Section-10.1 delta.** Add exactly these 11 bounded families, with the final Python leaf
> and MainPID literal reduced to exact values at freeze: (1) `/`; (2) `/opt`,
> `/opt/mtc-bridge`, `/opt/mtc-bridge/releases`, and `/opt/mtc-bridge/venvs`; (3) `/usr`
> and `/usr/bin`; (4) the exact frozen tool objects; (5) `/etc`; (6) `/var`, `/var/lib`,
> and `/var/log`; (7) `/proc/uptime`; (8) `/proc/self/mountinfo`; (9)
> `/proc/self/ns/{user,mnt,pid,net}`; (10) the exact
> `/proc/<WPI_MAINPID>/ns/net`; and (11) `/proc/self/fd/8`. Each rule carries the narrow
> justification recorded in `SEC101_RECONCILIATION_CODEX_2026-08-10.md`; no wildcard or
> arbitrary-prefix substitute is permitted.

## Gap 6 — one access qualifier per row is ambiguous for mixed-access paths

The proposed six-token grammar does not say whether `write-tree` includes readback, whether
an execute right implies a read right, or how the venv subtree can be read while only one
exact leaf is executed. One unexplained qualifier per path row is therefore insufficient.

Add this clause:

> **Access-capability grammar.** Access is default-deny and each qualifier grants only its
> named primitive: `read-exact`, `read-tree`, `read-terminal`,
> `read-execute-exact`, `write-tree`, or `connect`. Multiple rules may name the same exact
> object or subtree when different primitives are required; their capabilities combine
> only for the same resolved operand and never widen the path shape. The venv retains a
> `read-tree` rule and gains a separate `read-execute-exact` rule for the exact
> `<WPI_VENV_ROOT>/bin/python`; frozen tools use `read-execute-exact`; terminal metadata
> directories grant no descendant access. `<REMOTE_BASE>/**` is the only writable family
> and must carry both its required read and write capabilities explicitly; `write-tree`
> does not silently imply read. `127.0.0.1:8790` is the only `connect` rule. A path match
> with the wrong primitive is a freeze failure.

## Gap 7 — three reconciliation findings require source changes before final T0 acceptance

The skeleton schedules flagship acceptance before the path-scope gate even though the
reconciliation requires block changes. Any such byte change invalidates the preceding
acceptance.

Add this clause:

> **Pre-acceptance path repairs.** Before the final T0 pair reviews the artifacts:
> (1) remove every RP6/RP7 write-open of `/dev/null` rather than allowlisting it;
> (2) make `P0_TOOL_PINS` mandatory and exact for
> `stat readlink env find sha256sum systemctl ss curl timeout python3 id getent`, with no
> PATH fallback and with the shared paths equal to RP7's pins; and (3) require
> `P0_VENV_ROOT` to equal `/opt/mtc-bridge/venvs/$P0_CAND`, not merely to end in the
> candidate SHA. The composite proof must also enumerate wrapper/support-layer
> `/dev/null` opens: every write-open outside the evidence tree is removed, and any
> remaining read-open is either separately justified and access-qualified or removed.
> Apply these changes first, rerun their falsifications, then obtain acceptance on the
> final bytes; an acceptance of pre-repair bytes does not count.

## Gap 8 — no current executable implements section 8.2 rows 1-9

Current `RP6-P0.sh` explicitly says every section-8.2 row is out of scope and establishes
no RO host-state result. Current `RP7-WPI-RO.sh` executes and claims only rows 10-23. No
current function checks active state, restart count/policy, MainPID equality, candidate
binding, fragment `[Install]` absence/identity, sandbox properties, or start mode.

Add this clause:

> **Rows 1-9 coverage gate.** Operations 04 and 05 currently do not execute section-8.2
> rows 1-9. Freeze is blocked until an accepted frozen block and plan operation implement
> those nine rows in the preregistered first-divergence order, or the successor explicitly
> removes/defers them under an owner-approved scope change and narrows every claim and
> closure criterion accordingly. P0's Manager.Version readiness query is a premise only;
> it is not evidence for any B2/B4 row.

## Gap 9 — RP6 contradicts the draft's probe-execution-environment guarantee

The draft says every evidence-producing child uses a fixed trusted cwd, cleared
environment, and run-owned TMPDIR. Current RP6 instead records inherited environment for
`stat`, `readlink`, `id`, and `getent`, caller-inherited cwd, and inherited-or-unset TMPDIR,
and its terminal claim says the round-1.4 environment binding is not established.

Add this clause:

> **P0 environment reconciliation.** The successor may not carry the blanket
> probe-execution-environment rule while RP6 explicitly disclaims it. Before freeze, either
> repair RP6 so every evidence-producing child satisfies the preregistered cleared-env,
> fixed-cwd, run-owned-TMPDIR and pinned-target-chain contract and re-audit the changed
> bytes, or narrow the successor to the exact mixed environment RP6 proves and obtain
> explicit acceptance of that weaker claim. Silence or inheritance of the old paragraph
> is not reconciliation.

## Gap 10 — the skeleton's transport summary is stale

The skeleton says "round-2 repaired" and "first-FAIL". The current runner and draft use a
per-kind observed-outcome grammar and first-*mismatch* sequencing; transport failures and
cleanup consequences are not host FAILs.

Replace the section-6 sentence with:

> The successor reproduces the exact current `TRANSPORT_PLAN.tsv` ops 01-12 and the
> current runner's first-mismatch semantics: after the first mismatching or not-evaluable
> `sequence_ok` operation, later `sequence_ok` operations are skipped and all `always`
> operations still run; results are classified by operation kind and provenance, not by rc
> alone; ssh rc 255, every nonzero scp rc, an rc outside a kind's grammar, or an ssh rc
> without a remote-program marker is not-evaluable; and an `always` failure caused by an
> earlier broken sequence is not-evaluable rather than a new host FAIL. Ops 07/08 close via
> `remote_close_tree_wpi.sh`, ops 09/10 retrieve, ops 11/12 bind locally, and op 06 is the
> operator-side row-24 host contact.

## Gap 11 — the derived close-script preregistration does not match the current bytes

The draft says `remote_close_tree_wpi.sh` has derivation classes 5 and 6, a cleared launch
domain, and a run-owned `WORK_ROOT`. The current script accepts only `<EV_DIR> <RUNID>`,
explicitly inherits login `TMPDIR`, and states that class 2 is its only semantic delta; the
current plan likewise passes only two arguments. The report and the bytes cannot both be
the execution contract.

Add this clause:

> **Close-script contract gate.** Freeze is blocked until the actual
> `remote_close_tree_wpi.sh`, its plan argv, the derivation contract, and the RED/GREEN
> evidence describe the same launch domain and scratch-location semantics. If classes 5
> and 6 remain preregistered, the accepted script must implement them and the plan must pass
> the required run-owned work root; if the two-argument inherited-TMPDIR bytes remain, the
> successor must not claim those classes and must surface that weaker contract for T0
> adjudication. Hash agreement with a report whose prose describes different behavior is
> not closure evidence.

## Gap 12 — `WPI_INTERPRETER_TARGET` is a stale, unused freeze pin

`run_ro.sh` marks and exports `WPI_INTERPRETER_TARGET`, but current `RP7-WPI-RO.sh` never
reads it and deliberately refuses a symlinked venv interpreter instead of accepting a
target chain.

Add this clause:

> **No inert pins.** Remove `WPI_INTERPRETER_TARGET` from the wrapper and successor fill
> ledger unless an accepted block gives it an explicit predicate and consumer. A filled
> but unread value is not a preregistered check. Row 18 continues to require the exact
> `<WPI_VENV_ROOT>/bin/python` object to be a non-symlink regular executable unless the
> row itself is explicitly redesigned and re-audited.

## Gap 13 — the skeleton contains unresolved-status residue

Section 2 still says "see §5 OPEN DECISION" although section 5 says the decision is
resolved, and section 5 contains the stray standalone text `Gr`.

Replace those fragments with:

> `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`, both trusted-Python pins, the five row-8
> execution-domain identities, and `EXPECT_PARENT_MOUNT` are produced only by the committed
> grant-#6 attestation procedure described in section 5.

Delete the standalone `Gr` line and all three obsolete option branches; retain only the
owner-selected option-(a) contract and its exact ordering.

## Already correct — do not touch

- `WPI-<UTCSTAMP>Z-<8hex>`, once concretely filled, and its `-P0` / `-RO` RUNIDs are
  accepted by `rp0_require_safe_component`: they are nonempty, do not begin with `-`, and
  use only `[A-Za-z0-9._-]`. `p0` and `ro` are also accepted stage components.
- The refusal demonstration is specific, not gestural: the exact seven values
  `../escaped`, `a/b`, `.`, `..`, `-lead`, empty, and `bad name` are listed with expected
  rc 1, while every concrete allocated component must show rc 0 and the transcript must be
  preserved. Keep the burn-on-failed-allocation and no-retry rule.
- Keep the create-once remote and operator record roots and the collision checks against
  both recorded operator roots.
- Keep the final runkit member set exactly `RP0-LIB.sh`, `RP0-BOOTSTRAP.sh`, `RP6-P0.sh`,
  `RP7-WPI-RO.sh`, `run_p0.sh`, and `run_ro.sh`; keep `RP1-B3.sh` excluded.
- Keep the requirement that all three final artifact sets receive both flagship T0
  acceptances, subject to Gap 7's correction that acceptance must be on the post-repair
  bytes.
- Keep separate close invocations 07/08, retrieval 09/10, local-only binding 11/12, and
  the operator-side row-24 probe at op 06.
- Keep the owner-selected grant-#6 option (a), external-to-login-domain attestation, and
  the rule that the login session may never learn and re-pin its own namespace or mount
  identity.
- Keep the post-run evidence retrieval, digest-set binding, WP-I closure record, Audit 2
  dispatch, and later grant-#3 `RPD-VERIFY` sequence.

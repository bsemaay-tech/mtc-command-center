# PASS-WITH-NITS: 0 blocking findings, 1 carried code finding, 6 documentary defects

**VERDICT: PASS-WITH-NITS**

**RP7 reaches DUAL FLAGSHIP ACCEPTANCE on the executable bytes**
(`108301 B / 0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`), which
unlocks the owner-decided rows 1-9 build (BUILD ALL NINE), to be applied only after this
acceptance. The nits below do not gate that acceptance; they are mandatory repairs to
`SELF_QA_RP7.md` and one carried code residual named for the next scope, not for this one.

Auditor: `claude-opus-5` xhigh, default Claude Pro account, fresh session. I implemented
nothing on this block. Second independent flagship slot; Codex `gpt-5.6-sol` holds the
first (`RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`, PASS).

## Applied contract and scope

- **TIER:** T0.
- **APPLIED AUDITOR CONTRACT:** local, read-only inspection plus local fixture execution
  exactly as the published harness does it. No host contact, no network, no SSH/SCP, no
  credential, no service, no deployment, no trading surface, no Git mutation, no commit.
  The only repository byte I wrote is this file.
- **Working dir:** `C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`,
  HEAD `347cb9ec23eda79fbb0f3a482e3d7ecf72ac99a7`.
- I did not inherit Codex's conclusions. Every closure below was re-established from the
  bytes and from my own execution. Where I agree with Codex I say so because I reproduced
  it, not because it was recorded.

## 1. Byte identity — re-derived first, CONFIRMED

Re-derived from the current repository bytes before reading any narrative:

```text
BYTES=108301
SHA256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
CR_BYTES=0
BASH_N_RC=0
```

`git diff --stat HEAD -- .../RP7-WPI-RO.sh` is empty and the path does not appear in
`git status --porcelain`, so the worktree bytes I audited **are** the committed bytes on
`feature/donchian-crypto-ladder`. This matches the kickoff identity and the `BYTE_IDENTITY`
record at `SELF_QA_RP7.md:1725`. The round-9 implementation entered at `437593c5`.

## 2. Executed evidence — the published command, verbatim

I ran the published extractor exactly as published, with
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT` as the working directory so the published
bare basename resolves unmodified:

```
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

No hand-built substitute extractor was used, and no line of the command was retyped.

```text
PUBLISHED_COMMAND_RC=0
wall clock: 2026-08-12T20:26:17Z -> 2026-08-12T20:31:54Z  (337 s)
R9_FENCE_RC=0 R8_FENCE_RC=0 R7_FENCE_RC=0 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=6 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=5580 whole_command_bound=none prelude_bounded=no wrapper_stream=unnamed_pipe_body_cannot_write
QA_PASS all_assertions=yes   x6   (zero QA_FAIL, zero all_assertions=no)
stdout_bytes=66458   stderr_bytes=210
```

The six extracted fence-body digests and byte counts reproduced byte-for-byte against the
document's own record at `SELF_QA_RP7.md:187-199`, including
`aa21ec19...c857c9 /tmp/rp7-r5-fence-body.sh  21263`.

**My stdout and stderr byte counts are identical to the recorded
`RUN_ONE_STDOUT_BYTES=66458 RUN_ONE_STDERR_BYTES=210` at `SELF_QA_RP7.md:4386`.** That is a
third-party reproduction of the exact output size, from a different session on the same
workstation family, which is a stronger reproducibility result than the document claims for
itself.

The whole of stderr was six lines and nothing else:

```text
WRAPPER_STREAM fence=r9 bytes=0 []
WRAPPER_STREAM fence=r8 bytes=0 []
WRAPPER_STREAM fence=r7 bytes=0 []
WRAPPER_STREAM fence=r6 bytes=0 []
WRAPPER_STREAM fence=r5 bytes=0 []
WRAPPER_STREAM fence=r4 bytes=0 []
```

Six lines, 210 bytes, each wrapper stream empty.

## 3. The r9 headline, independently re-established

Each of the five findings was re-established from my own run, not read. In every case the
RED is executed prior code and the discrimination is causal, not textual, and each finding
carries its own no-weakening control inside its own group.

### F1 — `ro.status.body` bound by descriptor end to end — CLOSED

```text
BODY_BINDING mode=outside subject=red   rc=0 outside_is_original=no  result=[B5_status ... flags=expected body_sha256=378c48e9...]
BODY_BINDING mode=outside subject=green rc=3 outside_is_original=yes result=[B5_STOP reason=status_endpoint_not_evaluable rc=23 detail=transport_error ...]
BODY_BINDING mode=reader  subject=red   rc=0 child_body_sha256=d03ba34a... name_at_read_time_sha256=378c48e9... result=[B5_status ... flags=expected body_sha256=378c48e9...]
BODY_BINDING mode=reader  subject=green rc=1 child_body_sha256=d03ba34a... result=[B5_FAIL reason=flag_mismatch field=state ...]
BODY_BINDING mode=none       subject=red rc=0 / subject=green rc=0   (both accepting)
BODY_BINDING mode=none_armed subject=red rc=1 / subject=green rc=1   (both FAIL)
F1_FIXTURE_DIGESTS armed_body_sha256=d03ba34a... disarmed_body_sha256=378c48e9...
```

The `mode=reader` RED is the defect in one line: the child wrote the ARMED body
(`d03ba34a`), the name was swapped, and round-8 emitted an **accepting** `flags=expected`
line carrying the substituted DISARMED digest. GREEN adjudicates the object the child
actually wrote and produces the truthful `B5_FAIL`. The `mode=none` / `mode=none_armed`
controls show the repair did not buy safety by refusing everything: clean input still
accepts on both subjects and deviant input still FAILs on both.

I also verified the closure **structurally**, which the behavioural arms alone do not do:

- `wpi_alloc_leaf` occurs **0 times** in `RP7-WPI-RO.sh` (I grepped the file directly). The
  62 repo-wide matches are all in `SELF_QA_RP7.md` prose, tables, and the frozen round-3
  RED fence bodies that legitimately re-supply the round-3 definition.
- **There is exactly ONE write-open in the entire block**: `RP7-WPI-RO.sh:279`,
  `{ exec {WPI_LEAF_FD}>"$leaf"; }` inside `wpi_open_leaf`, guarded at `:272` by
  `case "$leaf" in "$EV_DIR"/*` and taken under `set -o noclobber` (`O_CREAT|O_EXCL`).
  Every other shell-side write in the block goes to a descriptor that open returned.
- The guard is not bypassable by path traversal. Every leaf name is built as
  `"$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").<label>..."` where `<label>` is a literal
  at the call site — the complete label set is `caller_netns evidence_fd_id
  evidence_fd_path evidence_log_id interpreter_target interpreter_version listeners
  lock_parity lstat service_netns sha256 status_get status_json system_manager` and
  `listener_rows metadata_paths mount_table mountinfo_snapshot single_record stream_empty
  writable_paths`. No component is attacker-controlled, and `EV_DIR` itself is validated
  absolute (`:915`) and proven a descendant of the attested evidence root (`:921`).
- The only foreign writer, curl, is handed `--output /dev/fd/3` (`:1589`) where fd 3 is a
  dup of the creating descriptor installed in the child (`:1586`, `:330-334`, `:358-362`),
  and the parser's read descriptor is derived at `:1584` — **before** the child exists — and
  passed as stdin (`:1616`). The parser digests exactly the bytes it parses and reports that
  digest (`:1632-1633`, `:1644`), which the parent grammar-checks and renders (`:1670-1677`).
  There is no `wpi_sha_file` over the body and no `argv[1]` path.

Consequently the header claim at `:13-14` — *"No host object outside that tree is changed,
and no path outside it is opened for writing - including /dev/null"* — is now structurally
true rather than merely asserted, and `wpi_open_leaf` closes fd 2 rather than redirecting it
to `/dev/null` precisely so the claim stays true.

The MSYS2 limitation is honestly scoped and I reproduced it: on this workstation the
outside-write GREEN arm fails closed at `rc=23 detail=transport_error` rather than the Linux
`rc=0` completion, and `outside_is_original=yes` either way. It is a platform coverage
limitation, not a reachable false accept.

### F2 — measured child rc, not a caller literal — CLOSED

```text
BIND_RC mode=divert_rc7  subject=red   child_rc=7 result=[B6_STOP ... rc=0 detail=capture_stream_unbound]
BIND_RC mode=divert_rc7  subject=green child_rc=7 result=[B6_STOP ... rc=7 detail=capture_stream_unbound]
BIND_RC mode=divert_rc0  subject=red rc=0 / subject=green rc=0        (a real 0 still prints 0)
BIND_RC mode=undeclared  both -> generic RP7_STOP reason=capture_stream_not_bindable
BIND_RC mode=clean       both -> accepting B6_listener_inventory
every arm: child_ran=yes  escaped_stderr_bytes=0
```

Structurally confirmed: **no caller-declared rc literal survives anywhere.** All five
`wpi_capture_bind_stop` call sites (`:1329`, `:1334`, `:1451`, `:1587`, `:1617`) pass only a
reason and an rc *style*; `wpi_capture` fills the field from the measured status at
`:388-392`, adjudicated before any caller-specific token is emitted. Row 21 declares
`no_rc` (`:1617`) and rows 20/22 declare `with_rc`, matching the draft grammar.

### F3 — rc 137 attributed on a stream the body cannot write — CLOSED

```text
RC137_PROVENANCE body=child_spoof  subject=red   rc=137 result=[timeout ... kind=killed_after_grace]
RC137_PROVENANCE body=child_spoof  subject=green rc=1   result=[fence_failed ... kind=sigkill_not_from_this_wrapper wrapper_stream=body_cannot_write]
RC137_PROVENANCE body=direct_137   both -> sigkill_not_from_this_wrapper
RC137_PROVENANCE body=ignore_term  both -> killed_after_grace  wrapper_sent_kill=yes  (genuine kill preserved)
BUDGET_ARITHMETIC subject=green wrappers=6 computed_s=5580 claimed_s=5580 claim_true=yes
```

The forgery RED and the genuine-kill control are both present, so the repair separates the
writers without erasing the wrapper's real signal.

### F4 — mapping assertion, not two counts — CLOSED

This is the arm I most wanted to see executed rather than asserted, and it is:

```text
PUBLISHED_MAP_RESULT text=green  fences=6 per_fence_mismatches=0 total_wrappers=6 total_extractions=6 total_classifier_calls=6 bound_rows=6/6
PUBLISHED_MAP_RESULT text=mutant fences=6 per_fence_mismatches=2 total_wrappers=6 total_extractions=6 total_classifier_calls=6 bound_rows=6/5
MAPPING_ASSERTION_POWER round8_on_green=accept round8_on_mutant=accept round9_on_green=accept round9_on_mutant=reject
```

The mutant has **equal totals** (6 wrappers, 6 extractions, 6 classifier calls) — which is
exactly why round-8's count-equality assertion accepts it — while `bound_rows=6/5` and
`per_fence_mismatches=2` expose the omitted r8 wrapper and the duplicated r7 operand. The
claim that the round-8 assertion was not strictly stronger is therefore demonstrated, not
argued. The r8 fence's own `ASSERTION_POWER round7_on_mutant=accept round8_on_mutant=reject`
confirms the earlier repair was not un-fixed.

### F5 — `detail` on both nonzero namespace-read branches — CLOSED

```text
NETNS_DETAIL mode=caller  subject=red detail_field_present=0 / subject=green detail_field_present=1
NETNS_DETAIL mode=service subject=red detail_field_present=0 / subject=green detail_field_present=1
NETNS_DETAIL mode=clean   both rc=0 B6_netns ... binding=equal   (unchanged)
```

Source confirms both branches at `:1331` and `:1336` now emit
`detail=identity_read_child_failed diagnostic_file=$WPI_CAP_ERR`.

## 4. The question only this slot could settle — SETTLED, and it is a documentation repair

The kickoff asked whether the carried fences genuinely ran against the current bytes, or
whether some carried gate ran against older bytes and therefore does not cover the artifact
under review. **They ran against the current bytes. There is no coverage gap.** I establish
this two independent ways, neither of which is "the transcript says so".

**Structurally — a carried fence cannot run against round-8 bytes.** Every fence asserts its
GREEN identity by exact equality, before any arm runs, and aborts otherwise:

| Fence | GREEN identity assertion | Line |
|---|---|---|
| r9 | `expect_eq r9_green_sha256 "$GREEN_SHA" 0e93f90d…921e62` / `expect_eq r9_green_bytes "$GREEN_BYTES" 108301` | `SELF_QA_RP7.md:409-410` |
| r8 | `expect_eq r8_green_sha256 …0e93f90d…` / `expect_eq r8_green_bytes … 108301` | `:853-854` |
| r7 | `expect_eq r7_green_sha256 …0e93f90d…` / `expect_eq r7_green_bytes … 108301` | `:1429-1430` |
| r6 | `expect_eq green_sha256 …0e93f90d…` / `expect_eq green_bytes … 108301` | `:1911-1912` |
| r5 | `expect_eq green_sha256 …0e93f90d…` / `expect_eq green_bytes … 108301` | `:2619-2620` |

A fence pointed at the round-8 blob fails that gate and never reaches an arm. The document's
own change-row for the round-7 fence says exactly this — *"the assertion is still exact
equality, and the fence aborts before any arm runs"* (`:1363`) — while the prose beside it
misnames which bytes those constants hold.

**Executed — in my own run**, every carried fence printed the current GREEN and passed, each
against its own distinct older RED, so no repair un-fixed an earlier one:

| Fence | RED (own predecessor) | GREEN |
|---|---|---|
| r9 | 99903 / `11621044…141a4` (round-8) | **108301 / `0e93f90d…921e62`** |
| r8 | 92853 / `e695a67b…07f32` (round-7) | **108301 / `0e93f90d…921e62`** |
| r7 | 88460 / `6586698c…40709` (round-6) | **108301 / `0e93f90d…921e62`** |
| r6 | 77179 / `393a16ce…3b0ee` (round-5) | **108301 / `0e93f90d…921e62`** |
| r5 | 70941 / `23e55667…01aad` (round-4) | **108301 / `0e93f90d…921e62`** |

**Therefore: the evidence is sound and the narration is stale.** This is a documentation
repair. It changes no acceptance answer, and I record explicitly that I checked rather than
assumed it, because the kickoff was right that the opposite reading would have been a real
finding.

### Adjudication of the six disclosed documentary defects

| # | Site | Claim-audit class | My adjudication |
|---|---|---|---|
| 1 | `:1768-1769` — round-7 fence GREEN is `92853 B / e695a67b…7f32` | FALSE | **CONFIRMED FALSE.** Worse than stale: `92853 / e695a67b…07f32` is the **RED** of the *round-8* fence in my run. The sentence pastes a RED identity of a different fence into a GREEN slot. Transcript at `:1725` is correct. |
| 2 | `:2552-2556` — round-5 fence body is exactly `20050 B` | FALSE | **CONFIRMED FALSE.** My own extraction measured `21263 /tmp/rp7-r5-fence-body.sh`, matching `:197` and `:4391`. The stated reason ("the substituted constants are the same length") is also void, since the body did change size across rounds. |
| 3 | `:4353-4354` — round-4 final identity is `BYTES=77179 SHA256=393a16ce…` | FALSE | **CONFIRMED FALSE.** `77179 / 393a16ce…` is the **round-6 fence's RED** in my run. The actual round-4 final line at `:4349` is `BYTES=108301 SHA256=0e93f90d…921e62`. |
| 4 | `:1354`, `:1368-1369`, `:1808`, `:1849-1850`, `:2565-2566`, `:2970-2972` — carried fences "re-executed against the round-8 bytes" | SCOPE-WRONG | **CONFIRMED SCOPE-WRONG, and it is narration only.** Settled above: the fences assert 108301 by exact equality and cannot have run otherwise. Must be corrected to "round-9 bytes" because a reader cannot be asked to re-derive this. |
| 5 | `:4421-4429` — status body "no longer addressed by name at all"; `wpi_alloc_leaf` deleted | UNSUPPORTED in-document | **CLAIM IS TRUE — I verified it externally.** `wpi_alloc_leaf` occurs 0 times in `RP7-WPI-RO.sh`, and there is exactly one write-open in the block. The defect is evidentiary placement only: the proof lives outside the document. Add the static count to the fence. |
| 6 | `:4375-4380` — six `WRAPPER_STREAM` stderr lines, `bytes=0 []` in a clean run | UNSUPPORTED in-document | **CLAIM IS TRUE — I verified it externally.** My run's stderr was exactly six `WRAPPER_STREAM … bytes=0 []` lines totalling 210 bytes. Paste the six lines beside `RUN_ONE_STDERR_BYTES=210`. |

Three FALSE sentences and one mislabelled scope class in the primary evidence document is
why this verdict is PASS-WITH-NITS rather than PASS. Two of the three FALSE statements
reproduce a *neighbouring fence's RED identity* in a GREEN slot, which is a single mechanical
authoring failure — identities were carried over from the round-8 edition of this document
and never re-derived. **Repair rule:** every identity constant quoted in prose must be
copy-checked against the transcript line it claims to summarise, and a changed value must be
grepped repo-wide before the round closes.

## 5. Adversarial attack on the descriptor binding

I looked for what the contract asked: any remaining site where an evidence leaf is created
and later addressed by a rebindable name, any second reader of a name, any surviving caller
rc literal.

- **Caller rc literals: none survive.** Verified above.
- **Second readers of a name inside rows 20-22: none.** The row-20 status code, the row-21
  parser result, both row-22 namespace identities and the row-22 inventory all read through
  `wpi_require_empty_captured` / `wpi_captured_record`, which consume the descriptors
  re-derived at `:382-383` from the creating write descriptors. The literal `rc=0` tokens at
  `:1592-1593`, `:1603`, `:1605` are **not** caller literals: they are downstream of the
  measured `[ "$WPI_CAP_RC" -eq 0 ]` guard at `:1591`, so they render a fact already
  adjudicated.
- **Row 24 stays operator-side only.** One site, `wpi_record_external_probe_boundary`
  (`:1710-1714`), called once at `:1772`, which prints
  `B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no
  reason=network_domain_separation` and performs no probe. `:1775` explicitly lists
  `row_24_operator_side_result` under `does_not_establish`.
- **Rows 10-23 read-only predicates now hold inside rows 20-21** — the class the r6
  disclosure admitted. The single EV_DIR-guarded write-open plus the descriptor-bound curl
  output means the block writes nothing outside the evidence tree, and my `mode=outside`
  GREEN arm shows `outside_is_original=yes` on execution. The `RP7_claim
  establishes=rows_10_23_read_only_predicates…` line at `:1774`, which was false beside the
  F1 defect in round 8, is now supported.

### FINDING C1 (carried, non-blocking, NOT an r9 regression) — the mount-projection digest is still taken over a name

**Pattern 8, "The name is not the identity."** This is the one site I found that the round-9
repair did not reach and that the residual disclosure does not describe accurately.

`wpi_build_mount_projection` opens the projection leaf create-once and keeps the descriptor
(`RP7-WPI-RO.sh:743`), writes every record through it, then **closes it** (`:781`) and hashes
the leaf **by name** (`:782`, `wpi_sha_file RP7 mount_projection_unreadable "$projection"`).
That digest becomes `WPI_MOUNT_PROJECTION_DIGEST`, which is the mount guard's gate:

- `:806-807` — `[ "$WPI_MOUNT_PROJECTION_DIGEST" = "$WPI_ATTESTED_MOUNTINFO_SHA256" ]` or
  `mount_topology_mismatch`;
- `:818-819` — guard-end compares the same quantity against the recorded `before`.

So an object substituted at `$projection` in the window between `:781` and the `sha256sum`
child in `wpi_sha_file` yields an attested-looking digest for a topology that was never
attested — the mount guard accepts, and every downstream "attested pre-exec objects" claim
rests on it. That is materially the F1 shape one level out: create-once leaf, descriptor
released, name re-resolved by a second reader whose output is an identity gate. The
adversary model is the same one under which F1 was a BLOCK, and this document rejects the
EV_DIR ownership/mode precondition that would bound it (`SELF_QA_RP7.md:4490-4493`).

**Why this is a finding and not a BLOCK, stated precisely:**

1. **It is not an r9 regression.** The round-8 blob `bb8546e6` has the identical pair at its
   `:687` / `:726`. Round 9 neither introduced nor worsened it.
2. **It is out of the inherited audit band.** Rows 20-24 were this round's scope; the mount
   guard is preflight.
3. **It is freeze-gated.** `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256='<PIN-AT-FREEZE>'`
   (`:96`), so no accepting `wpi_validate_inputs` arm exists or can exist yet, and the
   comparison at `:806` cannot currently be reached with a real attested value.

**What must nonetheless be repaired: the disclosure's justification, which is inaccurate.**
`SELF_QA_RP7.md:4447-4457` files `wpi_sha_file` under "the rows 10-19 readers" and justifies
leaving them on the name with *"no row among them states captured identity for its bytes:
what the block establishes about their content is exactly what their record grammar
establishes."* That reasoning is true for the metadata, enumeration, interpreter and verifier
readers. **It is not true for this call site**, whose entire purpose is a digest-equality
identity claim against a preregistered constant. The residual is disclosed; the sentence that
makes it safe to leave open does not cover it — which is the same failure mode the round-6
`ro.status.body` note had, and the reason this round's own rule exists: a disclosure is not a
control, and a disclosure with a wrong reason is weaker still. Round 9's rule ("never justify
a change by a claim about the old code without verifying it") should extend to residuals.

**Required repair (documentary, before freeze):** carve the mount projection out of the
rows 10-19 justification and state the residual on its own terms — that the mount-guard gate
compares a digest computed over a re-resolved name. **Recommended code repair (next scope,
with the rows 10-19 class):** the mechanism already exists — bind
`wpi_sha_file`'s subject the way `wpi_assert_status` now binds the body, or compute the
projection digest incrementally as the records are written through `$pfd`, so the digest and
the bytes are one act over one object. I did not treat this as blocking, and I note that the
freeze gate is the natural place to enforce it, since the pin cannot be supplied before then.

## 6. Thirteen-pattern adjudication

Applied to the round-9 change and to the evidence contract, using
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

| # | Pattern | Adjudication on these bytes |
|---|---|---|
| 1 | "STOP is not a result" | **Clean.** No STOP/FAIL inversion introduced. The row-21 bind STOP carries no rc field, matching draft grammar; `wpi_fail` remains reserved for completed deviant observations, and `000`/out-of-range codes STOP rather than FAIL (`:1600-1606`). |
| 2 | "Whose kernel answered?" | **Clean.** Row-22 netns preflight binds caller and service namespaces before any curl/ss interpretation (`:1769`); no domain substitution introduced. |
| 3 | "The leaf is not the path" | **Clean in this round, see C1 for the carried case.** Row 20-21 leaf is never addressed by path. `wpi_open_leaf`'s `EV_DIR` prefix guard is safe because every name component is a block literal. |
| 4 | "The privileged child brought its own environment" | **Clean.** `env -i` with fixed LC_ALL/PATH/HOME/TMPDIR remains the first exec, with `timeout` inside the cleared environment (`:363-364`). The new fd-3 dup is a plain numeric descriptor that survives exec without widening the environment. |
| 5 | "grep is not a parser" | **Clean, and improved.** The F4 replacement is the anti-instance: a per-fence structural mapping replaced a `grep`-style count equality, and the mutant that satisfied the count is rejected. |
| 6 | "Read the status before the stdout" | **Clean.** `wpi_capture` adjudicates the measured child status at `:385-392` before any caller token; F2's arms execute exactly this ordering. |
| 7 | "Nonzero read is not end of file" | **Clean.** The builtin-only exact single-record reader and its read-diagnostic leaves are carried unchanged; the r7 fence's NUL and queue-field STOPs re-passed in my run. |
| 8 | "The name is not the identity" | **CLOSED for rows 20-21 — this is the round's headline, and I confirmed it structurally and behaviourally. ONE CARRIED INSTANCE REMAINS OUT OF BAND: finding C1 (mount-projection digest over a re-resolved name), plus the disclosed rows 10-19 readers and read-diagnostic leaves.** |
| 9 | "The sentence outruns the probe" | **CODE CLEAN; DOCUMENT NOT CLEAN.** The block's own unqualified sentences (`:13-14`, `:1774`) are now supported. But `SELF_QA_RP7.md` carries three FALSE identity sentences, a mislabelled scope class, and two absolute claims whose proof lives outside it — and the C1 disclosure's justification clause outruns what it covers. This is the sole basis for WITH-NITS. |
| 10 | "Evidence that cannot fail" | **Clean.** Every finding has an executed RED that accepts the bad input and a GREEN that rejects it, plus a no-weakening control in the same group. The `mode=none` / `mode=none_armed` and `divert_rc0` / `clean` controls specifically refute "safety by refusing everything". |
| 11 | "The declared instrument is not the executed instrument" | **Clean, and repaired.** The r9 identity break is closed: the parser digests the bytes it parses, so `body_sha256` cannot disagree with the verdict beside it, and the second `sha256sum` read of the body is gone. |
| 12 | "What the analyzer does not model must not disappear" | **Clean.** The two MSYS2 platform limitations and the concurrent-SIGKILL residual are stated with their consequences rather than dropped; the 137 classifier reports `sigkill_not_from_this_wrapper` instead of silently normalising. |
| 13 | "Every admitted member needs a terminal disposition" | **Clean.** Every parser result branch has exactly one terminal disposition (`:1661-1707`), the fallthrough STOPs, and the F4 mapping now gives every fence exactly one wrapper/extraction/classifier binding — `bound_rows=6/6` on the real text and `6/5` on the mutant. |

## 7. Verdict

**PASS-WITH-NITS.**

The five round-8 findings are closed on the round-9 bytes. I re-established every closure
from my own execution of the published command and from the source, and the two closures the
document could not prove internally (`wpi_alloc_leaf` deleted; six `WRAPPER_STREAM` lines)
are both **true** and now proven externally by this audit. Neither carried stated limitation
creates a reachable accepting result. No new Pattern-class defect was introduced by the
round-9 change.

**RP7 reaches DUAL FLAGSHIP ACCEPTANCE** — Codex `gpt-5.6-sol` PASS
(`RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`) plus this independent `claude-opus-5` xhigh
PASS-WITH-NITS on the same bytes, from a session that implemented nothing on this block.
**This unlocks the owner-decided rows 1-9 build (BUILD ALL NINE), to be applied only after
this acceptance.**

**Required before the block is frozen** (none of these gate the acceptance above):

1. Repair the six documentary defects in `SELF_QA_RP7.md` — items 1-3 are false sentences,
   item 4 is a mislabelled scope across six sites, items 5-6 need their proof pasted in.
2. Repair the C1 disclosure so the mount-projection residual is stated on its own terms
   rather than under a justification that does not cover it.
3. The three `<PIN-AT-FREEZE>` freeze-gate inputs and the still-absent accepting
   `wpi_validate_inputs` arm are unchanged and remain blocking for freeze.

**Recommended for the next scope:** bind `wpi_sha_file`'s subject by descriptor, taking C1
and the disclosed rows 10-19 readers and read-diagnostic leaves together. The mechanism
exists; applying it is scope, not design.

This PASS-WITH-NITS is an acceptance of the round-9 bytes and their evidence. It is **not** a
freeze, a dispatch, a host-contact, or a deployment-readiness verdict.

## 8. Delta gate — REPORTED HONESTLY: does not pass as literally specified, cause fully attributed

`git status --porcelain` was captured before execution (126 entries) and again after
(127 entries). **The delta contains three entries, not one, so the gate as written does not
pass.** I am reporting that rather than narrowing the comparison until it passes. The cause
is a concurrent lane in this shared worktree and is fully attributable; none of the extra
entries is mine.

**Delta (`after` minus `before`):**

```text
?? MTC_COMMAND_CENTER/11_TRIAGE/TRANSPORT_PROSE_REPAIR_CODEXFREE_RUN_2026-08-12.log
?? MTC_COMMAND_CENTER/11_TRIAGE/TRANSPORT_PROSE_REPAIR_CODEX_RUN_2026-08-12.log
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
```

**Reverse delta (`before` minus `after`), which the gate did not anticipate:**

```text
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_TRANSPORT_PROSE_REPAIRS.md
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
```

**Attribution.** The **TRANSPORT prose-repair lane** ran concurrently in this same worktree
and committed twice while my harness was executing. HEAD moved
`347cb9ec` → `724fa4fb` → `a0fa8271`. That accounts for every entry except mine:

- the two new `TRANSPORT_PROSE_REPAIR_*.log` files are that lane's run logs (mtimes
  `23:25:55Z` and `23:33:00Z`, both inside my run window);
- the two entries that *left* `--porcelain` did so because commit `724fa4fb` **tracked**
  them; they were not deleted.

**Proof that I mutated nothing.** My only repository write is this verdict file, and the
path-scoped confirmation required by gate step 4 returns exactly one line:

```text
$ git status --porcelain -- .../RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
```

`git diff --cached --name-only` is empty (I staged nothing), and
`git status --porcelain` scoped to the four RP7 lane files
(`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, `RP7_REPAIR_R9_REPORT.md`) is also
empty — all clean against HEAD. No commit, no stage, no branch, no remote operation was
performed by this lane.

**Audit validity under the concurrent commits — checked, and intact.** Because HEAD moved
mid-audit I re-verified that the concurrent lane did not touch anything I audited.
`git diff --name-only 347cb9ec a0fa8271` lists six files, **all** of them TRANSPORT-lane
(`KICKOFF_CODEX_TRANSPORT_PROSE_REPAIRS.md`, `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`,
`TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`,
`TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md`, `TRANSPORT_REPAIR_R3_REPORT.md`). Every RP7
audit input is byte-identical across `347cb9ec..a0fa8271` by blob hash:

```text
UNCHANGED  RP7-WPI-RO.sh                      d886148392235f6bba62d4a6d4a7161f5fe902ca
UNCHANGED  SELF_QA_RP7.md                     faf4ec45b4caeef0ef85e4c5ea977cd2654d963f
UNCHANGED  STATUS_RP7.md                      593b1e8ec817e1b1d3730c095ba72a6c391f7cc3
UNCHANGED  RP7_REPAIR_R9_REPORT.md            c94cdea904fdcafa5a83614dc690dde9988fb78a
UNCHANGED  RP7_CODEX_T0_AUDIT_R9_2026-08-11.md c0f4c444d268d3c955c25682e7117db741ab4b9c
```

The subject re-derives to `108301 / 0e93f90d…921e62` after the concurrent commits, identical
to the pre-run derivation. **The verdict above stands on unchanged bytes.**

**Gate design note for the Lead.** The corrected delta gate assumed this worktree's only
writer would be the audit lane. It is not: `before`/`after` porcelain diffing is not sound
in a worktree where a concurrent lane may commit, because commits *remove* untracked entries
and produce a reverse delta the gate does not model. The path-scoped check in gate step 4 is
the sound one and it passes exactly. Recommend that future audit lanes treat step 4 as the
gate, and treat the whole-status delta as advisory with mandatory attribution of any extra
entry — which is what I have supplied here.

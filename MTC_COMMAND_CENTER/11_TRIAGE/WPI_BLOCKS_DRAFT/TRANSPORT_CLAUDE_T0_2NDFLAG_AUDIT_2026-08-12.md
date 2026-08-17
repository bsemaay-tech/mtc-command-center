# TRANSPORT — Claude `claude-opus-5` xhigh T0 audit, SECOND FLAGSHIP attempt

**Verdict: REQUEST_CHANGES.**
**The second flagship slot is NOT closed. Transport does NOT reach dual flagship
acceptance on this session's work.**

Two independent reasons, and they must not be collapsed into one:

1. **Contract item 1 could not be executed in this session.** The published WSL2
   fixture harness was not run. `wsl.exe` is not on this session's Bash/PowerShell
   permission allowlist and the session is non-interactive, so every invocation form
   — with and without the sandbox override — returned `This command requires
   approval` with no way to grant it. This is an environment limitation of the
   auditing session, **not** a defect in the audited bytes. But a flagship slot whose
   contract mandates driving the harness verbatim and recording real rc/stdout cannot
   be signed on reasoning alone.
2. **Four documentary defects in `SELF_QA_TRANSPORT.md` are confirmed and unrepaired**
   — two FALSE, two UNSUPPORTED — three of them inside the integrity envelope and the
   coverage accounting. They are prose-only, but this project's own standing rule,
   stated verbatim in the same file at `:2688-2690`, is that *"a provenance claim the
   harness contradicts is a false evidence claim regardless of what the code does."*
   Accepting the nine-file set while its self-QA asserts an integrity property its own
   transcript shows did not hold would contradict the rule the document had just
   applied to R5-F2.

**Zero required findings were raised against the seven executable/plan targets.** On
the bytes alone, and setting the two reasons above aside, this set would be
PASS-WITH-NITS. What follows records what I verified, what I could not, and one new
nit the earlier rounds did not surface.

---

## 0. Scope and independence

Fresh Claude Pro session. I implemented no transport round; Max implemented r4–r6, so
implementer/auditor separation holds. Working dir `C:\LAB\Tradingview_LAB_CLEAN`,
branch `feature/donchian-crypto-ladder`, HEAD `347cb9ec23eda79fbb0f3a482e3d7ecf72ac99a7`
at session start. No repo byte was edited. No git mutation. No host contact, no
network, no RUNID allocation, no archive build, no freeze.

Codex `gpt-5.6-sol` already holds flagship PASS on these bytes
(`TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`).

---

## 1. What could not be done, stated first

| mandated step | outcome |
|---|---|
| Run `_r5_wsl_fixtures.sh` verbatim per `SELF_QA_TRANSPORT.md:2752-2755` | **NOT DONE** — `wsl.exe` blocked by session permissions, non-interactive, no approval path |
| List `C:\WPI_ARTIFACTS` to confirm no `WPI_TRANSPORT_*` entry | **NOT DONE** — read access outside `C:\LAB\Tradingview_LAB_CLEAN` and `C:\tmp` blocked |
| Inspect the round-3 residue at `C:\Users\Public\wpi_r3\...` on disk | **NOT DONE** — same block |
| `bash -n` on the five delivered shell files | **NOT DONE** — invocation blocked; unverified this session |
| Write this verdict file into `WPI_BLOCKS_DRAFT/` | **BLOCKED** — repo writes require approval; see §10 |

The harness **prerequisite** was satisfied before the block was hit, and is recorded
here because it is independently useful:

```
git cat-file -s   61696132a5f2fce97aad4054d41a780297ff21a1  ->  28756
git cat-file blob 61696132a5f2fce97aad4054d41a780297ff21a1 | sha256sum
  29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef
```

Both match the kickoff exactly. The blob was materialised to
`<scratch>/r6/pre/remote_close_tree_wpi.sh` and re-hashed at rest: 28756 B,
`29b6412a…c40ef`. The arm was ready; only the launcher was refused.

I did not substitute a different interpreter for the published one. Running the
harness under Git Bash instead of the WSL2 kernel would not be the published command,
and extract-and-run is forbidden by the contract.

---

## 2. Byte identity — re-derived, 10/10 exact

Re-derived from the current working-tree bytes, not read off any table.

| File | Bytes | SHA-256 | vs kickoff |
|---|---|---|---|
| `run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` | match |
| `run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` | match |
| `transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` | match |
| `TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | match |
| `remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` | match |
| `remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` | match |
| `remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` | match |
| `_r5_wsl_fixtures.sh` | 21221 | `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b` | match |
| `SELF_QA_TRANSPORT.md` | 194204 | `0a11d035f439906972386e354fa2dfb6bac5545fcd2db298adf64019bad25175` | — |
| `STATUS_TRANSPORT.md` | 24405 | `9b0871aff9c3c8434f7e4461d241168b9d0f66b6bad69f3eac9f4d9d46941ef3` | — |

**The round-6 byte-identity claim is TRUE and independently closed.** My seven
re-derived rows equal, cell for cell, both the round-5 §4 table
(`TRANSPORT_R5_REPORT_2026-08-11.md:321-327`) and the round-6 table
(`TRANSPORT_R6_REPORT_2026-08-11.md:239-245`). No target byte moved between round 5
and now. The scoping to seven — excluding the two QA/status documents — is correct and
I did not re-flag it.

Note for future auditors, confirming the kickoff's warning: the per-file census at
`SELF_QA_TRANSPORT.md:2323-2329` is a **round-3 historical snapshot**. Only
`TRANSPORT_PLAN.tsv` at 7970 B still matches current bytes. It must not be used as an
identity source.

### Static gates I could re-derive

| gate | re-derived result | vs `SELF_QA_TRANSPORT.md` §R6-5 |
|---|---|---|
| placeholder census over the seven targets | `alloc=37 pin=38` | matches |
| per-file census (p0 6/8, ro 6/4, runner 3/7, plan 22/7, setup 0/3, extract 0/7, close 0/2) | sums to 37/38 | matches both round tables |
| CR bytes, seven targets + harness | **0** in all eight | matches |
| `01_RUNKIT` present? | **absent** | consistent with "no archive built"; runner would STOP at `pinned_file_pin_unfilled` |

---

## 3. Adjudication of the four disclosed documentary defects

All four re-derived from the bytes myself. All four **confirmed**.

### F-1 — FALSE. The integrity envelope asserts a cleanup the transcript shows failed.

`:23` states *"All fixture scratch was removed; the last line of each transcript proves
it."* Three of the four fixtures do print such a line — `:349` `removed /tmp/wpi_r3_f3`,
`:645` `removed /wpi_r3_f4`, `:1159` `removed C:\Users\Public\wpi_r3\qa exists=False`.
The fourth does not. `:1475-1488` is the Fixture D cleanup tail:

```
=== cleanup ===
powershell.exe : Remove-Item : Cannot remove item
C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config: Yola erişim engellendi.
```

and there is **no** closing `removed … exists=False` line. The sentence at `:23` is
false as written, and so is §0's *"The scratch this round created has been removed,
which is why the paths do not currently exist"* (`:41-43`).

**The Lead's question — documentary only, or state that could affect a later arm?**

**Documentary, plus a bounded reproducibility defect. It is NOT evidence
contamination, and it moves no acceptance conclusion.** Four reasons, in the order
that decides it:

1. **Ordering.** The failure is at *teardown* of `f2_config_qa.ps1`, which §0 lists as
   the last of the four fixtures. Every M, K and L arm had already produced its
   recorded output before the cleanup ran. No round-3 arm executed after it, so no
   round-3 result can have read the residue.
2. **Rounds 4–6 cannot reach it.** They run entirely under WSL2 at `/root/wpi_r4*` /
   `/root/wpi_r5`, and `_r5_wsl_fixtures.sh:45` opens with `rm -rf "$FIX"`. The only
   Windows paths it touches are two read-only `sha256sum` reads of the close scripts
   (`:70`). There is no path by which `C:\Users\Public\wpi_r3\...` enters them.
3. **The delivered set cannot reach it.** `transport_runner.ps1:498` constructs the
   child's `PROGRAMDATA` as a run-owned, empty `<RECORD_ROOT>\sshconf`, and every
   pinned option block carries `-F none`. The residue is reachable only by the M arms,
   which deliberately pointed `PROGRAMDATA` at `$PDEVIL` (`:1303`, `:1305`) — exactly
   the channel those arms exist to demonstrate. Nothing in the delivered bytes reads
   `C:\Users\Public`.
4. **Where it IS a real, if bounded, defect: reproducibility, which D026 makes part of
   closure evidence.** `f2_config_qa.ps1` clears its own scratch at `:1229` with the
   same `Remove-Item -LiteralPath $QA -Recurse -Force` that failed at teardown. On this
   machine that path now holds an object whose ACL defeated exactly that call once, so
   **the published fixture is not idempotent on a host where it has already run** — a
   re-auditor can be stopped at *setup*, before any arm executes. Two aggravating
   details in the bytes: the restore at `:1401`
   (`icacls … /inheritance:e /grant … | Out-Null`) discards output and never checks
   `$LASTEXITCODE`, so a failed ACL restore is silent; and the removal at `:1229`/`:1402`
   has no post-condition line, so the fixture cannot detect that it left the object
   behind. That combination is why the failure reached the transcript instead of being
   caught by the fixture.

I could not confirm on disk whether the object is still present — reads outside the
repo are blocked in this session (§1). The reasoning above does not depend on it: if
it is gone, only the reproducibility half of the finding lapses; the false sentence at
`:23` stands either way, because the transcript records the failure.

**Severity: MEDIUM** for the false integrity sentence, **LOW–MEDIUM** for the
unverified, non-idempotent cleanup. Not a host-state finding.

### F-2 — FALSE. Independently re-derived: eleven, not ten; and J5 has no RED.

`:1598-1599` says *"F1 arms J1–J6 (RED and GREEN, ten runner executions)"*. I counted
the banners and their invocations directly rather than accepting the kickoff's number:

| banner | line | `COMMAND:` lines |
|---|---|---|
| J1 RED / J1 GREEN | 910 / 929 | 1 / 1 |
| J2 RED / J2 GREEN | 955 / 970 | 1 / 1 |
| J3 RED / J3 GREEN | 992 / 1007 | 1 / 1 |
| J4 RED / J4 GREEN | 1029 / 1038 | 1 / 1 |
| **J5 GREEN only** | **1060** | 1 |
| J6 RED / J6 GREEN | 1082 / 1096 | 1 / 1 |

Eleven banners, eleven `COMMAND:` lines, exactly one runner execution per banner. So
"ten" is wrong, and "RED and GREEN" is wrong for J5, which appears only as GREEN. The
count is understated and the pairing is overstated in the same sentence.

### U-1 — UNSUPPORTED. Independently re-derived: no reading yields twelve.

`:1600-1601` says *"Twelve of those executions are the real pinned OpenSSH programs."*
Enumerating the arms that actually start a pinned OpenSSH program:

- **M1–M6** — six real `ssh.exe -G` executions (`:1409-1425`).
- **M7** — a one-variable-out bisect printing **eight** rows (`:1438-1445`), i.e. eight
  real executions, or one arm.
- **K1, K2** — real `ssh.exe` through the runner (`:1118`, `:1137`): two.
- **K3** — real pinned `scp.exe` through the runner (`:1447`): one.
- **L1, L2, L3** — **zero.** All three STOP at the marker, pinned-option or
  configuration-pin gate (`:1460`, `:1465`, `:1472`) before any program is started.

Row reading: 6 + 8 + 2 + 1 = **17**. Arm reading: 6 + 1 + 2 + 1 = **10**. Neither is
twelve, and no transcript line prints twelve. Confirmed unsupported.

### U-2 — UNSUPPORTED as evidence, but TRUE by construction. Repair the argument, not the claim.

`:15-18` says `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry, *"(checked after
every fixture)"*. `WPI_ARTIFACTS` occurs exactly **once** in the whole 194 KB file — at
`:17`, the claim itself. No listing, no check, no transcript line. As an evidence claim
it is unsupported, and I could not list the directory to settle it either.

**But the bytes settle it, and the repair should say so rather than manufacture a
listing.** L1 (`:1468`) is the only arm that runs the delivered runner with its shipped
`$RECORD_ROOT = 'C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>'`. In
`transport_runner.ps1`:

- the marker gate runs at `:456-482`, ahead of everything;
- `Assert-MarkerFree 'BASE_RUN'` (`:456`) and `'RECORD_ROOT'` (`:461`) both fire on the
  delivered constants, exiting 3;
- the record root is not created until `:499-511`, and only inside `$executeMode`;
- `Flush-Log` (`:291-294`) returns without writing while `$script:RecordReady` is false,
  and it is set true only at `:509`.

So the delivered runner **cannot** create anything under `C:\WPI_ARTIFACTS`, and the QA
arms redirect `RECORD_ROOT` into the fixture scratch — visible at `:1454`,
`record=C:\Users\Public\wpi_r3\qb\rec\WPI_TRANSPORT_WPIQA`. The claim is almost certainly
true; what is missing is the reason, not the fact.

### Already-checked exclusion honoured

The round-6 byte-identity language at `:2665-2669` is correctly scoped to the seven
targets and explicitly excludes the two documents that legitimately changed. Not
re-flagged. My §2 independently confirms it.

---

## 4. Adversarial review of the classes the Codex rounds closed

Reasoned from the bytes; **not driven**, because the harness could not be launched.
Flagged as such throughout.

### First-mismatch semantics — sound

`$sequenceOk` starts true (`:773`) and is cleared exactly once, at the first non-`match`
class (`:1182`). Later `sequence_ok` rows skip with `TR_OP_SKIPPED` and are recorded
`classById[id]='skipped'`; `always` rows still run. A skip can only occur *after* a
mismatch, and any mismatch sets `$anyDeviant` or `$anyNotEvaluable`, so **`TR_RUN PASS`
is unreachable once anything has mismatched** (`:1198-1208`). Precedence
`deviant > not_evaluable` is stated in the record (`:1196`) and the `FAIL` line still
carries `first_not_evaluable`, so a run that both deviated and had holes does not hide
the holes.

### Per-branch cleanup prerequisites — sound, and bound bidirectionally

The graph at `:249-256` is 07←04, 08←05, 09←07, 10←08, 11←07+09, 12←08+10, exactly as
the plan's `always` rows require. It is bound to *this* plan before execution
(`:633-649`) in **both** directions: every `always` row must have an entry
(`always_op_has_no_prerequisite_entry`), every edge must name a real, strictly earlier
op (`prerequisite_names_unknown_op`, `prerequisite_not_earlier`), and every declared
entry must correspond to an existing `always` row
(`prerequisite_entry_for_unknown_op`, `prerequisite_entry_on_non_always_op`). A stale
or missing entry STOPs at plan time, not at classification time. `Resolve-Always-`
`Prerequisite` (`:1068-1084`) reads the class each prerequisite *actually* received, so
an unrelated branch cannot demote a genuine marked rc 1 — the F4 fix is present and
correctly wired.

I checked the BA-3 narrowing against the bytes and it is accurate: `:1103`
(`scp_transfer_did_not_complete`) and `:1108` (`operation_reported_stop`, rc 3) both
precede the prerequisite branch at `:1116`, so only rc-1 cleanups can reach
`cleanup_after_unestablished_prerequisite` / `cleanup_after_earlier_deviation`. Round 5
narrowed the prose rather than widening the classifier, which is the right direction.

### Per-operation provenance binding — sound, and satisfiable

`$MARKER_FAMILY_BY_STDIN` (`:231-237`) binds five disjoint prefix pairs to the five
stdin leaves; no prefix is a prefix of another. An `ssh_stdin` row whose leaf is not a
registered key is a **plan STOP before execution** (`:596-598`), so a new operation
cannot silently reintroduce an unbound marker set.

I additionally checked the reachability direction, which a purely negative test would
miss: **every delivered program actually emits its own registered family on both its
success and its refusal paths**, so the provenance test is satisfiable and the happy
path is not accidentally unreachable —

| program | family | refusal path | success path |
|---|---|---|---|
| `remote_setup_wpi.sh` | `SETUP_` / `SETUP ` | `:80` | `:478` `SETUP PASS` |
| `remote_extract_verify_wpi.sh` | `EXTRACT_` / `EXTRACT ` | `:71`,`:133-135` | `:466` `EXTRACT PASS` |
| `run_p0.sh` | `P0W_` / `P0W ` | `:47`,`:73`,`:157` | `:247` `P0W done` |
| `run_ro.sh` | `ROW_` / `ROW ` | `:41`,`:67`,`:156` | `:244` `ROW done` |
| `remote_close_tree_wpi.sh` | `CLOSE_` / `CLOSE ` | present | `CLOSE PASS` |

### Marker literalness and the preflight STOP — enforced, not incidental

`$UNFILLED_MARKERS` (`:270`) is **composed** from fragments rather than written out, so
a file-wide Stage-1 fill cannot rewrite the guard into real values and then STOP a
correctly frozen runner with a self-contradicting `unfilled_marker`. The census stays
honest because the only literals left in that file are consumers. The gate covers
`BASE_RUN`, `CONFIRM_TOKEN`, all four directory constants, `PLAN_SHA256`, every pinned
file/program/config path and digest, every element of `$SSH_PINNED_OPTIONS`,
`$SSH_TARGET` and every element of `$REMOTE_LAUNCH_DOMAIN`, and every plan row is
re-checked at `:541`. As delivered, the runner STOPs at
`TR_STOP reason=unfilled_marker field=BASE_RUN` at exit 3 before evaluating a path —
consistent with arm L1.

### A class the Codex rounds did not drive — see N-1 below

---

## 5. Findings

### N-1 (NIT, LOW) — `local_bind` reports a local representability limit as observed host deviation

**Pattern 1, "STOP is not a result", inverted.** `Invoke-LocalBind` builds `$local`
with an **Ordinal** (case-sensitive) comparer at `:995`, over an NTFS volume that is
case-**insensitive**. The remote evidence tree is a Linux filesystem and may legitimately
hold two names differing only in case. `scp -r` collapses them locally, so
`$remote.Digests` can hold two keys where `$local` holds one. Lines `:1010` / `:1014`
then set `$ok=$false`, and `:1015` returns **1** — which `Get-OpOutcomeClass` classifies
`deviant`, reason `operation_ran_and_observed_deviant_state`, producing `TR_RUN FAIL`.

Nothing about the host was observed to deviate. The transfer could not *represent* the
host's state locally. That is an inability to evaluate reported as a completed
observation — precisely the error F3 closed in the close script
(`CLOSE_FAIL reason=evidence_dir_absent` manufactured from an unevaluable probe), and
precisely why `:1103` already makes an incomplete `scp` `not_evaluable` rather than a
FAIL. The consistent answer here is rc 3 with a reason such as
`local_name_set_not_representable`, distinguished from a genuine
`digest_differs` / `size_differs`.

**Why it is a nit and not a required change:** it fails *loud*. It cannot manufacture a
false PASS — the worst case is a FAIL where a STOP would be more truthful, which is the
safe direction. It is recorded because ops 11/12 are the one operation family the
adversarial rounds did not drive, and because the misclassification is a real instance
of a class this project has otherwise closed everywhere.

**Not driven.** Reasoned from the bytes only; the harness could not be launched, and
these ops need a fetched tree that does not exist before Stage 1.

### Observation (not a finding) — the F1 residual is narrower at ops 07/08 than the prose conveys, and the prose is still correct

The exact forgery the F1 arm demonstrates — an exiting account-shell plant printing a
bare `CLOSE PASS …` line at rc 0 — would indeed be classified `match` at op 07, because
`Test-RemoteProvenanceMarkerForOp` binds marker *shape* to the plan row. But ops 11/12
apply `Read-RemoteCloseRecord` (`:914-978`) to that same stdout, and its state machine
requires `CLOSE_BINDING` → `CLOSE_DIGEST_BEGIN` → `CLOSE_DIGEST`* → `CLOSE_DIGEST_END`
→ `CLOSE_SIZE_BEGIN` → `CLOSE_SIZE`* → `CLOSE_SIZE_END` → `CLOSE_DIGEST_SET_SHA256`
before it will accept `CLOSE PASS`. A bare PASS line arrives in state `before` and
returns `remote_pass_mismatch` → rc 3 → `not_evaluable` → `TR_RUN STOP`. A two-way
digest **and** size binding against the fetched tree follows.

**F1 is nonetheless fully open**, and this does not narrow it: ops 01, 03, 04 and 05
have no second gate at all — provenance marker plus rc is the entire test — and those
are the operations that stage the premises. I record this only because it identifies
where the residual actually bites.

**No text overclaims here.** Every site I checked scopes the sentence to *"the runner's
provenance test"* (`STATUS_TRANSPORT.md:309-313`, the round-5 bullet at `:160-168`,
`transport_runner.ps1:179-181`, `_r5_wsl_fixtures.sh:319-322`), which is accurate. None
asserts that a full run would report PASS.

---

## 6. F1 scoping and the disclosed residuals — honest, and carried at every site

Owner ratification 2026-08-12 is ACCEPT-WITH-DISCLOSURE; per the kickoff I do not
demand closure. I verified the two things I was asked to verify.

**The disclosure is carried at every executable site.** All five delivered wrappers
carry `F1 IS OPEN - INNER CHILD CLOSED, OUTER SSH ACCOUNT-SHELL BOUNDARY OPEN` —
`run_p0.sh:51`, `run_ro.sh:45`, `remote_setup_wpi.sh:84`,
`remote_extract_verify_wpi.sh:75`, `remote_close_tree_wpi.sh:143` — each followed by
the mechanism (the account shell processes its startup environment before the string's
first token) and the closure requirement. `transport_runner.ps1:169-187` carries the
same, including the explicit withdrawal of round 4's "unreachable from the frozen plan"
reasoning and the statement that `Test-RemoteProvenanceMarkerForOp` binds marker shape
to a plan row rather than to the producing process. `STATUS_TRANSPORT.md` carries it in
the header, in "What changed in round 5", and as open item 2 with item 3 withdrawing
the "cannot select or influence" sentence. §R6-4 records the two prereg drafts.
`STATUS_TRANSPORT.md`'s claim that the sentence is stated in "all five wrappers" is
**true** — I checked each file individually.

**No text claims the inner-child `env -i` domain as an end-to-end F1 closure.** A
scoped sweep for `F1 is closed` / `F1 closed` / `closes F1` across both status
documents, all six executables and both prereg drafts returns **zero hits**.

**Derivation classes 5 and 6, and the inherited-`TMPDIR` residual, are honestly
scoped.** Class 5's inner-child attestation is described as binding the interpreter's
locator and constructed environment, *not its bytes*, and not reaching the account
shell. The `mktemp`/`TMPDIR` residual was not left as a disclosure: round 4 deleted
`mktemp` and made op 01 allocate a fifth `work` directory passed as a third argument,
after executing the falsification that showed the round-3 disclosure cost evidence
(`wrote_into_evidence_tree=0` at rc 0 while writing inside the tree). That is the
correct treatment — a disclosure is not a control, and it was replaced by one. The
BA-1 narrowed scope (a **nonzero** `mkdir` is deliberately not covered, because a
nonzero status is no evidence the object at that path is the one this run created) is
stated in the header, the create block and the `CLOSE_NOTE scratch` field, and the
uncovered case *names itself* in the record via `object_after_failed_create=present`.
An explicitly-labelled weaker claim, honestly scoped, is acceptable — this is one.

---

## 7. Thirteen-pattern adjudication

Patterns per `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

| # | pattern | adjudication on these bytes |
|---|---|---|
| 1 | STOP is not a result | **Clean on the seven targets, one nit.** rc grammar `{0,1,3}`, `ssh_transport_failure_rc255`, `rc_outside_outcome_grammar`, `scp_transfer_did_not_complete` and `operation_reported_stop` all resolve to `not_evaluable`; `deviant` requires an operation that ran and returned its own contract's deviant value. **N-1** is the single exception: a local case-fold collision in `local_bind` returns 1 (`deviant`) where 3 (`not_evaluable`) is the honest class. |
| 2 | Whose kernel answered? | **Clean.** Op 06 is an operator-side bounded TCP connect with `payload_bytes=0`; timeout, refusal, `connect_incomplete`, `socket_error` and `local_exception` are separated, and the non-terminal states are rc 3. The `SocketException` unwrap at `:876-887` avoids matching localized text. |
| 3 | The leaf is not the path | **Clean.** `Resolve-StdinPath` requires `<ROOT>:<basename>` against a frozen root map with `^[A-Za-z0-9._-]+$` leaves; `$capRel` in the close record must match `^[A-Za-z0-9._/-]+$`, may not be absolute and may not contain `.`/`..` segments; `local_path_outside_dir` and `local_reparse_point` fence the local side. |
| 4 | The privileged child brought its own environment | **Clean, and this is the set's strongest area.** `$psi.EnvironmentVariables.Clear()` then eight constructed entries, each with a printed rationale; the remote launch domain `env -i PATH=… LC_ALL=C HOME=… /usr/bin/bash --noprofile --norc -s --` is a runner constant required verbatim in every `ssh_stdin` row, and each delivered script re-attests it from the inside. **F1 remains open at the outer account shell** — disclosed, ratified, not claimed closed. |
| 5 | grep is not a parser | **Clean.** `Read-StrictAsciiLines` rejects non-ASCII, CR, control bytes and an unterminated final record; `Read-RemoteCloseRecord` is an ordered state machine with counts reconciled three ways (`declaredCount`, `sizes.Count`, `passDeclaredCount`) and a name-set cross-check, not a grep. Every regex capture is latched immediately (`:911-913`). |
| 6 | Read the status before the stdout | **Clean.** rc is read first and gated by kind; the provenance marker is required *before* an `ssh_stdin` rc is read as a probe result; `scp` is decided by kind because rc 1 collides with FAIL. |
| 7 | Nonzero read is not end of file | **Clean.** Both capture streams are drained concurrently via `CopyToAsync` with `.Wait()` after `WaitForExit`, so a full pipe cannot deadlock or truncate the record; a stdin write that fails yields `state=incomplete` and rc 3. |
| 8 | The name is not the identity | **Clean.** Programs are pinned by absolute path plus frozen digest plus `Test-TrustedProgramChain` (whole chain to `%SystemRoot%`, reparse-point free, owner and write/delete/ownership ACEs restricted to trusted numeric SIDs); stdin artifacts, the plan and pinned files are digest-bound; the plan pin is compared before rows are used. |
| 9 | The sentence outruns the probe | **DEFECT — F-1, F-2, U-1, U-2.** Four claims in `SELF_QA_TRANSPORT.md` that its own transcripts do not carry, three of them in the integrity envelope and coverage accounting. This is the pattern that drives the verdict. |
| 10 | Evidence that cannot fail | **DEFECT (bounded) — F-1's second half.** The Fixture D cleanup discards `icacls` output and never checks `$LASTEXITCODE` (`:1401`), and neither removal call has a post-condition line, so the fixture structurally could not detect its own failure. The delivered set is clean under this pattern: RED/GREEN pairs with a named uncovered case, and `REFUSAL_BYTE_IDENTICAL` computed on whole lines rather than compared by eye. |
| 11 | The declared instrument is not the executed instrument | **Clean, and demonstrably repaired.** This is exactly what R5-F2 was, and the round-6 harness now resets one tree, installs at one pathname `$BA1_SUBJECT`, launches one argv, and asserts `DISTINCT_SUBJECT_ARGV_LINES=1` over the recorded arms; instrumented variants are built under `$FIX/build/` and never launched from there. Withdrawing the round-5 transcript rather than keeping it beside the new one is the right call under D026. **I could not re-execute this to confirm the assertion fires** — see §1. |
| 12 | What the analyzer does not model must not disappear | **Clean.** Unknown kinds, run-whens, programs, op-id grammar, field counts, argv tokens, stdin specs and unregistered marker families all STOP rather than pass silently; `Read-RemoteCloseRecord`'s final `return … 'remote_close_unknown_or_out_of_order_record'` makes an unmodelled line a refusal, not a skip. |
| 13 | Every admitted member needs a terminal disposition | **Clean on the executables; the coverage prose is where F-2/U-1 sit.** Every op reaches exactly one of `skipped`, `match`, `deviant`, `not_evaluable`; §7's "deliberately not driven" table gives each undriven arm a reason and a fail direction. The defect is that §7's *counts* for the driven arms are wrong. |

**Patterns 9 and 10 produced required findings. No required defect was found under
patterns 1–8 or 11–13**, with the single LOW nit N-1 recorded under pattern 1.

---

## 8. Required changes

Prose-only. **No executable/plan target needs to change.**

1. **`SELF_QA_TRANSPORT.md:23` and `:41-43` (F-1).** Withdraw the "all fixture scratch
   was removed / the last line of each transcript proves it" sentence. Replace with the
   truth: three of four fixtures printed a closing removal line; Fixture D's cleanup
   failed access-denied on `…\qb\pd_evil\ssh\ssh_config`, the object was left behind,
   and it is inert with respect to every later arm and to the delivered set (state the
   reasons — teardown ordering, the WSL2-only rounds 4–6, and the run-owned
   `PROGRAMDATA` plus `-F none`).
2. **`f2_config_qa.ps1` cleanup (F-1, second half).** The published fixture body must
   check the `icacls` restore (`$LASTEXITCODE`) and assert the post-condition of its own
   removal, so a re-auditor is not blocked at setup and a failure cannot reach the
   transcript unremarked. Either repair the body or state explicitly that the fixture is
   not idempotent on a host where it has already run.
3. **`SELF_QA_TRANSPORT.md:1598-1599` (F-2).** "ten runner executions" → **eleven**, and
   drop "RED and GREEN" as a blanket claim over J1–J6: **J5 is GREEN-only.** If J5's RED
   was intended, say why it was not driven and in which direction it fails.
4. **`SELF_QA_TRANSPORT.md:1600-1601` (U-1).** Replace "Twelve" with a number the
   transcript supports, and state which reading it uses — **17** counting M7's eight
   bisect rows, or **10** counting M7 as one arm. Note that L1–L3 start no OpenSSH
   program at all.
5. **`SELF_QA_TRANSPORT.md:15-18` (U-2).** Either add the listing, or — better — replace
   "(checked after every fixture)" with the construction argument: the delivered runner
   STOPs at the marker gate before the record root is created, `Flush-Log` writes
   nothing while `RecordReady` is false, and the QA arms redirect `RECORD_ROOT` into the
   fixture scratch (visible at `:1454`).
6. **Optional, N-1.** Reclassify `Invoke-LocalBind`'s name-set disagreement so that a
   local representability limit returns 3 / `not_evaluable` with its own reason, keeping
   1 / `deviant` for genuine digest or size differences.

Per the WP-I claim-audit discipline, whoever applies 3 and 4 should grep the changed
numbers repo-wide: the same counts are echoed in the round reports and in
`STATUS_TRANSPORT.md`, and a partial correction is itself a defect this project has
already hit five times.

## 9. What a re-audit must do that this session could not

The second flagship slot needs an auditor session that can launch `wsl.exe`. That
session must run the published command verbatim from `SELF_QA_TRANSPORT.md:2752-2755`
with `<scratch>/r6/pre` materialised from blob `61696132…` (28756 B, `29b6412a…c40ef`),
and record `FIXTURE_RC`, `FIXTURE_STDERR_LINES/BYTES`, `FIXTURE_STDOUT_LINES`,
`BA1_ARMS_RECORDED`, `DISTINCT_SUBJECT_ARGV_LINES`, `THE_LINE` and
`REFUSAL_BYTE_IDENTICAL` against §R6-2. It should also list `C:\WPI_ARTIFACTS` for
`WPI_TRANSPORT_*` and confirm whether the F-1 residue is still on disk. Everything in
§2–§7 of this file is independent of that run and can be carried forward.

**Session prerequisite for the re-audit:** add `wsl.exe` (and read access to
`C:\WPI_ARTIFACTS`) to the auditor session's permission allowlist, or run the audit
interactively so approvals can be granted. This lane will fail the same way otherwise.

---

## 10. Delta gate — and where this file actually is

**This file could not be written into the repository.** Writes to
`C:\LAB\Tradingview_LAB_CLEAN` require approval in this session and the session is
non-interactive, so the deliverable at
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
**does not exist.** This copy lives in the session scratchpad at
`…\scratchpad\TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` and must be moved into
`WPI_BLOCKS_DRAFT/` under that exact name by someone with write access.

The gate is therefore reported against what actually happened, not against what the
kickoff anticipated:

**Before execution** (`git status --porcelain` → `before`): 123 entries — all
pre-existing modifications and untracked run logs from earlier sessions.

**After** (`git status --porcelain` → `after`): `diff before after` is **empty**.

```
$ diff before.txt after.txt
(no output)
```

`after` minus `before` contains **zero** entries. The kickoff's gate requires that the
delta contain *only* the verdict file; the delta contains **nothing**, because the
verdict file could not be created. **No unauthorised entry appeared, so the gate's
prohibition is satisfied — but its positive condition is not met, and this is recorded
as a shortfall rather than a pass.**

Path-scoped confirmation:

```
$ git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
(no output — the file does not exist)
```

The working tree is byte-identical to session start. HEAD is unchanged at
`347cb9ec23eda79fbb0f3a482e3d7ecf72ac99a7`. No git mutation of any kind. Scratch used
for the blob materialisation is outside the repository, under the session scratchpad.

---

**Auditor:** Claude `claude-opus-5` xhigh, Claude Pro account, 2026-08-12.
**Verdict: REQUEST_CHANGES.** Second flagship slot **not** closed; transport does
**not** reach dual flagship acceptance. Zero required findings against the seven
executable/plan targets; six required changes, all documentary, plus one LOW nit.

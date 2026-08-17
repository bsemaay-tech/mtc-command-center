# TRANSPORT — Claude `claude-opus-5` xhigh T0 RE-AUDIT, SECOND FLAGSHIP (slot-closing)

**Verdict: PASS-WITH-NITS.**

**The transport set reaches DUAL FLAGSHIP ACCEPTANCE.** Codex `gpt-5.6-sol` holds
flagship PASS on the seven frozen targets
(`TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`); this session, as an independent second
flagship, accepts the same seven targets on re-derived bytes together with the six
documentary repairs applied at `a0fa8271`, having executed the mandated WSL2 harness
verbatim and reproduced the published transcript line-for-line.

Both grounds of the prior REQUEST_CHANGES
(`TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`) are cleared:

| prior ground | status now | evidence |
|---|---|---|
| (a) false integrity sentence in `SELF_QA_TRANSPORT.md`, violating its own rule at `:2688-2690` | **CLEARED** — corrected to what the transcript proves, at both sites, with the parallel correction carried into `STATUS_TRANSPORT.md` and a non-rewriting marker in `TRANSPORT_REPAIR_R3_REPORT.md` | §4.1, §4.5 |
| (b) mandated WSL harness could not run (session permissions) | **CLEARED** — run verbatim, `FIXTURE_RC=0`, 0 bytes of stderr, 280 stdout lines, transcript diff against the published block = **1 line, and that line differs only in this session's scratchpad id** | §3 |

Three LOW nits remain and none is a required change: **N-1** (carried, optional, from
the prior verdict's §8.6), **N-2** (new, a mis-attached causal clause in the Fixture D
disclosure), **N-3** (new, a pre-existing one-word imprecision in `STATUS_TRANSPORT.md`
that the repair round did not own).

---

## 0. Scope and independence

Fresh Claude Pro session, `claude-opus-5` xhigh, AUDITOR. I implemented no transport
round and I did not author the six repairs (Codex free authored them; Max implemented
r4–r6). Working dir `C:\LAB\Tradingview_LAB_CLEAN`, branch
`feature/donchian-crypto-ladder`, HEAD `97b5b98522224db2ca27c79d96be1e1d86992b44` at
session start.

No repo byte was edited except this file. No git mutation — the only Git commands run
were `git status --porcelain`, `git rev-parse`, `git cat-file` and one `git diff` of an
existing commit, all read operations. No host contact, no network, no RUNID allocation,
no archive build, no freeze. Local WSL2 fixture execution under `/root/wpi_r5` was
performed exactly as the published harness does it, which the original kickoff permits.
Bulk harness output was redirected to the session scratchpad, not the repo.

---

## 1. Identities — re-derived, 2026-08-13

Re-derived from the current working-tree bytes with `stat -c%s` and `sha256sum`, not
read off any table.

### The seven frozen targets — 7/7 exact against the frozen kickoff table

| File | Bytes | SHA-256 | vs frozen table |
|---|---:|---|---|
| `run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` | **match** |
| `run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` | **match** |
| `transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` | **match** |
| `TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | **match** |
| `remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` | **match** |
| `remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` | **match** |
| `remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` | **match** |

**No target byte moved.** These equal, cell for cell, the frozen table, the prior
Claude verdict's §2, and the post-repair table in
`TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md:76-82`. The repair round's claim that it
did not touch the seven targets is **independently true**.

The harness also matches its published identity:

| File | Bytes | SHA-256 | vs kickoff |
|---|---:|---|---|
| `_r5_wsl_fixtures.sh` | 21221 | `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b` | **match** |

### The documents that changed — NEW values, stated as required

| File | Bytes (was) | Bytes (now) | SHA-256 (now) |
|---|---:|---:|---|
| `SELF_QA_TRANSPORT.md` | 194204 | **195263** | `8a307344ccd16476c1ab07cd50b91708439ad7fae0abb4d07210d86e7d6ec456` |
| `STATUS_TRANSPORT.md` | 24405 | **25114** | `d1d041f31aa726908370890f4689122b614c1f10d187a56e2b007e7e864039f5` |
| `TRANSPORT_REPAIR_R3_REPORT.md` | — | **20640** | `f6b556098ac602dcc8dc1fbfaab986de8801b648320c4d39e0ec9b96d03947be` |

The two "was" values are the prior verdict's §2 rows. Both new values equal the repair
report's self-declared post-repair table (`:88-89`) exactly, so that report's identity
claim is confirmed rather than taken on trust. `TRANSPORT_REPAIR_R3_REPORT.md` was also
edited by the repair round; the report does not publish its identity, so the value above
is derived here for the first time.

Because `SELF_QA_TRANSPORT.md` grew by 1059 bytes, **its line numbers have shifted**
relative to every earlier audit. All `:NNN` references in this file are against the
**current** bytes. Where a prior audit's number is quoted, it is labelled as such.

---

## 2. What is inherited, and what is judged fresh

Per contract item 4:

- **Inherited and cited, not re-derived:** the prior verdict's §2 static gates (`alloc=37
  pin=38`, per-file census, zero CR bytes, `01_RUNKIT` absent), §4 (first-mismatch
  semantics, per-branch cleanup prerequisites, per-operation provenance binding, marker
  literalness), §6 (F1 scoping and the disclosed residuals carried at every site) and §7
  (thirteen-pattern adjudication). Those analyses were performed on the seven targets'
  bytes, and §1 above proves those bytes have not moved by a single byte. Re-deriving
  them would produce the same result by construction.
- **Judged fresh on current bytes:** everything in `SELF_QA_TRANSPORT.md`,
  `STATUS_TRANSPORT.md` and `TRANSPORT_REPAIR_R3_REPORT.md` — §4 and §5 below — and the
  harness execution, §3.

The prior verdict's pattern-9 and pattern-10 rows are the two that carried DEFECT
adjudications, and both were driven entirely by the four documentary findings. §4
re-adjudicates them. **Pattern 9 is now clean; pattern 10's delivered-set half was
already clean and its fixture half is now disclosed rather than hidden** (see N-2).

---

## 3. The mandated harness — EXECUTED

### Prerequisite

```
git cat-file -s   61696132a5f2fce97aad4054d41a780297ff21a1  ->  28756
sha256sum <scratch>/r6/pre/remote_close_tree_wpi.sh
  29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef
```

28756 B and `29b6412a…c40ef`, both matching the original kickoff, re-hashed at rest
after materialisation.

### The command, verbatim per `SELF_QA_TRANSPORT.md:2765-2768`

```text
wsl.exe -u root -- /usr/bin/bash --noprofile --norc \
  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh \
  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT \
  <scratch>/r6/pre
```

No interpreter was substituted and nothing was extracted and re-run. `<scratch>` is this
session's scratchpad, outside the repository.

### Result

| field | published `:2770-2773` | this run | |
|---|---|---|---|
| `FIXTURE_RC` | 0 | **0** | match |
| `FIXTURE_STDERR_LINES` | 0 | **0** | match |
| `FIXTURE_STDERR_BYTES` | 0 | **0** | match |
| `FIXTURE_STDOUT_LINES` | 280 | **280** | match |

Stdout was 16296 B, zero CR bytes.

**Measurement note for future auditors.** PowerShell's
`Get-Content | Measure-Object -Line` returns **257** for this stdout, because it does not
count the 23 empty lines (280 − 23 = 257). `wc -l` returns 280 and is the reading that
matches the published field. A re-auditor who measures with `Measure-Object -Line` will
see an apparent 23-line shortfall that is an artefact of the tool, not of the harness.

### The published summary assertions, re-derived from my own run

| assertion | published | this run |
|---|---|---|
| `RETARGET_ANCHORS` | `hit_in_both_arms` (`:2792`) | `hit_in_both_arms` (my `:11`) |
| `REFUSAL_BYTE_IDENTICAL` | `yes` (`:2845`) | `yes` (my `:64`) |
| `BA1_ARMS_RECORDED` | `10` (`:2718`, `:2983`) | `10` (my `:202`) |
| `DISTINCT_SUBJECT_ARGV_LINES` | `1` (`:2719`, `:2984`) | `1` (my `:203`) |
| `THE_LINE` | `:2720`, `:2985` | **identical string** (my `:204`) |

### The strongest single result: a whole-transcript diff

The published §R6-2 block is `SELF_QA_TRANSPORT.md:2782-3061` — exactly 280 lines. I
diffed my captured stdout against it in full:

```text
$ diff published_r6_2.txt r6_fixture_stdout.txt
10c10
< 29b6412a…c40ef  /mnt/c/Users/…/d99e3b8e-1ade-4486-9408-0cee0036ce6d/scratchpad/r6/pre/remote_close_tree_wpi.sh
---
> 29b6412a…c40ef  /mnt/c/Users/…/d297e528-d0f0-4c86-9854-f745e1036b4d/scratchpad/r6/pre/remote_close_tree_wpi.sh
```

**279 of 280 lines are byte-identical, and the one differing line differs only in the
session-id component of the scratch path — the digest on that line is the same.** Every
`SUBJECT_SHA256`, every `SCRIPT_RC`, every `RESIDUE_PRESENT`, every reason token, both
assertion lines, both refusals, the F1-outer arm and all seven BA-2 arms reproduce
exactly. The published transcript is not a narrative about a run; it is the run.

This is the first independent re-execution of this harness by a non-implementer. It
closes the prior verdict's §9 in full and settles the one pattern-11 item the prior
session had to leave open (*"I could not re-execute this to confirm the assertion
fires"*): `DISTINCT_SUBJECT_ARGV_LINES=1` **fires, live, over ten recorded arms**.

---

## 4. The six repairs, adjudicated against the prior verdict's §8

### 4.1 — §8.1, the false integrity sentence. **APPLIED, CORRECT.**

`SELF_QA_TRANSPORT.md:26-33` now reads that fixture cleanup *did not fully succeed*:
three fixtures printed closing removal lines, Fixture D's cleanup failed access-denied
on `C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config` and printed no closing
`removed ... exists=False` line. The withdrawn sentences ("All fixture scratch was
removed; the last line of each transcript proves it" and §0's "The scratch this round
created has been removed") are **gone from the file**.

Every element re-derived against the transcript, not accepted:

| claim | evidence in current bytes |
|---|---|
| three fixtures printed a closing removal line | `:361` `removed /tmp/wpi_r3_f3`; `:657` `removed /wpi_r3_f4`; `:1171` `removed C:\Users\Public\wpi_r3\qa exists=False` |
| Fixture D failed access-denied on that exact path | `:1487-1502`, `Remove-Item : Cannot remove item C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config: Yola erişim engellendi.` |
| Fixture D printed no closing line | `exists=False` occurs in the whole file only at `:30` (the prose) and `:1171` (Fixture C) |

The three stated reasons for inertness were each verified against bytes rather than
inherited:

1. **Teardown ordering.** The failure is in Fixture D's `=== cleanup ===` block, after
   the L1 arm at `:1480-1486`; Fixture D (§5) is the last fixture section.
2. **Rounds 4–6 are WSL2-rooted.** `_r5_wsl_fixtures.sh:40` `FIX=/root/wpi_r5`, `:45`
   `rm -rf "$FIX"`. Every write in that file is under `$FIX`. It contains no literal
   `C:\Users\Public` and no literal `/mnt/c` path at all — its only Windows access is
   through its two arguments, read-only (`:70` `sha256sum "$CUR/…" "$PRE/…"`, plus
   `mkfix` reading `$CUR`). There is no path by which the round-3 residue enters it.
3. **The delivered runner cannot reach it.** `transport_runner.ps1:496-497` and `:745`
   construct the child's `PROGRAMDATA` as a run-owned, empty directory; `:139` pins
   `'-F', 'none'` as the head of `$SSH_PINNED_OPTIONS`, and `:756` re-checks that.

### 4.2 — §8.2, the Fixture D non-idempotence. **APPLIED via the disclosure option.**

§8.2 permitted either repairing the fixture body or stating explicitly that it is not
idempotent. The disclosure route was taken, at `SELF_QA_TRANSPORT.md:50-55` and
`STATUS_TRANSPORT.md:60-66`. The published body is unchanged, which is consistent —
under D026 a historical transcript's body must not be silently rewritten.

Both cited mechanisms are true of the published body:

- `:1413` `& icacls.exe $evilCfg /inheritance:e /grant … | Out-Null` — output discarded,
  `$LASTEXITCODE` never read.
- `:1414` `if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }`
  — the removal that failed.

The scoping is exactly right: SELF_QA says "not idempotent **on a host where its prior
access-denied residue still exists**", and STATUS says a re-auditor "**may** need to
clear it". Both are conditional, and §6 below shows the condition is currently false on
this host — so the disclosure is conservative, not overstated. See **N-2** for the one
wording defect.

### 4.3 — §8.3, the J-family count. **APPLIED, CORRECT — independently re-derived.**

`:1611-1612`: *"F1 arms J1–J4 and J6 have RED/GREEN pairs, J5 is GREEN-only (eleven
runner executions total)"*. I counted the banners on current bytes rather than trusting
either the prior audit or the repair:

| banner | line |
|---|---|
| J1 RED / J1 GREEN | 922 / 941 |
| J2 RED / J2 GREEN | 967 / 982 |
| J3 RED / J3 GREEN | 1004 / 1019 |
| J4 RED / J4 GREEN | 1041 / 1050 |
| **J5 GREEN only** | **1072** |
| J6 RED / J6 GREEN | 1094 / 1108 |

**Eleven.** J5 has no RED banner. The blanket "RED and GREEN" is gone. Correct.

§8.3's trailing clause was conditional — *"if J5's RED was intended, say why it was not
driven"*. J5's RED was not intended: `:1197-1199` frames J5 as a survival control on the
repaired bytes (*"FAIL must survive … The repair narrows FAIL; it does not abolish
it"*), for which a pre-repair arm proves nothing. The conditional does not fire. J5 RED
is correspondingly absent from §7's "deliberately not driven" table, which is
consistent, though the document nowhere says in one place that J5 is GREEN-only *by
design*. Not a finding.

### 4.4 — §8.4, the OpenSSH count. **APPLIED, CORRECT — independently re-derived.**

`:1612-1614`: *"17 executions if M7's eight bisect rows are counted as rows, or 10
executions if M7 is counted as one arm. L1–L3 start no OpenSSH program."* Re-derived:

| arms | starts | lines |
|---|---:|---|
| M1–M6, real `ssh.exe -G` | 6 | `:1421-1445` |
| M7, one-variable-out bisect, eight printed rows | 8 rows / 1 arm | `:1447-1455` |
| K1, K2, real `ssh.exe` through the runner | 2 | `:1130`, `:1149` |
| K3, real pinned `scp.exe` through the runner | 1 | `:1459` |
| L1, L2, L3 | **0** | `:1480` marker STOP, `:1470` option-block refusal, `:1475` config pin unfilled |

Row reading 6+8+2+1 = **17**. Arm reading 6+1+2+1 = **10**. The document states both and
names which reading each is. Neither reading yields twelve, and "Twelve" is gone.
Correct, and better than the minimum §8.4 asked for, because it does not silently pick
one reading.

### 4.5 — §8.5, the U-2 construction argument. **APPLIED, and the stronger option was taken.**

§8.5 offered "either add the listing, or — better — replace it with the construction
argument". The better option was taken. `:17-21` now reads that the delivered runner
*cannot create* a `C:\WPI_ARTIFACTS\WPI_TRANSPORT_*` record root while shipped with
markers, because the marker gate stops at `BASE_RUN`/`RECORD_ROOT` before record-root
creation and `Flush-Log` writes nothing while `RecordReady` is false; the QA arms
redirected `RECORD_ROOT` into fixture scratch. `(checked after every fixture)` is gone,
and `STATUS_TRANSPORT.md:49-50` adds the explicit **"No external listing is claimed
here"**.

Every element checked against the runner's (unchanged) bytes:

| assertion | bytes |
|---|---|
| marker gate stops at `BASE_RUN` | `:456` `Assert-MarkerFree 'BASE_RUN' $BASE_RUN` |
| …and at `RECORD_ROOT` | `:461` `Assert-MarkerFree 'RECORD_ROOT' $RECORD_ROOT` |
| …before record-root creation | record root created at `:502`, inside `if ($executeMode)` at `:499` |
| `Flush-Log` writes nothing while `RecordReady` is false | `:291-292` early `return`; `:274` initialises `$false`; `:509` sets `$true` |
| QA arms redirected `RECORD_ROOT` into fixture scratch | the quoted line `TR_RUN PASS base_run=WPIQA record=C:\Users\Public\wpi_r3\qb\rec\WPI_TRANSPORT_WPIQA` is **verbatim present** at `:1466` |

That last row matters: the repair quotes a transcript line as its support, and the quote
is real, not manufactured. `WPI_ARTIFACTS` now occurs **exactly once** in the whole
195 KB file — at `:18`, inside the construction claim — so no residual evidence claim
survives anywhere in the document.

### 4.6 — §8.6, N-1. **Optional, not applied. Correctly so.**

`Invoke-LocalBind`'s case-fold classification is unchanged, as the repair report states
(`:32`). §8.6 marked it optional and it touches an executable target, which the repair
round was scoped out of. N-1 remains open and remains a LOW nit; it fails loud and
cannot manufacture a false PASS.

### 4.7 — repo-wide staleness sweep (WP-I claim-audit discipline)

The prior verdict's closing instruction was to grep the changed values repo-wide,
because partial correction has bitten this project five times. Swept for all five
withdrawn strings (`All fixture scratch was removed`, `checked after every fixture`,
`ten runner executions`, `Twelve of those executions`, `scratch this round created has
been removed`):

- **Zero hits in `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md` and
  `TRANSPORT_REPAIR_R3_REPORT.md`.** The correction is complete across all three owned
  documents.
- Surviving hits are confined to (i) the kickoffs and audit verdicts that *quote* the
  defect in order to raise it — including this lane's own two kickoffs and the prior
  verdict — (ii) the repair report's own before/after table and grep-command text, and
  (iii) historical run logs and claim-audit records under `11_TRIAGE/`. Every one is a
  legitimate historical quotation, not a live claim. **No uncorrected live claim
  remains.**

The historical `TRANSPORT_REPAIR_R3_REPORT.md` was handled correctly under D026: rather
than rewriting the past, `:14-18` marks the original `C:\WPI_ARTIFACTS` sentence as *not
external-listing evidence* and points at the construction proof, and `:48-52` marks the
original count shorthand and states the corrected eleven / 17 / 10 figures. That is the
right treatment — the record stays legible and the reader is not misled.

---

## 5. Did any repair introduce a new overclaim? (Rule 9b classes)

**No.** Each repaired sentence was tested against the artefact it cites:

| repaired claim | outrun by the probe? |
|---|---|
| three fixtures printed removal lines; D did not | **No** — `:361`, `:657`, `:1171` present; D's tail at `:1487-1502` |
| residue inert (teardown order, WSL2 rounds, run-owned `PROGRAMDATA` + `-F none`) | **No** — all three verified in §4.1 |
| fixture not idempotent where residue remains | **No** — conditional, and true; see N-2 for the mechanism wording |
| eleven J-family runner executions | **No** — eleven banners counted |
| 17 by row reading / 10 by arm reading; L1–L3 zero | **No** — both re-derived |
| runner cannot create a `WPI_TRANSPORT_*` record root | **No** — four runner line-refs verified; quoted transcript line verbatim at `:1466` |
| "No external listing is claimed here" | **No** — and this is the honest form; see §6 |

The repairs are, if anything, *weaker* than the evidence now permits (§6), which is the
safe direction. **Pattern 9 ("the sentence outruns the probe") is now clean on the
transport set.**

---

## 6. Two things the prior session could not check, settled here

Read access outside the repo was available to this session, so both of the prior
verdict's open empirical questions are now answered.

**1. `C:\WPI_ARTIFACTS` — listed. Zero `WPI_TRANSPORT_*` entries.** The directory exists
and holds 15 subdirectories and ~130 files, all from the GATE-A / WP-L lanes. It
contains `WPLP2_TRANSPORT_WPLP2-…` and `WPLP2B_TRANSPORT_WPLP2B-…` (WP-L Phase 2, a
different prefix) and **no `WPI_TRANSPORT_*` entry whatsoever**. The U-2 fact is
therefore true not only by construction but by external observation.

Note what this does *not* change: the repaired document still says "No external listing
is claimed here", and that remains the correct thing for it to say, because the
document's own transcripts contain no listing. A claim must be supported by the evidence
it cites, not by evidence an auditor happens to gather later. The repair should **not**
now be widened to assert the listing.

**2. The F-1 residue is gone.** `C:\Users\Public\wpi_r3` does not exist; neither does
`…\qb\pd_evil\ssh\ssh_config`. The prior verdict anticipated exactly this
(*"if it is gone, only the reproducibility half of the finding lapses; the false
sentence stands either way"*). Accordingly:

- the reproducibility half of F-1 **lapses on this host** — `f2_config_qa.ps1` would not
  be blocked at setup here today;
- the disclosure at `SELF_QA_TRANSPORT.md:50-55` is correctly conditional, so it remains
  accurate and simply does not bind on this host;
- the false-sentence half was real regardless, because the transcript records the
  failure, and it is repaired.

---

## 7. Nits (three, all LOW, none required)

### N-1 (LOW, carried, optional) — `Invoke-LocalBind` reports a representability limit as observed deviation

Unchanged from the prior verdict's §5/§8.6, on unchanged bytes. An NTFS case-fold
collision makes `$local` smaller than `$remote.Digests`, returning 1 (`deviant`) where 3
(`not_evaluable`, e.g. `local_name_set_not_representable`) is the honest class. It fails
loud and cannot manufacture a false PASS. Ops 11/12 remain the one operation family the
adversarial rounds have not driven; they cannot be driven before Stage 1 exists.

### N-2 (LOW, new) — the Fixture D disclosure attaches the right facts to the wrong mechanism

`SELF_QA_TRANSPORT.md:50-55` says the body is not idempotent *"because* the ACL restore
… does not check `$LASTEXITCODE` and the cleanup has no post-condition assertion."

Both cited facts are true, but neither is what blocks a re-run. The proximate blocker is
that the **setup-side** removal at `:1241` —
`if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }` — runs
under `$ErrorActionPreference = 'Stop'` (`:1227`, with `Set-StrictMode -Version 2.0` at
`:1226`), so on a host still holding the ACL-protected object the script **terminates at
setup**, before any arm. The two cited facts explain why the fixture *failed to notice*
its own teardown failure; they do not explain why a re-run *stops*.

There is a second, sharper detail worth stating, because a reader checking the body will
otherwise think the prose contradicts it: the body **does** carry a post-condition line —
`:1415` `Write-Host ('removed ' + $QA + ' exists=' + (Test-Path -LiteralPath $QA))`,
immediately after the failing removal at `:1414`. It never ran precisely *because*
`$ErrorActionPreference = 'Stop'` made the access-denied `Remove-Item` terminating. That
is also the complete explanation of why Fixture D's transcript has no closing
`removed … exists=False` line while Fixture C's does. So "no post-condition assertion" is
defensible as written — the line reports rather than asserts, and is unreachable on the
failure path — but it reads as though the line is absent, and it is not.

**Suggested wording**, if the Lead chooses to take it: *"…is not idempotent on a host
where its prior access-denied residue still exists, because the setup-side removal at
`:1241` runs under `$ErrorActionPreference='Stop'` and terminates on the same object. The
teardown failure went unremarked because the ACL restore (`icacls … | Out-Null`) does not
check `$LASTEXITCODE`, and because the post-condition line at `:1415` is unreachable once
the removal itself throws."*

Why this is a nit and not a required change: nothing asserted is false, the conclusion
(not idempotent) is true, the scoping is conditional and correct, and the condition is
currently false on this host (§6). It is a precision defect in a disclosure, not a claim
the evidence contradicts.

### N-3 (LOW, new, pre-existing text — not owned by the repair round) — one word in `STATUS_TRANSPORT.md`

`STATUS_TRANSPORT.md:55-58` reads *"Rounds 4, 5 and 6 ran their shell fixtures against a
local WSL2 Ubuntu kernel; every path they touch is under `/root/wpi_r4*` or
`/root/wpi_r5` on that local filesystem."*

Every path they **write** is. The round-6 harness also **reads** two `/mnt/c` paths —
`_r5_wsl_fixtures.sh:70` `sha256sum "$CUR/remote_close_tree_wpi.sh"
"$PRE/remote_close_tree_wpi.sh"`, plus `mkfix` reading `$CUR` — as my own run's transcript
lines 9–10 print. Substituting "write" for "touch" makes the sentence exactly true.

I confirmed by `git diff a0fa8271~1 a0fa8271` that this sentence is **unchanged context**,
not repair-introduced, so it is not a regression and was outside the repair kickoff's
ownership. Recorded so it is not lost. It fails in the safe direction: the understated
activity is read-only hashing of repo bytes.

---

## 8. Adjudication summary

| item | verdict |
|---|---|
| seven frozen targets, byte identity | **7/7 exact**, plus harness 1/1 |
| required findings against the seven targets | **zero** (this session and the prior one) |
| six repairs vs prior §8 | **five applied and correct; the sixth was optional and correctly not applied** |
| new overclaim introduced by a repair | **none** |
| repo-wide staleness of the corrected values | **complete across all three owned documents** |
| mandated WSL harness | **executed verbatim; 279/280 transcript lines byte-identical, the 280th differing only by session-id** |
| open nits | **N-1 (carried), N-2 (new), N-3 (new)** — all LOW, none required |
| F1 residual | **open, ratified ACCEPT-WITH-DISCLOSURE, not claimed closed anywhere** (inherited §6, unchanged bytes) |

**Second-flagship acceptance sentence.** *As the second flagship on these bytes, I accept
the WP-I transport set: the seven frozen executable/plan targets at the identities in §1,
together with `SELF_QA_TRANSPORT.md` at 195263 B /
`8a307344ccd16476c1ab07cd50b91708439ad7fae0abb4d07210d86e7d6ec456` and
`STATUS_TRANSPORT.md` at 25114 B /
`d1d041f31aa726908370890f4689122b614c1f10d187a56e2b007e7e864039f5`. With Codex
`gpt-5.6-sol`'s flagship PASS, the transport set reaches DUAL FLAGSHIP ACCEPTANCE.*

This closes the second-flagship slot. It is an acceptance of the transport documentary
and executable set as frozen; it authorises no host contact, no RUNID allocation, no
archive build and no freeze.

---

## 9. Delta gate

Per contract item 5, the **path-scoped confirmation is the gate**; the whole-status delta
is advisory, because concurrent lanes commit in this worktree.

### The gate — PASS

```text
$ git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md
```

Exactly one entry, untracked, at the exact path the kickoff names. **Gate passes.**

### Whole-status delta — advisory, with attribution

`before` (session start) and `after` (session end) each have 132 entries. HEAD moved
during the session, from `97b5b98522224db2ca27c79d96be1e1d86992b44` to
`d28a2735037282635e2b0ca6fe85edb304b48778`, because a concurrent lane committed.

**`after` minus `before` — 4 entries:**

| entry | attribution |
|---|---|
| `?? …/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md` | **mine** — this file |
| `?? …/11_TRIAGE/RP7_ROWS_1_9_REBUILD_CODEXFREE_RUN_2026-08-13.log` | concurrent RP7 rows-1–9 rebuild lane |
| `?? …/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP7_ROWS_1_9_EVIDENCE_REBUILD.md` | concurrent RP7 rows-1–9 rebuild lane |
| `?? …/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_R3_GLM_RUN_2026-08-13.log` | concurrent Pathscope r3 GLM lane |

**`before` minus `after` — 4 entries**, all Pathscope-lane files that stopped being dirty
because that lane committed them: `SELF_QA_PATHSCOPE.md`, `pathscope_prover.py`,
`GLOBAL_HANDOFF.md`, and `PATHSCOPE_GLM_T1_R3_REPAIR_REPORT_2026-08-13.md`. The two
commits are `08a0c43f` (pathscope round-3 repair of CRITICAL C-1) and `d28a2735`
(GLOBAL_HANDOFF entry for that lane).

**I authored exactly one of the eight delta entries.** The other seven belong to two
identified concurrent lanes and none is in my scope.

### Non-interference proof

The concurrent commits did not touch the bytes I accepted:

```text
$ git diff --name-only 97b5b985..HEAD -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/
(no output)
```

Zero files in `WPI_BLOCKS_DRAFT/` changed between session start and session end. I
re-hashed all nine acceptance-set files at the **new** HEAD after the concurrent commits
landed; every size and digest is unchanged from §1. The acceptance in §8 therefore
stands at `d28a2735` exactly as it was derived at `97b5b985`.

No git mutation was performed by this lane. The only Git commands run were
`git status --porcelain`, `git rev-parse`, `git log`, `git cat-file`, and
`git diff` of existing commits — all read operations. Scratch for the blob
materialisation and the harness capture is outside the repository, in the session
scratchpad. No repo byte was edited except this file.

---

**Auditor:** Claude `claude-opus-5`, effort **xhigh**, Claude Pro account, 2026-08-13.
**Verdict: PASS-WITH-NITS. Second flagship slot CLOSED; transport reaches DUAL FLAGSHIP
ACCEPTANCE.** Zero required findings against the seven executable/plan targets; six
repairs verified; harness executed verbatim and reproduced line-for-line; three LOW nits
recorded, none required.

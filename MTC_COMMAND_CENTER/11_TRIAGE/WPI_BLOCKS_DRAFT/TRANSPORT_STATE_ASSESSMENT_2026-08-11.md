# WP-I transport round-4 state assessment — 2026-08-11

## Assessment identity and method

- Gate-1 classification: **T2 — read-only documentation/evidence assessment**. No
  transport, block, wrapper, preregistration, QA, or status byte was modified.
- Round-3 accepted baseline: commit `78173bfd`.
- Current inspected HEAD: `df4bd0f182aef8aefad67c39b5cd00f43182d8f7`.
- Preservation commit: `cf049b6b978d811c2857862bf7ec4499f8fa6965`.
  Its message explicitly says the close-script edit was preserved from another
  session, was not verified or accepted, and had no accompanying QA or repair report.
- `git log 78173bfd..HEAD -- <the nine paths>` names only `cf049b6b`.
  `git diff --name-status 78173bfd..HEAD -- <the nine paths>` names only
  `remote_close_tree_wpi.sh`. The nine paths had no worktree modifications when this
  assessment began.
- Baseline identities below were computed from raw `git cat-file blob
  78173bfd:<path>` output; no checkout was used. Current identities were computed from
  the worktree bytes. No host or network contact occurred.

## Per-file identity and state

| File | Current bytes | Current SHA-256 | State against round 3 | Delta and scope mapping |
|---|---:|---|---|---|
| `transport_runner.ps1` | 57,826 | `13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4` | **Unchanged** | Byte-identical to `78173bfd`. Therefore no F1 operation-specific marker binding and no F4 per-branch prerequisite model exist. |
| `TRANSPORT_PLAN.tsv` | 7,219 | `2a1cd2a65d447526dee8748b17a762dfe85e88de686a8f7d337dff8830161650` | **Unchanged** | Byte-identical to `78173bfd`. All six `ssh_stdin` rows still use bare `bash -s --`; close ops 07/08 still pass two script arguments. F1 and T6 are not composed. |
| `remote_setup_wpi.sh` | 17,775 | `c0b7caa7f856db6b6d8aad4d407d42d450064a9e55a9cbbacf464f28e97b8d74` | **Unchanged** | Byte-identical to `78173bfd`. It does not establish a close-script `WORK_ROOT`. |
| `remote_extract_verify_wpi.sh` | 16,614 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` | **Unchanged** | Byte-identical to `78173bfd`; no round-4 scope item was applied here. |
| `remote_close_tree_wpi.sh` | 24,247 | `9ff2f1e02533769a7ad751eb2f3060c79a56a37aeca1707f0d32cc79c5969e53` | **Modified; unverified and non-operational** | Round-3 identity was 12,039 bytes / `fc183751c634c7fd6d1d9bd75143b7229357e52b7eec5f25a8eec0192bd1f75f`. The `+267/-62` delta attempts F1/F2/F3 and T6: launch-domain checks, exact absence classification, numeric identity, and a third `WORK_ROOT` argument with disjoint scratch. It has no matching plan/runner change, no R4 QA/status/report, and its launch-domain function check self-STOPs; details below. |
| `run_p0.sh` | 5,215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` | **Unchanged** | Byte-identical to `78173bfd`; T5 is absent. |
| `run_ro.sh` | 5,933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` | **Unchanged** | Byte-identical to `78173bfd`; T7 is absent. |
| `SELF_QA_TRANSPORT.md` | 100,406 | `84730522fd77b4a754d35556b740f6438a0bd0bc68e3d90340cb348b715c27da` | **Unchanged** | Byte-identical to `78173bfd`. It still records the old close identity at lines 261-263 and contains no F1-F4/T5-T8 R4 RED/GREEN evidence. |
| `STATUS_TRANSPORT.md` | 7,445 | `dfdf7fb931905e3f6404c14bb32dd3c93f0323c812dc5ae10c1fb3c9c2be23a7` | **Unchanged** | Byte-identical to `78173bfd`. It still says round 3 is repaired-pending-reaudit (line 3) and that program identity is the close script's only semantic delta (lines 53-60). |

There is no `TRANSPORT_REPAIR_R4_REPORT.md` in the current tree.

## Round-4 scope coverage

| Item | Honest status | Current-byte evidence and assessment |
|---|---|---|
| **F1 — pinned remote interpreter and correct marker family** | **Partially implemented** | The close script contains executable launch checks at `remote_close_tree_wpi.sh:89-129` and adds `/usr/bin/env` and `/usr/bin/bash` to its tool set at `:155-194`. This is only one of the six stdin programs, and the implementation self-STOPs at `:111-112`. The plan remains bare `bash -s --` for ops 01/03/04/05/07/08 (`TRANSPORT_PLAN.tsv:2,4-6,8-9`). The runner still accepts one global union of marker prefixes (`transport_runner.ps1:165-168,873-885`) rather than binding the expected family to the operation and stdin artifact. No wrong-family GREEN exists. |
| **F2 — run-owned scratch outside evidence** | **Partially implemented** | The close script requires `WORK_ROOT` at `remote_close_tree_wpi.sh:214-217`, binds it at `:237-260`, creates a disjoint work directory at `:338-380`, and no longer invokes `mktemp`. But no setup/plan byte establishes or passes that root; ops 07/08 remain two-argument calls. The code is therefore not part of an executable composition, and no TMPDIR RED/GREEN exists. |
| **F3 — mixed close probe error must STOP** | **Implemented but unverified** | `remote_close_tree_wpi.sh:269-312` calibrates one exact absence diagnostic, corroborates absence with `-e`/`-L`, and STOPs on multiline, mixed, or unequal diagnostics rather than using the old substring test. This is the requested code shape, but it is unreachable under the intended current launch because the earlier function check self-STOPs. `SELF_QA_TRANSPORT.md` is unchanged and provides no R4 mixed-diagnostic RED/GREEN, so this is not evidenced closure. |
| **F4 — per-branch/per-operation prerequisites** | **Not started** | `transport_runner.ps1` is byte-identical to round 3. It still has one global `$sequenceOk` (`:609`), passes its single snapshot into every operation (`:894,939-968`), and demotes every later `always` deviation through the same `cleanup_after_unestablished_prerequisite` arm (`:918-921`). There is no P0/RO branch state, no close/fetch/bind dependency chain, and no distinct `cleanup_after_earlier_deviation` reason. |
| **T5 — wire five `P0_ATTESTED_*` values** | **Not started** | `run_p0.sh:31-37` defines other P0 inputs, and `:106-107` exports them, but it defines/exports none of `P0_ATTESTED_USER_NS`, `P0_ATTESTED_MNT_NS`, `P0_ATTESTED_PID_NS`, `P0_ATTESTED_NET_NS`, or `P0_ATTESTED_ROOT_MOUNT_ID`. Current `RP6-P0.sh:675-689` requires all five. No composition test exists. |
| **T6 — make close contract, bytes, and plan agree** | **Partially implemented** | The close bytes now claim and encode classes 5 and 6 (`remote_close_tree_wpi.sh:3-55,89-129,214-217,237-380`), and the draft table describes them (`WPI_PREREGISTRATION_DRAFT.md:239,259-270`). The composition contradicts those claims: the plan/draft op table still uses bare `bash` and two arguments (`TRANSPORT_PLAN.tsv:8-9`; draft `:502-509`), the draft still says close retains `mktemp`/inherited TMPDIR (`:280-284`) and later says it differs only in class 2 (`:592-596`), and the clean launch self-STOPs. |
| **T7 — remove inert `WPI_INTERPRETER_TARGET`** | **Not started** | `run_ro.sh:45` still defines the pin and `:113-119` still exports it. Current `RP7-WPI-RO.sh` has no reference to that variable; its actual predicate constructs `<venv>/bin/python` and refuses a symlink at `RP7-WPI-RO.sh:979-1018`. |
| **T8 — current transport summary and F4 semantics** | **Not started** | No nine-file R4 document changed. The draft already carries the round-3 first-mismatch and per-kind grammar at `WPI_PREREGISTRATION_DRAFT.md:515-535`, but its cross-kind cleanup rule at `:537-544` is still the globally broad rule rejected by the Lead's F4 adjudication. It does not state per-branch prerequisites or the distinct cleanup reasons, and its op table still records the stale launch/argv contract. |

No scope item is **implemented and evidenced**. F3 is the only item whose isolated
predicate repair is present in complete-looking code, but D026 evidence and a reachable
composition are both absent.

## `remote_close_tree_wpi.sh`: what the edit actually does

### Derivation class 5 — present in text and code, but not viable

The code does attempt a clean launch-domain check: absolute Bash, no `BASH_ENV`, `ENV`,
or `TMPDIR`, fixed `PATH`/`LC_ALL`, a restricted exported-name set, and pinned
`/usr/bin/env` plus `/usr/bin/bash` (`remote_close_tree_wpi.sh:89-129,155-194`). It does
not produce a usable class-5 implementation:

1. `ld_stop` is defined at line 93.
2. Line 111 runs `LD_FUNCS="$(declare -F)"`.
3. Line 112 requires that result to be empty. It is not empty because it includes the
   script's own `ld_stop` function.

The exact current file passes `bash -n`, but the intended clean launch was driven locally
without network or host contact:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea \
  /usr/bin/bash --noprofile --norc remote_close_tree_wpi.sh \
  /tmp/evidence RUNID /tmp/work
CLOSE_STOP reason=launch_domain_inherited_shell_function
RC=3
```

Thus class 5 is syntactically present but deterministically refuses its own clean
execution. It also cannot close F1 for the other five stdin scripts; their plan rows still
select bare remote `bash`, and the runner still accepts an unrelated marker family.

### Derivation class 6 — coded locally, absent from the composition

The script genuinely removes `mktemp`, requires a third `WORK_ROOT`, proves canonical
two-way non-overlap with `EV_DIR`, creates `close_work_$RUNID` once at mode 0700, points
`TMPDIR` at it, and installs cleanup (`remote_close_tree_wpi.sh:214-217,237-260,338-380`).
That is a substantive partial implementation of class 6.

It is not an executable transport contract. Neither `remote_setup_wpi.sh` nor another plan
operation establishes the required run-owned root, and `TRANSPORT_PLAN.tsv:8-9` still
invokes the close script with only `<EV_DIR> <RUNID>`. The RUNID review's two-argument
observation is therefore **confirmed** against current bytes.

There is one further classification detail: if the class-5 self-STOP were repaired while
the plan remained unchanged, the argument-count arm at `remote_close_tree_wpi.sh:214`
calls `fail`, so the missing third argument would emit `CLOSE_FAIL` / rc 1, not STOP.
With an established branch the unchanged runner would count that as a host deviation.
In the exact current composition op 07 instead STOPs earlier at class 5, but for the wrong
reason. Either way, the close boundary cannot run as preregistered.

## Cross-checks from the independent reviews

### P0 attestation wiring

The finding is still true. `run_p0.sh` contains none of the five required
`P0_ATTESTED_*` names. Its only P0 exports are `P0_EXPECT_UID`, `P0_STATE_UID`,
`P0_STATE_GID`, `P0_FORBIDDEN_GIDS`, `P0_VENV_ROOT`, and `P0_TOOL_PINS`
(`run_p0.sh:31-37,106-107`). `RP6-P0.sh:675-689` STOPs when any of the five attested
inputs is missing and later requires equality with its frozen literals at `:717-736`.
T5 is wholly open.

### RO interpreter pin

The finding is still true. `run_ro.sh:45,118` defines and exports
`WPI_INTERPRETER_TARGET`, but current `RP7-WPI-RO.sh` never reads it. RP7 derives
`$WPI_VENV_ROOT/bin/python` itself and refuses a symlinked object
(`RP7-WPI-RO.sh:979-1018`). The wrapper pin is inert and T7 is wholly open.

## Ordered resumption list

1. **Lock the composition contract first.** Before editing individual files, specify one
   exact remote launch argv for every `ssh_stdin` row, the per-operation terminal marker
   family, the P0 and RO prerequisite graph, and the exact run-owned `WORK_ROOT` path,
   allocator, owner/mode, and lifetime. Every later code, plan, draft, and QA change
   depends on these decisions.
2. **Repair the close-script WIP against that contract.** Remove the class-5
   self-rejection; make unexpected/missing argv an inability-to-evaluate; retain and
   independently falsify the exact mixed-diagnostic STOP; ensure the selected
   `WORK_ROOT` is created before close and remains canonically disjoint; prove cleanup
   behavior instead of relying on the current ignored trap failure. This is the shared
   F1/F2/F3/T6 foundation.
3. **Compose the plan and launch domain.** Change all six stdin rows from bare `bash` to
   the frozen absolute `env -i`/Bash launch domain, pass the third close argument in ops
   07/08, and make the setup/allocation path establish that root. Recalculate the
   plan/runner pins only after the argv is final.
4. **Repair the runner on the final plan shape.** Bind each ssh operation to its own
   expected marker family and stdin artifact, then replace the global `$sequenceOk`
   cleanup snapshot with explicit P0-stage, RO-stage, P0-close/fetch, and
   RO-close/fetch prerequisites. Drive the decisive F4 case: ops 01-06 match, op 07
   `CLOSE_STOP`, op 08 genuine `CLOSE_FAIL` => RO deviation counted and final FAIL.
   Separately prove cleanup after a genuinely unestablished prerequisite remains STOP.
5. **Close the wrapper-only gaps.** Add and export the five `P0_ATTESTED_*` values in
   `run_p0.sh`, with the required real-block placeholder-present composition proof; remove
   `WPI_INTERPRETER_TARGET` from `run_ro.sh` and the fill ledger unless a separately
   accepted consumer is introduced.
6. **Reconcile the preregistration after executable semantics stop moving.** Update every
   affected section, not only the class table: the stale `mktemp` paragraph, all six
   remote launch argv, the third close argument, per-branch cleanup semantics, marker
   binding, fill manifest, and T8 summary. Remove every internal contradiction.
7. **Produce the missing evidence layer last.** Add literal D026 RED/GREEN commands and
   real output for F1-F4 and T5-T8, including PATH/BASH_ENV/wrong-marker, inherited
   TMPDIR, mixed diagnostic, the decisive cross-branch fixture, P0 composition, and inert
   pin absence. Then run `bash -n` on all five shell files, PowerShell 5.1 parsing on the
   runner, byte-counted CR checks, and fresh bytes/SHA-256 tables; update
   `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`, and the missing
   `TRANSPORT_REPAIR_R4_REPORT.md` before any T0 re-audit.

Plainly: round 4 is **not nearly done**. One of the nine files contains a substantial but
non-operational WIP edit covering parts of F1, F2, F3, and T6; eight files remain exactly
at the round-3 bytes, no R4 QA/status/report exists, and no one of F1-F4 or T5-T8 is both
implemented and evidenced. F4, T5, T7, and T8 are not started; F1, F2, and T6 are partial;
F3 has code but is unverified and currently unreachable.

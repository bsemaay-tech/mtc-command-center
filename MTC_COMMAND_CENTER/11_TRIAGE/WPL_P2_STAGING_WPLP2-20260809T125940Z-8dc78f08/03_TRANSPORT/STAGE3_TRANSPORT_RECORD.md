# WP-L Phase 2 — Stage 3 transport record (first host contact)

Unit: `WPLP2-20260809T125940Z-8dc78f08` · Lead session (Claude Fable 5), 2026-08-09 evening
Authority: owner authorization of Stage 3 (transport + B3 + R4-5) given this evening;
`OVERNIGHT_HANDOFF_2026-08-09_STAGE3.md`. Zero service mutation, zero ARM — held.

Result: **TR_RUN FAIL — first-FAIL engaged at op 05 (B3, rc=3 STOP).** Transport and
verification (ops 01–04) all PASS. B3 stopped on an unprivileged-probe error, not on
deviant host state. R4-5 (op 07) was skipped as a consequence and never ran. See
`B3_STOP_ADJUDICATION.md` for the Lead adjudication and disposition.

## Preflight (operator-side, before any connection)

- All 13 `PREREG_SHA256SUMS.txt` entries re-verified bit-identical, including
  `TRANSPORT_PLAN.tsv` `0850f24f…` and `transport_runner.ps1` `c5bdb47c…`.
- `runkit.tar` re-verified `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53`.
- Record root `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` absent
  (create-once satisfied); SSH identity present; host key for `172.24.55.233` present in
  `known_hosts` (ed25519/rsa/ecdsa); VM `GATEA-STAGING` Running (uptime 7d15h); TCP 22 open.
- Dry run (`transport_runner.ps1` with no flags): 12 ops planned, argv byte-identical to
  PREREGISTRATION.md §5, `TR_DRY_RUN no_process_was_started no_connection_was_opened`.
- Power continuity for the overnight session verified: `powercfg` STANDBYIDLE=0 and
  HIBERNATEIDLE=0 on both AC and DC (last night's sleep-kill fixed and confirmed).

## Execution (`-Execute -Confirm WPLP2-20260809T125940Z-8dc78f08-EXECUTE`)

| op | kind | rc | expect | outcome |
|---|---|---|---|---|
| 01 | ssh remote_setup.sh | 0 | 0 | four create-once dirs allocated, owner/mode asserted |
| 02 | scp runkit.tar up | 0 | 0 | archive uploaded |
| 03 | scp R4_5_runner.py up | 0 | 0 | runner uploaded |
| 04 | ssh remote_extract_verify.sh | 0 | 0 | `EXTRACT PASS … members=9 verified=9 executed=0`; archive re-hashed `618f7640…` remotely; all nine block hashes bit-identical to §3 |
| 05 | ssh run_b3.sh | **3** | 0 | **B3 STOP** — `RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot statx '/etc/mtc-bridge/mtc-bridge.env': Permission denied`. First-FAIL engaged. |
| 06 | ssh remote_close_tree.sh (B3) | 0 | 0 | `CLOSE PASS … files=1 wrote_into_evidence_tree=0`, digest set stable across 2 passes |
| 07 | ssh run_r45.sh | skipped | 0 | `prior_op_did_not_produce_its_preregistered_rc` |
| 08 | ssh remote_close_tree.sh (R45) | 1 | 0 | `CLOSE_FAIL reason=evidence_dir_absent` — expected consequence: R45 never allocated its leaf |
| 09 | scp B3 evidence down | 0 | 0 | `b3.log` retrieved |
| 10 | scp R45 evidence down | 1 | 0 | `No such file or directory` — same consequence |
| 11 | local_bind B3 | 0 | 0 | **TR_BIND_PASS files=1**; remote `CLOSE_DIGEST_SET_SHA256 b25612df80dbca41c617ba24eb294bfb8fcbfdf9c2d45beb0094c007577d830c` reproduced bit-identical locally; `b3.log` = `079d6ac9…`, 1784 bytes |
| 12 | local_bind R45 | 3 | 0 | `remote_digest_set_empty` — same consequence |

The B3 evidence tree is therefore **closed, retrieved and bound** (remote and local
digest sets equal name-for-name, digest-for-digest, and the digest-set rendering
reproduces the remote set hash). Every op's argv, stdout, stderr and rc are preserved
under `operator_record/` (copied bit-identical from the create-once record root, which
also remains untouched at `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08`).

One committed-copy exception: `operator_record/evidence/…-B3/b3.log` is excluded from
git by the repo guard's log-file rule. Its bytes stay preserved at the record root and
in the copy on disk; its identity is bound above (`079d6ac9…`, 1784 bytes, digest-set
`b25612df…`) and in `operator_record/TRANSPORT_SHA256SUMS.txt`.

## What B3 proved before stopping

From the bound `b3.log` (evidence, not narration):

- `/opt/mtc-bridge/releases/2ce41e34…321b` — `root:root` mode `555`; full `-perm /222`
  sweep finished in 0 s inside the 120 s budget; **no write bit anywhere in the tree**.
- `/opt/mtc-bridge/venvs/2ce41e34…321b` — same result: `root:root 555`, clean sweep.
- `/var/lib/mtc-bridge` and `/var/log/mtc-bridge` — `mtc-bridge:mtc-bridge 750`;
  `/etc/mtc-bridge` — `root:root 750`. All as recorded in the post-gate inventory.
- Predicted outcomes #1, #2, #3 of PREREGISTRATION.md §8 **held**. The stage stopped at
  the §8 #4 probe (env file) — on permissions, not on the name risk that was preregistered.

## Safety state after Stage 3

- Service stop/start/enable/mask, reboot, rollback, unit write, chmod/chown of host
  objects outside the run's create-once tree: **none**.
- Credential read, ARM, order, broker/exchange, TESTNET/mainnet contact: **none**.
- Blocks executed remotely: RP1-B3 only (read-only probes), via the accepted RP0
  bootstrap. RP3/RP4/RP5 blocks verified but never sourced. C1/C2/C3/C4/C5: not run.
- RUNID `…-B3` **burned** (allocation succeeded, stage stopped). RUNID `…-R45` **burned
  by policy** (its op sequence is spent and the record root is create-once; §11 requires
  a fresh preregistration for any retry — see `04_PREREG_R45B/`).

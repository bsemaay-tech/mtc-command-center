# KICKOFF — Stage 2B preregistration (re-frozen kit, repaired B3)

Authorized private-repo test-infrastructure work. You are the implementer writing an
immutable preregistration for ONE read-only staging check. Writing this document is NOT
an authorization to transport or run: it produces the plan and the operator artifacts.
The Lead performs the transport separately. Write ONLY into this directory
(`08_PREREG_B3B/`). ASCII only. English only. No host contact of any kind — no ssh, no
scp, no TCP probe. No git mutation.

## What changed and why this document exists

The previously frozen run-kit carried an old `RP1-B3.sh` whose env-file and
install-manifest checks were structurally impossible for an unprivileged operator (the
recorded gap `B3-GAP-ENV`: `/etc/mtc-bridge` is `0750 root:root`, so `stat` on any name
under it returns EACCES for the login user). That block went through a full repair and
adversarial audit cycle and the repaired design was accepted. The kit was re-frozen.

Because block digests and the archive digest changed, the earlier preregistration is
VOID for this kit. This is its replacement, covering the repaired B3 only.

## Pinned facts (use exactly these; do not re-derive)

- Archive: `../07_RUNKIT_B/runkit_b.tar`, 184320 bytes, sha256
  `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`, 10 members.
- Per-block digests and provenance: `../07_RUNKIT_B/BLOCK_IDENTITIES_B.tsv` (read it;
  reproduce the table in your document).
- Repaired block to execute: `RP1-B3.sh` sha256
  `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc` (662 lines),
  superseding `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af`.
- Route: `gatea@172.24.55.233`, identity
  `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`, options pinned on every op:
  `-o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20`.
- Preregistered inputs the repaired block requires (see its own guard block — read the
  script and take the exact variable names from it): the sweep budget, and the numeric
  service uid/gid the repaired design now demands instead of name-based ownership. For
  the service uid/gid use `<PIN-BEFORE-EXECUTE>` and state in the document that the Lead
  fills them from the recorded host inventory before execution, because a wrong
  preregistered value would produce a false FAIL.
- New unit id: `WPLP2B-<ALLOCATE-AT-DISPATCH>`; RUNID `…-B3B`; remote base
  `/home/gatea/wpl_p2b_staging_<unit>`; operator record root
  `C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_<unit>`. These MUST NOT collide with the existing
  `wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08` tree or the two existing record roots.

## Inputs (read these, nothing else)

- This file.
- `../02_PREREG/PREREGISTRATION.md` — the accepted rigor template. Match its section
  structure and discipline.
- `../02_PREREG/TRANSPORT_PLAN.tsv`, `../02_PREREG/transport_runner.ps1`,
  `../02_PREREG/remote_setup.sh`, `../02_PREREG/remote_extract_verify.sh`,
  `../02_PREREG/remote_close_tree.sh`, `../02_PREREG/run_b3.sh` — the accepted operator
  artifacts you are adapting.
- `../07_RUNKIT_B/BLOCK_IDENTITIES_B.tsv`, `../07_RUNKIT_B/STAGE1B_RECORD.md`.
- `../07_RUNKIT_B/RP1-B3.sh` — the block that will execute; read it to get its exact
  required inputs, its rc contract, and its real failure/stop reasons.
- `../03_TRANSPORT/B3_STOP_ADJUDICATION.md` — what went wrong last time.

## Deliverables (into `08_PREREG_B3B/`)

1. `PREREGISTRATION_B3B.md` — same sections as the template: run identifiers and
   evidence tree; preregistered inputs; block digest table (all ten, with provenance);
   support-script hashes; exact remote argv per op; operator-side evidence contract;
   closing/binding rules; **expectation table with the exact predicted first divergence
   per check, taken from the repaired block's real reason strings**; what is deliberately
   NOT preregistered; immutability/void rules; safety state at the moment of writing.
   The expectation table must cover the repaired block's NEW arms too: the EACCES
   boundary probe (pass arm), a visible env file (FAIL), ENOENT (FAIL — search
   permitted), ambiguous/multi-line diagnostics (STOP), and the three deferred checks
   that now emit `B3_deferred` lines instead of executing.
2. `TRANSPORT_PLAN_B3B.tsv` — same 9-column header and semantics as the accepted plan.
   Ops: create-once allocation; upload `runkit_b.tar`; remote extract+verify against the
   new archive digest and the ten member digests; run repaired B3; close the evidence
   tree (run_when `always`); fetch it (`always`); local bind (`always`). Every op
   `expect_rc = 0`; first-FAIL semantics identical to the accepted runner.
3. `run_b3b.sh` — the wrapper delivered on ssh stdin. Adapt the accepted `run_b3.sh`:
   pin every artifact it verifies to the NEW digests, refuse symlinks, export exactly
   the inputs the repaired block requires, source RP0-LIB and RP0-BOOTSTRAP from the
   extracted kit after verifying their hashes, and keep the 0/1/3 rc contract. `bash -n`
   it and record the result.
4. `remote_setup_b3b.sh`, `remote_extract_verify_b3b.sh`, `remote_close_tree_b3b.sh` —
   adapted from the accepted ones for the new paths/digests. Where an accepted script
   needs no change beyond its arguments, keep it byte-identical and say so explicitly.
5. `transport_runner_b3b.ps1` — adapted from the accepted runner: pin the new plan
   sha256, new record root, new confirm token `<unit>-B3B-EXECUTE`, dry-run default,
   create-once record root, per-op argv/stdout/stderr/rc capture, local bind.
6. `PREREG_B3B_SHA256SUMS.txt` — sha256 of every file you produced.
7. `SELF_QA_B3B.md` — every verification you ran with its exact command and real output:
   `bash -n` on each script, the archive/block digest re-verification, a demonstration
   that the runner's dry run prints the plan and opens nothing, and a check that no new
   path collides with the existing unit's paths.

## Hard constraints

- **Read-only staging check only.** No service stop/start/enable/mask, no reboot, no
  rollback, no unit write, no chmod/chown outside the run's own create-once tree.
- **Do not preregister C1, C2, C3, C4, C5, or RPD-VERIFY execution.** RPD-VERIFY is
  root-side and stays design-only: no root, no sudo, no privilege escalation is
  available or authorized. List them under "NOT preregistered" with their blockers.
- No credential read, no ARM, no orders, no broker/exchange, no TESTNET/mainnet, no
  master merge.
- The runner's default mode must be a dry run requiring both an explicit execute switch
  and the exact confirm token.

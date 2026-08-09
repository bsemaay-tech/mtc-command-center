# WP-L Phase 2 — staging unit closure record

Unit `WPLP2-20260809T125940Z-8dc78f08` (plus its re-frozen successor
`WPLP2B-20260809T210610Z-834380c5`), branch `feature/donchian-crypto-ladder`,
2026-08-09 → 2026-08-10 overnight. Lead: Claude Fable 5. Implementation and audit were
delegated throughout; the Lead orchestrated, verified, adjudicated and committed.

**Status: the unit's executable scope is CLOSED.** Both checks that were ever authorized
to run have run and PASSED on the real host. Everything still open is open for a stated
reason, not for want of effort.

## 1. What was achieved

| Item | Outcome | Evidence |
|---|---|---|
| Stage 1 run-kit freeze | 9 blocks, archive `618f7640…` | `01_RUNKIT/` |
| Stage 2 preregistration | complete, Lead-verified | `02_PREREG/` |
| Stage 3 transport | ops 01–04 PASS; 9/9 blocks verified remotely | `03_TRANSPORT/` |
| **B3 (original)** | **STOP rc 3** — design gap `B3-GAP-ENV` | `03_TRANSPORT/B3_STOP_ADJUDICATION.md` |
| **R4-5** | **PASS** — RP4-C3 symlink guard proven load-bearing | `05_TRANSPORT_R45B/` |
| B3 repair cycle | 6 rounds × 6 audits → **ACCEPTED** | `06_B3_REPAIR/` |
| Stage 1B re-freeze | 10 blocks, archive `888bec17…`, deterministic | `07_RUNKIT_B/` |
| Stage 2B preregistration | committed before execution | `08_PREREG_B3B/` |
| **B3 (repaired)** | **PASS on the host** — gap closed | `09_TRANSPORT_B3B/` |

## 2. The two substantive results

**R4-5 — a guard proven load-bearing.** The RED arm (the two-line
`dst_path.is_symlink()` guard deleted, delta proven unique file-wide) followed a dangling
symlink and wrote a real SQLite database *outside* the restore root. The GREEN arm
(accepted bytes) raised exactly the predicted `restore destination is a symlink` and left
the target absent. This is the one fixture that could not close on Windows; it closed on
Linux under a fresh one-use RUNID. Guard-scope claim only — C3 itself stays BLOCKED.

**B3 — a design gap found, repaired, and closed on the host.** The accepted block assumed
an unprivileged operator could `stat` inside `/etc/mtc-bridge` (`0750 root:root`). It
cannot; the stage STOPped on first host contact. The repair moved the env-file and
manifest-binding admission to a root-side block and replaced it, in the unprivileged path,
with an EACCES boundary falsification that is stronger than what it removed: a successful
`stat` is a FAIL, ENOENT is a FAIL (it would prove search succeeded — the host more open
than accepted), and only EACCES passes. The repaired block then PASSED on the host:
release and venv trees `0:0` mode `555` with clean any-write-bit sweeps, state and log
directories numerically `999:988`, conf dir canonical, unmounted, caller not in its group,
search denied on both probe names, and three checks explicitly *declared* deferred rather
than silently dropped.

## 3. What the adversarial cycle actually bought

Six audit rounds produced findings no self-review had caught, each with a concrete failure
scenario the auditor reproduced:

- `grep -qsF` binding checks defeated by a nested-decoy or duplicate-key JSON manifest.
- The root-side verifier reachable through a symlinked `/etc/mtc-bridge` parent.
- Name-based ownership (`root:root`) spoofable via an NSS mapping; `id -u = 0` proving only
  namespace-local root.
- The shared path probe creating temp files while the header claimed no mutation.
- ENOENT misrouted to STOP when it is positive evidence of a deviation.
- An unguarded `tr` able to leak a raw exit status through the 0/1/3 contract.
- After the fixes: a PYTHONPATH-shadowed `json` module returning a false "bound", `NaN`
  accepted as JSON, an unterminated final mount record skipped, an ambiguous two-line
  diagnostic selecting the pass arm.

The final code was accepted only when the auditor pasted the QA's prerequisite and four
closure blocks verbatim into a fresh shell and every one reproduced its recorded transcript.

## 4. Method notes worth keeping

- **A STOP is not a FAIL.** Every audit round turned on this. An unevaluable check that
  reports FAIL accuses a correct host; the whole B3 gap, and both HIGH findings later
  raised against the WP-I draft, are instances of exactly this confusion.
- **Preregistration must precede execution provably.** Both preregistrations were committed
  before their first invocation, so the ordering is checkable from git history rather than
  asserted in prose.
- **A manifest cannot attest to its own acceptance.** The same principle blocked the naive
  fix for the numeric service identity: `install.sh` allocates the account dynamically, so
  reading the uid off the host and then asserting the host matches it would be vacuous. The
  deployment contract is the *name*; a recorded `getent` probe resolved it to uid 999 /
  gid 988 — which differ, so the plausible `999:999` guess would have been wrong.
- **Freezing is not editing.** A repaired block could not be patched into the frozen kit;
  the kit was rebuilt with declared provenance per block, and the old preregistration was
  explicitly voided rather than reused.

## 5. Still open, with reasons

- **`RPD-VERIFY.sh`** — accepted, in the kit, hash-verified on the host, **never executed**.
  It is root-side and no root, sudo, group or ACL change is granted. Design-only until the
  owner opens a privileged channel. The three checks B3 defers land here.
- **C1, C2-A/B, C3, C4-A/B/C, C5** — BLOCKED throughout; never preregistered, never run.
  Their blockers are recorded in the accepted designs, unchanged by this unit.
- **WP-I** — draft at round 1.2 (Codex audit applied by GLM). F3/F4 (system-manager access)
  remain OPEN. Not dispatchable: it needs explicit host-contact authority and a budget lift.
- **The `bridge.env` naming risk** — raised in the Stage 2 preregistration as a named risk.
  It remains *unresolved, not triggered*: EACCES is name-independent, so no unprivileged
  block can settle it. It resolves only through RPD-VERIFY.

## 6. Safety state across the whole unit

Zero service stop/start/enable/mask, zero reboot, zero rollback, zero unit write, zero
chmod/chown outside each run's own create-once tree. Zero credential read, zero ARM, zero
order, zero broker/exchange contact, zero TESTNET/mainnet, zero master merge, zero
WP-V/KVM2, no payload-archive deletion, no host reprovisioning. The bridge stayed DISARMED,
credential-free and loopback-only. RUNID ledger: `-B3` burned (STOP), `-R45` burned (never
allocated), `-R45B` consumed (PASS), `-B3B` consumed (PASS).

## 7. Ledger

Booked prospectively: Stage 1+2 unit 0.8 h; Stage 3 + 3B 0.4 h; the overnight design,
repair, audit and re-freeze block 1.4 h. Running total for this unit **2.6 h** against the
ratified balance (29.5 h at WP-L P2 start), leaving **~26.9 h**. No retroactive
reconstruction; the owner may adjust at ratification.

Delegation split: Claude Max implemented rounds 1–6 and the re-freeze build; Codex
`gpt-5.6-sol` audited every round and wrote the Stage 2B preregistration; GLM-5.2 reviewed
the Audit-2 checklist and the WP-I draft and applied the WP-I repair. From the owner's
routing amendment onward, all new work went to Codex and GLM.

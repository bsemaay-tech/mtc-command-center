# Deploy path synthesis — what actually stands between here and a KVM2 first start — 2026-08-15

Lead synthesis over three lanes completed tonight: the Bridge readiness refresh
(`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md`), the freeze-blocker
reconciliation (`AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md`),
and the Packet 10 provisional baseline.

Finish line assumed throughout: **one hardened bridge service on KVM2, first
start DISARMED, TESTNET-only, loopback-only.** No ARM, no mainnet, no dashboard,
no AI lab.

## 1. The deploy is downstream of the whole WP-I chain, not parallel to it

This is the fact that most changes the schedule, and it is easy to misread.

`GLOBAL_HANDOFF.md:544-549` records the canonical plan sequence verbatim:

```text
3 one named expendable Ubuntu staging action
4 Audit 2 after WP-L Phase 2 + WP-I staging verification
5 WP-A on the retained host
6 discard host only after WP-A evidence
7 freeze final exact SHA/artifact
8 Audit 3 Gate-5 + Gate-6
9 Gate B
10 WP-V only after deployment approval
11 Gate C
```

The deployment gate is step 9. Every WP-I, Audit-2 and WP-A item sits in front of
it. So the Bridge checklist's own 27-47 hour critical path is **not** the total —
it is the tail of a longer chain, and its first row (the Pathscope decision) is
the same blocker the WP-I lane is stopped on.

## 2. The accepted Gate-A candidate is stranded on an unmerged branch

The Bridge lane reported that staging-accepted candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b` is not an ancestor of this checkout.
That framing understates it, and the Lead re-derived the load-bearing version:

```text
git merge-base --is-ancestor 2ce41e34 origin/master  -> rc=1  (NOT an ancestor)
git merge-base --is-ancestor 2ce41e34 master         -> rc=1  (NOT an ancestor)
git branch -a --contains 2ce41e34
  codex/gate-a-disarmed-start-mode
  remotes/origin/codex/gate-a-disarmed-start-mode
```

Not being an ancestor of `C:\R7FINAL` is expected — this is a WP-I documentation
branch and was never a deploy source. The real finding is that `2ce41e34` is not
in `origin/master` either. It exists only on `codex/gate-a-disarmed-start-mode`.

That is consistent with its own acceptance record, which granted staging
acceptance only and explicitly no merge authority
(`GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8, 56-65`). Nothing went wrong. But the
consequence is concrete and expensive: **the Gate-A A-0..A-9 pass cannot be
carried to any current release candidate.** The current mainline deployment
assets differ from the accepted ones, and the current systemd template still
starts a bare `python -m bridge.app` with no `credential_free_disarmed` mode
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:29-43`),
whereas the accepted staging run proved exactly that mode with a loopback
listener, DISARMED API, no broker attempt, and application-level ARM refusal
(`GATE_A_A4_PASS_2026-08-08C.md:38-54`).

So the release-candidate work in checklist item 1 is not "commit what exists". It
is: bring the accepted Gate-A behaviour into the release line, and re-earn the
acceptance on the new bytes.

## 3. Nothing on the ten-item checklist is closable by local work alone

The Bridge lane's `LOCAL-CLOSABLE` roll-up is empty, and its reasoning holds:
items 1, 4, 5 and 10 end at owner gates; items 2, 3, 6, 7, 8 and 9 need exact-SHA
evidence produced on a real Ubuntu host. Local work still exists in quantity —
it is just always a component of a mixed item, never a whole item.

The corollary for autonomous sessions: **local-only nights cannot close a deploy
checklist item.** They can only make the next gated step cheap.

## 4. Assembled estimate

Hands-on hours for a competent implementer. Not calendar time, not queue time,
not audit-quota wait. Assumes Pathscope Option C, the Lead recommendation.

| # | Stage | Hours | Kind | Source |
|---:|---|---:|---|---|
| 1 | Pathscope disposition implemented and accepted | 6-10 | local + audit | decision-options record |
| 2 | Stage-1 allocation, Commit-1 attestation, fills, Commit-2 freeze | 7-14.5 | local, one host step | freeze-blocker reconciliation §3 |
| 3 | WP-I staging execution and closure | 4-8 | host | not separately priced; bounded estimate |
| 4 | Pre-WP-A checkpoint freeze + ledger ratification | 2-4 | local + owner | prerequisites gates 5-6 |
| 5 | Audit 2 — two fresh flagships, allowing one repair round | 6-12 | audit | acceptance matrix, T0 roster |
| 6 | WP-A on the retained host | 4-8 | host | canonical sequence step 5 |
| 7 | Freeze final exact SHA/artifact + Audit 3 (Gate 5 + Gate 6) | 6-12 | local + audit | canonical sequence steps 7-8 |
| 8 | Release integration, exact-SHA freeze, full matrices | 12-20 | local | Bridge refresh row 2 |
| 9 | Owner decisions and secret provisioning | 0.9-1.5 | owner | Bridge refresh rows 1,3,7 |
| 10 | KVM2 baseline, install, verify, backups, rollback, monitoring | 5-10 | host | Bridge refresh rows 4-5 |
| 11 | Single-writer cutover + one DISARMED first start | 2.5-5 | host | Bridge refresh rows 6-7 |
| | **Total** | **55.4-105** | | |

Rounded honestly: **55 to 105 hours, centred near 75.** The spread is not
padding. It is the difference between audits passing first time and the
repair-and-re-audit pattern this project has produced repeatedly — including
four consecutive times on Pathscope alone.

Split by who does it: roughly **31-56 h local**, **8-12 h audits**, **15-31 h on
hosts**, **1-1.5 h of Barış's own time**.

If Barış picks Pathscope Option B instead of C, subtract about 5-8 hours from row
1 and accept the recorded loss of that safety proof.

## 5. What this changes about how to spend nights

Three of the eleven rows are pure local work that no gate blocks today: row 8's
release integration, the two test repairs found in Packet 10, and row 4's
documentation. Those are the honest targets for unattended sessions. Everything
else waits on a Barış sentence or on authorized host access.

## Boundaries

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action
was authorized or performed. Every estimate above is planning material, not
evidence, and no gate is opened by it.

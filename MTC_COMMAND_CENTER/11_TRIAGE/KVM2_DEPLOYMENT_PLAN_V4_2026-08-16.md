# KVM2 deployment plan V4 — replacement candidate `be689537` — 2026-08-16

Status: **PLAN — NOT AUTHORIZED TO EXECUTE. SUPERSEDES V3.** V4 **incorporates
V2 §0–§8 and V3 §D1–§D4 by reference as amended below; neither V2 nor V3 has
independent authority.** This version implements every DEFERRED-TO-PLAN item
from the round-1 T0 verdicts (`T0_KVM2PLANV3_CODEX_VERDICT_2026-08-16.md`,
`T0_KVM2PLANV3_CLAUDE_VERDICT_2026-08-16.md`) and re-pins the package around
the owner-approved replacement initial-release candidate. Round accounting:
this plan + its fresh T0 pair = **round 2 of the un-reset Plan-V3 T0 cap
(3)**, per `OWNER_DECISION_STATUS_PATCH_2026-08-16.md`.

## 1. Exact identities (all re-pinned)

| Item | Value |
|---|---|
| **Replacement initial-release candidate** | `be68953787c299bdaf30f83f301aa66a8ec0ea1f` — tip of `integration/bridge-release-20260815` (pushed), direct child of the previously accepted `62bf661b…`. KVM2 is empty and untouched; this REPLACES the initial-release candidate before any deployment — it is not an upgrade performed anywhere. |
| Candidate delta vs `62bf661b` | 11 files, +350/−77: owner-approved status patch (`/api/status` adds `host_identity`, `release_sha`, `service_start_ts`, per-response `status_ts`, `service_health`; System panel renders all five), `assert_ufw_bridge_safe` multi-tenant firewall predicate, complete dry-run mutation manifest (31 IDs), unit `MemoryHigh=768M`/`MemoryMax=1G` + `MTC_BRIDGE_RELEASE_SHA=@RELEASE_SHA@`, honest bounded logrotate (rotate 7, `maxsize 64M`, two named logs), genuinely read-only `verify.sh` (zero temp writes), non-mutating venv preflight. |
| Candidate test state | Full suite `1367 passed, 1 warning` — implementer run 183.59 s AND Lead-independent run 163.40 s. D026 RED/GREEN for all 11 new/extended regression arms recorded in `RIC1_IMPLEMENT_REPORT` (committed alongside this plan). |
| Payload | built from the clean worktree at `be689537`; `RELEASE_SHA256SUMS` sha256 `58705d925c0a2488347f0b6206bb0e75cc130ae704c5cb52ffc4f945891a8a24` |
| Launcher | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` **v2** — 9008 B, sha256 `e6e8bfa4217b05b0b134018175c082186b6fcbcb5c66d0cfbfa7ed84c2e1675c`. Fixes all round-1 launcher findings: EAP-safe native capture, agent rc-2/rc-1 distinction, real `ssh-keygen -F` pin check, intended-key fingerprint match (public file only), `-F NUL` + `IdentityFile=NUL` + proxy disabled + isolated known-hosts, child monitored through readiness with real exit-class reporting, try/finally lifetime ownership. |
| Host / access | unchanged: `srv1856225` = `152.239.123.231`, `baris`, pinned host key, owner-loaded agent |
| Old pins retired | candidate `62bf661b` payload (`1078ac22…`) and launcher v1 (`9c9beaeb…`) are superseded and must not be installed. |

## 2. Deferred-item repairs (the six from round 1)

**2.1 (Codex R7 + Claude R6) D3-5/D3-6 evidence spec — independent observation.**
D3-5 and D3-6 no longer accept application-log absence as proof. Required
evidence set:

- D3-6 refusal arm: the request is made from the DASHBOARD's own ARM control
  (well-formed by construction: current `X-Confirm = state_version`), and the
  recorded result MUST be HTTP **409** with the exact detail
  `ARM unavailable in credential-free DISARMED start mode; exchange access is
  disabled` — a stale-confirm 409 does NOT satisfy the row.
- Before/after `/api/status`: `state=DISARMED` and **unchanged
  `state_version`**.
- Independent side-effect observation for D3-5 and D3-6: host-side
  `ss -ntu` (all sockets) captured immediately before, during, and after the
  refusal attempt, plus `journalctl -u mtc-bridge-first-start` for the same
  window — the socket table must show no non-loopback connection from the
  service at any capture, observed by the operator session, not asserted by
  the application. Disclosure: this observes the attempt window, not every
  future instant; continuous egress enforcement remains a future item.

**2.2 (Codex R8) Rollback rehearsal — exact inputs and honest description.**
The stage-3 rehearsal runs `rollback.sh` with its mandatory inputs stated:
the state-manifest input is the freshly captured hash record of the (empty)
`/var/lib/mtc-bridge` state produced during stage-3 backup (§V2-5.3) — exact
command recorded in the execution record before running. The rehearsal IS NOT
a no-op: it writes/replaces `/etc/mtc-bridge/rollback_manifest.json` (inside
the Bridge boundary) and this write is authorized by §9. **Partial-install
disposition:** if the one bounded install fails at any point, the operator
(a) stops, (b) captures the dry-run-manifest-keyed list of mutations already
performed, (c) removes exactly those artifacts per the §7 enumeration under
the same §9 authority, (d) re-verifies the host equals the inventoried clean
baseline, and (e) reports; ANY retry needs a new owner sentence.

**2.3 (Claude R5) Citation hygiene.** This plan cites the owner requirement
record `OWNER_REQUIREMENT_DASHBOARD_2026-08-16.md` by its section list (items
1–8 as recorded there) and the multi-tenant record
`OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md` §2 items 1–12
separately. Reviewers verify against those records, not against V3's
renumbering.

**2.4 (Claude R7) Authority structure.** Stated above: V4 incorporates
V2/V3 by reference with no independent authority, and §9 below enumerates its
own action scope in full — the owner can read the sentence alone.

**2.5 (resource wording) Honest resource policy.** The Bridge tenant budget
is enforced as: unit `MemoryHigh=768M` (throttle) and `MemoryMax=1G` (hard
kill boundary); logs rotate at `maxsize 64M` with 7 retained generations per
log (two logs ⇒ policy-bounded retention ≈ 1 GiB worst case at rotation
points; scheduled logrotate is not a hard quota and between-run growth is
bounded only by disk monitoring §V2-5.4). The prior "logs capped at 64 MiB"
claim is retracted. Disk budget ≤10 G stands as a monitored, not enforced,
bound.

**2.6 (D3-4 now provable).** D3-4's five display legs are now real candidate
capabilities (fields + System-panel rendering, tested RED/GREEN). D3-4 wording
unchanged — the owner refused relaxation, and none is needed.

## 3. §9 — the single authorization ask (present ONLY after both fresh T0 verdicts accept)

> "I authorize the one-attempt masked DISARMED installation of exact
> replacement release `be68953787c299bdaf30f83f301aa66a8ec0ea1f` onto
> Hostinger KVM2 (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md —
> that is: payload transfer, dry run, one bounded install, read-only
> verification, and Bridge-scoped operational evidence (rollback rehearsal
> including its rollback-manifest write, Bridge-scoped backup/restore,
> monitoring baseline, tenancy re-inventory), all inside the Bridge tenancy
> boundary of V2 §0. No service start, no enable, no secret, no firewall
> change, no TESTNET/mainnet, no broker, no ARM, no orders, no action on
> reserved Hermes/web identities, no public exposure of port 8790 ever. The
> dashboard verification matrix D3 runs only after my separate first-start
> sentence. A failed attempt stops, restores the clean baseline per plan
> §2.2, and reports; any retry needs a new sentence."

## 4. Review contract for the fresh T0 pair (round 2)

Subjects: THIS file + launcher v2 + candidate `be689537` (they verify the
candidate delta against the owner-approved scope, re-run the full suite, and
check every round-1 REQUIRED is closed on mechanism — Codex R1–R10, Claude
R1–R7 — plus the six §2 repairs). Round 2 of cap 3; one round remains after
this. No KVM2 contact by reviewers.

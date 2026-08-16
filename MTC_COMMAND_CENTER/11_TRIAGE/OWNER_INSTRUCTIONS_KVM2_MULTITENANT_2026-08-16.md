# Owner instructions — chain-lane pause + KVM2 multi-tenant requirement — 2026-08-16

Recorded by the Fable 5 Lead from two owner chat messages received mid-session,
2026-08-16 afternoon. Both are binding immediately.

## 1. Two-commit-chain lane — PAUSED by owner cap ruling

Owner ruling, recorded as adopted: **V2 already consumed the T1 two-round
cap.** The Lead's "V3 is a fresh cycle" reading is rejected. Consequences,
applied same hour:

- The in-flight V4 repair lane was **stopped** (Codex dispatch killed; its
  38-byte partial output quarantined to `C:\tmp\lane_out\quarantine\`, never
  used).
- The completed V3 round-1 review
  (`WPI_PREREG_DRAFT_ROUND1/TWO_COMMIT_CHAIN_V3_REVIEW_R1_2026-08-16.md`) is
  reclassified **SUPPLEMENTAL ONLY** — not an audit round of record, not
  acceptance input.
- No further V3/V4 repair or review may start unless the Lead first
  demonstrates AND records a genuinely new Gate-1 scope, or the owner grants
  an explicit cap waiver in chat.
- **V3, and any closure that depends on it, must not be treated as accepted.**
  Checked: the gate-2 re-derivation
  (`AUDIT2_READINESS_PACKAGE/AUDIT2_GATE2_REDERIVATION_2026-08-16.md`) rests
  on RP6/RP7/transport/SEC102/Pathscope records only — the chain design is a
  gate-3 item and is cited there solely under "what this does NOT change", so
  gate 2 stands. The Stage-1 freeze (gate 3) is now blocked at the owner
  boundary: chain design has NO accepted version (V2 cap-exhausted
  REQUEST_CHANGES; V3 unaccepted, its review supplemental).
- KVM2 read-only inventory is COMPLETE and must not be repeated.

## 2. KVM2 is a future multi-tenant host — permanent requirement

The Hostinger VPS (`srv1856225`) will later also host a **Hermes agent** and
the owner's **websites**. The Bridge deployment plan must be revised BEFORE
its T0 review so the first installation is compatible with that future:

1. Do not install Hermes or websites now.
2. Bridge fully self-contained: own Linux user, directories, Python
   environment, service, logs, backup and rollback boundary.
3. No global Python packages, no shared application directories.
4. Reserve separate future locations and identities for Hermes and websites.
5. Bridge stays loopback-only on 8790; never exposed through the future
   website reverse proxy.
6. Ports 80/443 remain available for future websites. "SSH-only" is the
   present firewall state, not a permanent requirement.
7. No host-wide security change that would prevent future Docker, Node.js,
   reverse proxy, Hermes, or website services.
8. Backups, monitoring, log rotation, rollback: service-specific.
9. Bridge rollback/removal must never delete, stop, reconfigure or inspect
   future Hermes/web files, users, containers, services, ports or data.
10. Record CPU/RAM/disk headroom so the Bridge cannot later consume resources
    needed by Hermes or websites.
11. Service isolation: a Bridge compromise must not grant access to future
    Hermes or website data.
12. Future-upgrade section: ordinary Bridge releases reuse the foundation —
    never repeat the full bootstrap.

## 3. Bootstrap vs upgrade split (second message)

The plan must separate **one-time KVM2 bootstrap** from **repeatable
version-upgrade** work; first deployment creates a reusable, side-by-side,
rollback-safe upgrade procedure; include realistic forecasts for small /
normal / major upgrades; never a design that repeats the full 7–12 h
bootstrap per release.

## 4. Process consequences applied

- Plan v1 (`KVM2_DEPLOYMENT_PLAN_62BF661B_2026-08-16.md`) is superseded before
  review; its in-flight Claude T0 review was stopped before producing output
  (no verdict file existed at stop).
- Revised plan V2 + compact diff → then the T0 pair runs on V2.
- Nothing is uploaded, configured, installed or started on KVM2 until the
  reviewed V2 plan is presented for the single installation authorization.
- Stage-0 payload build (local-only, no host contact) was already complete
  before these messages: payload for `62bf661b` built, `RELEASE_SHA256SUMS`
  sha256 `1078ac22d3139be1ea50ede33fcb3dbc2ef01c5c860b46941c27ec8b550c175d`.
  It remains valid — the candidate is unchanged by any of this.

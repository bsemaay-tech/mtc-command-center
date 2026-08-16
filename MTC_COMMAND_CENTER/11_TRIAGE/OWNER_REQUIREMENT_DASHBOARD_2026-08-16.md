# Owner requirement — Bridge dashboard is completion-critical — 2026-08-16

Recorded by the Fable 5 Lead from the owner's chat message, 2026-08-16
evening. Binding on the KVM2 deployment scope immediately.

## Gate-1 scope change of record

The owner changed the Gate-1 scope of the KVM2 deployment plan BEFORE
acceptance: dashboard reachability is now completion-critical. Consequences:

- Plan V2's in-flight Codex T0 audit was **stopped before any verdict file
  existed**; had it finished, its result would be stale/supplemental. This is
  a recorded owner scope change before acceptance — **not** a repair round,
  not cap evasion. The fresh T0 pair runs only against the final pinned plan
  V3 bytes: exact `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh, no fallback.
- The chain lane remains PAUSED exactly as recorded; **no cap waiver is used
  and that lane is not reopened** (owner confirmation, same message).

## The requirement set (adopted verbatim in substance)

1. **8790 never public:** bound to `127.0.0.1` on KVM2 only; UFW never opens
   it; the future website reverse proxy never proxies the dashboard or any
   Bridge control endpoint.
2. **Operational completion definition:** initial deployment is complete only
   when, after the separately authorized first DISARMED start, Barış can
   securely open the existing Bridge dashboard from his Windows computer.
3. **One-click Windows launcher (T0, audited with the deployment package):**
   pinned SSH tunnel Windows → KVM2 `127.0.0.1:8790`; opens browser; stores
   no password/passphrase; uses the already-loaded ssh-agent key; strict
   host-key checking; clear failure on auth/forward/local-port errors.
4. **Dashboard verification must prove:** loopback-only 8790; unreachable
   from the internet; tunnel works from the owner's PC; dashboard shows
   correct host, candidate SHA, service health, last update time, DISARMED
   state; network/exchange/live-order capability disabled; no dashboard
   button can ARM or create live economic action in the credential-free
   DISARMED deployment.
5. **No redesign delay:** use and verify the EXISTING dashboard first
   (the candidate serves `bridge/static/index.html` at `/`).
6. **Dashboard V2 work package** (separately scoped, immediately after stable
   DISARMED deployment): polished owner view — connection/service health,
   DISARMED/ARMED state, deployed SHA + host identity, active strategy,
   positions + working orders, equity + P&L, risk gates, decision stream +
   recent errors, backup health, last successful update. Must separate a
   read-only monitoring dashboard from the private control dashboard
   (ARM/DISARM/KILL); public hosting never exposes control endpoints; any
   public/authenticated web access is a separate scope + authorization.
7. Multi-tenant protections of Plan V2 are retained unchanged.
8. This instruction authorizes **no** KVM2 installation, configuration,
   service start, firewall change, or deployment. Reviews first; then the
   single installation-authorization sentence.

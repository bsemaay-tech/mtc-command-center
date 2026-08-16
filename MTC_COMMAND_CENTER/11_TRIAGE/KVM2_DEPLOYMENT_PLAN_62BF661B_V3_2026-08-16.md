# KVM2 deployment plan V3 — candidate `62bf661b` — dashboard completion-critical — 2026-08-16

Status: **PLAN — NOT AUTHORIZED TO EXECUTE. SUPERSEDES V2**
(`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md`). V3 = V2 + the owner's
dashboard requirement (`OWNER_REQUIREMENT_DASHBOARD_2026-08-16.md`), recorded
as a Gate-1 scope change before acceptance — V2's stopped Codex audit produced
no verdict; nothing here is a repair round. Host-touching → **fresh T0 pair on
these exact bytes** (`claude-opus-5` xhigh + `gpt-5.6-sol` xhigh, no
fallback), then the single §9 owner sentence before any KVM2 action.

Audited package = THIS file + the launcher
`KVM2_RUNKIT/Open-BridgeDashboard.ps1` (host-contacting, T0, same review).

## Sections carried unchanged from V2 (by reference, still binding)

§0 tenancy model (three tenants, reserved `hermes`/`webapp` identities and
paths, 80/443 reserved, no host-wide security changes, isolation, resource
headroom ≤1 GiB RAM / ≤10 G disk vs measured 46.9 MiB); §1 identities
(candidate `62bf661b…`, payload manifest sha `1078ac22…`, host `srv1856225`);
§2 bootstrap-vs-upgrade split; §3 transfer + dry run; §4 one bounded install +
verify; §5 operational evidence; §6 later gates (secrets, first start, fresh
reset); §7 exact rollback enumeration; §8 repeatable upgrade procedure +
forecasts (small 1–2 h / normal 2–4 h / major 4–8 h). Read V2 for their full
text; V3 changes none of those bytes' meaning and adds the sections below.

## D1. Dashboard scope (NEW — completion-critical)

The candidate already ships the dashboard: `bridge/static/index.html`, served
by the FastAPI app at `/` with `/static` assets and the `/api/*` read
endpoints, all on the loopback-only listener `127.0.0.1:8790`. **No redesign
before first deployment — this existing dashboard is used and verified.**

Exposure rules (permanent):

- 8790 binds to `127.0.0.1` on KVM2 only. UFW never opens it. It is never
  reachable from the internet, and the future website reverse proxy never
  proxies the dashboard or ANY Bridge endpoint (control endpoints
  `/api/arm`, `/api/disarm`, `/api/kill`, `/api/config` included).
- Owner access is ONLY via the pinned SSH tunnel launcher (D2).

## D2. One-click Windows launcher (NEW — part of this audited package)

`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_RUNKIT/Open-BridgeDashboard.ps1`:

- opens `ssh -N -L 127.0.0.1:18790:127.0.0.1:8790` to `baris@152.239.123.231`
  with `BatchMode=yes`, `StrictHostKeyChecking=yes`, pinned
  `UserKnownHostsFile`, `ExitOnForwardFailure=yes`;
- authentication ONLY from the owner-loaded ssh-agent — the script stores no
  password, no passphrase, and names no key file for auth;
- preflights: ssh binary, known_hosts pin present, agent running with a
  loaded identity, local port free — each with a clear plain-language failure;
- verifies the dashboard answers through the tunnel (HTTP 200 at
  `http://127.0.0.1:18790/`) before opening the browser; kills the tunnel and
  fails clearly otherwise;
- closing the window closes the tunnel.

## D3. Dashboard verification matrix (NEW — runs after the separately authorized first DISARMED start)

Initial deployment is **operationally complete only when every row passes**:

| # | Assertion | How proven |
|---|---|---|
| D3-1 | 8790 listens ONLY on KVM2 loopback | `ss -tln` on host: exactly `127.0.0.1:8790`, no wildcard/public bind |
| D3-2 | 8790 unreachable from the internet | connection attempt from the operator PC to `152.239.123.231:8790` times out/refused; UFW shows no 8790 rule |
| D3-3 | Tunnel works from the owner's Windows PC | `Open-BridgeDashboard.ps1` end-to-end success, recorded |
| D3-4 | Dashboard shows correct facts | host identity `srv1856225`, candidate SHA `62bf661b…` (via `/api/status` fields rendered by the dashboard), service health, last update time, **DISARMED** state — screenshot + `/api/status` JSON recorded |
| D3-5 | No live capability | credential-free mode: no broker/exchange connection attempt (logs), `HL_LIVE_ACK` absent |
| D3-6 | No dashboard button can ARM or create live economic action | ARM attempted via the dashboard against the credential-free DISARMED service → application-level refusal (the Gate-A A-4-proven behavior) recorded; state remains DISARMED; no order/network side effect in logs |

D3-6 note: the ARM refusal check is executed exactly once, recorded, and is a
refusal-proof — not an ARM authorization. ARM remains forbidden.

## D4. Dashboard V2 — separately scoped successor work package (NEW)

Immediately after the stable DISARMED deployment (not an indefinite future
item): polished owner view — connection/service health; DISARMED/ARMED state;
deployed SHA + host identity; active strategy; positions + working orders;
equity + P&L; risk gates; decision stream + recent errors; backup health;
last successful update. **Hard split:** a polished READ-ONLY monitoring
dashboard, and a PRIVATE control dashboard (ARM/DISARM/KILL). Public website
hosting never exposes Bridge control endpoints; any public or authenticated
web access is its own scope + owner authorization. Tier split per owner item
12: local read-only visual work T1; anything touching host access,
deployment, reverse-proxy rules, authentication, or control endpoints T0.
Queued in `NEXT_STEPS.md` tagged [AI: Claude].

## §9 The single authorization ask (present AFTER the fresh T0 pair accepts these bytes)

> "I authorize the one-attempt masked DISARMED installation of exact accepted
> release `62bf661b065dec5b5d9895d83575581fe369252d` onto Hostinger KVM2
> (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md (V2
> stages 3–5 carried unchanged, inside the §0 Bridge tenancy boundary only).
> No service start, no enable, no secret, no firewall change, no
> TESTNET/mainnet, no broker, no ARM, no orders, no action on reserved
> Hermes/web identities, no public exposure of port 8790 ever. The dashboard
> verification matrix D3 runs only after my separate first-start sentence. A
> failed attempt stops and reports; retry needs a new sentence."

## V2 → V3 compact diff

1. NEW D1: dashboard completion-critical; existing `bridge/static` dashboard
   used as-is; 8790 never public; reverse proxy never touches Bridge.
2. NEW D2: one-click tunnel launcher added to the audited package (T0).
3. NEW D3: six-row dashboard verification matrix defining operational
   completion; D3-6 = ARM-refusal proof, not ARM.
4. NEW D4: Dashboard V2 successor package with read-only/control split and
   T1/T0 tier split; queued in NEXT_STEPS.
5. §9 sentence updated: names V3, adds no-public-8790 clause, D3 deferred to
   the separate first-start authorization.
6. Everything else carried from V2 unchanged by reference.

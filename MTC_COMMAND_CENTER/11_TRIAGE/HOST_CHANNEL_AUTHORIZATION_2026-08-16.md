# GATEA-STAGING host-channel authorization — 2026-08-16

Recorded by the Fable 5 Lead (session `f3a2cf9f`) from two owner messages in
chat on 2026-08-16. This supersedes, for GATEA-STAGING only, the "admin
conversation" route of owner decision §1
(`OWNER_DECISIONS_2026-08-16_MORNING.md`): Barış states there is no human
server administrator, so that route is unavailable.

## What the owner stated (message 1 — framing)

- There is **no human server administrator**.
- A documentation-only investigation confirmed `GATEA-STAGING` was created
  during an earlier AI-run workflow.
- The existing ordinary `gatea` login does **not** establish the requested
  privileged channel; the eight privileged-channel facts remain `UNKNOWN`.
- The Lead must **not** invent technical choices *and* must **not** connect to,
  probe, or modify the machine or credentials **without separate explicit
  approval** — and must prepare a design recommendation first.

## What the owner authorized (message 2 — execution grant)

Verbatim intent, recorded as adopted:

> "I authorize you to autonomously resolve the privileged read-only channel on
> the disposable GATEA-STAGING machine. You may design the safest route, use
> the existing pinned identity, connect to GATEA-STAGING, make the necessary
> security/configuration changes, use sudo/root where required, perform
> controlled verification tests, and create the required evidence. Complete the
> required T0 audits and continue the already-approved workflow without asking
> me for routine confirmations. This permission applies only to GATEA-STAGING.
> Do not touch Hostinger, KVM2, production systems, broker/exchange
> connections, ARM, orders, TESTNET/mainnet, trading logic, or master merge.
> Never display, copy, replace, or rotate private-key contents or other
> secrets. Stop only if an action outside these boundaries becomes necessary."

## How the Lead reads the two messages together

They are not contradictory. Message 1 forbids host contact *without separate
explicit approval*; message 2 *is* that separate explicit approval, and it also
resolves message 1's "do not invent choices" bar by explicitly delegating the
three design choices ("design the safest route"). Order of operations the Lead
will follow:

1. **Design first (this turn, documentation-only).** A reviewed design
   recommendation for the privileged read-only channel — the three category-(c)
   choices plus the independence/enforcement model — produced from records.
   Lane `CH1`. No host contact.
2. **Flagship T0 review of the design** before any host action.
3. **Execution phase** — connect, observe the five facts, configure the
   mutation-denial control under root, drop to a constrained principal, run the
   read-only attestation capture, verify RED/GREEN, seal evidence — under this
   authorization, GATEA-STAGING only, no routine confirmations required.
4. **Required T0 audits** of the produced evidence, then continue the
   already-approved WP-I workflow.

## Scope fence (binding on every phase)

ALLOWED (GATEA-STAGING only): connect via the existing pinned `gatea_ed25519`
identity; security/configuration changes on GATEA-STAGING; sudo/root on
GATEA-STAGING; controlled read-only verification tests; evidence creation.

FORBIDDEN: Hostinger provider/control-panel actions; KVM2; any production
system; broker/exchange connections; ARM; orders; TESTNET/mainnet; trading
logic; merge to master. **Never display, copy, replace, or rotate private-key
contents or any other secret.** Any action that would require crossing one of
these fences is a hard STOP that returns to the owner.

## The one limit the owner should see stated

With no human administrator and a single operator, the Lead configuring the
read-only control, connecting over it, and certifying it read-only cannot
*prove* independence to a second party — this is the project's self-confirming
pattern
(`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`).
The design's job is therefore to *enforce* read-only with a mechanism the
capturing process cannot silently lift (set once under root, capture under a
principal that lacks the privilege to remove it), and to **disclose** honestly
that residual continuity rests on operator integrity plus the fact that the
host is disposable. The disposable nature of GATEA-STAGING is what bounds the
residual risk to an acceptable level; that is the reason this is proceedable
rather than blocked.

## Material discovery — 2026-08-16, local read-only inspection

Before dispatching the design, the Lead established by **local inspection on
the operator PC only** (no VM started, no connection, no key contents read)
that several repository assumptions are wrong. These change the risk picture
substantially, and mostly in the owner's favour.

| Fact | Evidence | Consequence |
|---|---|---|
| `GATEA-STAGING` is a **local Hyper-V Generation 2 VM on Barış's own Windows PC**, not a remote or provider-hosted machine | `Get-VM` lists it beside `KVM2-Ubuntu-2404-Staging`; 4 vCPU, adapter on Hyper-V "Default Switch" | The hypervisor is the owner's own, so VM-object controls are inside scope. Hostinger and KVM2 stay hard-excluded. |
| Current state is **`Off`** | `Get-VM` State | Nothing can be observed until an authorized start; every category-(b) fact waits on it. |
| The pinned identity **exists locally** at `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519` | existence check only; matches the `-i` path in `.../09_TRANSPORT_B3B/operator_record/ops/01.argv:3` | The channel is usable without creating key material. Contents never read and never to be read. |
| The recorded address **`172.24.55.233` is stale** | host Default Switch adapter is now `172.25.64.1/20`; no `172.24.x` route exists | The address must be re-observed after start, never assumed. Any record still asserting it is stale. |
| **No checkpoints exist and `CheckpointType` is `Disabled`** | `Get-VMSnapshot` empty; VM property | The strongest available safety net is currently switched off. Enabling it (VM must be Off) is a proposed protective configuration step. |
| A sibling VM **`KVM2-Ubuntu-2404-Staging`** sits on the same host | `Get-VM` | Explicitly out of scope. Every command must name GATEA-STAGING; no all-VMs operations. |

**Why this improves the independence problem.** A Hyper-V checkpoint is a
rollback and integrity mechanism that no process inside the VM — including
in-VM root — can reach, alter, or delete. That is a real layer the single
operator's in-VM identity cannot silently lift, which is exactly what the
self-confirming-check lesson demands and what a purely in-VM design could not
provide. It does not make the operator independent of themselves at the host
level; that residual stays disclosed, bounded by the VM being disposable.

The design lane was re-dispatched with these corrected facts after its first
dispatch was stopped for being premised on a remote, possibly unreachable
provider host.

## Boundaries at time of writing

No host, network, SSH, connection, probe, configuration change, credential,
deployment, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC,
trading, merge-to-master, or economic action has occurred under this
authorization as of this record. Only the design lane has been dispatched.

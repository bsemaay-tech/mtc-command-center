# Research: Hosting Options and Costs for the Paper Soak

**Date: 2026-08-23**
**Answers:** GitHub issue #50 ("Research: hosting options and costs for the paper soak")
**Feeds:** decision ticket #39 ("Soak and shadow hosting: where forward clocks physically run")

A paper soak is an 8–16 week uninterrupted run of a light-CPU, bar-close-cadence Python
trading bot with simulated fills and no credentials/no real money. The defining constraint is
that **a stopped window can never resume** — any host outage (crash, reboot, sleep, forced
update restart, power loss) restarts the multi-week clock from zero. This document is
**facts only**: costs, specs, and documented policy behavior for three hosting options, each
checked against primary/official sources on 2026-08-23. It does not recommend an option — that
decision belongs to issue #39.

## Option Comparison Table

| Option | Monthly Cost | Setup Effort | Outage Risks | Effect on Never-Resume Rule | Key Sources |
|---|---|---|---|---|---|
| **(a) Owner's Windows 11 Pro PC, hardened** | $0 incremental (owner already owns it); optional UPS hardware cost not researched | Low-medium: GUI/`powercfg` sleep changes + Group Policy update-deadline changes, all local, no purchase | Mandatory security-update forced restart after a bounded deferral window (Microsoft-documented, see below); active-hours span capped at 18h/day; power cuts; accidental human interaction; shared-use PC | **Cannot be made fully immune.** Sleep/hibernate can be fully disabled; forced Windows Update restarts can only be **delayed**, not eliminated — Microsoft's own docs say a restart occurs "regardless of active hours" once its deadline + grace period elapse ([Microsoft Learn](https://learn.microsoft.com/en-us/windows/deployment/update/update-policies)) | [Microsoft Learn: powercfg](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options), [Microsoft Learn: update-policies](https://learn.microsoft.com/en-us/windows/deployment/update/update-policies), [Microsoft Learn: waas-restart](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart), [Microsoft Support: Power settings in Windows 11](https://support.microsoft.com/en-us/windows/power-settings-in-windows-11-0d6a2b6b-2e87-4611-9980-ac9ea2175734) |
| **(b) Reuse Hostinger KVM 2** | $8.99/mo intro, renews $14.99/mo (term-dependent) | Low if the box is already provisioned; needs a second isolated process/venv alongside whatever else runs there | Standard VPS-host risks (Hostinger-side maintenance/reboot, host incident) shared with whatever else is co-located; repo commit `9d20c84f` (branch `codex/rp7-r1-r4-repair-20260815`, not merged to master) documents an IBKR Paper Bridge V1 deployed disarmed on KVM2 since 2026-08-17 — real, but **not independently re-verified live** in this pass (see prose for full provenance) | Removes the local-PC sleep/update-restart problem entirely; adds "shared-fate-with-another-process-on-the-same-box" coupling instead | [hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting) (fetched 2026-08-23); repo: `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, commit `9d20c84f` |
| **(c-i) New Hostinger KVM 1** | $6.49/mo intro, renews $11.99/mo (term-dependent) | Low-medium: fresh box, needs its own provisioning/hardening from scratch | Same class of VPS-host risk as (b), but dedicated — no co-tenancy with an unrelated process | Same host-level benefit as (b) without the co-tenancy coupling | [hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting) (fetched 2026-08-23) |
| **(c-ii) New Hetzner Cloud (Cost-Optimized/CX line)** | **Not verified live** — pricing page is JavaScript-rendered and returned no visible price in three fetch attempts; only concrete figures found were in a 2024-06-06 Hetzner press release (€3.79–6.80/mo), now **~2 years stale** and likely superseded by reported 2026 repricing (unverified) | Low-medium, same class as (c-i) | Same VPS-host risk class as (b)/(c-i) | Same host-level benefit as (b)/(c-i) | [hetzner.com/pressroom/new-cx-plans](https://www.hetzner.com/pressroom/new-cx-plans/) (dated 2024-06-06); [docs.hetzner.com/cloud/servers/overview](https://docs.hetzner.com/cloud/servers/overview/); live price NOT obtainable via [hetzner.com/cloud](https://www.hetzner.com/cloud) in this research pass |

---

## (a) Hardening the owner's Windows 11 Pro PC

### Power, sleep, and hibernate settings

The consumer GUI path for sleep timeouts is **Settings > System > Power & battery > Screen,
sleep, & hibernate timeouts**, where the user selects how long to wait before the screen turns
off and before the device sleeps, via dropdown time intervals (Microsoft's own wording: "Select
how long you want your device to wait before going to sleep") — [Microsoft Support: Power
settings in Windows
11](https://support.microsoft.com/en-us/windows/power-settings-in-windows-11-0d6a2b6b-2e87-4611-9980-ac9ea2175734).
That fetched page did not itself describe an explicit "Never" option in its quoted text, but
setting sleep/hibernate to never-trigger is achieved reliably via the command-line tool below.

For an unattended multi-week run, the command-line tool is `powercfg.exe`. Per Microsoft's own
command reference ([Microsoft Learn: Powercfg command-line
options](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options)):

- **`powercfg /change <setting> <value>`** modifies a setting in the current power scheme, where
  `<value>` is in minutes and `<setting>` is one of: `monitor-timeout-ac`, `monitor-timeout-dc`,
  `disk-timeout-ac`, `disk-timeout-dc`, `standby-timeout-ac`, `standby-timeout-dc`,
  `hibernate-timeout-ac`, `hibernate-timeout-dc`. Setting the AC (plugged-in) standby and
  hibernate timeouts to `0` is the standard way to disable timed sleep/hibernate while on mains
  power (documented syntax; the "0 = disabled" behavior itself is standard, long-established
  Windows semantics for this value rather than a sentence quoted verbatim from this page).
- **`powercfg /hibernate off`** — "Disables the hibernate feature" outright (same source).
- **`powercfg /waketimers`** — "Enumerates the active wake timers. If enabled, the expiration of
  a wake timer wakes the system from sleep and hibernate states" (same source) — useful to audit
  what could still wake/interrupt the machine.
- **`powercfg /requests`** — "Enumerates application and driver Power Requests. Power Requests
  prevent the computer from automatically powering off the display or entering a low-power sleep
  mode" (same source) — useful to see what is currently holding the machine awake or could later
  release that hold.
- **`powercfg /requestsoverride`** — sets a Power Request override for a specific process,
  service, or driver (same source) — can be used to force-pin the soak's Python process (or its
  parent service) as an always-active requester if needed.
- **`powercfg /availablesleepstates` (`/A`)** — "Reports the sleep states available on the system.
  Attempts to report reasons why sleep states are unavailable" (same source) — useful to confirm
  which sleep states (S3 vs. Modern Standby/S0) the hardware supports, since sleep behavior differs
  between the two.

**USB selective suspend** (task-requested item): not covered by a `powercfg /change` alias
directly; it is a GUI/Control Panel advanced power setting. Per Microsoft's own support topic
("USB selective suspend feature is disabled in Windows"), the path is **Control Panel > Power
Options > Change plan settings > Change advanced power settings > USB settings > USB selective
suspend setting**, set to Disabled for both "On battery" and "Plugged in" —
[support.microsoft.com](https://support.microsoft.com/en-us/topic/usb-selective-suspend-feature-is-disabled-in-windows-5514cecf-59bd-57d3-d6d3-618a18c78011).
The same Microsoft topic notes selective suspend exists to conserve power and Microsoft does not
generally recommend disabling it purely for that reason — it's a targeted fix when USB-device
wake/hang issues appear, which is the relevant case here if the soak relies on any
USB-attached peripheral staying continuously responsive.

**"Allow wake timers"**: this is the Sleep-subgroup toggle inside the Advanced Power Options GUI
(Control Panel > Power Options > Change plan settings > Change advanced power settings > Sleep >
Allow wake timers). This exact GUI path is corroborated by Microsoft Q&A community answers on
learn.microsoft.com rather than by conceptual/reference documentation prose, so it is a weaker
citation than the items above — flagged accordingly rather than passed off as equally
authoritative. The command-line equivalent for auditing (not setting) wake timers is
`powercfg /waketimers`, documented above.

### Windows Update: active hours and forced restarts — can it be fully prevented?

**No.** Microsoft's own current documentation is explicit that forced restarts can be **delayed,
not indefinitely prevented**, on Windows 11.

**Active hours** identify when the device is expected to be in use; Windows avoids restarting
during that window. Default is 8 AM–5 PM, user-adjustable, with an "intelligent"
automatically-learned mode also available. Critically, **active hours have a hard maximum span**:
per Microsoft Learn, "The max active hours length for Windows 10, version 1607 and Windows
Server 2016 is 12. Later versions support max active hours length of 18 hours." — [Microsoft
Learn: Manage device restarts after
updates](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart). This means
the owner cannot mark all 24 hours of the day as "active" to blanket-suppress the update-restart
window; at least ~6 hours/day remain outside active hours where Windows considers itself free to
restart.

Beyond active hours, the mechanism that actually governs Windows 11 is the modern **"Specify
deadlines for automatic updates and restarts"** policy (configurable via Local Group Policy
Editor, available on Windows 11 Pro, under Computer Configuration > Administrative Templates >
Windows Components > Windows Update — or via MDM/registry). Per [Microsoft Learn: Policies for
update compliance and user
experience](https://learn.microsoft.com/en-us/windows/deployment/update/update-policies):

- Recommended default deadlines: **Quality update deadline: 1 day; Feature update deadline: 2
  days.**
- Recommended default grace periods: **Grace period for quality updates: 2 days; Grace period for
  feature updates: 7 days.**
- Explicit guidance: "don't use more than 7 days between the quality update publishing date and
  update completion (calculated by deferral + deadline + grace period)."
- The decisive sentence: **"Once the deadline and grace period have passed, updates are applied
  automatically, and a restart occurs regardless of active hours."**

Microsoft's own doc also directly addresses the older, theoretically stronger-sounding blocking
policies the task asked about — **"No auto-restart with logged on users for scheduled automatic
updates installations"** and **"Turn off auto-restart during active hours."** On the current
canonical restart-management page, Microsoft states, repeatedly and explicitly, that the classic
restart-blocking Group Policy Objects — "Always automatically restart at the scheduled time,"
"Specify deadline before auto-restart for update installation," "Specify engaged restart
transition and notification schedule for updates," and related notification-control policies —
are each individually flagged: **"This policy is a legacy policy and isn't applicable for Windows
11. Legacy policies might be removed in a future release."** — [Microsoft Learn: Manage device
restarts after updates](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart).

For "No auto-restart with logged on users" specifically (still nominally functional, unlike the
policies above), Microsoft's own caution is that it should not be relied on as a real block: **"In
Group Policy this policy doesn't work exactly as per description. This policy can result in no
quality update reboots period, given many users never log off. The recommendation to replace this
would be to leverage compliance deadline..."** (same source, and repeated verbatim in
[update-policies](https://learn.microsoft.com/en-us/windows/deployment/update/update-policies)).
In other words, Microsoft's own current position is: don't rely on the old "block forever"
policies; the supported behavior is bounded deferral via the deadline/grace-period mechanism, and
that mechanism explicitly forces a restart once its window elapses, active hours or not.

For completeness, the same page documents the older (Windows-10-era, "legacy, not applicable to
Windows 11") **"Limit restart delays"** policy, which likewise only bounds the delay rather than
removing it: "If the restart doesn't succeed after a default period of seven days, the user sees
a notification that a restart is required... The minimum value is two days and the maximum value
is two weeks (14 days)." Every mechanism Microsoft documents — legacy or current — caps the
deferral window; none removes the eventual forced restart.

*(Secondary, non-authoritative signal, not used as a citation for facts above: Microsoft Q&A
community threads on learn.microsoft.com report that since Windows 11 25H2 the update servicing
stack enforces restarts even more aggressively and increasingly disregards some of the classic
GPOs — directionally consistent with, but not itself proof of, Microsoft's own "legacy... isn't
applicable" labeling above.)*

### UPS (uninterruptible power supply)

General guidance, not tied to a specific cited source per the task's own framing (this sub-point
is intentionally brief): a desktop PC intended to run continuously for 8–16 weeks benefits from a
UPS sized to ride out short outages and to trigger a graceful, controlled response (rather than an
uncontrolled power-loss crash) on longer outages. This does not solve the never-resume constraint
by itself — it only removes brief-outage risk; a genuinely extended local power cut still stops
the clock unless the UPS is paired with generator-class backup, which is a materially bigger
commitment than the paper soak likely warrants.

### Residual risks (after full hardening)

- **Mandatory security-update deadlines** — per above, Microsoft's own documented mechanism
  forces a restart once deadline + grace period elapse, "regardless of active hours." This cannot
  be fully and indefinitely disabled on Windows 11 by Microsoft's own account of its own policies.
- **Physical power outages, ISP outages** — a local outage stops the clock regardless of OS
  configuration; a UPS mitigates only short outages (see above).
- **Accidental human interaction** — the owner or anyone else with physical/remote access to the
  machine could sleep, restart, sign out, or physically power-cycle it; unlike a dedicated remote
  VPS, this PC is also used for other things.
- **Laptop lid-close / monitor-off edge cases, if the machine is a laptop** — Windows has a
  separate "what closing the lid does" control (Settings > System > Power & battery, or Control
  Panel > Power Options), independent of the sleep timeout, that must also be set to not-sleep;
  this exact control text was not directly quoted from an official page in this research pass and
  should be verified hands-on if the target machine is a laptop rather than a desktop.
- **Crash-triggered auto-restart, driver/OEM power-tool overrides** — general Windows behavior
  (e.g., automatic restart after a system failure) and any vendor power-management utility
  layered on top of Windows can override or fight the `powercfg` settings above; not
  independently verified against a primary source in this pass.

---

## (b) Reusing the existing Hostinger VPS, "KVM 2"

### Current official specs and price

Per the official Hostinger VPS pricing page, fetched live on 2026-08-23
([hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting)):

**KVM 2:** 2 vCPU cores, 8 GB RAM, 100 GB NVMe SSD storage, 8 TB bandwidth. Listed at **$8.99/mo**
introductory price, renewing at **$14.99/mo** (the page describes this as "for 2 years" pricing).
All Hostinger VPS plans include a 1 Gbps network, weekly automated backups, and full root access.
Hostinger's displayed price depends on the selected billing-term commitment (the page did not let
this pass fully disambiguate every term length — 1/12/24/48-month options are typical for
Hostinger — so treat the intro/renewal figures above as the values shown by the page's default
selection at fetch time, not a guaranteed price at every term length).

### Current KVM2 occupancy — verified against the repo's own memory files

Per the task's instruction, this was checked directly against
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md` and
`...\NEXT_STEPS.md` (both internal repo files, cited here by path, not URL) — not taken from any
summary.

The most recent **directly dated, live-checked** KVM2-specific fact in `GLOBAL_HANDOFF.md` is the
entry **"[Codex gpt-5.6-sol] 2026-08-16 — Dashboard hosting decision queued; KVM2 checked live"**:
a read-only SSH check at 22:04 +03 on the KVM2 host (`srv1856225`) "returned `BRIDGE_DIR_ABSENT`,
no `mtc-bridge*` unit and no `:8790` listener; only `/home/baris/payload-acdf4e37` was present.
Therefore neither Bridge nor Dashboard V1 is installed/running on Hostinger KVM2" as of that
check. The same entry notes `python3.12-venv` was installed but "the Bridge install stopped
fail-closed before mutation."

The next entry chronologically, **"[Claude Fable 5] 2026-08-17 — Housekeeping lane: cleanup, phase
watch, notifier T0 prep,"** explicitly frames itself as running "coordinated alongside (never
touching) the KVM2 deployment-owner session" — i.e., a separate, concurrent session owned the
actual KVM2 deployment work, and this housekeeping entry does not itself record that session's
outcome. Within that same entry: "Phase watch: ... `WATCH_ACTIVE: NO` until the deployment owner
confirms a DISARMED start + activation preconditions" and "Telegram notifier: ... HOLD until the
KVM2 T0 lane clears" — both phrased as pending/unconfirmed as of that entry's writing.

`NEXT_STEPS.md`'s only KVM2-specific match is inside a standing daily "Phase Watch" instruction
block: "**[AI: Claude] Activation:** after the KVM2 install + first DISARMED start (live queue),
flip `WATCH_ACTIVE: YES`" — again phrased as a future trigger condition, not a confirmed past
event, within this file's own text.

**Within these two specific files**, no dated entry was found that itself records a *completed,
confirmed* KVM2 Bridge installation/DISARMED-start. The most recent direct fact in that pair is
the 2026-08-16 22:04 check showing nothing installed, and the following day's entries (in this
same file lineage) treat completion as pending and owned elsewhere.

**Broadening the check beyond those two files surfaced the completion event itself**, dated a few
hours later the same window. Commit `9d20c84f` ("docs(memory): morning handoff - bridge deployed
and running DISARMED on KVM2", authored 2026-08-17 06:25 +03, on branch
`codex/rp7-r1-r4-repair-20260815` — independently checkable via `git show 9d20c84f` in this repo)
adds a `GLOBAL_HANDOFF.md` entry stating: release `be007fd802bbfd2eb181d66038c374865d1562ee`
installed on host `srv1856225`; first DISARMED start `2026-08-17T00:25:02Z`; service left
"RUNNING (active, NRestarts=0, loopback-only 8790, credential-free, arm_enabled=false)"; full
evidence pointed to `11_TRIAGE/KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md`. The same commit edits
`NEXT_STEPS.md` to mark the prior "old payload only, nothing installed" line as **"SUPERSEDED by
2026-08-17 deployment."** This reads as a deliberate, specific completion record (real release
hash, real host name, real service-status fields), not a stray or speculative note.

**Provenance caveat — why the two-file check above didn't see it:** commit `9d20c84f` is **not**
an ancestor of this research worktree's base commit (`764da27f`), and is **not** on `origin/master`
either — it lives only on `codex/rp7-r1-r4-repair-20260815` (checked via `git merge-base
--is-ancestor` and `git branch --all --contains`, 2026-08-23). This repo runs many long-lived
parallel worktrees/branches whose memory-file edits are periodically hand-"ported" to master; this
particular entry evidently has not been ported yet. That is a documentation-propagation gap, not
necessarily evidence the deployment didn't happen — the commit describes a real action against a
named real host.

**Honest limitation, restated:** this document treats "Bridge V1 deployed disarmed on KVM2 since
2026-08-17" as the best-documented available fact (single specific dated commit, internally
consistent, superseding an explicit same-day "nothing installed" check), but that fact is now six
days old (2026-08-23) relative to this research date, its documentation lives on an unmerged
branch, and this task did not independently re-verify current live state (that would need a fresh
SSH/host check, out of scope for read-only public-page research). Treat "deployed as of 2026-08-17,
not re-confirmed since" as the operative caveat for the reasoning below. (Separately, note KVM2 —
a Hostinger VPS — is a different host from "GATEA-STAGING," a local Hyper-V VM that appears
elsewhere in these memory files in a similar "loopback-only, credential-free DISARMED" context;
that material was intentionally excluded here because it describes a different machine, not KVM2.)

### Isolation / headroom reasoning

Taking the best-documented state (Bridge V1 deployed disarmed/loopback-only/credential-free on
KVM2 as of 2026-08-17, per commit `9d20c84f` above, not re-confirmed live since), reasoning about
adding the soak process alongside it:

- **Network blast radius:** a loopback-only listener (bound to `127.0.0.1`, not a public
  interface) is not reachable from, and does not reach into, a second unrelated local process
  except through ordinary same-host OS mechanisms (shared filesystem, shared port/PID namespace).
  Co-locating a second local-only Python process does not, by itself, open new network exposure
  for either process.
- **Resource contention:** KVM 2 is specced at 2 vCPU / 8 GB RAM (see above). The soak bot is
  described as "light CPU, bar-close cadence" — i.e., largely idle between bar closes. A disarmed
  bridge (no live order flow) is also low-activity by design. Two low-activity processes on a 2
  vCPU/8 GB box is a generically low-contention pairing, but **not risk-free**: nothing in the
  reviewed memory files indicates cgroup/container-level resource limits are configured between
  processes on that host, so a memory leak, runaway log file, or CPU spike in either process is
  not walled off from the other by default.
  
- **Shared fate (the real coupling):** both processes share the same host's uptime, reboot
  schedule, and maintenance/patch cycle. Reusing KVM2 does not add a new outage vector beyond what
  choosing "reuse this VPS at all" already implies — but it does couple the soak's fate to any
  future operational action taken on the bridge on that same box (an install, upgrade, debugging
  restart, or `systemctl` mistake affecting the bridge could take the soak down as collateral
  damage). A fully separate host (option c) avoids this specific coupling.
- **Reverse blast radius:** because the soak bot itself carries no credentials and no real money
  by the task's own description, it adds negligible risk to the bridge side even if it crashed or
  misbehaved.

### Residual risks

- KVM2's occupancy is documented as of 2026-08-17 (commit `9d20c84f`, unmerged branch) but not
  re-verified live since — six days stale relative to this research date, and the documenting
  branch has not been ported to master (see provenance caveat above). Treat the isolation
  analysis above as grounded-but-not-freshly-confirmed, not as a live-verified current state.
- Standard VPS-host risk: Hostinger-side maintenance windows, host-level incidents, or noisy-
  neighbor effects on shared virtualization infrastructure (not independently quantified from an
  official source in this pass).
- Operational/human coupling with whatever else is deployed or later gets deployed to the same
  box (see "shared fate" above).

---

## (c) A second, small, dedicated Linux VPS

### Hostinger VPS "KVM 1"

Per the same official page fetched 2026-08-23
([hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting)): **1 vCPU core, 4 GB RAM, 50
GB NVMe SSD, 4 TB bandwidth.** Listed at **$6.49/mo** introductory price, renewing at **$11.99/mo**
(page describes this as "for 2 years" pricing) — same caveat as KVM 2 above regarding term-length
dependency. Same included extras: 1 Gbps network, weekly backups, full root access.

### Hetzner Cloud, entry/shared-vCPU line

Per Hetzner's own current documentation
([docs.hetzner.com/cloud/servers/overview](https://docs.hetzner.com/cloud/servers/overview/),
fetched live 2026-08-23), Hetzner's shared-vCPU cloud server lines are currently named **"Cost-
Optimized" (older hardware generation)** and **"Regular Performance" (most recent hardware
generation)**, alongside a separate dedicated-resource "General Purpose" line. This confirms the
task's caution not to assume a specific stale plan name — Hetzner's own docs describe the tiers
by these category names rather than only by SKU code today.

**Price could not be verified live.** Three separate fetch attempts against Hetzner's own pricing
pages —
[hetzner.com/cloud](https://www.hetzner.com/cloud),
[hetzner.com/cloud/cost-optimized](https://www.hetzner.com/cloud/cost-optimized/), and the docs
overview page above — returned either placeholder text ("starting from max/mo," with no numeric
value present in the fetched HTML) or, for the specific Cost-Optimized SKU shown (`CX23`, 2 vCPU /
4 GB RAM / 40 GB NVMe / 20 TB traffic for EU locations), an explicit **"This product is currently
unavailable. Please check back later"** status. Hetzner's cloud pricing page is JavaScript-
rendered, which appears to be why no price figure survived extraction; this is a genuine access
limitation, not an assumption.

The only concrete Euro figures obtainable from Hetzner's own domain came from an official press
release, **dated 2024-06-06** —
[hetzner.com/pressroom/new-cx-plans](https://www.hetzner.com/pressroom/new-cx-plans/):
CX22 (2 vCPU, 4 GB RAM, 40 GB disk) at €3.79/month; CX32 (4 vCPU, 8 GB RAM, 80 GB disk) at
€6.80/month; both bundled with 20 TB traffic and 1 IPv4 address. **These figures are over two
years old relative to this research date (2026-08-23) and should not be treated as current
pricing.** Search results surfaced (but this document does not cite as fact, since none were
official Hetzner sources) third-party claims of Hetzner shared-vCPU price increases in April 2026
and June 2026, which — if accurate — would mean the real current price is materially higher than
the 2024 figures above. **Before using Hetzner in any cost comparison, check
hetzner.com/cloud directly (or its price calculator) for the live number** — this document could
not extract it via automated fetch in this research pass.

### Residual risks

- Same general VPS-host risk class as (b): host-side maintenance/incidents outside the owner's
  control, not independently quantified here from an official source.
- Fresh provisioning/hardening effort not required for (b) if KVM2 turns out to already be
  suitably configured — (c) starts from a blank box either way.
- Hetzner price uncertainty (above) means (c-ii)'s true current cost is not established by this
  document; only (c-i) Hostinger KVM 1 has a directly-fetched, dated live price.

---

## Lean

Lean: hardening the owner's Windows 11 Pro PC removes local sleep/hibernate as a failure mode but,
by Microsoft's own current documentation, cannot remove the mandatory bounded Windows-Update
restart deadline, while both VPS paths (reuse KVM2, or provision a small new Linux box) remove
that specific mechanism entirely at a directly-verified monthly cost of roughly $6.49–14.99
depending on tier and billing term (Hostinger) with Hetzner's current price left unverified in
this pass.

**The decision itself is out of scope for this document and belongs to issue #39** — this file
supplies facts only.

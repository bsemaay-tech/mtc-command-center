# WP-P0-26 OPS-A — phone-push notifier proposal (DECISION INPUT FOR THE OWNER)

**Status: PROPOSAL — no signup, no credential, no message, no install happened.**
This document only compares candidate technologies for the dead-man watchdog's
phone-push notifier. The detect-to-delivery bound stays **`[OPEN]`** per the plan: it
can only be measured by the real phone drill, which is gated behind G9 and owner
authorization, and package acceptance explicitly requires that drill.

External facts below are **as-known 2026-08-25** and must be re-verified at adoption
time (pricing, limits and app behavior change; see the OSS dependency ledger rules
from WP-P0-24 — any adopted component gets a ledger entry).

## What the notifier must satisfy (from the package + repo policy)

1. **No third-party signup** to receive pushes on the owner's phone (no account
   creation, no phone-number registration with a vendor).
2. **No credential** the watched host or checker must hold — or at most a purely
   local credential that never leaves the owner's second machine.
3. **Fits the dead-man architecture (plan #39):** the checker runs OUTSIDE the
   watched host (owner PC), so delivery must survive a KVM2 outage and should not
   add a new single point of failure between the checker and the phone.
4. **Dependency-free client:** callable from our stdlib-only `watchdog.py`
   (`urllib` HTTPS POST) through the existing `Notifier` interface — no SDK, no app
   to install on the sending side.
5. **Alerts carry no secrets and no controls** (plan §12.6.2(f)) — true for every
   candidate; it constrains payload content, not the choice.
6. Low maintenance burden; bounded OSS lifecycle obligations (WP-P0-24 ledger).

## Candidates

| Criterion | **ntfy (self-hosted, owner PC)** | **ntfy.sh (public server)** | **Telegram bot** | **Pushover** |
|---|---|---|---|---|
| Signup | **none** (self-host; app points at our URL) | **none** (topic name only) | Telegram account + BotFather bot creation (phone number) | Account + purchase (one-time ~$5/platform) |
| Credential held by checker | **none** (optionally a local access token that never leaves the owner PC) | **none** (topic name is the only shared value) | bot token (a real secret, stored on the checker) | user key + app token (two secrets, stored on the checker) |
| Third party in the delivery path | **none on Android** (phone app subscribes directly to our server over websocket). **iOS: instant push requires routing through the upstream ntfy.sh APNS relay** (see caveat) | ntfy.sh (availability + visibility of topic names/message metadata) | Telegram cloud (sees message content; subject to ISP-level blocking in some jurisdictions, incl. periodic restrictions in Türkiye) | Pushover cloud (closed source, US company) |
| Survives KVM2 outage | **yes** — checker + server are on the owner PC by design | yes | yes | yes |
| Client effort | HTTP PUT/POST to `http://localhost:8080/<topic>` — one `urllib` call | same, to `https://ntfy.sh/<topic>` | `https://api.telegram.org/bot<token>/sendMessage` — one POST, but token handling | `https://api.pushover.net/1/messages.json` — one POST, two secrets |
| Self-hostable | **yes** — single Go binary (Apache-2.0), active project; add to OSS ledger at adoption | n/a | no (client side is; the delivery cloud is not) | no |
| Cost | none | free (hosted rate limits; irrelevant at dead-man volume) | free | ~$5 one-time per platform |
| Reliability risk points | owner PC itself (already required by #39), home network uplink, phone OS battery management | ntfy.sh availability | Telegram availability + regional blocking + token compromise | Pushover availability |
| Measured detect→phone latency | `[OPEN]` — needs the real drill | `[OPEN]` | `[OPEN]` | `[OPEN]` |

Excluded without a table row: Signal (`signal-cli` requires registering a phone
number and a heavy daemon — fails criteria 1–2 and 6); WhatsApp CallMeBot-style
hooks (unofficial, fragile — fails 6); email (not phone push; unbounded latency);
SMS gateway (cost + credential + third party).

## Recommendation

**Primary: self-hosted ntfy on the owner PC** (the second location the plan already
requires for the checker), with a long random topic name:

- No signup anywhere, no external credential, no third party in the loop on the
  Android delivery path — the strictest possible match to criteria 1–3.
- The sending side is one stdlib HTTPS POST; our shipped `LocalLogNotifier` gains a
  ~30-line `NtfyNotifier` sibling behind the existing `NOTIFIERS` registry — no
  watchdog core change (the extension point was built for exactly this).
- Single static binary on the owner PC; low maintenance; one OSS-ledger entry.

**Caveats the owner must weigh (decision inputs, not blockers):**

1. **iOS:** Apple does not allow self-hosted instant push; the ntfy iOS app needs
   the upstream ntfy.sh APNS relay for instant delivery (metadata exposure + a
   third-party dependency), or falls back to background polling (latency slides
   toward the poll period). If the owner's phone is iOS, either accept the relay for
   push (payloads remain secret-free) or accept poll-bounded latency — this directly
   affects the `[OPEN]` bound. On Android there is no such dependency.
2. **Home uplink:** if the owner PC serves ntfy directly, the phone must reach it —
   same-LAN wakeup is fine, but away-from-home delivery needs the router reachable
   (VPN/Tailscale-style path is out of tonight's scope and must be its own decision).
   The public-ntfy.sh fallback below exists precisely for this.
3. **Topic name = bearer capability** on the public path: anyone with the topic name
   can read/publish. A 32+ char random topic makes guessing infeasible; still, the
   self-hosted deployment should bind the checker's publisher to localhost.

**Fallback (zero-infrastructure): public ntfy.sh with a long random topic.** Same
no-signup/no-credential posture, one less box to run, at the cost of a third-party
availability and metadata dependency. Reasonable first drill target if the owner
wants the acceptance drill before standing up the self-hosted service.

**Contingency: Telegram bot** — only if measured reliability of the ntfy path
proves insufficient; it trades away the no-credential criterion and adds a cloud
that has faced periodic regional blocking. Pushover is **rejected** for this
package (paid + signup + two credentials + closed cloud, i.e. fails three of the
six criteria).

## What adoption would look like (NOT tonight, gated)

1. Owner picks a technology (this document) and authorizes the phone drill.
2. One `NtfyNotifier` (or the chosen one) added to `watchdog.py`'s `NOTIFIERS`
   registry; unit-tested with a local HTTP stub (no real send in tests).
3. G9-gated host step installs the server (if self-hosted) and schedules the
   checker — separate T0 authorization per the plan.
4. Real drill: kill a watched heartbeat → measure detect→phone latency → fill the
   `[OPEN]` bound and record it in the acceptance evidence. **Until that drill
   runs, WP-P0-26 acceptance stays OPEN by definition.**

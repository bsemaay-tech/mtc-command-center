# PROPOSAL — not applied; amending root governance is a separate change under its own authorization

**Package:** WP-P0-24

**Prepared:** 2026-08-24

**Audit tier of this proposal package:** T1

**Authority:** proposal only. This file does not amend `AGENTS.md`, authorize an adoption or update, or authorize retirement/removal.

## Proposed `AGENTS.md` text

> ## OSS lifecycle policy
>
> **Open-source first.** Before writing a component, search for a maintained open-source implementation. Prefer a library or adapter over a fork. Custom code remains appropriate for platform-specific strategy contracts, risk and allocation policy, execution and reconciliation, and safety behaviour. Independently validate every financial calculation against a second implementation before trusting it.
>
> **No adoption by convenience.** An installed package, an existing import, a plan-level recommendation, or a successful proof of concept is not adoption evidence. Before a component enters or expands in the repository, a separately authorized package must append a dependency-ledger entry and pass all controls below. The ledger may reject a candidate; it cannot authorize adoption unless the owner has separately granted that authority.
>
> **Owner and roles.** The Lead Orchestrator is the dependency steward: it keeps the ledger current, schedules reviews, triages advisories and presents decisions. The implementer prepares evidence and walks the proposed rollback. Barış is the only retirement/removal authority and retains any adoption authority not explicitly delegated in a bounded owner instruction. A component's update owner must be named in its ledger entry; `AI`, `team` or `upstream` alone is not an owner.
>
> **Integration-mode gate.** Every entry declares exactly one primary integration mode: `EMBED_SOURCE`, `LINK_AS_DEPENDENCY`, `SEPARATE_LOCAL_PROCESS`, `FILE_OR_API_INTEROP`, `POC_ONLY`, `ARCHITECTURE_REFERENCE` or `UI_REFERENCE`. Licence, vulnerability exposure, incident response and portability are evaluated for that mode. Rejecting an embedded or linked use does not automatically reject a separate process, file/API interop, POC or reference use.
>
> **No categorical legal conclusion.** Capture the licence identifier and the full licence/notice text at the exact adopted version. State the obligations relevant to the declared integration mode. Where compatibility or obligations are doubtful, write exactly: *"requires a documented licensing review before adoption in this integration mode"*. Architecture evidence is not legal advice.
>
> **Twelve mandatory controls.** Before adoption, on every version bump, and at the entry's review cadence, preserve evidence for:
>
> 1. canonical upstream provenance, exact tag/commit, published artifact hash and acquisition path;
> 2. licence identifier, full text/notice, integration mode and resulting obligations;
> 3. the complete transitive dependency set, exact versions and artifact hashes, plus the transitive count and any unmaintained dependency;
> 4. a dated vulnerability review against named advisory sources, with unresolved severity and exposure in this integration mode;
> 5. active-maintainer evidence, release cadence, median security-issue closure time and a documented security-reporting path; unknown or private metrics are recorded as unknown, never guessed, and a single-maintainer money-adjacent dependency is a named risk;
> 6. objective abandonment criteria declared before adoption;
> 7. a named update owner, review cadence and real-repository artifact tests for every bump; updates are never automatic;
> 8. incident actions for a published vulnerability, compromised release and breaking change; on a money-adjacent surface, the first action is disable or pin, never wait;
> 9. export of dependency-held data to a documented open format readable without the dependency;
> 10. a named replacement, switching-cost estimate and a rollback to the prior pinned state walked in a throwaway environment;
> 11. preservation of sources, hashes, licences, findings, measurements, benchmarks, decisions and rollback evidence before retirement/removal; and
> 12. a retirement/removal path that is a separate, explicitly owner-authorized cleanup act after control 11. No package may schedule its own deletion.
>
> **Supply-chain floor.** Python dependencies follow the Bridge standard: a human-readable direct-input file plus a fully resolved lock in which every package is exactly pinned and every permitted artifact has a hash. The installer must fail closed on unpinned or unhashed input. Other ecosystems must provide an equivalent immutable lock and integrity verification. A version bump regenerates the entire lock and receives the risk tier required by the highest affected surface.
>
> **Service cost gate.** A new service or local process must name who patches it, who monitors it, the health signal, the down-state behaviour, its data export and its removal/rollback. Missing any answer rejects the service at the current scale.
>
> **Objective abandonment floor.** An entry may set stricter conditions, but it must classify a component abandoned when any declared condition occurs. Conditions must be mechanically observable, for example: upstream archives the repository; the declared stable-release/activity window elapses; the security acknowledgement or mitigation deadline elapses; integrity-verified artifacts cease to be available; or the licence changes outside the accepted mode. "Looks inactive" and "maintainers seem slow" are not conditions.
>
> **Incident floor.** The dependency steward records the advisory and affected version on the same business day it is discovered, stops new installs/updates, preserves the current lock and evidence, and applies the entry's disable-or-pin action. Any upgrade, downgrade, mitigation or re-enable action is a separately reviewed change. Never contact a host, account, broker or live service merely because an advisory exists.
>
> **Append-only ledger.** Ledger entries are immutable after commit. Corrections and version changes are new entries. A later entry identifies every entry it supersedes; the earlier content remains. Status projections are appended as records rather than rewriting history. Rejected, expired, compromised, superseded and retired records remain readable forever.
>
> **Review cadence.** The dependency steward checks money-adjacent/runtime/network components monthly and research-only/UI components quarterly, plus an event review on an advisory, upstream archive, ownership/licence change or release-signing incident. A cadence review does not authorize an update.
>
> **Exit before entry.** Adoption evidence is incomplete until the replacement and rollback are named and at least one representative rollback in the package has executed successfully. Evidence that merely says an uninstall command exists is not a walked rollback.

## Intended insertion and non-effect

If separately authorized and accepted, the block above belongs in the root governance near the existing OSS and audit-tier rules. This proposal deliberately does not select a component version, install anything, change any existing dependency, amend `AGENTS.md`, or authorize cleanup.

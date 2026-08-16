# Gemini Draft — Dashboard on Same VPS Decision

**Draft Date:** 2026-08-16  
**Author:** Gemini Bounded Implementer  
**Target Transfer:** Bridge V2 Decision Record (to be reviewed and transferred by owning Codex thread / human owner)  
**Status:** Proposal / Draft only — does NOT claim acceptance.

---

## 1. Context & Scope

This document is a bounded design-decision proposal regarding the hosting architecture of the future Bridge dashboard.

- **Current Fact:** This draft represents documentation and architectural design guidance only. The current KVM2 installation, deployment configuration, and host state are **not** established, altered, or enacted by this document.
- **Future Plan:** A proposal to colocate the future Bridge dashboard on the same Virtual Private Server (VPS) that hosts the Bridge backend runtime.
- **Authority Notice:** The owning Codex thread must independently inspect, validate, and transfer any accepted text into the canonical Bridge V2 decision record. This draft claims no final authority or acceptance.

---

## 2. Proposed Decision

**Decision:** Host the future Bridge dashboard on the same VPS instance as the Bridge backend runtime under a **private-first, authenticated access** architecture.

- The dashboard service will **not** be public-by-default or exposed directly to the public internet.
- Access must require secure, private-first transport (e.g., authenticated reverse proxy over TLS, WireGuard/VPN, or SSH tunneling with multi-factor/key-based authentication).

---

## 3. Key Benefits

1. **Simpler Private Connectivity:**
   - Communication between the dashboard service and the Bridge backend occurs via local loopback (`127.0.0.1` / Unix domain sockets / local IPC) rather than traversals across public networks or multi-VPS overlays.
   - Eliminates latency overhead, cross-host network routing complexities, and external API gateways for internal management metrics.

2. **Fewer Exposed Attack Surfaces:**
   - Zero public internet listening ports required for internal Bridge APIs.
   - Tight attack surface minimized to the host's hardened management channel.

3. **Consistent Operational Boundary:**
   - Single unified administrative perimeter for logging, monitoring, host access policies, and operational maintenance.
   - Cohesive lifecycle management without multi-node orchestration overhead.

---

## 4. Risks, Constraints & Required Safeguards

Colocation introduces shared-host risks that require strict operational and architectural safeguards:

1. **Strict Failure Independence & Non-Interference:**
   - **Hard Rule:** Any dashboard failure (process crash, memory leak, hung worker, unhandled exception, high UI query load) must **never** degrade, delay, or interrupt the Bridge trading backend or its execution pipelines.
2. **Resource Isolation & Protection:**
   - Bridge backend must maintain absolute priority over CPU, memory, I/O, and file descriptors.
   - Dashboard process must be restricted via OS-level controls (e.g., dedicated systemd slices/cgroups, memory limits, process priority/niceness) to prevent CPU or RAM starvation of the core Bridge runtime.
3. **Transport Security & Authentication:**
   - Private-first access strictly enforced.
   - TLS encryption with strong session authentication (no default passwords, session tokens with expiration, IP/interface binding).
4. **Network & Firewall Isolation:**
   - Local firewall (e.g., UFW/nftables/iptables) configured with default-deny on public interfaces for dashboard and Bridge ports.
   - Dashboard bound strictly to local loopback interface or isolated private overlay.
5. **Monitoring & Health Checks:**
   - Independent watchdog and health check mechanisms monitoring both services separately.
   - Telemetry must clearly distinguish between Bridge engine health and dashboard UI health.
6. **Backup, Disaster Recovery & Reproducibility:**
   - Independent backup strategies for configurations and persistent data without requiring lockouts of the trading backend.
   - Clean, reproducible deployment runbooks isolating dashboard components from core bridge services.

---

## 5. Explicit Non-Authorization

> **CRITICAL BOUNDARY:** This document is strictly an informational design draft.
> 
> **NO AUTHORIZATION IS GRANTED OR IMPLIED FOR:**
> - Any deployment or staging execution.
> - Any server, operating system, package, or configuration change.
> - Any network, firewall, port forwarding, DNS, or routing modifications.
> - Any credential generation, secret storage, or identity modification.
> - Any broker, exchange, trading logic, order routing, or economic action.

---

## 6. Codex Acceptance & Transfer Checklist

The owning Codex thread should verify the following points prior to incorporating this proposal into the canonical Bridge V2 decision record:

- [ ] **Factual Separation Verified:** Current KVM2 operational state is clearly distinguished from the future dashboard proposal.
- [ ] **Private-First Requirement Preserved:** Strict non-public access requirement (VPN/TLS/private binding) is retained.
- [ ] **Trading Independence Guaranteed:** Safeguard stating dashboard failure cannot impact Bridge execution is intact.
- [ ] **Resource Limits Specified:** CPU/RAM/cgroup isolation requirements are explicitly included in implementation prerequisites.
- [ ] **No Live Actions Taken:** Confirmed no unauthorized config, deployment, network, or broker changes were made.
- [ ] **Ownership & Placement:** Decision is incorporated into the canonical Bridge V2 decision record under proper version control.

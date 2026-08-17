# OVERNIGHT RESULT — WP-L P2 Stage 3 + 3B (2026-08-09 night)

Lead session (Claude Fable 5), autonomous overnight run authorized by Barış this
evening. Read together with `OVERNIGHT_HANDOFF_2026-08-09_STAGE3.md` (inputs) and the
unit records under `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/03_TRANSPORT/`,
`04_PREREG_R45B/`, `05_TRANSPORT_R45B/`.

## One-paragraph summary

First host contact happened and stayed evidence-only: transport, remote extract and
9/9 block-hash verification all PASS. **B3 stopped (rc 3, STOP-not-FAIL)** because the
unprivileged `gatea` user cannot `stat` anything under `/etc/mtc-bridge` (`750
root:root`) — a design gap (`B3-GAP-ENV`), not host drift; everything B3 could check
before that point (release tree, venv tree, write-bit sweeps) **held exactly as
preregistered**. **R4-5 was re-preregistered as `-R45B` and PASSED both arms**: the
RP4-C3 `restore_into` symlink guard is proven load-bearing with real Linux symlinks —
the one item that could not close on Windows is now closed. Zero service mutation, zero
ARM, zero credential contact all night. Commits: `7e9d1c4a` (Stage 3 + adjudication),
`ee49a945` (Stage 3B PASS), pushed to `origin/feature/donchian-crypto-ladder`.

## State of the accepted WP-L P2 designs

| Item | State |
|---|---|
| B3 | **STOP → blocked on `B3-GAP-ENV`** (owner decision below). Checks 1–3 held; checks 4–5 unverifiable as `gatea`. RUNID `-B3` burned. |
| R4-5 | **PASS** (as `-R45B`; evidence bound, fixture preserved on host at `/tmp/r45.p3adetdb`) |
| C1, C2-A/B, C3, C4-A/B/C, C5 | BLOCKED, untouched, as required |

## OWNER DECISION NEEDED — `B3-GAP-ENV`

The accepted RP1-B3 block assumes the operator can stat `/etc/mtc-bridge/mtc-bridge.env`
and read `install_manifest.json` binding. Both live behind `750 root:root`; the accepted
execution model is unprivileged `gatea` with zero host mutation. Structurally
incompatible — one side must change:

1. **(Recommended) Repair the design**: B3's unprivileged scope keeps checks 1–3 +
   ancillary dir modes; the env-file/manifest-binding admission moves to a privileged
   deploy-time channel (root-side verify at install, already T0 territory). Cost: RP1-B3
   re-repair + re-audit cycle, runkit re-freeze (block hash changes → new Stage 1),
   because a frozen accepted block may not be edited silently.
2. **Host-side access**: put `gatea` in a group/ACL that can read `/etc/mtc-bridge`.
   Host mutation/reprovisioning — forbidden without your explicit instruction, and it
   widens what a compromised operator account can read (the env file holds runtime
   secrets paths). Not recommended.
3. **Narrow sudo**: `sudo -n` allowlist for exactly `stat`/`sha256sum` on two paths.
   Host mutation + a new privilege surface; middle ground, still needs your sign-off.

No improvised closure was attempted. B3 waits for this call; it does not block R4-5
evidence already banked, and per the accepted designs the C-items were blocked anyway.

## Also for the morning

- Two junk dirs + WSL/Docker items from the handoff remain open, unchanged.
- Ledger: Stage 3 + 3B booked 0.4 h prospectively → ~28.3 h remaining.
- Audit posture: per the tier policy audits run at WP boundaries; WP-L P2 is not closed
  (B3 pending), so no audit was dispatched tonight. Meta-artifacts (this file, records)
  are T3 self-verified.
- Single-writer held: no dispatch to the other Fable session; no Codex dispatch needed.

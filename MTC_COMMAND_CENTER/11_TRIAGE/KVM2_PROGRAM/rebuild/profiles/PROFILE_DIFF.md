# Machine-profile difference contract

| Surface | temporary-testnet-lab | future-trading-only |
|---|---|---|
| Bridge | Required, TESTNET only | Required; mode remains separately gated |
| `mtc-bridge` identity | Required, non-login | Required, non-login |
| `ai-lab` identity | Absent until Phase 6 admission; optional later | Forbidden |
| AI agent/coding/browser | Absent until individually admitted | Forbidden |
| Containers/Docker socket | Deferred; socket never given to agents | Forbidden unless separately required for bridge, audited, and owner-approved |
| Public app/listener | Forbidden | Forbidden |
| Bridge control | Loopback plus owner SSH tunnel | Same |
| Writable bridge paths | State and logs only | Same |
| Restore source | TESTNET bridge state only, per open P3-01 choice | Verified allowlist only; no lab image/home/cache |
| Credentials | TESTNET names under separate gate | Newly issued/rotated names under separate gates |
| Host trust | Mixed-use after any lab admission; TESTNET only | Clean trusted build required |
| Mainnet | Forbidden | Still blocked until final post-build audit and owner gate |

Any undeclared difference is a blocker. Package, user, service, listener, unit,
filesystem, and credential-name inventories must be mechanically diffed during
rehearsal and final build.

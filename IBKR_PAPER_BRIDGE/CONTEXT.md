# Bridge terminology

- **Bridge:** the Hyperliquid paper/TESTNET execution runtime under the legacy directory name.
- **ARM:** explicit transition permitting bounded paper/TESTNET execution; never automatic.
- **DISARMED:** startup-safe state; no execution authorization.
- **KILLED:** latched terminal safety state; not shorthand for unconditional `cancel_all()`.
- **Candidate identity:** repository commit plus frozen package/config/dependency hashes.
- **Deployed identity:** bytes installed on a host; distinct from candidate and running identity.
- **Running identity:** verified process and loaded artifact; never inferred from deploy success.

# Path-scope prover status

Status: `AUTHORED-PENDING-AUDIT`

Audit tier: T1 - local-only Stage-1 static analysis; no host, network, trading, Pine,
parity, MTC, deployment, transport, or runtime action.

Design: quote-aware complete-input Bash lexer, pinned scalar expansion with provenance,
filesystem/network sink extraction, lexical path normalization, exact/tree/terminal
allowlist verdicts, and fail-closed rc 3 for every unsupported or dynamic construction.

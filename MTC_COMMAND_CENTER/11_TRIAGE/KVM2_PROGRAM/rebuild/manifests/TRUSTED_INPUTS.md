# Trusted-input manifest contract

- Status: **PARTIALLY POPULATED / NOT A RELEASE**
- Base source commit: `423897b76b32f68cdabcae16b39c078fdd1f67cb`
- Base provenance: `origin/master`, merge of PR #25
- Python target: CPython 3.12 on Linux
- Direct dependency source: `IBKR_PAPER_BRIDGE/requirements.in`
- Exact transitive lock: `IBKR_PAPER_BRIDGE/requirements.lock`
- Lock generation: `uv pip compile` with hashes, Python 3.12, Linux platform
- Installer enforcement: venv, `--require-hashes`, `--no-deps`,
  `--only-binary=:all:`, no global pip

The following must be frozen before P3-02 can close:

| Input | Required proof | Current state |
|---|---|---|
| Ubuntu 24.04.x source/provider image | Exact version/ID plus official signature/checksum or documented provider clean-origin evidence | OPEN |
| Apt repositories | Exact official repository definitions and signatures | OPEN |
| OS packages | Names, versions, source repository, installed manifest hash | OPEN |
| Python runtime | Exact 3.12 patch version and OS package provenance | OPEN |
| Dependency lock | File SHA-256 and clean Linux install evidence | Prepared locally; Ubuntu install UNVERIFIED |
| Release source | Exact committed SHA; clean status; protected-scope diff zero | OPEN because this batch is uncommitted |
| Payload | `git archive` output plus externally recorded `RELEASE_SHA256SUMS` SHA-256 | OPEN |
| First-start unit | Rendered exact-SHA filename and SHA-256 | Template prepared; rendered hash OPEN |
| Steady unit | Separate rendered hash; never installed without later gate | Template prepared; admission OPEN |
| Bootstrap/installer | File SHA-256 plus syntax/static/rehearsal evidence | Local checks pending/final evidence OPEN |
| State artifact | WAL bundle DB, invariant, and manifest hashes | Tool prepared; owner choice and final capture OPEN |

No mutable branch, floating package, global application pip, unsigned download,
unrecorded repository, or unverified artifact may enter a release. Package
metadata resolution is not installation proof. P2-09 and P3-03 stay
`BLOCKED/UNVERIFIED` until a named expendable Ubuntu 24.04 environment reproduces
the complete manifest.

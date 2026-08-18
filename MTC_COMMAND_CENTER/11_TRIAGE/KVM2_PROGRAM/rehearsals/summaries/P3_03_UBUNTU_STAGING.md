# P3-03 Ubuntu staging summary

- Verdict: **BLOCKED / UNVERIFIED**
- Date: 2026-07-26
- Exact immutable candidate: unavailable; exact-base payload probe built, but
  the current 12-path readiness package remains uncommitted
- Named expendable Ubuntu environment: `KVM2-Ubuntu-2404-Staging`, prepared for
  local Hyper-V creation after the required Windows restart; not yet available
- Active KVM2 used: no

The local staging matrix is specified in `../STAGING_MATRIX.md`. A clean
detached worktree at `f61ed91919110e8856b2bc309c2c807365bb5fea`
successfully produced a 6,963-file local payload whose checksum-manifest hash is
`d2a4275268d27a911ea74d97d57ab2132e0da137a037bce663b3a98d37d12a21`;
manifest verification passed. This is a packaging probe, not the final
candidate, because post-merge verification found a required uncommitted
readiness repair and the owner subsequently amended the canonical deployment
sequence.

Hyper-V is enabled and pending one restart. The official Ubuntu cloud-image
archive, key-only cloud-init seed, VM creation script, and elevated
startup-resume task have been prepared outside the repository. That task
resumes the download and enforces the published media checksum and safe archive
layout before extraction or VM creation. No Ubuntu boot, bridge service action,
WAL migration rehearsal, active-KVM2/VPS action, TESTNET exchange check, or
bridge first start occurred. P3-03, P3-04, and P3-05 remain blocked/open.

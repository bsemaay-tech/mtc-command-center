# Gate A A5 run-kit E — local package evidence (2026-08-09)

## Source and package

- Accepted source commit: `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1`.
- Package directory: `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34`.
- Tar: `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34.tar`.
- Tar SHA-256: `895fe530f4fe85b9dc0c86332776899c88492197c2748c1de14f950f0e6f1cef`.
- Tar bytes: `133120`.
- Built from raw committed blobs, with deterministic uid/gid/mtime and executable mode 0755 on
  `gatea_A5.sh`; no Windows working-tree conversion and no bare `git archive`.

## Exact archive members

1. `gatea-run-kit-20260809E-2ce41e34/`
2. `gatea-run-kit-20260809E-2ce41e34/README.txt`
3. `gatea-run-kit-20260809E-2ce41e34/SHA256SUMS`
4. `gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh`
5. `gatea-run-kit-20260809E-2ce41e34/test_gatea_A5_readiness.py`

Member identities:

- README: `60bb9cafb2bb26400333c35d1570300fa5bb03c7bd7ad2411f3d4810e06f007f`,
  35289 B, 495 LF, CR0.
- Script: `74161fb4544baed3bc79587a2ad86068714b3873ce946769c012d167672ed8a3`,
  25066 B, 497 LF, CR0, tar mode 0755.
- Test: `0e50ebb967af606e6194d7547e22f75fa4bf5b44c086554af1542733bb7a0145`,
  59469 B, 1265 LF, CR0.
- Manifest: `1ef3c4b4926846429dc6386216d2228d99892d902c2e404e65227b17f5cfe5d8`,
  248 B, 3 LF, CR0; all three entries verify.

## Extracted local verification

Extraction root:
`C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34-verify\gatea-run-kit-20260809E-2ce41e34`.
Extracted bytes equal package bytes exactly.

- Extracted test vs frozen D: rc1, RED 6/29.
- Extracted test vs exact pre-repair E `61d88f12`: rc1, RED 28/29; boundary check sole failure.
- Extracted test vs extracted repaired E: rc0, GREEN 29/29.
- Extracted `gatea_A5.sh`: `bash -n` rc0.
- Extracted `SHA256SUMS`: all entries OK, rc0.
- Tar listing: expected five members only; script executable; rc0.

## State and next action

Package is local only. It has not been transferred, extracted remotely, or run on staging. A-5
remains FAIL under run-kit D; A-6..A-9 NOT RUN. Next: remote absence preflight, transfer tar,
verify tar hash, extract once, verify manifest/syntax/member modes and run the local-only E regression
on the extracted remote kit. Update `_AI_MEMORY` again before A-5 execution.

# WP-L Phase 2 — Stage 1 record (runkit extraction)

Result: **PASS**

## Source

- commit `4c0d5fc5aeb1e069cd6171c11d143ac2a49a6e2c`
- blob `76e0a66cd621ec5d38cc580904968262ce69678f` (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`)
- blob bytes 180987, sha256 `eae933f8823cfccfcca2b52fe0f1791a533cdbd6489e4d81c79266aa5dfde1d4`, CR bytes 0, BOM no
- read only via `git -C <repo> cat-file blob 76e0a66cd621ec5d38cc580904968262ce69678f`

## Blocks

Extraction: BLOCK-ID marker line inclusive, up to (not including) the closing fence.
LF line endings, final LF, no BOM, block bytes unmodified (no shebang added).

| Block | File | Lines exp/act | SHA-256 exp/act | Result |
|---|---|---|---|---|
| `RP0-LIB` | `RP0-LIB.sh` | 370/370 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | MATCH |
| `RP0-BOOTSTRAP` | `RP0-BOOTSTRAP.sh` | 36/36 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | MATCH |
| `RP1-B3` | `RP1-B3.sh` | 117/117 | `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af` | MATCH |
| `RP3-C2A-POST` | `RP3-C2A-POST.sh` | 104/104 | `e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27` | MATCH |
| `RP3-C2B-POST` | `RP3-C2B-POST.sh` | 74/74 | `26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412` | MATCH |
| `RP4-C3` | `RP4-C3.py` | 295/295 | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` | MATCH |
| `RP5-C4A` | `RP5-C4A.sh` | 374/374 | `a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2` | MATCH |
| `RP5-C4B` | `RP5-C4B.sh` | 249/249 | `10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e` | MATCH |
| `RP5-C4C` | `RP5-C4C.sh` | 228/228 | `de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8` | MATCH |

## Syntax validation

- `bash -n` on the eight shell blocks
- `py_compile` on `RP4-C3.py` with an explicit cfile in OS temp (no repo `__pycache__`)
- embedded python heredocs extracted to OS temp and compiled there: RP5-C4A x2, RP5-C4B x1, RP5-C4C x1 (the Stage 1 scope of record)
- ADDITIONAL, disclosed: `RP3-C2A-POST` also carries one `<<'PYEOF'` python heredoc, which §8.1 does not claim a `py_compile` check for. It was extracted and compiled in OS temp as well and is reported separately in `syntax_validation.txt`; it is extra evidence, not a change to the accepted §8.1 claim.
- all commands, argv and real rc/output recorded in `syntax_validation.txt`

## Archive

- `runkit.tar` — uncompressed, GNU tar format, 102400 bytes
- sha256 `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53`
- exactly the nine block files, no evidence or metadata members, no directory members
- fixed §8.1 table order; mtime=0, mode=0644, uid=0, gid=0, empty uname/gname
- platform tar on this host cannot normalize uid/gid/mtime/mode, so the archive is written
  by the purpose-built `stage1_build.py` kept here as evidence; the platform tar is still
  used read-only to cross-check the member listing (recorded in `ARCHIVE_MEMBERS.txt`)
- determinism was checked by running the same builder twice into two different output
  paths before this run: both produced the identical archive digest

## Self-QA

- the nine block files were re-read from disk and re-hashed
- `runkit.tar` was extracted into OS temp and every member byte-compared to its source block

disk   RP0-LIB        lines=370 sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48 OK
disk   RP0-BOOTSTRAP  lines= 36 sha256=e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33 OK
disk   RP1-B3         lines=117 sha256=f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af OK
disk   RP3-C2A-POST   lines=104 sha256=e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27 OK
disk   RP3-C2B-POST   lines= 74 sha256=26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412 OK
disk   RP4-C3         lines=295 sha256=0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5 OK
disk   RP5-C4A        lines=374 sha256=a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2 OK
disk   RP5-C4B        lines=249 sha256=10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e OK
disk   RP5-C4C        lines=228 sha256=de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8 OK
untar  RP0-LIB        bytes= 18968 sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48 IDENTICAL
untar  RP0-BOOTSTRAP  bytes=  1937 sha256=e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33 IDENTICAL
untar  RP1-B3         bytes=  5759 sha256=f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af IDENTICAL
untar  RP3-C2A-POST   bytes=  5308 sha256=e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27 IDENTICAL
untar  RP3-C2B-POST   bytes=  3804 sha256=26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412 IDENTICAL
untar  RP4-C3         bytes= 12770 sha256=0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5 IDENTICAL
untar  RP5-C4A        bytes= 19353 sha256=a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2 IDENTICAL
untar  RP5-C4B        bytes= 12110 sha256=10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e IDENTICAL
untar  RP5-C4C        bytes= 12089 sha256=de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8 IDENTICAL

## Not done (out of scope for Stage 1)

- no commit, no push, no branch action (Lead owns Git)
- no host, SSH, network, credential, service or economic action
- no file written outside `01_RUNKIT/`

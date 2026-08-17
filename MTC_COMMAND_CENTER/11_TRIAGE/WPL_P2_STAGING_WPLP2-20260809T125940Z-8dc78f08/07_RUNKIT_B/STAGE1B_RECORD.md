# WP-L Phase 2 - Stage 1B record (run-kit re-freeze)

Result: **PASS**

Build only. No host contact, no ssh/scp, no transport, no execution of any block,
no git mutation. Nothing was written outside `07_RUNKIT_B/` except compiled
artifacts, the tar unpack and the two determinism rebuilds, which live under an OS
temp root (`C:\Users\BARSEM~1\AppData\Local\Temp\wplp2_s1b_yy6k3alz`) and never touch the repo.

## What was built

A ten-block run-kit with two provenance classes, plus its identity table, source
identity record, deterministic archive, archive member listing, syntax validation
log and this record. Archive: `runkit_b.tar`, 184320 bytes, sha256
`888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`.

## Provenance classes

### Class A - `accepted_blob` (8 blocks, unchanged)

Extracted from the accepted proposals blob `76e0a66cd621ec5d38cc580904968262ce69678f`
(commit `4c0d5fc5aeb1e069cd6171c11d143ac2a49a6e2c`, `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`)
with the Stage 1 extraction rule, and verified bit-exactly against the Stage 1
table `01_RUNKIT/BLOCK_IDENTITIES.tsv`: `RP0-LIB`, `RP0-BOOTSTRAP`, `RP3-C2A-POST`, `RP3-C2B-POST`, `RP4-C3`, `RP5-C4A`, `RP5-C4B`, `RP5-C4C`.

### Class B - `repair_round6` (2 blocks, repair-cycle artifacts)

Copied byte-identical from `06_B3_REPAIR/round6/`, which is the audit-6-PASSed
content of the B3-GAP-ENV repair cycle:

- `RP1-B3` (`RP1-B3.sh`) - REPLACES the Stage 1 block of the same id; 37896 bytes; sha256 `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`; byte-identical to `06_B3_REPAIR/round6/RP1-B3.sh`.
- `RPD-VERIFY` (`RPD-VERIFY.sh`) - NEW block; 43940 bytes; sha256 `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`; byte-identical to `06_B3_REPAIR/round6/RPD-VERIFY.sh`.

The two classes are never mixed silently: `BLOCK_IDENTITIES_B.tsv` carries a
`provenance` column on every row, and `SOURCE_IDENTITY_B.txt` documents each class
in its own section.

## Blocks

| Block | File | Provenance | Lines exp/act | SHA-256 exp/act | Supersedes | Result |
|---|---|---|---|---|---|---|
| `RP0-LIB` | `RP0-LIB.sh` | `accepted_blob` | 370/370 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | - | MATCH |
| `RP0-BOOTSTRAP` | `RP0-BOOTSTRAP.sh` | `accepted_blob` | 36/36 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | - | MATCH |
| `RP1-B3` | `RP1-B3.sh` | `repair_round6` | 662/662 | `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc` | `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af` | MATCH |
| `RP3-C2A-POST` | `RP3-C2A-POST.sh` | `accepted_blob` | 104/104 | `e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27` | - | MATCH |
| `RP3-C2B-POST` | `RP3-C2B-POST.sh` | `accepted_blob` | 74/74 | `26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412` | - | MATCH |
| `RP4-C3` | `RP4-C3.py` | `accepted_blob` | 295/295 | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` | - | MATCH |
| `RP5-C4A` | `RP5-C4A.sh` | `accepted_blob` | 374/374 | `a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2` | - | MATCH |
| `RP5-C4B` | `RP5-C4B.sh` | `accepted_blob` | 249/249 | `10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e` | - | MATCH |
| `RP5-C4C` | `RP5-C4C.sh` | `accepted_blob` | 228/228 | `de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8` | - | MATCH |
| `RPD-VERIFY` | `RPD-VERIFY.sh` | `repair_round6` | 775/775 | `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c` | - | MATCH |

## What changed against the Stage 1 kit

- **Block added (1):** `RPD-VERIFY` (`RPD-VERIFY.sh`) - new, was not in the Stage 1
  kit at all. Root/deploy-channel admission verify block, frozen and NOT executed.
- **Block replaced (1):** `RP1-B3` (`RP1-B3.sh`) - the Stage 1 block
  (sha256 `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af`,
  117 lines) is superseded by the repaired round6 block
  (sha256 `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`, 662 lines).
- **Blocks unchanged (8):** `RP0-LIB`, `RP0-BOOTSTRAP`, `RP3-C2A-POST`, `RP3-C2B-POST`, `RP4-C3`, `RP5-C4A`, `RP5-C4B`, `RP5-C4C` - identical bytes and identical digests to the Stage 1 kit.
- **Archive digest changed:** Stage 1 `runkit.tar` sha256
  `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53` (9 members)
  -> Stage 1B `runkit_b.tar` sha256 `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b` (10 members).

### Disposition of the superseded block

The old `RP1-B3` payload is extracted from the accepted blob during the build only
to prove that the block being superseded is the expected one. It is not written to
any file in this kit and is not an archive member. The builder hard-fails if that
digest matches any shipped payload or if the digest string appears inside any block
file or inside the archive. Occurrence audit over the whole kit:

```
ARCHIVE_MEMBERS_B.txt            3098 bytes  non_ascii=0   old_sha_string=yes    evidence record
BLOCK_IDENTITIES_B.tsv           1991 bytes  non_ascii=0   old_sha_string=yes    evidence record
KICKOFF_STAGE1B_REFREEZE.md      4213 bytes  non_ascii=38  old_sha_string=yes    kickoff
RP0-BOOTSTRAP.sh                 1937 bytes  non_ascii=2   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP0-LIB.sh                      18968 bytes  non_ascii=22  old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP1-B3.sh                       37896 bytes  non_ascii=0   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP3-C2A-POST.sh                  5308 bytes  non_ascii=3   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP3-C2B-POST.sh                  3804 bytes  non_ascii=3   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP4-C3.py                       12770 bytes  non_ascii=9   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP5-C4A.sh                      19353 bytes  non_ascii=12  old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP5-C4B.sh                      12110 bytes  non_ascii=12  old_sha_string=no     shipped block payload (bytes inherited verbatim)
RP5-C4C.sh                      12089 bytes  non_ascii=6   old_sha_string=no     shipped block payload (bytes inherited verbatim)
RPD-VERIFY.sh                   43940 bytes  non_ascii=0   old_sha_string=no     shipped block payload (bytes inherited verbatim)
SOURCE_IDENTITY_B.txt            3732 bytes  non_ascii=0   old_sha_string=yes    evidence record
runkit_b.tar                   184320 bytes  non_ascii=69  old_sha_string=no     archive
runkit_b.tar.sha256                79 bytes  non_ascii=0   old_sha_string=no     evidence record
stage1b_build.py                43041 bytes  non_ascii=0   old_sha_string=yes    builder
syntax_validation_b.txt         14378 bytes  non_ascii=0   old_sha_string=no     evidence record
```

Every `old_sha_string=yes` row above is an evidence record, the builder's
verification constant, or the kickoff - never a shipped payload or the archive.
This record is not in the table because the table is computed before it is written;
it does carry the old digest, above, as the superseded value. `non_ascii` is nonzero
only for Class A payload bytes inherited verbatim from the accepted blob (and hence
for the archive that carries them); every file this builder authors is pure ASCII.

## Syntax validation

- `bash -n` on all nine shell blocks, including both Class B blocks
- `py_compile` on `RP4-C3.py` with an explicit cfile in OS temp (no repo `__pycache__`)
- embedded python heredocs extracted to OS temp and compiled there: `RP5-C4A` x2,
  `RP5-C4B` x1, `RP5-C4C` x1 (the Stage 1 scope of record)
- ADDITIONAL, disclosed: `RP3-C2A-POST` also carries one `<<'PYEOF'` python heredoc,
  which S8.1 does not claim a `py_compile` check for. It was extracted and compiled in
  OS temp as well and is reported separately in `syntax_validation_b.txt`; it is extra
  evidence, not a change to the accepted S8.1 claim.
- the heredoc count of every shell block is asserted against a fixed table, never
  inferred. The Class B expectation (zero embedded heredocs in `RP1-B3.sh` and
  `RPD-VERIFY.sh`) was established by direct inspection of the audit-6-PASSed round6
  files while authoring this builder and is asserted here the same way.
- all commands, argv and real rc/output recorded in `syntax_validation_b.txt`

## Archive

- `runkit_b.tar` - uncompressed, GNU tar format, 184320 bytes
- sha256 `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`
- exactly the ten block files, no evidence or metadata members, no directory members
- order: Stage 1 S8.1 order for the nine operator-channel blocks with `RP1-B3`
  replaced in place, then `RPD-VERIFY` appended as the tenth member. S8.1 has no
  slot for the new root/deploy-channel block, so the accepted ordering is preserved
  rather than reinterpreted.
- mtime=0, mode=0644, uid=0, gid=0, empty uname/gname, REGTYPE
- platform tar on this host cannot normalize uid/gid/mtime/mode, so the archive is
  written by this builder; the platform tar is still used read-only to cross-check
  the member listing (recorded in `ARCHIVE_MEMBERS_B.txt`)

### Determinism

- rebuilt twice by independent child processes into two different, previously
  non-existent output paths; all three archive digests are identical:

  - canonical `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`
  - rebuild_a `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b` (`C:\Users\BARSEM~1\AppData\Local\Temp\wplp2_s1b_yy6k3alz\rebuild_a`)
  - rebuild_b `888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b` (`C:\Users\BARSEM~1\AppData\Local\Temp\wplp2_s1b_yy6k3alz\rebuild_b`)

## Self-QA

- the ten block files were re-read from disk and re-hashed
- `runkit_b.tar` was extracted into OS temp and every member byte-compared to its
  source payload
- the builder refuses to clobber an existing output leaf artifact and exits nonzero
  with created files preserved on any identity, structure or syntax failure

```
disk   RP0-LIB        [accepted_blob] lines=370 sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48 OK
disk   RP0-BOOTSTRAP  [accepted_blob] lines= 36 sha256=e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33 OK
disk   RP1-B3         [repair_round6] lines=662 sha256=6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc OK
disk   RP3-C2A-POST   [accepted_blob] lines=104 sha256=e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27 OK
disk   RP3-C2B-POST   [accepted_blob] lines= 74 sha256=26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412 OK
disk   RP4-C3         [accepted_blob] lines=295 sha256=0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5 OK
disk   RP5-C4A        [accepted_blob] lines=374 sha256=a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2 OK
disk   RP5-C4B        [accepted_blob] lines=249 sha256=10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e OK
disk   RP5-C4C        [accepted_blob] lines=228 sha256=de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8 OK
disk   RPD-VERIFY     [repair_round6] lines=775 sha256=3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c OK
untar  RP0-LIB        [accepted_blob] bytes= 18968 sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48 IDENTICAL
untar  RP0-BOOTSTRAP  [accepted_blob] bytes=  1937 sha256=e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33 IDENTICAL
untar  RP1-B3         [repair_round6] bytes= 37896 sha256=6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc IDENTICAL
untar  RP3-C2A-POST   [accepted_blob] bytes=  5308 sha256=e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27 IDENTICAL
untar  RP3-C2B-POST   [accepted_blob] bytes=  3804 sha256=26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412 IDENTICAL
untar  RP4-C3         [accepted_blob] bytes= 12770 sha256=0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5 IDENTICAL
untar  RP5-C4A        [accepted_blob] bytes= 19353 sha256=a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2 IDENTICAL
untar  RP5-C4B        [accepted_blob] bytes= 12110 sha256=10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e IDENTICAL
untar  RP5-C4C        [accepted_blob] bytes= 12089 sha256=de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8 IDENTICAL
untar  RPD-VERIFY     [repair_round6] bytes= 43940 sha256=3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c IDENTICAL
```

## Transport status - NOT TRANSPORTED

**This kit has NOT been transported.** No host was contacted, no ssh/scp ran, no
block was executed anywhere. The kit exists only as files in `07_RUNKIT_B/`.

**Transporting this kit requires a NEW preregistration.** The existing Stage 2/3
preregistration is VOID for this kit: its S3 block hashes and its archive digest
no longer describe what is here. `RP1-B3` has a different digest, `RPD-VERIFY` did
not exist when that preregistration was written, and the archive digest changed from
`618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53` to
`888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`. Nothing in this kit may move to any host until a new
preregistration covering these ten block digests and this archive digest is
approved.

## Not done (out of scope for Stage 1B)

- no commit, no push, no branch action, no git mutation of any kind (Lead owns Git)
- no host, SSH, network, credential, service or economic action
- no transport, no execution, no preregistration
- nothing written outside `07_RUNKIT_B/` in the repo; `01_RUNKIT/` and
  `06_B3_REPAIR/` were read only

## Files in this kit

- `stage1b_build.py` (sha256 `c59989113045af8874f0827e17b5938c2133dd7e0cbe60f45cebd6055bdd128c`) - this builder
- the ten block files listed above
- `BLOCK_IDENTITIES_B.tsv`, `SOURCE_IDENTITY_B.txt`, `ARCHIVE_MEMBERS_B.txt`,
  `syntax_validation_b.txt`, `runkit_b.tar`, `runkit_b.tar.sha256`, this record


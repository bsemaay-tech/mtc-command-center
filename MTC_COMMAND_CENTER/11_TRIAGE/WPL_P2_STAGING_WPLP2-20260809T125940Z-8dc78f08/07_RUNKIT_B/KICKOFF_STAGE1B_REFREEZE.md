# KICKOFF — Stage 1B runkit re-freeze (build + evidence)

The B3-GAP-ENV repair cycle is ACCEPTED (audit 6 PASS, `06_B3_REPAIR/audit6/AUDIT6_REPORT.md`).
The frozen Stage 1 run-kit is now stale: it carries the OLD `RP1-B3.sh` and has no
`RPD-VERIFY.sh`. This unit produces the re-frozen kit. Build only — no host contact, no
transport, no execution against any host. Write ONLY into this directory
(`07_RUNKIT_B/`). ASCII only. English only.

## Provenance rule (the point of this unit)

The new kit has TWO provenance classes and the evidence must state which is which per
block. Never silently mix them:

- **Class A — unchanged, from the accepted frozen source.** Eight blocks extracted from
  the accepted proposals blob exactly as Stage 1 did: `RP0-LIB`, `RP0-BOOTSTRAP`,
  `RP3-C2A-POST`, `RP3-C2B-POST`, `RP4-C3`, `RP5-C4A`, `RP5-C4B`, `RP5-C4C`. Their
  expected SHA-256 are in `../01_RUNKIT/BLOCK_IDENTITIES.tsv` and must match bit-exactly.
- **Class B — repair-cycle artifacts.** `RP1-B3.sh` (REPLACES the old block) and
  `RPD-VERIFY.sh` (NEW), both taken byte-identical from
  `../06_B3_REPAIR/round6/`. Required SHA-256:
  - `RP1-B3.sh` = `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`
  - `RPD-VERIFY.sh` = `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`

Ten blocks total. The OLD `RP1-B3` sha `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af`
must appear NOWHERE in the new kit except in the evidence record as the superseded value.

## Inputs (read these, nothing else)

- This file.
- `../01_RUNKIT/stage1_build.py` — the accepted builder. Your builder is a derivative:
  keep its discipline (deterministic GNU-format uncompressed tar, fixed member order,
  mtime 0 / mode 0644 / uid 0 / gid 0 / empty uname+gname / REGTYPE, no directory
  members; BOM/CR/final-LF checks; bash -n and py_compile validation with cfile in OS
  temp so no `__pycache__` lands in the repo; platform-tar cross-check listing).
- `../01_RUNKIT/BLOCK_IDENTITIES.tsv`, `../01_RUNKIT/SOURCE_IDENTITY.txt`,
  `../01_RUNKIT/ARCHIVE_MEMBERS.txt` — the Stage 1 formats you are reproducing.
- `../06_B3_REPAIR/round6/RP1-B3.sh`, `../06_B3_REPAIR/round6/RPD-VERIFY.sh` — Class B.

Do not read the audit reports or handoffs; you do not need them.

## Deliverables (all into `07_RUNKIT_B/`)

1. `stage1b_build.py` — the builder. Must fail hard (nonzero exit, files preserved) on:
   any Class A identity mismatch, any Class B hash mismatch, wrong block count, BOM, CR
   byte, missing final LF, missing closing fence, or a syntax-check failure. It must
   refuse to clobber an existing output leaf.
2. The ten block files, extracted/copied by the builder.
3. `BLOCK_IDENTITIES_B.tsv` — same columns as Stage 1 plus a `provenance` column
   (`accepted_blob` / `repair_round6`), and for `RP1-B3` a `supersedes_sha256` column
   value naming the old digest.
4. `SOURCE_IDENTITY_B.txt` — Stage 1's fields for the Class A source, PLUS a Class B
   section: for each repair artifact, its path, byte count, sha256, and the one-line
   statement that it is byte-identical to the audit-6-PASSed round6 file.
5. `runkit_b.tar` + `runkit_b.tar.sha256` + `ARCHIVE_MEMBERS_B.txt` (Stage 1 format).
6. `syntax_validation_b.txt` — every command run with its real rc and output.
7. `STAGE1B_RECORD.md` — what was built, both provenance classes, the new archive digest,
   what changed vs the Stage 1 kit (block added, block replaced, eight unchanged), and an
   explicit statement that this kit has NOT been transported and that transporting it
   requires a NEW preregistration (the Stage 2/3 preregistration is void for this kit
   because §3 block hashes and the archive digest changed).

## Hard constraints

- No host contact. No ssh/scp. No git mutation (no add/commit/push/checkout/branch).
- Do not modify anything in `01_RUNKIT/`, `06_B3_REPAIR/`, or any other directory.
- Determinism: state in `ARCHIVE_MEMBERS_B.txt` that an independent rebuild reproduces
  the archive byte-for-byte, and demonstrate it (build twice to different paths, compare
  digests, record both).
- Print DONE plus the new archive sha256 and the ten block digests when finished.

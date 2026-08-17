# WPI SELF-QA claim audit - RP7

Audited document: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`

Method: documentary consistency only. I did not run the harness and did not inspect `SELF_QA_RP6.md`, `SELF_QA_TRANSPORT.md`, or `SELF_QA_PATHSCOPE.md`.

## Sections Covered

- Header, exact published command, environment disclosure, and exact-command transcript.
- Round-9 fence prose, table, code comments, and pasted transcript.
- Round-8, round-7, round-6, round-5, and round-4 carried-fence prose and pasted transcripts.
- Literal re-run section.
- `What this QA does not establish`.

Output lines checked: 461 nonblank pasted output lines across all `text` transcript blocks:
lines 186-219, 742-779, 1258-1296, 1722-1764, 2400-2509, 2912-2941, 4179-4351, and 4385-4394.

## Findings By Class

### False

1. `SELF_QA_RP7.md:1768-1769` says the round-7 fence transcript proves the GREEN subject is the repaired file at `92853 B / e695a67b...7f32`. The pasted transcript says otherwise: `SELF_QA_RP7.md:1725` records `green_bytes=108301 green_sha256=0e93f90d...921e62`. The prose is stale and contradicts the transcript.

2. `SELF_QA_RP7.md:2552-2556` says the round-5 fence is unchanged except for two GREEN identity constants and that its extracted body is still exactly `20050 B`. The pasted command output records `21263` bytes for `/tmp/rp7-r5-fence-body.sh` at `SELF_QA_RP7.md:197`, repeated as `21263 B` at `SELF_QA_RP7.md:4391`.

3. `SELF_QA_RP7.md:4353-4354` says the round-4 transcript's final identity line is `BASH_N_RC=0 BYTES=77179 SHA256=393a16ce...`. The actual transcript line immediately above is `SELF_QA_RP7.md:4349`, which records `BASH_N_RC=0 BYTES=108301 SHA256=0e93f90d...921e62`.

### Scope-Wrong

1. Several carried-fence summaries say GREEN was re-executed against "round-8 bytes" rather than the current repaired worktree bytes. Representative prose claims: `SELF_QA_RP7.md:1354`, `SELF_QA_RP7.md:1368-1369`, `SELF_QA_RP7.md:1808`, `SELF_QA_RP7.md:1849-1850`, `SELF_QA_RP7.md:2565-2566`, and `SELF_QA_RP7.md:2970-2972`. The pasted transcript identity lines instead show current GREEN bytes/hash: `SELF_QA_RP7.md:1725`, `SELF_QA_RP7.md:2403`, `SELF_QA_RP7.md:2915`, and `SELF_QA_RP7.md:4349` all record `108301 / 0e93f90d...921e62`. This is not just wording: it misstates which artifact the carried-fence evidence covers.

### Unsupported

1. `SELF_QA_RP7.md:4421-4429` claims "the status body is no longer addressed by name at all" and that `wpi_alloc_leaf` is deleted. The round-9 transcript supports the behavioral substitution cases (`SELF_QA_RP7.md:746-749`) and the carried static output reports `green_name_appends=0 green_open_leaf=1` (`SELF_QA_RP7.md:2507`), but no pasted transcript line proves `wpi_alloc_leaf=0` or a zero count for all remaining status-body name-addressed sites. This absolute/deletion claim is not transcript-supported inside this document.

2. `SELF_QA_RP7.md:4375-4380` claims the literal re-run stderr carries exactly six `WRAPPER_STREAM fence=<f> bytes=<n> [<text>]` lines, one per fence, with `bytes=0 []` in a clean run. The literal re-run output block only gives `RUN_ONE_STDERR_BYTES=210` at `SELF_QA_RP7.md:4386`; it does not paste the six stderr lines. The only pasted `WRAPPER_STREAM` output lines in the document are four nested `GREEN WRAPPER_STREAM` lines at `SELF_QA_RP7.md:2480-2483`, not the six-line literal re-run stderr being claimed.

## Most Consequential Finding

The stale carried-fence identity/scope claims are the most consequential. A downstream auditor reading the prose could believe several carried gates were run against round-8 bytes, while their own pasted transcript identities show the current round-9 repaired worktree (`108301 / 0e93f90d...921e62`). That undermines the document's artifact-identity narration even though many individual behavioral rows are transcript-backed.

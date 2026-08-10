# WP-I preregistration draft - Codex defect-catalogue pass

Date: 2026-08-10

Scope: the complete round-1.3 WP-I draft was swept against all ten patterns in
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`. Repairs were applied in place as draft round
1.4. No host contact, execution, authority lift, scope expansion, pinned-placeholder
fill, block implementation, or Git operation was performed.

## Findings and repairs

| ID | Pattern | Draft location | Defect | Repair applied |
|---|---:|---|---|---|
| C01 | 1 | Section 8.2, B2 rows 5-7; B3 rows 10-11 and 15; B1 rows 17-19 | Positively established absence was either left under a generic unreadable STOP or had no explicit outcome, so observable deviant state could be misreported as inability to evaluate. | Split searchable-parent ENOENT/object absence to row-specific FAIL; kept invocation, access, traversal, ambiguous-ENOENT, read and parse failures at STOP. Added valid `LoadState=not-found` as B2 FAIL. |
| C02 | 1 | Section 8.2, B5 row 20 | Every non-200 HTTP result used the same STOP, even when a complete valid response positively observed an unexpected endpoint state. | Kept transport/timeout/malformed results and valid 401/403 at STOP; made every other complete valid non-200 response a B5 FAIL; only a complete 200 proceeds. |
| C03 | 1 | Section 8.2, B6 row 24 | The external TCP row named only connected FAIL and treated refused/timeout as PASS, with no outcome for invocation, local-socket, routing, cancellation, clock or unclassified errors. | Added an explicit `external_probe_not_evaluable` STOP and limited FAIL/PASS to classified completed outcomes. |
| C04 | 2 | Sections 4 and 8.1, P0 rows 8-9 | Successful local identity/filesystem/manager answers were not bound to the named staging guest's externally established user, mount, PID, network and root-mount domain; a container/chroot/visible-PID-1 lookalike could answer. | Required deploy-channel attestation produced outside the ssh login domain, embedded in the frozen P0 block, compared before manager or RO checks, with missing/mismatch as STOP and no local PID-1 inference. |
| C05 | 2 | Section 8.2, B5 rows 20-21 and B6 rows 22-23; namespace rule; section 9 defer list | The service-netns preflight guarded `ss` only. `curl 127.0.0.1` could therefore PASS or FAIL against a different login namespace. | Made the service/caller netns comparison a shared preflight evaluated before both `curl` and `ss`; failure routes both B5 and the listener-set half to RPD-VERIFY. |
| C06 | 3 | Section 8.2, rows 6-7, 10-11, 15 and 17-19; section 10.1 | Leaf metadata/content checks did not bind the full component chain, accepted-vs-unaccepted symlinks, or mount topology, so a decoy reached through an intermediate link or mount could satisfy them. | Added one atomic path-object rule: component-wise non-following metadata, canonical components, numeric ownership, explicit accepted-symlink targets, externally attested mount topology, and STOP-before-leaf ordering. Updated affected rows. |
| C07 | 4 | Section 8 probe execution; section 10.3 RPD-VERIFY step 1 | Evidence children, including future root-authorised RPD helpers, had no binding clean-environment/tool-selection contract. PATH/PYTHONPATH/cwd/TMPDIR influence could select code or mutate a protected location. | Required fixed trusted cwd, cleared environment, fixed locale, pinned absolute helpers/minimal PATH, numeric ownership/mode/kind checks, run-owned TMPDIR and isolated Python. Root-side failure STOPs before child execution. |
| C08 | 5 | Section 8.2, B2 rows 5-6 and B4 row 9 | Candidate binding was textual (`cat` "shows both" roots), `[Install]` used grep, and start mode only "carried" a string. Comments, inactive directives, duplicate/shadowed assignments or substring decoys could pass. | Replaced presence matching with complete structural parsing of effective `ExecStart`, fragment/drop-in set, systemd section grammar and tokenized effective environment; only semantic values may PASS. |
| C09 | 5 | Section 8.2, B5 row 21 | The response-body predicate named fields without requiring strict whole-document JSON, duplicate-key rejection, non-JSON-constant rejection, top-level shape or exact types. | Required complete strict JSON parsing, duplicate-key and NaN/Infinity rejection, required top-level shape and exact typed-field comparison; unreadable/unparseable/schema-unknown states STOP before flag comparison. |
| C10 | 5 | Section 8.2, B6 rows 22-23; general structured-input rule | Listener assertions did not specify a full `ss` table parser, leaving room for substring/partial-row interpretation; other structured records had no single binding grammar rule. | Required complete `ss -H -ltn` row parsing and prohibited substring matching; added a cross-cutting full-grammar rule for JSON, systemd, TSV, digest sets, mount tables and diagnostics. |
| C11 | 6 | Sections 7 and 8 general probe-output precedence; P0 and B6 preflights | STOP-before-stdout applied to a named subset of remote tools but omitted `command -v`, `getent`, `id`, the TCP primitive, close/bind hashing and local/Stage-1 helpers. Two equal partial digest streams could also look closed. | Extended atomic capture/adjudication to every external command and local transport primitive. Required complete rc-0, diagnostic-free enumeration and hashing on both remote and local close/bind halves before comparing stdout. |
| C12 | 7 | Sections 4, 7, 8 and 10.2: transport TSV, digest/path/mount tables and multi-line outputs | No design rule distinguished clean EOF, an unterminated populated final record and hard read error, so a shell loop could admit a truncated or unreadable source. | Added a binding line-reader completion rule and required no-final-newline plus unreadable-source falsifications for every shared reader. |
| C13 | 8 | Section 8.1, P0 rows 1-3 | Executing identity, the dynamically allocated service account and wider-group checks relied on resolver-rendered names rather than the kernel numeric identities on which permissions depend. | Made the named accounts the resolver contracts but required unique complete `getent` parsing: `gatea` must equal its numeric euid/egid, `mtc-bridge` must still resolve to preregistered `999:988`, and numeric `id -G` must exclude gids 0 and 988; names are diagnostic only. |
| C14 | 8 | Sections 1, 2, 8.2 rows 10-11 and 15, 10.1 and 10.3 | Ownership expectations used `root:root`, `gatea:gatea` and `mtc-bridge:mtc-bridge`. In particular, the state-account row could assume uid=gid even though the recorded allocation is uid 999, gid 988. | Preregistered `WPI_STATE_UID=999` and `WPI_STATE_GID=988`; changed host ownership checks to numeric `0:0` or `999:988`; bound run-owned trees to P0's numeric euid:egid; retained names as diagnostics only. |
| C15 | 9 | Section 8, scope-of-claim paragraph; section 10.1 | The conclusion said the trees were "unwritable and byte-consistent with the expected lock," but the probes establish only absence of DAC write bits plus lock digest/installed-set parity. | Narrowed the admitted sentence to the exact probes and explicitly excluded ACL/capability/mount/future-mutation protection and whole-tree byte identity. |
| C16 | 10 | Sections 4 and 5, Stage-1 acceptance and first-FAIL runner evidence | Adversarial "transcript"/"demonstrate" language did not require executable RED/GREEN evidence; prose recipes or reconciled counts could satisfy it without being falsifiable. | Required exact paste-and-run commands with real RED against pre-fix behaviour or deliberate mutation and GREEN with accepted bytes; templates, counts and undeclared shell state are supplemental only. |
| C17 | 10 | Sections 0 and 10.2, path-scope proof | A scan of literal absolute paths cannot fail on a forbidden path assembled from variables or substitutions, yet it was offered as proof of the exhaustive runtime path allowlist. | Replaced literal scanning with a parsed closed-set expansion proof, rejection of unresolved dynamic construction, allowlist comparison after expansion, and a mandatory computed-forbidden-path RED/GREEN falsification. |

## Per-pattern coverage

| Pattern | Result | Coverage note |
|---:|---|---|
| 1 | 3 findings | Checked every PASS/FAIL/STOP row and every error/absence branch for truthful result classification. |
| 2 | 2 findings | Checked user, mount, PID, network and privilege domains for P0, manager, filesystem, loopback status and listener claims. |
| 3 | 1 finding | Checked every host path predicate for full component-chain, symlink, canonical-path and mount binding. |
| 4 | 1 finding | Checked all current and deferred child-process launch contracts for PATH, interpreter, cwd, environment and TMPDIR influence. |
| 5 | 3 findings | Checked JSON, unit files/properties, TSV, digest/mount tables, socket tables and diagnostics for whole-input grammatical parsing rather than matching. |
| 6 | 1 finding | Checked every interpreted output, including P0, Stage 1, remote, operator-local and evidence-close paths, for status/diagnostics-before-stdout ordering. |
| 7 | 1 finding | Checked every described line/table reader for clean EOF, final-record and hard-read-error separation. |
| 8 | 2 findings | Checked executing identities, group membership and all ownership predicates for numeric kernel identity; verified the seeded 999:988 service-account case. |
| 9 | 1 finding | Compared every conclusion and mechanism label with the narrower predicate actually described. |
| 10 | 2 findings | Checked acceptance transcripts, demonstrations, counts and static proofs for a real falsifiable failure mode and literal re-executability. |

No pattern was clean; therefore there are no per-pattern "no instance found" notes.

CATALOGUE-PASS-COMPLETE: 17 findings repaired, 0 patterns clean

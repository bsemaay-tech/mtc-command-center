# R16 and R23 freeze procedures — version 2

Status: FREEZE PROCEDURES V2 - SUPERSEDES V1 - NOT ACCEPTED

| Review finding | Where v2 closes it | Mechanical closure |
|---|---|---|
| **F1 — R23 was not executable or ceremony-specific** | §7 and §8 | R16 and R23 have different required schemas, variables, role sets, output names, and complete command sequences. Shared helpers require a literal `R16` or `R23` ceremony value and reject cross-ceremony rows. R23 never says “run R16 step.” |
| **F2 — the freeze moments could still be confused** | §3.2, §6.2, §8.2–§8.4 | R23 derives the prior R16 SHA only from a verified R16 manifest obtained through the independently anchored R16 publication source; it does not accept an operator-supplied R16 SHA. It also binds a uniquely parsed accepting Audit-2 close record that names the same R16 manifest and SHA before any R23 manifest may be published. |
| **F3 — identities were ambiguous or absent** | §4, §5, §7.4, §8.3–§8.7 | Every identity row carries ceremony, role, derivation mode, canonical namespace, canonical path, blob OID or `-`, bytes, and SHA-256. Tracked text uses `GIT_OBJECT` and pins its blob OID; anything consumed from a checkout also has `WORKTREE_RAW`; external files retain immutable-root identity plus root-relative path. Diff, input, close, index, order, and manifest identities use the same schema. |
| **F4 — the unchanged claim was wider than its proof** | §5.2, §7.5–§7.6, §9.1 | The scope is the exact set in an independently anchored authority universe, not a freezer-authored list. The copied universe bytes are manifest members. Before/after identity rows are emitted for every row selected for continuity. The conclusion quantifies only that exact set and exact modes; if any scope row is outside the compared set, v2 prints `NO_OVERALL_UNCHANGED_CLAIM`. |
| **F5 — WP-A continuity compared against freezer-supplied values** | §5.5, §8.5–§8.6 | There are no `$WpaArtifactBytes`, `$WpaArtifactSha256`, or operator-supplied artifact-path inputs. R23 parses the independently frozen capture-time index, derives the selector from the bound event ledger, requires exactly one `GIT_OBJECT` row and exactly one `WORKTREE_RAW` row, preserves those source rows verbatim, and compares the final artifact in the same modes. Zero, duplicate, cross-path, cross-SHA, or mismatching rows stop publication. |
| **F6 — recomputation was stronger than truth/completeness** | §3, §6, §9 | The auditor obtains authority roots directly, proves exact-set equality against the frozen scope universe, verifies the R16/Audit-2/WP-A chronology from separately anchored machine-readable records, reopens every source record by its namespaced identity, and independently repeats the WP-A row extraction. The procedure explicitly distinguishes “record integrity and cross-record consistency” from “real-world event truth” and stops if no independent event authority exists. |

The review required these six repairs. In particular, it identified R16-step reuse in R23, an unbound R16 ancestor, an unused Audit-2 close, ambiguous text identities, an unbound scope universe, freezer-supplied WP-A expectations, and chronology inferred only from narrative records. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:13-81`

## 1. Purpose, status, and authority boundary

This document is the complete v2 procedure for two different local evidence ceremonies:

- **R16** freezes the full pre-WP-A checkpoint after immutable Packet-9/WP-I closure. Packet 10 and Audit 2 consume that already-frozen checkpoint; Audit 2 does not create it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-67,119-122`
- **R23** freezes the later final exact release SHA/artifact only after an accepting Audit-2 close, WP-A completion and evidence capture, and the separately recorded discard boundary. It is distinct from R16 and is the subject of Audit 3/Gate 6. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60-64`; `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-980`

This procedure creates no gate verdict, acceptance, authorization, host action, network action, credential use, deployment, service action, broker/exchange action, ARM/order action, TESTNET/mainnet action, Pine/parity/MTC/trading action, merge, push, or economic action. It is local procedure material only. The readiness package itself grants no such authority. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:30-37`

Audit classification for this rewrite: **T2 overall** (documentation/evidence). Because F5 governs deployed-artifact identity, that finding requires the repository policy's single-flagship T1 identity verification before this document can be accepted. No such acceptance is claimed here.

## 2. Governing proof rule

Every check below has an external expected value, an exact quantified universe, and an enforced stop or changed result. The governing question is:

> What concrete false world makes this check fail?

The recurring defect record explains why a comparison is decorative when the checked party supplies both the artifact and its expected value, and requires reviewers to ask where the expectation came from, what is outside the universe, and whether the property is enforced. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-65`

For this procedure:

1. An **independent source** means a source frozen before the freezer starts, selected by a Lead/owner-adopted kickoff or equivalent authority record, and delivered directly to both freezer and auditor. A path or digest typed by the freezer is not an independent source.
2. An **authority anchor** is either:
   - a tracked record pinned by full commit SHA plus repo-relative path and verified as `GIT_OBJECT` with blob OID; or
   - an external create-once/read-only publication identified by immutable root/version identity plus a root manifest whose identity is supplied by the independent publisher.
3. A detached digest proves only consistency with the bytes beside it. It is not a trust root. The authority anchor selects the trusted detached record and manifest.
4. If an expected source, authority anchor, schema, unique selector, or recomputation path is absent, the outcome is **STOP / NOT PUBLISHABLE**, never PASS and never an inferred value.
5. Hashing a narrative record proves its current bytes, not that its narrative is true. Chronology is publishable only when separately anchored event records expose machine-readable event IDs, sequence numbers, UTC instants, subject identities, and cross-references that can be compared. Even then, the exact claim is “the independently anchored records are mutually consistent,” not “the freezer personally observed the events.”

The auditor-input contract already says copied digest strings alone are insufficient and requires access to immutable evidence for recomputation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`

## 3. Present `UNKNOWN` register and the exact facts that would settle it

These values are not established by the read sources. They must not be guessed.

| ID | Present state | Exact fact that settles it |
|---|---|---|
| U-R16-BASE | **UNKNOWN** — the future R16 comparison-base SHA is not named. | A pre-ceremony Lead/owner-adopted authority record naming the full base commit SHA. The upstream contract requires a base and exact diff but does not select the future base. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-56` |
| U-R16-UNIVERSE | **UNKNOWN** — no independently anchored final R16 scope-universe file, root identity, or authority-anchor identity exists in the read sources. | A frozen `R16_SCOPE_AUTHORITY.tsv` satisfying §5.2, plus an authority anchor published before R16 and delivered independently. It must enumerate every in-scope file and every artifact/manifest mode; Packet 10 requires that complete membership. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-61` |
| U-P9-PATHS | **UNKNOWN** — future Packet-9 closure/index paths and identities do not yet exist. | Immutable Packet-9 closure and final evidence index, each present in the R16 authority universe with an unambiguous identity. Packet 9 requires both. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39-41` |
| U-R16-PUBLICATION | **UNKNOWN** — no actual R16 publication root, manifest, detached manifest identity, or R16 SHA exists. | A completed §7 run whose publication root is independently anchored after creation. |
| U-A2-CLOSE | **UNKNOWN** — the future accepting Audit-2 close path, storage form, schema, and identity are not established. | A close source satisfying §5.3, independently anchored, with exactly one accepting row that binds the actual R16 SHA and R16 manifest identity. The review specifically records the tracked-versus-external form as unknown. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:39-45` |
| U-R23-UNIVERSE | **UNKNOWN** — no independently anchored final R23 scope universe exists. | A frozen `R23_SCOPE_AUTHORITY.tsv` satisfying §5.2, selected before R23 by an independent authority anchor. |
| U-WPA-ROOT | **UNKNOWN** — no immutable capture-time WP-A evidence root identity or capture manifest is defined by the read sources. | A capture-time root publication satisfying §5.4: immutable root identity, exact manifest, independently anchored manifest identity, direct read path, no missing/extra member, and a machine-readable artifact index. The plan requires captured evidence but does not define this identity schema. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:974-977,1021-1025` |
| U-WPA-INDEX | **UNKNOWN** — trusted WP-A artifact-identity source, selector, actual artifact ID/path/SHA/modes, and extraction rule do not currently exist. | The §5.5 index schema, exactly one selected `GIT_OBJECT` row and one selected `WORKTREE_RAW` row, and the §8.5 extraction. The selector's `artifact_id` and `tested_sha` must come from the independently anchored event ledger, not freezer variables. This is the specific missing fact identified by F5. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:59-69` |
| U-EVENTS | **UNKNOWN** — there is no independently anchored machine-readable R16/Audit-2/WP-A/evidence/discard chronology ledger in the read sources. | The §5.6 event ledger plus independently anchored source records for every required event. Narrative order alone is insufficient. F6 identifies this exact weakness. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:71-81` |
| U-R23-SHA | **UNKNOWN** — the future final SHA, final artifact identity, and final scope are not established. | A completed §8 run after every prior unknown is settled and every required comparison is true. |
| U-STORAGE | **UNKNOWN** — the sources do not choose an external create-once/WORM publication mechanism or root namespace. | A Lead/owner-adopted local storage contract naming the immutable root/version mechanism and independent access path. This document does not select or authorize one. |

**Current operational consequence:** neither R16 nor R23 is presently publishable from the sources read for this rewrite. That is a truthful STOP, not an incomplete procedure. The commands below become executable only after the named independent inputs exist.

## 4. Identity model — mandatory for every row

The repository declares `* text=auto`, so Git-object LF bytes and Windows working-tree bytes may differ. `.gitattributes:1-2` A prior identity table mixed these forms and became impossible to reproduce by one derivation method. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27`

Every identity table in R16 and R23 therefore uses this exact header:

```text
ceremony	role	mode	namespace	path	blob_oid	bytes	sha256
```

Rules:

- `ceremony` is exactly `R16` or `R23`.
- `mode` is exactly one of:
  - `GIT_OBJECT`: `namespace=REPO@<full-commit-sha>`, repo-relative `/`-separated path, mandatory blob OID, blob byte count, SHA-256 of blob bytes.
  - `WORKTREE_RAW`: `namespace=WORKTREE@<full-commit-sha>@<materialization-id>`, repo-relative path, `blob_oid=-`, raw file byte count and SHA-256.
  - `RAW_EXTERNAL_FILE`: `namespace=EXTERNAL_ROOT@<immutable-root-id>`, root-relative path, `blob_oid=-`, raw file byte count and SHA-256.
- No absolute path appears in `path`; the absolute source root is recorded separately in the command transcript. `path` is canonical root-relative with `/`, no `.` or `..`, no empty component, and no basename-only collapse.
- Every tracked file has a `GIT_OBJECT` row. Every tracked artifact, manifest, or text record consumed from a checkout also has a `WORKTREE_RAW` row. External files have `RAW_EXTERNAL_FILE` rows and remain bound to their immutable root namespace.
- A diff, scope input, evidence index, event ledger, close record, bundle manifest, and detached manifest identity are files and follow the same rule. No table may publish bare bytes/SHA-256.
- The standing repository rule is to state derivation mode and either publish both forms or pin the Git blob OID. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:48-64`

## 5. Normative input schemas

### 5.1 Authority-source descriptor

Each independent input arrives with one pre-ceremony descriptor selected by the adopted kickoff, not by a freezer variable:

```text
authority_id	ceremony	role	mode	namespace	path	blob_oid	bytes	sha256	published_at_utc
```

The descriptor must have exactly one row for the subject it selects. Its own authority anchor is recorded in the kickoff. The freezer and auditor obtain it separately and require byte equality. Zero or multiple descriptor rows, an unanchored descriptor, or a freezer-created descriptor is STOP.

### 5.2 R16 and R23 authoritative scope universes

Exact header:

```text
ceremony	universe_id	role	mode	namespace	path	continuity
```

- `ceremony` is exactly the ceremony being run.
- `universe_id` is identical and nonempty on every row.
- R16 roles are exactly `scope`, `artifact`, `manifest`, `packet9_close`, or `packet9_index`.
- R23 scope roles are exactly `final_scope`, `final_artifact`, or `final_manifest`. The accepting Audit-2 close is a mandatory, separately anchored boundary input under §5.3 and §8.3; it is not forced into the tracked-repository scope when its future storage form is still `UNKNOWN`.
- `mode` is `GIT_OBJECT` or `WORKTREE_RAW`; every tracked path has exactly one `GIT_OBJECT` row. Artifact/manifest paths consumed from the checkout also have exactly one `WORKTREE_RAW` row.
- `namespace` is `REPO_RELATIVE` at authority time; the procedure replaces it with the resolved commit/materialization namespace in derived identity rows.
- `continuity` is exactly `required` or `not_claimed`.
- Duplicate `(role,mode,path)` rows, duplicate logical roles for the same `(mode,path)`, missing mandatory roles, placeholders, absolute paths, `.`/`..`, or an empty universe are STOP.

The freezer does not supply a second scope list. It copies the independently anchored universe byte-for-byte into the output and derives all loops from that copy. Exact-set equality is therefore structural: there is only one admitted universe.

An `UNCHANGED` conclusion is permitted only when every `continuity=required` row has a before and after identity in the same mode and every comparison matches. If any universe row is `not_claimed`, the output must also say `NO_OVERALL_UNCHANGED_CLAIM`; it may state equality only for the named required subset. This deliberately narrows the sentence to the probe, matching the defect catalogue's claim-width rule. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-613`

### 5.3 Accepting Audit-2 close

Exact machine-readable header:

```text
record_kind	audit_cycle_id	verdict	r16_freeze_sha	r16_manifest_sha256	closed_at_utc
```

Requirements:

- Exactly one data row; `record_kind=AUDIT2_CLOSE`.
- `verdict` is exactly `PASS` or `PASS-WITH-NITS`.
- `r16_freeze_sha` is full-length and equals the SHA extracted from the verified R16 publication.
- `r16_manifest_sha256` equals the independently recomputed R16 manifest SHA-256.
- `closed_at_utc` is strict UTC ISO-8601 (`yyyy-MM-ddTHH:mm:ss.fffffffZ`).
- The close file itself is identified as `GIT_OBJECT` plus `WORKTREE_RAW` if tracked/checkout-consumed, or `RAW_EXTERNAL_FILE` under an immutable root if external. The chosen form and actual path remain `UNKNOWN` until the close is produced.
- The close source must point to the independently sealed required auditor verdict records. R23 verifies those members exist under their independently anchored identities; it does not decide acceptance itself.

### 5.4 WP-A capture-time root manifest

Exact header:

```text
capture_id	mode	namespace	path	blob_oid	bytes	sha256
```

Every retained evidence member appears exactly once as `RAW_EXTERNAL_FILE`, with `namespace=EXTERNAL_ROOT@<immutable-capture-root-id>` and a root-relative canonical path. The manifest must include the §5.5 artifact index and the §5.6 event ledger. The independently published authority descriptor binds this manifest at capture close. R23 re-enumerates the root and requires exact equality of `(path,bytes,sha256)` with no missing, extra, duplicate, or unreadable member before reading any claimed result.

This closes the temporal gap in v1: enumeration at R23 time is compared with the independently frozen capture-time set, not merely hashed for the first time at R23.

### 5.5 WP-A tested-artifact index — required future schema and extraction rule

The trusted source is presently **UNKNOWN**. The following is the schema that would settle it:

```text
record_kind	capture_id	artifact_id	repo_relative_path	mode	tested_sha	blob_oid	bytes	sha256
```

Normative rules:

1. The file is a member of the verified §5.4 capture root and is parsed only after the root exact-set check succeeds.
2. The selector is not typed by the freezer. `capture_id`, `artifact_id`, and `tested_sha` are extracted from the unique `WPA_COMPLETED` row in the independently anchored §5.6 event ledger.
3. Select rows where all of these equalities hold: `record_kind=WP_A_TESTED_ARTIFACT`, matching `capture_id`, matching `artifact_id`, and matching `tested_sha`.
4. Require exactly one selected `GIT_OBJECT` row and exactly one selected `WORKTREE_RAW` row. Require the same canonical `repo_relative_path` in both. Require a valid blob OID only on the Git row and `blob_oid=-` only on the raw row.
5. Zero rows, more than one row for either mode, a third mode, different paths, a SHA mismatch, malformed numeric bytes, malformed lowercase SHA-256, or a placeholder is STOP.
6. Preserve the header and the two selected source lines byte-for-byte in `R23_WPA_EXPECTED_ROWS.tsv`. Do not retype or reserialize their expected values.
7. Recompute the final R23 `GIT_OBJECT` identity at `R23_FREEZE_SHA` and `WORKTREE_RAW` identity from the R23 checkout for that derived path. Compare mode to same mode. Both must match the preserved expected rows before an R23 publication manifest may exist.

This rule removes all freezer-supplied expected artifact values. The review identified the absence of exactly this unique-row derivation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:59-69`

### 5.6 Independently anchored event ledger

Exact header:

```text
ceremony	event_id	sequence	occurred_at_utc	source_mode	source_namespace	source_path	source_blob_oid	source_bytes	source_sha256	r16_freeze_sha	r16_manifest_sha256	capture_id	artifact_id	tested_sha	verdict
```

Required unique event IDs and strict order:

```text
R16_FROZEN
AUDIT2_CLOSED_ACCEPTING
WPA_BEGAN
WPA_COMPLETED
WPA_EVIDENCE_CAPTURE_CLOSED
STAGING_DISCARD_RECORDED
```

Rules:

- Exactly one row per required event ID and no unknown event ID in the R23 ceremony slice.
- Integer `sequence` values are strictly increasing in the listed order with no duplicate.
- UTC instants are parseable and nondecreasing in the listed order; equality is allowed only when two records deliberately share the same captured instant and their sequence still orders them.
- Every row identifies its underlying source record using the §4 mode/namespace/path/OID/bytes/SHA rules. The auditor independently reopens and hashes every source record.
- `AUDIT2_CLOSED_ACCEPTING` has an accepting verdict and the same R16 SHA/manifest identity as §5.3.
- `WPA_COMPLETED` supplies the unique `capture_id`, `artifact_id`, and `tested_sha` selector used by §5.5.
- `WPA_EVIDENCE_CAPTURE_CLOSED` names the same `capture_id` as the verified capture manifest.
- `STAGING_DISCARD_RECORDED` must follow WP-A completion and evidence capture close. The governing plan requires discard only after both. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:974-977,1021-1023`

This ledger can prove integrity and consistency of independently anchored records. It cannot, by itself, prove that an untrusted author told the truth. Therefore the authority descriptor must identify an independent event publisher/source root and the auditor must receive it directly. If no such authority exists, chronology truth is **UNKNOWN** and R23 stops. Hashes over freezer-written chronology are forbidden.

## 6. Shared PowerShell prelude

The following prelude is normative for both procedures. It performs local reads/writes and read-only Git inspection only. It does not contact any host or network.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Utf8Lf {
    param([Parameter(Mandatory)][string]$Path,
          [Parameter(Mandatory)][string[]]$Lines)
    $utf8 = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($Path, (($Lines -join "`n") + "`n"), $utf8)
}

function Copy-ExactFile {
    param([Parameter(Mandatory)][string]$Source,
          [Parameter(Mandatory)][string]$Destination)
    [IO.File]::WriteAllBytes($Destination, [IO.File]::ReadAllBytes($Source))
}

function Assert-NoPlaceholder {
    param([Parameter(Mandatory)][string]$Value,
          [Parameter(Mandatory)][string]$Name)
    if ([string]::IsNullOrWhiteSpace($Value) -or
        $Value -match '(?i)(UNKNOWN|NOT-YET-AVAILABLE|<[^>]+>|TBD|PLACEHOLDER)') {
        throw "STOP missing-or-placeholder $Name"
    }
}

function Assert-CanonicalRelativePath {
    param([Parameter(Mandatory)][string]$Path)
    if ([IO.Path]::IsPathRooted($Path) -or $Path.Contains('\') -or
        $Path -match '(^|/)(\.|\.\.)(/|$)' -or $Path -match '(^|/)$' -or
        [string]::IsNullOrWhiteSpace($Path)) {
        throw "STOP noncanonical-relative-path $Path"
    }
}

function Get-RawIdentity {
    param([Parameter(Mandatory)][string]$LiteralPath,
          [Parameter(Mandatory)][ValidateSet('WORKTREE_RAW','RAW_EXTERNAL_FILE')][string]$Mode,
          [Parameter(Mandatory)][string]$Ceremony,
          [Parameter(Mandatory)][string]$Role,
          [Parameter(Mandatory)][string]$Namespace,
          [Parameter(Mandatory)][string]$DisplayPath)
    Assert-CanonicalRelativePath $DisplayPath
    $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    if ($item.PSIsContainer) { throw "STOP identity-subject-is-directory $LiteralPath" }
    [pscustomobject]@{
        ceremony=$Ceremony; role=$Role; mode=$Mode; namespace=$Namespace
        path=$DisplayPath; blob_oid='-'; bytes=[int64]$item.Length
        sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}

function Get-GitBlobIdentity {
    param([Parameter(Mandatory)][string]$Repo,
          [Parameter(Mandatory)][string]$Rev,
          [Parameter(Mandatory)][string]$Path,
          [Parameter(Mandatory)][string]$Ceremony,
          [Parameter(Mandatory)][string]$Role)
    Assert-CanonicalRelativePath $Path
    $resolved = (& git -C $Repo rev-parse --verify "$Rev^{commit}").Trim()
    if ($LASTEXITCODE -ne 0 -or $resolved -notmatch '^[0-9a-f]{40,64}$') {
        throw "STOP unresolved-commit $Rev"
    }
    $spec = "${resolved}:$Path"
    $oid = (& git -C $Repo rev-parse --verify $spec).Trim()
    if ($LASTEXITCODE -ne 0 -or $oid -notmatch '^[0-9a-f]{40,64}$') {
        throw "STOP unresolved-blob $spec"
    }
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = 'git'; $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
    foreach ($arg in @('-C',$Repo,'cat-file','blob',$spec)) { [void]$psi.ArgumentList.Add($arg) }
    $proc = [Diagnostics.Process]::Start($psi)
    $buffer = [IO.MemoryStream]::new()
    $proc.StandardOutput.BaseStream.CopyTo($buffer)
    $stderr = $proc.StandardError.ReadToEnd(); $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "STOP git-cat-file-failed $stderr" }
    $bytes = $buffer.ToArray(); $hash = [Security.Cryptography.SHA256]::Create()
    try { $sha = [Convert]::ToHexString($hash.ComputeHash($bytes)).ToLowerInvariant() }
    finally { $hash.Dispose(); $buffer.Dispose() }
    [pscustomobject]@{
        ceremony=$Ceremony; role=$Role; mode='GIT_OBJECT'; namespace="REPO@$resolved"
        path=$Path; blob_oid=$oid; bytes=[int64]$bytes.Length; sha256=$sha
    }
}

function Read-StrictTsv {
    param([Parameter(Mandatory)][string]$Path,
          [Parameter(Mandatory)][string[]]$Columns)
    $text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    if ($text.Contains("`r") -or -not $text.EndsWith("`n")) {
        throw "STOP TSV-must-be-UTF8-LF-final-newline $Path"
    }
    $lines = @($text.Substring(0,$text.Length-1) -split "`n")
    if ($lines.Count -lt 2) { throw "STOP empty-TSV $Path" }
    $header = @($lines[0] -split "`t",-1)
    if (($header -join "`t") -ne ($Columns -join "`t") -or
        (@($header | Sort-Object -Unique).Count -ne $header.Count)) {
        throw "STOP wrong-or-duplicate-TSV-header $Path"
    }
    $out = [Collections.Generic.List[object]]::new()
    for ($i=1; $i -lt $lines.Count; $i++) {
        $parts = @($lines[$i] -split "`t",-1)
        if ($parts.Count -ne $Columns.Count -or @($parts | Where-Object { $_ -eq '' }).Count -gt 0) {
            throw "STOP malformed-TSV-row line=$($i+1) path=$Path"
        }
        $map = [ordered]@{}
        for ($j=0; $j -lt $Columns.Count; $j++) { $map[$Columns[$j]]=$parts[$j] }
        $map['_raw_line']=$lines[$i]
        [void]$out.Add([pscustomobject]$map)
    }
    @($out)
}

function Format-IdentityRow {
    param([Parameter(Mandatory)]$Identity)
    "$($Identity.ceremony)`t$($Identity.role)`t$($Identity.mode)`t$($Identity.namespace)`t$($Identity.path)`t$($Identity.blob_oid)`t$($Identity.bytes)`t$($Identity.sha256)"
}

function Assert-CleanExactWorktree {
    param([Parameter(Mandatory)][string]$Repo,
          [Parameter(Mandatory)][string]$ExpectedSha,
          [Parameter(Mandatory)][string]$Label)
    $head = (& git -C $Repo rev-parse --verify 'HEAD^{commit}').Trim()
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedSha) { throw "STOP $Label-head-mismatch" }
    $status = @(& git -C $Repo status --porcelain=v1 --untracked-files=all)
    if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) { throw "STOP $Label-worktree-not-clean" }
}

function Assert-ExactStringSet {
    param([Parameter(Mandatory)][string[]]$Expected,
          [Parameter(Mandatory)][string[]]$Actual,
          [Parameter(Mandatory)][string]$Label)
    $e=@($Expected|Sort-Object -Unique); $a=@($Actual|Sort-Object -Unique)
    if ($e.Count -ne $Expected.Count -or $a.Count -ne $Actual.Count -or
        ($e -join "`n") -ne ($a -join "`n")) { throw "STOP exact-set-mismatch $Label" }
}
```

### 6.1 Required execution evidence

For each ceremony, record the literal script bytes, command line, PowerShell version, Git version, absolute input roots, authority descriptor identities, stdout, stderr, return code, start/end UTC, and output-root absolute path in an external transcript. The transcript is itself a manifested `RAW_EXTERNAL_FILE`. An edited template or command requiring substitutions after execution is not evidence; the defect catalogue requires literal reproducibility. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`

### 6.2 Ceremony non-conflation invariant

Before any output is created:

- R16 requires `ceremony=R16` in its authority descriptor and every universe row and rejects every R23 role.
- R23 requires `ceremony=R23` in its authority descriptor, universe, and event ledger and rejects every R16 output label except the explicitly namespaced copied prior-R16 inputs.
- R23 has no `$R16FreezeSha` input. It derives that SHA from the verified prior R16 publication (§8.2).
- R23 has no freezer-supplied `$WpaArtifactPath`, `$WpaArtifactBytes`, or `$WpaArtifactSha256` input. It derives all four identity fields and the path from §5.5 (§8.5).
- The R23 required-member set contains the verified prior R16 manifest, its detached identity, the accepting Audit-2 close, WP-A capture manifest/index, event ledger, and derived expected rows. R16's set cannot contain any of those post-R16 members.

What makes this fail: one wrong ceremony token, one wrong role, a missing prior-boundary member, or an R16-only label in an R23 output. Those are structural comparisons, not warnings.

## 7. R16 — complete pre-WP-A checkpoint procedure

### 7.1 R16 inputs

The adopted kickoff must name all of these literal values before execution:

```powershell
$R16Repo                         = '<isolated clean worktree at proposed R16 commit>'
$R16CandidateRepo                = '<separate clean worktree at candidate commit>'
$R16Out                          = '<new external create-once R16 output directory>'
$R16BaseSha                      = '<full independently adopted comparison-base SHA>'
$R16CandidateSha                 = '<full independently adopted candidate SHA>'
$R16ScopeAuthorityFile           = '<independently anchored R16_SCOPE_AUTHORITY.tsv>'
$R16ScopeAuthorityDescriptor     = '<independently anchored authority descriptor>'
$R16ExternalRootId               = '<immutable publication-root identity reserved for this run>'
```

No field may remain a placeholder. In the present record, the base, authority universe, future Packet-9 paths, and storage root are `UNKNOWN`; §3 defines what settles each.

### 7.2 Validate independent authority and create the R16 root

```powershell
foreach ($pair in @(
    @($R16Repo,'R16Repo'), @($R16CandidateRepo,'R16CandidateRepo'),
    @($R16Out,'R16Out'), @($R16BaseSha,'R16BaseSha'),
    @($R16CandidateSha,'R16CandidateSha'), @($R16ScopeAuthorityFile,'R16ScopeAuthorityFile'),
    @($R16ScopeAuthorityDescriptor,'R16ScopeAuthorityDescriptor'),
    @($R16ExternalRootId,'R16ExternalRootId'))) { Assert-NoPlaceholder $pair[0] $pair[1] }

$descriptorColumns=@('authority_id','ceremony','role','mode','namespace','path','blob_oid','bytes','sha256','published_at_utc')
$r16Descriptor=@(Read-StrictTsv $R16ScopeAuthorityDescriptor $descriptorColumns)
if ($r16Descriptor.Count -ne 1 -or $r16Descriptor[0].ceremony -ne 'R16' -or
    $r16Descriptor[0].role -ne 'scope_authority') { throw 'STOP wrong-R16-authority-descriptor' }
$authorityId=$r16Descriptor[0].authority_id
$authorityId | Assert-NoPlaceholder -Name 'R16 authority_id'

$authorityRaw=Get-RawIdentity $R16ScopeAuthorityFile 'RAW_EXTERNAL_FILE' 'R16' `
    'scope_authority_source' $r16Descriptor[0].namespace $r16Descriptor[0].path
if ($authorityRaw.bytes -ne [int64]$r16Descriptor[0].bytes -or
    $authorityRaw.sha256 -ne $r16Descriptor[0].sha256) { throw 'STOP R16-authority-bytes-mismatch' }

if (Test-Path -LiteralPath $R16Out) { throw 'STOP R16-output-already-exists' }
[void](New-Item -ItemType Directory -Path $R16Out)
Copy-ExactFile $R16ScopeAuthorityFile (Join-Path $R16Out 'R16_SCOPE_AUTHORITY.tsv')
Copy-ExactFile $R16ScopeAuthorityDescriptor (Join-Path $R16Out 'R16_SCOPE_AUTHORITY_DESCRIPTOR.tsv')
```

The descriptor is independently selected before the freezer starts. If the freezer changes the copied universe, the copied file identity differs from the descriptor and the run stops.

### 7.3 Resolve commits, worktrees, and exact R16 universe

```powershell
$R16FreezeSha=(& git -C $R16Repo rev-parse --verify 'HEAD^{commit}').Trim()
$R16ResolvedBase=(& git -C $R16Repo rev-parse --verify "$R16BaseSha^{commit}").Trim()
$R16ResolvedCandidate=(& git -C $R16Repo rev-parse --verify "$R16CandidateSha^{commit}").Trim()
foreach($sha in @($R16FreezeSha,$R16ResolvedBase,$R16ResolvedCandidate)) {
    if($sha -notmatch '^[0-9a-f]{40,64}$'){ throw 'STOP R16-unresolved-commit' }
}
Assert-CleanExactWorktree $R16Repo $R16FreezeSha 'R16-freeze'
Assert-CleanExactWorktree $R16CandidateRepo $R16ResolvedCandidate 'R16-candidate'

$scopeColumns=@('ceremony','universe_id','role','mode','namespace','path','continuity')
$r16Rows=@(Read-StrictTsv (Join-Path $R16Out 'R16_SCOPE_AUTHORITY.tsv') $scopeColumns)
if($r16Rows.Count -eq 0 -or @($r16Rows|Where-Object ceremony -ne 'R16').Count -gt 0){throw 'STOP R16-universe-ceremony'}
$universeIds=@($r16Rows.universe_id|Sort-Object -Unique)
if($universeIds.Count -ne 1){throw 'STOP R16-universe-id-count'}
$allowedR16Roles=@('scope','artifact','manifest','packet9_close','packet9_index')
foreach($row in $r16Rows){
    if($row.role -notin $allowedR16Roles -or $row.mode -notin @('GIT_OBJECT','WORKTREE_RAW') -or
       $row.namespace -ne 'REPO_RELATIVE' -or $row.continuity -notin @('required','not_claimed')){
        throw "STOP invalid-R16-universe-row $($row._raw_line)"
    }
    Assert-CanonicalRelativePath $row.path
}
$keys=@($r16Rows|ForEach-Object{"$($_.role)|$($_.mode)|$($_.path)"})
if(@($keys|Sort-Object -Unique).Count -ne $keys.Count){throw 'STOP duplicate-R16-universe-row'}
if(@($r16Rows|Where-Object role -eq 'packet9_close').Count -lt 1 -or
   @($r16Rows|Where-Object role -eq 'packet9_index').Count -lt 1 -or
   @($r16Rows|Where-Object role -eq 'artifact').Count -lt 1 -or
   @($r16Rows|Where-Object role -eq 'manifest').Count -lt 1){throw 'STOP missing-R16-mandatory-role'}

Write-Utf8Lf (Join-Path $R16Out 'R16_COMMITS.tsv') @(
 'ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256',
 "R16`tfreeze_commit`tGIT_COMMIT`tREPO@$R16FreezeSha`t-`t$R16FreezeSha`t-`t-",
 "R16`tbase_commit`tGIT_COMMIT`tREPO@$R16ResolvedBase`t-`t$R16ResolvedBase`t-`t-",
 "R16`tcandidate_commit`tGIT_COMMIT`tREPO@$R16ResolvedCandidate`t-`t$R16ResolvedCandidate`t-`t-"
)
```

`GIT_COMMIT` is used only in the commit table, not in file identity rows. It prevents a commit identifier from being misread as a file byte identity.

### 7.4 Publish the exact diff, tracked tree, and unambiguous identities

```powershell
$r16Patch=Join-Path $R16Out 'R16_BASE_TO_FREEZE.patch'
& git -C $R16Repo --no-pager diff --binary --full-index --no-ext-diff `
    --output=$r16Patch $R16ResolvedBase $R16FreezeSha --
if($LASTEXITCODE -ne 0){throw 'STOP R16-base-diff-generation'}
& git -C $R16Repo --no-pager diff --quiet --no-ext-diff $R16ResolvedBase $R16FreezeSha --
$r16BaseDiffRc=$LASTEXITCODE
if($r16BaseDiffRc -notin 0,1){throw 'STOP R16-base-diff-evaluation'}
$patchId=Get-RawIdentity $r16Patch 'RAW_EXTERNAL_FILE' 'R16' 'base_to_freeze_patch' `
    "EXTERNAL_ROOT@$R16ExternalRootId" 'R16_BASE_TO_FREEZE.patch'
Write-Utf8Lf (Join-Path $R16Out 'R16_BASE_TO_FREEZE_IDENTITY.tsv') @(
 'ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256',
 (Format-IdentityRow $patchId)
)
Write-Utf8Lf (Join-Path $R16Out 'R16_BASE_TO_FREEZE_RESULT.tsv') @(
 'ceremony`tcomparison`tbefore_sha`tafter_sha`tdiff_rc',
 "R16`tR16_BASE_TO_FREEZE`t$R16ResolvedBase`t$R16FreezeSha`t$r16BaseDiffRc"
)

$treeLines=@(& git -C $R16Repo ls-tree -r --full-tree $R16FreezeSha)
if($LASTEXITCODE -ne 0){throw 'STOP R16-tree-enumeration'}
Write-Utf8Lf (Join-Path $R16Out 'R16_FULL_TRACKED_TREE.txt') $treeLines

$identityLines=[Collections.Generic.List[string]]::new()
[void]$identityLines.Add('ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256')
foreach($row in $r16Rows){
    if($row.mode -eq 'GIT_OBJECT'){
        $id=Get-GitBlobIdentity $R16Repo $R16FreezeSha $row.path 'R16' $row.role
    } else {
        $id=Get-RawIdentity (Join-Path $R16Repo $row.path) 'WORKTREE_RAW' 'R16' $row.role `
            "WORKTREE@$R16FreezeSha@R16_FREEZE" $row.path
    }
    [void]$identityLines.Add((Format-IdentityRow $id))
}
Write-Utf8Lf (Join-Path $R16Out 'R16_FROZEN_SCOPE_IDENTITIES.tsv') $identityLines
```

The diff identity explicitly says `RAW_EXTERNAL_FILE`; the Packet-9 close/index and all tracked text are pinned as Git blobs, with raw rows as required by the authority universe. This satisfies Packet 10's exact diff, file-list, and identity requirements. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-61`

### 7.5 Produce before/after identities for the entire declared continuity set

```powershell
$comparison=[Collections.Generic.List[string]]::new()
[void]$comparison.Add('ceremony`tuniverse_id`trole`tmode`tpath`tbefore_namespace`tbefore_blob_oid`tbefore_bytes`tbefore_sha256`tafter_namespace`tafter_blob_oid`tafter_bytes`tafter_sha256`tmatch')
foreach($row in $r16Rows){
    if($row.continuity -ne 'required'){continue}
    if($row.mode -eq 'GIT_OBJECT'){
        $before=Get-GitBlobIdentity $R16Repo $R16ResolvedCandidate $row.path 'R16' $row.role
        $after=Get-GitBlobIdentity $R16Repo $R16FreezeSha $row.path 'R16' $row.role
    } else {
        $before=Get-RawIdentity (Join-Path $R16CandidateRepo $row.path) 'WORKTREE_RAW' 'R16' $row.role `
            "WORKTREE@$R16ResolvedCandidate@R16_CANDIDATE" $row.path
        $after=Get-RawIdentity (Join-Path $R16Repo $row.path) 'WORKTREE_RAW' 'R16' $row.role `
            "WORKTREE@$R16FreezeSha@R16_FREEZE" $row.path
    }
    $match=($before.bytes -eq $after.bytes -and $before.sha256 -eq $after.sha256 -and
            ($row.mode -ne 'GIT_OBJECT' -or $before.blob_oid -eq $after.blob_oid))
    [void]$comparison.Add("R16`t$($row.universe_id)`t$($row.role)`t$($row.mode)`t$($row.path)`t$($before.namespace)`t$($before.blob_oid)`t$($before.bytes)`t$($before.sha256)`t$($after.namespace)`t$($after.blob_oid)`t$($after.bytes)`t$($after.sha256)`t$match")
}
Write-Utf8Lf (Join-Path $R16Out 'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv') $comparison

$required=@($r16Rows|Where-Object continuity -eq 'required')
$notClaimed=@($r16Rows|Where-Object continuity -eq 'not_claimed')
$resultRows=@(Read-StrictTsv (Join-Path $R16Out 'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv') @(
 'ceremony','universe_id','role','mode','path','before_namespace','before_blob_oid','before_bytes','before_sha256','after_namespace','after_blob_oid','after_bytes','after_sha256','match'))
if($resultRows.Count -ne $required.Count){throw 'STOP R16-continuity-conservation'}
$mismatches=@($resultRows|Where-Object match -ne 'True')
$subsetConclusion=if($mismatches.Count -eq 0){
 "UNCHANGED: all $($required.Count) independently-authorized continuity rows match in their named modes"
}else{
 "CHANGED: $($mismatches.Count) of $($required.Count) independently-authorized continuity rows differ; no unchanged claim"
}
$overallConclusion=if($notClaimed.Count -eq 0 -and $mismatches.Count -eq 0){
 'OVERALL_UNCHANGED: every row in the independently-authorized universe was compared and matched'
}else{
 "NO_OVERALL_UNCHANGED_CLAIM: compared=$($required.Count) outside_claim=$($notClaimed.Count) mismatched=$($mismatches.Count)"
}
Write-Utf8Lf (Join-Path $R16Out 'R16_UNCHANGED_CONCLUSION.tsv') @(
 'ceremony`tuniverse_id`ttotal_rows`tcompared_rows`toutside_claim_rows`tmismatch_rows`tsubset_conclusion`toverall_conclusion',
 "R16`t$($universeIds[0])`t$($r16Rows.Count)`t$($required.Count)`t$($notClaimed.Count)`t$($mismatches.Count)`t$subsetConclusion`t$overallConclusion"
)
```

What makes this fail or turn red: a changed blob OID, changed byte count/hash, changed raw line endings, a missing before-side file, or a count other than one result per required authority row. An omitted relevant path can no longer be hidden by editing a freezer list: changing the copied universe violates its independent descriptor identity.

### 7.6 Publish the R16 manifest only after an exact output-member check

Before the manifest is created, the required non-manifest member set is:

```text
R16_BASE_TO_FREEZE.patch
R16_BASE_TO_FREEZE_IDENTITY.tsv
R16_BASE_TO_FREEZE_RESULT.tsv
R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv
R16_COMMITS.tsv
R16_FROZEN_SCOPE_IDENTITIES.tsv
R16_FULL_TRACKED_TREE.txt
R16_SCOPE_AUTHORITY.tsv
R16_SCOPE_AUTHORITY_DESCRIPTOR.tsv
R16_UNCHANGED_CONCLUSION.tsv
R16_TRANSCRIPT.txt
```

```powershell
$requiredR16Members=@(
 'R16_BASE_TO_FREEZE.patch','R16_BASE_TO_FREEZE_IDENTITY.tsv','R16_BASE_TO_FREEZE_RESULT.tsv',
 'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv','R16_COMMITS.tsv','R16_FROZEN_SCOPE_IDENTITIES.tsv',
 'R16_FULL_TRACKED_TREE.txt','R16_SCOPE_AUTHORITY.tsv','R16_SCOPE_AUTHORITY_DESCRIPTOR.tsv',
 'R16_UNCHANGED_CONCLUSION.tsv','R16_TRANSCRIPT.txt')
$actualR16Members=@(Get-ChildItem -LiteralPath $R16Out -Force -File|Select-Object -ExpandProperty Name)
Assert-ExactStringSet $requiredR16Members $actualR16Members 'R16-pre-manifest-members'

$manifestLines=[Collections.Generic.List[string]]::new()
[void]$manifestLines.Add('ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256')
foreach($name in ($requiredR16Members|Sort-Object)){
 $id=Get-RawIdentity (Join-Path $R16Out $name) 'RAW_EXTERNAL_FILE' 'R16' 'bundle_member' `
     "EXTERNAL_ROOT@$R16ExternalRootId" $name
 [void]$manifestLines.Add((Format-IdentityRow $id))
}
$r16Manifest=Join-Path $R16Out 'R16_FREEZE_MANIFEST.tsv'
Write-Utf8Lf $r16Manifest $manifestLines
$manifestId=Get-RawIdentity $r16Manifest 'RAW_EXTERNAL_FILE' 'R16' 'freeze_manifest' `
    "EXTERNAL_ROOT@$R16ExternalRootId" 'R16_FREEZE_MANIFEST.tsv'
Write-Utf8Lf (Join-Path $R16Out 'R16_FREEZE_MANIFEST.detached.tsv') @(
 'ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256',
 (Format-IdentityRow $manifestId)
)
```

The completed root is then independently anchored. Until that separate publication anchor exists, the output is a candidate bundle, not a trusted R16 source for R23.

## 8. R23 — complete final exact SHA/artifact procedure

### 8.1 R23 inputs

The adopted kickoff must name these literal sources. It must not name expected WP-A artifact values.

```powershell
$R23Repo                         = '<isolated clean worktree at proposed R23 commit>'
$R23Out                          = '<new external create-once R23 output directory>'
$R23ScopeAuthorityFile           = '<independently anchored R23_SCOPE_AUTHORITY.tsv>'
$R23ScopeAuthorityDescriptor     = '<independently anchored R23 scope descriptor>'
$PriorR16Root                    = '<independently anchored completed R16 publication root>'
$PriorR16RootDescriptor          = '<descriptor selecting that exact R16 root/manifest>'
$Audit2CloseFile                 = '<independently anchored machine-readable Audit-2 close>'
$Audit2CloseDescriptor           = '<descriptor selecting the exact close source>'
$WpaCaptureRoot                  = '<independently anchored immutable WP-A capture root>'
$WpaCaptureManifest              = '<capture-time root manifest inside that root>'
$WpaCaptureDescriptor            = '<descriptor selecting the capture manifest/root identity>'
$WpaArtifactIndexRelative        = '<root-relative path to §5.5 index; selected by capture manifest>'
$R23EventLedgerRelative          = '<root-relative path to §5.6 ledger; selected by capture manifest>'
$R23ExternalRootId               = '<immutable publication-root identity reserved for this run>'
```

All are presently `UNKNOWN` for an actual run. The sources in §3 state precisely what settles them. Supplying current-artifact hashes in the kickoff is forbidden because it would recreate F5.

Before §8.2, validate every value with `Assert-NoPlaceholder`, require the four descriptors to be independently anchored and to contain exactly one row with the expected ceremony/role, then create and seed the R23 output root:

```powershell
foreach($pair in @(
 @($R23Repo,'R23Repo'),@($R23Out,'R23Out'),
 @($R23ScopeAuthorityFile,'R23ScopeAuthorityFile'),
 @($R23ScopeAuthorityDescriptor,'R23ScopeAuthorityDescriptor'),
 @($PriorR16Root,'PriorR16Root'),@($PriorR16RootDescriptor,'PriorR16RootDescriptor'),
 @($Audit2CloseFile,'Audit2CloseFile'),@($Audit2CloseDescriptor,'Audit2CloseDescriptor'),
 @($WpaCaptureRoot,'WpaCaptureRoot'),@($WpaCaptureManifest,'WpaCaptureManifest'),
 @($WpaCaptureDescriptor,'WpaCaptureDescriptor'),
 @($WpaArtifactIndexRelative,'WpaArtifactIndexRelative'),
 @($R23EventLedgerRelative,'R23EventLedgerRelative'),
 @($R23ExternalRootId,'R23ExternalRootId'))){Assert-NoPlaceholder $pair[0] $pair[1]}
Assert-CanonicalRelativePath $WpaArtifactIndexRelative
Assert-CanonicalRelativePath $R23EventLedgerRelative
$WpaArtifactIndex=Join-Path $WpaCaptureRoot $WpaArtifactIndexRelative
$R23EventLedger=Join-Path $WpaCaptureRoot $R23EventLedgerRelative

if(Test-Path -LiteralPath $R23Out){throw 'STOP R23-output-already-exists'}
[void](New-Item -ItemType Directory -Path $R23Out)
Copy-ExactFile $R23ScopeAuthorityFile (Join-Path $R23Out 'R23_SCOPE_AUTHORITY.tsv')
Copy-ExactFile $R23ScopeAuthorityDescriptor (Join-Path $R23Out 'R23_SCOPE_AUTHORITY_DESCRIPTOR.tsv')
Copy-ExactFile $PriorR16RootDescriptor (Join-Path $R23Out 'R23_INPUT_R16_ROOT_DESCRIPTOR.tsv')
Copy-ExactFile $Audit2CloseFile (Join-Path $R23Out 'R23_INPUT_AUDIT2_CLOSE.tsv')
Copy-ExactFile $Audit2CloseDescriptor (Join-Path $R23Out 'R23_INPUT_AUDIT2_CLOSE_DESCRIPTOR.tsv')
Copy-ExactFile $WpaCaptureManifest (Join-Path $R23Out 'R23_INPUT_WPA_CAPTURE_MANIFEST.tsv')
Copy-ExactFile $WpaCaptureDescriptor (Join-Path $R23Out 'R23_INPUT_WPA_CAPTURE_DESCRIPTOR.tsv')
Copy-ExactFile $WpaArtifactIndex (Join-Path $R23Out 'R23_INPUT_WPA_ARTIFACT_INDEX.tsv')
Copy-ExactFile $R23EventLedger (Join-Path $R23Out 'R23_INPUT_EVENT_LEDGER.tsv')
```

### 8.2 Derive and bind R16 from its verified publication — never from an SHA variable

```powershell
$r16ManifestPath=Join-Path $PriorR16Root 'R16_FREEZE_MANIFEST.tsv'
$r16DetachedPath=Join-Path $PriorR16Root 'R16_FREEZE_MANIFEST.detached.tsv'
$idColumns=@('ceremony','role','mode','namespace','path','blob_oid','bytes','sha256')
$r16Detached=@(Read-StrictTsv $r16DetachedPath $idColumns)
if($r16Detached.Count -ne 1 -or $r16Detached[0].ceremony -ne 'R16' -or
   $r16Detached[0].role -ne 'freeze_manifest' -or $r16Detached[0].mode -ne 'RAW_EXTERNAL_FILE' -or
   $r16Detached[0].path -ne 'R16_FREEZE_MANIFEST.tsv'){throw 'STOP invalid-R16-detached-identity'}
$r16ManifestActual=Get-RawIdentity $r16ManifestPath 'RAW_EXTERNAL_FILE' 'R16' 'freeze_manifest' `
    $r16Detached[0].namespace 'R16_FREEZE_MANIFEST.tsv'
if($r16ManifestActual.bytes -ne [int64]$r16Detached[0].bytes -or
   $r16ManifestActual.sha256 -ne $r16Detached[0].sha256){throw 'STOP R16-manifest-detached-mismatch'}

$r16ManifestRows=@(Read-StrictTsv $r16ManifestPath $idColumns)
if(@($r16ManifestRows|Where-Object ceremony -ne 'R16').Count -gt 0){throw 'STOP cross-ceremony-R16-manifest'}
$commitMember=@($r16ManifestRows|Where-Object path -eq 'R16_COMMITS.tsv')
if($commitMember.Count -ne 1){throw 'STOP R16-commit-member-count'}
$r16CommitsPath=Join-Path $PriorR16Root 'R16_COMMITS.tsv'
$r16CommitsActual=Get-RawIdentity $r16CommitsPath 'RAW_EXTERNAL_FILE' 'R16' 'bundle_member' `
    $commitMember[0].namespace 'R16_COMMITS.tsv'
if($r16CommitsActual.bytes -ne [int64]$commitMember[0].bytes -or
   $r16CommitsActual.sha256 -ne $commitMember[0].sha256){throw 'STOP R16-commits-member-mismatch'}
$r16CommitRows=@(Read-StrictTsv $r16CommitsPath $idColumns)
$freezeCommit=@($r16CommitRows|Where-Object role -eq 'freeze_commit')
if($freezeCommit.Count -ne 1 -or $freezeCommit[0].ceremony -ne 'R16' -or
   $freezeCommit[0].mode -ne 'GIT_COMMIT'){throw 'STOP R16-freeze-commit-row-count'}
$DerivedR16FreezeSha=$freezeCommit[0].blob_oid
if($DerivedR16FreezeSha -notmatch '^[0-9a-f]{40,64}$'){throw 'STOP malformed-derived-R16-SHA'}
```

The independent R16 root descriptor is verified before this block using §5.1, and its selected manifest identity must equal `$r16ManifestActual`. An arbitrary ancestor cannot pass: it would need the independently anchored R16 manifest, the matching detached identity, the manifested commit table, and the matching Audit-2 close.

### 8.3 Bind the accepting Audit-2 close to that exact R16 publication

```powershell
$closeColumns=@('record_kind','audit_cycle_id','verdict','r16_freeze_sha','r16_manifest_sha256','closed_at_utc')
$closeRows=@(Read-StrictTsv $Audit2CloseFile $closeColumns)
if($closeRows.Count -ne 1 -or $closeRows[0].record_kind -ne 'AUDIT2_CLOSE' -or
   $closeRows[0].verdict -notin @('PASS','PASS-WITH-NITS')){throw 'STOP Audit2-close-not-uniquely-accepting'}
if($closeRows[0].r16_freeze_sha -ne $DerivedR16FreezeSha -or
   $closeRows[0].r16_manifest_sha256 -ne $r16ManifestActual.sha256){
   throw 'STOP Audit2-close-does-not-bind-verified-R16'
}
$null=[datetime]::ParseExact($closeRows[0].closed_at_utc,'yyyy-MM-ddTHH:mm:ss.fffffffZ',
    [Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::AssumeUniversal)
```

The close descriptor is independently verified in its declared `GIT_OBJECT`/`WORKTREE_RAW` or `RAW_EXTERNAL_FILE` mode before parsing. R23 copies the descriptor and close bytes into its output. If the eventual close is tracked text, its blob OID is mandatory; if external, its immutable root ID is mandatory. No bare path/bytes/hash form is allowed.

### 8.4 Validate R23 chronology, exact scope, commit, ancestry, and diff

```powershell
$eventColumns=@('ceremony','event_id','sequence','occurred_at_utc','source_mode','source_namespace','source_path','source_blob_oid','source_bytes','source_sha256','r16_freeze_sha','r16_manifest_sha256','capture_id','artifact_id','tested_sha','verdict')
$events=@(Read-StrictTsv $R23EventLedger $eventColumns)
$requiredEvents=@('R16_FROZEN','AUDIT2_CLOSED_ACCEPTING','WPA_BEGAN','WPA_COMPLETED',
                  'WPA_EVIDENCE_CAPTURE_CLOSED','STAGING_DISCARD_RECORDED')
Assert-ExactStringSet $requiredEvents @($events.event_id) 'R23-event-ids'
$priorSequence=[int64]::MinValue; $priorTime=[datetime]::MinValue
foreach($eventId in $requiredEvents){
 $e=@($events|Where-Object event_id -eq $eventId)
 if($e.Count -ne 1 -or $e[0].ceremony -ne 'R23'){throw 'STOP R23-event-row-count-or-ceremony'}
 $seq=[int64]$e[0].sequence
 $time=[datetime]::ParseExact($e[0].occurred_at_utc,'yyyy-MM-ddTHH:mm:ss.fffffffZ',
   [Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::AssumeUniversal)
 if($seq -le $priorSequence -or $time -lt $priorTime){throw 'STOP R23-chronology-not-monotone'}
 $priorSequence=$seq; $priorTime=$time
}
$auditEvent=@($events|Where-Object event_id -eq 'AUDIT2_CLOSED_ACCEPTING')[0]
if($auditEvent.r16_freeze_sha -ne $DerivedR16FreezeSha -or
   $auditEvent.r16_manifest_sha256 -ne $r16ManifestActual.sha256 -or
   $auditEvent.verdict -notin @('PASS','PASS-WITH-NITS')){throw 'STOP R23-Audit2-event-binding'}

$R23FreezeSha=(& git -C $R23Repo rev-parse --verify 'HEAD^{commit}').Trim()
if($R23FreezeSha -notmatch '^[0-9a-f]{40,64}$'){throw 'STOP R23-head-unresolved'}
Assert-CleanExactWorktree $R23Repo $R23FreezeSha 'R23-freeze'
& git -C $R23Repo merge-base --is-ancestor $DerivedR16FreezeSha $R23FreezeSha
if($LASTEXITCODE -ne 0){throw 'STOP verified-R16-is-not-R23-ancestor'}

$r23ScopeColumns=@('ceremony','universe_id','role','mode','namespace','path','continuity')
$r23Rows=@(Read-StrictTsv $R23ScopeAuthorityFile $r23ScopeColumns)
if($r23Rows.Count -eq 0 -or @($r23Rows|Where-Object ceremony -ne 'R23').Count -gt 0){throw 'STOP R23-universe-ceremony'}
$allowedR23Roles=@('final_scope','final_artifact','final_manifest','audit2_close')
foreach($row in $r23Rows){
 if($row.role -notin $allowedR23Roles -or $row.mode -notin @('GIT_OBJECT','WORKTREE_RAW') -or
    $row.namespace -ne 'REPO_RELATIVE' -or $row.continuity -notin @('required','not_claimed')){
    throw "STOP invalid-R23-universe-row $($row._raw_line)"
 }
 Assert-CanonicalRelativePath $row.path
}
foreach($role in @('final_artifact','final_manifest')){
 if(@($r23Rows|Where-Object role -eq $role).Count -lt 2){throw "STOP missing-R23-dual-form-role $role"}
}

$r23Patch=Join-Path $R23Out 'R23_VERIFIED_R16_TO_FINAL.patch'
& git -C $R23Repo --no-pager diff --binary --full-index --no-ext-diff `
    --output=$r23Patch $DerivedR16FreezeSha $R23FreezeSha --
if($LASTEXITCODE -ne 0){throw 'STOP R23-R16-diff-generation'}
& git -C $R23Repo --no-pager diff --quiet --no-ext-diff $DerivedR16FreezeSha $R23FreezeSha --
$r23DiffRc=$LASTEXITCODE
if($r23DiffRc -notin 0,1){throw 'STOP R23-R16-diff-evaluation'}
```

The R23 diff record label is exactly `R23_VERIFIED_R16_TO_FINAL`; its identity row explicitly uses `RAW_EXTERNAL_FILE`. R23 then enumerates `R23_FULL_TRACKED_TREE.txt` and `R23_FROZEN_SCOPE_IDENTITIES.tsv` using the same §7.4 mechanics but with only R23 variables, R23 roles, `R23FreezeSha`, and R23 filenames. No Packet-9 guard or R16 label is inherited.

### 8.5 Verify capture-time evidence exactness and extract the expected WP-A rows

```powershell
$captureColumns=@('capture_id','mode','namespace','path','blob_oid','bytes','sha256')
$captureRows=@(Read-StrictTsv $WpaCaptureManifest $captureColumns)
$captureIds=@($captureRows.capture_id|Sort-Object -Unique)
if($captureIds.Count -ne 1 -or @($captureRows|Where-Object mode -ne 'RAW_EXTERNAL_FILE').Count -gt 0){
 throw 'STOP invalid-WPA-capture-manifest'
}
foreach($row in $captureRows){Assert-CanonicalRelativePath $row.path}
$capturePaths=@($captureRows.path)
if(@($capturePaths|Sort-Object -Unique).Count -ne $capturePaths.Count){throw 'STOP duplicate-WPA-capture-path'}

$actualCaptureFiles=@(Get-ChildItem -LiteralPath $WpaCaptureRoot -Recurse -Force -File |
 ForEach-Object{[IO.Path]::GetRelativePath($WpaCaptureRoot,$_.FullName).Replace('\','/')})
Assert-ExactStringSet $capturePaths $actualCaptureFiles 'WPA-capture-root-members'
foreach($row in $captureRows){
 $actual=Get-RawIdentity (Join-Path $WpaCaptureRoot $row.path) 'RAW_EXTERNAL_FILE' 'R23' `
    'wpa_capture_member' $row.namespace $row.path
 if($actual.bytes -ne [int64]$row.bytes -or $actual.sha256 -ne $row.sha256){
    throw "STOP WPA-capture-member-drift $($row.path)"
 }
}

$wpaCompleted=@($events|Where-Object event_id -eq 'WPA_COMPLETED')
if($wpaCompleted.Count -ne 1){throw 'STOP WPA-completed-event-count'}
$derivedCaptureId=$wpaCompleted[0].capture_id
$derivedArtifactId=$wpaCompleted[0].artifact_id
$derivedTestedSha=$wpaCompleted[0].tested_sha
foreach($v in @($derivedCaptureId,$derivedArtifactId,$derivedTestedSha)){Assert-NoPlaceholder $v 'derived-WPA-selector'}
if($derivedCaptureId -ne $captureIds[0]){throw 'STOP WPA-event-capture-id-mismatch'}

$artifactColumns=@('record_kind','capture_id','artifact_id','repo_relative_path','mode','tested_sha','blob_oid','bytes','sha256')
$artifactRows=@(Read-StrictTsv $WpaArtifactIndex $artifactColumns)
$selected=@($artifactRows|Where-Object{
 $_.record_kind -eq 'WP_A_TESTED_ARTIFACT' -and $_.capture_id -eq $derivedCaptureId -and
 $_.artifact_id -eq $derivedArtifactId -and $_.tested_sha -eq $derivedTestedSha})
$expectedGit=@($selected|Where-Object mode -eq 'GIT_OBJECT')
$expectedRaw=@($selected|Where-Object mode -eq 'WORKTREE_RAW')
if($selected.Count -ne 2 -or $expectedGit.Count -ne 1 -or $expectedRaw.Count -ne 1){
 throw 'STOP WPA-artifact-selector-zero-multiple-or-mode-error'
}
if($expectedGit[0].repo_relative_path -ne $expectedRaw[0].repo_relative_path){
 throw 'STOP WPA-artifact-selected-paths-differ'
}
$DerivedWpaArtifactPath=$expectedGit[0].repo_relative_path
Assert-CanonicalRelativePath $DerivedWpaArtifactPath
if($expectedGit[0].blob_oid -notmatch '^[0-9a-f]{40,64}$' -or $expectedRaw[0].blob_oid -ne '-' -or
   $expectedGit[0].sha256 -notmatch '^[0-9a-f]{64}$' -or $expectedRaw[0].sha256 -notmatch '^[0-9a-f]{64}$'){
 throw 'STOP malformed-WPA-expected-identity'
}
Write-Utf8Lf (Join-Path $R23Out 'R23_WPA_EXPECTED_ROWS.tsv') @(
 ($artifactColumns -join "`t"), $expectedGit[0]._raw_line, $expectedRaw[0]._raw_line)
```

The expected rows are derived only after the independently anchored capture set and event selector agree. Duplicate valid-looking rows are not deduplicated; they stop the run. The exact source lines are preserved rather than rebuilt from freezer variables.

### 8.6 Compare the final artifact in both appropriate modes and stop on mismatch

```powershell
$finalGit=Get-GitBlobIdentity $R23Repo $R23FreezeSha $DerivedWpaArtifactPath 'R23' 'final_artifact'
$finalRaw=Get-RawIdentity (Join-Path $R23Repo $DerivedWpaArtifactPath) 'WORKTREE_RAW' 'R23' `
    'final_artifact' "WORKTREE@$R23FreezeSha@R23_FREEZE" $DerivedWpaArtifactPath
$gitMatch=($finalGit.blob_oid -eq $expectedGit[0].blob_oid -and
           $finalGit.bytes -eq [int64]$expectedGit[0].bytes -and
           $finalGit.sha256 -eq $expectedGit[0].sha256)
$rawMatch=($finalRaw.bytes -eq [int64]$expectedRaw[0].bytes -and
           $finalRaw.sha256 -eq $expectedRaw[0].sha256)
Write-Utf8Lf (Join-Path $R23Out 'R23_WPA_TO_FINAL_ARTIFACT.tsv') @(
 'ceremony`tartifact_id`tpath`tmode`texpected_blob_oid`texpected_bytes`texpected_sha256`tfinal_blob_oid`tfinal_bytes`tfinal_sha256`tmatch',
 "R23`t$derivedArtifactId`t$DerivedWpaArtifactPath`tGIT_OBJECT`t$($expectedGit[0].blob_oid)`t$($expectedGit[0].bytes)`t$($expectedGit[0].sha256)`t$($finalGit.blob_oid)`t$($finalGit.bytes)`t$($finalGit.sha256)`t$gitMatch",
 "R23`t$derivedArtifactId`t$DerivedWpaArtifactPath`tWORKTREE_RAW`t-`t$($expectedRaw[0].bytes)`t$($expectedRaw[0].sha256)`t-`t$($finalRaw.bytes)`t$($finalRaw.sha256)`t$rawMatch"
)
if(-not $gitMatch -or -not $rawMatch){
 throw 'STOP final-artifact-differs-from-independently-frozen-WPA-tested-identity; R23 manifest forbidden'
}
```

What makes this fail: changing either final blob or materialized bytes; changing the capture index after capture; selecting zero/duplicate rows; changing the path in one mode; or changing the event selector. Setting expectations equal to the current artifact is not an available input and cannot make the check pass.

### 8.7 R23 final identities and publication manifest

Before publication, copy byte-for-byte into `$R23Out` and identity-bind all of these independent inputs:

- verified prior `R16_FREEZE_MANIFEST.tsv` and `R16_FREEZE_MANIFEST.detached.tsv`;
- prior R16 root descriptor;
- Audit-2 close and its descriptor;
- R23 scope authority and descriptor;
- WP-A capture manifest and descriptor;
- WP-A artifact index and R23 event ledger;
- preserved `R23_WPA_EXPECTED_ROWS.tsv`.

Then create ceremony-specific outputs:

```text
R23_COMMITS.tsv
R23_VERIFIED_R16_TO_FINAL.patch
R23_VERIFIED_R16_TO_FINAL_IDENTITY.tsv
R23_VERIFIED_R16_TO_FINAL_RESULT.tsv
R23_FULL_TRACKED_TREE.txt
R23_FROZEN_SCOPE_IDENTITIES.tsv
R23_WPA_CAPTURE_RECOMPUTATION.tsv
R23_CHRONOLOGY_RESULT.tsv
R23_WPA_TO_FINAL_ARTIFACT.tsv
R23_TRANSCRIPT.txt
```

`R23_COMMITS.tsv` contains `R23_FREEZE_SHA` and `VERIFIED_PRIOR_R16_SHA`; it contains no operator-supplied R16 value. `R23_CHRONOLOGY_RESULT.tsv` records every event sequence/time comparison and the exact limited conclusion: `CONSISTENT: independently anchored records satisfy the required order`. It must not say the freezer observed the events.

The R23 manifest uses the §4 header and `ceremony=R23` on every row. It enumerates an explicit required filename set that includes every copied input and every generated output, then calls `Assert-ExactStringSet` against `Get-ChildItem -Force -File`. A hidden, missing, extra, or cross-ceremony file stops publication. Finally:

```powershell
$r23Manifest=Join-Path $R23Out 'R23_FREEZE_MANIFEST.tsv'
# Build rows exactly as in §7.6, using ceremony R23, the explicit R23 member set,
# mode RAW_EXTERNAL_FILE, and namespace EXTERNAL_ROOT@$R23ExternalRootId.
$r23ManifestId=Get-RawIdentity $r23Manifest 'RAW_EXTERNAL_FILE' 'R23' 'freeze_manifest' `
    "EXTERNAL_ROOT@$R23ExternalRootId" 'R23_FREEZE_MANIFEST.tsv'
Write-Utf8Lf (Join-Path $R23Out 'R23_FREEZE_MANIFEST.detached.tsv') @(
 'ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256',
 (Format-IdentityRow $r23ManifestId)
)
```

The manifest and detached identity are then independently anchored. Until that happens, they are a candidate publication, not accepted evidence. The final-release requirement is the exact final SHA/artifact, ancestry, path manifest, and artifact hash. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1021-1026`

## 9. Independent auditor verification

The auditor must obtain authority descriptors, anchored roots, and source records directly from the independent publisher, not solely from the freezer's bundle. Recomputing freezer-written digests is arithmetic verification; the checks below add source truth and completeness.

### 9.1 R16 auditor procedure

1. Verify the R16 scope descriptor against its pre-ceremony authority anchor. Independently fetch the selected universe and byte-compare it with `R16_SCOPE_AUTHORITY.tsv` in the bundle.
2. Parse the universe with §5.2. Recompute the exact admitted `(role,mode,path)` set. Require one terminal derived identity per universe row and one before/after result per `continuity=required` row. No row may disappear during parsing, normalization, or comparison; this is the conservation rule required by defect Pattern 13. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`
3. Create separate clean audit-only worktrees at the exact candidate SHA and R16 SHA. Record exact HEAD and empty pre/post status. The established audit contract requires exact SHA, isolated worktree, and pre/post cleanliness. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`
4. Recompute the base-to-freeze binary/full-index patch, its return code, explicit `RAW_EXTERNAL_FILE` identity, and byte equality.
5. Recompute the full tracked tree and every `GIT_OBJECT` OID/bytes/SHA. Recompute every `WORKTREE_RAW` identity from the correct worktree namespace. Never compare modes across one another.
6. Recompute every before/after row and both conclusion counts. If one row is `not_claimed`, require `NO_OVERALL_UNCHANGED_CLAIM` even when every compared row matches.
7. Recompute the manifest exact member set with a force-inclusive listing and its detached identity. Require the same R16 SHA throughout.
8. Reopen the Packet-9 closure/index through their independently identified sources; check their identities and member completeness, not only their copied digest strings.

Mandatory adversarial falsifications:

- Change one copied scope-universe byte: descriptor comparison must stop.
- Remove one authority row only from a derived table: conservation count must stop.
- Change one candidate or freeze blob: the corresponding comparison must become `False` or stop, never `UNCHANGED`.
- Change only checkout line endings on a required raw row: `WORKTREE_RAW` must become `False` while the Git row may remain equal.
- Add one hidden output member: exact manifest membership must stop.

The auditor records the actual command and red output for each arm. A merely described mutant is supplemental, not closure evidence.

### 9.2 R23 auditor procedure

1. Independently obtain and verify the prior R16 root descriptor, R16 manifest, detached identity, manifested commit table, and derived R16 SHA. Do not accept a SHA copied from `R23_COMMITS.tsv`.
2. Independently obtain and verify the Audit-2 close source, its identity mode/root/blob OID, its uniquely accepting row, its required auditor verdict members, and its exact binding to the same R16 SHA/manifest hash.
3. Independently obtain the R23 scope authority, require exact-set equality with the copied bytes, and recompute one R23 identity for every universe row in its required mode.
4. Independently obtain the WP-A capture authority descriptor and root. Re-enumerate it with a force-inclusive recursive listing; reject missing, extra, duplicate, unreadable, or changed members before interpreting results.
5. Parse the event ledger independently. Reopen and hash every event's namespaced source record. Recompute unique event IDs, sequence comparisons, UTC comparisons, the R16/Audit-2 binding, and the capture/artifact/tested-SHA selector.
6. Parse the artifact index independently. Require exactly the same two unique rows selected by §5.5 and byte-compare their original source lines to `R23_WPA_EXPECTED_ROWS.tsv`.
7. Create a clean audit-only worktree at R23 SHA. Recompute the final `GIT_OBJECT` and `WORKTREE_RAW` identities and compare them to the selected source rows in the same modes. Both must match.
8. Recompute the exact verified-R16-to-R23 diff, full tree, all scope identities, all copied-input identities, manifest exact member set, and detached manifest identity.
9. State the truth limit explicitly: the procedure establishes integrity, completeness against independently frozen universes, and consistency of independently anchored event records. If the event publisher/root is not independent or its real-world authority is not established, return STOP/BLOCK; do not upgrade consistent prose to event truth.

Mandatory adversarial falsifications:

- Substitute a different ancestor for R16: the anchored R16 manifest/Audit-2 close binding must stop.
- Remove or replace the Audit-2 close: the required-member set or close binding must stop.
- Add a second otherwise valid artifact-index row: unique selection must stop.
- Mutate either the expected Git row or raw row: capture-manifest recomputation must stop.
- Mutate only the final artifact after WP-A: the same-mode comparison must stop R23 manifest publication.
- Replace an evidence file with another file having the same basename under a different root: namespace/root-relative identity must stop.
- Swap, duplicate, or regress chronology sequence/time values: chronology validation must stop.
- Add one unmanifested evidence or R23-output file: the exact-set check must stop.

These attacks answer the governing question with constructible false worlds. They prevent the auditor from merely repeating the freezer's arithmetic.

## 10. Publication and stop conditions

### 10.1 R16 publication is forbidden if

- any U-R16 item in §3 is unresolved;
- the independent authority descriptor or universe cannot be verified;
- the worktree SHAs or cleanliness checks fail;
- the universe is empty, malformed, duplicated, missing a mandatory role, or loses a member between stages;
- a path cannot be identified in its declared mode;
- the exact base diff cannot be generated and identified;
- a conclusion count does not equal the authority-universe count;
- `OVERALL_UNCHANGED` appears while any universe row is outside the compared set or mismatches;
- output membership has a missing, extra, or hidden file; or
- the final R16 publication root is not independently anchored.

R16 may publish a truthful `CHANGED` result with an exact diff and identities, but it may not publish an unchanged conclusion that does not follow from the complete declared set.

### 10.2 R23 publication is forbidden if

- any U-R16-PUBLICATION, U-A2-CLOSE, U-R23-UNIVERSE, U-WPA-ROOT, U-WPA-INDEX, U-EVENTS, U-R23-SHA, or U-STORAGE item is unresolved;
- the R16 SHA is supplied independently of the verified R16 manifest chain;
- the Audit-2 close is absent, not uniquely accepting, or binds a different R16 SHA/manifest;
- the R23 commit is not a descendant of the verified R16 commit;
- the R23 scope authority, capture root, artifact index, or event ledger is missing, extra, duplicated, unreadable, changed, or not independently anchored;
- chronology cannot be evaluated from independently sourced records;
- the WP-A selector yields zero/multiple rows or anything other than one Git and one raw row for the same path/tested SHA;
- either final artifact mode differs from its capture-time expected row;
- any post-capture change would make the captured WP-A evidence stale; the governing plan blocks continuation on evidence-invalidating changes. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:982-984,1026-1028`
- the required R23 member set differs from the force-inclusive actual set; or
- the final R23 publication root is not independently anchored.

No “best effort,” guessed identity, inferred acceptance, nearby SHA, basename, current-artifact expectation, or narrative chronology may substitute.

## 11. What each proof does and does not establish

| Proof | Expected value comes from | Constructible red world | Exact claim; outside the universe |
|---|---|---|---|
| R16 scope completeness | Pre-ceremony independently anchored `R16_SCOPE_AUTHORITY.tsv` | Delete/add/change one copied or derived row | Exact equality to that authority universe. Files the authority itself omits are outside the claim and force `NO_OVERALL_UNCHANGED_CLAIM` unless the independent authority certifies completeness. |
| R16 identity continuity | Candidate/freeze Git objects and two exact clean checkouts, over authority rows marked `required` | Change a blob or raw materialization | Equality only for named rows/modes. `not_claimed` rows are printed as outside the unchanged claim. |
| R16/R23 separation | Verified R16 publication plus accepting close binding | Substitute another ancestor or omit close | R23 descends from the exact R16 reviewed by the accepting close; it is not merely descended from some commit. |
| WP-A evidence continuity | Independently frozen capture manifest | Modify/add/remove a capture member | Current evidence root equals the capture-time member universe. It does not prove the evidence content is truthful unless its producer authority is established. |
| WP-A artifact continuity | Two unique source rows derived from capture index using event-ledger selector | Change source row, duplicate it, or change final artifact | Final `GIT_OBJECT` and `WORKTREE_RAW` equal the WP-A-tested identities in the same modes. No other artifact/path is silently covered. |
| Chronology | Independently anchored event ledger plus independently reopenable source records | Duplicate/reorder events, regress time, break cross-reference | Source records are intact and mutually consistent with required order. Real-world truth remains outside the claim unless the independent publisher/source authority establishes it. |
| Bundle completeness | Explicit required filename set plus force-inclusive listing | Add a hidden file or omit a member | Exact bundle-root membership; nothing outside the named root is claimed. |

## 12. Estimates and final boundary

**R16: NO SOURCED ESTIMATE.** The work catalogue directs the future operator to produce an exact freeze procedure and time a dry run. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55`

**R23: NO SOURCED ESTIMATE.** The catalogue likewise directs the future operator to time a frozen identity/build procedure and supplies no disjoint row price. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:62`

Version 2 is procedure material only. It supersedes v1 as a rewrite, closes the six reviewed design defects in its contract, and remains **NOT ACCEPTED** pending the required independent review and the future resolution of the explicit `UNKNOWN` trust roots. It creates no acceptance and authorizes no action.

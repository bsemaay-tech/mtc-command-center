Status: FREEZE PROCEDURES V3 - SUPERSEDES V2 - NOT ACCEPTED

| Finding | V3 disposition | Failure demonstration required by this procedure |
|---|---|---|
| **F1 — R23 was not standalone and ceremony-specific** | **CONTRACT CLOSED; execution inputs remain `UNKNOWN`.** Section 8 gives the literal R23 sequence and exact member set. Its helpers take a mandatory `R23` ceremony token and reject every R16 output label except the explicitly named prior-R16 inputs. There is no “use the R16 mechanics” step. | In a disposable copy, change one R23 scope row to `ceremony=R16`, rename `R23_VERIFIED_R16_TO_FINAL` to an R16 label, or remove one required R23 member. Run the actual `Invoke-R23FreezeV3` procedure. It must stop with `V3_CEREMONY_MISMATCH`, `V3_R23_LABEL_SET`, or `V3_MEMBER_SET`; a separately written comparison is not evidence. V2 failed because the R23 tree, identities, and manifest were left as prose. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:13-15` |
| **F2 — R16 and R23 moments could be confused** | **CONTRACT CLOSED; the future boundary registry is `UNKNOWN`.** R23 has no runtime R16-SHA input. It derives the prior SHA from the manifest selected by a pre-R23 authority registry, binds the accepting Audit-2 close to that manifest, and requires strictly later WP-A completion/capture events before it resolves the final SHA. | Substitute any other ancestor while leaving the registry unchanged: `V3_PRIOR_R16_ANCHOR_MISMATCH`. Substitute a mutually consistent replacement root and descriptor: the registry-selected descriptor identity must differ and produce `V3_AUTHORITY_IDENTITY_MISMATCH`. Make R23’s event sequence or instant precede/equal the wrong boundary: `V3_EVENT_ORDER`. These attacks must be run through `Invoke-R23FreezeV3`. V2 never parsed and compared the supplied descriptors to their anchors. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:14` |
| **F3 — identities were absent or ambiguous under `* text=auto`** | **CONTRACT CLOSED.** Every consumed file is identified as `GIT_OBJECT`, `WORKTREE_RAW`, or `RAW_EXTERNAL_FILE`; tracked text consumed from a checkout requires both Git-object and raw rows. No bare byte-count/SHA pair is an identity. | Materialize one required text file with different line endings. The `GIT_OBJECT` row may remain equal while `WORKTREE_RAW` must differ and the procedure must stop or record `match=False`. Delete the mode, blob OID, namespace, or canonical path: strict parsing must stop. The repository’s prior mixed table proved why one unlabeled identity is unsatisfiable. `.gitattributes:1-2`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27,48-64` |
| **F4 — unchanged-bits claim outran its scope** | **CONTRACT CLOSED; actual independent scope publications are `UNKNOWN`.** Per-row continuity is always named. `OVERALL_UNCHANGED` is mechanically forbidden unless the independently anchored scope certificate says `COMPLETE`, binds the same universe ID and exact member-row count, and the auditor verifies its named completeness basis. The sentence never means “all relevant files” without that certification. | Remove the certificate, change its universe ID/count, add `not_claimed`, omit a terminal disposition, or mutate one required before/after identity. The actual R16 checker must emit `NO_OVERALL_UNCHANGED_CLAIM`, `CHANGED`, or STOP; it must never emit `OVERALL_UNCHANGED`. A changed path omitted by a purported authority is an attack on the authority’s completeness basis, not something the freezer may silently declare closed. V2 had no completeness-certification field or gate. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:16` |
| **F5 — WP-A expected identity was still supplied by the freezer’s material** | **OPEN — `CANNOT BE CLOSED UNTIL WP_A_TESTED_ARTIFACT_AUTHORITY_V1 EXISTS`.** No such independent publication, producer identity, create-once mechanism, selector values, or pinned registry identity is established. Section 4 names the artifact that would close it; §8.6 gives the exact conditional extraction and zero/multiple-row rejection. V3 does not call that future schema evidence. | **Present real world:** the pinned authority identity is `UNKNOWN`, so `Invoke-R23FreezeV3` must stop at `V3_WPA_AUTHORITY_NOT_ESTABLISHED` before reading freezer-selected evidence. **Closure RED is not currently reproducible because the independent source does not exist.** Once it exists, an auditor must run the actual checker twice: (a) add a second otherwise matching Git or raw source row and observe `V3_WPA_SELECTOR_CARDINALITY`; (b) keep the authority publication fixed, mutate the final same-mode artifact, and observe `V3_WPA_FINAL_MISMATCH`. Until both real RED arms and the unchanged GREEN arm are recorded, the continuity check is supplemental, not closure evidence. The original review named the trusted source and extraction as `UNKNOWN`; v2 also records that they do not exist. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:59-69`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_V2_2026-08-15.md:59-65,152-170`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:17,20-29` |
| **F6 — auditors recomputed arithmetic without proving truth/completeness** | **CONTRACT CLOSED subject to F5’s explicit block.** Auditors acquire authority publications directly, verify the production checker’s identity, invoke that checker for GREEN and mutations, reopen every event source, and distinguish record consistency from event truth. A reimplementation is supplemental only. | Make the production checker accept a bundle after an admitted row is removed, after an event source byte changes, or after the final artifact changes. The auditor must drive the named production function and preserve command/stdout/stderr/exit status. If only an independently written calculation detects the mutation, return `REQUEST_CHANGES`/`BLOCK`: the checker under review has not been falsified. The standing defect record rejects reimplementing a check instead of invoking it. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:25-28,45-63,73-83`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:18` |

## 1. Purpose, status, and authority boundary

This document defines two different local evidence ceremonies:

- **R16** is the pre-WP-A checkpoint produced after Packet 9 closes and before Packet 10/Audit 2. The work catalogue places that freeze at R16 and Audit 2 at R21. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54-60`
- **R23** is the later final-SHA/artifact freeze after Audit 2, WP-A, and evidence capture. It is not an R16 rerun. The work catalogue places WP-A at R22 and the final freeze at R23. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:61-63`

The governing plan independently requires: accepting Audit 2 before WP-A, WP-A evidence capture before staging-host discard, and the final release freeze only after those events. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:968-977`

Audit tier for this document is **T2**. F5 is deployed-artifact identity-sensitive and requires the separately prescribed T1 identity verification before any future acceptance. This document itself is **NOT ACCEPTED** and grants no verdict or authorization.

Nothing here authorizes or performs a host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or economic action. Commands are local file and read-only Git operations. Future host-derived evidence may be consumed only after it already exists under separate authority; this procedure does not create it.

## 2. Governing proof rules

The recurring defect is a check that can pass without proving its claim. A real check must identify an expected value outside the checked party’s control, a complete quantified universe, an enforcing mechanism, and a constructible false world. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`

V3 therefore applies these rules:

1. **Absence is STOP.** Unreadable, malformed, missing, ambiguous, unanchored, or cardinality-unknown inputs are inability-to-evaluate conditions. They are never PASS and never guessed.
2. **Expected-value provenance is part of the predicate.** Matching bytes do not establish that the right source selected them.
3. **One declared universe, one terminal disposition per member.** Input count must equal matched + changed + explicitly outside-claim; a silent drop or overwrite stops. This is Pattern 13’s conservation rule. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`
4. **Claim width equals probe width.** A row-level comparison can support only a row-level sentence. `OVERALL_UNCHANGED` additionally needs an independently anchored completeness certificate and verified basis. This follows Pattern 9. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-613`
5. **The executed instrument is the instrument under review.** RED/GREEN evidence must call the production procedure, not restate its comparison. Patterns 10 and 11 require literal reproducibility and real-caller reachability. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,860-895`
6. **Records prove only their exact claim.** A digest proves byte identity. An independently anchored event publication can prove integrity and cross-record consistency. Neither proves real-world truth unless the publisher’s authority and separation are established independently.

## 3. Current facts and blocking `UNKNOWN`s

| Required fact | Current state | What would settle it |
|---|---|---|
| Actual R16 base, candidate, freeze SHA, scope authority, scope certificate, Packet-9 paths, publication root | `UNKNOWN` | One adopted pre-R16 authority publication binding those values and exact sources. Packet 10 requires the full SHA, base/diff, every in-scope file, and final artifact/manifest identities. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-67` |
| Actual R16 publication selected for R23 | `UNKNOWN` | Completed R16 root plus manifest/detached identity, selected by a pre-R23 authority registry independent of the R23 freezer. |
| Accepting Audit-2 close storage form, path, identity, and data | `UNKNOWN` | A uniquely accepting machine-readable close binding the exact R16 manifest/SHA, plus its independent authority entry. The original review records the storage form as unknown. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:27-31,39-45` |
| R23 scope universe and completeness certificate | `UNKNOWN` | Independently published member set and certificate satisfying §5. |
| Trusted WP-A tested-artifact source | `UNKNOWN` | `WP_A_TESTED_ARTIFACT_AUTHORITY_V1` satisfying §4, with actual producer/separation/immutability evidence and a pinned pre-R23 registry identity. |
| WP-A selector values (`capture_id`, `artifact_id`, `tested_sha`) | `UNKNOWN` | Unique `WPA_COMPLETED` row inside the trusted §4 publication. The freezer is forbidden to type them. |
| R23 chronology authority and source records | `UNKNOWN` | Independently published ledger with unique events and directly reopenable source identities. Narrative ordering is insufficient. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_REVIEW_2026-08-15.md:71-81` |
| Create-once/read-only publication mechanism and namespace | `UNKNOWN` | Adopted local storage contract plus real evidence that the freezer has no write path to the closed authority publication. |
| Final R23 SHA and final artifact identities | `UNKNOWN` | A future clean local R23 worktree after every prior authority exists. |

**Operational result now:** R16 and R23 are not publishable. In particular, R23 must stop with `V3_WPA_AUTHORITY_NOT_ESTABLISHED`; it must not substitute current bytes, a freezer-written manifest, or mutually consistent capture-root material.

## 4. The independent WP-A source that does not yet exist

### 4.1 Finding of fact

The read sources do not name an existing trusted WP-A artifact-identity publisher or publication. V2 calls the source, selector, artifact ID/path/SHA/modes, and extraction rule `UNKNOWN`, and describes its schema as one that **would** settle the gap. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_V2_2026-08-15.md:59-65,152-170`

The program plan requires WP-A and captured evidence, but it does not name the machine-readable producer or immutable identity publication needed by F5. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-977,1021-1026` The work catalogue likewise says only “execute WP-A ... and preserve its evidence,” then freezes the final artifact later. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:61-63`

Therefore:

> **CANNOT BE CLOSED UNTIL `WP_A_TESTED_ARTIFACT_AUTHORITY_V1` EXISTS.**

### 4.2 What must create it

The following is a required future contract, not a claim that the mechanism exists:

- **Producer:** a specifically appointed **WP-A Capture Authority**, distinct from the R23 freezer. The producer’s actual principal/process identity is presently `UNKNOWN`.
- **Time:** after the WP-A tested artifact and evidence are final, at `WPA_EVIDENCE_CAPTURE_CLOSED`, before staging-host discard and before R23 begins.
- **Publication:** one create-once member root named `WP_A_TESTED_ARTIFACT_AUTHORITY_V1/`, plus its manifest and descriptor outside that enumerated root so neither file must hash itself.
- **Independent selection:** a pre-R23 `R23_FREEZE_INPUT_REGISTRY_V3.tsv`, published by an authority other than the freezer, pins the descriptor’s exact mode/namespace/path/OID-or-dash/bytes/SHA. The freezer receives only a local read path to those already-selected bytes.
- **Separation proof:** the publication must carry independently reviewable evidence naming the producer, the freezer, the close instant, the create-once/read-only mechanism, and why the freezer had no mutation path after close. A field merely saying `read_only=true` is an assertion, not proof.
- **Direct auditor access:** each auditor obtains the registry and authority publication from the publisher or an independently selected immutable snapshot, not only from the R23 bundle. Copied digests alone are insufficient. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`

Until a real publisher, mechanism, registry identity, and separation evidence are populated and verified, the sentence “the freezer cannot influence it” is **UNKNOWN**. V3 refuses to manufacture that independence from hashes.

### 4.3 Required non-self-referential layout

```text
<authority-parent>/
  WP_A_TESTED_ARTIFACT_AUTHORITY_V1.descriptor.tsv
  WP_A_TESTED_ARTIFACT_AUTHORITY_V1.manifest.tsv
  WP_A_TESTED_ARTIFACT_AUTHORITY_V1/
    PRODUCER_SEPARATION.tsv
    EVENTS.tsv
    TESTED_ARTIFACT.tsv
    <zero or more other retained evidence members>
```

The manifest enumerates **only** members below `WP_A_TESTED_ARTIFACT_AUTHORITY_V1/`. The descriptor identifies the manifest. The pre-R23 registry identifies the descriptor. This removes v2’s self-reference, where the manifest sat inside the root whose complete member set it had to describe. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:20-29`

Required descriptor header:

```text
publication_id	producer_id	producer_role	closed_at_utc	member_root_name	manifest_mode	manifest_namespace	manifest_path	manifest_blob_oid	manifest_bytes	manifest_sha256
```

Required manifest header:

```text
publication_id	role	mode	namespace	path	blob_oid	bytes	sha256
```

`role=events`, `role=tested_artifact`, and `role=producer_separation` must each occur exactly once. All members use `RAW_EXTERNAL_FILE`; `path` is canonical relative to the member root. Zero/multiple mandatory-role rows, missing/extra members, or changed bytes stop before results are interpreted.

Required tested-artifact header:

```text
record_kind	capture_id	artifact_id	repo_relative_path	mode	tested_sha	blob_oid	bytes	sha256
```

Required event header:

```text
event_id	sequence	occurred_at_utc	capture_id	artifact_id	tested_sha	source_role	source_mode	source_namespace	source_path	source_blob_oid	source_bytes	source_sha256
```

## 5. Scope completeness and identity contracts

### 5.1 File identity

Every file identity row uses:

```text
ceremony	role	mode	namespace	path	blob_oid	bytes	sha256
```

- `ceremony` is exactly `R16` or `R23`.
- `GIT_OBJECT`: namespace `REPO@<full-sha>`, canonical repo-relative path, mandatory blob OID, byte count/SHA over `git cat-file blob` bytes.
- `WORKTREE_RAW`: namespace `WORKTREE@<full-sha>@<materialization-id>`, same canonical repo-relative path, `blob_oid=-`, byte count/SHA over checkout bytes.
- `RAW_EXTERNAL_FILE`: namespace `EXTERNAL_ROOT@<immutable-root-id>`, canonical root-relative path, `blob_oid=-`, byte count/SHA over raw bytes.
- Tracked text consumed from a checkout has both `GIT_OBJECT` and `WORKTREE_RAW` rows. The two are never compared cross-mode.
- Absolute paths, basenames that discard a parent namespace, `.`/`..`, duplicate keys, placeholder values, malformed OIDs/SHA values, and bare bytes/SHA rows stop.

### 5.2 Scope member publication

Required member header:

```text
ceremony	universe_id	role	mode	path	continuity
```

Required certificate header:

```text
ceremony	universe_id	completeness_status	basis_mode	basis_namespace	basis_path	member_row_count	published_at_utc
```

Rules:

1. Member and certificate files are selected by an independent authority registry and copied byte-for-byte before parsing.
2. The certificate has exactly one row. `completeness_status` is `COMPLETE` or `NOT_CERTIFIED`.
3. `member_row_count` equals the strict-parser row count; universe IDs and ceremony agree.
4. `basis_*` identifies the source against which the independent publisher certified completeness. The auditor reopens that basis directly.
5. Every `(role,mode,path)` is unique. Every tracked path has one Git row; every tracked artifact/manifest consumed from the checkout also has one raw row.
6. Every `continuity=required` row produces exactly one before/after disposition in the same mode. Every `not_claimed` row is counted outside the unchanged claim.
7. `OVERALL_UNCHANGED` is permitted only when the certificate is `COMPLETE`, its basis was verified, every member is `required`, every row has one terminal disposition, and all match. Otherwise the literal conclusion is `NO_OVERALL_UNCHANGED_CLAIM`.
8. The sentence is always qualified: “relative to independently published universe `<universe_id>` and basis `<basis_namespace>:<basis_path>`.” It never means every relevant file in existence.

## 6. Normative local checker primitives

These functions are part of the production procedure. An auditor’s RED/GREEN run must invoke them through `Invoke-R16FreezeV3` or `Invoke-R23FreezeV3`, not copy their comparisons into another script.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Stop-V3([string]$Reason) { throw "STOP $Reason" }

function Write-Utf8Lf([string]$Path,[string[]]$Lines) {
    $utf8=[Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($Path,(($Lines -join "`n")+"`n"),$utf8)
}

function Copy-Exact([string]$Source,[string]$Destination) {
    [IO.File]::WriteAllBytes($Destination,[IO.File]::ReadAllBytes($Source))
}

function Assert-Known([string]$Value,[string]$Name) {
    if([string]::IsNullOrWhiteSpace($Value) -or $Value -eq 'UNKNOWN' -or
       $Value -match '(?i)(TBD|PLACEHOLDER|<[^>]+>)') { Stop-V3 "V3_UNKNOWN name=$Name" }
}

function Assert-CanonicalRelative([string]$Path) {
    if([string]::IsNullOrWhiteSpace($Path) -or [IO.Path]::IsPathRooted($Path) -or
       $Path.Contains('\') -or $Path -match '(^|/)(\.|\.\.)(/|$)' -or
       $Path -match '(^/|/$|//)') { Stop-V3 "V3_NONCANONICAL_PATH path=$Path" }
}

function Read-StrictTsv([string]$Path,[string[]]$Columns) {
    $bytes=[IO.File]::ReadAllBytes($Path)
    $utf8=[Text.UTF8Encoding]::new($false,$true)
    try { $text=$utf8.GetString($bytes) } catch { Stop-V3 "V3_TSV_UTF8 path=$Path" }
    if($text.Contains("`r") -or -not $text.EndsWith("`n")) {
        Stop-V3 "V3_TSV_FRAMING path=$Path"
    }
    $lines=@($text.Substring(0,$text.Length-1) -split "`n")
    if($lines.Count -lt 2 -or $lines[0] -ne ($Columns -join "`t")) {
        Stop-V3 "V3_TSV_HEADER_OR_EMPTY path=$Path"
    }
    $rows=[Collections.Generic.List[object]]::new()
    for($i=1;$i -lt $lines.Count;$i++) {
        $parts=@($lines[$i] -split "`t",-1)
        if($parts.Count -ne $Columns.Count -or @($parts|Where-Object { $_ -eq '' }).Count) {
            Stop-V3 "V3_TSV_ROW line=$($i+1) path=$Path"
        }
        $m=[ordered]@{}
        for($j=0;$j -lt $Columns.Count;$j++) { $m[$Columns[$j]]=$parts[$j] }
        $m['_raw_line']=$lines[$i]
        [void]$rows.Add([pscustomobject]$m)
    }
    @($rows)
}

function Assert-ExactSet([string[]]$Expected,[string[]]$Actual,[string]$Reason) {
    $e=@($Expected|Sort-Object); $a=@($Actual|Sort-Object)
    if(@($e|Sort-Object -Unique).Count -ne $e.Count -or
       @($a|Sort-Object -Unique).Count -ne $a.Count -or
       ($e -join "`n") -ne ($a -join "`n")) { Stop-V3 $Reason }
}

function Get-RawId([string]$LiteralPath,[string]$Ceremony,[string]$Role,
                   [ValidateSet('WORKTREE_RAW','RAW_EXTERNAL_FILE')][string]$Mode,
                   [string]$Namespace,[string]$DisplayPath) {
    Assert-CanonicalRelative $DisplayPath
    $item=Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    if($item.PSIsContainer) { Stop-V3 "V3_IDENTITY_DIRECTORY path=$LiteralPath" }
    [pscustomobject]@{ceremony=$Ceremony;role=$Role;mode=$Mode;namespace=$Namespace;
      path=$DisplayPath;blob_oid='-';bytes=[int64]$item.Length;
      sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}

function Get-GitId([string]$Repo,[string]$Sha,[string]$Path,[string]$Ceremony,[string]$Role) {
    Assert-CanonicalRelative $Path
    $commit=(& git -C $Repo rev-parse --verify "$Sha^{commit}").Trim()
    if($LASTEXITCODE -ne 0 -or $commit -notmatch '^[0-9a-f]{40,64}$') {
        Stop-V3 "V3_COMMIT_IDENTITY sha=$Sha"
    }
    $spec="${commit}:$Path"
    $oid=(& git -C $Repo rev-parse --verify $spec).Trim()
    if($LASTEXITCODE -ne 0 -or $oid -notmatch '^[0-9a-f]{40,64}$') {
        Stop-V3 "V3_BLOB_IDENTITY spec=$spec"
    }
    $psi=[Diagnostics.ProcessStartInfo]::new('git')
    $psi.UseShellExecute=$false; $psi.RedirectStandardOutput=$true; $psi.RedirectStandardError=$true
    foreach($arg in @('-C',$Repo,'cat-file','blob',$spec)){[void]$psi.ArgumentList.Add($arg)}
    $p=[Diagnostics.Process]::Start($psi); $ms=[IO.MemoryStream]::new()
    $p.StandardOutput.BaseStream.CopyTo($ms); $stderr=$p.StandardError.ReadToEnd(); $p.WaitForExit()
    if($p.ExitCode -ne 0){Stop-V3 "V3_CAT_FILE rc=$($p.ExitCode) detail=$stderr"}
    $raw=$ms.ToArray(); $hash=[Security.Cryptography.SHA256]::Create()
    try{$digest=[Convert]::ToHexString($hash.ComputeHash($raw)).ToLowerInvariant()}
    finally{$hash.Dispose();$ms.Dispose()}
    [pscustomobject]@{ceremony=$Ceremony;role=$Role;mode='GIT_OBJECT';namespace="REPO@$commit";
      path=$Path;blob_oid=$oid;bytes=[int64]$raw.Length;sha256=$digest}
}

function Format-Id($Id) {
    "$($Id.ceremony)`t$($Id.role)`t$($Id.mode)`t$($Id.namespace)`t$($Id.path)`t$($Id.blob_oid)`t$($Id.bytes)`t$($Id.sha256)"
}

function Assert-IdEqualsRow($Actual,$Expected,[string]$Reason) {
    if($Actual.mode -ne $Expected.mode -or $Actual.namespace -ne $Expected.namespace -or
       $Actual.path -ne $Expected.path -or $Actual.blob_oid -ne $Expected.blob_oid -or
       $Actual.bytes -ne [int64]$Expected.bytes -or $Actual.sha256 -ne $Expected.sha256) {
        Stop-V3 $Reason
    }
}

function Assert-CleanHead([string]$Repo,[string]$Sha,[string]$Label) {
    $head=(& git -C $Repo rev-parse --verify 'HEAD^{commit}').Trim()
    if($LASTEXITCODE -ne 0 -or $head -ne $Sha){Stop-V3 "V3_HEAD label=$Label"}
    $dirty=@(& git -C $Repo status --porcelain=v1 --untracked-files=all)
    if($LASTEXITCODE -ne 0 -or $dirty.Count){Stop-V3 "V3_DIRTY label=$Label"}
}

function Publish-ManifestV3([ValidateSet('R16','R23')][string]$Ceremony,[string]$Root,
                            [string]$RootId,[string[]]$ContentMembers) {
    $actualBefore=@(Get-ChildItem -LiteralPath $Root -Force -File|ForEach-Object Name)
    Assert-ExactSet $ContentMembers $actualBefore 'V3_MEMBER_SET'
    $lines=[Collections.Generic.List[string]]::new()
    [void]$lines.Add("ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256")
    foreach($name in ($ContentMembers|Sort-Object)){
        $id=Get-RawId (Join-Path $Root $name) $Ceremony 'bundle_member' 'RAW_EXTERNAL_FILE' `
            "EXTERNAL_ROOT@$RootId" $name
        [void]$lines.Add((Format-Id $id))
    }
    $manifestName="${Ceremony}_FREEZE_MANIFEST.tsv"
    $manifest=Join-Path $Root $manifestName
    Write-Utf8Lf $manifest $lines
    $manifestId=Get-RawId $manifest $Ceremony 'freeze_manifest' 'RAW_EXTERNAL_FILE' `
        "EXTERNAL_ROOT@$RootId" $manifestName
    $detachedName="${Ceremony}_FREEZE_MANIFEST.detached.tsv"
    Write-Utf8Lf (Join-Path $Root $detachedName) @(
      "ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256",(Format-Id $manifestId))
    $actualAfter=@(Get-ChildItem -LiteralPath $Root -Force -File|ForEach-Object Name)
    Assert-ExactSet (@($ContentMembers)+$manifestName+$detachedName) $actualAfter 'V3_FINAL_MEMBER_SET'
}
```

Any real implementation must preserve this behavior. Syntax checking a copied fragment is not execution evidence.

## 7. R16 — literal pre-WP-A procedure

### 7.1 Inputs

All actual values are presently `UNKNOWN`. They must arrive in a pre-R16 authority registry independently selected before the freezer starts:

```powershell
$R16Repo='UNKNOWN'
$R16CandidateRepo='UNKNOWN'
$R16Out='UNKNOWN'
$R16BaseSha='UNKNOWN'
$R16CandidateSha='UNKNOWN'
$R16ScopeMembers='UNKNOWN'
$R16ScopeCertificate='UNKNOWN'
$R16ExternalRootId='UNKNOWN'
```

The registry must pin both scope files using the identity schema in §5. A freezer-supplied path is only a local locator; the registry-selected identity is the expectation. If the independent registry or its anchor is absent, R16 stops before output.

### 7.2 Strict scope/certificate gate and complete R16 production

```powershell
function Invoke-R16FreezeV3 {
  param([string]$R16Repo,[string]$R16CandidateRepo,[string]$R16Out,
        [string]$R16BaseSha,[string]$R16CandidateSha,[string]$R16ScopeMembers,
        [string]$R16ScopeCertificate,[string]$R16ExternalRootId)

  foreach($p in $PSBoundParameters.GetEnumerator()){Assert-Known ([string]$p.Value) $p.Key}
  if(Test-Path -LiteralPath $R16Out){Stop-V3 'V3_R16_OUTPUT_EXISTS'}

  $freezeSha=(& git -C $R16Repo rev-parse --verify 'HEAD^{commit}').Trim()
  $baseSha=(& git -C $R16Repo rev-parse --verify "$R16BaseSha^{commit}").Trim()
  $candidateSha=(& git -C $R16Repo rev-parse --verify "$R16CandidateSha^{commit}").Trim()
  foreach($sha in @($freezeSha,$baseSha,$candidateSha)){
    if($sha -notmatch '^[0-9a-f]{40,64}$'){Stop-V3 'V3_R16_SHA'}
  }
  Assert-CleanHead $R16Repo $freezeSha 'R16_FREEZE'
  Assert-CleanHead $R16CandidateRepo $candidateSha 'R16_CANDIDATE'

  $memberColumns=@('ceremony','universe_id','role','mode','path','continuity')
  $rows=@(Read-StrictTsv $R16ScopeMembers $memberColumns)
  $certColumns=@('ceremony','universe_id','completeness_status','basis_mode','basis_namespace',
                 'basis_path','member_row_count','published_at_utc')
  $cert=@(Read-StrictTsv $R16ScopeCertificate $certColumns)
  if($rows.Count -eq 0 -or @($rows|Where-Object ceremony -ne 'R16').Count){Stop-V3 'V3_CEREMONY_MISMATCH'}
  if($cert.Count -ne 1 -or $cert[0].ceremony -ne 'R16'){Stop-V3 'V3_SCOPE_CERT_CARDINALITY'}
  $universe=@($rows.universe_id|Sort-Object -Unique)
  if($universe.Count -ne 1 -or $cert[0].universe_id -ne $universe[0] -or
     [int64]$cert[0].member_row_count -ne $rows.Count){Stop-V3 'V3_SCOPE_CERT_BINDING'}
  $allowedRoles=@('scope','artifact','manifest','packet9_close','packet9_index')
  foreach($r in $rows){
    Assert-CanonicalRelative $r.path
    if($r.role -notin $allowedRoles -or $r.mode -notin @('GIT_OBJECT','WORKTREE_RAW') -or
       $r.continuity -notin @('required','not_claimed')){Stop-V3 'V3_R16_SCOPE_ROW'}
  }
  $keys=@($rows|ForEach-Object{"$($_.role)|$($_.mode)|$($_.path)"})
  if(@($keys|Sort-Object -Unique).Count -ne $keys.Count){Stop-V3 'V3_R16_SCOPE_DUPLICATE'}
  foreach($role in @('packet9_close','packet9_index','artifact','manifest')){
    if(@($rows|Where-Object role -eq $role).Count -lt 1){Stop-V3 "V3_R16_ROLE role=$role"}
  }

  [void](New-Item -ItemType Directory -Path $R16Out)
  Copy-Exact $R16ScopeMembers (Join-Path $R16Out 'R16_SCOPE_MEMBERS.tsv')
  Copy-Exact $R16ScopeCertificate (Join-Path $R16Out 'R16_SCOPE_CERTIFICATE.tsv')
  Write-Utf8Lf (Join-Path $R16Out 'R16_COMMITS.tsv') @(
    "ceremony`trole`tsha", "R16`tbase`t$baseSha", "R16`tcandidate`t$candidateSha", "R16`tfreeze`t$freezeSha")

  $patch=Join-Path $R16Out 'R16_BASE_TO_FREEZE.patch'
  & git -C $R16Repo --no-pager diff --binary --full-index --no-ext-diff --output=$patch $baseSha $freezeSha --
  if($LASTEXITCODE -ne 0){Stop-V3 'V3_R16_DIFF_GENERATE'}
  & git -C $R16Repo --no-pager diff --quiet --no-ext-diff $baseSha $freezeSha --
  $diffRc=$LASTEXITCODE; if($diffRc -notin 0,1){Stop-V3 'V3_R16_DIFF_STATUS'}
  $patchId=Get-RawId $patch 'R16' 'base_to_freeze_patch' 'RAW_EXTERNAL_FILE' `
      "EXTERNAL_ROOT@$R16ExternalRootId" 'R16_BASE_TO_FREEZE.patch'
  Write-Utf8Lf (Join-Path $R16Out 'R16_BASE_TO_FREEZE_IDENTITY.tsv') @(
    "ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256",(Format-Id $patchId))
  Write-Utf8Lf (Join-Path $R16Out 'R16_BASE_TO_FREEZE_RESULT.tsv') @(
    "ceremony`tcomparison`tbefore_sha`tafter_sha`tdiff_rc",
    "R16`tR16_BASE_TO_FREEZE`t$baseSha`t$freezeSha`t$diffRc")

  $tree=@(& git -C $R16Repo ls-tree -r --full-tree $freezeSha)
  if($LASTEXITCODE -ne 0){Stop-V3 'V3_R16_TREE'}
  Write-Utf8Lf (Join-Path $R16Out 'R16_FULL_TRACKED_TREE.txt') $tree

  $frozen=[Collections.Generic.List[string]]::new()
  [void]$frozen.Add("ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256")
  $compare=[Collections.Generic.List[string]]::new()
  [void]$compare.Add("ceremony`tuniverse_id`trole`tmode`tpath`tbefore_namespace`tbefore_blob_oid`tbefore_bytes`tbefore_sha256`tafter_namespace`tafter_blob_oid`tafter_bytes`tafter_sha256`tmatch")
  foreach($r in $rows){
    if($r.mode -eq 'GIT_OBJECT'){
      $after=Get-GitId $R16Repo $freezeSha $r.path 'R16' $r.role
      if($r.continuity -eq 'required'){$before=Get-GitId $R16Repo $candidateSha $r.path 'R16' $r.role}
    }else{
      $after=Get-RawId (Join-Path $R16Repo $r.path) 'R16' $r.role 'WORKTREE_RAW' `
          "WORKTREE@$freezeSha@R16_FREEZE" $r.path
      if($r.continuity -eq 'required'){
        $before=Get-RawId (Join-Path $R16CandidateRepo $r.path) 'R16' $r.role 'WORKTREE_RAW' `
            "WORKTREE@$candidateSha@R16_CANDIDATE" $r.path
      }
    }
    [void]$frozen.Add((Format-Id $after))
    if($r.continuity -eq 'required'){
      $match=($before.mode -eq $after.mode -and $before.bytes -eq $after.bytes -and
              $before.sha256 -eq $after.sha256 -and
              ($r.mode -ne 'GIT_OBJECT' -or $before.blob_oid -eq $after.blob_oid))
      [void]$compare.Add("R16`t$($r.universe_id)`t$($r.role)`t$($r.mode)`t$($r.path)`t$($before.namespace)`t$($before.blob_oid)`t$($before.bytes)`t$($before.sha256)`t$($after.namespace)`t$($after.blob_oid)`t$($after.bytes)`t$($after.sha256)`t$match")
    }
  }
  Write-Utf8Lf (Join-Path $R16Out 'R16_FROZEN_SCOPE_IDENTITIES.tsv') $frozen
  Write-Utf8Lf (Join-Path $R16Out 'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv') $compare

  $resultColumns=@('ceremony','universe_id','role','mode','path','before_namespace','before_blob_oid',
    'before_bytes','before_sha256','after_namespace','after_blob_oid','after_bytes','after_sha256','match')
  $results=@(Read-StrictTsv (Join-Path $R16Out 'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv') $resultColumns)
  $required=@($rows|Where-Object continuity -eq 'required'); $outside=@($rows|Where-Object continuity -eq 'not_claimed')
  if($results.Count -ne $required.Count){Stop-V3 'V3_R16_TERMINAL_CONSERVATION'}
  $bad=@($results|Where-Object match -ne 'True')
  $basisVerified=$false # set true only by the independent-auditor basis-verification record
  $overall=if($cert[0].completeness_status -eq 'COMPLETE' -and $basisVerified -and
              $outside.Count -eq 0 -and $bad.Count -eq 0){
    "OVERALL_UNCHANGED relative_to=$($universe[0]) basis=$($cert[0].basis_namespace):$($cert[0].basis_path)"
  }else{
    "NO_OVERALL_UNCHANGED_CLAIM universe=$($universe[0]) cert=$($cert[0].completeness_status) basis_verified=$basisVerified outside=$($outside.Count) changed=$($bad.Count)"
  }
  Write-Utf8Lf (Join-Path $R16Out 'R16_UNCHANGED_CONCLUSION.tsv') @(
    "ceremony`tuniverse_id`ttotal`tcompared`toutside_claim`tchanged`tconclusion",
    "R16`t$($universe[0])`t$($rows.Count)`t$($required.Count)`t$($outside.Count)`t$($bad.Count)`t$overall")

  if(-not (Test-Path -LiteralPath (Join-Path $R16Out 'R16_TRANSCRIPT.txt'))){Stop-V3 'V3_R16_TRANSCRIPT'}
  $members=@('R16_SCOPE_MEMBERS.tsv','R16_SCOPE_CERTIFICATE.tsv','R16_COMMITS.tsv',
    'R16_BASE_TO_FREEZE.patch','R16_BASE_TO_FREEZE_IDENTITY.tsv','R16_BASE_TO_FREEZE_RESULT.tsv',
    'R16_FULL_TRACKED_TREE.txt','R16_FROZEN_SCOPE_IDENTITIES.tsv',
    'R16_CANDIDATE_TO_FREEZE_IDENTITIES.tsv','R16_UNCHANGED_CONCLUSION.tsv','R16_TRANSCRIPT.txt')
  Publish-ManifestV3 'R16' $R16Out $R16ExternalRootId $members
}
```

The `$basisVerified` value may not be set by the freezer. The actual production wrapper must read a registry-pinned independent basis-verification record and compare its identity before setting it true. Because that record is presently `UNKNOWN`, the executable outcome today is necessarily `NO_OVERALL_UNCHANGED_CLAIM`, not a global conclusion.

## 8. R23 — literal final-freeze procedure

### 8.1 Required authority inputs

```powershell
$R23Repo='UNKNOWN'
$R23Out='UNKNOWN'
$R23ExternalRootId='UNKNOWN'
$R23InputRegistry='UNKNOWN'
$PriorR16Root='UNKNOWN'
$Audit2CloseFile='UNKNOWN'
$R23ScopeMembers='UNKNOWN'
$R23ScopeCertificate='UNKNOWN'
$WpaAuthorityParent='UNKNOWN'
```

`R23InputRegistry` is the only selection authority. It is published before the R23 freezer starts and is obtained independently by the auditor. It must uniquely identify the prior R16 descriptor/manifest/detached identity, Audit-2 close, R23 scope members/certificate, `WP_A_TESTED_ARTIFACT_AUTHORITY_V1.descriptor.tsv`, and R23 chronology publication. Runtime paths are locators only; recomputed identities must equal the registry rows before parsing.

Since the registry and WP-A authority are currently `UNKNOWN`, the real procedure stops. The remainder is the exact conditional procedure that becomes reachable only after those sources exist.

### 8.2 Verify the exact prior R16 and accepting Audit-2 boundary

```powershell
function Invoke-R23FreezeV3 {
  param([string]$R23Repo,[string]$R23Out,[string]$R23ExternalRootId,[string]$R23InputRegistry,
        [string]$PriorR16Root,[string]$Audit2CloseFile,[string]$R23ScopeMembers,
        [string]$R23ScopeCertificate,[string]$WpaAuthorityParent)

  foreach($p in $PSBoundParameters.GetEnumerator()){
    if([string]$p.Value -eq 'UNKNOWN' -and $p.Key -eq 'WpaAuthorityParent'){
      Stop-V3 'V3_WPA_AUTHORITY_NOT_ESTABLISHED'
    }
    Assert-Known ([string]$p.Value) $p.Key
  }
  if(Test-Path -LiteralPath $R23Out){Stop-V3 'V3_R23_OUTPUT_EXISTS'}

  # The adopted v3 checker must contain the registry's pinned Git-object identity.
  # These are facts, not operator inputs; they remain UNKNOWN in the present document.
  $PinnedRegistryCommit='UNKNOWN'
  $PinnedRegistryPath='UNKNOWN'
  $PinnedRegistryBlobOid='UNKNOWN'
  $PinnedRegistryBytes='UNKNOWN'
  $PinnedRegistrySha256='UNKNOWN'
  foreach($v in @($PinnedRegistryCommit,$PinnedRegistryPath,$PinnedRegistryBlobOid,
                  $PinnedRegistryBytes,$PinnedRegistrySha256)){
    if($v -eq 'UNKNOWN'){Stop-V3 'V3_R23_REGISTRY_NOT_ESTABLISHED'}
  }
  $registryGit=Get-GitId $R23Repo $PinnedRegistryCommit $PinnedRegistryPath 'R23' 'input_registry'
  if($registryGit.blob_oid -ne $PinnedRegistryBlobOid -or
     $registryGit.bytes -ne [int64]$PinnedRegistryBytes -or
     $registryGit.sha256 -ne $PinnedRegistrySha256){Stop-V3 'V3_AUTHORITY_IDENTITY_MISMATCH'}
  $registryRaw=Get-RawId $R23InputRegistry 'R23' 'input_registry' 'WORKTREE_RAW' `
      "WORKTREE@$PinnedRegistryCommit@R23_INPUT_REGISTRY" $PinnedRegistryPath
  # A registry row separately pins this raw form; compare it before using any selected locator.

  $idColumns=@('ceremony','role','mode','namespace','path','blob_oid','bytes','sha256')
  $r16Manifest=Join-Path $PriorR16Root 'R16_FREEZE_MANIFEST.tsv'
  $r16Detached=Join-Path $PriorR16Root 'R16_FREEZE_MANIFEST.detached.tsv'
  $detached=@(Read-StrictTsv $r16Detached $idColumns)
  if($detached.Count -ne 1 -or $detached[0].ceremony -ne 'R16' -or
     $detached[0].role -ne 'freeze_manifest' -or $detached[0].mode -ne 'RAW_EXTERNAL_FILE' -or
     $detached[0].path -ne 'R16_FREEZE_MANIFEST.tsv'){Stop-V3 'V3_PRIOR_R16_DETACHED'}
  $manifestActual=Get-RawId $r16Manifest 'R16' 'freeze_manifest' 'RAW_EXTERNAL_FILE' `
      $detached[0].namespace $detached[0].path
  Assert-IdEqualsRow $manifestActual $detached[0] 'V3_PRIOR_R16_ANCHOR_MISMATCH'
  # The registry-selected prior-R16 row must also equal $manifestActual here.

  $manifestRows=@(Read-StrictTsv $r16Manifest $idColumns)
  $commitMember=@($manifestRows|Where-Object path -eq 'R16_COMMITS.tsv')
  if($commitMember.Count -ne 1){Stop-V3 'V3_PRIOR_R16_COMMIT_MEMBER'}
  $commitFile=Join-Path $PriorR16Root 'R16_COMMITS.tsv'
  $commitActual=Get-RawId $commitFile 'R16' 'bundle_member' 'RAW_EXTERNAL_FILE' `
      $commitMember[0].namespace 'R16_COMMITS.tsv'
  Assert-IdEqualsRow $commitActual $commitMember[0] 'V3_PRIOR_R16_COMMIT_MEMBER_ID'
  $commitRows=@(Read-StrictTsv $commitFile @('ceremony','role','sha'))
  $freeze=@($commitRows|Where-Object {$_.ceremony -eq 'R16' -and $_.role -eq 'freeze'})
  if($freeze.Count -ne 1 -or $freeze[0].sha -notmatch '^[0-9a-f]{40,64}$'){
    Stop-V3 'V3_PRIOR_R16_SHA_CARDINALITY'
  }
  $DerivedR16Sha=$freeze[0].sha

  $closeColumns=@('record_kind','audit_cycle_id','verdict','r16_freeze_sha',
                  'r16_manifest_sha256','closed_at_utc')
  $close=@(Read-StrictTsv $Audit2CloseFile $closeColumns)
  if($close.Count -ne 1 -or $close[0].record_kind -ne 'AUDIT2_CLOSE' -or
     $close[0].verdict -notin @('PASS','PASS-WITH-NITS')){Stop-V3 'V3_AUDIT2_CLOSE'}
  if($close[0].r16_freeze_sha -ne $DerivedR16Sha -or
     $close[0].r16_manifest_sha256 -ne $manifestActual.sha256){
    Stop-V3 'V3_AUDIT2_R16_BINDING'
  }
  $Audit2Time=[datetime]::ParseExact($close[0].closed_at_utc,'yyyy-MM-ddTHH:mm:ss.fffffffZ',
      [Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::AssumeUniversal)
  # The registry-selected Audit-2 row must equal the recomputed close identity before this parse.
```

### 8.3 Verify the non-self-referential WP-A authority publication

```powershell
  $descriptorPath=Join-Path $WpaAuthorityParent 'WP_A_TESTED_ARTIFACT_AUTHORITY_V1.descriptor.tsv'
  $descriptorColumns=@('publication_id','producer_id','producer_role','closed_at_utc','member_root_name',
    'manifest_mode','manifest_namespace','manifest_path','manifest_blob_oid','manifest_bytes','manifest_sha256')
  $descriptor=@(Read-StrictTsv $descriptorPath $descriptorColumns)
  if($descriptor.Count -ne 1 -or $descriptor[0].producer_role -ne 'WP_A_CAPTURE_AUTHORITY'){
    Stop-V3 'V3_WPA_DESCRIPTOR'
  }
  # Before this point, recompute the descriptor identity and require exact equality to the
  # registry-selected descriptor row. A matching adjacent descriptor is not a trust root.
  $memberRoot=Join-Path $WpaAuthorityParent $descriptor[0].member_root_name
  $manifestPath=Join-Path $WpaAuthorityParent $descriptor[0].manifest_path
  if((Split-Path -Parent $manifestPath) -ne (Get-Item -LiteralPath $WpaAuthorityParent).FullName){
    Stop-V3 'V3_WPA_MANIFEST_NOT_DETACHED'
  }
  $manifestActual=Get-RawId $manifestPath 'R23' 'wpa_authority_manifest' 'RAW_EXTERNAL_FILE' `
      $descriptor[0].manifest_namespace $descriptor[0].manifest_path
  if($descriptor[0].manifest_mode -ne 'RAW_EXTERNAL_FILE' -or
     $manifestActual.bytes -ne [int64]$descriptor[0].manifest_bytes -or
     $manifestActual.sha256 -ne $descriptor[0].manifest_sha256){
    Stop-V3 'V3_WPA_MANIFEST_IDENTITY'
  }

  $memberColumns=@('publication_id','role','mode','namespace','path','blob_oid','bytes','sha256')
  $memberRows=@(Read-StrictTsv $manifestPath $memberColumns)
  if($memberRows.Count -eq 0 -or @($memberRows|Where-Object publication_id -ne $descriptor[0].publication_id).Count){
    Stop-V3 'V3_WPA_PUBLICATION_ID'
  }
  foreach($r in $memberRows){
    Assert-CanonicalRelative $r.path
    if($r.mode -ne 'RAW_EXTERNAL_FILE' -or $r.blob_oid -ne '-'){
      Stop-V3 'V3_WPA_MEMBER_MODE'
    }
  }
  $paths=@($memberRows.path)
  if(@($paths|Sort-Object -Unique).Count -ne $paths.Count){Stop-V3 'V3_WPA_MEMBER_DUPLICATE'}
  foreach($role in @('events','tested_artifact','producer_separation')){
    if(@($memberRows|Where-Object role -eq $role).Count -ne 1){
      Stop-V3 "V3_WPA_MANDATORY_ROLE role=$role"
    }
  }
  $actualPaths=@(Get-ChildItem -LiteralPath $memberRoot -Recurse -Force -File|ForEach-Object{
    [IO.Path]::GetRelativePath($memberRoot,$_.FullName).Replace('\','/')})
  Assert-ExactSet $paths $actualPaths 'V3_WPA_MEMBER_SET'
  foreach($r in $memberRows){
    $actual=Get-RawId (Join-Path $memberRoot $r.path) 'R23' $r.role 'RAW_EXTERNAL_FILE' `
        $r.namespace $r.path
    Assert-IdEqualsRow $actual $r 'V3_WPA_MEMBER_IDENTITY'
  }
```

### 8.4 Verify event truth inputs and chronology before extracting expectations

```powershell
  $eventMember=@($memberRows|Where-Object role -eq 'events')[0]
  $eventsPath=Join-Path $memberRoot $eventMember.path
  $eventColumns=@('event_id','sequence','occurred_at_utc','capture_id','artifact_id','tested_sha',
    'source_role','source_mode','source_namespace','source_path','source_blob_oid','source_bytes','source_sha256')
  $events=@(Read-StrictTsv $eventsPath $eventColumns)
  $requiredEvents=@('WPA_BEGAN','WPA_COMPLETED','WPA_EVIDENCE_CAPTURE_CLOSED')
  Assert-ExactSet $requiredEvents @($events.event_id) 'V3_EVENT_SET'
  $previousSeq=[int64]::MinValue; $previousTime=$Audit2Time
  foreach($eventId in $requiredEvents){
    $e=@($events|Where-Object event_id -eq $eventId)
    if($e.Count -ne 1){Stop-V3 'V3_EVENT_CARDINALITY'}
    $seq=0L
    if(-not [int64]::TryParse($e[0].sequence,[ref]$seq)){Stop-V3 'V3_EVENT_SEQUENCE_FORMAT'}
    $time=[datetime]::ParseExact($e[0].occurred_at_utc,'yyyy-MM-ddTHH:mm:ss.fffffffZ',
      [Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::AssumeUniversal)
    if($seq -le $previousSeq -or $time -le $previousTime){Stop-V3 'V3_EVENT_ORDER'}
    $previousSeq=$seq; $previousTime=$time

    $source=@($memberRows|Where-Object {$_.role -eq $e[0].source_role -and $_.path -eq $e[0].source_path})
    if($source.Count -ne 1){Stop-V3 'V3_EVENT_SOURCE_CARDINALITY'}
    $sourceActual=Get-RawId (Join-Path $memberRoot $source[0].path) 'R23' $source[0].role `
        'RAW_EXTERNAL_FILE' $source[0].namespace $source[0].path
    Assert-IdEqualsRow $sourceActual $source[0] 'V3_EVENT_SOURCE_MEMBER_IDENTITY'
    if($e[0].source_mode -ne $source[0].mode -or $e[0].source_namespace -ne $source[0].namespace -or
       $e[0].source_blob_oid -ne $source[0].blob_oid -or
       [int64]$e[0].source_bytes -ne $source[0].bytes -or
       $e[0].source_sha256 -ne $source[0].sha256){Stop-V3 'V3_EVENT_SOURCE_CROSS_BINDING'}
  }
  $wpaCompleted=@($events|Where-Object event_id -eq 'WPA_COMPLETED')
  if($wpaCompleted.Count -ne 1){Stop-V3 'V3_WPA_COMPLETED_CARDINALITY'}
  $DerivedCaptureId=$wpaCompleted[0].capture_id
  $DerivedArtifactId=$wpaCompleted[0].artifact_id
  $DerivedTestedSha=$wpaCompleted[0].tested_sha
  foreach($v in @($DerivedCaptureId,$DerivedArtifactId,$DerivedTestedSha)){Assert-Known $v 'WPA_SELECTOR'}
  if($DerivedTestedSha -notmatch '^[0-9a-f]{40,64}$'){Stop-V3 'V3_WPA_TESTED_SHA_FORMAT'}
```

This block verifies record integrity, source membership, cross-binding, and ordering. It supports only: “the independently anchored records are intact and mutually consistent.” If the producer/separation evidence does not establish real-world authority, the auditor returns BLOCK; hashes cannot upgrade the narrative to truth.

### 8.5 Verify R23 scope, exact SHA, ancestry, diff, tree, and identities

```powershell
  $scopeColumns=@('ceremony','universe_id','role','mode','path','continuity')
  $scope=@(Read-StrictTsv $R23ScopeMembers $scopeColumns)
  $certColumns=@('ceremony','universe_id','completeness_status','basis_mode','basis_namespace',
                 'basis_path','member_row_count','published_at_utc')
  $scopeCert=@(Read-StrictTsv $R23ScopeCertificate $certColumns)
  if($scope.Count -eq 0 -or @($scope|Where-Object ceremony -ne 'R23').Count){Stop-V3 'V3_CEREMONY_MISMATCH'}
  $scopeUniverse=@($scope.universe_id|Sort-Object -Unique)
  if($scopeCert.Count -ne 1 -or $scopeCert[0].ceremony -ne 'R23' -or
     $scopeUniverse.Count -ne 1 -or $scopeCert[0].universe_id -ne $scopeUniverse[0] -or
     [int64]$scopeCert[0].member_row_count -ne $scope.Count){Stop-V3 'V3_R23_SCOPE_CERT'}
  $allowedR23Roles=@('final_scope','final_artifact','final_manifest')
  foreach($r in $scope){
    Assert-CanonicalRelative $r.path
    if($r.role -notin $allowedR23Roles -or $r.mode -notin @('GIT_OBJECT','WORKTREE_RAW')){
      Stop-V3 'V3_R23_SCOPE_ROW'
    }
  }
  $scopeKeys=@($scope|ForEach-Object{"$($_.role)|$($_.mode)|$($_.path)"})
  if(@($scopeKeys|Sort-Object -Unique).Count -ne $scopeKeys.Count){Stop-V3 'V3_R23_SCOPE_DUPLICATE'}

  $R23FreezeSha=(& git -C $R23Repo rev-parse --verify 'HEAD^{commit}').Trim()
  if($R23FreezeSha -notmatch '^[0-9a-f]{40,64}$'){Stop-V3 'V3_R23_SHA'}
  Assert-CleanHead $R23Repo $R23FreezeSha 'R23_FREEZE'
  & git -C $R23Repo merge-base --is-ancestor $DerivedR16Sha $R23FreezeSha
  if($LASTEXITCODE -ne 0){Stop-V3 'V3_PRIOR_R16_NOT_ANCESTOR'}

  [void](New-Item -ItemType Directory -Path $R23Out)
  Copy-Exact $R23InputRegistry (Join-Path $R23Out 'R23_INPUT_REGISTRY.tsv')
  Copy-Exact $r16Manifest (Join-Path $R23Out 'R23_INPUT_R16_FREEZE_MANIFEST.tsv')
  Copy-Exact $r16Detached (Join-Path $R23Out 'R23_INPUT_R16_FREEZE_MANIFEST.detached.tsv')
  Copy-Exact $Audit2CloseFile (Join-Path $R23Out 'R23_INPUT_AUDIT2_CLOSE.tsv')
  Copy-Exact $R23ScopeMembers (Join-Path $R23Out 'R23_SCOPE_MEMBERS.tsv')
  Copy-Exact $R23ScopeCertificate (Join-Path $R23Out 'R23_SCOPE_CERTIFICATE.tsv')
  Copy-Exact $descriptorPath (Join-Path $R23Out 'R23_INPUT_WPA_AUTHORITY_DESCRIPTOR.tsv')
  Copy-Exact $manifestPath (Join-Path $R23Out 'R23_INPUT_WPA_AUTHORITY_MANIFEST.tsv')
  Copy-Exact $eventsPath (Join-Path $R23Out 'R23_INPUT_WPA_EVENTS.tsv')

  Write-Utf8Lf (Join-Path $R23Out 'R23_COMMITS.tsv') @(
    "ceremony`trole`tsha","R23`tverified_prior_r16`t$DerivedR16Sha","R23`tfreeze`t$R23FreezeSha")
  $patch=Join-Path $R23Out 'R23_VERIFIED_R16_TO_FINAL.patch'
  & git -C $R23Repo --no-pager diff --binary --full-index --no-ext-diff `
      --output=$patch $DerivedR16Sha $R23FreezeSha --
  if($LASTEXITCODE -ne 0){Stop-V3 'V3_R23_DIFF_GENERATE'}
  & git -C $R23Repo --no-pager diff --quiet --no-ext-diff $DerivedR16Sha $R23FreezeSha --
  $diffRc=$LASTEXITCODE; if($diffRc -notin 0,1){Stop-V3 'V3_R23_DIFF_STATUS'}
  $patchId=Get-RawId $patch 'R23' 'verified_r16_to_final_patch' 'RAW_EXTERNAL_FILE' `
      "EXTERNAL_ROOT@$R23ExternalRootId" 'R23_VERIFIED_R16_TO_FINAL.patch'
  Write-Utf8Lf (Join-Path $R23Out 'R23_VERIFIED_R16_TO_FINAL_IDENTITY.tsv') @(
    "ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256",(Format-Id $patchId))
  Write-Utf8Lf (Join-Path $R23Out 'R23_VERIFIED_R16_TO_FINAL_RESULT.tsv') @(
    "ceremony`tcomparison`tbefore_sha`tafter_sha`tdiff_rc",
    "R23`tR23_VERIFIED_R16_TO_FINAL`t$DerivedR16Sha`t$R23FreezeSha`t$diffRc")

  $tree=@(& git -C $R23Repo ls-tree -r --full-tree $R23FreezeSha)
  if($LASTEXITCODE -ne 0){Stop-V3 'V3_R23_TREE'}
  Write-Utf8Lf (Join-Path $R23Out 'R23_FULL_TRACKED_TREE.txt') $tree
  $ids=[Collections.Generic.List[string]]::new()
  [void]$ids.Add("ceremony`trole`tmode`tnamespace`tpath`tblob_oid`tbytes`tsha256")
  foreach($r in $scope){
    $id=if($r.mode -eq 'GIT_OBJECT'){
      Get-GitId $R23Repo $R23FreezeSha $r.path 'R23' $r.role
    }else{
      Get-RawId (Join-Path $R23Repo $r.path) 'R23' $r.role 'WORKTREE_RAW' `
        "WORKTREE@$R23FreezeSha@R23_FREEZE" $r.path
    }
    [void]$ids.Add((Format-Id $id))
  }
  Write-Utf8Lf (Join-Path $R23Out 'R23_FROZEN_SCOPE_IDENTITIES.tsv') $ids
```

### 8.6 Exact F5 extraction, zero/multiple rejection, and same-mode comparison

```powershell
  $artifactMember=@($memberRows|Where-Object role -eq 'tested_artifact')
  if($artifactMember.Count -ne 1){Stop-V3 'V3_WPA_INDEX_MEMBER_CARDINALITY'}
  $artifactPath=Join-Path $memberRoot $artifactMember[0].path
  $artifactColumns=@('record_kind','capture_id','artifact_id','repo_relative_path','mode',
                     'tested_sha','blob_oid','bytes','sha256')
  $artifactRows=@(Read-StrictTsv $artifactPath $artifactColumns)

  # Unique-row selector. Every equality is mandatory and values come only from the unique
  # authority-published WPA_COMPLETED row above.
  $selected=@($artifactRows|Where-Object {
    $_.record_kind -eq 'WP_A_TESTED_ARTIFACT' -and
    $_.capture_id -ceq $DerivedCaptureId -and
    $_.artifact_id -ceq $DerivedArtifactId -and
    $_.tested_sha -ceq $DerivedTestedSha
  })
  $selectedGit=@($selected|Where-Object mode -ceq 'GIT_OBJECT')
  $selectedRaw=@($selected|Where-Object mode -ceq 'WORKTREE_RAW')
  if($selected.Count -ne 2 -or $selectedGit.Count -ne 1 -or $selectedRaw.Count -ne 1){
    Stop-V3 "V3_WPA_SELECTOR_CARDINALITY selected=$($selected.Count) git=$($selectedGit.Count) raw=$($selectedRaw.Count)"
  }
  if($selectedGit[0].repo_relative_path -cne $selectedRaw[0].repo_relative_path -or
     $selectedGit[0].tested_sha -cne $selectedRaw[0].tested_sha){
    Stop-V3 'V3_WPA_SELECTOR_CROSS_MODE_BINDING'
  }
  if($selectedGit[0].blob_oid -notmatch '^[0-9a-f]{40,64}$' -or
     $selectedRaw[0].blob_oid -ne '-' -or
     $selectedGit[0].sha256 -notmatch '^[0-9a-f]{64}$' -or
     $selectedRaw[0].sha256 -notmatch '^[0-9a-f]{64}$'){
    Stop-V3 'V3_WPA_SELECTOR_IDENTITY_FORMAT'
  }
  $DerivedArtifactPath=$selectedGit[0].repo_relative_path
  Assert-CanonicalRelative $DerivedArtifactPath
  Write-Utf8Lf (Join-Path $R23Out 'R23_WPA_EXPECTED_ROWS.tsv') @(
    ($artifactColumns -join "`t"),$selectedGit[0]._raw_line,$selectedRaw[0]._raw_line)

  $finalGit=Get-GitId $R23Repo $R23FreezeSha $DerivedArtifactPath 'R23' 'final_artifact'
  $finalRaw=Get-RawId (Join-Path $R23Repo $DerivedArtifactPath) 'R23' 'final_artifact' `
      'WORKTREE_RAW' "WORKTREE@$R23FreezeSha@R23_FREEZE" $DerivedArtifactPath
  $gitMatch=($finalGit.blob_oid -eq $selectedGit[0].blob_oid -and
             $finalGit.bytes -eq [int64]$selectedGit[0].bytes -and
             $finalGit.sha256 -eq $selectedGit[0].sha256)
  $rawMatch=($finalRaw.bytes -eq [int64]$selectedRaw[0].bytes -and
             $finalRaw.sha256 -eq $selectedRaw[0].sha256)
  Write-Utf8Lf (Join-Path $R23Out 'R23_WPA_TO_FINAL_ARTIFACT.tsv') @(
    "ceremony`tartifact_id`tpath`tmode`texpected_blob_oid`texpected_bytes`texpected_sha256`tfinal_blob_oid`tfinal_bytes`tfinal_sha256`tmatch",
    "R23`t$DerivedArtifactId`t$DerivedArtifactPath`tGIT_OBJECT`t$($selectedGit[0].blob_oid)`t$($selectedGit[0].bytes)`t$($selectedGit[0].sha256)`t$($finalGit.blob_oid)`t$($finalGit.bytes)`t$($finalGit.sha256)`t$gitMatch",
    "R23`t$DerivedArtifactId`t$DerivedArtifactPath`tWORKTREE_RAW`t-`t$($selectedRaw[0].bytes)`t$($selectedRaw[0].sha256)`t-`t$($finalRaw.bytes)`t$($finalRaw.sha256)`t$rawMatch")
  if(-not $gitMatch -or -not $rawMatch){Stop-V3 'V3_WPA_FINAL_MISMATCH'}

  Write-Utf8Lf (Join-Path $R23Out 'R23_CHRONOLOGY_RESULT.tsv') @(
    "ceremony`tresult`tclaim",
    "R23`tCONSISTENT`tindependently anchored records are intact and satisfy Audit2<WPA_BEGAN<WPA_COMPLETED<WPA_EVIDENCE_CAPTURE_CLOSED")
  Write-Utf8Lf (Join-Path $R23Out 'R23_WPA_CAPTURE_RECOMPUTATION.tsv') @(
    "ceremony`tpublication_id`tmanifest_members`tselector_rows`tresult",
    "R23`t$($descriptor[0].publication_id)`t$($memberRows.Count)`t$($selected.Count)`tEXACT_MEMBER_SET_AND_IDENTITIES_MATCH")

  if(-not (Test-Path -LiteralPath (Join-Path $R23Out 'R23_TRANSCRIPT.txt'))){Stop-V3 'V3_R23_TRANSCRIPT'}
```

There is no freezer input for artifact path, byte count, blob OID, or SHA. The selector is case-sensitive and rejects zero rows, one-mode-only rows, three or more rows, duplicate same-mode rows, different cross-mode paths, malformed identities, and final mismatches.

### 8.7 Exact R23 publication member set

```powershell
  $members=@(
    'R23_INPUT_REGISTRY.tsv',
    'R23_INPUT_R16_FREEZE_MANIFEST.tsv',
    'R23_INPUT_R16_FREEZE_MANIFEST.detached.tsv',
    'R23_INPUT_AUDIT2_CLOSE.tsv',
    'R23_SCOPE_MEMBERS.tsv',
    'R23_SCOPE_CERTIFICATE.tsv',
    'R23_INPUT_WPA_AUTHORITY_DESCRIPTOR.tsv',
    'R23_INPUT_WPA_AUTHORITY_MANIFEST.tsv',
    'R23_INPUT_WPA_EVENTS.tsv',
    'R23_COMMITS.tsv',
    'R23_VERIFIED_R16_TO_FINAL.patch',
    'R23_VERIFIED_R16_TO_FINAL_IDENTITY.tsv',
    'R23_VERIFIED_R16_TO_FINAL_RESULT.tsv',
    'R23_FULL_TRACKED_TREE.txt',
    'R23_FROZEN_SCOPE_IDENTITIES.tsv',
    'R23_WPA_EXPECTED_ROWS.tsv',
    'R23_WPA_TO_FINAL_ARTIFACT.tsv',
    'R23_CHRONOLOGY_RESULT.tsv',
    'R23_WPA_CAPTURE_RECOMPUTATION.tsv',
    'R23_TRANSCRIPT.txt')
  Publish-ManifestV3 'R23' $R23Out $R23ExternalRootId $members
}
```

This is a complete literal R23 member-production and manifest call. `Publish-ManifestV3` rejects cross-ceremony tokens and checks the force-inclusive set both before and after manifest creation. No R16 filename substitution or unimplemented comment is required.

## 9. Auditor verification: test the production truth predicate

The auditor must use an independent, local, read-only evidence view. For repository bytes, use a separate exact-SHA audit worktree and require empty pre/post status; that is the established auditor contract. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`

### 9.1 Mandatory acquisition and identity checks

1. Obtain the adopted checker/document identity, R16/R23 registry, scope publications, prior R16 root, Audit-2 close, and WP-A authority directly from their independent publishers or independently selected immutable snapshots.
2. Prove the checker invoked is byte-identical to the checker under review. A helper with equivalent logic is not the production checker.
3. Verify every registry-selected descriptor before opening the source it selects. A descriptor adjacent to a root is not its own anchor.
4. Reopen every event source and completeness basis. Record whether the source establishes only byte integrity, record consistency, or actual event/completeness authority.
5. Recompute Git-object and raw identities in their declared modes. Never use a clean Git status as proof that Windows raw bytes match Git blob bytes.

### 9.2 Required GREEN and RED runs

The evidence package records exact checker bytes/identity, literal command, cwd, PowerShell and Git versions, input-root identities, stdout, stderr, exit status, start/end UTC, and pre/post cleanliness.

Run the unmodified production invocation once as GREEN, then invoke that same procedure against disposable copies for every applicable mutation:

| Mutation | Required production-checker result |
|---|---|
| R16 scope certificate removed, universe ID/count changed, basis unverifiable | STOP or `NO_OVERALL_UNCHANGED_CLAIM`; never `OVERALL_UNCHANGED` |
| One admitted R16 row removed only after parsing or from the result | `V3_R16_TERMINAL_CONSERVATION` |
| One required Git blob changed | `CHANGED`/no overall unchanged |
| Only checkout line endings changed | raw-row mismatch even if Git row remains equal |
| R23 prior R16 replaced with a different ancestor | `V3_PRIOR_R16_ANCHOR_MISMATCH` or registry identity stop |
| Audit-2 close removed/replaced or bound to another R16 | `V3_AUDIT2_CLOSE` or `V3_AUDIT2_R16_BINDING` |
| WP-A descriptor/root replaced with a mutually consistent freezer-created set | registry-selected descriptor identity mismatch |
| Authority root gains an extra hidden file | `V3_WPA_MEMBER_SET` |
| Event source bytes change, event duplicated, sequence/time regresses | source-identity, event-set/cardinality, or `V3_EVENT_ORDER` stop |
| Selector matches zero rows | `V3_WPA_SELECTOR_CARDINALITY selected=0 git=0 raw=0` |
| Selector matches two Git rows and one raw row | `V3_WPA_SELECTOR_CARDINALITY selected=3 git=2 raw=1` |
| Expected Git and raw rows name different paths | `V3_WPA_SELECTOR_CROSS_MODE_BINDING` |
| Authority remains fixed; final Git object changes | `V3_WPA_FINAL_MISMATCH` |
| Authority remains fixed; only final raw materialization changes | `V3_WPA_FINAL_MISMATCH` |
| Required R23 output removed or hidden extra added | `V3_MEMBER_SET` or `V3_FINAL_MEMBER_SET` |

For F5, the current first run is not GREEN: it is the required stop `V3_WPA_AUTHORITY_NOT_ESTABLISHED`. Do not fabricate a fixture and call it closure evidence. A fixture may validate selector syntax, but F5 remains open until the real independent authority exists and the actual production path shows GREEN plus both cardinality and final-mismatch RED arms.

### 9.3 Truth limit and verdict rule

- Recomputing the freezer’s hashes proves arithmetic only.
- Invoking the production checker with mutations proves the checker discriminates.
- Comparing against independently acquired authority proves binding to that authority.
- Establishing that the authority describes real WP-A requires independent producer/separation evidence.

If any layer is absent, say which layer is `UNKNOWN` and stop. Do not collapse these four claims into “verified.” This directly applies the standing questions: what makes the check fail, where the expected value came from, what lies outside the universe, and whether a mechanism enforces the property. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`

## 10. Publication prohibitions

### R16 may not publish if

- its independent registry, scope members, certificate, completeness basis, Packet-9 inputs, or publication identity is `UNKNOWN` or mismatched;
- any identity mode/path/OID/bytes/SHA is absent or ambiguous;
- an admitted member lacks exactly one terminal disposition;
- `OVERALL_UNCHANGED` is emitted without a verified `COMPLETE` certificate, zero outside-claim rows, and zero mismatches;
- exact output membership or detached-manifest identity fails.

### R23 may not publish if

- `WP_A_TESTED_ARTIFACT_AUTHORITY_V1` does not exist or its actual independence is not established;
- the adopted checker still contains any pinned registry fact as `UNKNOWN`;
- a runtime path selects bytes not equal to the registry-selected identity;
- the prior R16/Audit-2 binding or event order is absent, ambiguous, or inconsistent;
- the WP-A member root/manifest is self-referential, missing, extra, duplicate, changed, or unreadable;
- the unique selector does not yield exactly one Git and one raw row for one path/tested SHA;
- either final same-mode identity differs;
- an authority source can be mutated by the freezer after close;
- a RED/GREEN package reimplements rather than invokes the production check;
- exact R23 output membership or detached-manifest identity fails.

## 11. Exact claims and deliberately excluded claims

| Output | Exact claim | Not claimed |
|---|---|---|
| R16 per-row result | The named before/after identity matches or differs in the named mode. | Other paths, modes, or real-world relevance. |
| R16 overall result | Only when enabled by a verified independent completeness certificate: every row in that exact universe reached one matching terminal disposition. | Files omitted by the certified basis or a broader “everything relevant” assertion. |
| R16/R23 boundary | The registry-selected R16 manifest/SHA is the one bound by the uniquely accepting close, and R23 descends from it. | Acceptance of R23 or authority for any later action. |
| WP-A authority root | Current bytes equal the independently selected, non-self-referential publication. | Truth of WP-A unless producer/separation authority is established. |
| WP-A selector | Exactly one Git row and one raw row match the unique authority-published `WPA_COMPLETED` selector. | Any other artifact/path/mode. |
| WP-A-to-final comparison | Final Git object and final raw materialization equal those two authority rows in the same modes. | Closure today: the independent authority does not yet exist. |
| Chronology | Independently acquired records and reopened sources are intact and ordered. | Personal observation by the freezer or real-world truth beyond publisher authority. |
| Bundle manifest | Exact membership inside the named output root. | Anything outside that root. |

## 12. Final status

V3 fixes the procedure shapes that made v2 incomplete: it gives literal R23 tree/scope/diff/identity/member/manifest commands; mechanically binds descriptors to a pinned registry before parsing; puts the WP-A manifest outside its enumerated root; gates any overall unchanged claim on an independent completeness certificate and basis verification; keeps Git-object and raw identities distinct; reopens event sources; and requires auditors to mutate and invoke the production checker rather than reimplement it.

F5 is intentionally not declared closed. The project has not yet produced or established an independent `WP_A_TESTED_ARTIFACT_AUTHORITY_V1`. The only truthful operational result is:

> **CANNOT BE CLOSED UNTIL `WP_A_TESTED_ARTIFACT_AUTHORITY_V1` EXISTS.**

This v3 remains **NOT ACCEPTED**, performs no action, and grants no authorization.

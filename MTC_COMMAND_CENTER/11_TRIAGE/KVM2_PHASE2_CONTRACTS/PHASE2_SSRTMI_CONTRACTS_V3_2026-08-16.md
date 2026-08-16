Status: PHASE2 CONTRACT SET V3 — secret/state/recovery/teardown/maintenance/incident — SUPERSEDES V2 AND HL_LIVE_ACK_V3 — NOT ACCEPTED

# KVM2 Phase-2 contracts V3 — secret, state, recovery, teardown, maintenance, incident

| Finding | V3 closure mechanism | Cite |
|---|---|---|
| Secret checker inspected only one section | The agreement checker removes non-normative fenced examples, then scans the entire remaining secret-contract prose for a second policy, local list, narrowing, override, or service-surface exception. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:131-348` |
| Secret checker asserted rather than verified same-candidate identity | One independently frozen binding record supplies a candidate ID and SHA-256 for each of the service and secret documents; missing, malformed, mixed, path-mismatched, or hash-mismatched identity is STOP. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:98-130` |
| State had no exact four-class clean predicates | The v4 schema, schema-catalog binding, complete business-table zero census, four literal SQL predicates, raw-exchange input record, and read-only verifier outcome grammar are frozen here. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:359-444` |
| Recovery denial could turn a missing target into GREEN | A retained, non-secret, exact-version canary is proven present before and after two routine-role probes; only an authenticated provider-native authority-denial tuple is GREEN. Not-found is STOP. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:446-526` |
| Teardown discovery was only a category assertion | Every teardown category now has an independent collector, sources, stable identity, terminal grammar, completeness rule, STOP rule, and falsification. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:528-589` |
| Maintenance policy values remained open in several places | All origins, packages, commands, blackout, reboot, and restart decisions are fields of one closed owner-input record; absence or any unfilled field STOPs. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:591-639` |
| Incident credential universe lacked exact discovery sources | The universe is the union of the names inventory and exact independent store and consumer collectors, with backend coverage and terminal accounting. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:658-692` |
| Incident capability denial could turn a missing target into GREEN | A known-valid local canary, pinned errno helper, privileged pre/post observations, and an exact errno grammar accept only `EACCES` or `EPERM`; target-not-found is STOP. | `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md:693-732` |

The findings and required remedies are the independent verdict of record
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_V2_INDEPENDENT_VERDICTS_2026-08-16.md:15-20,27-31`). This is a T2
documentation/evidence repair only. It makes no host claim, performs no operational check,
and grants no acceptance or authority.

## 0. Supersession, inputs, and binding outcome grammar

This single document replaces, in full, both
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md`
and
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_CONTRACT_HL_LIVE_ACK_V3_2026-08-16.md`.
Neither superseded document may be combined with V3 to fill a missing value or relax a
V3 result. V2 mechanisms that the review found closed remain binding here: independent
expectations, producer/verifier separation, terminal accounting, effective-state
observation, and STOP on incomplete observation
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_V2_INDEPENDENT_VERDICTS_2026-08-16.md:15-20`;
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:12-23`).

Every V3 check has exactly three semantic outcomes:

- **PASS/GREEN:** the observation completed, its universe is complete, and it equals an
  expectation frozen independently of the producer or action under test.
- **FAIL/RED:** the observation completed and positively found deviant state.
- **STOP/BLOCK:** the observation could not be completed or interpreted, a required input
  is absent/unfrozen, an identity does not bind, a backend is unmodelled, or terminal
  accounting does not conserve. STOP is never converted to FAIL or PASS.

Each probe captures completion, status, output, and diagnostics before content is
interpreted. A producer's manifest, hash, inventory, explanation, or canonical result is
supplemental unless an independent record supplied the expectation. This applies the
project's falsifiability test and STOP-first ordering
(`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63,73-83`;
`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107,368-420,933-967`).

No check below is execution evidence. Before operational use, its real implementation must
be shown RED against the stated falsification and GREEN against the conforming fixture. A
missing RED/GREEN transcript leaves the check UNVERIFIED; it does not change the specified
PASS/FAIL/STOP grammar.

## 1. Secret contract

### 1.1 Required end state retained from V2

The wallet remains deferred: no wallet is provisioned, requested, inferred, generated,
stored, or represented by a key value, and the first-start checklist remains blocked
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`). A future
separately authorized mechanism may use one sanctioned root-owned `0600` at-rest source;
the service's runtime copy is not a second at-rest store. Secret values remain forbidden
from arguments, logs, journal, diagnostics, crash/core output, manifests, evidence,
screenshots, exports, and backups. The concrete future wallet-delivery channel is not
established by the sources and therefore remains a prerequisite supplied only by the named
`KVM2_SECRET_DELIVERY_OWNER_INPUT_V1`; its absence blocks, and V3 does not guess it
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:27-42,58-77`).

<!-- BEGIN V3 SECRET/SERVICE AGREEMENT -->
### 1.2 Normative `HL_LIVE_ACK` deference — the only local agreement section

Normative source file: `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md`

Normative source heading: `### 4.2 Normative HL_LIVE_ACK boundary — service/secret agreement point`

Normative source role: `sole authority`

Local surface list: `prohibited`

The secret contract incorporates, whole and without qualification, the complete content
under that exact unique service heading through the next same-level heading. The service
section's prohibited forms, allowed identifier-only forms, enforcement layers, effective
systemd defense, terminal rules, egress accounting, and falsification matrix are the sole
semantic boundary. Its present source is
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:391-457`.

No secret-side sentence, list, example, scanner scope, code fence, later section, or
verification rule may narrow, replace, override, independently restate, or create an
exception to the incorporated section. A fenced example is non-normative and cannot grant
permission. Any conflicting local wording makes the secret document non-conforming; it
does not alter the service authority. PASS requires the incorporated service evaluation to
PASS in its complete universe. A forbidden form is FAIL. An unreadable source, missing or
ambiguous authority, unavailable evaluation, inaccessible surface, incomplete enumeration,
or unadjudicated result is STOP/BLOCK, never absence and never PASS.
<!-- END V3 SECRET/SERVICE AGREEMENT -->

### 1.3 Independent two-document identity record

The checker consumes one independently frozen UTF-8 LF-terminated record named
`KVM2_PHASE2_V3_DOCUMENT_BINDING_V1.txt`. It is created by the candidate freezer, not by
either checked document or the agreement checker. It contains exactly these ten keys in
this order, once each, with no blank or additional line:

```text
record_schema=KVM2_PHASE2_V3_DOCUMENT_BINDING_V1
candidate_id=<1-128 characters from A-Z a-z 0-9 . _ : ->
service_relative_path=<relative path inside candidate root>
service_candidate_id=<exact candidate_id>
service_sha256=<64 lowercase hexadecimal characters>
secret_relative_path=<relative path inside candidate root>
secret_candidate_id=<exact candidate_id>
secret_sha256=<64 lowercase hexadecimal characters>
frozen_by=<independent freezer identity, not UNKNOWN/TBD/TODO>
frozen_at_utc=<RFC3339 UTC timestamp ending Z>
```

The two relative paths must resolve inside the same supplied candidate root; rooted paths,
empty segments, `.` and `..` segments are invalid. The service path must equal the normative
source file above. Both per-document candidate IDs must exist and equal the top-level
candidate ID. Each hash is calculated from the same bytes later decoded as strict UTF-8.
The auditor also supplies the binding record's 64-hex SHA-256 as
`ExpectedBindingSha256`, sourced from the independent freeze/dispatch ledger rather than
from this record or either document; the checker hashes the record bytes before parsing.
Absence, malformed grammar, mixed candidate IDs, path mismatch, hash mismatch, unreadable
bytes, or changed bytes is **STOP**, because the checker cannot establish which frozen
documents it is comparing. An author-written hash beside its own document is not a
substitute. This closes the identity assertion defect in the prior checker
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_V2_INDEPENDENT_VERDICTS_2026-08-16.md:28`).

### 1.4 Read-only whole-document agreement checker

The checker below reads only the binding record and the two bound document byte strings.
It hashes the bytes before decoding them, proves both paths and identities, resolves the
unique service authority, and then scans the **entire secret contract prose**, not merely
the deference section. Fenced blocks are removed only because this contract declares them
non-normative; an unterminated fence STOPs. The scan rejects a second agreement section,
any local policy list, any occurrence of the governed identifier outside the sole agreement
section, any local service-injection surface token, the discredited unqualified phrase, and
any permission/exception paragraph that combines an agreement subject with a prohibited
surface. Thus a later prose section permitting pass-through cannot escape the scan.

```powershell
param(
    [Parameter(Mandatory=$true)][string]$CandidateRoot,
    [Parameter(Mandatory=$true)][string]$BindingPath,
    [Parameter(Mandatory=$true)][string]$ExpectedBindingSha256,
    [Parameter(Mandatory=$true)][string]$ServicePath,
    [Parameter(Mandatory=$true)][string]$SecretPath
)

$ErrorActionPreference = 'Stop'
function Stop-Check([string]$Reason) { throw "STOP: $Reason" }
function Fail-Check([string]$Reason) { throw "FAIL: $Reason" }

$expectedKeys = @(
    'record_schema','candidate_id','service_relative_path','service_candidate_id',
    'service_sha256','secret_relative_path','secret_candidate_id','secret_sha256',
    'frozen_by','frozen_at_utc'
)

try {
    $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $bindingBytes = [System.IO.File]::ReadAllBytes($BindingPath)
    $bindingText = $strictUtf8.GetString($bindingBytes)
} catch { Stop-Check 'binding record absent, unreadable, or not strict UTF-8' }
if ($ExpectedBindingSha256 -cnotmatch '^[0-9a-f]{64}$') {
    Stop-Check 'independent binding-record hash is absent or malformed'
}
$actualBindingSha256 = [System.Convert]::ToHexString(
    [System.Security.Cryptography.SHA256]::HashData($bindingBytes)
).ToLowerInvariant()
if ($actualBindingSha256 -cne $ExpectedBindingSha256) {
    Stop-Check 'binding record hash mismatches the independent freeze ledger'
}
if (-not $bindingText.EndsWith("`n")) { Stop-Check 'binding record lacks final LF' }
$recordLines = $bindingText -split "\r?\n"
if ($recordLines[-1] -ne '') { Stop-Check 'binding record termination is ambiguous' }
$recordLines = @($recordLines[0..($recordLines.Count - 2)])
if ($recordLines.Count -ne $expectedKeys.Count) { Stop-Check 'binding record line count mismatch' }

$record = @{}
for ($i = 0; $i -lt $expectedKeys.Count; $i++) {
    $splitAt = $recordLines[$i].IndexOf('=')
    if ($splitAt -le 0) { Stop-Check 'binding record line has no key/value delimiter' }
    $key = $recordLines[$i].Substring(0, $splitAt)
    $value = $recordLines[$i].Substring($splitAt + 1)
    if ($key -cne $expectedKeys[$i] -or $record.ContainsKey($key) -or $value.Length -eq 0) {
        Stop-Check 'binding record key order, uniqueness, or value is invalid'
    }
    $record[$key] = $value
}
if ($record.record_schema -cne 'KVM2_PHASE2_V3_DOCUMENT_BINDING_V1') {
    Stop-Check 'binding schema mismatch'
}
if ($record.candidate_id -notmatch '^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$' -or
    $record.candidate_id -match '(?i)UNKNOWN|TBD|TODO|PLACEHOLDER') {
    Stop-Check 'candidate identity absent or placeholder'
}
if ($record.service_candidate_id -cne $record.candidate_id -or
    $record.secret_candidate_id -cne $record.candidate_id) {
    Stop-Check 'document candidate identities are mixed or absent'
}
if ($record.service_relative_path -ceq $record.secret_relative_path) {
    Stop-Check 'service and secret roles resolve to the same document path'
}
foreach ($hashKey in @('service_sha256','secret_sha256')) {
    if ($record[$hashKey] -cnotmatch '^[0-9a-f]{64}$') { Stop-Check "$hashKey is absent or malformed" }
}
if ($record.frozen_by -match '(?i)UNKNOWN|TBD|TODO|PLACEHOLDER' -or
    $record.frozen_at_utc -notmatch '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$') {
    Stop-Check 'independent freeze identity or UTC time is absent'
}

try { $root = [System.IO.Path]::GetFullPath($CandidateRoot) } catch { Stop-Check 'candidate root is invalid' }
function Resolve-BoundPath([string]$RelativePath) {
    $badSegments = @($RelativePath -split '/' | Where-Object { $_ -in @('', '.', '..') })
    if ([System.IO.Path]::IsPathRooted($RelativePath) -or $RelativePath -match '\\' -or
        $badSegments.Count -gt 0) {
        Stop-Check 'a bound relative path is non-canonical'
    }
    $resolved = [System.IO.Path]::GetFullPath((Join-Path $root ($RelativePath -replace '/', [System.IO.Path]::DirectorySeparatorChar)))
    $prefix = $root.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $resolved.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        Stop-Check 'a bound path escapes the candidate root'
    }
    return $resolved
}

$expectedServiceRel = 'MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md'
if ($record.service_relative_path -cne $expectedServiceRel) { Stop-Check 'normative service path mismatch' }
$boundService = Resolve-BoundPath $record.service_relative_path
$boundSecret = Resolve-BoundPath $record.secret_relative_path
if ([System.IO.Path]::GetFullPath($ServicePath) -cne $boundService -or
    [System.IO.Path]::GetFullPath($SecretPath) -cne $boundSecret) {
    Stop-Check 'supplied document path does not equal its bound path'
}

function Read-BoundDocument([string]$Path, [string]$ExpectedHash) {
    try { $bytes = [System.IO.File]::ReadAllBytes($Path) } catch { Stop-Check 'a bound document is unreadable' }
    $actualHash = [System.Convert]::ToHexString(
        [System.Security.Cryptography.SHA256]::HashData($bytes)
    ).ToLowerInvariant()
    if ($actualHash -cne $ExpectedHash) { Stop-Check 'a bound document hash mismatches' }
    try { $text = $strictUtf8.GetString($bytes) } catch { Stop-Check 'a bound document is not strict UTF-8' }
    return [pscustomobject]@{ Text = $text; Hash = $actualHash }
}
$service = Read-BoundDocument $boundService $record.service_sha256
$secret = Read-BoundDocument $boundSecret $record.secret_sha256

$serviceHeading = '### 4.2 Normative HL_LIVE_ACK boundary — service/secret agreement point'
$serviceHeadingCount = [regex]::Matches(
    $service.Text, '(?m)^' + [regex]::Escape($serviceHeading) + '\r?$'
).Count
if ($serviceHeadingCount -ne 1) { Stop-Check 'service authority heading is missing or ambiguous' }
$serviceSection = [regex]::Match(
    $service.Text, '(?ms)^' + [regex]::Escape($serviceHeading) + '\r?$.*?(?=^### |\z)'
).Value
if ([string]::IsNullOrWhiteSpace($serviceSection)) { Stop-Check 'service authority extraction is incomplete' }

function Remove-FencedBlocks([string]$Text) {
    $inside = $false
    $kept = [System.Collections.Generic.List[string]]::new()
    foreach ($line in ($Text -split "\r?\n")) {
        if ($line -match '^\s*```') { $inside = -not $inside; continue }
        if (-not $inside) { $kept.Add($line) }
    }
    if ($inside) { Stop-Check 'secret document has an unterminated fence' }
    return ($kept -join "`n")
}
$wholeProse = Remove-FencedBlocks $secret.Text
$secretContractHeading = '## 1. Secret contract'
$secretContractHeadingCount = [regex]::Matches(
    $wholeProse, '(?m)^' + [regex]::Escape($secretContractHeading) + '\r?$'
).Count
if ($secretContractHeadingCount -ne 1) {
    Fail-Check 'the complete secret-contract heading is missing or ambiguous'
}
$secretContract = [regex]::Match(
    $wholeProse,
    '(?ms)^' + [regex]::Escape($secretContractHeading) + '\r?$.*?(?=^## |\z)'
).Value
if ([string]::IsNullOrWhiteSpace($secretContract)) {
    Fail-Check 'the complete secret contract could not be extracted'
}
$begin = '<!-- BEGIN V3 SECRET/SERVICE AGREEMENT -->'
$end = '<!-- END V3 SECRET/SERVICE AGREEMENT -->'
if (([regex]::Matches($secretContract, [regex]::Escape($begin))).Count -ne 1 -or
    ([regex]::Matches($secretContract, [regex]::Escape($end))).Count -ne 1) {
    Fail-Check 'the sole agreement markers are missing or duplicated'
}
$beginAt = $secretContract.IndexOf($begin, [System.StringComparison]::Ordinal)
$endAt = $secretContract.IndexOf($end, [System.StringComparison]::Ordinal)
if ($endAt -le $beginAt) { Fail-Check 'agreement marker order is invalid' }
$agreementEnd = $endAt + $end.Length
$agreement = $secretContract.Substring($beginAt, $agreementEnd - $beginAt)
$outsideAgreement = $secretContract.Substring(0, $beginAt) + "`n" + $secretContract.Substring($agreementEnd)

$requiredRecords = @(
    'Normative source file: `' + $expectedServiceRel + '`',
    'Normative source heading: `' + $serviceHeading + '`',
    'Normative source role: `sole authority`',
    'Local surface list: `prohibited`'
)
foreach ($required in $requiredRecords) {
    if (([regex]::Matches($secretContract, [regex]::Escape($required))).Count -ne 1 -or
        -not $agreement.Contains($required)) {
        Fail-Check 'a required sole-authority record is missing, duplicated, or outside the agreement'
    }
}
$normalizedAgreement = [regex]::Replace($agreement, '\s+', ' ')
foreach ($phrase in @(
    'incorporates, whole and without qualification',
    'may narrow, replace, override, independently restate, or create an exception',
    'PASS requires the incorporated service evaluation to PASS',
    'is STOP/BLOCK, never absence and never PASS'
)) {
    if (-not $normalizedAgreement.Contains($phrase)) {
        Fail-Check 'a required incorporation, precedence, or outcome rule is missing'
    }
}
if ([regex]::IsMatch($secretContract, '(?m)^\s*(?:[-*+]|\d+\.)\s+')) {
    Fail-Check 'a local secret-side surface list exists'
}
if ($outsideAgreement.Contains('HL_LIVE_ACK') -or
    [regex]::IsMatch($secretContract, '(?i)present\s+in\s+any\s+form')) {
    Fail-Check 'local governed-identifier policy exists outside the sole agreement'
}
if ([regex]::IsMatch(
    $secretContract,
    '(?i)PassEnvironment|UnsetEnvironment|EnvironmentFile|ExecStart(?:Pre|Post)?|SetCredential|LoadCredential|ImportCredential'
)) { Fail-Check 'a local service-injection surface rule exists outside the sole agreement' }
$subject = '(?i)policy\s+(?:name|identifier)|acknowledg(?:e)?ment|service\s+(?:boundary|section)|incorporated\s+section'
$permission = '(?i)allow(?:ed|s)?|permit(?:ted|s)?|may\s+(?:appear|enter|pass|be)|exception|exempt|override|narrow|replace|restate|pass[- ]?through'
$surface = '(?i)manager\s+environment|process\s+environment|argv|stdout|stderr|journal|diagnostic|crash|core|screenshot|backup|export(?:ed)?\s+evidence|credential\s+injection'
foreach ($paragraph in ($secretContract -split "(?:\r?\n){2,}")) {
    if ($paragraph -match $subject -and $paragraph -match $permission -and $paragraph -match $surface) {
        Fail-Check 'a local narrowing, override, or surface exception exists outside the sole agreement'
    }
}

'PASS: both document identities bind one candidate; unique service authority; entire secret prose has no local narrowing or override'
```

**One-line falsification:** bind service candidate A to secret candidate B or change one
bound byte and the real checker must STOP; add a later prose sentence permitting
service-manager pass-through and it must FAIL; the unchanged bound pair must PASS. Until all three
arms are executed against the real checker, its result is UNVERIFIED.

### 1.5 Secret verification and violation signature

The deferred-owner gate, independently enumerated names-only source universe, structural
parsers, value-free evidence, egress terminal accounting, and synthetic non-secret fixtures
from V2 remain required. Missing owner lift, inaccessible source, unknown include, count
mismatch, or incomplete scanner execution STOPs. Provisioning, inspecting, or recording a
secret value is outside this contract
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:58-91`). **One-line falsification:** inject one synthetic active definition and it must FAIL, make one enumerated member unreadable and it must STOP, while an identifier-only comment remains GREEN.

## 2. State contract

### 2.1 Frozen schema and the sole state input record

D5 selects a fresh database with no inherited daily-loss counter, consecutive-loss
counter, order history, or foreign-position record, while preserving or blocking on the
source evidence. Raw empty exchange positions and orders remain separate before/after
single-writer observations; SQLite cannot establish them
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-116`;
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:16-26`).

For this candidate contract the exact destination schema is SQLite schema version **4**.
That value is not guessed: version 4 is the runtime's default target, higher versions are
explicit opt-ins, the application calls `initialize()` without an override, and a fresh
initialization writes `meta.schema_version = '4'`
(`IBKR_PAPER_BRIDGE/bridge/store/db.py:263-299,523-546,604-635`;
`IBKR_PAPER_BRIDGE/bridge/app.py:104-110`). A destination whose runtime selects another
schema version is not adjudicated by these predicates: it STOPs and requires a revised,
independently reviewed predicate set. No owner record may silently substitute a different
version.

All variable prerequisite values live in one exact record named
`KVM2_STATE_V3_INPUT_RECORD_V1`. It must be independently frozen before the reset producer
runs and contain: record ID; candidate ID; candidate release SHA-256; destination relative
DB path; reset-producer artifact SHA-256 and literal argv; read-only-verifier artifact
SHA-256 and literal argv; normalized `sqlite_master` catalog SHA-256 for the accepted v4
schema; final source-capture record ID, DB SHA-256, invariant SHA-256, and successful
retrieval result; the owner's archive branch (`OFF_HOST_ARCHIVE` or
`RETAINED_OLD_HOST_STATE`) and location record ID; pre-stop and post-revocation raw-exchange
capture record IDs and hashes; and independent freezer identity/time. Every field is
required, duplicate/additional fields are rejected, and `UNKNOWN`, `TBD`, `TODO`, null,
empty, or a placeholder is invalid. The record is not supplied by the reviewed sources, so
the present operational result is **STOP/BLOCKED**. This is a named STOP input, not an
invented value.

### 2.2 Read-only verifier binding and schema gate

The verifier opens the stopped, independently hashed destination bytes through SQLite
read-only mode and sets `PRAGMA query_only=ON`; it never calls application initialization
and never writes or repairs the database. It captures rc/output/diagnostics for every
statement before interpretation. PASS requires all of the following:

1. `PRAGMA integrity_check` returns exactly one row, exactly `ok`;
2. `PRAGMA foreign_key_check` returns zero rows;
3. `SELECT key,value FROM meta ORDER BY key` returns exactly one row,
   `('schema_version','4')`;
4. the normalized `sqlite_master` catalog hash equals the independent catalog hash in
   `KVM2_STATE_V3_INPUT_RECORD_V1`, and the exact table set is
   `meta`, `runs`, `bars`, `decisions`, `orders`, `fills`, `trades`, `equity`,
   `risk_days`, `directives`, `llm_calls`, `events`, `signal_fingerprints`,
   `order_identity`, `submission_attempts`, and `submission_recovery_evidence`; and
5. every table except `meta` has zero rows. The verifier issues one literal
   `SELECT COUNT(*) FROM <quoted-table>` for every name in that frozen list and enforces
   `sum(all fifteen counts) = 0`; it does not accept an omitted table, a view alias, or a
   producer-supplied total.

The required v4 risk/history columns and ledgers are defined by the runtime schema
(`IBKR_PAPER_BRIDGE/bridge/store/db.py:653-833,853-898`). Catalog mismatch, missing/extra
table, missing column, query failure, busy/changed bytes, sidecar ambiguity, hash drift, or
an incomplete count vector is STOP. A completed nonzero count is FAIL.

**One-line falsification:** add a row to an otherwise unqueried v4 business table and the
complete census must FAIL; remove a table or deny a read and it must STOP; an untouched
fresh v4 artifact must remain GREEN.

### 2.3 Four exact semantic predicates

The following SQL is literal and bound to the read-only verifier. All statements must
complete against the same byte identity after the schema gate. No risk-day input is needed:
D5 requires *no inherited rows for any day*, so adding a date filter would create an
omission path.

| Risk class | Literal query | Exact clean result | Independent expectation and STOP rule | One-line falsification |
|---|---|---|---|---|
| Daily loss | `SELECT (SELECT COUNT(*) FROM risk_days) AS risk_day_rows, (SELECT COUNT(*) FROM equity) AS equity_rows, (SELECT COUNT(*) FROM trades WHERE exit_ts IS NOT NULL OR pnl IS NOT NULL) AS realized_trade_rows;` | exactly `(0,0,0)` | D5 supplies “no inherited daily-loss counter”; schema/catalog identity comes from §2.1. Any absent table/column, query error, or incomplete tuple STOPs. | Insert only an `equity.realized_today` row or a `risk_days` row; the exact query must FAIL. |
| Consecutive loss | `SELECT (SELECT COUNT(*) FROM risk_days WHERE consecutive_losses_end IS NOT NULL) AS persisted_streak_rows, (SELECT COUNT(*) FROM trades WHERE exit_ts IS NOT NULL AND pnl IS NOT NULL) AS closed_trade_rows;` | exactly `(0,0)` | The actual runtime derives the streak from closed trades and also persists an end-of-day streak (`IBKR_PAPER_BRIDGE/bridge/store/db.py:4588-4625,6431-6459`). Query inability STOPs. | Insert one closed losing trade while leaving `risk_days` empty; the second count must make the check FAIL. |
| Order history | `SELECT (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM fills), (SELECT COUNT(*) FROM trades), (SELECT COUNT(*) FROM decisions), (SELECT COUNT(*) FROM order_identity), (SELECT COUNT(*) FROM submission_attempts), (SELECT COUNT(*) FROM submission_recovery_evidence);` | exactly seven zeros | D5 supplies “no order history”; the v4 schema fixes every order/submission ledger. Missing ledger, duplicate/short tuple, or query error STOPs. | Insert an `order_identity` or recovery-evidence row while `orders` stays empty; the seven-way query must FAIL. |
| Foreign-position record | `SELECT COUNT(*) FROM events WHERE code = 'FOREIGN_POSITION_IGNORED';` plus the two bound raw-exchange records | DB result exactly `0`; each raw record independently says complete positions query `0` and complete orders query `0` | The runtime records an unowned position with that exact event code (`IBKR_PAPER_BRIDGE/bridge/engine/orders.py:1018-1027`). Raw exchange capture IDs/hashes come only from `KVM2_STATE_V3_INPUT_RECORD_V1`. Either raw record absent, stale, incomplete, identity-mismatched, or unable to query STOPs; SQLite zero alone can never PASS this class. | Insert only that event and the DB arm must FAIL; remove either raw capture and the combined arm must STOP. |

No alternative “clean” path exists. The four class results, complete business-table census,
source retrieval, archive choice, reset identity, raw-exchange records, integrity, foreign
keys, catalog identity, and unchanged single-writer evidence all must terminate GREEN.
Missing input cannot be treated as a zero. A producer-authored digest cannot replace any
query. Source capture precedes reset and remains retrievable under the owner-selected
branch; failure or semantic mismatch blocks reset/start
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:183-211,327-332`).

## 3. Recovery contract

### 3.1 Retained mechanisms and named owner inputs

Recovery continues to consume state's accepted capture and semantic verifier; it does not
re-adjudicate the reset. Rollback identities are frozen before rollback and every selected
release, effective unit, writer-absence, state-preservation, secret-store, and exposure
postcondition is observed independently. A rollback manifest remains supplemental. Restore
is isolated and uses the same four-class semantic verifier
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:158-188`). **One-line falsifications:** alter restored semantics while retaining packaging metadata and restore must FAIL (unreadable capture STOPs); run a no-op rollback with a truthful-looking manifest and independently observed postconditions must FAIL (observer loss STOPs).

Later backups remain encrypted, off-host, versioned, retention-locked, restorable in
isolation, and free of secret values. The routine write role cannot delete a version or
weaken retention; the recovery role is separately held. Access recovery records roles and
procedures without private identifiers or values and may not depend on one powered-on
device or one untested path
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:28-43`;
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:166-178`).

Provider, object namespace, retention duration, routine-role identity, recovery-role
identity, recovery objectives, and native provider response codes are not established by
the sources. They must appear together in one independently frozen owner record named
`KVM2_RECOVERY_POLICY_AND_CANARY_INPUT_V1`. Required fields are: candidate ID; provider and
API version; account/project and repository/bucket logical IDs; routine and recovery
principal logical IDs; RPO/RTO and retention duration; canary object key and immutable
version ID; canary creation evidence ID; current retain-until UTC; exact syntactically valid
shorter retain-until UTC used by the probe; literal provider request shapes for
`HEAD_EXACT_VERSION`, `DELETE_EXACT_VERSION`, `SHORTEN_RETENTION_EXACT_VERSION`, and
`RESTORE_EXACT_VERSION`; and exhaustive native outcome tuples mapped to
`AUTHORITY_DENIED`, `TARGET_NOT_FOUND`, `REQUEST_INVALID`, `AUTHENTICATION_FAILED`,
`SUCCESS`, or `UNKNOWN`. The independently frozen record hash and freezer identity/time are
also required. Missing/unfilled/ambiguous fields STOP. No placeholder or locally guessed
provider code is admitted.

### 3.2 Known-valid retained-version canary and exact denial grammar

The canary content is the non-secret UTF-8 byte string
`KVM2-RETENTION-CANARY-V1` followed by LF, whose SHA-256 is
`12d1f2a8a08baa975166af71e49008f968aedc7c7fd872a9a88d2ba136c70a4e`.
It is a dedicated non-production object version and contains no release, state, credential,
account, or private value. Its provider-assigned immutable version ID and current retention
time come only from the owner record.

The independent recovery role first performs `HEAD_EXACT_VERSION`. GREEN preflight requires
an authenticated recovery-principal identity, exact immutable version ID, exact content
hash/length, and retention through at least the recorded current retain-until time. Not
found, latest-version substitution, delete-marker resolution, identity ambiguity, clock
ambiguity, or incomplete metadata is STOP; the routine-role denial is not attempted.

The routine role then performs exactly two non-economic probes against that same immutable
version: `DELETE_EXACT_VERSION` and `SHORTEN_RETENTION_EXACT_VERSION`. Each raw provider
response is classified only by the exhaustive tuple table frozen in the owner record:

| Canonical class | Result |
|---|---|
| `AUTHORITY_DENIED` | GREEN only when the principal was authenticated as the exact routine role and the native status/code tuple exactly equals a pre-frozen authority-denial tuple for that operation. |
| `SUCCESS` or any observed deletion/shortening | FAIL. |
| `TARGET_NOT_FOUND` | STOP; it does not prove lack of authority. |
| `REQUEST_INVALID` | STOP; the request did not exercise authority. |
| `AUTHENTICATION_FAILED` | STOP; the intended routine principal was not tested. |
| `UNKNOWN`, unlisted tuple, timeout, parse error, transport gap, or incomplete response | STOP. |

After both authority denials, the independent recovery role repeats
`HEAD_EXACT_VERSION`. PASS requires the same immutable ID, hash, length, and retention time.
A changed or missing canary is FAIL; inability to observe is STOP. The separate recovery
role's isolated restore of this exact canary must also GREEN before the provider/role
contract is accepted. No value is printed or persisted by the denial checker.

**One-line falsification:** point the routine probe at a nonexistent version while using a
delete-capable principal; `TARGET_NOT_FOUND` must STOP, whereas making deletion succeed on
the known-valid canary must FAIL and an authenticated `AUTHORITY_DENIED` on the unchanged
canary must GREEN.

### 3.3 Remaining recovery outcomes

Wrong release, missing risk evidence, byte-equal but semantically deviant state, no-op
rollback, false manifest booleans, incomplete observation, secret-bearing backup/evidence,
single-device recovery dependency, or a routine principal that can delete/weaken retention
is FAIL/BLOCK. A not-yet-supplied owner record or an unevaluable restore/rollback is STOP,
never PASS. Backup, restore, rollback, role provisioning, provider contact, and access
recovery remain outside this T2 artifact.

## 4. Teardown contract

### 4.1 Complete independent discovery grammar

The teardown universe is the union of the admission ledger and all collectors below. The
category set comes from the teardown source, which requires services, identities, packages,
repositories, schedulers/timers, units, outputs/files, credential names, network rules,
namespaces, container artifacts, browser profiles, caches, and monitoring extensions
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/TEARDOWN_AND_REPROVISION.md:3-9`).
The target platform is the declared Ubuntu 24.04.x Server profile
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/temporary-testnet-lab.md:7-18`).

Collectors are read-only and independent of the teardown/uninstaller. Each emits zero or
more `KVM2_TD_MEMBER_V3` JSONL rows and exactly one terminal `KVM2_TD_SUMMARY_V3` row. A
member row has `phase` (`PRE` or `POST`), category, collector ID/version/hash, backend,
stable ID, restricted attributes hash, and source identity. It never contains file content,
secret value, environment value, or private credential. The summary has collector ID,
source count, member count, duplicate count, unresolved count, rc, completion flag, and
start/end monotonic times. PASS requires rc 0, `complete=true`, zero duplicates/unresolved,
and `source_count = sources_terminally_accounted`. Missing summary, nonzero rc, stderr that
signals loss, timeout, truncation, parse error, unreadable source, unstable identity,
unknown backend, or count mismatch is STOP. An observed prohibited survivor is FAIL.

### 4.2 Frozen collector matrix

| Category and collector | Exact independent sources and stable identity | Completeness / STOP rule | One-line falsification |
|---|---|---|---|
| Service — `TD3-SERVICE-SYSTEMD` | systemd manager `ListUnits`, `ListUnitFiles`, and properties for every `.service`, reconciled with every readable `/proc/<pid>/cgroup`; identity `systemd-service:<escaped unit name>`. | Manager and full `/proc` censuses must both complete and every service/process membership gets one row; unknown init, manager error, PID-race gap, or unreconciled service STOPs. | Add an unregistered loaded service: it must be discovered and FAIL; deny manager access: STOP. |
| Identity — `TD3-IDENTITY-NSS` | parse `/etc/nsswitch.conf` passwd/group backends, enumerate full libc NSS passwd and group databases, numeric UID/GID and supplementary memberships; identities `uid:<decimal>` and `gid:<decimal>`. | Every configured NSS backend must terminate; duplicate numeric IDs, name/number drift, backend error, or incomplete membership STOPs. No shadow/hash/value is read. | Add a UID absent from admission: discover and FAIL; break one NSS backend: STOP. |
| Package — `TD3-PACKAGE-UBUNTU` | complete `dpkg-query` status census; if detected by package/unit/socket/executable preflight, complete Snap and Flatpak system/per-user censuses; every `pyvenv.cfg` found by `TD3-FILESYSTEM-WALK` is enumerated through that venv's pinned interpreter metadata. Identity is manager + canonical package + architecture + version or venv path + canonical distribution + version. | dpkg is mandatory. Every detected manager must have an adapter and complete; RPM/Nix/Homebrew or another unmodelled manager, unreadable database, duplicate canonical name, or venv metadata error STOPs. | Install one package only in a venv and it must FAIL; hide that venv from the file walk and conservation must STOP. |
| Repository — `TD3-REPOSITORY-ALL` | all APT `.list`/`.sources` records, Snap channels, package-manager repositories detected above, and every VCS control directory found by the full filesystem walk; stable ID is backend + canonical source/repository identity or mount/device/inode/path. | Every package backend and every VCS marker must be parsed; unsupported source grammar, unreadable file, duplicate identity, or discovered repository without a terminal row STOPs. | Add a `.git` directory outside the admission ledger: discover and FAIL; make its parent unreadable: STOP. |
| Scheduler — `TD3-SCHEDULER-ALL` | systemd manager/unit-file timer census plus `/etc/crontab`, `/etc/cron.d`, `/etc/cron.{hourly,daily,weekly,monthly}`, `/var/spool/cron`, `/var/spool/anacron`, and `/var/spool/at`; user sources are derived from the complete UID census. Stable ID is backend + unit name or device/inode/path + entry ordinal/hash. | Every path is classified present/absent by `lstat`; every present source is completely read by a privileged names/metadata-only parser. at/cron/systemd backend or syntax uncertainty STOPs. | Add one cron file omitted by the ledger: FAIL; truncate or deny one spool: STOP. |
| Unit — `TD3-UNIT-SYSTEMD` | systemd `ListUnits`, `ListUnitFiles`, fragment/source/drop-in paths and all generator output for every unit type; identity `systemd-unit:<escaped name>:<type>`. | Loaded and on-disk unit sets must reconcile, and the service subset must equal `TD3-SERVICE-SYSTEMD`; manager/generator/query gap or orphan source STOPs. | Add a disabled path unit or drop-in: discover and FAIL; suppress generator output: STOP. |
| Files/output — `TD3-FILESYSTEM-WALK` | `findmnt` mount census followed by descriptor-relative, no-symlink `lstat` traversal of every mounted filesystem except kernel API pseudo-filesystems `proc`, `sysfs`, `devtmpfs`, `devpts`, `cgroup2`, `securityfs`, `pstore`, `tracefs`, `debugfs`, `configfs`, `fusectl`, `mqueue`, `hugetlbfs`, and `autofs`; those excluded domains are owned by dedicated collectors. Identity is mount ID + device + inode + encoded path + type. | Mount census is frozen before/after the walk; any mount drift, loop, unreadable directory, path race, unhandled filesystem, duplicate inode/path representation, or unexplained count change STOPs. tmpfs and `/run` are not silently excluded. | Place an unregistered output under a separate tmpfs: discover and FAIL; unmount during the walk: STOP. |
| Network rule/listener — `TD3-NETWORK-ALLNS` | namespace set from `TD3-NAMESPACE-PROC`; inside every network namespace collect complete netlink link/address/route/rule/neighbor state, nftables JSON ruleset, legacy ip/ip6tables saves when detected, and listener/socket census. Provider firewall/export source is the separately frozen `KVM2_TD_PROVIDER_NETWORK_INPUT_V1`. Stable ID is namespace inode + backend + native rule/socket identity. | Every namespace and detected firewall backend must complete. Missing provider record (including an explicit independently evidenced `NO_PROVIDER_SURFACE` decision), inaccessible namespace, nft/legacy ambiguity, or socket query loss STOPs. | Add an unregistered nft rule in a non-default namespace: FAIL; omit the provider record: STOP. |
| Namespace — `TD3-NAMESPACE-PROC` | two complete `/proc/<pid>/ns/*` device/inode censuses around `lsns` plus named `ip netns` handles and systemd namespace-join properties; identity is namespace type + kernel inode. | The future teardown observation runs quiesced. PID churn, unreadable proc entry, disagreement between sources, unnamed inode without disposition, or incomplete second census STOPs. | Create an extra network namespace: FAIL; cause process churn between censuses: STOP. |
| Container — `TD3-CONTAINER-BACKENDS` | backend detection is the union of package, service, unit, socket, process, and executable censuses. Adapters enumerate all containers including stopped, images, volumes, networks, pods, machines, and build cache for Docker, Podman, containerd/nerdctl, LXC, Incus, and systemd-nspawn. Identity is backend + native immutable object ID. | Every detected backend must be queryable and all object classes terminally accounted. Unknown runtime/socket/process, permission denial, API-version gap, or reduced object class STOPs; zero is GREEN only after all absence probes complete. | Leave one stopped volume: FAIL; expose an unknown runtime socket: STOP. |
| Browser/profile — `TD3-BROWSER-PROFILES` | browser/automation candidates derive from package, executable, process, and full filesystem censuses. Adapters enumerate Firefox, Chromium, Chrome, Edge, Brave, Playwright, Selenium, and WebDriver profile/cache roots for every NSS home; identity is product + UID + device/inode/path. | Every detected product needs an adapter and every profile root a terminal row. Unknown browser package/signature, unreadable home, or filesystem/package disagreement STOPs. | Add a second profile under another UID: FAIL; install an unmodelled browser: STOP. |
| Cache — `TD3-CACHE-ROOTS` | full members of every NSS home's `.cache`, `/root/.cache`, `/var/cache`, `/tmp`, `/var/tmp`, container/build caches, browser caches, venv/package caches, and every cache root named by an admission record; identity is owner UID + device/inode/path. | Each declared/detected cache-producing product must map to a root or explicit `NO_CACHE`; unknown producer, unreadable root, mount drift, volatile-entry churn, or unmatched root STOPs. | Leave one lab-owned file in `/var/tmp`: FAIL; make a cache subtree unreadable: STOP. |
| Monitoring extension — `TD3-MONITORING-JOIN` | join the complete package, service, unit, process, scheduler, container, browser-extension, kernel-module, and `/sys/fs/bpf` censuses against the independently frozen `KVM2_MONITORING_PRODUCT_UNIVERSE_V1`; identity is source collector + native stable ID. | The universe record must name every admitted monitoring product and adapter. Any unclassified candidate, unavailable source collector, unknown eBPF/module owner, or missing universe record STOPs. | Add a monitoring timer under an unregistered product name: STOP as unclassified, never clean. |
| Credential name — `TD3-CREDENTIAL-NAMES` | exactly the store/consumer collectors in §6.2 plus the names-only inventory; identity is canonical credential name, never its value. | Every source must complete and every name must have one disposition. Any inaccessible store/consumer, dynamic name, unknown backend, value-bearing output, omission, or count mismatch STOPs. | Add one consumer-only environment name: discover and FAIL/BLOCK; make its grammar dynamic: STOP. |

### 4.3 Conservation, post-state, and clean allowlist

For each phase and category the verifier enforces
`ledger members ∪ independently discovered members = removed + explicitly retained by sanitized export allowlist + rejected from export + unresolved`.
Stable IDs cannot be overwritten or renormalized between stages; each input member reaches
exactly one terminal disposition. Discovered-unregistered members are retained as such and
block; they never disappear from the universe.

Post-reprovision collectors are the same bound collector hashes and grammars. Their result
is compared with `KVM2_TD_CLEAN_PROFILE_ALLOWLIST_V1`, independently frozen before
teardown. That record is not present in the sources, so current teardown proof STOPs. An
allowlist missing a category, collector, expected member, or explicit expected-empty set is
invalid and STOPs. An unexpected survivor/addition is FAIL. This preserves the never-restore
rule for lab image/home/workspace/cache/package/container/browser/scheduler/log/backup
state and the sanitized export boundary
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/TEARDOWN_AND_REPROVISION.md:11-27`).

**Whole-matrix falsification:** inject one member in every category outside the admission
ledger; its category collector must discover it and FAIL/BLOCK. Disable any one collector
or backend adapter; the category and whole teardown result must STOP, never silently pass.

## 5. Maintenance contract

### 5.1 The one owner-input record

Automatic updates remain disabled unless and until one owner-authored, independently
frozen record named `KVM2_MAINTENANCE_POLICY_V1.json` exists. It is the sole source for all
previously open policy values and contains exactly these required fields:

| Field | Required closed content |
|---|---|
| `record_schema`, `record_id`, `candidate_id`, `frozen_at_utc`, `owner_decision_cite` | Exact identities; no null, placeholder, `UNKNOWN`, `TBD`, or `TODO`. |
| `os_release` | Exact `ID`, `VERSION_ID`, image/provenance record ID, and accepted package-backend set. |
| `automatic_updates` | Explicit boolean. `false` is a complete policy, not a missing value. |
| `allowed_origins` | Exhaustive sorted array of exact backend, URI, suite/channel, component, and signing-key fingerprint. Empty requires explicit `automatic_updates=false`. |
| `allowed_packages` | Exhaustive sorted array of exact package name, architecture, current version, allowed target version/range, origin ID, and disposition. Empty requires explicit `automatic_updates=false`. |
| `command_argv` | Ordered array of literal argv arrays with pinned absolute executable path/hash, cleared environment, fixed cwd, timeout, and expected exit grammar. Shell strings, globs, substitutions, and undeclared arguments are invalid. |
| `blackout_policy` | IANA timezone, explicit intervals/recurrence, boundary inclusivity, DST fold/gap rule, and action `DEFER` or `BLOCK`. An explicit empty interval set means no blackout. |
| `reboot_policy` | Exactly `FORBIDDEN` or `SEPARATELY_AUTHORIZED_ONCE`; the latter includes the required owner sentence record and exact allowed window. |
| `restart_policy` | Exactly `FORBIDDEN` or `SEPARATELY_AUTHORIZED_DISARMED_ONCE`; the latter lists exact unit, reason, owner sentence record, preconditions, and allowed window. No wildcard units. |
| `executor_role`, `exception_adjudicator` | Distinct named roles. The executor cannot adjudicate its own drift. |
| `pre_post_collector_binding` | Exact hashes/versions for package, origin, effective unit/drop-in, config, release, venv, listener, identity, storage, log, reboot, and process-invocation collectors. |
| `recovery_and_rollback_binding` | Accepted pre-window recovery artifact identity/hash, rollback procedure identity/hash, and exact rollback trigger grammar. |

The JSON is strict UTF-8, duplicate-key rejecting, exact-schema validating, and rejects
additional fields. The independent dispatch record binds its SHA-256 before the window.
Absence, unreadability, invalidity, unfilled content, hash mismatch, or a detected package
backend not named by `os_release` is STOP. There is no other owner-selectable maintenance
value outside this one record. The source requirement for exact scope and restart behavior
is retained, not weakened
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/MAINTENANCE.md:3-21`).

### 5.2 Executable decision table once the record exists

| Check | PASS / FAIL / STOP | Independent expectation | One-line falsification |
|---|---|---|---|
| `MNT3-01` record and candidate binding | PASS only for exact schema/hash/candidate and every closed field. Content mismatch is FAIL only after identity binds; inability to bind is STOP. | Owner record frozen before the window. | Delete `restart_policy`: STOP; change a bound value after freeze: STOP on hash mismatch. |
| `MNT3-02` proposed origin/package set | PASS only when every proposed origin and package transition exactly matches one array member and every member has a disposition. Extra/mismatched member FAILs; incomplete census STOPs. | `allowed_origins` and `allowed_packages`. | Add one undeclared package: FAIL. |
| `MNT3-03` command | PASS only for exact argv sequence, executable hashes, clean environment, cwd, timeout, and status grammar. Deviation FAILs; instrument/hash/status uncertainty STOPs. | `command_argv`, independent executable binding. | Add one harmless-looking option: FAIL. |
| `MNT3-04` blackout | Convert one independently observed UTC instant with the named timezone/DST rule; inside blackout follows exact `DEFER`/`BLOCK`, outside may proceed. Clock/timezone ambiguity STOPs. | `blackout_policy`, independent monotonic/UTC collector. | Move the fixture instant one second across an inclusive boundary and require opposite adjudication. |
| `MNT3-05` reboot | Any reboot is FAIL under `FORBIDDEN`; under the one-shot branch only the exact separately authorized window/identity may PASS. Missing boot-ID evidence STOPs. | `reboot_policy`, pre/post kernel boot ID and event source. | Change boot ID under `FORBIDDEN`: FAIL. |
| `MNT3-06` service restart | Any new invocation is FAIL under `FORBIDDEN`; the one-shot branch requires exact unit, DISARMED/single-writer preconditions, owner record, window, and exactly one invocation. Watcher gap STOPs. | `restart_policy`, independent systemd event/invocation observer. | Start the unit twice or restart another unit: FAIL. |
| `MNT3-07` pre/post conservation | Every collector completes and every delta maps to a preregistered disposition; unexplained drift FAILs, collection/count gap STOPs, executor explanation cannot alter the result. | `pre_post_collector_binding`, independent adjudicator. | Add a drop-in while package hashes stay equal: FAIL. |
| `MNT3-08` recovery/reconcile | Accepted recovery artifact precedes change; post-change state/reconcile proof completes; any bound rollback trigger invokes the recorded block/rollback outcome. Semantic drift FAILs; missing evidence STOPs. | `recovery_and_rollback_binding` and State §2. | Supply a producer hash with missing semantic evidence: STOP, not clean. |

Once the single owner record exists and binds, this table leaves no policy choice to an
executor. Package/unit/config drift, reboot, restart, reconcile gap, evidence gap,
provider-panel action, or changed profile identity retains the reset/reclassification rule
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/MAINTENANCE.md:23-28`). No update,
reboot, restart, rollback, or drill is authorized by this artifact.

## 6. Incident contract

### 6.1 Retained classification and response rules

Classification remains two independently expected booleans: resource/SLO impact and
security-boundary impact. Neither, either, or both may be true; security impact invokes the
conservative contamination branch even when resource impact is also true. A scenario author
freezes inputs and both expected booleans before the responder runs. Automation remains
alert-only and cannot restart, DISARM, ARM, reconcile, deploy, contain, revoke, rotate, or
modify bridge state. Evidence is sanitized and off-host heartbeat observation is mandatory
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/INCIDENT_RESPONSE.md:3-36`;
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:303-342`).

**One-line falsification:** freeze a dual-impact scenario and make the responder classify it
resource-only; the real comparator must FAIL, while missing scenario expectation or
heartbeat observation must STOP.

### 6.2 Exact independent credential store/consumer discovery

The base expectation source is the names-only inventory, presently six named entries; it
also states that monitoring/backup names are not established until a later provider record
exists (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/SECRET_INVENTORY.md:6-18`).
The incident universe is not that list alone. It is the set union of that inventory and
every name emitted by **all** store and consumer collectors below:

| Collector | Exact source and names-only grammar | STOP rule | One-line falsification |
|---|---|---|---|
| `IC3-STORE-ENV` | structurally parse active assignments in every environment source reached from the complete systemd unit/drop-in/transient census and every file under the independently admitted environment-source roots; emit canonical variable names only. | Unknown include, dynamic assignment name, unreadable source, duplicate representation, parser gap, or emitted value STOPs. | Add a name only in a secondary environment file: it must enter the universe. |
| `IC3-STORE-SYSTEMD-CREDENTIAL` | parse effective `LoadCredential`, `LoadCredentialEncrypted`, `SetCredential`, `SetCredentialEncrypted`, and `ImportCredential` name mappings for every unit; enumerate basenames only under `/etc/credstore`, `/etc/credstore.encrypted`, and every `/run/credentials/<unit>` directory discovered by the full filesystem/unit census. | Manager query failure, unknown directive grammar, inaccessible directory, path race, or value/content output STOPs. | Add a credential only through a drop-in: discover it; hide the drop-in: STOP. |
| `IC3-STORE-SCHEDULED` | structurally parse credential-name references from every complete systemd timer/service, cron, anacron, and at source in `TD3-SCHEDULER-ALL`; emit names and consumer stable IDs only. | Opaque command, computed name, unreadable schedule, or scheduler coverage gap STOPs. | Add a cron-only consumer name: it must enter the universe. |
| `IC3-STORE-LOCAL-BACKEND` | backend preflight joins packages, services, sockets, executables, NSS homes, and filesystem signatures for `pass`, Secret Service/keyring, cloud CLI stores, SSH agents, backup agents, and monitoring agents; a frozen adapter enumerates logical item names only from each detected backend. | Detected backend without an exact names-only adapter, locked/unreadable backend, or possible value-bearing output STOPs. Absence requires all probes to complete. | Install an unmodelled keyring backend: STOP, never empty-PASS. |
| `IC3-STORE-CONTAINER` | for every container backend detected by `TD3-CONTAINER-BACKENDS`, enumerate secret/config object names, mount/source names, and injected environment names across running and stopped objects. | Backend/API/object-class gap, permission denial, dynamic injection, or incomplete stopped-object census STOPs. | Add a secret to a stopped container: it must enter the universe. |
| `IC3-STORE-PROVIDER` | consume the separately owner-frozen `KVM2_INCIDENT_PROVIDER_CREDENTIAL_INPUT_V1` required for monitoring, backup, and alerting; reconcile its exact provider/issuer/store names with local provider consumers. | A selected/detected provider without that record and complete names export STOPs. An explicit `NO_PROVIDER_SELECTED` disposition in the record is required for an expected-empty provider set. | Detect a backup-agent consumer with no provider record: STOP. |
| `IC3-CONSUMER-CODE` | parse the bound candidate with an AST/token adapter for literal environment lookups, settings fields, credential-loader calls, and config schema names; each hit emits canonical name + source symbol. | Dynamic/computed key, unsupported language/grammar, generated code without source map, unreadable file, or incomplete candidate census STOPs. | Replace a literal lookup with string concatenation: STOP as dynamic, not absence. |
| `IC3-CONSUMER-EFFECTIVE-UNIT` | consume the complete effective systemd environment/credential/pass-through name set for every service from the manager API, including manager-to-unit inheritance, without persisting values. | Manager/namespace query error, incomplete property, inaccessible service, or any value-bearing evidence STOPs. | Inject a manager-only name into one unit: it must enter the universe. |
| `IC3-CONSUMER-RUNTIME` | for each admitted bridge/monitor/backup process, bind PID/invocation/cgroup and parse the NUL-delimited `/proc/<pid>/environ` in memory, emitting keys only; reconcile argv/config name references from the process/artifact binder. | PID race, permission denial, malformed record, process identity drift, missing process, or emitted value STOPs. | Add a runtime-only synthetic name: discover it; recycle the PID mid-read: STOP. |
| `IC3-CONSUMER-CONFIG` | parse every config, unit, scheduler, backup, monitoring, notifier, and recovery artifact found by the complete file/unit/package collectors with its registered grammar; emit only credential-name fields and consumer stable IDs. | Unknown file grammar, unregistered config producer, unreadable artifact, parser loss, or incomplete file universe STOPs. | Add a notifier config with a consumer-only name: it must enter the universe. |

Every collector uses the common rc/output/diagnostic/completion-first grammar. Each canonical
name receives exactly one terminal disposition: `NOT_PROVISIONED_INDEPENDENTLY_PROVED`,
`PROVISIONED_AND_REVOKE`, `PROVISIONED_NO_REVOKE_WITH_OWNER_CITE`, or `UNRESOLVED_STOP`.
`inventory ∪ store names ∪ consumer names = the terminal-disposition set`, with no duplicate
collapse, local filtering, or missing member. Any collector STOP, unknown name grammar,
consumer/store mismatch, count mismatch, or value-bearing evidence STOPs the whole incident
credential result. An observed undisposed name is FAIL/BLOCK. This supplies the exact
independent sources absent from V2
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_V2_INDEPENDENT_VERDICTS_2026-08-16.md:20`).

**Whole-universe falsification:** inject one synthetic name only into each store and each
consumer source in turn; the real union must discover it and block until disposition. Make
one source unreadable; the result must STOP rather than report a smaller clean universe.

### 6.3 Known-valid observer capability canary and errno grammar

The local canary is a regular file at the exact non-runtime path
`/var/lib/mtc-contract-canaries/observer-denial-v1`, containing the non-secret UTF-8 byte
string `KVM2-OBSERVER-CAPABILITY-CANARY-V1` followed by LF, SHA-256
`2a1f0123258c63dc2508efca313ec4dfc71ec0c9860c5e9d95b78c96bea7f3ae`.
It is root-owned numeric `0:0`, mode `0600`; its parent is root-owned numeric `0:0`, mode
`0700`. It is never a bridge state, release, credential, order, or provider object.

A separately authorized prerequisite provisions it and freezes
`KVM2_INCIDENT_OBSERVER_CANARY_INPUT_V1`: candidate ID, observer numeric UID/GID, exact
path, parent and leaf device/inode/type/owner/mode/size/hash, pinned errno-helper absolute
path/SHA-256, independent pre/post collector identity, and freeze time. The current sources
do not supply that record or numeric observer identity, so the present capability result is
STOP. No identity is guessed.

The privileged independent preflight first `lstat`s the parent and leaf and hashes the leaf;
all fields must equal the frozen record. The observer then invokes the pinned helper under
its independently verified numeric identity. The helper calls exactly
`open(path, O_WRONLY|O_APPEND|O_CLOEXEC|O_NOFOLLOW)` and, if open succeeds, immediately
closes without writing. It emits one of these actual syscall classes:

| Observed class | Result |
|---|---|
| exact `EACCES` or `EPERM`, with bound observer identity and existing preflight canary | GREEN authority denial. |
| open succeeds | FAIL; the observer has write capability. |
| `ENOENT`, `ENOTDIR`, `ESTALE`, or missing preflight identity | STOP; target validity was not exercised. |
| `ELOOP` | STOP; the bound regular-file target was not reached. |
| `EROFS` | STOP; filesystem state, not observer authority, denied the open. |
| any other errno, raw exit, timeout, helper/hash mismatch, parse error, or incomplete observation | STOP. |

The privileged postflight repeats every parent/leaf observation and hash. Missing or changed
state is FAIL; inability is STOP. The check never writes a byte and never treats a prose
diagnostic such as “permission denied” as errno evidence, applying the project's grammar
rule (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:303-364`).

**One-line falsification:** use a mutation-capable observer against a nonexistent path;
`ENOENT` must STOP, then make the known-valid canary writable and an opened descriptor must
FAIL, while exact `EACCES`/`EPERM` on the unchanged valid canary must GREEN.

### 6.4 Incident violation signature

A dual incident reduced to resource-only, responder-authored expectation, automation with a
mutating capability, reduced credential universe, undisposed name, missing off-host
heartbeat, absent/invalid canary, target-not-found reported as authority denial, incomplete
observation reported as clean, or secret-bearing evidence/export blocks the incident
contract. Threshold/provider/retry values not established by sources remain fields of the
named `KVM2_INCIDENT_SCENARIO_AND_TIMING_INPUT_V1` and STOP while absent; V3 does not invent
them. No response, containment, termination, provider contact, revocation, rotation,
recovery, or bridge-state action is authorized here.

## 7. Boundary and present status

This document performed no host, network, SSH, deployment, service, credential,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading,
merge-to-master, Git mutation, product-code, or economic action. It contains no secret value
and authorizes none of those actions. It is not acceptance.

The named binding/owner/canary/allowlist records and all operational RED/GREEN transcripts
are absent from the supplied sources unless explicitly stated otherwise. Their absence is
the named STOP condition, not a reason to manufacture a value or claim failure. V3 is a
closed contract design that becomes evaluable only when those independently sourced inputs
exist and bind; its present operational verdict is **BLOCKED / UNVERIFIED / NOT ACCEPTED**.

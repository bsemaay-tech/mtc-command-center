# Secret contract v3 — `HL_LIVE_ACK` section only

Status: **T2 contract text / preparation only / no action / no acceptance / no authorization**.

Replacement scope: this text replaces only the `HL_LIVE_ACK` boundary, verification, and violation wording in the secret contract. The current secret-side wording claims equivalence while defining a shorter boundary (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_STATE_RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_V2_2026-08-15.md:43-56,63-84`). Nothing else in that contract is rewritten here.

## Structure chosen and why

This v3 chooses **normative cross-reference**, not reproduction. The service contract already declares its `HL_LIVE_ACK` section to be the agreement point and requires the secret contract either to reproduce or normatively cross-reference the exact surface list (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:391-457`). A second copy would create two editable universes and recreate the drift found by the v2 cross-check (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_V2_CROSSCHECK_2026-08-16.md:40-67`). One live normative source also answers the recurring completeness question—what is outside the universe—without allowing the secret-side producer to select a shorter set (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`).

## Normative `HL_LIVE_ACK` deference

Normative source file: `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md`

Normative source heading: `### 4.2 Normative HL_LIVE_ACK boundary — service/secret agreement point`

Normative source role: `sole authority`

Local surface list: `prohibited`

The secret contract incorporates by reference the complete current content under that exact heading, ending immediately before the next same-level heading. The incorporation is whole and without qualification: it adopts the service section's prohibited forms, permitted identifier-only mentions, semantic distinction, enforcement layers, effective-systemd defense, PASS/FAIL/STOP rules, egress-universe accounting, and falsification matrix. The present source location is `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:391-457`; the line range is a citation, while the file path plus exact unique heading identifies the live normative referent.

For avoidance of doubt, the incorporation includes the mandatory effective `UnsetEnvironment=HL_LIVE_ACK` defense defined at `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:425-435`. This is a non-exhaustive control highlight, not a secret-side surface list. The complete prohibited-surface universe remains only in the service source at `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:402-415`; its allowed identifier-only forms and forbidden value-bearing forms remain only at `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:417-423`; and its complete mutation/STOP matrix remains only at `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:441-447`.

No secret-side sentence, list, example, scanner scope, or verification rule may narrow, replace, override, or independently restate that incorporated section. If any local secret-side wording appears to conflict with it, the service section controls and the secret contract is non-conforming until the local conflict is removed. A future editor changes the surface universe in one place only—the service section. If the source file or heading is renamed or moved, the editor must update this pointer and rerun the agreement check below; ordinary line movement requires no secret-side edit.

## Secret-side verification and outcome

A secret-side `HL_LIVE_ACK` result must consume the same service-defined evaluation and complete service-defined universe; it may not evaluate a locally declared subset. PASS requires the incorporated service evaluation to PASS, including its mandatory effective defense and complete terminal accounting. An observed forbidden form or defeated required defense is FAIL. An unreadable source, ambiguous or missing normative target, unavailable evaluation, inaccessible surface, incomplete enumeration, or unadjudicated result is STOP/BLOCK, never absence and never PASS. The evaluation must not read or emit a value, as required by the service authority (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:425-447,459-472`).

The expected boundary comes from the service contract named above, not from this secret section, an installer, a scanner result, or the observed candidate. The cross-document rule is therefore enforced by deference to one authority rather than asserted by two prose claims. Whether an integrated repository already has an executable shared evaluator and recorded RED/GREEN evidence is **UNKNOWN**; the source explicitly describes corrected design contracts rather than executed evidence (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:505-517`). Until that evaluator and evidence exist, the operational result remains BLOCKED / UNVERIFIED.

## Auditor agreement check — run this last

The auditor uses the service and secret documents from the same frozen candidate. The check is structural and read-only: resolve the exact service file and unique heading above; extract that section through the next same-level heading; confirm the secret section names it as the sole authority; confirm local surface-list reproduction is prohibited; and confirm no secret-side rule narrows or overrides the incorporation. The expected source comes from the service contract's own agreement requirement, not from secret-side scanner output (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md:449-457`).

The auditor runs this read-only PowerShell check after setting the two paths to the candidate documents:

```powershell
$servicePath = '<candidate service-contract path>'
$secretPath = '<candidate secret-contract path>'
$serviceRel = 'MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md'
$serviceHeading = '### 4.2 Normative HL_LIVE_ACK boundary — service/secret agreement point'
$secretHeading = '## Normative `HL_LIVE_ACK` deference'

try {
    $serviceText = Get-Content -LiteralPath $servicePath -Raw -Encoding UTF8 -ErrorAction Stop
    $secretText = Get-Content -LiteralPath $secretPath -Raw -Encoding UTF8 -ErrorAction Stop
} catch {
    throw 'STOP: an input document could not be read'
}

$serviceHeadingCount = [regex]::Matches(
    $serviceText,
    '(?m)^' + [regex]::Escape($serviceHeading) + '\r?$'
).Count
$secretHeadingCount = [regex]::Matches(
    $secretText,
    '(?m)^' + [regex]::Escape($secretHeading) + '\r?$'
).Count
if ($serviceHeadingCount -ne 1 -or $secretHeadingCount -ne 1) {
    throw 'STOP: a normative section heading is missing or ambiguous'
}

$serviceSection = [regex]::Match(
    $serviceText,
    '(?ms)^' + [regex]::Escape($serviceHeading) + '\r?$.*?(?=^### |\z)'
).Value
$secretSection = [regex]::Match(
    $secretText,
    '(?ms)^' + [regex]::Escape($secretHeading) + '\r?$.*?(?=^## |\z)'
).Value
if ([string]::IsNullOrWhiteSpace($serviceSection) -or [string]::IsNullOrWhiteSpace($secretSection)) {
    throw 'STOP: a normative section could not be extracted completely'
}

$requiredSecretRecords = @(
    'Normative source file: `' + $serviceRel + '`',
    'Normative source heading: `' + $serviceHeading + '`',
    'Normative source role: `sole authority`',
    'Local surface list: `prohibited`'
)
foreach ($record in $requiredSecretRecords) {
    if (-not $secretSection.Contains($record)) {
        throw 'FAIL: the secret section does not defer to the sole normative service section'
    }
}
if ([regex]::IsMatch($secretSection, '(?m)^\s*(?:[-*+]|\d+\.)\s+')) {
    throw 'FAIL: an independent secret-side surface list exists'
}
if (-not $secretSection.Contains('without qualification') -or
    -not $secretSection.Contains('may narrow, replace, override, or independently restate')) {
    throw 'FAIL: the incorporation or precedence rule is missing'
}

'PASS: one service-side authority; exact secret-side deference; no independent secret-side list'
```

The displayed path strings are document-location inputs, not secret or credential placeholders. The auditor substitutes only filesystem locations and never supplies or reads a secret value.

The check **FAILs** if the secret pointer names a different file or heading, the sole-authority or no-local-list record is removed, a secret-side surface list is added, or local wording can narrow or override the incorporated service section. It **STOPs/BLOCKs** if either candidate document is unreadable, the candidate identities are not frozen together, a target heading is missing or duplicated, or either section cannot be extracted completely. A service-side list change under the same unique heading does not fail the agreement check: the secret contract incorporates that live section automatically. Review of whether the changed service boundary is itself correct is a separate service-contract audit, not evidence that the two documents disagree. To falsify this agreement check, an auditor makes a disposable copy, changes the secret pointer or adds a local list, and must observe FAIL; deleting or duplicating the target heading must produce STOP/BLOCK. No PASS counts until those RED arms and the unchanged GREEN arm are run against the real check, consistent with `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:73-83`.

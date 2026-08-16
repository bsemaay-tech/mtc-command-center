Status: ARCHIVE PROCEDURE DRAFT — FOR LEAD REVIEW — implements owner decision §5 of 2026-08-16 — NOT EXECUTED

# Pre-cutover archive procedure

This is a procedure for the owner to run later on the retiring Windows PC. It does not authorize or perform a capture, copy, encryption, restore, cutover, reset, start, or deletion. The owner approved drafting and review only; the actual machine work remains a later owner action (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:10-12`; `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:53-60`).

Scope classification: **T2 — documentation/evidence**. This file is a draft for Lead review, not an acceptance.

## Before using this draft: unresolved inputs

Do not start the procedure until every `UNKNOWN` below has an owner-approved answer.

- **UNKNOWN — source database path.** What is the exact path of the retiring PC's old `bridge.db`?
- **UNKNOWN — repository/tool path on the retiring PC.** What exact local repository path contains the accepted `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`?
- **UNKNOWN — raw-capture file list and format.** What are the exact filenames for the T4 and T8 positions, orders, and pre/post-revocation responses, and what exact field proves that positions and orders are empty?
- **UNKNOWN — raw-capture sanitization check.** Who or what confirms that every raw capture contains no secret before it is copied into the archive?
- **UNKNOWN — cutover-record path.** What is the exact owner-held, out-of-band cutover record that will receive the hashes and restore result?
- **UNKNOWN — final storage target.** Which one of the `OWNER-CHOICE` targets in section 5 is selected, and what is its exact device, machine path, or object identifier?
- **UNKNOWN — restore-test machine.** Which Windows machine, other than the retiring PC, will perform the restore test?
- **UNKNOWN — BitLocker availability.** Does the retiring PC and the restore-test PC expose BitLocker management (`manage-bde.exe` and the BitLocker PowerShell module)? If not, use the one fallback in section 3.

The tabletop also says that a hot WAL without its `-shm` file can make a read-only capture impossible. That is a deliberate STOP requiring separate authority, not a reason to improvise (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:408-410`; `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:215-236`).

## 1. What goes in the bundle

There are two different things called a bundle here. Keep them distinct:

- The **risk-state bundle** is the output of `wal_state_bundle.py`.
- The **transport package** is one ZIP containing the risk-state bundle, the raw cutover captures, and the procedure's hash evidence. The ZIP is then placed inside one encrypted container.

The transport package contains exactly these evidence groups:

1. **Risk-state bundle directory.** It contains the self-contained `bridge.db` and `bundle_manifest.json` produced by the WAL-consistent online-backup tool. The database carries the full history; the manifest carries sanitized counts, aggregates, timestamps, invariants, and hashes. The tabletop defines this evidence at `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:263-285` and `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:301-321`; the tool fixes the two output names at `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:77-86`. Do **not** copy the source `bridge.db`, `bridge.db-wal`, and `bridge.db-shm` trio into the package; the tool deliberately replaces that unsafe copy with one consistent database (`IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:5-25`).

2. **Create report.** Save the tool's JSON stdout as `wal_create_report.json`. It supplies the authoritative `bundle_db_sha256` and `invariants_sha256` values that must also be recorded outside the archive. The tabletop defines that requirement at `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:316-321`; the tool emits the values at `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:747-755` and `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:1083-1116`.

3. **T4 first raw captures.** Include the timestamped raw empty positions capture and raw empty orders capture taken before the old writer is stopped or its authority is revoked. Their definition is at `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:133-133` and `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:322-327`. **UNKNOWN:** the tabletop does not define their filenames, file format, or whether one or several files hold each response. Owner question: what exact T4 files form the complete capture?

4. **T8 second raw captures.** Include the second timestamped raw empty positions and orders captures taken VPS-side after revocation, together with the sanitized pre/post-revocation responses. Their definition is at `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:137-137` and `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:322-327`. **UNKNOWN:** the tabletop does not define their filenames, file format, or exact file count. Owner question: what exact T8 files form the complete capture?

5. **Local verification report.** Save the first successful `verify` JSON stdout as `wal_local_verify_report.json`. The archive must verify with the two externally recorded hashes and return exit code 0 with verdict `VALID` (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:328-333`). This report is supporting evidence; it does not replace the restore test on another machine.

6. **File hash inventory.** Add `FILE_SHA256.txt`, generated by section 2. It lists the SHA-256 of every evidence file above. It does not replace the two authoritative tool hashes.

The authoritative cutover record is **not** allowed to exist only inside this package. It must remain owner-held and out-of-band because `verify` refuses to trust hashes supplied only by the archive it is checking (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:316-321`). A convenience copy may be added only after the Lead decides that point; the tabletop leaves it undefined.

## 2. Hashing and packaging

### 2.1 Prepare named locations

Use one elevated Windows PowerShell window for the later authorized run. Replace every `REPLACE_...` value first; the guard deliberately stops if a placeholder remains.

This command records the paths used by all later commands and stops if the owner has not filled them in.

```powershell
$Repo = "C:\REPLACE_WITH_ACCEPTED_REPOSITORY"
$SourceDb = "C:\REPLACE_WITH_OLD_BRIDGE_DB\bridge.db"
$ArchiveId = "REPLACE_WITH_UTC_ID_LIKE_pre_cutover_20260816T120000Z"
$StagingParent = "C:\REPLACE_WITH_LOCAL_STAGING_PARENT"
$HoldingDir = "C:\REPLACE_WITH_LOCAL_CONTAINER_HOLDING_DIR"
$CutoverRecord = "C:\REPLACE_WITH_OWNER_HELD_CUTOVER_RECORD.md"

if (($Repo + $SourceDb + $ArchiveId + $StagingParent + $HoldingDir + $CutoverRecord) -match "REPLACE_") {
    throw "STOP: replace every REPLACE_ value before continuing."
}

$ArchiveRoot = Join-Path $StagingParent $ArchiveId
$RiskBundle = Join-Path $ArchiveRoot "risk_state_bundle"
$T4Dir = Join-Path $ArchiveRoot "raw_cutover_captures\T4_before_stop"
$T8Dir = Join-Path $ArchiveRoot "raw_cutover_captures\T8_after_revocation"
$CreateReportPath = Join-Path $ArchiveRoot "wal_create_report.json"
$LocalVerifyReportPath = Join-Path $ArchiveRoot "wal_local_verify_report.json"
$InventoryPath = Join-Path $ArchiveRoot "FILE_SHA256.txt"

New-Item -ItemType Directory -Path $RiskBundle,$T4Dir,$T8Dir,$HoldingDir -ErrorAction Stop | Out-Null
```

The source must already be quiesced, with the accepted single-writer and flat evidence complete. The capture command must not contain `--allow-live-source` or `--force`; those would violate the cutover capture contract (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:307-315`; `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:1062-1074`).

### 2.2 Create the risk-state bundle and preserve its hashes

This command creates the risk-state bundle and saves the tool's sanitized JSON report.

```powershell
Set-Location -LiteralPath $Repo
& python ".\IBKR_PAPER_BRIDGE\tools\wal_state_bundle.py" create --source $SourceDb --out-dir $RiskBundle |
    Tee-Object -FilePath $CreateReportPath
$CreateExit = $LASTEXITCODE
if ($CreateExit -ne 0) { throw "STOP: capture failed with exit code $CreateExit; do not reset or continue." }

$CreateReport = Get-Content -LiteralPath $CreateReportPath -Raw | ConvertFrom-Json
if ($CreateReport.verdict -ne "CAPTURED" -or $CreateReport.exit_code -ne 0) {
    throw "STOP: the create report is not CAPTURED/0."
}
$BundleDbSha256 = $CreateReport.bundle_db_sha256.ToLowerInvariant()
$InvariantsSha256 = $CreateReport.invariants_sha256.ToLowerInvariant()
if ($BundleDbSha256 -notmatch '^[0-9a-f]{64}$' -or $InvariantsSha256 -notmatch '^[0-9a-f]{64}$') {
    throw "STOP: an authoritative hash is missing or malformed."
}
```

Immediately copy those two values into the out-of-band cutover record using section 6; do not wait until the encrypted package exists. The tool also records source DB/WAL/SHM provenance hashes in `bundle_manifest.json`, while the produced bundle DB hash is authoritative (`IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:14-25`; `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:688-716`). The invariants hash is the SHA-256 of canonical JSON for the sanitized invariant object, not a hash of the manifest file (`IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:405-406`).

### 2.3 Add the already-authorized raw captures

Do not use this archive procedure to contact an exchange or create the raw captures. This step only copies the exact files produced by the separately authorized T4/T8 cutover steps. Fill the two lists only after the `UNKNOWN` file-list question has been answered.

This command copies the owner-approved T4 and T8 files into separate folders and stops if a listed file is missing.

```powershell
$T4Sources = @(
    "C:\REPLACE_WITH_T4_POSITIONS_CAPTURE",
    "C:\REPLACE_WITH_T4_ORDERS_CAPTURE"
)
$T8Sources = @(
    "C:\REPLACE_WITH_T8_POSITIONS_CAPTURE",
    "C:\REPLACE_WITH_T8_ORDERS_CAPTURE",
    "C:\REPLACE_WITH_ANY_ADDITIONAL_PRE_POST_RESPONSE"
)

if (($T4Sources + $T8Sources) -match "REPLACE_") {
    throw "STOP: the authoritative raw-capture file list is still UNKNOWN."
}
foreach ($Path in $T4Sources) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "STOP: missing T4 file: $Path" }
    Copy-Item -LiteralPath $Path -Destination $T4Dir -ErrorAction Stop
}
foreach ($Path in $T8Sources) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "STOP: missing T8 file: $Path" }
    Copy-Item -LiteralPath $Path -Destination $T8Dir -ErrorAction Stop
}
```

Before continuing, the owner must confirm that the T4/T8 evidence is timestamped, readable, sanitized, and shows empty positions and empty orders. The bundle manifest's `live_orders` value must also be 0. A disagreement is a STOP, not something to average away (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:322-327`; `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:423-423`). The exact raw-file emptiness test remains `UNKNOWN` until the owner answers the format question above.

### 2.4 Verify locally before packaging

This command re-derives the bundle invariants, compares both external expected hashes, and saves the local verification report.

```powershell
Set-Location -LiteralPath $Repo
& python ".\IBKR_PAPER_BRIDGE\tools\wal_state_bundle.py" verify --bundle-dir $RiskBundle `
    --expect-bundle-sha256 $BundleDbSha256 `
    --expect-invariants-sha256 $InvariantsSha256 |
    Tee-Object -FilePath $LocalVerifyReportPath
$VerifyExit = $LASTEXITCODE
if ($VerifyExit -ne 0) { throw "STOP: local verification failed with exit code $VerifyExit." }

$VerifyReport = Get-Content -LiteralPath $LocalVerifyReportPath -Raw | ConvertFrom-Json
if ($VerifyReport.verdict -ne "VALID" -or $VerifyReport.exit_code -ne 0) {
    throw "STOP: local verification is not VALID/0."
}

$Manifest = Get-Content -LiteralPath (Join-Path $RiskBundle "bundle_manifest.json") -Raw | ConvertFrom-Json
if ([int]$Manifest.invariants.live_orders -ne 0) {
    throw "STOP: bundle live_orders is not zero."
}
```

### 2.5 Hash every evidence file and the complete transport package

The per-file inventory hashes `bridge.db`, `bundle_manifest.json`, both JSON reports, and every T4/T8 file. It intentionally cannot include its own hash; its hash is recorded separately in the cutover record.

This command writes a sorted SHA-256 inventory using paths relative to the archive root, then hashes the inventory itself.

```powershell
$Base = (Resolve-Path -LiteralPath $ArchiveRoot).Path.TrimEnd('\') + '\'
$InventoryLines = Get-ChildItem -LiteralPath $ArchiveRoot -File -Recurse |
    Where-Object { $_.FullName -ne $InventoryPath } |
    Sort-Object FullName |
    ForEach-Object {
        $Relative = $_.FullName.Substring($Base.Length)
        $Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$Hash  $Relative"
    }
$InventoryLines | Set-Content -LiteralPath $InventoryPath -Encoding ascii
$FileInventorySha256 = (Get-FileHash -LiteralPath $InventoryPath -Algorithm SHA256).Hash.ToLowerInvariant()
```

The outer ZIP is the complete unencrypted transport package. Its SHA-256 covers the risk-state bundle, raw captures, reports, and file inventory as one object.

This command creates the transport ZIP with Windows' built-in `tar.exe`, then records its SHA-256.

```powershell
$TransportZip = Join-Path $HoldingDir ($ArchiveId + ".zip")
$ArchiveParent = Split-Path -Parent $ArchiveRoot
$ArchiveLeaf = Split-Path -Leaf $ArchiveRoot
& "$env:SystemRoot\System32\tar.exe" -a -c -f $TransportZip -C $ArchiveParent $ArchiveLeaf
if ($LASTEXITCODE -ne 0) { throw "STOP: transport ZIP creation failed." }
$TransportZipSha256 = (Get-FileHash -LiteralPath $TransportZip -Algorithm SHA256).Hash.ToLowerInvariant()
```

Record `FileInventorySha256` and `TransportZipSha256` outside the archive using section 6. Do not delete the staging folder or plain ZIP under this draft; any later cleanup belongs to a separately reviewed teardown step.

## 3. Encryption

### Primary: a BitLocker-encrypted VHDX container

Use a **BitLocker-encrypted VHDX** created with stock Windows `diskpart.exe` and encrypted with stock Windows `manage-bde.exe`. This is preferred because it requires no third-party archiver, can be stored as one file on an external disk, another machine, or object storage, supports a password plus a separate recovery key, and can be restore-tested on another BitLocker-capable Windows machine.

Prerequisites: run in elevated Windows PowerShell; confirm drive letter `R:` is unused; confirm both the retiring and restore-test PCs have BitLocker management. If those prerequisites are false, use only the fallback below.

This command calculates a container size larger than the ZIP, creates and mounts one NTFS VHDX as drive `R:`, and stops if `R:` is already in use.

```powershell
if (Get-PSDrive -Name R -ErrorAction SilentlyContinue) { throw "STOP: drive R: is already in use." }

$ZipSizeMiB = [math]::Ceiling((Get-Item -LiteralPath $TransportZip).Length / 1MB)
$VhdSizeMiB = [int][math]::Max(512, [math]::Ceiling(($ZipSizeMiB * 1.25) + 256))
$EncryptedContainer = Join-Path $HoldingDir ($ArchiveId + ".bitlocker.vhdx")
$DiskPartScript = Join-Path $env:TEMP ($ArchiveId + "_create_vhd.txt")

@"
create vdisk file="$EncryptedContainer" maximum=$VhdSizeMiB type=expandable
select vdisk file="$EncryptedContainer"
attach vdisk
create partition primary
format fs=ntfs quick label=PRE_CUTOVER
assign letter=R
"@ | Set-Content -LiteralPath $DiskPartScript -Encoding ascii

& "$env:SystemRoot\System32\diskpart.exe" /s $DiskPartScript
if ($LASTEXITCODE -ne 0) { throw "STOP: encrypted-container volume creation failed." }
```

This command turns on XTS-AES-256 BitLocker, prompts for a password, generates a 48-digit recovery password, and waits for encryption to finish.

```powershell
& "$env:SystemRoot\System32\manage-bde.exe" -on R: -Password -RecoveryPassword -UsedSpaceOnly -EncryptionMethod xts_aes256 -Synchronous
if ($LASTEXITCODE -ne 0) { throw "STOP: BitLocker encryption failed." }
& "$env:SystemRoot\System32\manage-bde.exe" -status R:
```

At the prompt, use a password-manager-generated password. Immediately save the password and displayed 48-digit recovery password according to **Key custody** below. Do not continue unless `manage-bde -status` says protection is on and encryption is complete.

This command copies only the transport ZIP into the encrypted volume and proves that the copied ZIP still has the expected package hash.

```powershell
$ZipInsideContainer = Join-Path "R:\" (Split-Path -Leaf $TransportZip)
Copy-Item -LiteralPath $TransportZip -Destination $ZipInsideContainer -ErrorAction Stop
$InsideZipSha256 = (Get-FileHash -LiteralPath $ZipInsideContainer -Algorithm SHA256).Hash.ToLowerInvariant()
if ($InsideZipSha256 -ne $TransportZipSha256) { throw "STOP: ZIP changed while copying into the encrypted container." }
```

This command locks and detaches the BitLocker container, then hashes the final encrypted VHDX for transport checking.

```powershell
& "$env:SystemRoot\System32\manage-bde.exe" -lock R: -ForceDismount
if ($LASTEXITCODE -ne 0) { throw "STOP: BitLocker container did not lock." }
Dismount-DiskImage -ImagePath $EncryptedContainer
$EncryptedContainerSha256 = (Get-FileHash -LiteralPath $EncryptedContainer -Algorithm SHA256).Hash.ToLowerInvariant()
Remove-Item -LiteralPath $DiskPartScript -ErrorAction SilentlyContinue
```

Do not mount the VHDX writable after its hash is recorded. Copy the locked `.bitlocker.vhdx`—not the plain ZIP—to the owner-chosen final storage target.

### Fallback: 7-Zip AES-256

If BitLocker management is unavailable on either machine, install the official 7-Zip package and use one AES-256 `.7z` file with encrypted filenames. This is the only fallback in this procedure. It is simpler and broadly portable, but it is not preferred because it adds third-party software and another version/install dependency.

This command prompts for the archive password instead of placing it on the command line, encrypts filenames and contents, and hashes the resulting encrypted file.

```powershell
$SevenZip = "C:\Program Files\7-Zip\7z.exe"
if (-not (Test-Path -LiteralPath $SevenZip -PathType Leaf)) { throw "STOP: approved 7-Zip is not installed." }
$Encrypted7z = Join-Path $HoldingDir ($ArchiveId + ".encrypted.7z")
& $SevenZip a -t7z -mx=9 -mhe=on -p $Encrypted7z $TransportZip
if ($LASTEXITCODE -ne 0) { throw "STOP: 7-Zip encryption failed." }
$EncryptedContainerSha256 = (Get-FileHash -LiteralPath $Encrypted7z -Algorithm SHA256).Hash.ToLowerInvariant()
```

### Key custody

The key must never be stored next to the encrypted archive, inside the archive, in its filename, or in the cutover record.

Owner options:

- **Password manager entry:** easiest regular recovery and searchable by archive ID, but depends on access to the password-manager account.
- **Printed copy in a separate physical location:** independent of accounts and devices, but can be lost, damaged, or read by someone with physical access.
- **Both:** one password-manager entry plus one sealed printed recovery copy at a separate location.

**Recommendation: both.** For BitLocker, store the archive password and 48-digit recovery password in one password-manager entry named with the archive ID; print the recovery password and store it at a separate physical location. For 7-Zip, store the generated archive password the same two ways. The cutover record stores only a custody note and entry label—never the secret itself.

## 4. Verification before trust

**Non-negotiable rule: the archive does not count as existing until a restore test has passed on a machine other than the retiring PC.** Local verification is useful but insufficient. The recovery contract requires off-host encryption, off-PC key recovery, and an isolated restore drill (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:36-43`).

### 4.1 BitLocker restore test on the second machine

Bring three things to the second machine by separate custody paths: the encrypted VHDX from final storage, the owner-held cutover record with expected hashes, and the password or recovery information. Do not copy the key beside the VHDX.

This command sets the restore-test values and deliberately stops if a placeholder remains.

```powershell
$RestoreRepo = "C:\REPLACE_WITH_ACCEPTED_REPOSITORY_ON_RESTORE_PC"
$FinalContainer = "C:\REPLACE_WITH_COPIED_OR_DOWNLOADED_BITLOCKER_VHDX"
$ArchiveId = "REPLACE_WITH_THE_ARCHIVE_ID"
$ExpectedContainerSha256 = "REPLACE_WITH_CUTOVER_RECORD_VALUE"
$ExpectedTransportZipSha256 = "REPLACE_WITH_CUTOVER_RECORD_VALUE"
$ExpectedInventorySha256 = "REPLACE_WITH_CUTOVER_RECORD_VALUE"
$ExpectedBundleDbSha256 = "REPLACE_WITH_CUTOVER_RECORD_VALUE"
$ExpectedInvariantsSha256 = "REPLACE_WITH_CUTOVER_RECORD_VALUE"
$RestoreRoot = "C:\REPLACE_WITH_EMPTY_RESTORE_TEST_DIRECTORY"

if (($RestoreRepo + $FinalContainer + $ArchiveId + $ExpectedContainerSha256 + $ExpectedTransportZipSha256 + $ExpectedInventorySha256 + $ExpectedBundleDbSha256 + $ExpectedInvariantsSha256 + $RestoreRoot) -match "REPLACE_") {
    throw "STOP: fill every restore-test value from the cutover record."
}
New-Item -ItemType Directory -Path $RestoreRoot -ErrorAction Stop | Out-Null
```

This command proves that the encrypted VHDX arrived byte-for-byte unchanged.

```powershell
$ActualContainerSha256 = (Get-FileHash -LiteralPath $FinalContainer -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualContainerSha256 -ne $ExpectedContainerSha256.ToLowerInvariant()) {
    throw "STOP: encrypted-container hash mismatch."
}
```

This command mounts the VHDX read-only, discovers the drive letter Windows assigned, prompts securely for the BitLocker password, and unlocks the volume.

```powershell
Mount-DiskImage -ImagePath $FinalContainer -Access ReadOnly
$MountedPartition = Get-DiskImage -ImagePath $FinalContainer | Get-Disk | Get-Partition |
    Where-Object { $_.DriveLetter } | Sort-Object Size -Descending | Select-Object -First 1
if (-not $MountedPartition) {
    throw "STOP: Windows did not assign a drive letter to the read-only VHDX."
}
$RestoreMountPoint = $MountedPartition.DriveLetter + ":"
$ArchivePassword = Read-Host "Enter the BitLocker archive password" -AsSecureString
Unlock-BitLocker -MountPoint $RestoreMountPoint -Password $ArchivePassword
Remove-Variable ArchivePassword
```

If the ordinary password is unavailable, the owner may use the separately held 48-digit recovery password through the Windows BitLocker recovery interface. Do not type that key into this document or save it in a script.

This command copies the ZIP out of the unlocked container and proves that its hash matches the out-of-band cutover record.

```powershell
$RestoredZip = Join-Path $RestoreRoot ($ArchiveId + ".zip")
Copy-Item -LiteralPath (Join-Path ($RestoreMountPoint + "\") ($ArchiveId + ".zip")) -Destination $RestoredZip -ErrorAction Stop
$ActualTransportZipSha256 = (Get-FileHash -LiteralPath $RestoredZip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualTransportZipSha256 -ne $ExpectedTransportZipSha256.ToLowerInvariant()) {
    throw "STOP: restored transport ZIP hash mismatch."
}
```

This command extracts the verified ZIP into the empty restore directory.

```powershell
& "$env:SystemRoot\System32\tar.exe" -x -f $RestoredZip -C $RestoreRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: restored ZIP could not be extracted." }
$RestoredArchiveRoot = Join-Path $RestoreRoot $ArchiveId
$RestoredInventory = Join-Path $RestoredArchiveRoot "FILE_SHA256.txt"
```

This command verifies the inventory file itself and then verifies every evidence file listed inside it.

```powershell
$ActualInventorySha256 = (Get-FileHash -LiteralPath $RestoredInventory -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualInventorySha256 -ne $ExpectedInventorySha256.ToLowerInvariant()) {
    throw "STOP: file-inventory hash mismatch."
}

$InventoryErrors = @()
foreach ($Line in Get-Content -LiteralPath $RestoredInventory) {
    if ($Line -notmatch '^([0-9a-f]{64})  (.+)$') {
        $InventoryErrors += "Malformed inventory line: $Line"
        continue
    }
    $Expected = $Matches[1]
    $Relative = $Matches[2]
    $ItemPath = Join-Path $RestoredArchiveRoot $Relative
    if (-not (Test-Path -LiteralPath $ItemPath -PathType Leaf)) {
        $InventoryErrors += "Missing: $Relative"
        continue
    }
    $Actual = (Get-FileHash -LiteralPath $ItemPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Actual -ne $Expected) { $InventoryErrors += "Hash mismatch: $Relative" }
}
if ($InventoryErrors.Count -ne 0) {
    $InventoryErrors
    throw "STOP: one or more restored evidence files failed verification."
}
```

This command runs the application-level bundle verifier against the two expected hashes held outside the archive.

```powershell
$RestoredRiskBundle = Join-Path $RestoredArchiveRoot "risk_state_bundle"
$RestoreVerifyReport = Join-Path $RestoreRoot "wal_restore_verify_report.json"
Set-Location -LiteralPath $RestoreRepo
& python ".\IBKR_PAPER_BRIDGE\tools\wal_state_bundle.py" verify --bundle-dir $RestoredRiskBundle `
    --expect-bundle-sha256 $ExpectedBundleDbSha256 `
    --expect-invariants-sha256 $ExpectedInvariantsSha256 |
    Tee-Object -FilePath $RestoreVerifyReport
$RestoreVerifyExit = $LASTEXITCODE
if ($RestoreVerifyExit -ne 0) { throw "STOP: restored risk-state bundle verification failed." }

$RestoreVerify = Get-Content -LiteralPath $RestoreVerifyReport -Raw | ConvertFrom-Json
if ($RestoreVerify.verdict -ne "VALID" -or $RestoreVerify.exit_code -ne 0) {
    throw "STOP: restored risk-state bundle is not VALID/0."
}
```

Finally, open every restored T4/T8 raw capture using the owner-approved reader and confirm that it is readable, timestamped, sanitized, and shows empty positions and empty orders; compare the empty-orders result with manifest `live_orders = 0`. The exact reader and field check are `UNKNOWN` until the owner answers the raw-format question, so the restore test cannot be marked PASS before that answer exists.

This command locks and detaches the read-only BitLocker VHDX after the test.

```powershell
Lock-BitLocker -MountPoint $RestoreMountPoint
Dismount-DiskImage -ImagePath $FinalContainer
```

### 4.2 Fallback restore test for 7-Zip

For the fallback, first compare the encrypted `.7z` hash with `ExpectedContainerSha256`, then use the separately held password to extract it. Continue with the same ZIP-hash, file-inventory, WAL verification, and raw-capture checks above.

This command prompts for the 7-Zip password and extracts the encrypted file without putting the password on the command line.

```powershell
$SevenZip = "C:\Program Files\7-Zip\7z.exe"
$Encrypted7z = "C:\REPLACE_WITH_COPIED_OR_DOWNLOADED_ENCRYPTED_7Z"
& $SevenZip x -p ("-o" + $RestoreRoot) $Encrypted7z
if ($LASTEXITCODE -ne 0) { throw "STOP: encrypted 7-Zip restore failed." }
```

### PASS definition

The restore test is PASS only when all of these are true on the non-retiring machine:

- the encrypted-container hash equals the cutover record;
- the decrypted transport ZIP hash equals the cutover record;
- the hash-inventory file hash equals the cutover record;
- every listed evidence file exists and its SHA-256 matches;
- `wal_state_bundle.py verify` exits 0 and reports `VALID` using the external `bundle_db_sha256` and `invariants_sha256`;
- all required T4/T8 files are readable, timestamped, sanitized, and show empty positions and orders;
- bundle `live_orders` is 0 and agrees with the raw empty-orders capture;
- the date, second-machine identity, and PASS result are added to the cutover record.

Any missing, unreadable, mismatching, ambiguous, or `UNKNOWN` result is STOP/FAIL. It is not PASS. Until PASS is recorded, say **“archive not yet established”**, not “archive exists.”

## 5. Storage target options — OWNER-CHOICE

- **OWNER-CHOICE — external disk:** simple, offline, and physically portable, but one disk is still one failure point and ordinary removable storage does not by itself provide versioning or retention lock.
- **OWNER-CHOICE — second machine:** quick to copy and restore-test, but it can share the same building, power, theft, ransomware, or administrator risk as the retiring PC.
- **OWNER-CHOICE — cloud object storage:** off-site and can provide versioning plus retention lock, but requires an account, network upload, recovery access, and a checked retention configuration.

The standing recovery contract calls for encrypted off-host, versioned/retention-locked storage with separately held recovery credentials (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:36-39`). The owner must record the chosen target and exact location; this draft does not choose or configure one.

## 6. Recording

The owner-held cutover record must gain the following exact field names. Replace angle-bracket values with real values; repeat the `PRE_CUTOVER_RAW_CAPTURE_SHA256` line once for every T4/T8 file. Never place a password or recovery key in this block.

This is the exact record block to add to the cutover record.

```text
PRE_CUTOVER_ARCHIVE_ID: <archive ID>
PRE_CUTOVER_CAPTURE_GENERATED_AT_UTC: <value from wal_create_report.json>
PRE_CUTOVER_SOURCE_DB_SHA256: <value from risk_state_bundle/bundle_manifest.json source.db_sha256>
PRE_CUTOVER_SOURCE_WAL_PRESENT: <true or false from bundle_manifest.json>
PRE_CUTOVER_SOURCE_WAL_SHA256: <64 lowercase hex, or NONE when absent>
PRE_CUTOVER_SOURCE_SHM_PRESENT: <true or false from bundle_manifest.json>
PRE_CUTOVER_SOURCE_SHM_SHA256: <64 lowercase hex, or NONE when absent>
PRE_CUTOVER_BUNDLE_DB_SHA256: <bundle_db_sha256 from wal_create_report.json>
PRE_CUTOVER_INVARIANTS_SHA256: <invariants_sha256 from wal_create_report.json>
PRE_CUTOVER_RAW_CAPTURE_SHA256: <relative T4/T8 filename> | <64 lowercase hex>
PRE_CUTOVER_FILE_INVENTORY_SHA256: <SHA-256 of FILE_SHA256.txt>
PRE_CUTOVER_TRANSPORT_ZIP_SHA256: <SHA-256 of the unencrypted transport ZIP>
PRE_CUTOVER_ENCRYPTED_CONTAINER_SHA256: <SHA-256 of the locked VHDX or encrypted 7z>
PRE_CUTOVER_ENCRYPTION_METHOD: <BITLOCKER_VHDX_XTS_AES_256 or 7ZIP_AES_256>
PRE_CUTOVER_KEY_CUSTODY: <password-manager entry label and/or sealed-print location; never the key; confirm not stored beside archive>
PRE_CUTOVER_STORAGE_LOCATION: <external device ID and path, second-machine path, or cloud bucket/object/version ID>
PRE_CUTOVER_RESTORE_TEST_DATE_UTC: <YYYY-MM-DDTHH:MM:SSZ>
PRE_CUTOVER_RESTORE_TEST_MACHINE: <machine identity; must not be the retiring PC>
PRE_CUTOVER_RESTORE_TEST_RESULT: <PASS, or STOP/FAIL with reason>
```

The two authoritative tool hashes and every raw-capture hash must be in this owner-held record. The tabletop requires the bundle DB and invariants hashes out-of-band (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:316-321`) and requires raw-capture hashes plus a timestamped ordered record (`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:322-341`).

After the record says PASS, this procedure has produced evidence for Lead review. It still grants no cutover, reset, first-start, ARM, deletion, or acceptance authority.

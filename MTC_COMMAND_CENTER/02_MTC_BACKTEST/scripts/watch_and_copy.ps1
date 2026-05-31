$ErrorActionPreference = "Stop"

$strategyPath = Resolve-Path "$PSScriptRoot/../00_MASTER_TEMPLATE/MASTER_TEMPLATE_v2_RC1.pine"
$folder = Split-Path $strategyPath
$filter = Split-Path $strategyPath -Leaf

if (-not (Test-Path $strategyPath)) {
    Write-Error "Strategy file not found at: $strategyPath"
    exit 1
}

Write-Host "WATCHING: $filter"
Write-Host "FOLDER:   $folder"
Write-Host "MODE:     Auto-Copy on Save"
Write-Host "---------------------------------------------------"
Write-Host "Keep this terminal open. Press Ctrl+C to stop."
Write-Host "---------------------------------------------------"

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $folder
$watcher.Filter = $filter
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

# Debounce handling to prevent double events
$global:lastEventTime = [DateTime]::MinValue

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $now = [DateTime]::Now
    
    # Simple debounce: ignore events within 500ms
    if (($now - $global:lastEventTime).TotalMilliseconds -lt 500) {
        return
    }
    $global:lastEventTime = $now

    Write-Host "[$($now.ToString('HH:mm:ss'))] * Detected change..." -NoNewline
    
    try {
        # Small delay to ensure file lock is released by editor
        Start-Sleep -Milliseconds 200
        
        Get-Content -Path $path -Raw | Set-Clipboard
        Write-Host " COPIED!" -ForegroundColor Green
        
        # Optional beep to notify user audibly
        [System.Console]::Beep(1000, 200)
    }
    catch {
        Write-Host " FAILED: $_" -ForegroundColor Red
    }
}

Register-ObjectEvent $watcher "Changed" -Action $action | Out-Null

# Keep script running
while ($true) {
    Start-Sleep -Seconds 1
}

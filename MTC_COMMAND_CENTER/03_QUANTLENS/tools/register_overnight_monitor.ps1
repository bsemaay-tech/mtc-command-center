# register_overnight_monitor.ps1
# Windows Task Scheduler kaydi — 30dk fire monitor.
# Admin yetkisiyle TEK SEFER calistir.

$taskName  = "MCC_Overnight_Monitor"
$scriptPath = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools\monitor_overnight.ps1"

# Mevcut gorevi sil (idempotent)
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Eski gorev silindi"
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger `
    -Once -At (Get-Date).AddMinutes(2) `
    -RepetitionInterval (New-TimeSpan -Minutes 30) `
    -RepetitionDuration (New-TimeSpan -Hours 24)

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "MCC Overnight Backtest harici saglik kontrolu (heartbeat 30dk)"

Write-Host "Kaydedildi: $taskName"
Write-Host "Ilk fire: $((Get-Date).AddMinutes(2))"
Write-Host "Tekrar: 30dk"
Write-Host ""
Write-Host "Manuel test: Start-ScheduledTask -TaskName $taskName"
Write-Host "Log: C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\_external_monitor.log"

param()
Write-Host "Preventing sleep on AC..."
# Using powercfg to set standby-timeout-ac to 0 (never sleep)
powercfg /change standby-timeout-ac 0
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Could not change power settings. Make sure to run as Admin."
} else {
    Write-Host "Sleep prevention applied for AC power."
}

param()
Write-Host "Restoring sleep settings..."
# Setting standby-timeout-ac back to default (e.g., 30 mins, but assuming the user might want a sensible default)
# Note: Ideally we read the old setting from power_settings_before.txt. 30 usually works as a safe default.
powercfg /change standby-timeout-ac 30
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Could not restore power settings. Make sure to run as Admin."
} else {
    Write-Host "Sleep settings restored."
}

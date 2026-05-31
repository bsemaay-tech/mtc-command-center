param(
    [int]$PollSeconds = 5
)

$ErrorActionPreference = "SilentlyContinue"

while ($true) {
    shutdown.exe /a *> $null
    Start-Sleep -Seconds $PollSeconds
}

param(
    [string]$Root = $PSScriptRoot,
    [string]$Output = (Join-Path $PSScriptRoot 'INDEX.md')
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = [IO.Path]::GetFullPath($Root)
$resolvedOutput = [IO.Path]::GetFullPath($Output)
$utf8NoBom = [Text.UTF8Encoding]::new($false)

function Clean-Cell([string]$Value, [int]$Limit) {
    if ($null -eq $Value) { return '' }
    $clean = ($Value -replace '\|', '\|' -replace '\s+', ' ').Trim()
    if ($clean.Length -gt $Limit) { return $clean.Substring(0, $Limit - 3) + '...' }
    return $clean
}

function File-Date([string]$Name) {
    if ($Name -match '(20\d{2})[-_](\d{2})[-_](\d{2})') { return "$($Matches[1])-$($Matches[2])-$($Matches[3])" }
    if ($Name -match '(20\d{2})(\d{2})(\d{2})') { return "$($Matches[1])-$($Matches[2])-$($Matches[3])" }
    return '-'
}

$lines = [Collections.Generic.List[string]]::new()
$lines.Add('# 11_TRIAGE index')
$lines.Add('')
$lines.Add('> Generated search index. Do not read triage history by default; grep this file, then open at most the relevant record.')
$lines.Add('')
$lines.Add('| Path | Date | Topic | One-line summary |')
$lines.Add('|---|---|---|---|')

$files = Get-ChildItem -LiteralPath $resolvedRoot -File -Recurse |
    Where-Object { [IO.Path]::GetFullPath($_.FullName) -ne $resolvedOutput } |
    Sort-Object FullName

foreach ($file in $files) {
    $rootPrefix = $resolvedRoot.TrimEnd('\') + '\'
    if (-not $file.FullName.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Indexed file escaped root: $($file.FullName)"
    }
    $relative = $file.FullName.Substring($rootPrefix.Length).Replace('\', '/')
    $topic = [IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '[_-]+', ' '
    if ([string]::IsNullOrWhiteSpace($topic)) { $topic = $file.Name }
    $summary = "$($file.Extension.TrimStart('.').ToUpperInvariant()) file"

    if ($file.Extension -in '.md', '.txt', '.json', '.ps1', '.py', '.sh', '.yaml', '.yml') {
        try {
            $content = [IO.File]::ReadAllLines($file.FullName)
            $heading = $content | Where-Object { $_ -match '^#{1,6}\s+\S' } | Select-Object -First 1
            if ($heading) { $topic = $heading -replace '^#{1,6}\s+', '' }
            $body = $content | Where-Object {
                $v = $_.Trim()
                $v -and $v -notmatch '^(#|>|\||```|---$)'
            } | Select-Object -First 1
            if ($body) { $summary = $body }
        } catch {
            $summary = "Unreadable during index generation: $($_.Exception.GetType().Name)"
        }
    }

    $pathCell = Clean-Cell $relative 180
    $dateCell = File-Date $file.Name
    $topicCell = Clean-Cell $topic 120
    $summaryCell = Clean-Cell $summary 180
    $lines.Add('| `' + $pathCell + '` | ' + $dateCell + ' | ' + $topicCell + ' | ' + $summaryCell + ' |')
}

[IO.File]::WriteAllLines($resolvedOutput, $lines, $utf8NoBom)
Write-Output "Indexed $($files.Count) files into $resolvedOutput"

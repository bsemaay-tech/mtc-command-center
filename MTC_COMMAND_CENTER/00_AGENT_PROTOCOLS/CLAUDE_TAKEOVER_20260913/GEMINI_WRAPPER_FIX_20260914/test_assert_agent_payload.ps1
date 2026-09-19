param([Parameter(Mandatory = $true)][string] $WrapperPath)
# Unit test of Assert-AgentPayload extracted from a wrapper file (no Gemini call). Prints one line per case.
$ErrorActionPreference = 'Stop'
$src = Get-Content -LiteralPath $WrapperPath -Raw
function Extract([string] $name) {
    $m = [regex]::Match($src, "(?ms)^function $name \{.*?^\}")
    if (-not $m.Success) { throw "function $name not found" }
    return $m.Value
}
# The strict-JSON guard (C# here-string) is not under test; stub it with a plain parse so the payload logic is isolated.
function Assert-StrictJsonObject { param([string] $JsonText) $null = $JsonText | ConvertFrom-Json }
Invoke-Expression (Extract 'Assert-ExactJsonProperties')
Invoke-Expression (Extract 'Assert-AgentPayload')

$usage = '{"input_tokens":1,"output_tokens":2,"thinking_tokens":3,"cache_read_tokens":4,"total_tokens":10}'
$cases = @(
    @{ name = 'six members, SUCCESS, sentinel'; expect = 'PASS'; json = '{"conversation_id":"c","status":"SUCCESS","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1,"usage":' + $usage + '}' },
    @{ name = 'seven members (extra error object), SUCCESS, sentinel'; expect = 'PASS'; json = '{"conversation_id":"c","status":"SUCCESS","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1,"usage":' + $usage + ',"error":{"attempts":5,"message":"INTERNAL (code 500)"}}' },
    @{ name = 'seven members, status ERROR'; expect = 'THROW'; json = '{"conversation_id":"c","status":"ERROR","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1,"usage":' + $usage + ',"error":"x"}' },
    @{ name = 'seven members, SUCCESS, sentinel missing'; expect = 'THROW'; json = '{"conversation_id":"c","status":"SUCCESS","response":"OK\n","duration_seconds":1.5,"num_turns":1,"usage":' + $usage + ',"error":"x"}' },
    @{ name = 'usage missing'; expect = 'THROW'; json = '{"conversation_id":"c","status":"SUCCESS","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1}' },
    @{ name = 'usage with an extra member'; expect = 'THROW'; json = '{"conversation_id":"c","status":"SUCCESS","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1,"usage":{"input_tokens":1,"output_tokens":2,"thinking_tokens":3,"cache_read_tokens":4,"total_tokens":10,"total_usd":0.1}}' },
    @{ name = 'member name wrong case (Status)'; expect = 'THROW'; json = '{"conversation_id":"c","Status":"SUCCESS","response":"OK\nGEMINI_READ_ONLY_OK\n","duration_seconds":1.5,"num_turns":1,"usage":' + $usage + '}' }
)
$fail = 0
foreach ($c in $cases) {
    $outcome = 'PASS'; $msg = ''
    try { Assert-AgentPayload -JsonText $c.json } catch { $outcome = 'THROW'; $msg = ($_.Exception.Message -split "`n")[0] }
    $verdict = if ($outcome -eq $c.expect) { 'OK ' } else { 'BAD'; $fail++ }
    Write-Output ("{0} expected={1} got={2} :: {3} {4}" -f $verdict, $c.expect, $outcome, $c.name, $msg)
}
Write-Output ("RESULT: {0}" -f $(if ($fail -eq 0) { 'ALL CASES AS EXPECTED' } else { "$fail CASE(S) DIFFER" }))
exit $fail

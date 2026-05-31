param(
    [string]$ApiKey = $env:LITELLM_KEY
)

Write-Host "--- 1. Netstat Check (Port 4000) ---" -ForegroundColor Cyan
netstat -ano | findstr :4000

$baseUrl = "http://localhost:4000/v1"
$headers = @{}

Write-Host "`n--- 2. Testing /v1/models ---" -ForegroundColor Cyan
try {
    Write-Host "Attempting GET $baseUrl/models without headers..."
    $models = Invoke-RestMethod -Uri "$baseUrl/models" -Method Get -ErrorAction Stop
    Write-Host "Success without headers!"
} catch {
    Write-Host "Failed without headers. Retrying with Authorization..."
    if (-not $ApiKey) {
        Write-Host "No API Key provided. Defaulting to sk-stack-b-admin (as per instructions)." -ForegroundColor Yellow
        $ApiKey = "sk-stack-b-admin"
    }
    
    if ($ApiKey) {
        $headers = @{ 'Authorization' = "Bearer $ApiKey" }
        try {
            $models = Invoke-RestMethod -Uri "$baseUrl/models" -Method Get -Headers $headers -ErrorAction Stop
            Write-Host "Success with Authorization!"
        } catch {
            Write-Host "Failed even with Authorization: $_" -ForegroundColor Red
        }
    }
}

if ($models) {
    $models.data | ForEach-Object { Write-Host "Model found: $($_.id)" }
}

Write-Host "`n--- 3. Testing /v1/chat/completions ---" -ForegroundColor Cyan
$targetModel = "gpt-4o"
if ($models.data) { $targetModel = $models.data[0].id }

$requestBody = @{
    model = $targetModel
    messages = @(
        @{ role = 'user'; content = 'Sadece OK yaz.' }
    )
} | ConvertTo-Json

try {
    Write-Host "Sending chat request using model: $targetModel"
    $response = Invoke-RestMethod -Uri "$baseUrl/chat/completions" -Method Post -Headers $headers -Body $requestBody -ContentType 'application/json' -ErrorAction Stop
    Write-Host "Response: $($response.choices[0].message.content)" -ForegroundColor Green
} catch {
    Write-Host "Chat request failed: $_" -ForegroundColor Red
}

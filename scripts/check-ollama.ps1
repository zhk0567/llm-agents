# Check Ollama connectivity and default model
$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

$cfg = Get-Content (Join-Path $ProjectRoot "config\ollama.json") -Raw | ConvertFrom-Json
$hostUrl = $cfg.host

try {
    $resp = Invoke-RestMethod -Uri "$hostUrl/api/tags" -Method Get -TimeoutSec 5
    Write-Host "Ollama: running at $hostUrl" -ForegroundColor Green
    $models = @($resp.models | ForEach-Object { $_.name })
    if ($models) {
        Write-Host "Models: $($models -join ', ')"
    } else {
        Write-Host "No models pulled yet. Run: .\scripts\pull-models.ps1" -ForegroundColor Yellow
    }
    if ($models -contains $cfg.default_model -or ($models | Where-Object { $_ -like "$($cfg.default_model)*" })) {
        Write-Host "Default model '$($cfg.default_model)' is available." -ForegroundColor Green
        exit 0
    }
    Write-Host "Default model '$($cfg.default_model)' not found." -ForegroundColor Yellow
    exit 1
} catch {
    Write-Host "Ollama: not reachable ($hostUrl)" -ForegroundColor Red
    Write-Host "Start with: ollama serve"
    exit 2
}

# Check Ollama connectivity and default model (no download)
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
        Write-Host "Installed: $($models -join ', ')"
    } else {
        Write-Host "No models listed." -ForegroundColor Yellow
    }
    $match = $models | Where-Object { $_ -eq $cfg.default_model -or $_ -like "$($cfg.default_model)*" }
    if ($match) {
        Write-Host "Default '$($cfg.default_model)' is ready." -ForegroundColor Green
        exit 0
    }
    Write-Host "Default '$($cfg.default_model)' not found — pick one from list or edit config/ollama.json" -ForegroundColor Yellow
    exit 1
} catch {
    Write-Host "Ollama: not reachable ($hostUrl)" -ForegroundColor Red
    Write-Host "Start with: ollama serve"
    exit 2
}

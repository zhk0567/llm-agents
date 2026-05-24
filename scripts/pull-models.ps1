# Verify Ollama models (does NOT download by default)
param(
    [switch]$Download
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

$configPath = Join-Path (Split-Path -Parent $PSScriptRoot) "config\ollama.json"
$cfg = Get-Content $configPath -Raw | ConvertFrom-Json

Write-Host "Installed models:"
ollama list

$default = $cfg.default_model
$found = ollama list 2>$null | Select-String -SimpleMatch ($default.Split(':')[0])
if ($found) {
    Write-Host "Default model '$default' is available." -ForegroundColor Green
} else {
    Write-Host "Default model '$default' not in list." -ForegroundColor Yellow
    Write-Host "Edit config/ollama.json or: `$env:OLLAMA_MODEL = '<your-model>'"
}

if (-not $Download) {
    Write-Host ""
    Write-Host "No download (use -Download to pull from config)."
    exit 0
}

foreach ($m in @($cfg.default_model, $cfg.fallback_model) | Where-Object { $_ }) {
    Write-Host "Pulling $m ..."
    ollama pull $m
}

Write-Host "Done. Models directory: $env:OLLAMA_MODELS"

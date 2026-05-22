# Configure Ollama to use project-local model directory (Windows PowerShell)
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ModelsDir = Join-Path $ProjectRoot "models\ollama"

if (-not (Test-Path $ModelsDir)) {
    New-Item -ItemType Directory -Path $ModelsDir -Force | Out-Null
}

$env:OLLAMA_MODELS = $ModelsDir
Write-Host "OLLAMA_MODELS = $env:OLLAMA_MODELS"

$configPath = Join-Path $ProjectRoot "config\ollama.json"
if (Test-Path $configPath) {
    $cfg = Get-Content $configPath -Raw | ConvertFrom-Json
    Write-Host "Default model: $($cfg.default_model)"
    Write-Host "Base URL: $($cfg.base_url)"
}

Write-Host ""
Write-Host "Run in this session before 'ollama serve' or 'ollama pull':"
Write-Host "  .\scripts\setup-ollama.ps1"
Write-Host "Or dot-source to persist for current shell:"
Write-Host "  . .\scripts\setup-ollama.ps1"

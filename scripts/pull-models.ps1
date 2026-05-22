# Pull default Ollama models into project-local models/ollama
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

$configPath = Join-Path (Split-Path -Parent $PSScriptRoot) "config\ollama.json"
$cfg = Get-Content $configPath -Raw | ConvertFrom-Json

$models = @($cfg.default_model)
if ($cfg.fallback_model -and $cfg.fallback_model -ne $cfg.default_model) {
    $models += $cfg.fallback_model
}

foreach ($m in $models) {
    Write-Host "Pulling $m ..."
    ollama pull $m
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Failed to pull $m — ensure Ollama is installed and on PATH."
    }
}

Write-Host "Done. Models directory: $env:OLLAMA_MODELS"

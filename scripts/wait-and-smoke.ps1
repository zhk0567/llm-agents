# Run live smoke with installed model only (no ollama pull)
param(
    [string]$Model = "",
    [string]$Topic = "AI Agent 框架选型"
)

$ErrorActionPreference = "Stop"
$configPath = Join-Path (Split-Path -Parent $PSScriptRoot) "config\ollama.json"
if (-not $Model -and (Test-Path $configPath)) {
    $Model = (Get-Content $configPath -Raw | ConvertFrom-Json).default_model
}

if (-not $Model) {
    Write-Host "Specify -Model or set config/ollama.json default_model"
    exit 1
}

$list = ollama list 2>$null | Out-String
if ($list -notmatch [regex]::Escape($Model.Split(':')[0])) {
    Write-Host "Model '$Model' not installed. Available:"
    ollama list
    exit 1
}

Write-Host "Smoke with installed model: $Model"
& (Join-Path $PSScriptRoot "run-smoke-live.ps1") -Model $Model -Topic $Topic
& (Join-Path $PSScriptRoot "update-matrix-from-smoke.ps1")

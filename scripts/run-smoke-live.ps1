# Run live smoke using an already-installed Ollama model (no download)
param(
    [string]$Model = "",
    [string]$Topic = "AI Agent 框架选型"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

$configPath = Join-Path $ProjectRoot "config\ollama.json"
$cfg = Get-Content $configPath -Raw | ConvertFrom-Json

if (-not $Model) {
    $Model = $cfg.default_model
    $list = ollama list 2>$null | Out-String
    if ($list -notmatch [regex]::Escape($Model.Split(':')[0])) {
        foreach ($line in (ollama list 2>$null | Select-Object -Skip 1)) {
            $name = ($line -split '\s+')[0]
            if ($name -and $name -notmatch 'embed') {
                Write-Host "Default '$Model' not found; using installed: $name" -ForegroundColor Yellow
                $Model = $name
                break
            }
        }
    }
}

if (-not $Model) {
    Write-Host "No model specified. Example: .\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud"
    exit 1
}

Write-Host "Using installed model: $Model (no download)"
$env:OLLAMA_MODEL = $Model
& (Join-Path $PSScriptRoot "run-all-smoke.ps1")

# Wait for Ollama model then run live smoke
param(
    [string]$Model = "qwen2.5:7b",
    [int]$TimeoutMinutes = 60
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

Write-Host "Pulling $Model (if missing)..."
ollama pull $Model 2>&1 | Out-File (Join-Path $ProjectRoot "docs\pull-$($Model -replace '[:.]','-').log") -Encoding utf8

$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
while ((Get-Date) -lt $deadline) {
    $list = ollama list 2>$null | Out-String
    if ($list -match [regex]::Escape($Model.Split(':')[0])) {
        Write-Host "Model available: $Model"
        & (Join-Path $PSScriptRoot "run-smoke-live.ps1") -Model $Model
        & (Join-Path $PSScriptRoot "update-matrix-from-smoke.ps1")
        exit 0
    }
    Start-Sleep -Seconds 15
}
Write-Host "Timeout waiting for $Model"
exit 1

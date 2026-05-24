# Run smoke with a specific Ollama model (live LLM, not fallback when model works)
param(
    [string]$Model = "",
    [string]$Topic = "AI Agent 框架选型"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

if (-not $Model) {
    try {
        $tags = ollama list 2>$null | Select-Object -Skip 1
        foreach ($line in $tags) {
            $name = ($line -split '\s+')[0]
            if ($name -and $name -notmatch 'embed') {
                $Model = $name
                break
            }
        }
    } catch { }
}

if (-not $Model) {
    Write-Host "No model specified and none detected. Use: .\scripts\run-smoke-live.ps1 -Model qwen2.5:7b"
    exit 1
}

Write-Host "OLLAMA_MODEL = $Model"
$env:OLLAMA_MODEL = $Model
$env:Topic = $Topic

& (Join-Path $PSScriptRoot "run-all-smoke.ps1")

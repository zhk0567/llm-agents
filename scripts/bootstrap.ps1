# One-shot project bootstrap (Windows PowerShell)
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "=== llm-agents bootstrap ===" -ForegroundColor Cyan

function Test-Command($Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { Write-Host "  OK  $Name" -ForegroundColor Green; return $true }
    Write-Host "  --  $Name (not found)" -ForegroundColor Yellow
    return $false
}

Write-Host "`n[1/5] Toolchain"
Test-Command python | Out-Null
Test-Command node | Out-Null
$hasOllama = Test-Command ollama
Test-Command dotnet | Out-Null
Test-Command mvn | Out-Null

Write-Host "`n[2/5] Ollama models path"
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

Write-Host "`n[3/5] Python venv"
$PyDir = Join-Path $ProjectRoot "python"
$VenvPython = Join-Path $PyDir ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Set-Location $PyDir
    python -m venv .venv
    Set-Location $ProjectRoot
}
Set-Location $PyDir
& .\.venv\Scripts\pip.exe install -e ".[all]" -q
Set-Location $ProjectRoot
Write-Host "  Python deps installed" -ForegroundColor Green

Write-Host "`n[4/5] TypeScript"
$TsDir = Join-Path $ProjectRoot "typescript"
if (Test-Path (Join-Path $TsDir "package.json")) {
    Set-Location $TsDir
    npm install --silent 2>$null
    Set-Location $ProjectRoot
    Write-Host "  npm install done" -ForegroundColor Green
}

Write-Host "`n[5/5] Optional .NET restore"
$DotnetSln = Join-Path $ProjectRoot "dotnet\llm-agents.sln"
if ((Test-Command dotnet) -and (Test-Path $DotnetSln)) {
    dotnet restore $DotnetSln --verbosity quiet
    Write-Host "  dotnet restore done" -ForegroundColor Green
}

Write-Host "`n=== Done ===" -ForegroundColor Cyan
if (-not $hasOllama) {
    Write-Host "Install Ollama: https://ollama.com/download"
} else {
    Write-Host "Next: ollama serve  (then .\scripts\pull-models.ps1)"
}
Write-Host "Run smoke: .\scripts\run-all-smoke.ps1"

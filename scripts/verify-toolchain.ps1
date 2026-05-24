# Verify optional toolchain for dotnet/java smoke
$ErrorActionPreference = "Continue"
Write-Host "=== Toolchain check ===" -ForegroundColor Cyan
$allOk = $true

function Test-Tool($Name, $Cmd) {
    if (Get-Command $Cmd -ErrorAction SilentlyContinue) {
        $v = & $Cmd --version 2>$null | Select-Object -First 1
        Write-Host "  OK  $Name : $v" -ForegroundColor Green
        return $true
    }
    Write-Host "  --  $Name not found" -ForegroundColor Yellow
    return $false
}

Test-Tool "python" "python" | Out-Null
Test-Tool "node" "node" | Out-Null
Test-Tool "ollama" "ollama" | Out-Null
if (-not (Test-Tool ".NET SDK" "dotnet")) { $allOk = $false }
if (-not (Test-Tool "Maven" "mvn")) { $allOk = $false }
if (-not (Test-Tool "Java" "java")) { $allOk = $false }

Write-Host ""
if (-not $allOk) {
    Write-Host "Install guide: docs\INSTALL_TOOLCHAIN.md"
    exit 1
}
Write-Host "All optional tools present."
exit 0

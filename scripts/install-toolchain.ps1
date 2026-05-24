# Optional: install .NET 8 SDK, JDK 17, Maven via winget (Windows)
param(
    [switch]$SkipDotnet,
    [switch]$SkipMaven,
    [switch]$WhatIf
)

$ErrorActionPreference = "Continue"
Write-Host "=== install-toolchain (winget) ===" -ForegroundColor Cyan

function Install-Winget($Id, $Name) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Host "winget not found; install manually: docs\INSTALL_TOOLCHAIN.md" -ForegroundColor Yellow
        return
    }
    Write-Host "Installing $Name ($Id) ..."
    if ($WhatIf) {
        winget show --id $Id
        return
    }
    winget install --id $Id -e --accept-source-agreements --accept-package-agreements
}

if (-not $SkipDotnet) {
    Install-Winget "Microsoft.DotNet.SDK.8" ".NET 8 SDK"
}
if (-not $SkipMaven) {
    Install-Winget "EclipseAdoptium.Temurin.17.JDK" "Temurin JDK 17"
    Install-Winget "Apache.Maven" "Apache Maven"
}

Write-Host ""
Write-Host "Restart terminal, then: .\scripts\verify-toolchain.ps1"

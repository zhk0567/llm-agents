# Install all Python framework dependencies into python/.venv
$ErrorActionPreference = "Stop"
$PythonDir = Split-Path -Parent $PSScriptRoot
Set-Location $PythonDir

$venvPip = Join-Path $PythonDir ".venv\Scripts\pip.exe"
if (-not (Test-Path $venvPip)) {
    python -m venv .venv
}

Write-Host "Installing editable package..."
& $venvPip install -e ".[all]"
Write-Host "Done."

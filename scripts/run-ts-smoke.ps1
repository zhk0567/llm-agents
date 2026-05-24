# Quick smoke for TypeScript demos only
$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "setup-ollama.ps1")

$Topic = "AI Agent 框架选型"
$PyVenv = Join-Path $ProjectRoot "python\.venv\Scripts\python.exe"
$Validator = Join-Path $ProjectRoot "python\scripts\validate_stdout.py"

function Invoke-NpxTsMain {
    param([string]$Dir, [string]$Topic)
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "cmd.exe"
    $psi.Arguments = "/c npx --yes tsx main.ts `"$Topic`""
    $psi.RedirectStandardOutput = $true
    $psi.UseShellExecute = $false
    $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $psi.WorkingDirectory = $Dir
    $p = [System.Diagnostics.Process]::Start($psi)
    $out = $p.StandardOutput.ReadToEnd()
    $p.WaitForExit()
    return $out
}

function Test-StdoutJson {
    param([string]$Out)
    $tmp = Join-Path $env:TEMP ("llm-agents-validate-{0}.json" -f [guid]::NewGuid().ToString('N'))
    try {
        $utf8 = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($tmp, $Out, $utf8)
        & $PyVenv $Validator $tmp 2>$null | Out-Null
        return $LASTEXITCODE
    } finally {
        Remove-Item $tmp -ErrorAction SilentlyContinue
    }
}

foreach ($pkg in @("langgraph-js", "openai-agents")) {
    $dir = Join-Path $ProjectRoot "typescript\$pkg"
    Write-Host "[$pkg] ..."
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $out = Invoke-NpxTsMain -Dir $dir -Topic $Topic
    $code = Test-StdoutJson -Out $out
    $sw.Stop()
    $status = if ($code -eq 0) { "OK" } elseif ($code -eq 3) { "OK_FALLBACK" } else { "FAIL" }
    Write-Host "  $status ($([int]$sw.ElapsedMilliseconds)ms) validate=$code"
}

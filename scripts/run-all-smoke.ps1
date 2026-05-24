# Run smoke tests with timing + JSON schema validation
$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogFile = Join-Path $ProjectRoot "docs\smoke-log.txt"
$BenchFile = Join-Path $ProjectRoot "docs\benchmarks.md"
$Topic = "AI Agent 框架选型"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$OllamaStatus = "unknown"
try {
    & (Join-Path $PSScriptRoot "check-ollama.ps1") 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $OllamaStatus = "running+model" }
    elseif ($LASTEXITCODE -eq 1) { $OllamaStatus = "running (default model missing)" }
    else { $OllamaStatus = "down" }
} catch { $OllamaStatus = "down" }

@(
    "# Smoke log",
    "",
    "- Run: $Timestamp",
    "- Topic: $Topic",
    "- Ollama: $OllamaStatus",
    "",
    "| Framework | Status | ms | Schema | Fallback |",
    "|-----------|--------|-----|--------|----------|"
) | Out-File $LogFile -Encoding utf8

$benchRows = @(
    "# Benchmarks",
    "",
    "Updated: $Timestamp",
    "",
    "| Framework | Elapsed ms | Schema | Fallback | Notes |",
    "|-----------|------------|--------|----------|-------|"
)

function Invoke-Smoke {
    param([string]$Name, [scriptblock]$RunBlock)
    Write-Host "[$Name] ..."
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $status = "FAIL"
    $schema = "-"
    $fallback = "-"
    $note = ""
    try {
        $out = & $RunBlock 2>$null | Out-String
        $sw.Stop()
        $PyVenv = Join-Path $ProjectRoot "python\.venv\Scripts\python.exe"
        $Validator = Join-Path $ProjectRoot "python\scripts\validate_stdout.py"
        if ($out -match "\{") {
            $out | & $PyVenv $Validator 2>$null
            $vcode = $LASTEXITCODE
            if ($vcode -eq 0) {
                $schema = "OK"
                $fallback = "no"
                $status = "OK"
            } elseif ($vcode -eq 3) {
                $schema = "OK"
                $fallback = "yes"
                $status = "OK_FALLBACK"
                $note = "Ollama unavailable or LLM error"
            } elseif ($vcode -eq 2) {
                $schema = "FAIL"
                $status = "FAIL"
            } else {
                $schema = "INVALID"
                $status = "FAIL"
            }
        } else {
            $status = "FAIL"
            $note = "no JSON in output"
        }
        if ($LASTEXITCODE -ne 0 -and $status -eq "OK") { $status = "FAIL" }
    } catch {
        $sw.Stop()
        $status = "FAIL"
        $note = $_.Exception.Message
    }
    $ms = [int]$sw.ElapsedMilliseconds
    Write-Host "  $status (${ms}ms) schema=$schema fallback=$fallback"
    "| $Name | $status | $ms | $schema | $fallback |" | Out-File $LogFile -Append -Encoding utf8
    $benchRows += "| $Name | $ms | $schema | $fallback | $note |"
}

$PyVenv = Join-Path $ProjectRoot "python\.venv\Scripts\python.exe"
$PyRoot = Join-Path $ProjectRoot "python"
$ValidateScript = Join-Path $ProjectRoot "python\scripts\validate_stdout.py"

if (-not (Test-Path $PyVenv)) {
    Write-Host "Run .\scripts\bootstrap.ps1 first" -ForegroundColor Yellow
}

if (Test-Path $PyVenv) {
    foreach ($fw in @("langgraph", "crewai", "llamaindex", "pydantic_ai", "smolagents", "ag2", "maf", "haystack", "dspy")) {
        foreach ($script in @("main.py", "crew_research.py")) {
            $main = Join-Path $PyRoot "$fw\$script"
            if (Test-Path $main) {
                $label = if ($script -eq "main.py") { "python/$fw" } else { "python/$fw-crew" }
                Invoke-Smoke $label {
                    Push-Location (Join-Path $PyRoot $fw)
                    try { & $PyVenv $script $Topic } finally { Pop-Location }
                }
            }
        }
    }
}

$DotnetProj = Join-Path $ProjectRoot "dotnet\src\TopicResearchAgent\TopicResearchAgent.csproj"
if ((Get-Command dotnet -ErrorAction SilentlyContinue) -and (Test-Path $DotnetProj)) {
    Invoke-Smoke "dotnet/TopicResearchAgent" {
        dotnet run --project $DotnetProj -- $Topic
    }
} else {
    "| dotnet/TopicResearchAgent | SKIP | - | - | .NET SDK not installed |" | Out-File $LogFile -Append -Encoding utf8
}

$TsRoot = Join-Path $ProjectRoot "typescript"
if (Test-Path (Join-Path $TsRoot "node_modules")) {
    foreach ($pkg in @("langgraph-js", "openai-agents")) {
        $pkgDir = Join-Path $TsRoot $pkg
        if (Test-Path (Join-Path $pkgDir "package.json")) {
            Invoke-Smoke "typescript/$pkg" {
                Push-Location $pkgDir
                try { npm run start -- $Topic 2>$null } finally { Pop-Location }
            }
        }
    }
}

$JavaDir = Join-Path $ProjectRoot "java\langchain4j"
if ((Get-Command mvn -ErrorAction SilentlyContinue) -and (Test-Path (Join-Path $JavaDir "pom.xml"))) {
    Invoke-Smoke "java/langchain4j" {
        Push-Location $JavaDir
        try { mvn -Dmaven.repo.local=..\.m2\repository -q exec:java "-Dexec.args=$Topic" } finally { Pop-Location }
    }
} else {
    "| java/langchain4j | SKIP | - | - | Maven not installed |" | Out-File $LogFile -Append -Encoding utf8
}

$benchRows | Out-File $BenchFile -Encoding utf8
Write-Host ""
Write-Host "Log: $LogFile"
Write-Host "Benchmarks: $BenchFile"
Get-Content $LogFile

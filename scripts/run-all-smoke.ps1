# Run smoke tests for all framework demos (non-blocking on failure)
$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogFile = Join-Path $ProjectRoot "docs\smoke-log.txt"
$Topic = "AI Agent 框架选型"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"" | Out-File $LogFile -Encoding utf8
"Smoke run: $Timestamp" | Out-File $LogFile -Append -Encoding utf8
"Topic: $Topic" | Out-File $LogFile -Append -Encoding utf8
"---" | Out-File $LogFile -Append -Encoding utf8

function Invoke-Smoke {
    param([string]$Name, [scriptblock]$Block)
    Write-Host "[$Name] ..."
    try {
        & $Block
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            "OK  $Name" | Out-File $LogFile -Append -Encoding utf8
            Write-Host "  OK"
        } else {
            "FAIL $Name (exit $LASTEXITCODE)" | Out-File $LogFile -Append -Encoding utf8
            Write-Host "  FAIL (exit $LASTEXITCODE)"
        }
    } catch {
        "FAIL $Name : $_" | Out-File $LogFile -Append -Encoding utf8
        Write-Host "  FAIL: $_"
    }
}

$PyVenv = Join-Path $ProjectRoot "python\.venv\Scripts\python.exe"
$PyRoot = Join-Path $ProjectRoot "python"

if (Test-Path $PyVenv) {
    foreach ($fw in @("langgraph", "crewai", "llamaindex", "pydantic_ai", "smolagents", "ag2", "maf")) {
        $main = Join-Path $PyRoot "$fw\main.py"
        if (Test-Path $main) {
            Invoke-Smoke "python/$fw" {
                Push-Location (Join-Path $PyRoot $fw)
                try {
                    & $PyVenv main.py $Topic 2>&1 | Out-Null
                } finally {
                    Pop-Location
                }
            }
        }
    }
}

$DotnetProj = Join-Path $ProjectRoot "dotnet\src\TopicResearchAgent\TopicResearchAgent.csproj"
if (Test-Path $DotnetProj) {
    Invoke-Smoke "dotnet/TopicResearchAgent" {
        dotnet run --project $DotnetProj -- $Topic 2>&1 | Out-Null
    }
}

$TsRoot = Join-Path $ProjectRoot "typescript"
if (Test-Path (Join-Path $TsRoot "node_modules")) {
    foreach ($pkg in @("langgraph-js", "openai-agents")) {
        $pkgDir = Join-Path $TsRoot $pkg
        if (Test-Path (Join-Path $pkgDir "package.json")) {
            Invoke-Smoke "typescript/$pkg" {
                Set-Location $pkgDir
                npm run start -- $Topic 2>&1 | Out-Null
                Set-Location $ProjectRoot
            }
        }
    }
}

$JavaDir = Join-Path $ProjectRoot "java\langchain4j"
if (Test-Path (Join-Path $JavaDir "pom.xml")) {
    Invoke-Smoke "java/langchain4j" {
        Set-Location $JavaDir
        mvn -q exec:java "-Dexec.args=$Topic" 2>&1 | Out-Null
        Set-Location $ProjectRoot
    }
}

Write-Host ""
Write-Host "Log: $LogFile"
Get-Content $LogFile

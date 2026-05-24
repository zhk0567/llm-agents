# Parse docs/smoke-log.txt into docs/benchmarks.md and patch FRAMEWORK_MATRIX.md
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Log = Join-Path $ProjectRoot "docs\smoke-log.txt"
$BenchFile = Join-Path $ProjectRoot "docs\benchmarks.md"
$Matrix = Join-Path $ProjectRoot "docs\FRAMEWORK_MATRIX.md"

if (-not (Test-Path $Log)) { Write-Host "Missing smoke-log"; exit 1 }

$lines = Get-Content $Log
$runLine = ($lines | Where-Object { $_ -match '^- Run:' }) -replace '^- Run:\s*',''
$topicLine = ($lines | Where-Object { $_ -match '^- Topic:' }) -replace '^- Topic:\s*',''
$ollamaLine = ($lines | Where-Object { $_ -match '^- Ollama:' }) -replace '^- Ollama:\s*',''

$benchOut = @(
    "# Benchmarks",
    "",
    "Updated: $runLine",
    "Topic: $topicLine",
    "Ollama: $ollamaLine",
    "",
    "| Framework | Elapsed ms | Schema | Fallback | Status |",
    "|-----------|------------|--------|----------|--------|"
)

$map = @{
    'python/langgraph' = 'LangGraph'
    'python/langgraph-crew' = 'LangGraph'
    'python/crewai' = 'CrewAI'
    'python/llamaindex' = 'LlamaIndex'
    'python/pydantic_ai' = 'Pydantic AI'
    'python/ag2' = 'AG2'
    'python/smolagents' = 'Smolagents'
    'python/maf' = 'MAF (Python)'
    'python/haystack' = 'Haystack'
    'python/dspy' = 'DSPy'
    'typescript/langgraph-js' = 'LangGraph.js'
    'typescript/openai-agents' = 'OpenAI Agents SDK'
}

$matrixNotes = @{}

foreach ($line in $lines) {
    if ($line -match '^\|\s*([^\|]+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*([^|]*)\|\s*([^|]*)\|') {
        $fw = $Matches[1].Trim()
        $status = $Matches[2].Trim()
        $ms = $Matches[3].Trim()
        $schema = $Matches[4].Trim()
        $fb = $Matches[5].Trim()
        $benchOut += "| $fw | $ms | $schema | $fb | $status |"
        if ($map.ContainsKey($fw) -and $status -match 'OK') {
            $key = $map[$fw]
            $note = "${ms}ms fb=$fb (nemotron-3-super:cloud smoke)"
            if (-not $matrixNotes.ContainsKey($key)) { $matrixNotes[$key] = $note }
        }
    }
}

$benchOut | Set-Content $BenchFile -Encoding utf8

$content = Get-Content $Matrix -Raw -Encoding UTF8
foreach ($name in $matrixNotes.Keys) {
    $note = $matrixNotes[$name]
    $esc = [regex]::Escape($name)
    $content = $content -replace "(\|\s*$esc\s*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|)[^\|]*(\|)", "`${1}$note`${2}"
}
$content | Set-Content $Matrix -Encoding utf8 -NoNewline
Write-Host "Updated benchmarks + matrix from smoke-log"

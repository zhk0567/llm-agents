# Benchmarks

Updated: 2026-05-24 11:49:59  
Topic: AI Agent 框架选型  
Ollama: running (model: nemotron-3-super:cloud via OLLAMA_MODEL)

| Framework | Elapsed ms | Schema | Fallback | Status |
|-----------|------------|--------|----------|--------|
| python/langgraph | 2479 | - | - | FAIL (import fixed) |
| python/langgraph-crew | 10537 | OK | no | OK |
| python/crewai | 42241 | OK | no | OK |
| python/crewai-crew | 37415 | OK | no | OK |
| python/llamaindex | 2915 | OK | no | OK |
| python/pydantic_ai | 7207 | OK | no | OK |
| python/smolagents | 25553 | OK | no | OK |
| python/ag2 | 9881 | OK | no | OK |
| python/ag2-crew | 9288 | OK | no | OK |
| python/maf | 8464 | OK | no | OK |
| python/maf-crew | 9080 | OK | no | OK |
| python/haystack | 5886 | OK | no | OK |
| python/dspy | 15401 | OK | no | OK |
| dotnet/TopicResearchAgent | 13 | - | - | FAIL (.NET SDK) |
| typescript/langgraph-js | 1839 | INVALID | - | FAIL |
| typescript/openai-agents | 6174 | INVALID | - | FAIL |

Regenerate: `.\scripts\run-smoke-live.ps1 -Model <name>` then `.\scripts\update-matrix-from-smoke.ps1`

# .NET — Semantic Kernel + Ollama

NuGet 包缓存于 `dotnet/packages`（见 `nuget.config`）。

## 运行

```powershell
cd f:\commercial\llm-agents\dotnet
dotnet restore
dotnet run --project src\TopicResearchAgent -- "测试主题"
```

需 Ollama 运行且已执行 `.\scripts\setup-ollama.ps1`。

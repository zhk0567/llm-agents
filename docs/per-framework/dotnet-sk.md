# .NET Semantic Kernel

## 范式

`Kernel` + `ResearchPlugin` + `InvokePromptAsync`，OpenAI 连接器指向 Ollama。

## NuGet

包缓存在 `dotnet/packages`（`nuget.config`）。

## 运行

```powershell
cd dotnet
dotnet run --project src\TopicResearchAgent -- "主题"
```

# Windows 工具链安装指引（运行 dotnet/ java 示例前）

## .NET 8 SDK

1. 下载：https://dotnet.microsoft.com/download/dotnet/8.0  
2. 安装后验证：`dotnet --version`  
3. 运行示例：

```powershell
cd f:\commercial\llm-agents\dotnet
dotnet restore
dotnet run --project src\TopicResearchAgent -- "测试主题"
```

NuGet 缓存位于 `dotnet/packages`（见 `nuget.config`）。

## JDK 17 + Maven

1. 安装 [Temurin JDK 17](https://adoptium.net/)  
2. 安装 [Maven](https://maven.apache.org/download.cgi)，加入 `PATH`  
3. 验证：`java -version`、`mvn -version`  
4. 运行 LangChain4j：

```powershell
cd f:\commercial\llm-agents\java\langchain4j
mvn -Dmaven.repo.local=..\.m2\repository -q exec:java "-Dexec.args=测试主题"
```

## Ollama 与默认模型

```powershell
. .\scripts\setup-ollama.ps1
.\scripts\pull-models.ps1
# 或使用已有模型：
.\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud
```

## 一键检查

```powershell
.\scripts\bootstrap.ps1
.\scripts\check-ollama.ps1
```

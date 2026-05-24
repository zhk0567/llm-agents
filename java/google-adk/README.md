# Google ADK (Java)

[Google Agent Development Kit](https://google.github.io/adk-docs/) 示例，对齐 [TASK_SPEC.md](../../shared/TASK_SPEC.md)。

## 模式

- **有 `GOOGLE_API_KEY`**：ADK `LlmAgent` + `searchTopic` 工具（Gemini）
- **无 API Key**：输出 mock JSON（与 Python fallback 一致，便于 smoke）

## 运行

```powershell
cd f:\commercial\llm-agents\java\google-adk
mvn -Dmaven.repo.local=..\.m2\repository -q exec:java "-Dexec.args=测试主题"
```

可选：`$env:ADK_MODEL = "gemini-2.0-flash"`

## Ollama

ADK 默认面向 Gemini；本地 Ollama 需按 [Models & Authentication](https://google.github.io/adk-docs/agents/models/) 配置。本仓库 smoke 无 Key 时走 mock。

## 前置

JDK 17+、Maven 3.9+ — 见 [docs/INSTALL_TOOLCHAIN.md](../../docs/INSTALL_TOOLCHAIN.md) 或 `..\..\scripts\install-toolchain.ps1`

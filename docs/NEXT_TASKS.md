# 后续任务清单

## 模型策略

**不自动下载**。默认使用 [`config/ollama.json`](../config/ollama.json) 中的 `nemotron-3-super:cloud`（与本机 `ollama list` 一致）。

```powershell
ollama list
.\scripts\check-ollama.ps1
.\scripts\run-smoke-live.ps1
```

仅当需要新模型时：`.\scripts\pull-models.ps1 -Download`

## 待办

- [ ] `install-toolchain.ps1` → dotnet / Maven smoke
- [ ] ADK + `GOOGLE_API_KEY`（可选）

# 任务清单（收尾完成）

> 项目交付状态见 [PROJECT_STATUS.md](./PROJECT_STATUS.md)

## 已完成

- [x] 多语言 Agent 框架 demo（Python / TypeScript / dotnet / Java 参考代码）
- [x] 统一 TopicResearchAgent + mock 检索 + JSON schema
- [x] Ollama 本地模型策略（不自动下载，默认 `nemotron-3-super:cloud`）
- [x] Live smoke：Python 13 + TypeScript 2（2026-05-24，全部 OK）
- [x] Windows TS smoke UTF-8 修复
- [x] 对比矩阵与 benchmarks 回填

## 范围外（本仓库策略下不做）

- dotnet / Java live smoke（需安装 .NET SDK、Maven — 见 [INSTALL_TOOLCHAIN.md](./INSTALL_TOOLCHAIN.md)）
- Google ADK 真机（需 `GOOGLE_API_KEY`，非 Ollama）
- 自动 `ollama pull`、winget 工具链安装

## 日常复现

```powershell
.\scripts\check-ollama.ps1
.\scripts\run-smoke-live.ps1
```

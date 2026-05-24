# 后续任务清单

## 已完成

- Sprint A/B、P1–P3、Haystack/DSPy/HITL
- `run-smoke-live.ps1` + 真机 smoke（`nemotron-3-super:cloud`，12/14 Python OK）
- `update-matrix-from-smoke.ps1`、CONFIG / INSTALL_TOOLCHAIN 文档
- Google ADK 占位 `java/google-adk/`

## 待办

- [ ] `pull-models.ps1` 完成 `qwen2.5:7b` 拉取（见 `docs/pull-qwen.log`）
- [ ] 安装 .NET 8 / Maven（见 INSTALL_TOOLCHAIN）
- [ ] TypeScript smoke 真连（已支持 `OLLAMA_MODEL` 环境变量）
- [ ] Google ADK 可运行 demo（依赖 ADK GA）

## 命令

```powershell
.\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud
.\scripts\update-matrix-from-smoke.ps1
```

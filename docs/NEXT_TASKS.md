# 后续任务清单

## 已完成

- Sprint A/B、P1、P2（Haystack/DSPy/checkpoint/COMPARISON_REPORT）
- P3：`load_agent_config`、`hitl_demo.py`、config 测试
- Git push：`640c477..9b7b981` 已推送到 origin/main

## 下一批

- [ ] A1 拉取 `qwen2.5:7b` → 非 fallback smoke
- [ ] .NET 8 / Maven 本机验证
- [ ] Google ADK（可选 Java 子模块）
- [ ] 矩阵 B4：重跑 smoke 填实测列
- [ ] 各框架 README 补充 `config/agent.json` 说明

## 命令

```powershell
.\scripts\bootstrap.ps1
.\scripts\pull-models.ps1
.\scripts\run-all-smoke.ps1
cd python\langgraph
..\.venv\Scripts\python hitl_demo.py "主题"
```

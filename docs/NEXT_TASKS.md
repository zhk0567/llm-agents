# 后续任务清单

> 仓库：https://github.com/zhk0567/llm-agents

**最近更新**：P2 已加 Haystack、DSPy、LangGraph checkpoint；对比报告初版。

---

## 当前进度

| 类别 | 状态 |
|------|------|
| Sprint A/B 基础设施 | ✅ |
| P1 ResearchCrew + search 切换 | ✅ |
| P2 Haystack + DSPy demo | ✅ |
| P2 LangGraph checkpoint_demo | ✅ |
| P3 COMPARISON_REPORT 初版 | ✅ |
| P0 OpenTelemetry constraints 文件 | ✅（`constraints-otel.txt`） |
| Git push 上一批 | ⚠️ 本地已 commit `e4b5dab`，push 待网络恢复 |
| A1 拉取 qwen2.5:7b | ⬜ |
| .NET / Maven | ⬜ |
| Google ADK | ⬜ |
| HITL 样例 | ⬜ |

---

## 下一批（P3 剩余）

- [ ] LangGraph HITL：`python/langgraph/hitl_demo.py`（工具调用前确认）
- [ ] `config/agent.json` 接入各 main（timeout/retries）
- [ ] Google ADK Java 子模块（可选）
- [ ] 矩阵 B4：默认模型就绪后重跑 smoke 填实测列
- [ ] `pip install -c constraints-otel.txt` 验证 pytest 无 logfire 插件错误

---

## 本机命令

```powershell
git push origin main   # 推送 e4b5dab + 下一批 commit
.\scripts\pull-models.ps1
.\scripts\run-all-smoke.ps1
```

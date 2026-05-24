# 后续任务清单

> 仓库：https://github.com/zhk0567/llm-agents  
> 基准任务：[shared/TASK_SPEC.md](../shared/TASK_SPEC.md) · 框架矩阵：[FRAMEWORK_MATRIX.md](./FRAMEWORK_MATRIX.md)

**最近更新**：已执行 Sprint A/B 大部分自动化项；smoke 见 [smoke-log.txt](./smoke-log.txt)、[benchmarks.md](./benchmarks.md)。

---

## 当前进度

| 类别 | 状态 |
|------|------|
| bootstrap / check-ollama / schema / smoke 增强 | ✅ |
| ResearchCrew（langgraph、ag2、maf、crewai） | ✅ |
| USE_MOCK_SEARCH + duckduckgo | ✅ |
| pytest（3 项） | ✅ |
| GitHub Actions smoke | ✅ |
| CONTRIBUTING / agent.json / requirements-lock | ✅ |
| Ollama 默认模型 qwen2.5:7b 拉取 | ⬜ 需本机 `pull-models.ps1` |
| .NET / Maven 真机 | ⬜ 本机未安装 SDK |
| Haystack / DSPy / ADK | ⬜ |
| 对比报告 COMPARISON_REPORT | ⬜ |

---

## 近期 Sprint

### Sprint A — 真机跑通

- [x] **A0** `scripts/bootstrap.ps1`、`scripts/check-ollama.ps1`
- [ ] **A1** `pull-models.ps1` 拉取 `qwen2.5:7b` 到 `./models/ollama`
- [ ] **A2** 三框架非 fallback（需 A1 或 `$env:OLLAMA_MODEL=已有模型`）
- [ ] **A3** 安装 .NET 8 SDK → `dotnet run`
- [ ] **A4** 安装 Maven + JDK 17 → `mvn exec:java`
- [x] **A5** smoke 基线 → `docs/smoke-log.txt`、`docs/benchmarks.md`

### Sprint B — 对比可信

- [x] **B1** `shared/schema/research_output.json`
- [x] **B2** smoke + `python/scripts/validate_stdout.py`
- [x] **B3** `docs/benchmarks.md` 自动生成
- [ ] **B4** 回填矩阵实测列（在默认模型就绪后重跑 smoke）

---

## P0 — 环境与工程化

- [x] `scripts/bootstrap.ps1`
- [x] `python/requirements-lock.txt`
- [ ] OpenTelemetry / logfire 版本冲突（`pip check`）
- [x] `.github/workflows/smoke.yml`
- [x] `.env.example` + USE_MOCK_SEARCH 说明

---

## P1 — 基准任务深化

- [x] `python/langgraph/crew_research.py`
- [x] `python/ag2/crew_research.py`
- [x] `python/maf/crew_research.py`
- [x] `llm_agents_common/search.py` + `duckduckgo_search.py`
- [x] `config/agent.json`

---

## P2～P5（未开始）

见历史版本清单：Haystack、DSPy、checkpoint、HITL、COMPARISON_REPORT 等。

---

## 本机下一步（推荐顺序）

```powershell
. .\scripts\setup-ollama.ps1
.\scripts\pull-models.ps1          # 或 $env:OLLAMA_MODEL = "nemotron-3-super:cloud"
.\scripts\run-all-smoke.ps1
```

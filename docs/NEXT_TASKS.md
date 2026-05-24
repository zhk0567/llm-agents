# 后续任务清单

## 已完成

- Sprint A/B、P1–P3、Haystack/DSPy/HITL、TS 真连
- smoke-live + 矩阵实测（nemotron-3-super:cloud）
- Google ADK Java demo（mock fallback 无 GOOGLE_API_KEY）
- install-toolchain.ps1、wait-and-smoke.ps1

## 待办（需本机）

- [ ] `qwen2.5:7b` 拉取完成：`.\scripts\wait-and-smoke.ps1` 或 `pull-models.ps1`
- [ ] `install-toolchain.ps1` → `verify-toolchain.ps1` 全绿
- [ ] ADK + Gemini：设置 `GOOGLE_API_KEY` 后重跑 `java/google-adk`

## 常用命令

```powershell
.\scripts\install-toolchain.ps1 -WhatIf
.\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud
.\scripts\wait-and-smoke.ps1 -Model qwen2.5:7b
```

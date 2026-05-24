# 后续任务清单

## 已完成

- 真机 smoke-live（Python 12/13 OK @ nemotron-3-super:cloud）
- TS JSON 解析增强 + 工具结果合成兜底
- verify-toolchain.ps1、CONFIG / INSTALL_TOOLCHAIN

## 待 push

```powershell
git push origin main   # cd592f9 + 本批
```

## 待办

- [ ] pull `qwen2.5:7b` 并重跑 smoke
- [ ] 安装 .NET / Maven
- [ ] Google ADK 可运行 demo

## 命令

```powershell
.\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud
.\scripts\verify-toolchain.ps1
```

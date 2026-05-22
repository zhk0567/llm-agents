# TopicResearchAgent — 统一基准任务

所有框架实现同一业务逻辑，便于横向对比。

## 输入

- 命令行参数或 stdin：主题字符串，例如 `Rust 与 Go 在 CLI 工具中的取舍`

## 工具：`search_topic(topic: str)`

- 使用 **本地 mock**（见 `shared/tools/mock_search.py` 及各语言等价实现）
- 返回固定结构的 JSON 字符串（模拟检索结果）

## 输出

结构化 JSON，字段：

```json
{
  "topic": "<用户主题>",
  "bullets": ["要点1", "要点2", "要点3"],
  "summary": "一两段总结"
}
```

## 模型

- 默认：`config/ollama.json` 中的 `default_model`（`qwen2.5:7b`）
- 连接：`http://127.0.0.1:11434/v1`，OpenAI 兼容模式

## 扩展：ResearchCrew（多 Agent）

- `Researcher`：调用 `search_topic`，整理要点
- `Writer`：根据要点生成最终 JSON 输出
- 适用于 CrewAI、AG2、MAF 等多 Agent 框架

## 验收

从仓库根目录（PowerShell）：

```powershell
cd python\langgraph
..\..\.venv\Scripts\python main.py "测试主题"
```

应打印合法 JSON 到 stdout。

# 配置说明

## config/ollama.json

| 字段 | 说明 |
|------|------|
| `host` | Ollama HTTP 地址（无 `/v1`） |
| `base_url` | OpenAI 兼容端点 |
| `default_model` | 默认聊天模型 |
| `fallback_model` | `pull-models.ps1` 备选拉取 |

环境变量覆盖：`OLLAMA_MODEL` 优先于 `default_model`。

## config/agent.json

| 字段 | 说明 |
|------|------|
| `max_retries` | LLM 重试次数（LangGraph 等已接入） |
| `timeout_seconds` | 请求超时（秒） |
| `default_topic` | 无命令行参数时的默认主题 |
| `use_mock_search` | `true` 用 mock；`false` 用 DuckDuckGo |

环境变量：

- `USE_MOCK_SEARCH=0` → 真实检索（需 `pip install duckduckgo-search`）
- `AGENT_TIMEOUT_SECONDS=180`

## 示例

```powershell
$env:OLLAMA_MODEL = "nemotron-3-super:cloud"
$env:USE_MOCK_SEARCH = "1"
cd python\langgraph
..\.venv\Scripts\python main.py
```

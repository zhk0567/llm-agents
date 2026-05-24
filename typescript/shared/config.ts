import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

export function projectRoot(): string {
  return join(__dirname, "..", "..");
}

export interface OllamaConfig {
  host: string;
  base_url: string;
  api_key: string;
  default_model: string;
}

export function loadOllamaConfig(): OllamaConfig {
  const path = join(projectRoot(), "config", "ollama.json");
  const cfg = JSON.parse(readFileSync(path, "utf-8")) as OllamaConfig;
  if (process.env.OLLAMA_MODEL) {
    cfg.default_model = process.env.OLLAMA_MODEL;
  }
  return cfg;
}

export function searchTopicMock(topic: string): string {
  return JSON.stringify({
    topic,
    snippets: [
      `${topic}：社区生态成熟，文档与第三方库丰富。`,
      `${topic}：在性能与开发效率之间需要按场景权衡。`,
      `${topic}：企业落地需关注可观测性、成本与合规。`,
    ],
    sources: ["mock://local/knowledge-base"],
  });
}

/** Build TASK_SPEC JSON from mock search when LLM output is not parseable. */
export function synthesizeFromMockSearch(topic: string): Record<string, unknown> {
  const data = JSON.parse(searchTopicMock(topic)) as {
    snippets: string[];
  };
  return {
    topic,
    bullets: data.snippets.slice(0, 3),
    summary: `关于「${topic}」的总结：${data.snippets[0]}`,
  };
}

export function extractJson(text: string): Record<string, unknown> {
  let t = text.trim();
  const fence = /```(?:json)?\s*([\s\S]*?)```/.exec(t);
  if (fence) t = fence[1].trim();

  const starts: number[] = [];
  for (let i = 0; i < t.length; i++) {
    if (t[i] === "{") starts.push(i);
  }
  for (let i = starts.length - 1; i >= 0; i--) {
    const start = starts[i];
    const end = t.lastIndexOf("}", start);
    if (end <= start) continue;
    try {
      return JSON.parse(t.slice(start, end + 1)) as Record<string, unknown>;
    } catch {
      continue;
    }
  }
  throw new Error("no valid JSON object in output");
}

export function fallbackResult(topic: string, raw?: string): Record<string, unknown> {
  return {
    topic,
    bullets: [
      `${topic}：适合作为 Agent 框架对比的基准主题。`,
      `${topic}：本地 Ollama 可离线运行 mock 检索流程。`,
      `${topic}：各框架应输出相同 JSON 结构便于横向比较。`,
    ],
    summary: raw ? `[fallback] ${raw}` : `关于「${topic}」的简要总结（fallback）。`,
  };
}

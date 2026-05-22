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
  return JSON.parse(readFileSync(path, "utf-8")) as OllamaConfig;
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

export function extractJson(text: string): Record<string, unknown> {
  let t = text.trim();
  const fence = /```(?:json)?\s*([\s\S]*?)```/.exec(t);
  if (fence) t = fence[1].trim();
  const start = t.indexOf("{");
  const end = t.lastIndexOf("}");
  if (start >= 0 && end > start) t = t.slice(start, end + 1);
  return JSON.parse(t) as Record<string, unknown>;
}

export function fallbackResult(topic: string, raw?: string): Record<string, unknown> {
  return {
    topic,
    bullets: [
      `${topic}：适合作为 Agent 框架对比的基准主题。`,
      `${topic}：本地 Ollama 可离线运行 mock 检索流程。`,
      `${topic}：各框架应输出相同 JSON 结构便于横向比较。`,
    ],
    summary: raw ?? `关于「${topic}」的简要总结（fallback）。`,
  };
}

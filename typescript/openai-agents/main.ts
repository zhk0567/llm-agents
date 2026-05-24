import OpenAI from "openai";
import { Agent, run, tool } from "@openai/agents";
import { z } from "zod";
import {
  extractJson,
  fallbackResult,
  loadOllamaConfig,
  searchTopicMock,
  synthesizeFromMockSearch,
} from "../shared/config.js";

const topic = process.argv.slice(2).join(" ") || "AI Agent 框架选型";
const cfg = loadOllamaConfig();

process.env.OPENAI_API_KEY = cfg.api_key;
process.env.OPENAI_BASE_URL = cfg.base_url;

const client = new OpenAI({
  apiKey: cfg.api_key,
  baseURL: cfg.base_url,
});

const searchTopicTool = tool({
  name: "search_topic",
  description: "Search for information about a topic",
  parameters: z.object({ topic: z.string() }),
  execute: async ({ topic: t }) => searchTopicMock(t),
});

const agent = new Agent({
  name: "researcher",
  instructions:
    "必须先调用 search_topic，然后只输出 JSON：topic, bullets(3条), summary。",
  model: cfg.default_model,
  tools: [searchTopicTool],
  client,
});

function parseOutput(text: string): Record<string, unknown> {
  try {
    return extractJson(text);
  } catch {
    return synthesizeFromMockSearch(topic);
  }
}

try {
  const result = await run(agent, `研究主题：${topic}`);
  const text =
    typeof result.finalOutput === "string"
      ? result.finalOutput
      : JSON.stringify(result.finalOutput);
  console.log(JSON.stringify(parseOutput(text), null, 2));
} catch (e) {
  console.log(JSON.stringify(fallbackResult(topic, String(e)), null, 2));
}

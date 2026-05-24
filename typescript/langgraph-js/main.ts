import { HumanMessage } from "@langchain/core/messages";
import { tool } from "@langchain/core/tools";
import { ChatOllama } from "@langchain/ollama";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
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

const searchTopic = tool(
  async ({ topic: t }: { topic: string }) => searchTopicMock(t),
  {
    name: "search_topic",
    description: "Search for information about a topic",
    schema: z.object({ topic: z.string() }),
  }
);

const llm = new ChatOllama({
  model: cfg.default_model,
  baseUrl: cfg.host,
  temperature: 0.2,
});

const agent = createReactAgent({ llm, tools: [searchTopic] });

const prompt = `研究主题：${topic}
1. 必须调用 search_topic 工具
2. 最后一条消息只输出 JSON：{"topic":"...","bullets":["","",""],"summary":"..."}
不要 markdown，不要其它文字。`;

function parseOutput(text: string): Record<string, unknown> {
  try {
    return extractJson(text);
  } catch {
  }
  const usedTool = text.includes("search_topic") || text.includes("mock://");
  if (usedTool) return synthesizeFromMockSearch(topic);
  throw new Error("no valid JSON object in output");
}

try {
  const result = await agent.invoke({
    messages: [new HumanMessage(prompt)],
  });
  const last = result.messages[result.messages.length - 1];
  const text = typeof last.content === "string" ? last.content : JSON.stringify(last.content);
  const allText = result.messages.map((m) => JSON.stringify(m)).join("\n");
  try {
    console.log(JSON.stringify(parseOutput(text), null, 2));
  } catch {
    console.log(JSON.stringify(parseOutput(allText), null, 2));
  }
} catch (e) {
  console.log(JSON.stringify(fallbackResult(topic, String(e)), null, 2));
}

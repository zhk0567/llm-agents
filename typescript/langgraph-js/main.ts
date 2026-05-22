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
1. 调用 search_topic 工具
2. 输出 JSON：{"topic":"...","bullets":["","",""],"summary":"..."}
只输出 JSON，不要 markdown。`;

try {
  const result = await agent.invoke({
    messages: [new HumanMessage(prompt)],
  });
  const last = result.messages[result.messages.length - 1];
  const text = typeof last.content === "string" ? last.content : JSON.stringify(last.content);
  console.log(JSON.stringify(extractJson(text), null, 2));
} catch (e) {
  console.log(JSON.stringify(fallbackResult(topic, String(e)), null, 2));
}

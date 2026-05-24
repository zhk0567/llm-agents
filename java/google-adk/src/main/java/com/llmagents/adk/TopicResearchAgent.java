package com.llmagents.adk;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.FunctionTool;

import java.util.Map;

/** ADK LlmAgent + search_topic tool (Gemini when GOOGLE_API_KEY is set). */
public final class TopicResearchAgent {

    public static final BaseAgent ROOT = build();

    private static BaseAgent build() {
        return LlmAgent.builder()
                .name("topic-research-agent")
                .description("Research a topic and output structured JSON")
                .instruction("""
                    You are a research assistant.
                    1. Call search_topic with the user topic.
                    2. Output JSON only: {"topic":"...","bullets":["a","b","c"],"summary":"..."}
                    """)
                .model(System.getenv().getOrDefault("ADK_MODEL", "gemini-2.0-flash"))
                .tools(FunctionTool.create(TopicResearchAgent.class, "searchTopic"))
                .build();
    }

    @Schema(description = "Search for information about a topic")
    public static Map<String, String> searchTopic(
            @Schema(name = "topic", description = "Research topic") String topic) {
        return Map.of("result", MockSearch.searchTopic(topic));
    }

    private TopicResearchAgent() {}
}

package com.llmagents.adk;

import com.google.adk.agents.RunConfig;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import io.reactivex.rxjava3.core.Flowable;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class TopicResearchApp {

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Pattern FENCE = Pattern.compile("```(?:json)?\\s*([\\s\\S]*?)```");

    public static void main(String[] args) throws Exception {
        String topic = args.length > 0 ? String.join(" ", args) : defaultTopic();
        String apiKey = System.getenv("GOOGLE_API_KEY");
        if (apiKey == null || apiKey.isBlank()) {
            System.out.println(GSON.toJson(mockResult(topic, "[fallback] GOOGLE_API_KEY not set; ADK requires Gemini or configure Models & Auth for Ollama")));
            return;
        }
        RunConfig runConfig = RunConfig.builder().build();
        InMemoryRunner runner = new InMemoryRunner(TopicResearchAgent.ROOT);
        Session session = runner.sessionService()
                .createSession(runner.appName(), "smoke-user")
                .blockingGet();
        Content userMsg = Content.fromParts(Part.fromText("研究主题：" + topic));
        Flowable<Event> events = runner.runAsync(session.userId(), session.id(), userMsg, runConfig);
        StringBuilder sb = new StringBuilder();
        events.blockingForEach(event -> {
            if (event.finalResponse()) {
                sb.append(event.stringifyContent());
            }
        });
        try {
            System.out.println(GSON.toJson(parseJson(sb.toString())));
        } catch (Exception ex) {
            System.out.println(GSON.toJson(mockResult(topic, ex.getMessage())));
        }
    }

    private static String defaultTopic() throws Exception {
        Path root = findProjectRoot();
        String json = Files.readString(root.resolve("config").resolve("agent.json"), StandardCharsets.UTF_8);
        Matcher m = Pattern.compile("\"default_topic\"\\s*:\\s*\"([^\"]+)\"").matcher(json);
        return m.find() ? m.group(1) : "AI Agent 框架选型";
    }

    private static Path findProjectRoot() {
        Path dir = Path.of(".").toAbsolutePath().normalize();
        for (int i = 0; i < 8; i++) {
            if (Files.exists(dir.resolve("config").resolve("agent.json"))) {
                return dir;
            }
            Path parent = dir.getParent();
            if (parent == null) break;
            dir = parent;
        }
        return Path.of(".").toAbsolutePath().normalize().getParent().getParent().getParent();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> parseJson(String text) {
        String t = text.trim();
        Matcher m = FENCE.matcher(t);
        if (m.find()) t = m.group(1).trim();
        int start = t.indexOf('{');
        int end = t.lastIndexOf('}');
        if (start >= 0 && end > start) t = t.substring(start, end + 1);
        return GSON.fromJson(t, Map.class);
    }

    private static Map<String, Object> mockResult(String topic, String summary) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("topic", topic);
        out.put("bullets", List.of(
                topic + "：适合作为 Agent 框架对比的基准主题。",
                topic + "：本地 mock 检索已对齐 TASK_SPEC。",
                topic + "：设置 GOOGLE_API_KEY 可启用 ADK + Gemini。"
        ));
        out.put("summary", summary);
        return out;
    }
}

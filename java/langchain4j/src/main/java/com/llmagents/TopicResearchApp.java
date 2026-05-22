package com.llmagents;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.service.AiServices;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class TopicResearchApp {

    interface ResearchAssistant {
        String research(String topic);
    }

    static class ResearchTools {
        @Tool("Search for information about a topic")
        String searchTopic(String topic) {
            return MockSearch.searchTopic(topic);
        }
    }

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Pattern FENCE = Pattern.compile("```(?:json)?\\s*([\\s\\S]*?)```");

    private static Path findProjectRoot() throws Exception {
        Path dir = Path.of(".").toAbsolutePath().normalize();
        for (int i = 0; i < 8; i++) {
            if (Files.exists(dir.resolve("config").resolve("ollama.json"))) {
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

    private static Map<String, Object> fallback(String topic, String raw) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("topic", topic);
        out.put("bullets", List.of(
                topic + "：适合作为 Agent 框架对比的基准主题。",
                topic + "：本地 Ollama 可离线运行 mock 检索流程。",
                topic + "：各框架应输出相同 JSON 结构便于横向比较。"
        ));
        out.put("summary", raw != null ? raw : "关于「" + topic + "」的简要总结（fallback）。");
        return out;
    }

    public static void main(String[] args) throws Exception {
        String topic = args.length > 0 ? String.join(" ", args) : "AI Agent 框架选型";
        Path root = findProjectRoot();
        OllamaConfig cfg = OllamaConfig.load(root);

        ChatLanguageModel model = OllamaChatModel.builder()
                .baseUrl(cfg.host())
                .modelName(cfg.defaultModel())
                .temperature(0.2)
                .build();

        ResearchAssistant assistant = AiServices.builder(ResearchAssistant.class)
                .chatLanguageModel(model)
                .tools(new ResearchTools())
                .build();

        String prompt = """
                研究主题：%s
                1. 调用 searchTopic 工具
                2. 只输出 JSON：{"topic":"...","bullets":["a","b","c"],"summary":"..."}
                """.formatted(topic);

        try {
            String raw = assistant.research(prompt);
            System.out.println(GSON.toJson(parseJson(raw)));
        } catch (Exception ex) {
            System.out.println(GSON.toJson(fallback(topic, ex.getMessage())));
        }
    }
}

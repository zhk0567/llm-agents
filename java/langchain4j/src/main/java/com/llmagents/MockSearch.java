package com.llmagents;

import com.google.gson.Gson;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class MockSearch {
    private static final Gson GSON = new Gson();

    private MockSearch() {}

    public static String searchTopic(String topic) {
        Map<String, Object> payload = new LinkedHashMap<>();
        payload.put("topic", topic);
        payload.put("snippets", List.of(
                topic + "：社区生态成熟，文档与第三方库丰富。",
                topic + "：在性能与开发效率之间需要按场景权衡。",
                topic + "：企业落地需关注可观测性、成本与合规。"
        ));
        payload.put("sources", List.of("mock://local/knowledge-base"));
        return GSON.toJson(payload);
    }
}

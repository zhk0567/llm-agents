package com.llmagents;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.nio.file.Files;
import java.nio.file.Path;

public record OllamaConfig(String host, String baseUrl, String apiKey, String defaultModel) {
    private static final Gson GSON = new Gson();

    public static OllamaConfig load(Path projectRoot) throws Exception {
        String json = Files.readString(projectRoot.resolve("config").resolve("ollama.json"));
        JsonObject o = GSON.fromJson(json, JsonObject.class);
        return new OllamaConfig(
                o.get("host").getAsString(),
                o.get("base_url").getAsString(),
                o.get("api_key").getAsString(),
                o.get("default_model").getAsString()
        );
    }
}

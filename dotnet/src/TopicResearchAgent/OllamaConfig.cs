using System.Text.Json;

namespace TopicResearchAgent;

public sealed class OllamaConfig
{
    public string Host { get; init; } = "http://127.0.0.1:11434";
    public string BaseUrl { get; init; } = "http://127.0.0.1:11434/v1";
    public string ApiKey { get; init; } = "ollama";
    public string DefaultModel { get; init; } = "nemotron-3-super:cloud";

    public static OllamaConfig Load(string projectRoot)
    {
        var path = Path.Combine(projectRoot, "config", "ollama.json");
        var json = File.ReadAllText(path);
        using var doc = JsonDocument.Parse(json);
        var root = doc.RootElement;
        return new OllamaConfig
        {
            Host = root.GetProperty("host").GetString() ?? "http://127.0.0.1:11434",
            BaseUrl = root.GetProperty("base_url").GetString() ?? "http://127.0.0.1:11434/v1",
            ApiKey = root.GetProperty("api_key").GetString() ?? "ollama",
            DefaultModel = root.GetProperty("default_model").GetString() ?? "qwen2.5:7b",
        };
    }
}

using System.ComponentModel;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;

namespace TopicResearchAgent;

public sealed class ResearchPlugin
{
    [KernelFunction, Description("Search for information about a topic")]
    public string SearchTopic(
        [Description("Research topic")] string topic) =>
        MockSearch.SearchTopic(topic);
}

internal static class Program
{
    private static string ProjectRoot()
    {
        var dir = AppContext.BaseDirectory;
        for (var i = 0; i < 6; i++)
        {
            if (File.Exists(Path.Combine(dir, "config", "ollama.json")))
                return dir;
            var parent = Directory.GetParent(dir);
            if (parent is null) break;
            dir = parent.FullName;
        }
        return Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));
    }

    private static Dictionary<string, object> Fallback(string topic, string? raw = null) => new()
    {
        ["topic"] = topic,
        ["bullets"] = new[]
        {
            $"{topic}：适合作为 Agent 框架对比的基准主题。",
            $"{topic}：本地 Ollama 可离线运行 mock 检索流程。",
            $"{topic}：各框架应输出相同 JSON 结构便于横向比较。",
        },
        ["summary"] = raw ?? $"关于「{topic}」的简要总结（fallback）。",
    };

    private static Dictionary<string, object> ParseJson(string text)
    {
        text = text.Trim();
        var fence = Regex.Match(text, @"```(?:json)?\s*([\s\S]*?)```");
        if (fence.Success) text = fence.Groups[1].Value.Trim();
        var start = text.IndexOf('{');
        var end = text.LastIndexOf('}');
        if (start >= 0 && end > start) text = text[start..(end + 1)];
        return JsonSerializer.Deserialize<Dictionary<string, object>>(text)
               ?? throw new InvalidOperationException("Invalid JSON");
    }

    public static async Task Main(string[] args)
    {
        var topic = args.Length > 0 ? string.Join(' ', args) : "AI Agent 框架选型";
        var root = ProjectRoot();
        var cfg = OllamaConfig.Load(root);

#pragma warning disable SKEXP0010
        var kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(
                modelId: cfg.DefaultModel,
                apiKey: cfg.ApiKey,
                endpoint: new Uri(cfg.BaseUrl))
            .Build();
#pragma warning restore SKEXP0010

        kernel.ImportPluginFromType<ResearchPlugin>();

        var prompt = $"""
            研究主题：{topic}
            调用 SearchTopic 工具，然后只输出 JSON：
            {{"topic":"...","bullets":["a","b","c"],"summary":"..."}}
            """;

        try
        {
            var result = await kernel.InvokePromptAsync(prompt);
            var parsed = ParseJson(result.ToString());
            Console.WriteLine(JsonSerializer.Serialize(parsed, new JsonSerializerOptions { WriteIndented = true }));
        }
        catch (Exception ex)
        {
            var fallback = Fallback(topic, ex.Message);
            Console.WriteLine(JsonSerializer.Serialize(fallback, new JsonSerializerOptions { WriteIndented = true }));
        }
    }
}

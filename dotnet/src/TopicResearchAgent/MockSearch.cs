using System.Text.Json;

namespace TopicResearchAgent;

public static class MockSearch
{
    public static string SearchTopic(string topic)
    {
        var payload = new
        {
            topic,
            snippets = new[]
            {
                $"{topic}：社区生态成熟，文档与第三方库丰富。",
                $"{topic}：在性能与开发效率之间需要按场景权衡。",
                $"{topic}：企业落地需关注可观测性、成本与合规。",
            },
            sources = new[] { "mock://local/knowledge-base" },
        };
        return JsonSerializer.Serialize(payload);
    }
}

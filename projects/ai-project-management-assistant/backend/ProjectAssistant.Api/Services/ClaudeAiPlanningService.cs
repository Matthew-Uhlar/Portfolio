using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Services;

/// <summary>Settings for the hosted LLM, read from the "Ai" configuration section.</summary>
public class AiOptions
{
    public const string SectionName = "Ai";

    /// <summary>Anthropic API key. Leave empty to use the built-in rules engine.</summary>
    public string ApiKey { get; set; } = "";

    public string Model { get; set; } = "claude-haiku-4-5";

    public string BaseUrl { get; set; } = "https://api.anthropic.com/";

    public int MaxTokens { get; set; } = 1500;

    public int TimeoutSeconds { get; set; } = 30;

    public bool IsConfigured => !string.IsNullOrWhiteSpace(ApiKey);
}

/// <summary>
/// Planning assistant backed by Anthropic's Claude Messages API. Each feature asks the model
/// for JSON in the same shape the frontend already uses. If the API is down, slow, out of
/// credit or returns something unusable, the request is answered by the rules engine instead,
/// so the assistant never breaks the app.
/// </summary>
public class ClaudeAiPlanningService(
    HttpClient http,
    AiOptions options,
    LocalAiPlanningService fallback,
    ILogger<ClaudeAiPlanningService> logger) : IAiPlanningService
{
    private static readonly int[] ValidPoints = [1, 2, 3, 5, 8, 13];

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        Converters = { new JsonStringEnumConverter() }
    };

    private const string SystemPrompt =
        "You are an experienced Agile coach and Scrum Master helping a software team plan work. " +
        "Be specific to the project details you are given, practical and concise. " +
        "Reply with a single JSON object that matches the requested shape exactly. " +
        "Do not wrap it in markdown and do not add any text before or after it.";

    public string Provider => $"Claude ({options.Model})";

    public async Task<StoryGenerationResponse> GenerateStoriesAsync(Project project, string featureIdea, CancellationToken cancellationToken = default)
    {
        var prompt = $$"""
            Break this feature idea into 3 to 6 user stories for the project below.

            Project: {{project.Name}}
            Description: {{project.Description}}
            Goal: {{project.Goal}}
            Feature idea: {{featureIdea}}

            JSON shape:
            {
              "overview": "two sentences on how you split the work",
              "stories": [
                {
                  "title": "short imperative title",
                  "description": "As a <role>, I want <goal> so that <benefit>.",
                  "acceptanceCriteria": "testable criteria in one or two sentences",
                  "priority": "Low | Medium | High | Critical",
                  "suggestedPoints": 1 | 2 | 3 | 5 | 8 | 13
                }
              ]
            }
            """;

        return await AskAsync(
            prompt,
            json =>
            {
                var result = json.Deserialize<StoryGenerationResponse>(JsonOptions);
                if (result is null || string.IsNullOrWhiteSpace(result.Overview) || result.Stories is not { Count: > 0 })
                {
                    return null;
                }

                var stories = result.Stories
                    .Where(story => !string.IsNullOrWhiteSpace(story.Title))
                    .Select(story => story with { SuggestedPoints = NearestValidPoints(story.SuggestedPoints) })
                    .ToList();

                return stories.Count == 0 ? null : result with { Stories = stories };
            },
            () => fallback.GenerateStories(project, featureIdea),
            cancellationToken);
    }

    public async Task<StoryPointResponse> SuggestPointsAsync(string title, string description, string acceptanceCriteria, CancellationToken cancellationToken = default)
    {
        var prompt = $$"""
            Estimate story points for this work item using the Fibonacci scale (1, 2, 3, 5, 8, 13).
            Consider complexity, uncertainty and the amount of work. Suggest splitting anything you rate 13.

            Title: {{title}}
            Description: {{description}}
            Acceptance criteria: {{acceptanceCriteria}}

            JSON shape:
            { "suggestedPoints": 5, "reasoning": "one or two sentences explaining the estimate" }
            """;

        return await AskAsync(
            prompt,
            json =>
            {
                var result = json.Deserialize<StoryPointResponse>(JsonOptions);
                return result is null || string.IsNullOrWhiteSpace(result.Reasoning)
                    ? null
                    : result with { SuggestedPoints = NearestValidPoints(result.SuggestedPoints) };
            },
            () => fallback.SuggestPoints(title, description, acceptanceCriteria),
            cancellationToken);
    }

    public async Task<SprintSummaryResponse> SummarizeSprintAsync(Sprint sprint, IReadOnlyList<WorkItem> items, CancellationToken cancellationToken = default)
    {
        var prompt = $$"""
            Summarize this sprint for a stakeholder update.

            Sprint: {{sprint.Name}}
            Goal: {{sprint.Goal}}
            Dates: {{sprint.StartDate:yyyy-MM-dd}} to {{sprint.EndDate:yyyy-MM-dd}}
            Work items:
            {{DescribeItems(items)}}

            JSON shape:
            {
              "summary": "two or three sentences on progress toward the goal, using the real numbers",
              "highlights": ["three short factual highlights"],
              "nextSteps": ["two or three concrete next steps"]
            }
            """;

        return await AskAsync(
            prompt,
            json =>
            {
                var result = json.Deserialize<SprintSummaryResponse>(JsonOptions);
                return result is null || string.IsNullOrWhiteSpace(result.Summary) || result.Highlights is null || result.NextSteps is null
                    ? null
                    : result;
            },
            () => fallback.SummarizeSprint(sprint, items),
            cancellationToken);
    }

    public async Task<RiskReviewResponse> ReviewRisksAsync(Project project, IReadOnlyList<WorkItem> items, CancellationToken cancellationToken = default)
    {
        var prompt = $$"""
            Review this project's backlog for delivery risks such as unowned work, oversized items,
            review bottlenecks, open critical work and unclear acceptance criteria.

            Project: {{project.Name}}
            Goal: {{project.Goal}}
            Work items:
            {{DescribeItems(items)}}

            JSON shape:
            {
              "overallRisk": "Low | Medium | High",
              "risks": ["each risk in one sentence, naming the items involved"],
              "recommendations": ["one concrete recommendation per risk"]
            }
            """;

        return await AskAsync(
            prompt,
            json =>
            {
                var result = json.Deserialize<RiskReviewResponse>(JsonOptions);
                if (result is null || result.Risks is null || result.Recommendations is null)
                {
                    return null;
                }

                var overall = result.OverallRisk?.Trim() switch
                {
                    { } value when value.Equals("high", StringComparison.OrdinalIgnoreCase) => "High",
                    { } value when value.Equals("medium", StringComparison.OrdinalIgnoreCase) => "Medium",
                    { } value when value.Equals("low", StringComparison.OrdinalIgnoreCase) => "Low",
                    _ => null
                };

                return overall is null ? null : result with { OverallRisk = overall };
            },
            () => fallback.ReviewRisks(project, items),
            cancellationToken);
    }

    /// <summary>
    /// Sends one prompt, parses the JSON reply and validates it. Any failure is logged and
    /// answered by the rules engine so callers always get a usable response.
    /// </summary>
    private async Task<T> AskAsync<T>(
        string prompt,
        Func<JsonNode, T?> parse,
        Func<T> useFallback,
        CancellationToken cancellationToken) where T : class
    {
        try
        {
            var text = await SendAsync(prompt, cancellationToken);
            var json = JsonNode.Parse(ExtractJson(text))
                ?? throw new JsonException("The model returned empty JSON.");

            var result = parse(json);
            if (result is not null)
            {
                return result;
            }

            logger.LogWarning("The model reply did not match the expected shape for {Type}. Using the rules engine.", typeof(T).Name);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            throw;
        }
        catch (Exception exception)
        {
            logger.LogWarning(exception, "The LLM request for {Type} failed. Using the rules engine.", typeof(T).Name);
        }

        return useFallback();
    }

    private async Task<string> SendAsync(string prompt, CancellationToken cancellationToken)
    {
        var body = new JsonObject
        {
            ["model"] = options.Model,
            ["max_tokens"] = options.MaxTokens,
            ["system"] = SystemPrompt,
            ["messages"] = new JsonArray
            {
                new JsonObject { ["role"] = "user", ["content"] = prompt }
            }
        };

        using var request = new HttpRequestMessage(HttpMethod.Post, "v1/messages")
        {
            Content = new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json")
        };
        request.Headers.Add("x-api-key", options.ApiKey);
        request.Headers.Add("anthropic-version", "2023-06-01");
        request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        using var timeout = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeout.CancelAfter(TimeSpan.FromSeconds(options.TimeoutSeconds));

        using var response = await http.SendAsync(request, timeout.Token);
        var payload = await response.Content.ReadAsStringAsync(timeout.Token);

        if (!response.IsSuccessStatusCode)
        {
            throw new HttpRequestException($"Anthropic API returned {(int)response.StatusCode}: {Truncate(payload, 300)}");
        }

        var reply = JsonNode.Parse(payload);
        var text = reply?["content"]?.AsArray()
            .Where(block => block?["type"]?.GetValue<string>() == "text")
            .Select(block => block!["text"]!.GetValue<string>())
            .FirstOrDefault();

        return string.IsNullOrWhiteSpace(text)
            ? throw new JsonException("The Anthropic response had no text content.")
            : text;
    }

    /// <summary>Pulls the JSON object out of a reply, tolerating markdown fences or stray text.</summary>
    public static string ExtractJson(string text)
    {
        var start = text.IndexOf('{');
        var end = text.LastIndexOf('}');
        return start >= 0 && end > start
            ? text[start..(end + 1)]
            : throw new JsonException("The model reply did not contain a JSON object.");
    }

    public static int NearestValidPoints(int points) =>
        ValidPoints.OrderBy(valid => Math.Abs(valid - points)).ThenBy(valid => valid).First();

    private static string DescribeItems(IReadOnlyList<WorkItem> items)
    {
        if (items.Count == 0)
        {
            return "(no work items)";
        }

        var lines = items.Take(60).Select(item =>
            $"- #{item.Id} \"{item.Title}\" | status {item.Status} | priority {item.Priority} | " +
            $"{item.StoryPoints} pts | assignee {(string.IsNullOrWhiteSpace(item.Assignee) ? "none" : item.Assignee)}");

        var description = string.Join('\n', lines);
        return items.Count > 60 ? $"{description}\n(and {items.Count - 60} more)" : description;
    }

    private static string Truncate(string value, int length) =>
        value.Length <= length ? value : value[..length] + "...";
}

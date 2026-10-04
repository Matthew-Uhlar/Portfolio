using System.Net;
using System.Text.Json;
using System.Text.Json.Nodes;
using Microsoft.Extensions.Logging.Abstractions;
using ProjectAssistant.Api.Models;
using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Tests;

public class ClaudeAiPlanningServiceTests
{
    private readonly Project project = new() { Id = 1, Name = "Inventory", Goal = "Replace spreadsheets" };

    [Fact]
    public async Task GenerateStories_SendsAuthenticatedRequestAndParsesReply()
    {
        var handler = new FakeHandler(_ => Reply("""
            ```json
            {"overview":"Split by workflow.","stories":[
              {"title":"Scan item","description":"As staff...","acceptanceCriteria":"Count updates","priority":"high","suggestedPoints":4}
            ]}
            ```
            """));

        var result = await CreateService(handler).GenerateStoriesAsync(project, "QR scanning");

        var story = Assert.Single(result.Stories);
        Assert.Equal(WorkItemPriority.High, story.Priority);
        Assert.Equal(3, story.SuggestedPoints);
        Assert.Equal("https://api.anthropic.com/v1/messages", handler.LastRequest!.RequestUri!.ToString());
        Assert.Equal("test-key", handler.LastRequest.Headers.GetValues("x-api-key").Single());
        Assert.Equal("2023-06-01", handler.LastRequest.Headers.GetValues("anthropic-version").Single());

        var body = JsonNode.Parse(handler.LastBody!)!;
        Assert.Equal("claude-haiku-4-5", body["model"]!.GetValue<string>());
        Assert.Contains("QR scanning", body["messages"]![0]!["content"]!.GetValue<string>());
    }

    [Fact]
    public async Task ApiError_FallsBackToRulesEngine()
    {
        var handler = new FakeHandler(_ => new HttpResponseMessage(HttpStatusCode.TooManyRequests) { Content = new StringContent("rate limited") });

        var result = await CreateService(handler).GenerateStoriesAsync(project, "QR scanning");

        Assert.Equal(new LocalAiPlanningService().GenerateStories(project, "QR scanning").Overview, result.Overview);
    }

    [Fact]
    public async Task ReplyWithoutJson_FallsBackToRulesEngine()
    {
        var handler = new FakeHandler(_ => Reply("Sorry, I can't help with that."));

        var result = await CreateService(handler).SuggestPointsAsync("Fix label", "Change text", "Matches design");

        Assert.Equal(2, result.SuggestedPoints);
    }

    [Fact]
    public async Task ReviewRisks_NormalizesRiskLevel()
    {
        var handler = new FakeHandler(_ => Reply("""{"overallRisk":"MEDIUM","risks":["Two items have no owner"],"recommendations":["Assign owners"]}"""));

        var result = await CreateService(handler).ReviewRisksAsync(project, [new WorkItem { Id = 7, Title = "Scan" }]);

        Assert.Equal("Medium", result.OverallRisk);
        Assert.Contains("#7", handler.LastBody);
    }

    [Fact]
    public async Task ReviewRisks_WithUnknownRiskLevel_FallsBack()
    {
        var handler = new FakeHandler(_ => Reply("""{"overallRisk":"Severe","risks":["x"],"recommendations":["y"]}"""));

        var result = await CreateService(handler).ReviewRisksAsync(project, []);

        Assert.Equal("Low", result.OverallRisk);
    }

    [Fact]
    public async Task SummarizeSprint_ParsesReply()
    {
        var handler = new FakeHandler(_ => Reply("""{"summary":"On track.","highlights":["3 done"],"nextSteps":["Finish review"]}"""));

        var result = await CreateService(handler).SummarizeSprintAsync(new Sprint { Name = "Sprint 1" }, []);

        Assert.Equal("On track.", result.Summary);
        Assert.Equal(new[] { "3 done" }, result.Highlights);
    }

    [Fact]
    public async Task CallerCancellation_IsNotSwallowed()
    {
        using var cancelled = new CancellationTokenSource();
        cancelled.Cancel();
        var handler = new FakeHandler(_ => Reply("{}"));

        await Assert.ThrowsAnyAsync<OperationCanceledException>(() =>
            CreateService(handler).SuggestPointsAsync("a", "b", "c", cancelled.Token));
    }

    [Theory]
    [InlineData(0, 1)]
    [InlineData(4, 3)]
    [InlineData(6, 5)]
    [InlineData(10, 8)]
    [InlineData(40, 13)]
    public void NearestValidPoints_SnapsToFibonacciScale(int input, int expected) =>
        Assert.Equal(expected, ClaudeAiPlanningService.NearestValidPoints(input));

    [Fact]
    public void ExtractJson_IgnoresSurroundingText() =>
        Assert.Equal("""{"a":1}""", ClaudeAiPlanningService.ExtractJson("Here you go: {\"a\":1} Thanks"));

    [Fact]
    public void ExtractJson_ThrowsWhenThereIsNoObject() =>
        Assert.Throws<JsonException>(() => ClaudeAiPlanningService.ExtractJson("nothing"));

    private static ClaudeAiPlanningService CreateService(FakeHandler handler) =>
        new(
            new HttpClient(handler) { BaseAddress = new Uri("https://api.anthropic.com/") },
            new AiOptions { ApiKey = "test-key" },
            new LocalAiPlanningService(),
            NullLogger<ClaudeAiPlanningService>.Instance);

    private static HttpResponseMessage Reply(string text) => new(HttpStatusCode.OK)
    {
        Content = new StringContent(JsonSerializer.Serialize(new { content = new[] { new { type = "text", text } } }))
    };

    private sealed class FakeHandler(Func<HttpRequestMessage, HttpResponseMessage> respond) : HttpMessageHandler
    {
        public HttpRequestMessage? LastRequest { get; private set; }
        public string? LastBody { get; private set; }

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            cancellationToken.ThrowIfCancellationRequested();
            LastRequest = request;
            LastBody = request.Content is null ? null : await request.Content.ReadAsStringAsync(cancellationToken);
            return respond(request);
        }
    }
}

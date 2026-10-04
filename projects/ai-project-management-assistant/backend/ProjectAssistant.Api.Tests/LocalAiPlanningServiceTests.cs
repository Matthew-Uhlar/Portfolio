using ProjectAssistant.Api.Models;
using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Tests;

public class LocalAiPlanningServiceTests
{
    private readonly LocalAiPlanningService service = new();
    private readonly Project project = new() { Id = 1, Name = "Inventory", Goal = "Replace spreadsheets" };

    [Fact]
    public void GenerateStories_ReturnsWorkflowPermissionsAuditAndTests()
    {
        var result = service.GenerateStories(project, "QR code scanning.");

        Assert.Equal(4, result.Stories.Count);
        Assert.All(result.Stories, story => Assert.Contains("qr code scanning", story.Title));
        Assert.DoesNotContain(result.Stories, story => story.Title.EndsWith('.'));
    }

    [Fact]
    public void GenerateStories_HandlesBlankIdea()
    {
        var result = service.GenerateStories(project, "   ");

        Assert.Contains("the requested feature", result.Stories[0].Title);
    }

    [Theory]
    [InlineData("Fix label", "Change button text", "Text matches design", 2)]
    [InlineData("Add login", "Role permission checks", "Users see their data", 3)]
    [InlineData("Sync", "External api webhook with database migration", "Data syncs", 8)]
    public void SuggestPoints_ScalesWithComplexity(string title, string description, string criteria, int expected)
    {
        var result = service.SuggestPoints(title, description, criteria);

        Assert.Equal(expected, result.SuggestedPoints);
        Assert.False(string.IsNullOrWhiteSpace(result.Reasoning));
    }

    [Fact]
    public void SummarizeSprint_UsesStoryPointsForCompletion()
    {
        var sprint = new Sprint { Name = "Sprint 1", Goal = "Ship login" };
        var items = new List<WorkItem>
        {
            new() { Status = WorkItemStatus.Done, StoryPoints = 3 },
            new() { Status = WorkItemStatus.Review, StoryPoints = 1 }
        };

        var result = service.SummarizeSprint(sprint, items);

        Assert.Contains("75%", result.Summary);
        Assert.Contains("1 of 2 work items are complete.", result.Highlights);
        Assert.Contains(result.NextSteps, step => step.Contains("reviews", StringComparison.OrdinalIgnoreCase));
    }

    [Fact]
    public void SummarizeSprint_WithNoItems_DoesNotDivideByZero()
    {
        var result = service.SummarizeSprint(new Sprint { Name = "Empty" }, []);

        Assert.Contains("0%", result.Summary);
    }

    [Fact]
    public void ReviewRisks_FlagsOpenCriticalWorkAsHighRisk()
    {
        var items = new List<WorkItem>
        {
            new() { Priority = WorkItemPriority.Critical, Status = WorkItemStatus.InProgress, Assignee = "Sam", StoryPoints = 3 },
            new() { Status = WorkItemStatus.Backlog, Assignee = "", StoryPoints = 8 }
        };

        var result = service.ReviewRisks(project, items);

        Assert.Equal("High", result.OverallRisk);
        Assert.Contains(result.Risks, risk => risk.Contains("do not have an assignee"));
        Assert.Contains(result.Risks, risk => risk.Contains("eight points"));
    }

    [Fact]
    public void ReviewRisks_WithHealthyBacklog_IsLowRisk()
    {
        var items = new List<WorkItem> { new() { Assignee = "Sam", StoryPoints = 2 } };

        var result = service.ReviewRisks(project, items);

        Assert.Equal("Low", result.OverallRisk);
        Assert.Single(result.Risks);
    }
}

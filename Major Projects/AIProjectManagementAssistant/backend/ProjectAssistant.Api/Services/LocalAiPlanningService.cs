using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Services;

public class LocalAiPlanningService : IAiPlanningService
{
    public StoryGenerationResponse GenerateStories(Project project, string featureIdea)
    {
        var cleanIdea = featureIdea.Trim().TrimEnd('.');
        var subject = string.IsNullOrWhiteSpace(cleanIdea) ? "the requested feature" : cleanIdea;

        var stories = new List<GeneratedStory>
        {
            new(
                $"Create the main {subject.ToLowerInvariant()} workflow",
                $"As a team member, I want to use {subject.ToLowerInvariant()} so I can complete the process without leaving the application.",
                "The user can open the feature, complete the required fields and save a valid result. Clear validation appears when required information is missing.",
                WorkItemPriority.High,
                5),
            new(
                $"Add permissions for {subject.ToLowerInvariant()}",
                $"As an administrator, I want access to be based on user roles so sensitive actions stay limited to the right people.",
                "Authorized users can complete the action. Unauthorized users receive a clear message and the API returns the correct status code.",
                WorkItemPriority.High,
                3),
            new(
                $"Track activity for {subject.ToLowerInvariant()}",
                $"As an administrator, I want important changes recorded so I can understand what happened and who made the change.",
                "The system records the action, user and timestamp. The activity can be reviewed from the application.",
                WorkItemPriority.Medium,
                3),
            new(
                $"Test the {subject.ToLowerInvariant()} experience",
                $"As a product owner, I want the feature covered by tests so future changes do not break the main workflow.",
                "Unit tests cover the main business rules and an integration test covers the successful API workflow.",
                WorkItemPriority.Medium,
                3)
        };

        return new StoryGenerationResponse(
            $"I broke the idea into a main workflow, access control, traceability and testing. That gives the team a usable first version without ignoring the work needed around it.",
            stories);
    }

    public StoryPointResponse SuggestPoints(string title, string description, string acceptanceCriteria)
    {
        var combined = $"{title} {description} {acceptanceCriteria}".ToLowerInvariant();
        var score = 2;

        if (combined.Length > 220) score++;
        if (ContainsAny(combined, "database", "migration", "schema", "integration")) score += 2;
        if (ContainsAny(combined, "authentication", "permission", "security", "role")) score += 2;
        if (ContainsAny(combined, "external", "api", "webhook", "third-party")) score += 2;
        if (ContainsAny(combined, "real-time", "offline", "sync", "upload")) score += 2;

        var points = score switch
        {
            <= 2 => 2,
            <= 4 => 3,
            <= 6 => 5,
            <= 8 => 8,
            _ => 13
        };

        var reasoning = points <= 3
            ? "This looks fairly contained and should not require many dependencies."
            : points <= 5
                ? "This has a moderate amount of logic or integration work. I would plan time for testing and edge cases."
                : "This touches several parts of the system or has added uncertainty. It may be worth splitting before the sprint starts.";

        return new StoryPointResponse(points, reasoning);
    }

    public SprintSummaryResponse SummarizeSprint(Sprint sprint, IReadOnlyList<WorkItem> items)
    {
        var done = items.Count(item => item.Status == WorkItemStatus.Done);
        var active = items.Count(item => item.Status is WorkItemStatus.InProgress or WorkItemStatus.Review);
        var totalPoints = items.Sum(item => item.StoryPoints);
        var donePoints = items.Where(item => item.Status == WorkItemStatus.Done).Sum(item => item.StoryPoints);
        var completion = totalPoints == 0 ? 0 : (int)Math.Round(donePoints * 100d / totalPoints);

        var highlights = new List<string>
        {
            $"{done} of {items.Count} work items are complete.",
            $"{donePoints} of {totalPoints} planned story points are finished.",
            $"{active} work items are currently active or waiting for review."
        };

        var nextSteps = new List<string>();
        if (items.Any(item => item.Status == WorkItemStatus.Review))
            nextSteps.Add("Finish reviews early so completed work does not sit at the end of the sprint.");
        if (items.Any(item => item.Priority == WorkItemPriority.Critical && item.Status != WorkItemStatus.Done))
            nextSteps.Add("Confirm ownership and a clear plan for the remaining critical work.");
        if (completion < 50)
            nextSteps.Add("Review the remaining scope and move lower-priority work if the sprint goal is at risk.");
        if (nextSteps.Count == 0)
            nextSteps.Add("Keep the current focus and confirm that completed work meets the acceptance criteria.");

        return new SprintSummaryResponse(
            $"{sprint.Name} is about {completion}% complete based on story points. The team has made progress but should keep the remaining work focused on the sprint goal: {sprint.Goal}",
            highlights,
            nextSteps);
    }

    public RiskReviewResponse ReviewRisks(Project project, IReadOnlyList<WorkItem> items)
    {
        var risks = new List<string>();
        var recommendations = new List<string>();

        var unassigned = items.Count(item => string.IsNullOrWhiteSpace(item.Assignee) && item.Status != WorkItemStatus.Done);
        var largeItems = items.Count(item => item.StoryPoints >= 8 && item.Status != WorkItemStatus.Done);
        var stalledReview = items.Count(item => item.Status == WorkItemStatus.Review);
        var criticalOpen = items.Count(item => item.Priority == WorkItemPriority.Critical && item.Status != WorkItemStatus.Done);

        if (unassigned > 0)
        {
            risks.Add($"{unassigned} open work items do not have an assignee.");
            recommendations.Add("Assign an owner before pulling those items into active sprint work.");
        }

        if (largeItems > 0)
        {
            risks.Add($"{largeItems} open work items are estimated at eight points or more.");
            recommendations.Add("Split large work into smaller pieces with separate acceptance criteria.");
        }

        if (stalledReview > 2)
        {
            risks.Add("Several items are waiting for review which could create a bottleneck.");
            recommendations.Add("Set a daily review window or rotate a clear reviewer for the sprint.");
        }

        if (criticalOpen > 0)
        {
            risks.Add($"{criticalOpen} critical work items are still open.");
            recommendations.Add("Confirm dependencies and make critical work visible in the daily standup.");
        }

        if (risks.Count == 0)
        {
            risks.Add("No major planning risks stand out in the current project data.");
            recommendations.Add("Keep work items small and continue updating ownership and status as the project changes.");
        }

        var overall = criticalOpen > 0 || largeItems > 2 ? "High"
            : risks.Count >= 3 ? "Medium"
            : "Low";

        return new RiskReviewResponse(overall, risks, recommendations);
    }

    private static bool ContainsAny(string value, params string[] terms) =>
        terms.Any(value.Contains);
}

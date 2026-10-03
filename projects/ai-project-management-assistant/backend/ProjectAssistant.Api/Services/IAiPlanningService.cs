using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Services;

public interface IAiPlanningService
{
    StoryGenerationResponse GenerateStories(Project project, string featureIdea);
    StoryPointResponse SuggestPoints(string title, string description, string acceptanceCriteria);
    SprintSummaryResponse SummarizeSprint(Sprint sprint, IReadOnlyList<WorkItem> items);
    RiskReviewResponse ReviewRisks(Project project, IReadOnlyList<WorkItem> items);
}

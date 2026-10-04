using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Services;

/// <summary>
/// Everything the planning assistant can do. Controllers only depend on this interface,
/// so the rules engine and the hosted LLM can be swapped with configuration alone.
/// </summary>
public interface IAiPlanningService
{
    /// <summary>Human-readable name of the engine answering requests.</summary>
    string Provider { get; }

    Task<StoryGenerationResponse> GenerateStoriesAsync(Project project, string featureIdea, CancellationToken cancellationToken = default);
    Task<StoryPointResponse> SuggestPointsAsync(string title, string description, string acceptanceCriteria, CancellationToken cancellationToken = default);
    Task<SprintSummaryResponse> SummarizeSprintAsync(Sprint sprint, IReadOnlyList<WorkItem> items, CancellationToken cancellationToken = default);
    Task<RiskReviewResponse> ReviewRisksAsync(Project project, IReadOnlyList<WorkItem> items, CancellationToken cancellationToken = default);
}

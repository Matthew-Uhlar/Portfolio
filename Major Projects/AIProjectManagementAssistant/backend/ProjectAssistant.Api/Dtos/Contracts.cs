using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Dtos;

public record LoginRequest(string Email, string Password);
public record LoginResponse(string Token, string Name, string Role);

public record ProjectRequest(string Name, string Description, string Goal);
public record SprintRequest(
    int ProjectId,
    string Name,
    string Goal,
    DateTime StartDate,
    DateTime EndDate,
    bool IsActive);

public record WorkItemRequest(
    int ProjectId,
    int? SprintId,
    string Title,
    string Description,
    string AcceptanceCriteria,
    WorkItemStatus Status,
    WorkItemPriority Priority,
    int StoryPoints,
    string Assignee);

public record StatusUpdateRequest(WorkItemStatus Status);

public record UserStoryGenerationRequest(int ProjectId, string FeatureIdea);
public record StoryPointRequest(string Title, string Description, string AcceptanceCriteria);
public record SprintSummaryRequest(int SprintId);
public record RiskReviewRequest(int ProjectId);

public record GeneratedStory(
    string Title,
    string Description,
    string AcceptanceCriteria,
    WorkItemPriority Priority,
    int SuggestedPoints);

public record StoryGenerationResponse(string Overview, IReadOnlyList<GeneratedStory> Stories);
public record StoryPointResponse(int SuggestedPoints, string Reasoning);
public record SprintSummaryResponse(string Summary, IReadOnlyList<string> Highlights, IReadOnlyList<string> NextSteps);
public record RiskReviewResponse(string OverallRisk, IReadOnlyList<string> Risks, IReadOnlyList<string> Recommendations);

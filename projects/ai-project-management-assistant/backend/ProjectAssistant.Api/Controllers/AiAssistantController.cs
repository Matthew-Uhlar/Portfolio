using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/ai")]
public class AiAssistantController(AppDbContext db, IAiPlanningService ai) : ControllerBase
{
    [HttpGet("status")]
    public ActionResult<AiStatusResponse> Status() => Ok(new AiStatusResponse(ai.Provider));

    [HttpPost("generate-stories")]
    public async Task<ActionResult<StoryGenerationResponse>> GenerateStories(UserStoryGenerationRequest request, CancellationToken cancellationToken)
    {
        var project = await db.Projects.FindAsync(request.ProjectId);
        if (project is null)
        {
            return NotFound(new { message = "I could not find that project." });
        }

        return Ok(await ai.GenerateStoriesAsync(project, request.FeatureIdea, cancellationToken));
    }

    [HttpPost("suggest-points")]
    public async Task<ActionResult<StoryPointResponse>> SuggestPoints(StoryPointRequest request, CancellationToken cancellationToken)
    {
        return Ok(await ai.SuggestPointsAsync(request.Title, request.Description, request.AcceptanceCriteria, cancellationToken));
    }

    [HttpPost("sprint-summary")]
    public async Task<ActionResult<SprintSummaryResponse>> SprintSummary(SprintSummaryRequest request, CancellationToken cancellationToken)
    {
        var sprint = await db.Sprints.FindAsync(request.SprintId);
        if (sprint is null)
        {
            return NotFound(new { message = "I could not find that sprint." });
        }

        var items = await db.WorkItems.Where(item => item.SprintId == request.SprintId).ToListAsync(cancellationToken);
        return Ok(await ai.SummarizeSprintAsync(sprint, items, cancellationToken));
    }

    [HttpPost("risk-review")]
    public async Task<ActionResult<RiskReviewResponse>> RiskReview(RiskReviewRequest request, CancellationToken cancellationToken)
    {
        var project = await db.Projects.FindAsync(request.ProjectId);
        if (project is null)
        {
            return NotFound(new { message = "I could not find that project." });
        }

        var items = await db.WorkItems.Where(item => item.ProjectId == request.ProjectId).ToListAsync(cancellationToken);
        return Ok(await ai.ReviewRisksAsync(project, items, cancellationToken));
    }
}

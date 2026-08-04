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
    [HttpPost("generate-stories")]
    public async Task<ActionResult<StoryGenerationResponse>> GenerateStories(UserStoryGenerationRequest request)
    {
        var project = await db.Projects.FindAsync(request.ProjectId);
        if (project is null)
        {
            return NotFound(new { message = "I could not find that project." });
        }

        return Ok(ai.GenerateStories(project, request.FeatureIdea));
    }

    [HttpPost("suggest-points")]
    public ActionResult<StoryPointResponse> SuggestPoints(StoryPointRequest request)
    {
        return Ok(ai.SuggestPoints(request.Title, request.Description, request.AcceptanceCriteria));
    }

    [HttpPost("sprint-summary")]
    public async Task<ActionResult<SprintSummaryResponse>> SprintSummary(SprintSummaryRequest request)
    {
        var sprint = await db.Sprints.FindAsync(request.SprintId);
        if (sprint is null)
        {
            return NotFound(new { message = "I could not find that sprint." });
        }

        var items = await db.WorkItems.Where(item => item.SprintId == request.SprintId).ToListAsync();
        return Ok(ai.SummarizeSprint(sprint, items));
    }

    [HttpPost("risk-review")]
    public async Task<ActionResult<RiskReviewResponse>> RiskReview(RiskReviewRequest request)
    {
        var project = await db.Projects.FindAsync(request.ProjectId);
        if (project is null)
        {
            return NotFound(new { message = "I could not find that project." });
        }

        var items = await db.WorkItems.Where(item => item.ProjectId == request.ProjectId).ToListAsync();
        return Ok(ai.ReviewRisks(project, items));
    }
}

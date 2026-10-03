using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/sprints")]
public class SprintsController(AppDbContext db) : ControllerBase
{
    [HttpGet("project/{projectId:int}")]
    public async Task<ActionResult<IEnumerable<Sprint>>> GetForProject(int projectId)
    {
        return Ok(await db.Sprints
            .Where(item => item.ProjectId == projectId)
            .OrderByDescending(item => item.StartDate)
            .ToListAsync());
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<ActionResult<Sprint>> Create(SprintRequest request)
    {
        var sprint = new Sprint
        {
            ProjectId = request.ProjectId,
            Name = request.Name.Trim(),
            Goal = request.Goal.Trim(),
            StartDate = request.StartDate.ToUniversalTime(),
            EndDate = request.EndDate.ToUniversalTime(),
            IsActive = request.IsActive
        };

        db.Sprints.Add(sprint);
        await db.SaveChangesAsync();
        return Ok(sprint);
    }
}

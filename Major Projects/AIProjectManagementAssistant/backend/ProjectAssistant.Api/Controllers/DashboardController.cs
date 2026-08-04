using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/dashboard")]
public class DashboardController(AppDbContext db) : ControllerBase
{
    [HttpGet("{projectId:int}")]
    public async Task<IActionResult> Get(int projectId)
    {
        var items = await db.WorkItems.Where(item => item.ProjectId == projectId).ToListAsync();
        var activeSprint = await db.Sprints.FirstOrDefaultAsync(item => item.ProjectId == projectId && item.IsActive);

        return Ok(new
        {
            totalItems = items.Count,
            completedItems = items.Count(item => item.Status == WorkItemStatus.Done),
            activeItems = items.Count(item => item.Status is WorkItemStatus.InProgress or WorkItemStatus.Review),
            backlogPoints = items.Where(item => item.Status == WorkItemStatus.Backlog).Sum(item => item.StoryPoints),
            criticalItems = items.Count(item => item.Priority == WorkItemPriority.Critical && item.Status != WorkItemStatus.Done),
            activeSprint
        });
    }
}

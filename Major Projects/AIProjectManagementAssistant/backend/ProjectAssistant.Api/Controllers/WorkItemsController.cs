using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/work-items")]
public class WorkItemsController(AppDbContext db) : ControllerBase
{
    [HttpGet("project/{projectId:int}")]
    public async Task<ActionResult<IEnumerable<WorkItem>>> GetForProject(int projectId)
    {
        return Ok(await db.WorkItems
            .Where(item => item.ProjectId == projectId)
            .OrderByDescending(item => item.Priority)
            .ThenBy(item => item.Id)
            .ToListAsync());
    }

    [HttpPost]
    public async Task<ActionResult<WorkItem>> Create(WorkItemRequest request)
    {
        var item = new WorkItem
        {
            ProjectId = request.ProjectId,
            SprintId = request.SprintId,
            Title = request.Title.Trim(),
            Description = request.Description.Trim(),
            AcceptanceCriteria = request.AcceptanceCriteria.Trim(),
            Status = request.Status,
            Priority = request.Priority,
            StoryPoints = request.StoryPoints,
            Assignee = request.Assignee.Trim()
        };

        db.WorkItems.Add(item);
        await db.SaveChangesAsync();
        return Ok(item);
    }

    [HttpPatch("{id:int}/status")]
    public async Task<ActionResult<WorkItem>> UpdateStatus(int id, StatusUpdateRequest request)
    {
        var item = await db.WorkItems.FindAsync(id);
        if (item is null)
        {
            return NotFound();
        }

        item.Status = request.Status;
        await db.SaveChangesAsync();
        return Ok(item);
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
    {
        var item = await db.WorkItems.FindAsync(id);
        if (item is null)
        {
            return NotFound();
        }

        db.WorkItems.Remove(item);
        await db.SaveChangesAsync();
        return NoContent();
    }
}

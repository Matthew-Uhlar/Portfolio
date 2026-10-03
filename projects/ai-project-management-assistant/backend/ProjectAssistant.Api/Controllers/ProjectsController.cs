using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/projects")]
public class ProjectsController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Project>>> GetAll()
    {
        return Ok(await db.Projects.OrderBy(project => project.Name).ToListAsync());
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<Project>> Get(int id)
    {
        var project = await db.Projects
            .Include(item => item.Sprints)
            .Include(item => item.WorkItems)
            .SingleOrDefaultAsync(item => item.Id == id);

        return project is null ? NotFound() : Ok(project);
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<ActionResult<Project>> Create(ProjectRequest request)
    {
        var project = new Project
        {
            Name = request.Name.Trim(),
            Description = request.Description.Trim(),
            Goal = request.Goal.Trim()
        };

        db.Projects.Add(project);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = project.Id }, project);
    }
}

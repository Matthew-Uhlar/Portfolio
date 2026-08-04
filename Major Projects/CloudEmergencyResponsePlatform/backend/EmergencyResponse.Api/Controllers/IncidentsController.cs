using System.Security.Claims;
using EmergencyResponse.Api.Data;
using EmergencyResponse.Api.Dtos;
using EmergencyResponse.Api.Hubs;
using EmergencyResponse.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/incidents")]
public class IncidentsController(AppDbContext db, IHubContext<IncidentHub> hub) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Incident>>> GetAll()
    {
        return Ok(await db.Incidents
            .Include(item => item.Assignments)
            .ThenInclude(item => item.ResponseUnit)
            .Include(item => item.Activity)
            .OrderByDescending(item => item.Severity)
            .ThenByDescending(item => item.ReportedAt)
            .ToListAsync());
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<Incident>> Get(int id)
    {
        var incident = await db.Incidents
            .Include(item => item.Assignments)
            .ThenInclude(item => item.ResponseUnit)
            .Include(item => item.Activity.OrderByDescending(activity => activity.CreatedAt))
            .SingleOrDefaultAsync(item => item.Id == id);

        return incident is null ? NotFound() : Ok(incident);
    }

    [Authorize(Roles = "Dispatcher")]
    [HttpPost]
    public async Task<ActionResult<Incident>> Create(IncidentRequest request)
    {
        var incident = new Incident
        {
            Title = request.Title.Trim(),
            Description = request.Description.Trim(),
            Address = request.Address.Trim(),
            Latitude = request.Latitude,
            Longitude = request.Longitude,
            Severity = request.Severity
        };

        db.Incidents.Add(incident);
        await db.SaveChangesAsync();

        await AddActivity(incident.Id, "Incident was created.");
        await hub.Clients.All.SendAsync("IncidentCreated", incident);

        return CreatedAtAction(nameof(Get), new { id = incident.Id }, incident);
    }

    [HttpPatch("{id:int}/status")]
    public async Task<ActionResult<Incident>> UpdateStatus(int id, IncidentStatusRequest request)
    {
        var incident = await db.Incidents.FindAsync(id);
        if (incident is null)
        {
            return NotFound();
        }

        incident.Status = request.Status;
        incident.ClosedAt = request.Status == IncidentStatus.Closed ? DateTime.UtcNow : null;

        await db.SaveChangesAsync();

        var note = string.IsNullOrWhiteSpace(request.Note)
            ? $"Status changed to {request.Status}."
            : request.Note.Trim();

        await AddActivity(id, note);
        await hub.Clients.All.SendAsync("IncidentUpdated", incident);

        return Ok(incident);
    }

    [HttpPost("{id:int}/activity")]
    public async Task<IActionResult> AddNote(int id, ActivityRequest request)
    {
        if (!await db.Incidents.AnyAsync(item => item.Id == id))
        {
            return NotFound();
        }

        var activity = await AddActivity(id, request.Message.Trim());
        await hub.Clients.Group($"incident-{id}").SendAsync("ActivityAdded", activity);

        return Ok(activity);
    }

    private async Task<IncidentActivity> AddActivity(int incidentId, string message)
    {
        var activity = new IncidentActivity
        {
            IncidentId = incidentId,
            Message = message,
            CreatedBy = User.FindFirstValue(ClaimTypes.Name) ?? "Unknown user"
        };

        db.IncidentActivities.Add(activity);
        await db.SaveChangesAsync();
        return activity;
    }
}

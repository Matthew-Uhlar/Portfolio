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

[Authorize(Roles = "Dispatcher")]
[ApiController]
[Route("api/assignments")]
public class AssignmentsController(AppDbContext db, IHubContext<IncidentHub> hub) : ControllerBase
{
    [HttpPost]
    public async Task<ActionResult<IncidentAssignment>> Assign(AssignmentRequest request)
    {
        var incident = await db.Incidents.FindAsync(request.IncidentId);
        var unit = await db.ResponseUnits.FindAsync(request.ResponseUnitId);

        if (incident is null || unit is null)
        {
            return NotFound(new { message = "The incident or response unit could not be found." });
        }

        var alreadyAssigned = await db.IncidentAssignments.AnyAsync(item =>
            item.IncidentId == request.IncidentId &&
            item.ResponseUnitId == request.ResponseUnitId &&
            item.ClearedAt == null);

        if (alreadyAssigned)
        {
            return BadRequest(new { message = "That unit is already assigned to the incident." });
        }

        var assignment = new IncidentAssignment
        {
            IncidentId = request.IncidentId,
            ResponseUnitId = request.ResponseUnitId
        };

        unit.Status = UnitStatus.Assigned;
        incident.Status = incident.Status == IncidentStatus.Reported
            ? IncidentStatus.Dispatched
            : incident.Status;

        db.IncidentAssignments.Add(assignment);
        db.IncidentActivities.Add(new IncidentActivity
        {
            IncidentId = request.IncidentId,
            Message = $"{unit.UnitName} was assigned.",
            CreatedBy = User.FindFirstValue(ClaimTypes.Name) ?? "Unknown user"
        });

        await db.SaveChangesAsync();
        await hub.Clients.All.SendAsync("AssignmentCreated", new
        {
            assignment.Id,
            assignment.IncidentId,
            assignment.ResponseUnitId,
            unit.UnitName
        });

        return Ok(assignment);
    }

    [HttpPatch("{id:int}/clear")]
    public async Task<IActionResult> Clear(int id)
    {
        var assignment = await db.IncidentAssignments
            .Include(item => item.ResponseUnit)
            .SingleOrDefaultAsync(item => item.Id == id);

        if (assignment is null)
        {
            return NotFound();
        }

        assignment.ClearedAt = DateTime.UtcNow;
        if (assignment.ResponseUnit is not null)
        {
            assignment.ResponseUnit.Status = UnitStatus.Available;
        }

        await db.SaveChangesAsync();
        await hub.Clients.All.SendAsync("AssignmentCleared", id);

        return NoContent();
    }
}

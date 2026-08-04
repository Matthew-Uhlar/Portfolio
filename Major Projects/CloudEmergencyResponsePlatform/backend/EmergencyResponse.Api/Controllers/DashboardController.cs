using EmergencyResponse.Api.Data;
using EmergencyResponse.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/dashboard")]
public class DashboardController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var incidents = await db.Incidents.ToListAsync();
        var units = await db.ResponseUnits.ToListAsync();

        return Ok(new
        {
            activeIncidents = incidents.Count(item => item.Status != IncidentStatus.Closed),
            criticalIncidents = incidents.Count(item => item.Severity == IncidentSeverity.Critical && item.Status != IncidentStatus.Closed),
            availableUnits = units.Count(item => item.Status == UnitStatus.Available),
            assignedUnits = units.Count(item => item.Status is UnitStatus.Assigned or UnitStatus.EnRoute or UnitStatus.OnScene),
            recentlyReported = incidents
                .Where(item => item.ReportedAt >= DateTime.UtcNow.AddHours(-24))
                .OrderByDescending(item => item.ReportedAt)
                .Take(5)
        });
    }
}

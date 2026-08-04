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
[Route("api/units")]
public class UnitsController(AppDbContext db, IHubContext<IncidentHub> hub) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<ResponseUnit>>> GetAll()
    {
        return Ok(await db.ResponseUnits.OrderBy(item => item.UnitName).ToListAsync());
    }

    [Authorize(Roles = "Dispatcher")]
    [HttpPost]
    public async Task<ActionResult<ResponseUnit>> Create(UnitRequest request)
    {
        var unit = new ResponseUnit
        {
            UnitName = request.UnitName.Trim(),
            UnitType = request.UnitType.Trim(),
            RadioCode = request.RadioCode.Trim(),
            CurrentLocation = request.CurrentLocation.Trim()
        };

        db.ResponseUnits.Add(unit);
        await db.SaveChangesAsync();
        return Ok(unit);
    }

    [HttpPatch("{id:int}/status")]
    public async Task<ActionResult<ResponseUnit>> UpdateStatus(int id, UnitStatusRequest request)
    {
        var unit = await db.ResponseUnits.FindAsync(id);
        if (unit is null)
        {
            return NotFound();
        }

        unit.Status = request.Status;
        unit.CurrentLocation = request.CurrentLocation.Trim();
        await db.SaveChangesAsync();

        await hub.Clients.All.SendAsync("UnitUpdated", unit);
        return Ok(unit);
    }
}

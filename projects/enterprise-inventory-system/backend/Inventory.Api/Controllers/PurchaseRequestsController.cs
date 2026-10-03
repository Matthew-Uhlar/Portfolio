using System.Security.Claims;
using Inventory.Api.Data;
using Inventory.Api.Dtos;
using Inventory.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Controllers;

[ApiController, Route("api/requests"), Authorize]
public class PurchaseRequestsController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var q=db.PurchaseRequests.Include(x=>x.RequestedByUser).AsNoTracking();
        if(!User.IsInRole("Admin")){var id=int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);q=q.Where(x=>x.RequestedByUserId==id);}
        return Ok(await q.OrderByDescending(x=>x.CreatedAt).Select(x=>new{x.Id,x.ItemName,x.Quantity,x.Reason,Status=x.Status.ToString(),RequestedBy=x.RequestedByUser!.Name,x.CreatedAt,x.ReviewedAt,x.ReviewNotes}).ToListAsync());
    }
    [HttpPost]
    public async Task<IActionResult> Create(PurchaseRequestCreate r)
    {
        var id=int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);var pr=new PurchaseRequest{ItemName=r.ItemName,Quantity=r.Quantity,Reason=r.Reason,RequestedByUserId=id};db.Add(pr);await db.SaveChangesAsync();return Ok(pr);
    }
    [HttpPut("{id:int}/review"), Authorize(Roles="Admin")]
    public async Task<IActionResult> Review(int id, PurchaseRequestReview r)
    {
        var pr=await db.PurchaseRequests.FindAsync(id);if(pr is null)return NotFound();if(!Enum.TryParse<RequestStatus>(r.Status,true,out var status))return BadRequest(new{message="Invalid status."});pr.Status=status;pr.ReviewNotes=r.ReviewNotes;pr.ReviewedAt=DateTime.UtcNow;await db.SaveChangesAsync();return Ok(pr);
    }
}

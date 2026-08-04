using Inventory.Api.Data;
using Inventory.Api.Dtos;
using Inventory.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Controllers;

[ApiController, Route("api/inventory"), Authorize]
public class InventoryController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Get([FromQuery] string? search)
    {
        var q = db.InventoryItems.AsNoTracking();
        if (!string.IsNullOrWhiteSpace(search)) q = q.Where(x => x.Name.Contains(search) || x.Sku.Contains(search) || x.Category.Contains(search));
        return Ok(await q.OrderBy(x => x.Name).ToListAsync());
    }

    [HttpGet("low-stock")]
    public async Task<IActionResult> LowStock() => Ok(await db.InventoryItems.AsNoTracking().Where(x => x.Quantity <= x.ReorderLevel).OrderBy(x => x.Quantity).ToListAsync());

    [HttpPost, Authorize(Roles = "Admin")]
    public async Task<IActionResult> Create(InventoryItemRequest request)
    {
        var item = new InventoryItem { Sku = request.Sku, Name = request.Name, Category = request.Category, Location = request.Location, Quantity = request.Quantity, ReorderLevel = request.ReorderLevel, UnitCost = request.UnitCost };
        db.InventoryItems.Add(item); await db.SaveChangesAsync(); return CreatedAtAction(nameof(Get), new { id = item.Id }, item);
    }

    [HttpPut("{id:int}"), Authorize(Roles = "Admin")]
    public async Task<IActionResult> Update(int id, InventoryItemRequest request)
    {
        var item = await db.InventoryItems.FindAsync(id); if (item is null) return NotFound();
        item.Sku=request.Sku; item.Name=request.Name; item.Category=request.Category; item.Location=request.Location; item.Quantity=request.Quantity; item.ReorderLevel=request.ReorderLevel; item.UnitCost=request.UnitCost; item.UpdatedAt=DateTime.UtcNow;
        await db.SaveChangesAsync(); return Ok(item);
    }

    [HttpDelete("{id:int}"), Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    { var item=await db.InventoryItems.FindAsync(id); if(item is null)return NotFound(); db.Remove(item); await db.SaveChangesAsync(); return NoContent(); }
}

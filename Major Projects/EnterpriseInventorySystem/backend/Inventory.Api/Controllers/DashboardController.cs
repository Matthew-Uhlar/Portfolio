using Inventory.Api.Data;
using Inventory.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Controllers;

[ApiController, Route("api/dashboard"), Authorize]
public class DashboardController(AppDbContext db):ControllerBase
{
 [HttpGet] public async Task<IActionResult> Get()=>Ok(new{
   inventoryItems=await db.InventoryItems.CountAsync(),
   lowStockItems=await db.InventoryItems.CountAsync(x=>x.Quantity<=x.ReorderLevel),
   totalInventoryValue=await db.InventoryItems.SumAsync(x=>x.Quantity*x.UnitCost),
   activeAssets=await db.Assets.CountAsync(x=>x.Status==AssetStatus.Active),
   pendingRequests=await db.PurchaseRequests.CountAsync(x=>x.Status==RequestStatus.Pending)
 });
}

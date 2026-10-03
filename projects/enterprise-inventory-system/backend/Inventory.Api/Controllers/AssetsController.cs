using Inventory.Api.Data;
using Inventory.Api.Dtos;
using Inventory.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Controllers;

[ApiController, Route("api/assets"), Authorize]
public class AssetsController(AppDbContext db) : ControllerBase
{
    [HttpGet] public async Task<IActionResult> Get() => Ok(await db.Assets.AsNoTracking().OrderBy(x=>x.AssetTag).ToListAsync());
    [HttpPost, Authorize(Roles="Admin")]
    public async Task<IActionResult> Create(AssetRequest r)
    {
        if(!Enum.TryParse<AssetStatus>(r.Status,true,out var status)) return BadRequest(new{message="Invalid status."});
        var a=new Asset{AssetTag=r.AssetTag,Name=r.Name,Category=r.Category,AssignedTo=r.AssignedTo,Location=r.Location,Status=status,PurchaseDate=r.PurchaseDate,WarrantyExpiration=r.WarrantyExpiration};
        db.Assets.Add(a); await db.SaveChangesAsync(); return Ok(a);
    }
    [HttpPut("{id:int}"), Authorize(Roles="Admin")]
    public async Task<IActionResult> Update(int id, AssetRequest r)
    {
        var a=await db.Assets.FindAsync(id); if(a is null)return NotFound(); if(!Enum.TryParse<AssetStatus>(r.Status,true,out var status))return BadRequest();
        a.AssetTag=r.AssetTag;a.Name=r.Name;a.Category=r.Category;a.AssignedTo=r.AssignedTo;a.Location=r.Location;a.Status=status;a.PurchaseDate=r.PurchaseDate;a.WarrantyExpiration=r.WarrantyExpiration;
        await db.SaveChangesAsync();return Ok(a);
    }
}

using System.Security.Claims;
using System.Text.Json;
using Inventory.Api.Controllers;
using Inventory.Api.Data;
using Inventory.Api.Dtos;
using Inventory.Api.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Tests;

public class InventoryTests
{
    [Fact]
    public async Task LowStock_ReturnsItemsAtOrBelowReorderLevel_LowestFirst()
    {
        using var db = CreateDb();
        db.InventoryItems.AddRange(
            new InventoryItem { Sku = "A", Name = "Gloves", Quantity = 5, ReorderLevel = 10 },
            new InventoryItem { Sku = "B", Name = "Wipes", Quantity = 10, ReorderLevel = 10 },
            new InventoryItem { Sku = "C", Name = "Paper", Quantity = 50, ReorderLevel = 10 });
        await db.SaveChangesAsync();

        var result = Assert.IsType<OkObjectResult>(await As(new InventoryController(db), 1, "Staff").LowStock());

        var items = Assert.IsAssignableFrom<IEnumerable<InventoryItem>>(result.Value).Select(item => item.Name);
        Assert.Equal(new[] { "Gloves", "Wipes" }, items);
    }

    [Fact]
    public async Task Search_MatchesSkuAndCategory()
    {
        using var db = CreateDb();
        db.InventoryItems.AddRange(
            new InventoryItem { Sku = "CLN-01", Name = "Wipes", Category = "Cleaning" },
            new InventoryItem { Sku = "OFF-01", Name = "Paper", Category = "Office" });
        await db.SaveChangesAsync();
        var controller = As(new InventoryController(db), 1, "Staff");

        var bySku = Assert.IsType<OkObjectResult>(await controller.Get("CLN"));
        var byCategory = Assert.IsType<OkObjectResult>(await controller.Get("Office"));

        Assert.Equal("Wipes", Assert.Single(Assert.IsAssignableFrom<IEnumerable<InventoryItem>>(bySku.Value)).Name);
        Assert.Equal("Paper", Assert.Single(Assert.IsAssignableFrom<IEnumerable<InventoryItem>>(byCategory.Value)).Name);
    }

    [Fact]
    public async Task Update_UnknownItem_ReturnsNotFound()
    {
        using var db = CreateDb();

        var result = await As(new InventoryController(db), 1, "Admin").Update(9, new InventoryItemRequest("X", "X", "X", "X", 1, 1, 1m));

        Assert.IsType<NotFoundResult>(result);
    }

    [Fact]
    public async Task PurchaseRequests_StaffSeeOnlyTheirOwn_AdminsSeeAll()
    {
        using var db = CreateDb();
        db.Users.AddRange(
            new User { Id = 1, Name = "Sam Staff", Email = "sam@example.com" },
            new User { Id = 2, Name = "Pat Staff", Email = "pat@example.com" },
            new User { Id = 3, Name = "Alex Admin", Email = "alex@example.com", Role = UserRole.Admin });
        await db.SaveChangesAsync();

        await As(new PurchaseRequestsController(db), 1, "Staff").Create(new PurchaseRequestCreate("Laptop", 1, "New hire"));
        await As(new PurchaseRequestsController(db), 2, "Staff").Create(new PurchaseRequestCreate("Monitor", 2, "Dual screens"));

        var staffView = await ItemNames(await As(new PurchaseRequestsController(db), 1, "Staff").Get());
        var adminView = await ItemNames(await As(new PurchaseRequestsController(db), 3, "Admin").Get());

        Assert.Equal(new[] { "Laptop" }, staffView);
        Assert.Equal(2, adminView.Count);
    }

    [Theory]
    [InlineData("", 1)]
    [InlineData("Laptop", 0)]
    public async Task CreatePurchaseRequest_RejectsMissingNameOrQuantity(string itemName, int quantity)
    {
        using var db = CreateDb();

        var result = await As(new PurchaseRequestsController(db), 1, "Staff").Create(new PurchaseRequestCreate(itemName, quantity, "Need it"));

        Assert.IsType<BadRequestObjectResult>(result);
        Assert.Empty(db.PurchaseRequests);
    }

    [Fact]
    public async Task Review_ApprovesAndStampsTheReview()
    {
        using var db = CreateDb();
        db.PurchaseRequests.Add(new PurchaseRequest { Id = 1, ItemName = "Laptop", Quantity = 1, RequestedByUserId = 1 });
        await db.SaveChangesAsync();

        var result = await As(new PurchaseRequestsController(db), 3, "Admin").Review(1, new PurchaseRequestReview("approved", "Within budget"));

        var request = Assert.IsType<PurchaseRequest>(Assert.IsType<OkObjectResult>(result).Value);
        Assert.Equal(RequestStatus.Approved, request.Status);
        Assert.Equal("Within budget", request.ReviewNotes);
        Assert.NotNull(request.ReviewedAt);
    }

    [Theory]
    [InlineData("Shipped")]
    [InlineData("7")]
    public async Task Review_RejectsUnknownStatus(string status)
    {
        using var db = CreateDb();
        db.PurchaseRequests.Add(new PurchaseRequest { Id = 1, ItemName = "Laptop", Quantity = 1, RequestedByUserId = 1 });
        await db.SaveChangesAsync();

        var result = await As(new PurchaseRequestsController(db), 3, "Admin").Review(1, new PurchaseRequestReview(status, null));

        Assert.IsType<BadRequestObjectResult>(result);
        Assert.Equal(RequestStatus.Pending, (await db.PurchaseRequests.FindAsync(1))!.Status);
    }

    [Theory]
    [InlineData("Lost")]
    [InlineData("12")]
    public async Task CreateAsset_RejectsUnknownStatus(string status)
    {
        using var db = CreateDb();

        var result = await As(new AssetsController(db), 3, "Admin").Create(new AssetRequest("TAG-1", "Laptop", "IT", "Sam", "Office", status, null, null));

        Assert.IsType<BadRequestObjectResult>(result);
    }

    [Fact]
    public async Task CreateAsset_AcceptsStatusInAnyCase()
    {
        using var db = CreateDb();

        var result = await As(new AssetsController(db), 3, "Admin").Create(new AssetRequest("TAG-1", "Laptop", "IT", "Sam", "Office", "maintenance", null, null));

        var asset = Assert.IsType<Asset>(Assert.IsType<OkObjectResult>(result).Value);
        Assert.Equal(AssetStatus.Maintenance, asset.Status);
    }

    private static AppDbContext CreateDb() =>
        new(new DbContextOptionsBuilder<AppDbContext>().UseInMemoryDatabase(Guid.NewGuid().ToString()).Options);

    private static T As<T>(T controller, int userId, string role) where T : ControllerBase
    {
        var identity = new ClaimsIdentity(
            new[] { new Claim(ClaimTypes.NameIdentifier, userId.ToString()), new Claim(ClaimTypes.Role, role) },
            "Test");
        controller.ControllerContext = new ControllerContext { HttpContext = new DefaultHttpContext { User = new ClaimsPrincipal(identity) } };
        return controller;
    }

    private static Task<List<string>> ItemNames(IActionResult result)
    {
        // The list endpoint returns anonymous objects, so read them the way the frontend does: as JSON.
        var json = JsonSerializer.Serialize(Assert.IsType<OkObjectResult>(result).Value);
        var names = JsonDocument.Parse(json).RootElement.EnumerateArray()
            .Select(item => item.GetProperty("ItemName").GetString()!)
            .ToList();
        return Task.FromResult(names);
    }
}

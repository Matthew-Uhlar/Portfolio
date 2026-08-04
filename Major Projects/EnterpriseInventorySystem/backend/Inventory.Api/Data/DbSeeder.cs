using Inventory.Api.Models;
using Inventory.Api.Services;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Data;

public static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db)
    {
        await db.Database.EnsureCreatedAsync();
        if (!await db.Users.AnyAsync())
        {
            db.Users.AddRange(
                new User { Name = "Admin User", Email = "admin@example.com", PasswordHash = PasswordService.Hash("Admin123!"), Role = UserRole.Admin },
                new User { Name = "Staff User", Email = "staff@example.com", PasswordHash = PasswordService.Hash("Staff123!"), Role = UserRole.Staff });
        }
        if (!await db.InventoryItems.AnyAsync())
        {
            db.InventoryItems.AddRange(
                new InventoryItem { Sku = "OFF-001", Name = "Printer Paper", Category = "Office", Location = "Supply Room", Quantity = 12, ReorderLevel = 20, UnitCost = 7.49m },
                new InventoryItem { Sku = "CLN-002", Name = "Disinfectant Wipes", Category = "Cleaning", Location = "Janitorial Closet", Quantity = 48, ReorderLevel = 24, UnitCost = 4.99m },
                new InventoryItem { Sku = "IT-003", Name = "USB-C Dock", Category = "Technology", Location = "IT Storage", Quantity = 6, ReorderLevel = 3, UnitCost = 89.00m });
        }
        if (!await db.Assets.AnyAsync())
        {
            db.Assets.AddRange(
                new Asset { AssetTag = "AST-1001", Name = "Dell Latitude Laptop", Category = "Computer", AssignedTo = "Front Office", Location = "Building A", Status = AssetStatus.Active },
                new Asset { AssetTag = "AST-1002", Name = "Epson Projector", Category = "AV", AssignedTo = "Training Room", Location = "Building B", Status = AssetStatus.Maintenance });
        }
        await db.SaveChangesAsync();
    }
}

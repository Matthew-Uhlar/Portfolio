using Inventory.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<User> Users => Set<User>();
    public DbSet<InventoryItem> InventoryItems => Set<InventoryItem>();
    public DbSet<Asset> Assets => Set<Asset>();
    public DbSet<PurchaseRequest> PurchaseRequests => Set<PurchaseRequest>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>().HasIndex(x => x.Email).IsUnique();
        modelBuilder.Entity<InventoryItem>().HasIndex(x => x.Sku).IsUnique();
        modelBuilder.Entity<Asset>().HasIndex(x => x.AssetTag).IsUnique();
        modelBuilder.Entity<InventoryItem>().Property(x => x.UnitCost).HasPrecision(12, 2);
    }
}

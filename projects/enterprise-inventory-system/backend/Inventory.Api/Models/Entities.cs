namespace Inventory.Api.Models;

public enum UserRole { Staff, Admin }
public enum RequestStatus { Pending, Approved, Rejected, Ordered, Fulfilled }
public enum AssetStatus { Active, Maintenance, Retired }

public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string PasswordHash { get; set; } = "";
    public UserRole Role { get; set; } = UserRole.Staff;
}

public class InventoryItem
{
    public int Id { get; set; }
    public string Sku { get; set; } = "";
    public string Name { get; set; } = "";
    public string Category { get; set; } = "";
    public string Location { get; set; } = "";
    public int Quantity { get; set; }
    public int ReorderLevel { get; set; }
    public decimal UnitCost { get; set; }
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

public class Asset
{
    public int Id { get; set; }
    public string AssetTag { get; set; } = "";
    public string Name { get; set; } = "";
    public string Category { get; set; } = "";
    public string AssignedTo { get; set; } = "";
    public string Location { get; set; } = "";
    public AssetStatus Status { get; set; } = AssetStatus.Active;
    public DateTime? PurchaseDate { get; set; }
    public DateTime? WarrantyExpiration { get; set; }
}

public class PurchaseRequest
{
    public int Id { get; set; }
    public string ItemName { get; set; } = "";
    public int Quantity { get; set; }
    public string Reason { get; set; } = "";
    public RequestStatus Status { get; set; } = RequestStatus.Pending;
    public int RequestedByUserId { get; set; }
    public User? RequestedByUser { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ReviewedAt { get; set; }
    public string? ReviewNotes { get; set; }
}

namespace Inventory.Api.Dtos;

public record LoginRequest(string Email, string Password);
public record LoginResponse(string Token, string Name, string Role);
public record InventoryItemRequest(string Sku, string Name, string Category, string Location, int Quantity, int ReorderLevel, decimal UnitCost);
public record AssetRequest(string AssetTag, string Name, string Category, string AssignedTo, string Location, string Status, DateTime? PurchaseDate, DateTime? WarrantyExpiration);
public record PurchaseRequestCreate(string ItemName, int Quantity, string Reason);
public record PurchaseRequestReview(string Status, string? ReviewNotes);

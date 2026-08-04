export type InventoryItem={id:number;sku:string;name:string;category:string;location:string;quantity:number;reorderLevel:number;unitCost:number;updatedAt:string};
export type Asset={id:number;assetTag:string;name:string;category:string;assignedTo:string;location:string;status:string;purchaseDate?:string;warrantyExpiration?:string};
export type PurchaseRequest={id:number;itemName:string;quantity:number;reason:string;status:string;requestedBy:string;createdAt:string;reviewNotes?:string};

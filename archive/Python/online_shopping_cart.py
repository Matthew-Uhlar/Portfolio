class ItemToPurchase:
    def __init__(self):
        self.item_name = "none"
        self.item_price = 0.0
        self.item_quantity = 0

    def print_item_cost(self):
        item_total = self.item_price * self.item_quantity
        print(
            f"{self.item_name} {self.item_quantity} @ "
            f"${self.item_price} = ${item_total}"
        )


def main():
    cart_items = []

    print("ONLINE SHOPPING CART")
    print("Enter item information. Type 'quit' as the item name when finished.\n")

    while True:
        item_name = input("Enter item name: ")

        if item_name.lower() == "quit":
            break

        item_price = float(input("Enter item price: $"))
        item_quantity = int(input("Enter item quantity: "))

        item = ItemToPurchase()
        item.item_name = item_name
        item.item_price = item_price
        item.item_quantity = item_quantity
        cart_items.append(item)

        print("Item added to cart.\n")

    total_cost = 0.0

    print("\nTOTAL COST")
    for item in cart_items:
        item.print_item_cost()
        total_cost += item.item_price * item.item_quantity

    print(f"Total: ${total_cost}")


if __name__ == "__main__":
    main()

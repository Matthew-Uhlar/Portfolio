class ItemToPurchase:
    def __init__(self):
        self.item_name = "none"
        self.item_price = 0.0
        self.item_quantity = 0
        self.item_description = "none"

    def print_item_cost(self):
        item_total = self.item_price * self.item_quantity
        print(
            f"{self.item_name} {self.item_quantity} @ "
            f"${self.item_price:.2f} = ${item_total:.2f}"
        )

    def print_item_description(self):
        print(f"{self.item_name}: {self.item_description}")


class ShoppingCart:
    def __init__(self, customer_name="none", current_date="January 1, 2020"):
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items = []

    def add_item(self, item_to_purchase):
        self.cart_items.append(item_to_purchase)

    def remove_item(self, item_name):
        for item in self.cart_items:
            if item.item_name == item_name:
                self.cart_items.remove(item)
                return
        print("Item not found in cart. Nothing removed.")

    def modify_item(self, item_to_purchase):
        for item in self.cart_items:
            if item.item_name == item_to_purchase.item_name:
                if item_to_purchase.item_description != "none":
                    item.item_description = item_to_purchase.item_description
                if item_to_purchase.item_price != 0.0:
                    item.item_price = item_to_purchase.item_price
                if item_to_purchase.item_quantity != 0:
                    item.item_quantity = item_to_purchase.item_quantity
                return
        print("Item not found in cart. Nothing modified.")

    def get_num_items_in_cart(self):
        total_quantity = 0
        for item in self.cart_items:
            total_quantity += item.item_quantity
        return total_quantity

    def get_cost_of_cart(self):
        total_cost = 0.0
        for item in self.cart_items:
            total_cost += item.item_price * item.item_quantity
        return total_cost

    def print_total(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print(f"Number of Items: {self.get_num_items_in_cart()}")

        if len(self.cart_items) == 0:
            print("SHOPPING CART IS EMPTY")
        else:
            print()
            for item in self.cart_items:
                item.print_item_cost()

        print(f"Total: ${self.get_cost_of_cart():.2f}")

    def print_descriptions(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print("Item Descriptions")

        if len(self.cart_items) == 0:
            print("SHOPPING CART IS EMPTY")
        else:
            for item in self.cart_items:
                item.print_item_description()


def print_menu(shopping_cart):
    choice = ""

    while choice != "q":
        print()
        print("MENU")
        print("a - Add item to cart")
        print("r - Remove item from cart")
        print("c - Change item quantity")
        print("i - Output items' descriptions")
        print("o - Output shopping cart")
        print("q - Quit")
        print()

        choice = input("Choose an option: ").lower()

        while choice not in ["a", "r", "c", "i", "o", "q"]:
            choice = input("Choose an option: ").lower()

        if choice == "a":
            print()
            print("ADD ITEM TO CART")
            new_item = ItemToPurchase()
            new_item.item_name = input("Enter the item name: ")
            new_item.item_description = input("Enter the item description: ")
            new_item.item_price = float(input("Enter the item price: $"))
            new_item.item_quantity = int(input("Enter the item quantity: "))
            shopping_cart.add_item(new_item)

        elif choice == "r":
            print()
            print("REMOVE ITEM FROM CART")
            item_name = input("Enter name of item to remove: ")
            shopping_cart.remove_item(item_name)

        elif choice == "c":
            print()
            print("CHANGE ITEM QUANTITY")
            modified_item = ItemToPurchase()
            modified_item.item_name = input("Enter the item name: ")
            modified_item.item_quantity = int(input("Enter the new quantity: "))
            shopping_cart.modify_item(modified_item)

        elif choice == "i":
            print()
            print("OUTPUT ITEMS' DESCRIPTIONS")
            shopping_cart.print_descriptions()

        elif choice == "o":
            print()
            print("OUTPUT SHOPPING CART")
            shopping_cart.print_total()


def main():
    customer_name = input("Enter customer's name: ")
    current_date = input("Enter today's date: ")

    print()
    print(f"Customer name: {customer_name}")
    print(f"Today's date: {current_date}")

    shopping_cart = ShoppingCart(customer_name, current_date)
    print_menu(shopping_cart)


if __name__ == "__main__":
    main()

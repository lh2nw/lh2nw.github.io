inventory = {
    "laptop": {"price": 1200, "quantity": 4},
    "mouse": {"price": 25, "quantity": 20},
    "keyboard": {"price": 75, "quantity": 10}
}

# 1. Compute total inventory value
def get_total_value(inv):
    total = sum(item["price"] * item["quantity"] for item in inv.values())
    return total

# 2. Find the most valuable product (by total stock value)
def get_most_valuable(inv):
    # max() with a custom key finding the highest (price * quantity)
    most_valuable = max(inv, key=lambda k: inv[k]["price"] * inv[k]["quantity"])
    return most_valuable

# 3. Update quantities when items are sold
def sell_item(inv, product, amount):
    if product in inv and inv[product]["quantity"] >= amount:
        inv[product]["quantity"] -= amount
    else:
        print(f"Error: Not enough {product} in stock.")

# 4. Return a sorted list of products by total value
def get_sorted_inventory(inv):
    # Create list of tuples: ("product", total_value)
    product_values = [(name, d["price"] * d["quantity"]) for name, d in inv.items()]
    # Sort descending by the second element in the tuple (the total value)
    return sorted(product_values, key=lambda x: x[1], reverse=True)

# Testing the functions
print(f"Initial Total Value: ${get_total_value(inventory)}")
print(f"Most Valuable Item: {get_most_valuable(inventory)}")

sell_item(inventory, "mouse", 5)
print(f"New 'mouse' quantity: {inventory['mouse']['quantity']}")

sorted_inv = get_sorted_inventory(inventory)
print("\nSorted Inventory (Product, Total Value):")
print(sorted_inv)
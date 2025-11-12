"""
Main Application for Product Inventory List System
Provides a console-based user interface for managing inventory
"""

from inventory_system import InventorySystem
from product import Product


def print_header():
    """Print the application header"""
    print("=" * 80)
    print(" " * 15 + "Product Inventory List System")
    print(" " * 10 + "List, Stack, Queue, Linked Lists (ADTs & Linear DS)")
    print("=" * 80)
    print()


def print_menu():
    """Print the main menu options"""
    print("\n" + "-" * 80)
    print("MENU OPTIONS:")
    print("-" * 80)
    print("1.  Add Product (Linked List)")
    print("2.  Remove Product (Linked List)")
    print("3.  Search Product by ID (Linked List)")
    print("4.  Search Products by Name (Linked List)")
    print("5.  Display All Products (Linked List)")
    print("6.  Display Products by Category (Linked List)")
    print("7.  Update Product Quantity")
    print("8.  Update Product Price")
    print("9.  Add Order to Queue (Queue)")
    print("10. Process Order from Queue (Queue)")
    print("11. Display Pending Orders (Queue)")
    print("12. Undo Last Operation (Stack)")
    print("13. Display Recent Operations (Stack)")
    print("14. View Inventory Statistics")
    print("15. Exit")
    print("-" * 80)


def add_product_ui(inventory):
    """User interface for adding a product"""
    print("\n--- Add Product ---")
    try:
        name = input("Enter product name: ").strip()
        if not name:
            print("Error: Product name cannot be empty!")
            return
        
        category = input("Enter product category: ").strip()
        if not category:
            print("Error: Category cannot be empty!")
            return
        
        price = float(input("Enter product price: $"))
        if price < 0:
            print("Error: Price cannot be negative!")
            return
        
        quantity = int(input("Enter product quantity: "))
        if quantity < 0:
            print("Error: Quantity cannot be negative!")
            return
        
        product = inventory.add_product(name, category, price, quantity)
        print(f"\n✓ Product added successfully!")
        print(f"  {product}")
    except ValueError:
        print("Error: Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


def remove_product_ui(inventory):
    """User interface for removing a product"""
    print("\n--- Remove Product ---")
    try:
        product_id = int(input("Enter product ID to remove: "))
        product = inventory.remove_product(product_id)
        if product:
            print(f"\n✓ Product removed successfully!")
            print(f"  {product}")
        else:
            print(f"\n✗ Product with ID {product_id} not found!")
    except ValueError:
        print("Error: Invalid input! Please enter a valid product ID.")
    except Exception as e:
        print(f"Error: {e}")


def search_product_ui(inventory):
    """User interface for searching a product by ID"""
    print("\n--- Search Product by ID ---")
    try:
        product_id = int(input("Enter product ID to search: "))
        product = inventory.search_product(product_id)
        if product:
            print(f"\n✓ Product found:")
            print(f"  {product}")
        else:
            print(f"\n✗ Product with ID {product_id} not found!")
    except ValueError:
        print("Error: Invalid input! Please enter a valid product ID.")
    except Exception as e:
        print(f"Error: {e}")


def search_by_name_ui(inventory):
    """User interface for searching products by name"""
    print("\n--- Search Products by Name ---")
    name = input("Enter product name (or partial name): ").strip()
    if not name:
        print("Error: Search term cannot be empty!")
        return
    
    results = inventory.search_by_name(name)
    if results:
        print(f"\n✓ Found {len(results)} product(s):")
        for product in results:
            print(f"  {product}")
    else:
        print(f"\n✗ No products found matching '{name}'")


def display_all_products_ui(inventory):
    """User interface for displaying all products"""
    print("\n--- All Products ---")
    products = inventory.display_all_products()
    if products:
        print(f"\nTotal products: {len(products)}")
        print("-" * 80)
        for product in products:
            print(f"  {product}")
    else:
        print("\nNo products in inventory.")


def display_by_category_ui(inventory):
    """User interface for displaying products by category"""
    print("\n--- Products by Category ---")
    category = input("Enter category name: ").strip()
    if not category:
        print("Error: Category cannot be empty!")
        return
    
    results = inventory.display_by_category(category)
    if results:
        print(f"\n✓ Found {len(results)} product(s) in category '{category}':")
        for product in results:
            print(f"  {product}")
    else:
        print(f"\n✗ No products found in category '{category}'")


def update_quantity_ui(inventory):
    """User interface for updating product quantity"""
    print("\n--- Update Product Quantity ---")
    try:
        product_id = int(input("Enter product ID: "))
        new_quantity = int(input("Enter new quantity: "))
        if new_quantity < 0:
            print("Error: Quantity cannot be negative!")
            return
        
        if inventory.update_product_quantity(product_id, new_quantity):
            product = inventory.search_product(product_id)
            print(f"\n✓ Quantity updated successfully!")
            print(f"  {product}")
        else:
            print(f"\n✗ Product with ID {product_id} not found!")
    except ValueError:
        print("Error: Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


def update_price_ui(inventory):
    """User interface for updating product price"""
    print("\n--- Update Product Price ---")
    try:
        product_id = int(input("Enter product ID: "))
        new_price = float(input("Enter new price: $"))
        if new_price < 0:
            print("Error: Price cannot be negative!")
            return
        
        if inventory.update_product_price(product_id, new_price):
            product = inventory.search_product(product_id)
            print(f"\n✓ Price updated successfully!")
            print(f"  {product}")
        else:
            print(f"\n✗ Product with ID {product_id} not found!")
    except ValueError:
        print("Error: Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


def add_order_ui(inventory):
    """User interface for adding an order to the queue"""
    print("\n--- Add Order to Queue ---")
    try:
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity to order: "))
        if quantity <= 0:
            print("Error: Quantity must be positive!")
            return
        
        order = inventory.add_order(product_id, quantity)
        if order:
            print(f"\n✓ Order added to queue successfully!")
            print(f"  Product: {order['product_name']}")
            print(f"  Quantity: {order['quantity']}")
            print(f"  Total Price: ${order['total_price']:.2f}")
        else:
            product = inventory.search_product(product_id)
            if product:
                print(f"\n✗ Insufficient stock! Available: {product.quantity}")
            else:
                print(f"\n✗ Product with ID {product_id} not found!")
    except ValueError:
        print("Error: Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


def process_order_ui(inventory):
    """User interface for processing an order from the queue"""
    print("\n--- Process Order from Queue ---")
    order = inventory.process_order()
    if order:
        print(f"\n✓ Order processed successfully!")
        print(f"  Product: {order['product_name']}")
        print(f"  Quantity: {order['quantity']}")
        print(f"  Total Price: ${order['total_price']:.2f}")
    else:
        print("\n✗ No orders in queue to process!")


def display_pending_orders_ui(inventory):
    """User interface for displaying pending orders"""
    print("\n--- Pending Orders in Queue ---")
    orders = inventory.display_pending_orders()
    if orders:
        print(f"\nTotal pending orders: {len(orders)}")
        print("-" * 80)
        for i, order in enumerate(orders, 1):
            print(f"{i}. Product: {order['product_name']} | "
                  f"Quantity: {order['quantity']} | "
                  f"Total: ${order['total_price']:.2f}")
    else:
        print("\nNo pending orders in queue.")


def undo_operation_ui(inventory):
    """User interface for undoing the last operation"""
    print("\n--- Undo Last Operation ---")
    if inventory.undo_last_operation():
        print("\n✓ Last operation undone successfully!")
    else:
        print("\n✗ No operations to undo!")


def display_recent_operations_ui(inventory):
    """User interface for displaying recent operations"""
    print("\n--- Recent Operations (Stack) ---")
    try:
        n = input("Enter number of operations to display (default 5): ").strip()
        n = int(n) if n else 5
        if n <= 0:
            print("Error: Number must be positive!")
            return
    except ValueError:
        print("Error: Invalid input! Using default value of 5.")
        n = 5
    
    operations = inventory.display_recent_operations(n)
    if operations:
        print(f"\nRecent {len(operations)} operation(s):")
        print("-" * 80)
        for i, op in enumerate(operations, 1):
            op_type = op[0]
            if op_type == "add":
                print(f"{i}. ADD: {op[1]}")
            elif op_type == "remove":
                print(f"{i}. REMOVE: {op[1]}")
            elif op_type == "update_quantity":
                print(f"{i}. UPDATE QUANTITY: {op[1].name} (was {op[2]})")
            elif op_type == "update_price":
                print(f"{i}. UPDATE PRICE: {op[1].name} (was ${op[2]:.2f})")
    else:
        print("\nNo recent operations.")


def display_statistics_ui(inventory):
    """User interface for displaying inventory statistics"""
    print("\n--- Inventory Statistics ---")
    stats = inventory.get_statistics()
    print(f"\nTotal Products: {stats['total_products']}")
    print(f"Total Quantity: {stats['total_quantity']}")
    print(f"Total Inventory Value: ${stats['total_value']:.2f}")
    print(f"Number of Categories: {stats['categories']}")
    print(f"Pending Orders in Queue: {stats['pending_orders']}")


def main():
    """Main function to run the application"""
    inventory = InventorySystem()
    
    # Add some sample data for demonstration
    print("Loading sample products...")
    inventory.add_product("Laptop", "Electronics", 999.99, 10)
    inventory.add_product("Mouse", "Electronics", 29.99, 50)
    inventory.add_product("Keyboard", "Electronics", 79.99, 30)
    inventory.add_product("Desk Chair", "Furniture", 199.99, 15)
    inventory.add_product("Coffee Maker", "Appliances", 89.99, 20)
    print("Sample products loaded!")
    
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("\nEnter your choice (1-15): ").strip()
            
            if choice == "1":
                add_product_ui(inventory)
            elif choice == "2":
                remove_product_ui(inventory)
            elif choice == "3":
                search_product_ui(inventory)
            elif choice == "4":
                search_by_name_ui(inventory)
            elif choice == "5":
                display_all_products_ui(inventory)
            elif choice == "6":
                display_by_category_ui(inventory)
            elif choice == "7":
                update_quantity_ui(inventory)
            elif choice == "8":
                update_price_ui(inventory)
            elif choice == "9":
                add_order_ui(inventory)
            elif choice == "10":
                process_order_ui(inventory)
            elif choice == "11":
                display_pending_orders_ui(inventory)
            elif choice == "12":
                undo_operation_ui(inventory)
            elif choice == "13":
                display_recent_operations_ui(inventory)
            elif choice == "14":
                display_statistics_ui(inventory)
            elif choice == "15":
                print("\nThank you for using Product Inventory List System!")
                print("Goodbye!")
                break
            else:
                print("\n✗ Invalid choice! Please enter a number between 1-15.")
            
            input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()










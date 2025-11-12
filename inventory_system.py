"""
Product Inventory List System
Main inventory management system using Lists, Stack, Queue, and Linked Lists
"""

from data_structures import LinkedList, Stack, Queue
from product import Product


class InventorySystem:
    """Product Inventory Management System using various data structures"""
    
    def __init__(self):
        # Linked List for storing products
        self.product_list = LinkedList()
        
        # Stack for tracking recent operations (for undo functionality)
        self.operation_stack = Stack()
        
        # Queue for processing orders/transactions
        self.order_queue = Queue()
        
        # List for storing all products (Python list)
        self.product_array = []
        
        # Counter for product IDs
        self.next_id = 1
    
    def add_product(self, name, category, price, quantity):
        """Add a new product to the inventory using Linked List"""
        product = Product(self.next_id, name, category, price, quantity)
        self.product_list.append(product)
        self.product_array.append(product)
        self.operation_stack.push(("add", product))
        self.next_id += 1
        return product
    
    def remove_product(self, product_id):
        """Remove a product from the inventory"""
        # Search in linked list
        current = self.product_list.head
        prev = None
        found = False
        
        while current is not None:
            if current.data.product_id == product_id:
                found = True
                product = current.data
                # Remove from linked list
                if prev is None:
                    self.product_list.head = current.next
                else:
                    prev.next = current.next
                self.product_list.size -= 1
                
                # Remove from array list
                self.product_array = [p for p in self.product_array if p.product_id != product_id]
                
                # Push to operation stack
                self.operation_stack.push(("remove", product))
                return product
            prev = current
            current = current.next
        
        return None
    
    def search_product(self, product_id):
        """Search for a product by ID"""
        current = self.product_list.head
        while current is not None:
            if current.data.product_id == product_id:
                return current.data
            current = current.next
        return None
    
    def search_by_name(self, name):
        """Search for products by name"""
        results = []
        current = self.product_list.head
        while current is not None:
            if name.lower() in current.data.name.lower():
                results.append(current.data)
            current = current.next
        return results
    
    def update_product_quantity(self, product_id, new_quantity):
        """Update the quantity of a product"""
        product = self.search_product(product_id)
        if product:
            old_quantity = product.quantity
            product.update_quantity(new_quantity)
            self.operation_stack.push(("update_quantity", product, old_quantity))
            return True
        return False
    
    def update_product_price(self, product_id, new_price):
        """Update the price of a product"""
        product = self.search_product(product_id)
        if product:
            old_price = product.price
            product.update_price(new_price)
            self.operation_stack.push(("update_price", product, old_price))
            return True
        return False
    
    def add_order(self, product_id, quantity):
        """Add an order to the queue for processing"""
        product = self.search_product(product_id)
        if product:
            if product.quantity >= quantity:
                order = {
                    "product_id": product_id,
                    "product_name": product.name,
                    "quantity": quantity,
                    "total_price": product.price * quantity
                }
                self.order_queue.enqueue(order)
                return order
            else:
                return None  # Insufficient stock
        return None
    
    def process_order(self):
        """Process the next order from the queue"""
        if not self.order_queue.is_empty():
            order = self.order_queue.dequeue()
            product = self.search_product(order["product_id"])
            if product and product.quantity >= order["quantity"]:
                product.update_quantity(product.quantity - order["quantity"])
                return order
        return None
    
    def undo_last_operation(self):
        """Undo the last operation using the stack"""
        if not self.operation_stack.is_empty():
            operation = self.operation_stack.pop()
            op_type = operation[0]
            
            if op_type == "add":
                # Undo add: remove the product
                product = operation[1]
                self.remove_product(product.product_id)
                # Remove the undo operation from stack
                if not self.operation_stack.is_empty():
                    self.operation_stack.pop()
                return True
            elif op_type == "remove":
                # Undo remove: add the product back
                product = operation[1]
                self.product_list.append(product)
                self.product_array.append(product)
                return True
            elif op_type == "update_quantity":
                # Undo quantity update
                product = operation[1]
                old_quantity = operation[2]
                product.update_quantity(old_quantity)
                return True
            elif op_type == "update_price":
                # Undo price update
                product = operation[1]
                old_price = operation[2]
                product.update_price(old_price)
                return True
        return False
    
    def display_all_products(self):
        """Display all products using Linked List"""
        if self.product_list.is_empty():
            return []
        return self.product_list.display()
    
    def display_by_category(self, category):
        """Display products filtered by category"""
        results = []
        current = self.product_list.head
        while current is not None:
            if current.data.category.lower() == category.lower():
                results.append(current.data)
            current = current.next
        return results
    
    def get_statistics(self):
        """Get inventory statistics"""
        total_products = len(self.product_list)
        total_quantity = 0
        total_value = 0
        categories = set()
        
        current = self.product_list.head
        while current is not None:
            product = current.data
            total_quantity += product.quantity
            total_value += product.price * product.quantity
            categories.add(product.category)
            current = current.next
        
        return {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "total_value": total_value,
            "categories": len(categories),
            "pending_orders": len(self.order_queue)
        }
    
    def display_recent_operations(self, n=5):
        """Display recent operations from the stack"""
        operations = []
        temp_stack = Stack()
        count = 0
        
        while not self.operation_stack.is_empty() and count < n:
            op = self.operation_stack.pop()
            temp_stack.push(op)
            operations.append(op)
            count += 1
        
        # Restore stack
        while not temp_stack.is_empty():
            self.operation_stack.push(temp_stack.pop())
        
        return operations[::-1]  # Reverse to show most recent first
    
    def display_pending_orders(self):
        """Display all pending orders in the queue"""
        orders = []
        temp_queue = Queue()
        
        while not self.order_queue.is_empty():
            order = self.order_queue.dequeue()
            orders.append(order)
            temp_queue.enqueue(order)
        
        # Restore queue
        while not temp_queue.is_empty():
            self.order_queue.enqueue(temp_queue.dequeue())
        
        return orders










"""
Product class definition for the Inventory System
"""


class Product:
    """Product class to represent items in the inventory"""
    def __init__(self, product_id, name, category, price, quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"ID: {self.product_id} | Name: {self.name} | Category: {self.category} | Price: ${self.price:.2f} | Quantity: {self.quantity}"
    
    def __repr__(self):
        return f"Product({self.product_id}, '{self.name}', '{self.category}', {self.price}, {self.quantity})"
    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.product_id == other.product_id
        return False
    
    def update_quantity(self, new_quantity):
        """Update the quantity of the product"""
        self.quantity = new_quantity
    
    def update_price(self, new_price):
        """Update the price of the product"""
        self.price = new_price










"""
Flask Web Application for Product Inventory List System
Provides a web-based user interface for managing inventory
"""

from flask import Flask, render_template, jsonify, request
from inventory_system import InventorySystem
from product import Product

app = Flask(__name__)
inventory = InventorySystem()


def product_to_dict(product):
    """Convert Product object to dictionary for JSON serialization"""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "quantity": product.quantity
    }


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    products = inventory.display_all_products()
    # Convert Product objects to dictionaries
    products_list = []
    current = inventory.product_list.head
    while current is not None:
        products_list.append(product_to_dict(current.data))
        current = current.next
    return jsonify({"success": True, "products": products_list})


@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        category = data.get('category', '').strip()
        price = float(data.get('price', 0))
        quantity = int(data.get('quantity', 0))
        
        if not name or not category:
            return jsonify({"success": False, "error": "Name and category are required"}), 400
        
        if price < 0 or quantity < 0:
            return jsonify({"success": False, "error": "Price and quantity must be non-negative"}), 400
        
        product = inventory.add_product(name, category, price, quantity)
        return jsonify({"success": True, "product": product_to_dict(product)})
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = inventory.search_product(product_id)
    if product:
        return jsonify({"success": True, "product": product_to_dict(product)})
    return jsonify({"success": False, "error": "Product not found"}), 404


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    """Remove a product"""
    product = inventory.remove_product(product_id)
    if product:
        return jsonify({"success": True, "product": product_to_dict(product)})
    return jsonify({"success": False, "error": "Product not found"}), 404


@app.route('/api/products/<int:product_id>/quantity', methods=['PUT'])
def update_quantity(product_id):
    """Update product quantity"""
    try:
        data = request.get_json()
        new_quantity = int(data.get('quantity', 0))
        
        if new_quantity < 0:
            return jsonify({"success": False, "error": "Quantity cannot be negative"}), 400
        
        if inventory.update_product_quantity(product_id, new_quantity):
            product = inventory.search_product(product_id)
            return jsonify({"success": True, "product": product_to_dict(product)})
        return jsonify({"success": False, "error": "Product not found"}), 404
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/products/<int:product_id>/price', methods=['PUT'])
def update_price(product_id):
    """Update product price"""
    try:
        data = request.get_json()
        new_price = float(data.get('price', 0))
        
        if new_price < 0:
            return jsonify({"success": False, "error": "Price cannot be negative"}), 400
        
        if inventory.update_product_price(product_id, new_price):
            product = inventory.search_product(product_id)
            return jsonify({"success": True, "product": product_to_dict(product)})
        return jsonify({"success": False, "error": "Product not found"}), 404
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products by name"""
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"success": False, "error": "Search term is required"}), 400
    
    results = inventory.search_by_name(name)
    products_list = [product_to_dict(p) for p in results]
    return jsonify({"success": True, "products": products_list})


@app.route('/api/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    results = inventory.display_by_category(category)
    products_list = [product_to_dict(p) for p in results]
    return jsonify({"success": True, "products": products_list})


@app.route('/api/orders', methods=['POST'])
def add_order():
    """Add an order to the queue"""
    try:
        data = request.get_json()
        product_id = int(data.get('product_id', 0))
        quantity = int(data.get('quantity', 0))
        
        if quantity <= 0:
            return jsonify({"success": False, "error": "Quantity must be positive"}), 400
        
        order = inventory.add_order(product_id, quantity)
        if order:
            return jsonify({"success": True, "order": order})
        else:
            product = inventory.search_product(product_id)
            if product:
                return jsonify({"success": False, "error": f"Insufficient stock! Available: {product.quantity}"}), 400
            return jsonify({"success": False, "error": "Product not found"}), 404
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/orders/process', methods=['POST'])
def process_order():
    """Process the next order from the queue"""
    order = inventory.process_order()
    if order:
        return jsonify({"success": True, "order": order})
    return jsonify({"success": False, "error": "No orders in queue"}), 404


@app.route('/api/orders', methods=['GET'])
def get_pending_orders():
    """Get all pending orders"""
    orders = inventory.display_pending_orders()
    return jsonify({"success": True, "orders": orders})


@app.route('/api/operations/undo', methods=['POST'])
def undo_operation():
    """Undo the last operation"""
    if inventory.undo_last_operation():
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "No operations to undo"}), 404


@app.route('/api/operations/recent', methods=['GET'])
def get_recent_operations():
    """Get recent operations"""
    try:
        n = int(request.args.get('n', 5))
        if n <= 0:
            n = 5
    except (ValueError, TypeError):
        n = 5
    
    operations = inventory.display_recent_operations(n)
    operations_list = []
    for op in operations:
        op_type = op[0]
        if op_type == "add":
            operations_list.append({
                "type": "add",
                "description": f"Added: {op[1].name}",
                "product": product_to_dict(op[1])
            })
        elif op_type == "remove":
            operations_list.append({
                "type": "remove",
                "description": f"Removed: {op[1].name}",
                "product": product_to_dict(op[1])
            })
        elif op_type == "update_quantity":
            operations_list.append({
                "type": "update_quantity",
                "description": f"Updated quantity: {op[1].name} (was {op[2]})",
                "product": product_to_dict(op[1]),
                "old_value": op[2]
            })
        elif op_type == "update_price":
            operations_list.append({
                "type": "update_price",
                "description": f"Updated price: {op[1].name} (was ${op[2]:.2f})",
                "product": product_to_dict(op[1]),
                "old_value": op[2]
            })
    
    return jsonify({"success": True, "operations": operations_list})


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get inventory statistics"""
    stats = inventory.get_statistics()
    return jsonify({"success": True, "statistics": stats})


# Initialize sample data on module import
# This ensures data is loaded when the app starts
def init_sample_data():
    """Initialize with sample products"""
    if inventory.product_list.is_empty():  # Only add if empty
        inventory.add_product("Laptop", "Electronics", 999.99, 10)
        inventory.add_product("Mouse", "Electronics", 29.99, 50)
        inventory.add_product("Keyboard", "Electronics", 79.99, 30)
        inventory.add_product("Desk Chair", "Furniture", 199.99, 15)
        inventory.add_product("Coffee Maker", "Appliances", 89.99, 20)

# Initialize sample data
init_sample_data()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


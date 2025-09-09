#!/usr/bin/env python3
# flask_inventory_api.py

# to check...
# http://127.0.0.1:5000/products
# http://localhost:5000/

from flask import Flask, jsonify, request
from models import (Base, session, Product, engine)
from sqlite_CSV_backup import make_csv_backup_from_sqlite
from datetime import datetime
import logging

# Setup
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure DB exists
Base.metadata.create_all(engine)

# --- CRUD Endpoints ---

@app.route("/products", methods=["GET"])
def get_products():
    """List all products"""
    products = session.query(Product).all()
    result = [
        {
            "id": p.id,
            "name": p.product_name,
            "price": p.product_price / 100,  # back to dollars
            "quantity": p.product_quantity,
            "last_updated": str(p.date_updated),
        }
        for p in products
    ]
    return jsonify(result)


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get one product by ID"""
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.product_name,
        "price": product.product_price / 100,
        "quantity": product.product_quantity,
        "last_updated": str(product.date_updated),
    })


@app.route("/products", methods=["POST"])
def add_product():
    """Add a new product"""
    data = request.get_json()
    try:
        new_product = Product(
            product_name=data["name"],
            product_price=int(float(data["price"]) * 100),  # convert dollars → cents
            product_quantity=float(data["quantity"]),
            date_updated=datetime.strptime(data["last_updated"], "%Y-%m-%d").date()
        )
        session.add(new_product)
        session.commit()
    except Exception as e:
        session.rollback()
        logging.exception("Failed to add product")
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Product added successfully!"}), 201


@app.route("/backup", methods=["POST"])
def backup():
    """Backup DB to CSV"""
    make_csv_backup_from_sqlite("inventory.db", "backup_csv.csv")
    return jsonify({"message": "Backup created successfully!"})


# --- Run server ---
if __name__ == "__main__":
    app.run(debug=True)

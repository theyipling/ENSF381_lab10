"""
================================================
Name        : server.py
Assignment  : Lab 10 Exercise A, B, C
Author(s)   : Sarah Yip, Stephenie Oboh
Submission  : March 27, 2024
Description : Flask
================================================
"""

# import flask and other needed modules
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# function to read the product data
def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    
# fetch all products or a specfic product by ID
@app.route('/products', methods = ['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        #return all products wrapped in an object with an 'products' key
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        # If a specific product is requested ,
        # wrap it in an object with a ' products ' key
        # Note : You might want to change this
        # if you want to return a single product not wrapped in a list
        return jsonify(product) if product else ('',404)

# add a new product
@app.route('/products/add', methods = ['POST'])
def add_products():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products)+1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products},f)
    return jsonify(new_product), 201

#serve images from the product images folder 
@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

#for update a function with put 
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    product_index = next((index for index, p in enumerate(products) if p['id'] == product_id), None)
    if product_index is not None:
        updated_product = request.json
        products[product_index] = updated_product
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(updated_product)
    else:
        return jsonify({"error": "Product not found"}), 404
    
# delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    product_index = next((index for index, p in enumerate(products) if p['id'] == product_id), None)
    if product_index is not None:
        deleted_product = products.pop(product_index)
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(deleted_product)
    else:
        return jsonify({"error": "Product not found"}), 404

#to run flask application
if __name__ == '__main__':
    app.run(debug=True)
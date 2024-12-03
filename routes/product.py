from flask import jsonify
from app import app, render_template, request, IMAGE_DIR
import os
import time
from sqlalchemy import create_engine, text
from helpers import file_upload

# Create the engine
engine = create_engine(
    "postgresql+psycopg2://postgres.lzjgsezlsuibnncuuwnb:GHKosal%4002Web@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

# Ensure the IMAGE_DIR ends with a slash
IMAGE_DIR = os.path.join(IMAGE_DIR, 'product')


@app.route('/product')
def product():
    module = 'product'
    return render_template('product.html', module=module)


@app.get('/product/list')
def productList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM products"))
            data = result.fetchall()
            products = [
                {
                    "id": item[0],
                    "name": item[1],
                    "cost": item[2],
                    "price": item[3],
                    "category_id": item[4],
                    "unit_id": item[5],
                    "brand_id": item[6],
                    "tag_id": item[7],
                    "image": item[8]
                }
                for item in data
            ]
            return jsonify(products)  # Return as JSON response
    except Exception as e:
        print("Error fetching products:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/product/save')
def saveProduct():
    try:
        form = request.get_json()
        name = form.get('name')
        cost = form.get('cost')
        price = form.get('price')
        category_id = form.get('category_id')
        unit_id = form.get('unit_id')
        brand_id = form.get('brand_id')
        tag_id = form.get('tag_id')
        image_string = form.get('image')  # Ensure 'image' exists in the request

        if not name or cost is None or price is None:
            return jsonify({"error": "Name, cost, and price are required"}), 400

        image_name = None

        # Check if there's an image and it's in base64 format
        if image_string and image_string.startswith('data:image/'):
            image_name = f"{time.time()}.png"
            image_path = os.path.join(IMAGE_DIR, image_name)
            file_upload.upload(image_string, IMAGE_DIR, image_name)  # Ensure this handles errors properly

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO products (name, cost, price, category_id, unit_id, brand_id, tag_id, image)
            VALUES (:name, :cost, :price, :category_id, :unit_id, :brand_id, :tag_id, :image)
        """)

        # Execute the query within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(insert_query, {
                    'name': name,
                    'cost': cost,
                    'price': price,
                    'category_id': category_id,
                    'unit_id': unit_id,
                    'brand_id': brand_id,
                    'tag_id': tag_id,
                    'image': image_name
                })

        return jsonify({
            "message": "Record saved successfully",
            "data": {
                "name": name,
                "cost": cost,
                "price": price,
                "category_id": category_id,
                "unit_id": unit_id,
                "brand_id": brand_id,
                "tag_id": tag_id,
                "image": image_name
            }
        })

    except Exception as e:
        print("Error saving product:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/product/update')
def updateProduct():
    try:
        form = request.get_json()
        product_id = form.get('id')
        name = form.get('name')
        cost = form.get('cost')
        price = form.get('price')
        category_id = form.get('category_id')
        unit_id = form.get('unit_id')
        brand_id = form.get('brand_id')
        tag_id = form.get('tag_id')
        image_string = form.get('image')  # New image base64 string (if any)

        if not product_id or not name:
            return jsonify({"error": "Product ID and name are required"}), 400

        # Fetch existing image name from database
        with engine.connect() as connection:
            existing_image_query = text("SELECT image FROM products WHERE id = :id")
            existing_image = connection.execute(existing_image_query, {'id': product_id}).fetchone()

            # Remove existing image if the new image is not provided
            if existing_image and image_string is None:
                existing_image_path = os.path.join(IMAGE_DIR, existing_image[0])
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)

                # Set image to None in the update query
                image_string = None

            # Process new image upload if provided
            elif image_string and image_string.startswith('data:image/'):
                image_name = f"{time.time()}.png"
                file_upload.upload(image_string, IMAGE_DIR, image_name)  # Handle image upload
                image_string = image_name  # Assign new image name for database

                # Remove old image file if a new image is uploaded
                if existing_image:
                    existing_image_path = os.path.join(IMAGE_DIR, existing_image[0])
                    if os.path.exists(existing_image_path):
                        os.remove(existing_image_path)

        # Use parameterized query for updating the product record
        update_query = text("""
            UPDATE products
            SET name = :name, cost = :cost, price = :price, category_id = :category_id, 
                unit_id = :unit_id, brand_id = :brand_id, tag_id = :tag_id, image = :image
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': product_id,
                    'name': name,
                    'cost': cost,
                    'price': price,
                    'category_id': category_id,
                    'unit_id': unit_id,
                    'brand_id': brand_id,
                    'tag_id': tag_id,
                    'image': image_string  # This could be None or an image filename
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                'id': product_id,
                "name": name,
                "cost": cost,
                "price": price,
                "category_id": category_id,
                "unit_id": unit_id,
                "brand_id": brand_id,
                "tag_id": tag_id,
                "image": image_string
            }
        })

    except Exception as e:
        print("Error updating product:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/product/delete')
def deleteProduct():
    try:
        form = request.get_json()
        product_id = form.get('id')

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # First, fetch the record to check if it exists and get the image name (if any)
                select_query = text("SELECT image FROM products WHERE id = :id")
                product_record = connection.execute(select_query, {'id': product_id}).fetchone()

                if not product_record:
                    return jsonify({"error": "Product not found"}), 404

                # Delete the image from the filesystem if it exists
                image_name = product_record[0]
                if image_name:
                    image_path = os.path.join(IMAGE_DIR, image_name)
                    if os.path.exists(image_path):
                        os.remove(image_path)

                # Now delete the product from the database
                delete_query = text("DELETE FROM products WHERE id = :id")
                connection.execute(delete_query, {'id': product_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": product_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                print("Error deleting product:", e)
                return jsonify({"error": str(e)}), 500

    except Exception as e:
        print("Error in delete operation:", e)
        return jsonify({"error": str(e)}), 500

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
    print(e)


@app.route('/category')
def category():
    module = 'category'
    return render_template('category.html', module=module)


@app.get('/category/list')
def categoryList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM categories"))
            data = result.fetchall()
            connection.commit()
            category_list = []
            for item in data:
                category_list.append(
                    {
                        "id": item[0],
                        "name": item[1],
                        "description": item[2],
                    }
                )
            return category_list
    except Exception as e:
        print(e)
        return {"error": str(e)}

@app.get('/product/category/<int:category_id>')
def getProductsByCategory(category_id):
    try:
        query = text("""
            SELECT p.*
            FROM products p
            WHERE p.category_id = :category_id
        """)

        with engine.connect() as connection:
            result = connection.execute(query, {'category_id': category_id})
            products = result.fetchall()

        if not products:
            return jsonify({"error": "No products found in this category"}), 404

        product_list = []
        for product in products:
            product_list.append({

                    "id": product[0],
                    "name": product[1],
                    "cost": product[2],
                    "price": product[3],
                    "category_id": product[4],
                    "unit_id": product[5],
                    "brand_id": product[6],
                    "tag_id": product[7],
                    "image": product[8]

            })

        return jsonify(product_list)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500







@app.post('/category/save')
def saveCategory():
    try:
        form = request.get_json()
        name = form.get('name')
        description = form.get('description')

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO categories (name, description) 
            VALUES (:name, :description)
        """)

        # Execute the query within a transaction
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(insert_query, {
                    'name': name,
                    'description': description
                })

        return jsonify({
            "message": "Record saved successfully",
            "data": {
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/category/update')
def updateCategory():
    try:
        form = request.get_json()
        category_id = form.get('id')
        name = form.get('name')
        description = form.get('description')

        # Use parameterized query for updating the user record
        update_query = text("""
            UPDATE categories
            SET name = :name, description = :description
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': category_id,
                    'name': name,
                    'description': description,
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                "id": category_id,
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/category/delete')
def deleteCategory():
    try:
        form = request.get_json()
        category_id = form.get('id')

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # Now delete the category from the database
                delete_query = text("DELETE FROM categories WHERE id = :id")
                connection.execute(delete_query, {'id': category_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": category_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                raise e

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



from flask import jsonify

from app import app, render_template, request, IMAGE_DIR
import os
import time
from sqlalchemy import create_engine, text
from helpers import file_upload

engine = create_engine(
    "postgresql+psycopg2://postgres.lzjgsezlsuibnncuuwnb:GHKosal%4002Web@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(e)

IMAGE_DIR += '/user'


@app.route('/user')
def user():
    module = 'user'
    return render_template('user.html', module=module)


@app.get('/user/list')
def userList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users"))
            data = result.fetchall()
            connection.commit()
            users = []
            for item in data:
                users.append(
                    {
                        "id": item[0],
                        "name": item[1],
                        "gender": item[2],
                        "phone": item[3],
                        "email": item[4],
                        "address": item[5],
                        "image": item[6]
                    }
                )
            return users
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post('/user/save')
def saveUser():
    try:
        form = request.get_json()
        name = form.get('name')
        gender = form.get('gender')
        phone = form.get('phone')
        email = form.get('email')
        address = form.get('address')
        image = form.get('image')  # Ensure 'image' exists in the request

        # Check if there's an image and it's in base64 format
        if image and image.startswith('data:image/'):
            image_path = os.path.join(IMAGE_DIR)
            image_name = f"{time.time()}.png"
            file_upload.upload(image, image_path, image_name)  # Make sure this handles errors properly
            image = image_name

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO users (name, gender, phone, email, address, image)
            VALUES (:name, :gender, :phone, :email, :address, :image)
        """)

        # Execute the query within a transaction
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(insert_query, {
                    'name': name,
                    'gender': gender,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'image': image
                })

        return jsonify({
            'message': 'Record saved successfully',
            'data': {
                'name': name,
                'gender': gender,
                'phone': phone,
                'email': email,
                'address': address,
                'image': image
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/user/update')
def updateUser():
    try:
        form = request.get_json()
        user_id = form.get('id')
        name = form.get('name')
        gender = form.get('gender')
        phone = form.get('phone')
        email = form.get('email')
        address = form.get('address')
        image = form.get('image')  # New image base64 string (if any)

        # Fetch existing image name from database
        with engine.connect() as connection:
            existing_image_query = text("SELECT image FROM users WHERE id = :id")
            existing_image = connection.execute(existing_image_query, {'id': user_id}).fetchone()

            # Check if the user is removing the image
            if existing_image[0] and image is None:
                # Remove the image file from the storage
                existing_image_path = os.path.join(IMAGE_DIR, existing_image[0])
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)
                image = None  # Update the DB to set image field to NULL or empty string

            # If a new image is uploaded (base64), process it
            elif image and image.startswith('data:image/'):
                image_path = os.path.join(IMAGE_DIR)
                image_name = f"{time.time()}.png"
                file_upload.upload(image, image_path, image_name)  # Handle image upload
                image = image_name  # Assign new image name for database

                # Remove old image file if a new image is uploaded
                if existing_image[0]:
                    existing_image_path = os.path.join(IMAGE_DIR, existing_image[0])
                    if os.path.exists(existing_image_path):
                        os.remove(existing_image_path)

        # Use parameterized query for updating the user record
        update_query = text("""
            UPDATE users
            SET name = :name, gender = :gender, phone = :phone, email = :email, 
                address = :address, image = :image
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': user_id,
                    'name': name,
                    'gender': gender,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'image': image  # This could be None, a filename, or an empty value
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                'id': user_id,
                'name': name,
                'gender': gender,
                'phone': phone,
                'email': email,
                'address': address,
                "image": image
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/user/delete')
def deleteUser():
    try:
        form = request.get_json()
        user_id = form.get('id')

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # First, fetch the record to check if it exists and get the image name (if any)
                select_query = text("SELECT image FROM users WHERE id = :id")
                user_record = connection.execute(select_query, {'id': user_id}).fetchone()

                if not user_record:
                    return jsonify({"error": "User not found"}), 404

                # Optional: If the user has an image, delete the image from the filesystem
                image_name = user_record[0]
                if image_name:
                    image_path = os.path.join(IMAGE_DIR, image_name)
                    if os.path.exists(image_path):
                        os.remove(image_path)

                # Now delete the user from the database
                delete_query = text("DELETE FROM users WHERE id = :id")
                connection.execute(delete_query, {'id': user_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": user_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                raise e

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
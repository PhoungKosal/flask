from flask import jsonify
from app import app, render_template, request
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres.lzjgsezlsuibnncuuwnb:GHKosal%4002Web@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
)


# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(e)


@app.route('/tag')
def tag():
    module = 'tag'
    return render_template('tag.html', module=module)


@app.get('/tag/list')
def tagList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM tags"))
            data = result.fetchall()
            connection.commit()
            tags = []
            for item in data:
                tags.append(
                    {
                        "id": item[0],
                        "name": item[1],
                        "description": item[2],
                    }
                )
            return tags
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post('/tag/save')
def saveTag():
    try:
        form = request.get_json()
        name = form.get('name')
        description = form.get('description')

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO tags (name, description) 
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


@app.post('/tag/update')
def updateTag():
    try:
        form = request.get_json()
        tag_id = form.get('id')
        name = form.get('name')
        description = form.get('description')

        # Use parameterized query for updating the user record
        update_query = text("""
            UPDATE tags
            SET name = :name, description = :description
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': tag_id,
                    'name': name,
                    'description': description,
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                "id": tag_id,
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/tag/delete')
def deleteTag():
    try:
        form = request.get_json()
        tag_id = form.get('id')

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # Now delete the tag from the database
                delete_query = text("DELETE FROM tags WHERE id = :id")
                connection.execute(delete_query, {'id': tag_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": tag_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                raise e

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



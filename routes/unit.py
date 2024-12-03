from flask import jsonify
from app import app, render_template, request
from sqlalchemy import create_engine, text

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


@app.route('/unit')
def unit():
    module = 'unit'
    return render_template('unit.html', module=module)


@app.get('/unit/list')
def unitList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM units"))
            data = result.fetchall()
            units = []
            for item in data:
                units.append(
                    {
                        "id": item[0],
                        "name": item[1],
                        "description": item[2],
                    }
                )
            return jsonify(units)  # Return JSON response for better API compatibility
    except Exception as e:
        print("Error fetching units:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/unit/save')
def saveUnit():
    try:
        form = request.get_json()
        name = form.get('name')
        description = form.get('description')

        # Validate input parameters
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO units (name, description) 
            VALUES (:name, :description)
        """)

        # Execute the query within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(insert_query, {
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
        print("Error saving unit:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/unit/update')
def updateUnit():
    try:
        form = request.get_json()
        unit_id = form.get('id')
        name = form.get('name')
        description = form.get('description')

        # Validate input parameters
        if not unit_id or not name:
            return jsonify({"error": "ID and Name are required"}), 400

        # Use parameterized query for updating the unit record
        update_query = text("""
            UPDATE units
            SET name = :name, description = :description
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': unit_id,
                    'name': name,
                    'description': description,
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                "id": unit_id,
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print("Error updating unit:", e)
        return jsonify({"error": str(e)}), 500


@app.post('/unit/delete')
def deleteUnit():
    try:
        form = request.get_json()
        unit_id = form.get('id')

        # Validate input parameters
        if not unit_id:
            return jsonify({"error": "ID is required"}), 400

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # Now delete the unit from the database
                delete_query = text("DELETE FROM units WHERE id = :id")
                connection.execute(delete_query, {'id': unit_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": unit_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                print("Error deleting unit:", e)
                return jsonify({"error": str(e)}), 500

    except Exception as e:
        print("Error in delete operation:", e)
        return jsonify({"error": str(e)}), 500

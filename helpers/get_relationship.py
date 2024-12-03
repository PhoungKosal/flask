# from sqlalchemy import create_engine, text
# import os
#
# # Use environment variables for credentials (as an example)
# # engine = create_engine(os.getenv("DATABASE_URL"))
#
# # Hardcoded for demonstration purposes; replace with environment variables
# engine = create_engine("mysql+mysqlconnector://root:endhe%40d@127.0.0.1/class_flask")
#
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Error: {e}")
#
#
# def get_relationship(relationship, id):
#     try:
#         # Ensure the relationship is a valid table name to prevent SQL injection
#         # valid_tables = ['your_table1', 'your_table2']  # List valid table names
#         # if relationship not in valid_tables:
#         #     return {"error": "Invalid table name"}
#
#         with engine.connect() as connection:
#             # Use parameterized queries to avoid SQL injection
#             result = connection.execute(text(f'SELECT * FROM {relationship} WHERE id = :id'), {"id": id})
#             record = result.fetchone()
#
#             if record:
#                 # Use _mapping attribute to get a dictionary-like object
#                 return dict(record._mapping)
#             else:
#                 return None
#
#     except Exception as e:
#         print(f"Error: {e}")
#         return {"error": str(e)}

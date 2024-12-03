#### Start Dev env

````
flask run --debug
````

## Connect to mysql

```
# install driver and package
pip install mysql-connector-python
pip install SQLAlchemy

# create connection
try:
    engine = create_engine("mysql+mysqlconnector://root:mysql@127.0.0.1/st2_6_ap")
    # Test the connection
    connection = engine.connect()
except Exception as e:
    print(e)
    
# execut query
result = connection.execute(text("SELECT * FROM product"))
data = result.fetchall()
connection.commit()
```

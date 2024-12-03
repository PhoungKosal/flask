## Branch Management Module
### + Branch*
```
1. list
2. create
3. update
```
```
id *
name *
logo
phone *
alt_phone
location*
```

## User Management Module
### User*
```
1. list
2. create
3. update
4. delete
```
```
id*
name*
user_name*
password*
role*
profile
```

## Warehouse Management Module
### Warehouse*
```
1. list
2. create
3. update
```
```
id*
name*
```

## Product Management Module
### Category*
```
1. list
2. create
3. update
4. delete
```
```
id*
name*
```

### Unit*
```
1. list
2. create
3. update
4. delete
```
```
id*
name*
description
```

### Tag
```
1. list
2. create
3. update
4. delete
```
```
id*
name*
description
```

### Brand
```
1. list
2. create
3. update
4. delete
```
```
id*
name*
description
```

### Product*
```
1. list
2. create
3. update
4. delete
```

```
id*
name*
cost*
price*
category_id*
unit_id*
brand_id
tag_id
```

## Partner Management Module
### Customer*
```
1. list
2. create
3. update
4. delete
```
```
id*
name
phone*
```

### Supplier*
```
1. list
2. create
3. update
4. delete
```

```
id*
name*
phone*
alt_phone
address*
description
```


## Purchase Management modules
```
1. list
2. create
3. update
4. delete
```

```
id*
supplier_id*
transaction_date*
ref_no*
grand_total*
qty
cost
sub_total
discount_about
product_id
```

## Stock Management modules
### Stock List
### Stock Adjustment IN(+)
````
1. create
````

````
id*
warehouse_id*
product*
qyt*
ref_no
user_id*
````

### Stock Adjustment Out(-)
````
1. create
````

````
id*
warehouse_id*
product*
qyt*
ref_no
user_id*
````

### Stock Transfer(from a warehouse-> to warehouse)
```
1. list
2. create
```

````
id*
from_warehouse_id*
to_warehouse_id*
product*
qyt*
ref_no
user_id*
````


## Sale Management modules (Admin)

#### Sale Management modules (POS)

##### recent sale(10)
```
1. list
2. create
3. update
4. delete
```

````
id*
product*
qyt*
price*
sub_total*
discount_amount*
invoice_number* (auto)
grand_total*
customer*
user_id*
````








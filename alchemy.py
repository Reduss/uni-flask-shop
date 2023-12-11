from sqlalchemy import create_engine, text


engine = create_engine('mysql+mysqlconnector://root:root@localhost/sdb_shop', echo=None)

sql_new_product = text('INSERT INTO product (title, price, category_id, amount_in_stock) VALUES (:title, :price, :category_id, :amount)')


with engine.connect() as con:
    res = con.execute(sql_new_product, {'title': 'TEST', 'price': 99999, 'category_id': 4, 'amount': 999999}, )
    con.commit()
    print(res)

with engine.connect() as con:
    res = con.execute(text('SELECT * FROM product'))
prods = res.fetchall()

for p in prods:
    print(p)


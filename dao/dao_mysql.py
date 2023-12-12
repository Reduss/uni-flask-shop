from sqlalchemy import text, create_engine

from dao.dao import DAO
from models import Product, Customer, Order, Category, Cart, OrderStatus
from config import Config


class MysqlConnection():
    def __init__(self) -> None:
        self.db = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class CustomerDAOMySQL(DAO, MysqlConnection):
    _sql_get_all = text('SELECT * FROM customer')
    _sql_insert = text('INSERT INTO customer (first_name, last_name, phone_num, address) VALUES (:fname, :lname, :phone, :addr);')
    
    def __init__(self) -> None:
        super().__init__()
        
    
    def insert(self, c: Customer):
        with self.db.connect() as c:
            c.execute(
                self._sql_insert, 
                {
                    'fname': c.first_name, 
                    'lname': c.last_name, 
                    'phone': c.phone_num, 
                    'addr': c.address
                }
            )
            c.commit()
    
    def update(self, id, entity: Product):
        pass
    
    def delete(self, id):
        pass
    
    def get_all(self):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        custs = [Customer(*r) for r in res.fetchall()]
        return custs
    


class ProductDAOMySQL(DAO, MysqlConnection):
    _sql_insert = text('INSERT INTO product (title, price, category_id, amount_in_stock) VALUES (:title, :price, :category_id, :amount);')
    _sql_update = text('UPDATE product SET title=:title, price=:price, category_id=:category_id, amount_in_stock=:amnt WHERE id=:id')
    _sql_delete = text('DELETE FROM product WHERE product.id = :id;')
    _sql_get = text("""
                    SELECT product.id, product.title, product.price, category.title, product.amount_in_stock 
                    FROM product 
                    LEFT JOIN category 
                    ON product.category_id = category.id 
                    WHERE product.id = :id""")
    _sql_get_all = text("""
                        SELECT product.id, product.title, product.price, category.title, product.amount_in_stock 
                        FROM product 
                        LEFT JOIN category 
                        ON product.category_id = category.id;""")

    _sql_get_cat_by_name = text('SELECT id from category WHERE category.title = :category')

    def __init__(self) -> None:
        super().__init__()
    
    def insert(self, prod: Product):
        with self.db.connect() as c:
            cat_id = c.execute(self._sql_get_cat_by_name, {'category': prod.category}).fetchone()[0]
            c.execute(
                self._sql_insert, 
                {
                    'title': prod.title, 
                    'price': prod.price, 
                    'category_id': cat_id, 
                    'amount': prod.amount_in_stock
                }
            )
            c.commit()
    
    def update(self, id, entity: Product):
        with self.db.connect() as c:
            try:
                cat_id = c.execute(self._sql_get_cat_by_name, {'category': entity.category}).fetchone()[0]
                c.execute(
                    self._sql_update, 
                    {
                        'title': entity.title, 
                        'price': entity.price, 
                        'category_id': cat_id, 
                        'amnt': entity.amount_in_stock,
                        'id': id
                    }
                )
                c.commit()
            except Exception as e:
                print(f'Error updating: {e}')
                
    def delete(self, id):   
        with self.db.connect() as c:
            c.execute(self._sql_delete, {'id': id})
            c.commit()

    def get_all(self):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        prods = [Product(id= r[0], title= r[1], price= r[2],category= r[3],amount_in_stock= r[4]) for r in res.fetchall()]
        return prods
    
    def get(self, id):
        with self.db.connect() as c:
            res = c.execute(self._sql_get, {'id': id})
        res_l = res.fetchone()
        if res:
            return Product(
                id= res_l[0],
                title= res_l[1],
                price= res_l[2],
                category= res_l[3],
                amount_in_stock= res_l[4]
            )
        return None


class CategoryDAOMySQL(DAO, MysqlConnection):
    _sql_get_all = text('SELECT * FROM category')
    _sql_get_by_title= text('SELECT * FROM category WHERE title=:title')
    _sql_get = text('SELECT * FROM category WHERE id=:id')
    
    def __init__(self) -> None:
        super().__init__()
    
    def get_all(self):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        cats = [Category(*r) for r in res.fetchall()]
        return cats

    def get_by_title(self, cat_title):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_by_title, {'title': cat_title}).fetchone()
        return Category(res[0], res[1])

    def get(self, id):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get, {'id': id}).fetchone()
        
        return Category(res[0], res[1])



class OrderDAOMySQL(DAO, MysqlConnection):
    _sql_create = text('CALL PlaceOrder(:fname, :lname, :phone, :address, :prod_ids, :prod_amnts);')
    _sql_get_all = text("""
                        SELECT customer_order.id, customer_order.customer_id, customer_order.status_id, customer_order.order_date, customer_order.total_price
                        FROM customer_order
                        LEFT JOIN customer
                        ON customer_order.customer_id = customer.id
                        LEFT JOIN order_status
                        ON customer_order.status_id = order_status.id
                        WHERE customer_order.customer_id = customer_id
                        """)
    _sql_get_items_amount = text("""
                        SELECT order_item.id, order_item.customer_order_id, order_item.product_id, order_item.price, order_item.amount
                        FROM order_item
                        LEFT JOIN customer_order
                        ON customer_order.id = order_item.customer_order_id
                        WHERE order_item.customer_order_id = :id
                        """)
    
    
    def __init__(self) -> None:
        super().__init__()

    def place_order(self, customer: Customer, cart: Cart):
        prod_ids = (str(p.id) for p in cart.prods.keys())
        prod_amnts = cart.prods.values()
        
        id_str = ', '.join(prod_ids)
        amnt_str = ', '.join(map(str, prod_amnts))
        
        try:
            with self.db.engine.connect() as c:
                c.execute(
                    self._sql_create,
                    {
                        'fname': customer.first_name,
                        'lname': customer.last_name,
                        'phone': customer.phone_num,
                        'address': customer.address,
                        'prod_ids': id_str,
                        'prod_amnts': amnt_str,
                    }
                )
                c.commit()
        except Exception as e:
            print(f'Exception while placing order: {e}')
    
    def get_all(self):
        c_dao = CustomerDAOMySQL()
        p_dao = ProductDAOMySQL()
        s_dao = OrderStatusDAOMySQL()
        print('in order dao')
        customers = c_dao.get_all()
        
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        orders = []
        for r in res.fetchall():
            ord = Order(
                id=r[0],
                customer=list(filter(lambda c: c.id == r[1], customers))[0],
                status=s_dao.get(r[2]).title,
                order_date=str(r[-2]),
                total_price=r[-1],
                products= {}
            )
            print(f'ORDER ID {ord.id}')
            with self.db.engine.connect() as c:
                res = c.execute(self._sql_get_items_amount, {'id': ord.id})
            
            for ent in res.fetchall():
                prod = p_dao.get(ent[-3])
                prod.price = ent[-2]
                ord.products[prod] = ent[-1]
            orders.append(ord)
        print(f'ORDERS FETCHED')
        return orders


class OrderStatusDAOMySQL(DAO, MysqlConnection):
    _sql_get = text('SELECT * FROM order_status WHERE id=:id')
    _sql_get_all = text('SELECT * FROM order_status')
    
    def __init__(self) -> None:
        super().__init__()
    
    def get(self, id):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get, {'id': id})
        st = [OrderStatus(id=r[0], title=r[1]) for r in res.fetchall()]
        return st[0]
    
    def get_all(self):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        st = [OrderStatus(id=r[0], title=r[1]) for r in res.fetchall()]
        return st
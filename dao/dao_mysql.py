from sqlalchemy import text, create_engine
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

from dao.dao import DAO
from models import Product, Customer, Order, Category
from config import Config

class CustomerDAOMySQL(DAO):
    pass


class ProductDAOMySQL(DAO):
    _sql_insert = text('INSERT INTO product (title, price, category_id, amount_in_stock) VALUES (:title, :price, :category_id, :amount);')
    _sql_update = text('UPDATE product SET title=:title, price=:price, category_id=:category_id, amount_in_stock=:amnt WHERE id=:id')
    _sql_delete = text('DELETE FROM product WHERE product.id = :id;')
    _sql_get = text('SELECT id, title, price, category_id, amount_in_stock FROM product WHERE product.id = :id')
    _sql_get_all = text('SELECT * FROM product')

    def __init__(self) -> None:
        super().__init__()
        self.db = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    def insert(self, prod: Product):
        with self.db.connect() as c:
            c.execute(
                self._sql_insert, 
                {
                    'title': prod.title, 
                    'price': prod.price, 
                    'category_id': prod.category_id, 
                    'amount': prod.amount_in_stock
                }
            )
            c.commit()
    
    def update(self, id, entity: Product):
        with self.db.connect() as c:
            try:
                res = c.execute(
                    self._sql_update, 
                    {
                    'title': entity.title, 
                    'price': entity.price, 
                    'category_id': entity.category_id, 
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
        prods = [Product(*r) for r in res.fetchall()]
        return prods
    
    def get(self, id):
        with self.db.connect() as c:
            res = c.execute(self._sql_get, {'id': id})
        res_l = res.first()
        if res:
            return Product(
                id= res_l[0],
                title= res_l[1],
                price= res_l[2],
                category_id= res_l[3],
                amount_in_stock= res_l[4]
            )
        return None


class CategoryDAOMySQL(DAO):
    _sql_get_all = text('SELECT * FROM category')
    
    def __init__(self) -> None:
        super().__init__()
        self.db = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    def get_all(self):
        with self.db.engine.connect() as c:
            res = c.execute(self._sql_get_all)
        cats = [Category(*r) for r in res.fetchall()]
        return cats


class OrderDAOMySQL(DAO):
    pass


class OrderItemDAOMySQL(DAO):
    pass


class StatusDAOMySQL(DAO):
    pass
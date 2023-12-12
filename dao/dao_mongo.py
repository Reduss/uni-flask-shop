from dao.dao import DAO
from config import Config
from models import Product, Order, Customer, OrderStatus, Category

from bson import ObjectId
from pymongo import MongoClient


class CustomerDAOMongo(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoClient(Config.MONGO_URI)['sdb_shop']
        self.customer_collection = self.db['customer']
    
    def get_all(self):
        cursor = self.customer_collection.find()
        
        customers = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
            ) for c in cursor]
        return customers


class ProductDAOMongo(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoClient(Config.MONGO_URI)['sdb_shop']
        self.product_collection = self.db['product']
    
    def save(self, entity):
        pass
    
    def update(self, id, entity):
        
        # TODO: impl update
        pass
    
    def delete(self, id):
        pass
    
    def get_all(self):
        cursor = self.product_collection.find()
        cat_dao = CategoryDAOMongo()
        
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=cat_dao.get(c['category_id']).title, 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods
    
    def get(self, id):
        cursor = self.product_collection.find({"_id": ObjectId(id)})
        
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=c['category'], 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods[0]


class CategoryDAOMongo(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoClient(Config.MONGO_URI)['sdb_shop']
        self.category_collection = self.db['category']
    
    def get_all(self):
        cursor = self.category_collection.find()
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats
    
    def get(self, id):
        cursor = self.category_collection.find({"_id": ObjectId(id)})
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats[0]
    
    def get_by_title(self, title):
        cursor = self.category_collection.find({"title": title})
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats[0]


class OrderDAOMongo(DAO):
    pass


class OrderItemDAOMongo(DAO):
    pass


class OrderStatusDAOMongo(DAO):
    pass

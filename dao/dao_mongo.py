from dao.dao import DAO
from config import Config

from pymongo import MongoClient

class CustomerDAOMongo(DAO):
    pass

class ProductDAOMongo(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoClient(Config.MONGO_URI)

    def save(self, entity):
        pass
    
    def update(self, id, entity):
        pass
    
    def delete(self, id):
        pass
    
    def get_all(self):
        bb = self.db['testdb']
        collection = bb['col1'].find_one()
        return collection
    
    def get(self, id):
        pass


class CategoryDAOMongo(DAO):
    pass


class OrderDAOMongo(DAO):
    pass


class OrderItemDAOMongo(DAO):
    pass


class OrderStatusDAOMongo(DAO):
    pass

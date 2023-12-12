from enum import Enum
from abc import ABC, abstractmethod

from dao.dao_mysql import ProductDAOMySQL, CategoryDAOMySQL, CustomerDAOMySQL, OrderDAOMySQL, OrderStatusDAOMySQL
from dao.dao_mongo import ProductDAOMongo, CategoryDAOMongo, CustomerDAOMongo, OrderDAOMongo, OrderStatusDAOMongo


class FactoryType(Enum):
    MYSQL = 0
    MONGO = 1


class AbsDAOFactory(ABC):
    @abstractmethod
    def get_customer_dao(self):
        pass
    
    @abstractmethod
    def get_product_dao(self):
        pass

    @abstractmethod
    def get_order_dao(self):
        pass


class MySQLDAOFactory(AbsDAOFactory):
    def get_customer_dao(self):
        return CustomerDAOMySQL()
    
    def get_product_dao(self):
        return ProductDAOMySQL()

    def get_order_dao(self):
        return OrderDAOMySQL()
    
    def get_category_dao(self):
        return CategoryDAOMySQL()
    
    def get_order_status_dao(self):
        return OrderStatusDAOMySQL()


class MongoDAOFactory(AbsDAOFactory):
    def __init__(self) -> None:
        super().__init__()

    def get_customer_dao(self):
        return CustomerDAOMongo()
    
    def get_product_dao(self):
        return ProductDAOMongo()

    def get_order_dao(self):
        return OrderDAOMongo()
    
    def get_category_dao(self):
        return CategoryDAOMongo()
    
    def get_order_status_dao(self):
        return OrderStatusDAOMongo()

class DAOFactory():
    def __init__(self, factory) -> None:
        if factory == FactoryType.MYSQL:
            self.factory = MySQLDAOFactory()
        elif factory == FactoryType.MONGO:
            self.factory = MongoDAOFactory()
        else:
            raise TypeError(f'Incorrect DBMS type: {self.factory}.')
    
    def get_customer_dao(self):
        return self.factory.get_customer_dao()
    
    def get_product_dao(self):
        return self.factory.get_product_dao()
    
    def get_order_dao(self):
        return self.factory.get_order_dao()
    
    def get_category_dao(self):
        return self.factory.get_category_dao()
    
    def get_order_status_dao(self):
        return self.factory.get_order_status_dao()
from dao.factory import DAOFactory, FactoryType
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config

from pymongo import MongoClient


# factory = DAOFactory(app, FactoryType.MYSQL)
# db = factory.db

def get_mysql_engine():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    return engine
# p_dao = factory.get_product_dao()

def get_mongo_client():
    cl = MongoClient(Config.MONGO_URI)
    return cl

class DBHelper:
    def __init__(self) -> None:
        self.db = None
from dao import DAOFactory, FactoryType
from models import Product, Customer


class DBMigrationTool():
    def __init__(self) -> None:
        self.mysql_factory = DAOFactory(FactoryType.MYSQL)
        self.mongo_factory = DAOFactory(FactoryType.MONGO)
    
    def migrate_to_mongo(self):
        # get all data from mysql
        # insert into mongo
        # keep track of key id's 
        
        # DAOs
        
        category_dao_mysql = self.mysql_factory.get_category_dao()
        category_dao_mongo = self.mongo_factory.get_category_dao()
        
        customer_dao_mysql = self.mysql_factory.get_customer_dao()
        customer_dao_mongo = self.mongo_factory.get_customer_dao()
        
        prod_dao_mysql = self.mysql_factory.get_product_dao()
        prod_dao_mongo = self.mongo_factory.get_product_dao()
        
        status_dao_mysql = self.mysql_factory.get_order_status_dao()
        status_dao_mongo = self.mongo_factory.get_order_status_dao()
        
        order_dao_mysql = self.mysql_factory.get_order_dao()
        order_dao_mongo = self.mongo_factory.get_order_dao()
        
        
        try:
            # migrate customers
            
            print('[mysql -> mongo]: - Migrating customers...')
            
            customers_ids_map = {}
            mysql_customers = customer_dao_mysql.get_all()
            for entry in mysql_customers:
                mongo_insert_result = customer_dao_mongo.insert(entry) 
                customers_ids_map[mongo_insert_result.inserted_id] = entry.id
            
            print('[mysql -> mongo]: - Migrating customers: FINISHED.')
            
            # migrate categories
            
            print('[mysql -> mongo]: - Migrating categories...')
            
            categories_ids_map = {}
            mysql_cats = category_dao_mysql.get_all()
            for entry in mysql_cats:
                mongo_insert_result = category_dao_mongo.insert(entry) 
                categories_ids_map[mongo_insert_result.inserted_id] = entry.id
            
            print('[mysql -> mongo]: - Migrating categories: FINISHED.')
            
            # migrate products
            
            print('[mysql -> mongo]: - Migrating products...')
            
            prod_ids_map = {}
            mysql_prods = prod_dao_mysql.get_all()
            for entry in mysql_prods:
                mongo_insert_result = prod_dao_mongo.insert(entry) 
                prod_ids_map[mongo_insert_result.inserted_id] = entry.id
            
            print('[mysql -> mongo]: - Migrating products: FINISHED.')
            
            # migrate statuses
            
            print('[mysql -> mongo]: - Migrating statuses...')
            
            statuses_ids_map = {}
            mysql_statues = status_dao_mysql.get_all()
            for entry in mysql_statues:
                mongo_insert_result = status_dao_mongo.insert(entry) 
                statuses_ids_map[mongo_insert_result.inserted_id] = entry.id 
            
            print('[mysql -> mongo]: - Migrating statuses: FINISHED.')
            
            # migrate orders
            
            print('[mysql -> mongo]: - Migrating orders...')
            
            order_ids_map = {}
            mysql_orders = order_dao_mysql.get_all()
            for entry in mysql_orders:
                mongo_insert_result = order_dao_mongo.insert(entry) 
                order_ids_map[mongo_insert_result.inserted_id] = entry.id 
            
            print('[mysql -> mongo]: - Migrating orders: FINISHED.')
            
            # migrate customer_order
            
            # fetch order_item and push em into inserted orders
            
        except Exception as e:
            print(f'Error migrating to mongo: {e}')

    def migrate_to_mysql():
        pass
    
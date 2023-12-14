from typing import List
from dao.factory import FactoryType, DAOFactory
from models import Product, Customer, Order


class DBMigrationTool():
    def __init__(self) -> None:
        self.mysql_factory = DAOFactory(FactoryType.MYSQL)
        self.mongo_factory = DAOFactory(FactoryType.MONGO)
        
        self.category_dao_mysql = self.mysql_factory.get_category_dao()
        self.category_dao_mongo = self.mongo_factory.get_category_dao()
        
        self.customer_dao_mysql = self.mysql_factory.get_customer_dao()
        self.customer_dao_mongo = self.mongo_factory.get_customer_dao()
        
        self.prod_dao_mysql = self.mysql_factory.get_product_dao()
        self.prod_dao_mongo = self.mongo_factory.get_product_dao()
        
        self.status_dao_mysql = self.mysql_factory.get_order_status_dao()
        self.status_dao_mongo = self.mongo_factory.get_order_status_dao()
        
        self.order_dao_mysql = self.mysql_factory.get_order_dao()
        self.order_dao_mongo = self.mongo_factory.get_order_dao()
    
    def migrate_to_mongo(self):
        try:
            # migrate customers
            
            print('[mysql -> mongo]: - Migrating customers...')
            
            customers_ids_map = {}
            mongo_customers = self.customer_dao_mysql.get_all()
            for entry in mongo_customers:
                mongo_insert_result = self.customer_dao_mongo.insert(entry) 
                customers_ids_map[entry.id] = str(mongo_insert_result.inserted_id)
            
            print('[mysql -> mongo]: - Migrating customers: FINISHED.')
            
            # migrate categories
            
            print('[mysql -> mongo]: - Migrating categories...')
            
            categories_ids_map = {}
            mysql_cats = self.category_dao_mysql.get_all()
            for entry in mysql_cats:
                mongo_insert_result = self.category_dao_mongo.insert(entry) 
                categories_ids_map[entry.id] = str(mongo_insert_result.inserted_id)
            
            print('[mysql -> mongo]: - Migrating categories: FINISHED.')
            
            # migrate products
            
            print('[mysql -> mongo]: - Migrating products...')
            
            prod_ids_map = {}
            mysql_prods = self.prod_dao_mysql.get_all()
            for entry in mysql_prods:
                mongo_insert_result = self.prod_dao_mongo.insert(entry) 
                prod_ids_map[entry.id] = str(mongo_insert_result.inserted_id)
            
            print('[mysql -> mongo]: - Migrating products: FINISHED.')
            
            # migrate statuses
            
            print('[mysql -> mongo]: - Migrating statuses...')
            
            statuses_ids_map = {}
            mysql_statues = self.status_dao_mysql.get_all()
            for entry in mysql_statues:
                mongo_insert_result = self.status_dao_mongo.insert(entry) 
                statuses_ids_map[entry.id] = mongo_insert_result.inserted_id 
            
            print('[mysql -> mongo]: - Migrating statuses: FINISHED.')
            
            # migrate orders
            
            print('[mysql -> mongo]: - Migrating orders...')
            
            order_ids_map = {}
            mysql_orders: List[Order] = self.order_dao_mysql.get_all()

            for entry in mysql_orders:
                # remap customer's mysql ids to mongo ids
                if entry.customer.id in customers_ids_map.keys():
                    entry.customer.id = customers_ids_map[entry.customer.id]
                
                #remap products mysql ids to mongo ids
                for prod, amount in entry.products.items():
                    prod.id = prod_ids_map.get(prod.id)
                
                
                mongo_insert_result = self.order_dao_mongo.insert(entry) 
                order_ids_map[entry.id] = mongo_insert_result.inserted_id
            
            print('[mysql -> mongo]: - Migrating orders: FINISHED.')
            
            print('[mysql -> mongo]: - MIGRATION FINISHED.')
        except Exception as e:
            print(f'Error migrating to mongo: {e}')

    def migrate_to_mysql(self):
        try:
            # migrate customers
            
            print('[mongo -> mysql]: - Migrating customers...')
            
            customers_ids_map = {}
            mongo_customers = self.customer_dao_mongo.get_all()
            for entry in mongo_customers:
                insert_result = self.customer_dao_mysql.insert(entry)
                customers_ids_map[entry.id] = str(insert_result)
            
            print('[mongo -> mysql]: - Migrating customers: FINISHED.')
            
            # migrate categories
            
            print('[mongo -> mysql]: - Migrating categories...')
            
            categories_ids_map = {}
            mongo_cats = self.category_dao_mongo.get_all()
            for entry in mongo_cats:
                insert_result = self.category_dao_mysql.insert(entry)
                categories_ids_map[entry.id] = str(insert_result)
            
            print('[mongo -> mysql]: - Migrating categories: FINISHED.')
            
            # migrate statuses
            
            print('[mongo -> mysql]: - Migrating statuses...')
            
            statuses_ids_map = {}
            mongo_stats = self.status_dao_mongo.get_all()
            for entry in mongo_stats:
                insert_result = self.status_dao_mysql.insert(entry)
                statuses_ids_map[entry.id] = str(insert_result)
            
            print('[mongo -> mysql]: - Migrating statuses: FINISHED.')
            
            # migrate products
            
            print('[mongo -> mysql]: - Migrating products...')
            
            prods_ids_map = {}
            mongo_prods = self.prod_dao_mongo.get_all()
            for entry in mongo_prods:
                insert_result = self.prod_dao_mysql.insert(entry)
                prods_ids_map[entry.id] = str(insert_result)
            
            print('[mongo -> mysql]: - Migrating products: FINISHED.')
            
            
            # migrate orders
            
            print('[mongo -> mysql]: - Migrating orders...')
            
            ords_ids_map = {}
            mongo_ords = self.order_dao_mongo.get_all()
            
            for entry in mongo_ords:
                # remap order.customer_id to mysql id's
                if entry.customer.id in customers_ids_map.keys():
                    entry.customer.id = customers_ids_map.get(entry.customer.id)
                
                # remap order.products id's to mysql id's
                for prod in entry.products.keys():
                    if prod.id in prods_ids_map.keys():
                        prod.id = prods_ids_map.get(prod.id)
                
                insert_result = self.order_dao_mysql.insert_with_items(entry)
                ords_ids_map[entry.id] = str(insert_result)
            
            print('[mongo -> mysql]: - Migrating orders: FINISHED.')
            
            print('[mongo -> mysql]: - MIGRATION FINISHED.')
            
        except Exception as e:
            print(f'Error migrating to mysql: {e}')


migration_tool = DBMigrationTool()
migration_tool.migrate_to_mongo()
import time

from db_migration import DBMigrationTool
from db_performace import DbPerformanceTester
from dao.factory import FactoryType
from dao.dao_mysql import CustomerDAOMySQL
from dao.dao_mongo import CustomerDAOMongo
from models import Customer



#
#   === DB MIGRATION ===
#


# migration_tool = DBMigrationTool()
# migration_tool.migrate_to_mysql()


#
#   === DB TESTING ===
# 

ENTITY_AMOUNTS = [100, 1000, 10000, 50000, 100000]
db = DbPerformanceTester(FactoryType.MONGO)

@DbPerformanceTester.time_elapsed_decor
def init(amount):
    print("Creating objects...")
    db.generate_data(amount)

@DbPerformanceTester.time_elapsed_decor
def get_by_fname_check():
    prod = db.get_random_customer()
    print(f"- Looking for customer with fname={prod.first_name}...")
    return db.dao.get_by_fname(prod.first_name)

@DbPerformanceTester.time_elapsed_decor
def get_by_full_name_check():
    prod = db.get_random_customer()
    print(f"- Looking for the customer with fname={prod.first_name} and lname={prod.last_name}...")
    return db.dao.get_by_full_name(prod.first_name, prod.last_name)



results = {}

for amount in ENTITY_AMOUNTS:
    a, i_elapsed = init(amount)
    print(f"{amount} objects created in {i_elapsed} seconds.")
    print('Running tests...')
    prod, elapsed = get_by_full_name_check()
    print(f'- Customer found: {prod}')
    results[amount] = elapsed

print('Results:')

for k, v in results.items():
    print(f'- # of entities: {k}, time elapsed: {v} seconds.')




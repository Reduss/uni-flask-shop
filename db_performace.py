from dao.factory import FactoryType, DAOFactory
from models import Customer, Product

import random
import time

class DbPerformanceTester:
    def __init__(self, dbms_type) -> None:
        self.factory = DAOFactory(dbms_type)
        self.dao_c = self.factory.get_customer_dao()
        self.dao_p = self.factory.get_product_dao()
        self.dao_cat = self.factory.get_category_dao()
        self.customers = []
        self.prods = []
    
    def generate_data_customer(self, amount):
        self.dao_c.delete_all()
        for it in range(amount):
            c = self._generate_random_customer()
            self.customers.append(c)
            if it % 100 == 0:
                print(f"- Inserting customers: {it}")
            self.dao_c.insert(c)
    
    def generate_data_prod(self, amount):
        self.dao_p.delete_all()
        for it in range(amount):
            prod = self._generate_random_product()
            self.prods.append(prod)
            if it % 100 == 0:
                print(f"- Inserting products: {it}")
            self.dao_p.insert(prod)
    
    def _generate_random_customer(self):
        fname = 'fname' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        lname = 'lname' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        phone = '+38' + ''.join(str(random.randint(0, 9)) for _ in range(10))
        addr = 'addr' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        return Customer(id=-1, f_name=fname, l_name=lname, phone_num=phone, address=addr)

    def _generate_random_product(self):
        cats = self.dao_cat.get_all()
        title = 'prod' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        price = random.randint(0, 1000)
        category = random.choice(cats).title
        amount = random.randint(0, 100)
        return Product(id=-1, title=title, price=price, category=category, amount_in_stock=amount)


    def get_random_customer(self):
        return self.dao_c.get_random()
    
    @staticmethod
    def time_elapsed_decor(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            return result, elapsed_time
        return wrapper
        


#
#   === DB TESTING ===
# 

def run():

    ENTITY_AMOUNTS = [100, 1000, 10000, 50000, 100000]
    DBMS_TYPE = FactoryType.MONGO

    db = DbPerformanceTester(DBMS_TYPE)

    @DbPerformanceTester.time_elapsed_decor
    def init(amount):
        print("Creating objects...")
        db.generate_data_customer(amount)

    @DbPerformanceTester.time_elapsed_decor
    def get_by_fname_check():
        prod = db.get_random_customer()
        print(f"- Looking for customer with fname={prod.first_name}...")
        return db.dao_c.get_by_fname(prod.first_name)

    @DbPerformanceTester.time_elapsed_decor
    def get_by_full_name_check():
        prod = db.get_random_customer()
        print(f"- Looking for the customer with fname={prod.first_name} and lname={prod.last_name}...")
        return db.dao_c.get_by_full_name(prod.first_name, prod.last_name)



    results = {}

    for amount in ENTITY_AMOUNTS:
        print(f'Querying {DBMS_TYPE} database')
        a, i_elapsed = init(amount)
        print(f"{amount} objects created in {i_elapsed} seconds.")
        print('Running tests...')
        prod, elapsed = get_by_full_name_check()
        print(f'- Customer found: {prod}')
        results[amount] = elapsed

    print('Results:')

    for k, v in results.items():
        print(f'- # of entities: {k}, time elapsed: {v} seconds.')


if __name__ == '__main__':
    run()


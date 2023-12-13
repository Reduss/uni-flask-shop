from dao.factory import FactoryType, DAOFactory
from models import Customer

import random
import time

class DbPerformanceTester:
    def __init__(self, dbms_type) -> None:
        self.factory = DAOFactory(dbms_type)
        self.dao = self.factory.get_customer_dao()
        self.customers = []
    
    def generate_data(self, amount):
        self.dao.delete_all()
        for _ in range(amount):
            prod = self._generate_random_customer()
            self.dao.insert(prod)
        # self.customers = self.dao.get_all()
    
    
    def _generate_random_customer(self):
        fname = 'fname' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        lname = 'lname' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        phone = '+38' + ''.join(str(random.randint(0, 9)) for _ in range(10))
        addr = 'addr' + ''.join(str(random.randint(0, 9)) for _ in range(4))
        return Customer(id=-1, f_name=fname, l_name=lname, phone_num=phone, address=addr)

    def get_random_customer(self):
        return self.dao.get_random()
        return random.choice(self.customers)
    
    @staticmethod
    def time_elapsed_decor(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            return result, elapsed_time
        return wrapper
        

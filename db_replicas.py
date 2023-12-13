from dao.factory import FactoryType
from dao.dao_mongo import CustomerDAOMongo
from db_performace import DbPerformanceTester


dao = CustomerDAOMongo()
dbtool = DbPerformanceTester(FactoryType.MONGO)

dbtool.generate_data_customer(10000)
cs = dbtool.dao_c.get_all()

print(f'Resulting lens:')
print(len(cs))
print(len(dbtool.customers))



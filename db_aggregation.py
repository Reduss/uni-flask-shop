from db_performace import DbPerformanceTester
from dao.factory import FactoryType
from dao.dao_mongo import ProductDAOMongo

dao = ProductDAOMongo()
dbtool = DbPerformanceTester(FactoryType.MONGO)

dbtool.generate_data_prod(100)



@DbPerformanceTester.time_elapsed_decor
def get_test(id):
    return dbtool.dao_p.get(id)

@DbPerformanceTester.time_elapsed_decor
def aggr_get_test(id):
    return dbtool.dao_p.aggr_get(id)


@DbPerformanceTester.time_elapsed_decor
def aggr_price(min, max):
    return dbtool.dao_p.aggr_get_price_in_range(min, max)

@DbPerformanceTester.time_elapsed_decor
def price(min, max):
    return dbtool.dao_p.get_price_in_range(min, max)


@DbPerformanceTester.time_elapsed_decor
def aggr_amount(amount):
    return dbtool.dao_p.aggr_get_amount_less_then(amount)

@DbPerformanceTester.time_elapsed_decor
def amount(amount):
    return dbtool.dao_p.get_amount_less_than(amount)


@DbPerformanceTester.time_elapsed_decor
def aggr_group_by_category():
    return dbtool.dao_p.aggr_group_by_category()

@DbPerformanceTester.time_elapsed_decor
def group_by_category():
    return dbtool.dao_p.group_by_category()


@DbPerformanceTester.time_elapsed_decor
def aggr_avg_price():
    return dbtool.dao_p.aggr_get_avg_price_by_category()

@DbPerformanceTester.time_elapsed_decor
def avg_price():
    return dbtool.dao_p.get_avg_price_by_category()


# ======= get =======
print("- Get ")

gp, gt = get_test(dao.get_random().id)
a_gp, a_gt = aggr_get_test(dao.get_random().id)

print(f'Time: {gt}')
print(f'Time: {a_gt} (aggregation)')

# ======= amount less than =======
print("- Amount less than")
ap, at = amount(10)
a_ap, a_at = aggr_amount(10)

print(f'Time: {at}')
print(f'Time: {a_at} (aggregation)')

# =======price in range=======
print("- Price in range")
price_prod, price_time = price(10, 50)
ag_price_prod, ag_price_time = aggr_price(10, 50)

print(f'Time: {price_time}')
print(f'Time: {ag_price_time} (aggregation)')

# ======= num of prods by category =======
print("- Entries by category")

d, dt = group_by_category()
a_d, a_dt = aggr_group_by_category()

print(f'Time: {dt}')
print(f'Time: {a_dt} (aggregation)')


# ======= avg price and prod count by category =======
print("- Avg price")

avg, avgt = avg_price()
a_avg, a_avgt = aggr_avg_price()

print(f'Time: {avgt}')
print(f'Time: {a_avgt} (aggregation)')


print("- Finished")
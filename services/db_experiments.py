from dao.factory import FactoryType, DAOFactory


entity_amounts = [100, 1000, 10000, 50000, 100000, 500000]

factory = DAOFactory(FactoryType.MYSQL)

product_dao = factory.get_product_dao()
category_dao = factory.get_category_dao()
customer_dao = factory.get_customer_dao()
order_dao = factory.get_order_dao()
status_dao = factory.get_order_status_dao()


# add entity_amounts of customers MYSQL + MONGO

# update/insert(?) and select time to complete MYSQL + MONGO
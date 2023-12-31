from dao.dao import DAO
from config import Config
from models import Product, Order, Customer, OrderStatus, Category, Cart

from bson import ObjectId
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern
from datetime import datetime

from utils import catch_error

class MongoConnection():
    def __init__(self) -> None:
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client['sdb_shop']



class CustomerDAOMongo(DAO, MongoConnection):
    def __init__(self) -> None:
        super().__init__()
        self.customer_collection = self.db['customer']

    def insert(self, customer: Customer):
        res = self.customer_collection.with_options(write_concern=WriteConcern(w='majority', wtimeout=1000, j=True)).insert_one(
            {
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_num": customer.phone_num,
                "addr": customer.address
            }
        )
        return res
    
    def update(self, id, entity: Customer):
        self.customer_collection.update_one(
            { 
                "_id": ObjectId(id)
            },
            { 
                '$set' : 
                {
                    "first_name": entity.first_name,
                    "last_name": entity.last_name,
                    "phone_num": entity.phone_num,
                    "addr": entity.address
                }
            }
        )
    
    def delete_all(self):
        return self.customer_collection.drop()
    
    def insert_indexes(self):
        self.customer_collection.create_index([('first_name', 1)])
        self.customer_collection.create_index([('last_name', 1)])
    
    def get_indexes(self):
        return self.customer_collection.index_information()
    
    def get_all(self):
        cursor = self.customer_collection.find()
        
        customers = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
        ) for c in cursor]
        return customers
    
    def get(self, id):
        cursor = self.customer_collection.find({"_id": ObjectId(id)})
        
        cust = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
        ) for c in cursor]
        return cust[0]
    
    def get_by_fname(self, fname):
        cursor = self.customer_collection.find({"first_name": fname})
        cust = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
        ) for c in cursor]
        return cust[0]

    def get_random(self):
        cursor = self.customer_collection.aggregate([{"$sample": {"size": 1}}])
        
        cust = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
        ) for c in cursor]
        return cust[0]

    def get_by_full_name(self, fname, lname):
        cursor = self.customer_collection.find({"first_name": fname, "last_name": lname})
        cust = [Customer(
            id=str(c['_id']), 
            f_name=c['first_name'], 
            l_name=c['last_name'], 
            phone_num=c['phone_num'], 
            address=c['addr']
        ) for c in cursor]
        return cust[0]

    def get_entities_count(self):
        return self.customer_collection.count_documents({})



class ProductDAOMongo(DAO, MongoConnection):
    def __init__(self) -> None:
        super().__init__()
        self.product_collection = self.db['product']
        self.category_dao = CategoryDAOMongo()

    def insert(self, entity):
        res = self.product_collection.insert_one(
            {
                "title": entity.title,
                "price": float(entity.price),
                "amount_in_stock": entity.amount_in_stock,
                "category_id": self.category_dao.get_by_title(entity.category).id
            }
        )
        return res
    
    def update(self, id, entity: Product):
        self.product_collection.update_one(
            { 
                "_id": ObjectId(id)
            },
            { 
                '$set' : 
                {
                    "title": entity.title,
                    "price": float(entity.price),
                    "amount_in_stock": entity.amount_in_stock,
                    "category_id": self.category_dao.get_by_title(entity.category).id
                }
            }
            
        )
    
    def delete(self, id):
        pass
    
    def delete_all(self):
        return self.product_collection.drop()
    
    def get_all(self):
        cursor = self.product_collection.find()
        
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=self.category_dao.get(c['category_id']).title, 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods
    
    def get(self, id):
        cursor = self.product_collection.find({"_id": ObjectId(id)})
        
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=self.category_dao.get(c['category_id']).title, 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods[0]
    
    def group_by_category(self):
        prods = self.get_all()
        res = {}
        
        for p in prods:
            cat = p.category
            res.setdefault(cat, 0)
            res[cat] += 1
        return res
    
    def get_avg_price_by_category(self):
        prods = self.get_all()
        res = {}

        category_totals = {}

        for p in prods:
            cat = p.category

            category_totals.setdefault(cat, {"total_price": 0, "count": 0})
            category_totals[cat]["total_price"] += p.price  
            category_totals[cat]["count"] += 1

        result_list = []
        for cat, totals in category_totals.items():
            if totals["count"] > 0:
                average_price = totals["total_price"] / totals["count"]
                result_list.append((cat, average_price, totals["count"]))

        return result_list
    
    def get_price_in_range(self, min, max):
        prods = self.get_all()
        res = []
        for p in prods:
            if p.price >= min and p.price <= max:
                res.append(p)
        return res
    
    def get_amount_less_than(self, value):
        prods = self.get_all()
        res = []
        for p in prods:
            if p.amount_in_stock <= value:
                res.append(p)
        return res
    
    def get_random(self):
        cursor = self.product_collection.aggregate([{"$sample": {"size": 1}}])
        
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=self.category_dao.get(c['category_id']).title, 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods[0]


    def aggr_get(self, id):
        cursor = self.product_collection.aggregate([
            {
                "$match": {"_id": ObjectId(id)}
            }])
        prods = [Product(
            id=str(c['_id']), 
            title=c['title'], 
            price=float(c['price']), 
            category=self.category_dao.get(c['category_id']).title, 
            amount_in_stock=int(c['amount_in_stock'])
            ) for c in cursor]
        return prods[0]
    
    def aggr_group_by_category(self):
        cursor = self.product_collection.aggregate([
            {
                '$group': {
                    '_id': '$category_id',
                    'count': { '$sum': 1 }
                }
            },
            {
                '$project': {
                    'category_id': '$_id',
                    'count': 1,
                    '_id': 0
                }
            }
        ])
        res = {self.category_dao.get(c["category_id"]).title: c["count"] for c in cursor}
        return res
    
    def aggr_get_price_in_range(self, min, max):
        cursor = self.product_collection.aggregate([
            {
                '$match': {
                    'price': {
                        '$gte': min,
                        '$lt': max
                    }
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'title': 1,
                    'price': 1,
                    'amount_in_stock': 1,
                    'category_id': 1
                }
            }
        ])
        prods = [
            Product(
                id=str(c['_id']),
                title=c['title'],
                price=float(c['price']),
                category=self.category_dao.get(c['category_id']).title,
                amount_in_stock=int(c['amount_in_stock'])
        ) for c in cursor]
        return prods

    def aggr_get_amount_less_then(self, amount):
        cursor = self.product_collection.aggregate([
            {
                '$match': {
                    'amount_in_stock': { '$lt': amount }
                }
            },
            {
                '$project': {
                    'id': 1,
                    'title': 1,
                    'amount_in_stock': 1,
                    'price': 1,
                    'category_id': 1,
                }
            }
        ])
        prods = [
            Product(
                id=str(c['_id']),
                title=c['title'],
                price=float(c['price']),
                category=self.category_dao.get(c['category_id']).title,
                amount_in_stock=int(c['amount_in_stock'])
        ) for c in cursor]
        return prods

    def aggr_get_avg_price_by_category(self):
        cursor = self.product_collection.aggregate([
        {
            '$group': {
                '_id': '$category_id',
                'averagePrice': { '$avg': '$price' },
                'productCount': { '$sum': 1 }
            }
        },
        {
            '$project': {
                '_id': 1,
                'category_id': 1,
                'averagePrice': 1,
                'productCount': 1
            }
        }
        ])
        res = []

        for c in cursor:
            cat = self.category_dao.get(c['_id']).title
            price = c['averagePrice']
            count = c['productCount']
            res.append((cat, price, count))
        return res
        

class CategoryDAOMongo(DAO, MongoConnection):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoClient(Config.MONGO_URI)['sdb_shop']
        self.category_collection = self.db['category']
    
    def insert(self, entity):
        res = self.category_collection.insert_one(
            {
                "title": entity.title,
            }
        )
        return res
    
    def get_all(self):
        cursor = self.category_collection.find()
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats
    
    def get(self, id):
        cursor = self.category_collection.find({"_id": ObjectId(id)})
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats[0]
    
    def get_by_title(self, title):
        cursor = self.category_collection.find({"title": title})
        
        cats = [Category(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return cats[0]



class OrderDAOMongo(DAO, MongoConnection):
    def __init__(self) -> None:
        super().__init__()
        self.order_collection = self.db['order']
        self.status_dao = OrderStatusDAOMongo()
        self.product_dao = ProductDAOMongo()
        self.customer_dao = CustomerDAOMongo()
    
    def insert(self, entity: Order):
        products = []
        for k, v in entity.products.items():
            products.append(
                { 
                    "product_id" : k.id,
                    "amount" : v,
                    "price" : k.price,
                })
        res = self.order_collection.insert_one(
            {
                "customer_id": str(entity.customer.id),
                "status_id":  self.status_dao.get_by_title(entity.status).id,
                "order_date": str(entity.order_date),
                "total_price": entity.total_price,
                "products": products,
            }
        )
        return res
    
    def place_order(self,customer: Customer, cart: Cart):
        try:
            # insret customer
            self.customer_dao.insert(customer)
            
            # insert order
            cust_id = self.customer_dao.get_all()[-1].id
            order_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            total_price = sum(p.price*a for p, a in cart.prods.items())
            products = []
            for k, v in cart.prods.items():
                products.append(
                    { 
                        "product_id" : k.id,
                        "amount" : v,
                        "price" : k.price,
                    })
            try:
                res = self.order_collection.insert_one(
                    {
                        'customer_id': cust_id,
                        'status_id': self.status_dao.get_by_title("New").id,
                        'order_date': order_date,
                        'total_price': total_price,
                        'products': products
                    }
                )
            except Exception as e:
                print(f'Couldnt create order object: {e}')
            # update stock product amount 
            try:
                for k, v in cart.prods.items():
                    p = Product(
                        id=k.id,
                        title=k.title,
                        price=k.price,
                        category=k.category,
                        amount_in_stock=k.amount_in_stock - v,
                    )
                    self.product_dao.update(k.id, p)
            except Exception as e:
                print(f'Couldnt update stock amount: {e}')
        except Exception as e:
            print(f"Error while creating order: {e}")
    
    def get_all(self):
        cursor = self.order_collection.find()
        
        orders = []
        for c in cursor:
            ord = Order(
                id = str(c["_id"]),
                customer = self.customer_dao.get(c["customer_id"]),
                status = self.status_dao.get(c["status_id"]).title,
                order_date = c["order_date"],
                total_price = c["total_price"],
                products = {},
            )
            
            for p in c["products"]:
                prod = self.product_dao.get(p['product_id'])
                prod.price = p["price"]
                amount = p["amount"]
                ord.products[prod] = amount
            orders.append(ord)
        return orders



class OrderStatusDAOMongo(DAO, MongoConnection):
    def __init__(self) -> None:
        super().__init__()
        self.status_collection = self.db['order_status']
    
    def insert(self, entity):
        res = self.status_collection.insert_one(
            {
                "title": entity.title,
            }
        )
        return res
    
    def get(self, id):
        cursor = self.status_collection.find({"_id": ObjectId(id)})
        st = [OrderStatus(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return st[0]
    
    def get_all(self):
        cursor = self.status_collection.find()
        st = [OrderStatus(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return st
    
    def get_by_title(self, title):
        cursor = self.status_collection.find({"title": title})
        
        ords = [OrderStatus(
            id=str(c['_id']), 
            title=c['title'], 
            ) for c in cursor]
        return ords[0]


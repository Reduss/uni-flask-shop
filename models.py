class Product:
    def __init__(self, id, title, price, category_id, amount_in_stock, category_value='no_value') -> None:
        self.id = id
        self.title = title
        self.price = price
        self.category_id = category_id
        self.amount_in_stock = amount_in_stock
        self.category_value = category_value
    
    def __repr__(self) -> str:
        return f'Product object. Id: {self.id}; title: {self.title}; price: {self.price}; amount: {self.amount_in_stock}:'
    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)

class Category:
    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title
    
    def __repr__(self) -> str:
        return f'Category object. Id: {self.id}; Title: {self.title}'


class Customer:
    def __init__(self, id, f_name, l_name, phone_num, address) -> None:
        self.id = id
        self.first_name = f_name
        self.last_name = l_name
        self.phone_num = phone_num
        self.address = address
    

class Order:
    def __init__(self, id, customer_id, status_id, order_date, total_price) -> None:
        self.id = id
        self.customer_id = customer_id
        self.status_id = status_id
        self.order_date = order_date
        self.total_price = total_price

class OrderStatus:
    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title

class OrderItem:
    def __init__(self, id, order_id, prod_id, amount, price) -> None:
        self.id = id
        self.order_id = order_id
        self.product_id = prod_id
        self.amount = amount
        self.price = price


class Cart():
    def __init__(self) -> None:
        self.prods = {}
    
    def get_items(self):
        return self.prods.items()
    
    def add_product(self, prod: Product, amount):
        if prod not in self.prods:
            self.prods[prod] = amount
    
    def remove_product(self, prod, amount):
        if prod in self.prods and self.prods[prod] > 1:
            self.prods[prod] = self.prods[prod] - amount
        elif prod in self.prods and self.prods[prod] == 1:
            del self.prods[prod]

    def inc(self, prod: Product, amount):
        if prod in self.prods and self.prods[prod] < prod.amount_in_stock:
            self.prods[prod] = self.prods[prod] + amount
    
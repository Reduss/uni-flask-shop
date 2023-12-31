class Product:
    def __init__(self, id, title, price, category, amount_in_stock) -> None:
        self.id = id
        self.title = title
        self.price = price
        self.category = category
        self.amount_in_stock = amount_in_stock
    
    def __repr__(self) -> str:
        return f'Product object. Id: {self.id}; title: {self.title}; price: {self.price}; stock_amount: {self.amount_in_stock}; category: {self.category};'
    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)


class Customer:
    def __init__(self, id, f_name, l_name, phone_num, address) -> None:
        self.id = id
        self.first_name = f_name
        self.last_name = l_name
        self.phone_num = phone_num
        self.address = address
    
    def __repr__(self) -> str:
        return f'Customer object: Id: {self.id}; fname: {self.first_name}; lname: {self.last_name}; phone: {self.phone_num}; address: {self.address};'

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.first_name == other.first_name
        return False

class Order:
    def __init__(self, id, customer, status, order_date, total_price, products={}) -> None:
        self.id = id
        self.customer = customer
        self.status = status
        self.order_date = order_date
        self.total_price = total_price
        self.products = products
    
    def __repr__(self) -> str:
        return f"""Order object. 
            Id: {self.id}; 
            status: {self.status}; 
            date: {self.order_date}; 
            price: {self.total_price}; 
            customer: {self.customer};
            prods: {self.products}"""


class Category:
    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title
    
    def __repr__(self) -> str:
        return f'Category object. Id: {self.id}; Title: {self.title}'


class OrderStatus:
    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title


class Cart():
    def __init__(self) -> None:
        self.prods = {}
    
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
    
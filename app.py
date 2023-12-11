from flask import Flask, render_template, redirect, request, session, url_for
from sqlalchemy import text

from dao.dao import DAO 
from models import Product, Category, Customer, Order, Cart
from forms import NewProductForm, UpdateProductForm, CustomerInfoForm
from dao.factory import DAOFactory, FactoryType
from config import Config
from db import get_mysql_engine, get_mongo_client



app = Flask(__name__)
app.config.from_object(Config)


factory = DAOFactory(FactoryType.MYSQL)
cart = Cart()
product_dao = factory.get_product_dao()
category_dao = factory.get_category_dao()
customer_dao = factory.get_customer_dao()
order_dao = factory.get_order_dao()
order_item_dao = factory.get_order_item_dao()


@app.route('/')
def index():
    prods = product_dao.get_all()
    cats = category_dao.get_all()
    available_prods = list(filter(lambda p: p.amount_in_stock > 0, prods))
    
    return render_template('index.html', products=available_prods, categories=cats)


@app.route('/cart', methods = ['GET', 'POST'])
def cart_view():
    cust_form = CustomerInfoForm()
    prods = product_dao.get_all()
    print([l for l in cart.prods])
    if cust_form.validate_on_submit() and cart.prods.__len__() > 0:        
        c = Customer(
            id=-1,
            f_name=cust_form.f_name.data,
            l_name=cust_form.l_name.data,
            phone_num=cust_form.phone.data,
            address=cust_form.address.data,
        )
        order_dao.place_order(c, cart)
        cart.prods = {}
        return redirect(url_for('index'))
    else:
        print('order not placed')
        print(cust_form.errors)
        print([l for l in cart.prods])
        
    return render_template('cart.html', cart=cart, products=prods, form=cust_form)


@app.route('/add_to_cart/<int:product_id>/<int:quantity>')
def add_to_cart(product_id, quantity):
    cart.add_product(product_dao.get(product_id), quantity)
    return redirect(url_for('index'))


@app.route('/cart_inc/<int:product_id>/<int:quantity>')
def cart_increase_amount(product_id, quantity):
    cart.inc(product_dao.get(product_id), quantity)
    
    return redirect(url_for('cart_view'))


@app.route('/cart_dec/<int:product_id>/<int:quantity>')
def cart_decrease_amount(product_id, quantity):
    cart.remove_product(product_dao.get(product_id), quantity)
    prods = product_dao.get_all()
    
    return redirect(url_for('cart_view'))


@app.route('/admin')
def admin_index():
    ords = order_dao.get_all()
    ord_its = order_item_dao.get_all()
    customers = customer_dao.get_all()
    prods = product_dao.get_all()
    print(len(ord_its))
    for p in ord_its:
        print('item')
        print(p.id, p.order_id, p.product_id)
    
    
    return render_template('admin/orders.html', orders=ords, order_items=ord_its, customers=customers, products=prods)


@app.route('/admin/products', methods = ['GET', 'POST'])
def admin_products():
    form = NewProductForm()
    prods = product_dao.get_all()
    cats = category_dao.get_all()
    form.category.choices = [(cat.id, cat.title) for cat in cats or []]
    
    if form.validate_on_submit():
        prod = Product(
            id=-1,
            title=form.title.data,
            price=form.price.data,
            category_id=form.category.data,
            amount_in_stock=form.amount.data,
        )
        product_dao.insert(prod)
        return redirect('/admin/products')
    else:
        print(form.errors)
    return render_template('admin/products.html', products=prods, categories=cats ,form=form)


@app.route('/admin/products/update/<int:product_id>', methods = ['GET', 'POST'])
def admin_product_update(product_id):
    # TODO: fix update
    prod_to_upd = product_dao.get(product_id)
    cats = category_dao.get_all()
    form = UpdateProductForm(
        title = prod_to_upd.title,
        price = prod_to_upd.price,
        category = prod_to_upd.category_id,
        amount = prod_to_upd.amount_in_stock,
    )
    
    form.category.choices = [(cat.id, cat.title) for cat in cats or []]
    
    if form.validate_on_submit():
        
        prod = Product(
            id=-1,
            title=form.title.data,
            price=form.price.data,
            category_id=form.category.data,
            amount_in_stock=form.amount.data,
        )
        print('Printing prod to update')
        print(prod)
        product_dao.update(product_id, prod)
        return redirect('/admin/products')
    else:
        print(form.errors)
    return render_template('admin/update.html', form=form, product_id=product_id)


@app.route('/admin/customers')
def admin_customers():
    customers = customer_dao.get_all()
    return render_template('admin/customers.html', customers=customers)


if __name__ == '__main__':
    app.run(debug=True)

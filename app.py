from flask import Flask, render_template, redirect, request, session, url_for
from sqlalchemy import text

from dao.dao import DAO 
from models import Product, Category, Customer, Order, Cart
from forms import NewProductForm, UpdateProductForm, CustomerInfoForm
from dao.factory import DAOFactory, FactoryType
from config import Config
from db import get_mysql_engine, get_mongo_client


#
# init
#
app = Flask(__name__)
app.config.from_object(Config)

#
# dao init
#
factory = DAOFactory(FactoryType.MYSQL)
cart = Cart()
p_dao: DAO = factory.get_product_dao()
cat_dao: DAO = factory.get_category_dao()




@app.route('/')
def index():
    prods = p_dao.get_all()
    return render_template('index.html', products=prods)


@app.route('/cart', methods = ['GET', 'POST'])
def cart_view():
    cust_form = CustomerInfoForm()
    print([l for l in cart.prods])
    if cust_form.validate_on_submit() and cart.prods.__len__() > 0:
        print(f'order placed: {cart}')
        print([l for l in cart.prods])
        
        return redirect(url_for('index'))
    else:
        print('order not placed')
        print(cust_form.errors)
        print([l for l in cart.prods])
        
    return render_template('cart.html', cart=cart, form=cust_form)

@app.route('/add_to_cart/<int:product_id>/<int:quantity>')
def add_to_cart(product_id, quantity):
    cart.add_product(p_dao.get(product_id), quantity)
    return redirect(url_for('index'))


@app.route('/cart_inc/<int:product_id>/<int:quantity>')
def cart_increase_amount(product_id, quantity):
    cart.inc(p_dao.get(product_id), quantity)
    return redirect(url_for('cart_view'))

@app.route('/cart_dec/<int:product_id>/<int:quantity>')
def cart_decrease_amount(product_id, quantity):
    cart.remove_product(p_dao.get(product_id), quantity)
    return redirect(url_for('cart_view'))

@app.route('/m')
def index_mongo():
    prod = p_dao.get(0)
    
    return(f'{prod}')

@app.route('/admin')
def admin_index():
    return render_template('admin/orders.html')

@app.route('/admin/products', methods = ['GET', 'POST'])
def admin_products():
    form = NewProductForm()
    prods = p_dao.get_all()
    cats = cat_dao.get_all()
    form.category.choices = [(cat.id, cat.title) for cat in cats or []]
    if form.validate_on_submit():
        prod = Product(
            id=-1,
            title=form.title.data,
            price=form.price.data,
            category_id=form.category.data,
            amount_in_stock=form.amount.data,
        )
        p_dao.insert(prod)
        return redirect('/admin/products')
    return render_template('admin/products.html', products=prods, form=form)

@app.route('/admin/products/update/<int:product_id>', methods = ['GET', 'POST'])
def admin_product_update(product_id):
    # TODO: fix update
    prod_to_upd = p_dao.get(product_id)
    cats = cat_dao.get_all()
    form = UpdateProductForm()
    
    form.category.choices = [(cat.id, cat.title) for cat in cats or []]
    
    form.title.data = prod_to_upd.title
    form.price.data = prod_to_upd.price
    # form.category.data = prod_to_upd.category_id
    form.amount.data = prod_to_upd.amount_in_stock
    if form.validate_on_submit():
        
        prod = Product(
            id=-1,
            title=form.title.data,
            price=form.price.data,
            category_id=form.category.data,
            amount_in_stock=form.amount.data,
        )
        p_dao.update(product_id, prod)
        return redirect('/admin/products')
    else:
        print(form.errors)
    return render_template('admin/update.html', form=form, product_id=product_id)


@app.route('/admin/customers')
def admin_customers():
    return render_template('admin/customers.html')


if __name__ == '__main__':
    app.run(debug=True)



# TODO: mysqldaos impl
# TODO: order proc
# TODO: order impl
# TODO: other views